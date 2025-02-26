# cin/tcc/tools/topic_classifier_tool.py
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class TopicClassifierToolInput(BaseModel):
    """Input schema for Topic Classifier Tool."""
    text: str = Field(..., description="Text of the paper to classify.")

class TopicClassifierTool(BaseTool):
    name: str = "Topic Classifier Tool"
    description: str = ("Classifies the given text into relevant research topics.")
    args_schema: Type[BaseModel] = TopicClassifierToolInput

    def _run(self, text: str) -> list:
        # Implementation logic to classify the topics of the text
        return ["Artificial Intelligence", "Deep Learning"]
