from models.agent import Agent
from langchain.prompts import ChatPromptTemplate
import json


def load_agents() -> dict[str, Agent]:
    with open('../agents/customer_support_automation/agents.json', 'r') as file:
        agents_data = json.load(file)

    agents = agents_data["agents"]
    agents_dict = {}

    for agent_name, agent_info in agents.items():
        agent = Agent(agent_name=agent_name, prompt=agent_info["role"], key_abilities=agent_info["key_abilities"], tool_result=agent_info["mocked_tool_result"])
        agents_dict[agent_name] = agent

    return agents_dict
