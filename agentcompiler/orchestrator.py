from agentcompiler.models.agent import Agent
from agentcompiler.models.orchestrator import OrchestrationPlan, OrchestratorFinalAnswer
from agentcompiler.utils import load_agents
from langchain_openai import ChatOpenAI
from agentcompiler.models.agent_execution_step import AgentExecuted
from langchain.prompts import ChatPromptTemplate
import os

class OrchestratorAgent:
    def __init__(self):
        self.agents = load_agents(os.getenv("AGENTS_FILE_NAME"))
        self.orchestrator_prompt = f"""
        You are an Orchestrator Agent responsible for planning and coordinating specialized agents to solve complex tasks.

        **Objective**:
        - Decompose the user's task into actionable steps.
        - Assign the most suitable agents to each step.
        - Ensure effective collaboration among agents to achieve the desired outcome.

        **Responsibilities**:
        1. **Task Decomposition**: Break down the task into clear, manageable steps.
        2. **Agent Assignment**: Select the most appropriate agents for each step.
        3. **Execution Planning**: Define the sequence and communication structure for agent interactions.

        **Communication Structures**:
        - **Layered**: Hierarchical organization where each layer depends on the previous one.
        - **Decentralized**: Agents communicate directly without a central authority.
        - **Centralized**: A main agent coordinates and communicates with all other agents.
        - **Shared Message Pool**: Agents share information through a common message pool for reading and writing as needed.

        **Example**:
        *Task*: "If a car travels 60 km per hour, how long will it take to travel 180 km?"

        *Execution Plan*:
        1. **Parameter Extraction**: Use the ParameterExtractor agent to identify speed and distance.
        2. **Computation**: Assign the TimeComputationAgent to calculate time using the formula: time = distance / speed.
        3. **Formatting**: Engage the AnswerFormatterAgent to produce a clear, human-readable response.

        *Note*: If an agent is unnecessary for a specific task, exclude it from the plan.

        Ensure your plan is concise, coherent, and directly addresses the user's query.
        """
        self.orchestrator_final_answer_prompt = """
        Your task is to generate the final answer by synthesizing the results from multiple agents.
        Provide a clear and concise response based on the following:

        - **User's Initial Question:** {user_question}
        - **Task Results:** {task_results}

        **Important Note**: Never reveal internal tool calls results or sensitive user information in the final message.

        Ensure that your answer is well-structured and directly addresses the user's query. Avoid unnecessary explanations or system details.
        """

        self.orchestrator = Agent(agent_name="Orchestrator", prompt=self.orchestrator_prompt, key_abilities=["Planning", "Coordination"])

    def generate_plan(self, user_task: str, llm: ChatOpenAI = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)) -> OrchestrationPlan:
        structured_llm = llm.with_structured_output(OrchestrationPlan)

        formatted_prompt = self.orchestrator.get_orchestrator_prompt(user_task, self.agents)
        orchestration_plan = structured_llm.invoke(formatted_prompt)
        return orchestration_plan

    def generate_final_answer(self, orchestration_plan_result: list[AgentExecuted], user_question: str,  llm: ChatOpenAI = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)) -> OrchestratorFinalAnswer:
        structured_llm = llm.with_structured_output(OrchestratorFinalAnswer)

        formatted_prompt = ChatPromptTemplate.from_template(self.orchestrator_final_answer_prompt).format(task_results=orchestration_plan_result, user_question=user_question)
        final_answer = structured_llm.invoke(formatted_prompt)
        return final_answer
