# cin/tcc/tools/report_generator_tool.py
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class ReportGeneratorToolInput(BaseModel):
    """Input schema for Report Generator Tool."""
    summaries: list = Field(..., description="List of summaries with their corresponding paper IDs.")

class ReportGeneratorTool(BaseTool):
    name: str = "Report Generator Tool"
    description: str = ("Compiles given summaries and generates a structured report.")
    args_schema: Type[BaseModel] = ReportGeneratorToolInput

    def _run(self, summaries: list) -> str:
        # Implementation logic to generate a report from the summaries
        return "Generated report with " + str(len(summaries)) + " summaries."
