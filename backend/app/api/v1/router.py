from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    resumes,
    job_descriptions,
    applications,
    outreach,
    analytics,
    subscription,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(job_descriptions.router, prefix="/job-descriptions", tags=["job-descriptions"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(outreach.router, prefix="/outreach", tags=["outreach"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(subscription.router, prefix="/subscription", tags=["subscription"])
