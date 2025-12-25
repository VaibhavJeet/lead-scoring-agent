"""Scoring API endpoints."""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.models.lead import Lead, LeadResponse
from app.agents.lead_scorer import LeadScorerAgent

router = APIRouter()


class BatchScoreRequest(BaseModel):
    lead_ids: List[str]


class BatchScoreResult(BaseModel):
    scored: int
    failed: int
    leads: List[LeadResponse]


@router.post("/batch", response_model=BatchScoreResult)
async def batch_score_leads(
    request: BatchScoreRequest,
    db: AsyncSession = Depends(get_db)
):
    """Batch score multiple leads."""
    scorer = LeadScorerAgent()
    scored_leads = []
    failed_count = 0

    for lead_id in request.lead_ids:
        result = await db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        
        if not lead:
            failed_count += 1
            continue

        try:
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
            scored_leads.append(lead)
        except Exception:
            failed_count += 1

    await db.commit()

    return BatchScoreResult(
        scored=len(scored_leads),
        failed=failed_count,
        leads=[LeadResponse.model_validate(l) for l in scored_leads]
    )


@router.get("/tiers")
async def get_leads_by_tier(db: AsyncSession = Depends(get_db)):
    """Get lead counts by tier."""
    result = await db.execute(select(Lead))
    leads = result.scalars().all()

    tiers = {"hot": 0, "warm": 0, "cold": 0, "unscored": 0}
    for lead in leads:
        if lead.score_tier:
            tiers[lead.score_tier] = tiers.get(lead.score_tier, 0) + 1
        else:
            tiers["unscored"] += 1

    return tiers
