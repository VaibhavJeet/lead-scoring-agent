"""Analytics API endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.lead import Lead, LeadStatus, LeadSource

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Get dashboard statistics."""
    total_leads = await db.execute(select(func.count(Lead.id)))
    total = total_leads.scalar() or 0

    hot_leads = await db.execute(
        select(func.count(Lead.id)).where(Lead.score_tier == "hot")
    )
    hot = hot_leads.scalar() or 0

    warm_leads = await db.execute(
        select(func.count(Lead.id)).where(Lead.score_tier == "warm")
    )
    warm = warm_leads.scalar() or 0

    avg_score = await db.execute(
        select(func.avg(Lead.score)).where(Lead.score > 0)
    )
    avg = avg_score.scalar() or 0

    enriched = await db.execute(
        select(func.count(Lead.id)).where(Lead.enriched_at.isnot(None))
    )
    enriched_count = enriched.scalar() or 0

    return {
        "total_leads": total,
        "hot_leads": hot,
        "warm_leads": warm,
        "cold_leads": total - hot - warm,
        "average_score": round(avg, 1),
        "enriched_leads": enriched_count,
        "enrichment_rate": round((enriched_count / total * 100) if total > 0 else 0, 1)
    }


@router.get("")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    """Get comprehensive analytics."""
    # Leads by source
    by_source = await db.execute(
        select(Lead.source, func.count(Lead.id).label("count"))
        .group_by(Lead.source)
    )
    source_data = [{"source": r[0].value if r[0] else "unknown", "count": r[1]} for r in by_source.all()]

    # Leads by status
    by_status = await db.execute(
        select(Lead.status, func.count(Lead.id).label("count"))
        .group_by(Lead.status)
    )
    status_data = [{"status": r[0].value if r[0] else "unknown", "count": r[1]} for r in by_status.all()]

    # Score distribution
    score_ranges = [
        ("0-20", 0, 20),
        ("21-40", 21, 40),
        ("41-60", 41, 60),
        ("61-80", 61, 80),
        ("81-100", 81, 100)
    ]
    score_dist = []
    for label, min_s, max_s in score_ranges:
        count = await db.execute(
            select(func.count(Lead.id)).where(Lead.score >= min_s, Lead.score <= max_s)
        )
        score_dist.append({"range": label, "count": count.scalar() or 0})

    return {
        "leads_by_source": source_data,
        "leads_by_status": status_data,
        "score_distribution": score_dist
    }
