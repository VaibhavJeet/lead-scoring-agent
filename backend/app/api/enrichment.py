"""Enrichment API endpoints."""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.core.database import get_db
from app.models.lead import Lead, LeadResponse
from app.agents.enrichment_agent import EnrichmentAgent

router = APIRouter()


class BatchEnrichRequest(BaseModel):
    lead_ids: List[str]


@router.post("/batch")
async def batch_enrich_leads(
    request: BatchEnrichRequest,
    db: AsyncSession = Depends(get_db)
):
    """Batch enrich multiple leads."""
    enricher = EnrichmentAgent()
    enriched_count = 0
    failed_count = 0

    for lead_id in request.lead_ids:
        result = await db.execute(select(Lead).where(Lead.id == lead_id))
        lead = result.scalar_one_or_none()
        
        if not lead:
            failed_count += 1
            continue

        try:
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
            enriched_count += 1
        except Exception:
            failed_count += 1

    await db.commit()

    return {
        "enriched": enriched_count,
        "failed": failed_count
    }
