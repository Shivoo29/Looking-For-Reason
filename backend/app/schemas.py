from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    TEAM = "team"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class OutreachStatus(str, Enum):
    DRAFT = "draft"
    SENT = "sent"
    OPENED = "opened"
    REPLIED = "replied"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    avatar_url: Optional[str] = None
    subscription_tier: SubscriptionTier
    subscription_status: SubscriptionStatus
    created_at: datetime

    class Config:
        from_attributes = True


# Resume Schemas
class ResumeCreate(BaseModel):
    name: str
    file_name: str


class ResumeResponse(BaseModel):
    id: str
    user_id: str
    name: str
    file_name: str
    file_url: str
    ats_score: float
    parsed_data: Optional[Dict[str, Any]] = None
    ats_feedback: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ATSScoreResponse(BaseModel):
    score: float
    feedback: Dict[str, Any]
    missing_keywords: List[str]
    suggestions: List[str]


# Job Description Schemas
class JobDescriptionCreate(BaseModel):
    title: str
    company: str
    url: Optional[str] = None
    text: Optional[str] = None


class JobDescriptionResponse(BaseModel):
    id: str
    user_id: str
    title: str
    company: str
    url: Optional[str] = None
    raw_text: str
    keywords: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    location: Optional[str] = None
    remote_friendly: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# Application Schemas
class ApplicationCreate(BaseModel):
    job_description_id: str
    resume_id: str
    company: str
    position: str
    url: Optional[str] = None


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[List[str]] = None
    next_steps: Optional[List[str]] = None


class ApplicationResponse(BaseModel):
    id: str
    user_id: str
    resume_id: str
    job_description_id: str
    company: str
    position: str
    url: Optional[str] = None
    status: ApplicationStatus
    match_score: float
    notes: List[str] = []
    next_steps: List[str] = []
    applied_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Outreach Schemas
class OutreachCreate(BaseModel):
    application_id: str
    contact_name: str
    contact_title: str
    contact_email: Optional[str] = None
    contact_linkedin: Optional[str] = None
    message_type: str  # 'email' or 'linkedin'


class OutreachResponse(BaseModel):
    id: str
    application_id: str
    contact_name: str
    contact_title: str
    contact_email: Optional[str] = None
    contact_linkedin: Optional[str] = None
    message_type: str
    subject: Optional[str] = None
    body: str
    status: OutreachStatus
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Analytics Schemas
class AnalyticsOverview(BaseModel):
    total_applications: int
    active_applications: int
    interviews: int
    response_rate: float
    avg_ats_score: float


class ApplicationStats(BaseModel):
    status: str
    count: int
    percentage: float


# Organization Graph Schemas
class ContactResponse(BaseModel):
    id: str
    company: str
    name: str
    title: str
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    department: Optional[str] = None
    seniority_level: Optional[str] = None
    is_decision_maker: bool

    class Config:
        from_attributes = True


# Optimization Schemas
class OptimizationRequest(BaseModel):
    resume_id: str
    job_description_id: str


class OptimizationResponse(BaseModel):
    optimized_resume_url: str
    improvements: List[str]
    before_score: float
    after_score: float
    keyword_additions: List[str]


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
