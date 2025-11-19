from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models import User, Application, Resume, OutreachMessage
from app.schemas import AnalyticsOverview, ApplicationStats
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
def get_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics overview"""

    # Total applications
    total_applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).count()

    # Active applications (pending, applied, screening, interview)
    active_applications = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status.in_(['pending', 'applied', 'screening', 'interview'])
    ).count()

    # Interviews
    interviews = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status == 'interview'
    ).count()

    # Response rate (applied that got a response)
    applied_count = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status.in_(['applied', 'screening', 'interview', 'offer', 'accepted'])
    ).count()

    responded_count = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.status.in_(['screening', 'interview', 'offer', 'accepted'])
    ).count()

    response_rate = (responded_count / applied_count * 100) if applied_count > 0 else 0

    # Average ATS score
    avg_ats = db.query(func.avg(Resume.ats_score)).filter(
        Resume.user_id == current_user.id
    ).scalar() or 0

    return {
        'total_applications': total_applications,
        'active_applications': active_applications,
        'interviews': interviews,
        'response_rate': round(response_rate, 1),
        'avg_ats_score': round(avg_ats, 1),
    }


@router.get("/applications", response_model=List[ApplicationStats])
def get_application_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get application statistics by status"""

    total = db.query(Application).filter(Application.user_id == current_user.id).count()

    if total == 0:
        return []

    stats = db.query(
        Application.status,
        func.count(Application.id).label('count')
    ).filter(
        Application.user_id == current_user.id
    ).group_by(Application.status).all()

    return [
        {
            'status': stat.status,
            'count': stat.count,
            'percentage': round((stat.count / total) * 100, 1)
        }
        for stat in stats
    ]


@router.get("/resumes")
def get_resume_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get resume performance metrics"""

    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()

    return [
        {
            'resume_id': resume.id,
            'resume_name': resume.name,
            'ats_score': resume.ats_score,
            'applications_count': db.query(Application).filter(
                Application.resume_id == resume.id
            ).count(),
        }
        for resume in resumes
    ]


@router.get("/outreach")
def get_outreach_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get outreach statistics"""

    total_outreach = db.query(OutreachMessage).join(Application).filter(
        Application.user_id == current_user.id
    ).count()

    sent = db.query(OutreachMessage).join(Application).filter(
        Application.user_id == current_user.id,
        OutreachMessage.status.in_(['sent', 'opened', 'replied'])
    ).count()

    replied = db.query(OutreachMessage).join(Application).filter(
        Application.user_id == current_user.id,
        OutreachMessage.status == 'replied'
    ).count()

    reply_rate = (replied / sent * 100) if sent > 0 else 0

    return {
        'total_outreach': total_outreach,
        'sent': sent,
        'replied': replied,
        'reply_rate': round(reply_rate, 1),
    }
