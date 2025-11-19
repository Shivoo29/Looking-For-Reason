from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.database import get_db
from app.models import User, Application, Resume, JobDescription
from app.schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.api.v1.endpoints.auth import get_current_user
from app.services.jd_parser import JobDescriptionParser

router = APIRouter()
jd_parser = JobDescriptionParser()


@router.get("/", response_model=List[ApplicationResponse])
def list_applications(
    status: Optional[str] = None,
    limit: int = Query(100, le=1000),
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List applications with optional filtering"""
    query = db.query(Application).filter(Application.user_id == current_user.id)

    if status:
        query = query.filter(Application.status == status)

    applications = query.order_by(Application.created_at.desc()).offset(offset).limit(limit).all()
    return applications


@router.post("/", response_model=ApplicationResponse)
def create_application(
    app_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new job application"""

    # Verify resume exists
    resume = db.query(Resume).filter(
        Resume.id == app_data.resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    # Verify job description exists
    jd = db.query(JobDescription).filter(
        JobDescription.id == app_data.job_description_id,
        JobDescription.user_id == current_user.id
    ).first()

    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    # Calculate match score
    match_score = jd_parser.extract_match_score(resume.raw_text, jd.parsed_data)

    # Create application
    application = Application(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        resume_id=app_data.resume_id,
        job_description_id=app_data.job_description_id,
        company=app_data.company,
        position=app_data.position,
        url=app_data.url,
        match_score=match_score,
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get application by ID"""
    app = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    return app


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: str,
    app_data: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update application"""
    app = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    # Update fields
    if app_data.status:
        app.status = app_data.status
        if app_data.status == 'applied' and not app.applied_at:
            app.applied_at = datetime.utcnow()

    if app_data.notes is not None:
        app.notes = app_data.notes

    if app_data.next_steps is not None:
        app.next_steps = app_data.next_steps

    db.commit()
    db.refresh(app)

    return app


@router.delete("/{application_id}")
def delete_application(
    application_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete application"""
    app = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    db.delete(app)
    db.commit()

    return {"message": "Application deleted successfully"}


@router.post("/{application_id}/notes")
def add_note(
    application_id: str,
    note: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add note to application"""
    app = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    if not app.notes:
        app.notes = []

    app.notes.append(note)
    db.commit()

    return {"message": "Note added successfully", "notes": app.notes}
