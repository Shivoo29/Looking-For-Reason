from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UsageMetric
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/")
def get_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current subscription details"""
    return {
        'tier': current_user.subscription_tier,
        'status': current_user.subscription_status,
        'stripe_customer_id': current_user.stripe_customer_id,
    }


@router.get("/usage")
def get_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get usage metrics for current billing period"""

    # Count applications this month
    from sqlalchemy import extract, func
    from datetime import datetime
    from app.models import Application

    current_month = datetime.now().month
    current_year = datetime.now().year

    applications_count = db.query(func.count(Application.id)).filter(
        Application.user_id == current_user.id,
        extract('month', Application.created_at) == current_month,
        extract('year', Application.created_at) == current_year
    ).scalar() or 0

    # Limits based on tier
    limits = {
        'free': {'applications': 5, 'resumes': 1},
        'pro': {'applications': -1, 'resumes': -1},  # Unlimited
        'team': {'applications': -1, 'resumes': -1},
        'enterprise': {'applications': -1, 'resumes': -1},
    }

    tier_limits = limits.get(current_user.subscription_tier, limits['free'])

    return {
        'applications_used': applications_count,
        'applications_limit': tier_limits['applications'],
        'can_create_application': (
            tier_limits['applications'] == -1 or
            applications_count < tier_limits['applications']
        ),
    }


@router.post("/cancel")
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel subscription"""

    if current_user.subscription_tier == 'free':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Free tier cannot be canceled"
        )

    current_user.subscription_status = 'canceled'
    db.commit()

    return {"message": "Subscription canceled successfully"}
