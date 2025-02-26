from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class TextExtractionToolInput(BaseModel):
    """Input schema for Text Extraction Tool."""
    paper_id: str = Field(..., description="Identifier of the paper to extract text from.")
    paper_url: str = Field(..., description="URL to access the paper.")

class TextExtractionTool(BaseTool):
    name: str = "Text Extraction Tool"
    description: str = ("Extracts and cleans text content from a given research paper.")
    args_schema: Type[BaseModel] = TextExtractionToolInput

    def _run(self, paper_id: str, paper_url: str) -> str:
        # Implementation logic to extract text from the paper
        return "Extracted text from paper: " + paper_id
