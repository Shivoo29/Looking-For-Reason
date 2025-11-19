from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app.models import User, JobDescription
from app.schemas import JobDescriptionCreate, JobDescriptionResponse
from app.api.v1.endpoints.auth import get_current_user
from app.services.jd_parser import JobDescriptionParser

router = APIRouter()
jd_parser = JobDescriptionParser()


@router.get("/", response_model=List[JobDescriptionResponse])
def list_job_descriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all job descriptions"""
    jds = db.query(JobDescription).filter(JobDescription.user_id == current_user.id).all()
    return jds


@router.post("/", response_model=JobDescriptionResponse)
def create_job_description(
    jd_data: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create and parse a job description"""

    if not jd_data.text and not jd_data.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either text or url must be provided"
        )

    # Parse JD
    try:
        jd_text = jd_data.text or f"Job URL: {jd_data.url}"
        parsed_data = jd_parser.parse(jd_text)

        # Create JD record
        jd = JobDescription(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            title=jd_data.title,
            company=jd_data.company,
            url=jd_data.url,
            raw_text=jd_text,
            parsed_data=parsed_data,
            keywords=parsed_data.get('keywords', []),
            required_skills=parsed_data.get('required_skills', []),
            preferred_skills=parsed_data.get('preferred_skills', []),
            experience_years=parsed_data.get('experience_years'),
            location=parsed_data.get('location'),
            remote_friendly=parsed_data.get('remote_friendly', False),
        )

        db.add(jd)
        db.commit()
        db.refresh(jd)

        return jd

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error parsing job description: {str(e)}"
        )


@router.get("/{jd_id}", response_model=JobDescriptionResponse)
def get_job_description(
    jd_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get job description by ID"""
    jd = db.query(JobDescription).filter(
        JobDescription.id == jd_id,
        JobDescription.user_id == current_user.id
    ).first()

    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    return jd


@router.delete("/{jd_id}")
def delete_job_description(
    jd_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete job description"""
    jd = db.query(JobDescription).filter(
        JobDescription.id == jd_id,
        JobDescription.user_id == current_user.id
    ).first()

    if not jd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")

    db.delete(jd)
    db.commit()

    return {"message": "Job description deleted successfully"}
