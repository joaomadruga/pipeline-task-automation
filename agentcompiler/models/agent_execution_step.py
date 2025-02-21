from pydantic import BaseModel, Field
from enum import Enum
from utils import load_agents

class AgentEnum(str, Enum):
    AGENTS = {agent.agent_name: agent for agent in load_agents()} if load_agents() else {}

class AgentExecutionStep(BaseModel):
    agent: AgentEnum = Field(
        description="The specialized agent responsible for a specific step in the task."
    )
    action_description: str = Field(
        description="A detailed description of what the agent will do in this step."
    )
