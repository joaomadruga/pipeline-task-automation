from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class Agent(BaseModel):
    agent_name: str
    prompt: str
    key_abilities: list[str]
    is_central_authority: bool = Field(default=False, description="Flag indicating if this agent is a central authority.")

    def get_prompt(self, user_task: str) -> str:
        prompt = (f"Your name is {self.agent_name}.\n"
                  f"Your key abilities are: {', '.join(self.key_abilities)}.\n"
                  f"Central Authority: {self.is_central_authority}\n\n"
                  f"{self.prompt}\n\n"
                  "Task: {user_task}")
        print(prompt)

        return ChatPromptTemplate.from_template(prompt).format(user_task=user_task)

    def run(self, user_task: str, llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)):
        return llm.invoke(self.get_prompt(user_task))
