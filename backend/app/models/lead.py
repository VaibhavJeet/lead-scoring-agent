"""Lead models."""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, String, DateTime, Text, JSON, Float, Integer, Enum as SQLEnum
import uuid

from app.core.database import Base


class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"


class LeadSource(str, Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    LINKEDIN = "linkedin"
    COLD_OUTREACH = "cold_outreach"
    EVENT = "event"
    ADVERTISING = "advertising"
    OTHER = "other"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    company = Column(String)
    job_title = Column(String)
    phone = Column(String)
    website = Column(String)
    linkedin_url = Column(String)
    source = Column(SQLEnum(LeadSource), default=LeadSource.WEBSITE)
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW)
    
    # Scoring
    score = Column(Float, default=0.0)
    score_breakdown = Column(JSON, default=dict)
    score_tier = Column(String)  # hot, warm, cold
    last_scored_at = Column(DateTime)
    
    # Enrichment
    enrichment_data = Column(JSON, default=dict)
    enriched_at = Column(DateTime)
    
    # Intent signals
    intent_signals = Column(JSON, default=list)
    intent_score = Column(Float, default=0.0)
    
    # Metadata
    tags = Column(JSON, default=list)
    notes = Column(Text)
    assigned_to = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LeadCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: LeadSource = LeadSource.WEBSITE
    tags: List[str] = []
    notes: Optional[str] = None


class LeadScore(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    tier: str  # hot, warm, cold
    firmographic_score: float = Field(ge=0, le=100)
    behavioral_score: float = Field(ge=0, le=100)
    engagement_score: float = Field(ge=0, le=100)
    fit_score: float = Field(ge=0, le=100)
    reasoning: str
    recommendations: List[str] = []


class LeadResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    source: LeadSource
    status: LeadStatus
    score: float
    score_breakdown: dict = {}
    score_tier: Optional[str] = None
    enrichment_data: dict = {}
    intent_signals: List[dict] = []
    intent_score: float = 0.0
    tags: List[str] = []
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
