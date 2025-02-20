from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config.settings import MODEL_NAME, TEMPERATURE
from models.agent_models import OrchestrationPlan


def run_abstract_agent(action_description, agent_prompt, agent_name):
    llm = ChatOpenAI(model_name=MODEL_NAME, temperature=TEMPERATURE)
    prompt = ChatPromptTemplate.from_template(
        """
        You are an {agent_name} Agent.
        {agent_prompt}
        Task: {action_description}
        """
    )
    formatted_prompt = prompt.format(
        agent_name=agent_name,
        agent_prompt=agent_prompt,
        action_description=action_description
    )
    answer = llm.invoke(formatted_prompt)
    return answer


def run_list_of_agents(orchestration_plan: OrchestrationPlan):
    """
    This is a very simple implementation of this function, the idea here is to improve this to have a more compiler way of running the agents.
    Since we already have all the steps in a list, we could make this very fast.
    """
    last_answer = ""
    for step in orchestration_plan.agent_execution_plan:
        last_answer = run_abstract_agent(
            step.action_description,
            step.agent_prompt + f"Here is last agent answer {last_answer}",
            step.agent_name
        )
        print("Agent:", step.agent_name)
        print("Action Description:", step.action_description)
        print("Agent Prompt:", step.agent_prompt)
        print(last_answer.content)
        print()
