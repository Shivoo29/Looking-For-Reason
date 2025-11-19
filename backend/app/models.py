from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.database import Base


class SubscriptionTier(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    TEAM = "team"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"


class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    APPLIED = "applied"
    SCREENING = "screening"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class OutreachStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    OPENED = "opened"
    REPLIED = "replied"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    avatar_url = Column(String, nullable=True)
    subscription_tier = Column(Enum(SubscriptionTier), default=SubscriptionTier.FREE)
    subscription_status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship("JobDescription", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    raw_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)
    ats_score = Column(Float, default=0.0)
    ats_feedback = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    url = Column(String, nullable=True)
    raw_text = Column(Text, nullable=False)
    parsed_data = Column(JSON, nullable=True)
    keywords = Column(JSON, nullable=True)  # List of keywords
    required_skills = Column(JSON, nullable=True)  # List of required skills
    preferred_skills = Column(JSON, nullable=True)  # List of preferred skills
    experience_years = Column(Integer, nullable=True)
    education_level = Column(String, nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    remote_friendly = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    applications = relationship("Application", back_populates="job_description")


class Application(Base):
    __tablename__ = "applications"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(String, ForeignKey("job_descriptions.id"), nullable=False)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    url = Column(String, nullable=True)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    optimized_resume_url = Column(String, nullable=True)
    match_score = Column(Float, default=0.0)
    notes = Column(JSON, default=[])  # List of notes
    next_steps = Column(JSON, default=[])  # List of next steps
    applied_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
    job_description = relationship("JobDescription", back_populates="applications")
    outreach_messages = relationship("OutreachMessage", back_populates="application", cascade="all, delete-orphan")


class OutreachMessage(Base):
    __tablename__ = "outreach_messages"

    id = Column(String, primary_key=True, index=True)
    application_id = Column(String, ForeignKey("applications.id"), nullable=False)
    contact_name = Column(String, nullable=False)
    contact_title = Column(String, nullable=False)
    contact_email = Column(String, nullable=True)
    contact_linkedin = Column(String, nullable=True)
    message_type = Column(String, nullable=False)  # 'email' or 'linkedin'
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    status = Column(Enum(OutreachStatus), default=OutreachStatus.DRAFT)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    replied_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    application = relationship("Application", back_populates="outreach_messages")


class OrganizationContact(Base):
    __tablename__ = "organization_contacts"

    id = Column(String, primary_key=True, index=True)
    company = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    email = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    department = Column(String, nullable=True)
    seniority_level = Column(String, nullable=True)
    is_decision_maker = Column(Boolean, default=False)
    profile_data = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UsageMetric(Base):
    __tablename__ = "usage_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    metric_type = Column(String, nullable=False)  # 'application', 'resume_optimization', 'outreach', etc.
    metric_value = Column(Integer, default=1)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
