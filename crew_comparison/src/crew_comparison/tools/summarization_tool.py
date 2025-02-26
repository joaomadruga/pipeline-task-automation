from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class SummarizationToolInput(BaseModel):
    """Input schema for Summarization Tool."""
    text: str = Field(..., description="Text of the research paper to summarize.")

class SummarizationTool(BaseTool):
    name: str = "Summarization Tool"
    description: str = ("Generates a concise summary from the provided text.")
    args_schema: Type[BaseModel] = SummarizationToolInput

    def _run(self, text: str) -> str:
        # Implementation logic to summarize the text
        return "Summary of the text: " + text
