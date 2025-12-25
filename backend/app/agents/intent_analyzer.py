"""Intent analysis agent."""

from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.core.llm import get_llm


class IntentSignal(BaseModel):
    signal_type: str
    description: str
    strength: float = Field(ge=0, le=1)
    buying_stage: str  # awareness, consideration, decision


class IntentAnalysisResult(BaseModel):
    signals: List[IntentSignal]
    overall_intent_score: float = Field(ge=0, le=1)
    buying_stage: str
    recommended_action: str
    urgency: str  # low, medium, high


class IntentAnalyzerAgent:
    """Agent for analyzing lead intent signals."""

    def __init__(self):
        self.llm = get_llm()
        self.parser = JsonOutputParser(pydantic_object=IntentAnalysisResult)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an intent analysis expert. Analyze the provided lead behavior and signals to determine buying intent.

Identify intent signals such as:
- Website behavior (pricing page visits, demo requests, feature comparisons)
- Email engagement (opens, clicks, replies)
- Content consumption (whitepapers, case studies, product docs)
- Direct actions (form submissions, meeting bookings)
- Social signals (LinkedIn engagement, social mentions)

Determine:
1. Individual signal strength (0-1)
2. Buying stage: awareness, consideration, decision
3. Overall intent score (0-1)
4. Recommended sales action
5. Urgency level: low, medium, high

{format_instructions}"""),
            ("human", """Analyze intent for this lead:

Lead Info:
{lead_info}

Behavior Data:
{behavior_data}

Engagement History:
{engagement_history}""")
        ])

    async def analyze(
        self,
        lead_info: dict,
        behavior_data: list = None,
        engagement_history: list = None
    ) -> IntentAnalysisResult:
        """Analyze lead intent."""
        chain = self.prompt | self.llm | self.parser

        result = await chain.ainvoke({
            "lead_info": str(lead_info),
            "behavior_data": str(behavior_data or []),
            "engagement_history": str(engagement_history or []),
            "format_instructions": self.parser.get_format_instructions()
        })

        signals = []
        for signal_data in result.get("signals", []):
            try:
                signals.append(IntentSignal(
                    signal_type=signal_data.get("signal_type", "unknown"),
                    description=signal_data.get("description", ""),
                    strength=min(1, max(0, signal_data.get("strength", 0))),
                    buying_stage=signal_data.get("buying_stage", "awareness")
                ))
            except:
                continue

        return IntentAnalysisResult(
            signals=signals,
            overall_intent_score=min(1, max(0, result.get("overall_intent_score", 0))),
            buying_stage=result.get("buying_stage", "awareness"),
            recommended_action=result.get("recommended_action", ""),
            urgency=result.get("urgency", "low")
        )
