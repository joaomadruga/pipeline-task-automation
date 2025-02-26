from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field


class SentimentAnalysisToolInput(BaseModel):
    """Input schema for SentimentAnalysisTool."""
    emails: List[dict] = Field(..., description="List of emails to analyze.")

class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = (
        "Analyzes the tone and sentiment of provided emails to determine urgency and required actions."
    )
    args_schema: Type[BaseModel] = SentimentAnalysisToolInput

    def _run(self, emails: List[dict]) -> List[dict]:
        # Mocked result to simulate sentiment analysis
        return [
            {
                "email_id": "123",
                "sentiment": "neutral"
            },
            {
                "email_id": "124",
                "sentiment": "positive"
            }
        ]
