"""Lead scoring agent."""

from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from app.core.llm import get_llm
from app.models.lead import LeadScore


class LeadScorerAgent:
    """Agent for scoring leads based on multiple factors."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=LeadScore)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert sales lead analyst. Score the provided lead based on:

1. **Firmographic Score (0-100)**: Company size, industry fit, revenue potential
2. **Behavioral Score (0-100)**: Website visits, content downloads, email engagement
3. **Engagement Score (0-100)**: Response rate, meeting attendance, interaction frequency
4. **Fit Score (0-100)**: Job title relevance, decision-making authority, budget control

Calculate overall_score as weighted average:
- Firmographic: 25%
- Behavioral: 30%
- Engagement: 25%
- Fit: 20%

Assign tier:
- hot: score >= 70
- warm: score 40-69
- cold: score < 40

Provide reasoning and actionable recommendations.

{format_instructions}"""),
            ("human", """Score this lead:

Contact Info:
- Email: {email}
- Name: {first_name} {last_name}
- Job Title: {job_title}
- Company: {company}
- Source: {source}

Enrichment Data:
{enrichment_data}

Intent Signals:
{intent_signals}

Additional Context:
{additional_context}""")
        ])

    async def score(
        self,
        email: str,
        first_name: str = "",
        last_name: str = "",
        job_title: str = "",
        company: str = "",
        source: str = "",
        enrichment_data: dict = None,
        intent_signals: list = None,
        additional_context: str = ""
    ) -> LeadScore:
        """Score a lead."""
        chain = self.prompt | self.llm | self.parser

        result = await chain.ainvoke({
            "email": email,
            "first_name": first_name or "Unknown",
            "last_name": last_name or "",
            "job_title": job_title or "Unknown",
            "company": company or "Unknown",
            "source": source or "Unknown",
            "enrichment_data": str(enrichment_data or {}),
            "intent_signals": str(intent_signals or []),
            "additional_context": additional_context or "No additional context",
            "format_instructions": self.parser.get_format_instructions()
        })

        tier = result.get("tier", "cold")
        if tier not in ["hot", "warm", "cold"]:
            score = result.get("overall_score", 0)
            tier = "hot" if score >= 70 else "warm" if score >= 40 else "cold"

        return LeadScore(
            overall_score=min(100, max(0, result.get("overall_score", 0))),
            tier=tier,
            firmographic_score=min(100, max(0, result.get("firmographic_score", 0))),
            behavioral_score=min(100, max(0, result.get("behavioral_score", 0))),
            engagement_score=min(100, max(0, result.get("engagement_score", 0))),
            fit_score=min(100, max(0, result.get("fit_score", 0))),
            reasoning=result.get("reasoning", ""),
            recommendations=result.get("recommendations", [])
        )
