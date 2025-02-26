from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field


class EmailIngestionToolInput(BaseModel):
    """Input schema for EmailIngestionTool."""
    inbox_source: str = Field(..., description="Source of the emails to fetch.")

class EmailIngestionTool(BaseTool):
    name: str = "Email Ingestion Tool"
    description: str = (
        "Fetches new emails from the specified inbox source, extracts relevant text, "
        "and formats data for further processing."
    )
    args_schema: Type[BaseModel] = EmailIngestionToolInput

    def _run(self, inbox_source: str) -> List[dict]:
        # Mocked result to simulate fetching emails
        return [
            {
                "id": "123",
                "subject": "Need help with my order",
                "body": "Hi, I placed an order last week, but it hasn't arrived yet. Can you help me track it?"
            },
            {
                "id": "124",
                "subject": "Question about my subscription",
                "body": "Hello, I have a question about my subscription renewal. Can you provide more details?"
            }
        ]
