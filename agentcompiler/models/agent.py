from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json

class Agent(BaseModel):
    agent_name: str
    prompt: str
    key_abilities: list[str]
    is_central_authority: bool = Field(default=False, description="Flag indicating if this agent is a central authority.")
    tool_result: dict = Field(default={}, description="The agent tool result.")

    def get_orchestrator_prompt(self, user_task: str, agents) -> str:
        prompt = (f"Your name is {self.agent_name}.\n"
                  f"Your key abilities are: {', '.join(self.key_abilities)}.\n"
                  f"Central Authority: {self.is_central_authority}\n\n"
                  f"{self.prompt}\n\n"
                  "Agents available: {agents}\n"
                  "Task: {user_task}")

        return ChatPromptTemplate.from_template(prompt).format(user_task=user_task, agents=agents)

    def get_prompt_with_tools(self, user_task: str) -> str:
        prompt = (f"Your name is {self.agent_name}.\n"
                  f"Your key abilities are: {', '.join(self.key_abilities)}.\n"
                  f"Central Authority: {self.is_central_authority}\n\n"
                  f"{self.prompt}\n\n"
                  "Tool result: {tool_result}\n"
                  "Task: {user_task}")
        # if self.tool_result:
        #     tool_name = list(self.tool_result.keys())[0]
        #     tool_result = json.dumps(self.tool_result[tool_name])
        #     prompt = (f"Tool name: {tool_name}\n"
        #               f"Tool result: {tool_result}\n" + prompt)


        return ChatPromptTemplate.from_template(prompt).format(user_task=user_task, tool_result=self.tool_result)

    def run(self, user_task: str, llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)):
        return llm.invoke(self.get_prompt_with_tools(user_task))
