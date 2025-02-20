from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from models.agent_models import OrchestrationPlan
from config.settings import MODEL_NAME, TEMPERATURE


def generate_orchestration_plan(user_task: str) -> OrchestrationPlan:
    llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE)
    orchestration_prompt = ChatPromptTemplate.from_template(
        """
        You are an Orchestrator Agent responsible for planning and coordinating other specialized agents to solve complex tasks.
        Task: {user_task}
        Your responsibilities:
        1. Decompose the task into clear, actionable steps.
        2. Identify the most suitable agents to execute each step.
        3. Define the sequence of agent execution to ensure accurate and complete results.
        Example:
        Task: "If a car travels 60 km per hour, how long will it take to travel 180 km?"
        Execution Plan:
        - Step 1: Use a ParameterExtractor agent to identify speed and distance.
        - Step 2: Invoke TimeComputationAgent to calculate time using time = distance / speed.
        - Step 3: Call AnswerFormatterAgent to produce a clear, human-readable response.
        Output your reasoning and the ordered list of required agents to fulfill the task.
        """
    )
    formatted_prompt = orchestration_prompt.format(user_task=user_task)
    structured_llm = llm.with_structured_output(OrchestrationPlan)
    orchestration_plan = structured_llm.invoke(formatted_prompt)
    return orchestration_plan
