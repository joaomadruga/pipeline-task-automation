from models.agent import Agent
from langchain.prompts import ChatPromptTemplate
import json
from pathlib import Path


def load_agents(agents_file_name) -> dict[str, Agent]:
    agents_file_path = Path(f'agents/{agents_file_name}/agents.json')
    with agents_file_path.open('r') as file:
        agents_data = json.load(file)

    agents = agents_data["agents"]
    agents_dict = {}

    for agent_name, agent_info in agents.items():
        agent = Agent(
            agent_name=agent_name,
            prompt=agent_info["role"],
            key_abilities=agent_info["key_abilities"],
            tool_result=agent_info["mocked_tool_result"]
        )
        agents_dict[agent_name] = agent

    return agents_dict
