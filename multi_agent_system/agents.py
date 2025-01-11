from langchain.agents import Agent

class HumanTaskAgent(Agent):
    def perform_task(self, task):
        # Logic for human task
        return "Describe Success Criteria"

class DeveloperAgent(Agent):
    def perform_task(self, task):
        # Logic for developer task
        return "Code Developed"

class PlanAndSolveAgent(Agent):
    def perform_task(self, task):
        # Logic for planning and solving
        return "Plan and Solve"

class RagWithDocsAgent(Agent):
    def perform_task(self, task):
        # Logic for rag with docs
        return "Rag with Docs"

class TesterUnitAgent(Agent):
    def perform_task(self, task):
        # Logic for unit testing
        return "Tested"

class ReviewerAgent(Agent):
    def perform_task(self, task):
        # Logic for reviewing
        return "Reviewed"

class SuccessCriteriaAgent(Agent):
    def perform_task(self, task):
        # Logic for success criteria
        return "Success Criteria Met"
