from enum import Enum, IntEnum
from pydantic import BaseModel, ValidationError, Field
from models.agent_execution_step import AgentExecutionStep
from typing import Optional, List

class CommunicationStructure(str, Enum):
    LAYERED = "Layered: Agents are organized hierarchically, where each layer depends on the previous one."
    DECENTRALIZED = "Decentralized: All agents communicate directly with each other without a central authority."
    CENTRALIZED = "Centralized: One main agent coordinates and communicates with all other agents."
    SHARED_MESSAGE_POOL = "Shared Message Pool: Agents share information through a common message pool where each agent reads and writes as needed."

class OrchestrationPlan(BaseModel):
    agent_execution_plan: List[AgentExecutionStep] = Field(
        default_factory=list,
        description="A sequential list detailing the agents to be invoked and their responsibilities in the task pipeline."
    )
    communication_structure: Optional[CommunicationStructure] = Field(
        description="The communication structure used to coordinate the agents in the task execution."
    )

class OrchestratorFinalAnswer(BaseModel):
    final_answer: str = Field(
        description="The conclusive output generated by coordinating multiple agents to solve the given task."
    )
