from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Type
from agentcompiler.utils import load_agents
import os

AVAILABLE_MODELS = load_agents(os.getenv("AGENTS_FILE_NAME"))

class AgentExecutionStep(BaseModel):
    agent: str = Field(
        description="The specialized agent responsible for a specific step in the task."
    )
    action_description: str = Field(
        description="A detailed description of what the agent will do in this step."
    )

    @validator("agent")
    def check_valid_agent(cls, value: str):
        if value not in AVAILABLE_MODELS.keys():
            raise ValueError(f"Invalid model '{value}'. Choose from {AVAILABLE_MODELS.keys()}.")
        return AVAILABLE_MODELS[value]

class AgentExecuted(AgentExecutionStep):
    result: str = Field(description="The result of the agent's execution")
