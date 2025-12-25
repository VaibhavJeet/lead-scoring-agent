"""Enrichment data models."""

from typing import Optional, List
from pydantic import BaseModel


class CompanyData(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    employee_count: Optional[int] = None
    employee_range: Optional[str] = None
    revenue_range: Optional[str] = None
    founded_year: Optional[int] = None
    location: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    technologies: List[str] = []
    funding_total: Optional[str] = None
    funding_stage: Optional[str] = None


class ContactData(BaseModel):
    full_name: Optional[str] = None
    email_verified: bool = False
    job_title: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    linkedin_url: Optional[str] = None
    twitter_url: Optional[str] = None
    location: Optional[str] = None
    bio: Optional[str] = None


class EnrichmentData(BaseModel):
    company: Optional[CompanyData] = None
    contact: Optional[ContactData] = None
    enriched_at: Optional[str] = None
    source: Optional[str] = None
