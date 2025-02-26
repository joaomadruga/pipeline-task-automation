from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field


class FAQLookupToolInput(BaseModel):
    """Input schema for FAQLookupTool."""
    email_ids: List[str] = Field(..., description="List of email IDs for which to find answers.")

class FAQLookupTool(BaseTool):
    name: str = "FAQ Lookup Tool"
    description: str = (
        "Attempts to find relevant answers from a knowledge base for the provided email IDs."
    )
    args_schema: Type[BaseModel] = FAQLookupToolInput

    def _run(self, email_ids: List[str]) -> List[dict]:
        # Mocked result to simulate FAQ lookup
        return [
            {
                "email_id": "123",
                "response": "Please allow 3-5 business days for your order to arrive."
            },
            {
                "email_id": "124",
                "response": "Your subscription will renew on the 15th of next month."
            }
        ]
