from agents import (
    HumanTaskAgent, DeveloperAgent, PlanAndSolveAgent,
    RagWithDocsAgent, TesterUnitAgent, ReviewerAgent, SuccessCriteriaAgent
)

def setup_pipeline():
    # Initialize agents
    human_task = HumanTaskAgent()
    developer = DeveloperAgent()
    plan_and_solve = PlanAndSolveAgent()
    rag_with_docs = RagWithDocsAgent()
    tester_unit = TesterUnitAgent()
    reviewer = ReviewerAgent()
    success_criteria = SuccessCriteriaAgent()

    # Define the pipeline
    task = "Initial Task"
    task = human_task.perform_task(task)
    task = developer.perform_task(task)
    task = plan_and_solve.perform_task(task)
    task = rag_with_docs.perform_task(task)
    task = tester_unit.perform_task(task)
    task = reviewer.perform_task(task)
    task = success_criteria.perform_task(task)

    print(f"Final Task Status: {task}")

if __name__ == "__main__":
    setup_pipeline()
