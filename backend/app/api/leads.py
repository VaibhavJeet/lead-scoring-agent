"""Lead API endpoints."""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.lead import Lead, LeadCreate, LeadResponse, LeadStatus, LeadSource
from app.agents.lead_scorer import LeadScorerAgent
from app.agents.enrichment_agent import EnrichmentAgent
from app.agents.intent_analyzer import IntentAnalyzerAgent

router = APIRouter()


@router.post("", response_model=LeadResponse)
async def create_lead(lead_data: LeadCreate, db: AsyncSession = Depends(get_db)):
    """Create a new lead."""
    # Check for duplicate
    existing = await db.execute(select(Lead).where(Lead.email == lead_data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "Lead with this email already exists")

    lead = Lead(
        email=lead_data.email,
        first_name=lead_data.first_name,
        last_name=lead_data.last_name,
        company=lead_data.company,
        job_title=lead_data.job_title,
        phone=lead_data.phone,
        website=lead_data.website,
        linkedin_url=lead_data.linkedin_url,
        source=lead_data.source,
        tags=lead_data.tags,
        notes=lead_data.notes
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


@router.get("", response_model=List[LeadResponse])
async def list_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[LeadStatus] = None,
    source: Optional[LeadSource] = None,
    tier: Optional[str] = None,
    min_score: Optional[float] = None,
    db: AsyncSession = Depends(get_db)
):
    """List leads with optional filtering."""
    query = select(Lead).order_by(Lead.score.desc())

    if status:
        query = query.where(Lead.status == status)
    if source:
        query = query.where(Lead.source == source)
    if tier:
        query = query.where(Lead.score_tier == tier)
    if min_score is not None:
        query = query.where(Lead.score >= min_score)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    """Get lead details."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(404, "Lead not found")
    return lead


@router.post("/{lead_id}/score", response_model=LeadResponse)
async def score_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    """Score a lead using AI."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(404, "Lead not found")

    scorer = LeadScorerAgent()
    score_result = await scorer.score(
        email=lead.email,
        first_name=lead.first_name or "",
        last_name=lead.last_name or "",
        job_title=lead.job_title or "",
        company=lead.company or "",
        source=lead.source.value if lead.source else "",
        enrichment_data=lead.enrichment_data,
        intent_signals=lead.intent_signals
    )

    lead.score = score_result.overall_score
    lead.score_tier = score_result.tier
    lead.score_breakdown = {
        "firmographic": score_result.firmographic_score,
        "behavioral": score_result.behavioral_score,
        "engagement": score_result.engagement_score,
        "fit": score_result.fit_score,
        "reasoning": score_result.reasoning,
        "recommendations": score_result.recommendations
    }
    lead.last_scored_at = datetime.utcnow()

    await db.commit()
    await db.refresh(lead)
    return lead


@router.post("/{lead_id}/enrich", response_model=LeadResponse)
async def enrich_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    """Enrich lead data using AI."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(404, "Lead not found")

    enricher = EnrichmentAgent()
    enrichment = await enricher.enrich(
        email=lead.email,
        first_name=lead.first_name or "",
        last_name=lead.last_name or "",
        company=lead.company or "",
        job_title=lead.job_title or "",
        website=lead.website or "",
        linkedin_url=lead.linkedin_url or ""
    )

    lead.enrichment_data = enrichment.model_dump()
    lead.enriched_at = datetime.utcnow()

    await db.commit()
    await db.refresh(lead)
    return lead


@router.post("/{lead_id}/analyze-intent", response_model=LeadResponse)
async def analyze_lead_intent(
    lead_id: str,
    behavior_data: List[dict] = [],
    engagement_history: List[dict] = [],
    db: AsyncSession = Depends(get_db)
):
    """Analyze lead intent."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(404, "Lead not found")

    analyzer = IntentAnalyzerAgent()
    intent_result = await analyzer.analyze(
        lead_info={
            "email": lead.email,
            "company": lead.company,
            "job_title": lead.job_title,
            "source": lead.source.value if lead.source else None
        },
        behavior_data=behavior_data,
        engagement_history=engagement_history
    )

    lead.intent_signals = [s.model_dump() for s in intent_result.signals]
    lead.intent_score = intent_result.overall_intent_score

    await db.commit()
    await db.refresh(lead)
    return lead


@router.patch("/{lead_id}/status", response_model=LeadResponse)
async def update_lead_status(
    lead_id: str,
    status: LeadStatus,
    db: AsyncSession = Depends(get_db)
):
    """Update lead status."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(404, "Lead not found")

    lead.status = status
    await db.commit()
    await db.refresh(lead)
    return lead


@router.delete("/{lead_id}")
async def delete_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a lead."""
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(404, "Lead not found")

    await db.delete(lead)
    await db.commit()
    return {"message": "Lead deleted successfully"}
