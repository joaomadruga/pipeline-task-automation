from models.agent import Agent
from langchain.prompts import ChatPromptTemplate
import json

def load_agents() -> list[Agent]:
    with open('../agents/customer_support_automation/agents.json', 'r') as file:
        agents_data = json.load(file)

    agents = agents_data["agents"]
    list_of_agents = []

    for agent_name, agent_info in agents.items():
        agent = Agent(agent_name=agent_name, prompt=agent_info["role"], key_abilities=agent_info["key_abilities"])
        list_of_agents.append(agent)

    return list_of_agents
