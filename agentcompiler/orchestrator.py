from models.agent import Agent
from models.orchestrator import OrchestrationPlan
from utils import load_agents
from langchain_openai import ChatOpenAI

class OrchestratorAgent:
    def __init__(self):
        self.agents = load_agents()
        self.orchestrator_prompt = f"""
            You are an Orchestrator Agent responsible for planning and coordinating other specialized agents to solve complex tasks.

            Here are the available agents:
            {self.agents}

            Your responsibilities:
            1. Decompose the task into clear, actionable steps.
            2. Identify the most suitable agents to execute each step.
            3. Define the sequence of agent execution to ensure accurate and complete results.

            Communication Structures:
            1. Layered: Agents are organized hierarchically, where each layer depends on the previous one.
            2. Decentralized: All agents communicate directly with each other without a central authority.
            3. Centralized: One main agent coordinates and communicates with all other agents.
            4. Shared Message Pool: Agents share information through a common message pool where each agent reads and writes as needed.

            Example:
            Task: "If a car travels 60 km per hour, how long will it take to travel 180 km?"

            Execution Plan:
            - Step 1: Use a ParameterExtractor agent to identify speed and distance.
            - Step 2: Invoke TimeComputationAgent to calculate time using time = distance / speed.
            - Step 3: Call AnswerFormatterAgent to produce a clear, human-readable response.

            Output your reasoning and the ordered list of required agents to fulfill the task.
            """

        self.orchestrator = Agent(agent_name="Orchestrator", prompt=self.orchestrator_prompt, key_abilities=["Planning", "Coordination"])

    def generate_plan(self, user_task: str, llm: ChatOpenAI = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)) -> OrchestrationPlan:
        structured_llm = llm.with_structured_output(OrchestrationPlan)

        formatted_prompt = self.orchestrator.get_prompt(user_task)

        orchestration_plan = structured_llm.invoke(formatted_prompt)

        return orchestration_plan
