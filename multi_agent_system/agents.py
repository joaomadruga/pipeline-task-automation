from langchain.agents import Agent
from langchain.llms import OpenAI

class HumanTaskAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Describe the success criteria for the task.")
        return response

class DeveloperAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Develop the code for the task.")
        return response

class PlanAndSolveAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Plan and solve the task.")
        return response

class RagWithDocsAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Integrate documentation with the task.")
        return response

class TesterUnitAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Conduct unit testing for the task.")
        return response

class ReviewerAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Review the task.")
        return response

class DBAnalystAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Analyze the database requirements for the task.")
        return response

class SuccessCriteriaAgent(Agent):
    def perform_task(self, task):
        llm = OpenAI()
        response = llm("Ensure the task meets the success criteria.")
        return response
