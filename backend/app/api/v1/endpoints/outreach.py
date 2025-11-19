from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from app.database import get_db
from app.models import User, OutreachMessage, Application
from app.schemas import OutreachCreate, OutreachResponse
from app.api.v1.endpoints.auth import get_current_user
from app.services.outreach_generator import OutreachGenerator

router = APIRouter()
outreach_gen = OutreachGenerator()


@router.post("/generate")
def generate_outreach(
    outreach_data: OutreachCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized outreach message"""

    # Verify application exists
    app = db.query(Application).filter(
        Application.id == outreach_data.application_id,
        Application.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    # Get resume summary
    resume_summary = f"Professional with experience in {', '.join(app.resume.parsed_data.get('skills', [])[:5])}"
    job_keywords = app.job_description.keywords or []

    try:
        # Generate message based on type
        if outreach_data.message_type == 'email':
            result = outreach_gen.generate_email(
                outreach_data.contact_name,
                outreach_data.contact_title,
                app.company,
                app.position,
                resume_summary,
                job_keywords
            )
            subject = result['subject']
            body = result['body']
        else:  # LinkedIn
            body = outreach_gen.generate_linkedin_message(
                outreach_data.contact_name,
                outreach_data.contact_title,
                app.company,
                app.position,
                resume_summary
            )
            subject = None

        # Create outreach message record
        outreach = OutreachMessage(
            id=str(uuid.uuid4()),
            application_id=outreach_data.application_id,
            contact_name=outreach_data.contact_name,
            contact_title=outreach_data.contact_title,
            contact_email=outreach_data.contact_email,
            contact_linkedin=outreach_data.contact_linkedin,
            message_type=outreach_data.message_type,
            subject=subject,
            body=body,
        )

        db.add(outreach)
        db.commit()
        db.refresh(outreach)

        return outreach

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating outreach: {str(e)}"
        )


@router.get("/{application_id}", response_model=List[OutreachResponse])
def list_outreach_messages(
    application_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List outreach messages for an application"""

    # Verify application exists
    app = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()

    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    messages = db.query(OutreachMessage).filter(
        OutreachMessage.application_id == application_id
    ).all()

    return messages


@router.post("/{outreach_id}/send")
def send_outreach(
    outreach_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark outreach as sent (actual sending would be handled separately)"""

    outreach = db.query(OutreachMessage).join(Application).filter(
        OutreachMessage.id == outreach_id,
        Application.user_id == current_user.id
    ).first()

    if not outreach:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outreach message not found")

    outreach.status = 'sent'
    outreach.sent_at = datetime.utcnow()
    db.commit()

    return {"message": "Outreach marked as sent", "outreach_id": outreach_id}
