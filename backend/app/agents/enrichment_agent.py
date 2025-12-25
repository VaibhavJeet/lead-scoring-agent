"""Lead enrichment agent."""

from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from app.core.llm import get_llm
from app.models.enrichment import EnrichmentData, CompanyData, ContactData


class EnrichmentAgent:
    """Agent for enriching lead data."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=EnrichmentData)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a data enrichment specialist. Based on the provided lead information and any available data, infer and enrich the lead profile.

For company data, estimate:
- Industry based on domain/company name
- Employee range (1-10, 11-50, 51-200, 201-500, 501-1000, 1000+)
- Location based on any available signals
- Likely technologies used

For contact data, infer:
- Seniority level (entry, mid, senior, executive, c-level)
- Department (sales, marketing, engineering, product, operations, hr, finance, executive)
- Decision-making authority

Be conservative with estimates. Mark as null if insufficient data.

{format_instructions}"""),
            ("human", """Enrich this lead:

Email: {email}
Name: {first_name} {last_name}
Company: {company}
Job Title: {job_title}
Website: {website}
LinkedIn: {linkedin_url}

Additional Data:
{additional_data}""")
        ])

    async def enrich(
        self,
        email: str,
        first_name: str = "",
        last_name: str = "",
        company: str = "",
        job_title: str = "",
        website: str = "",
        linkedin_url: str = "",
        additional_data: dict = None
    ) -> EnrichmentData:
        """Enrich lead data."""
        chain = self.prompt | self.llm | self.parser

        result = await chain.ainvoke({
            "email": email,
            "first_name": first_name or "",
            "last_name": last_name or "",
            "company": company or "",
            "job_title": job_title or "",
            "website": website or "",
            "linkedin_url": linkedin_url or "",
            "additional_data": str(additional_data or {}),
            "format_instructions": self.parser.get_format_instructions()
        })

        company_data = None
        if result.get("company"):
            company_data = CompanyData(**result["company"])

        contact_data = None
        if result.get("contact"):
            contact_data = ContactData(**result["contact"])

        return EnrichmentData(
            company=company_data,
            contact=contact_data,
            source="ai_enrichment"
        )
