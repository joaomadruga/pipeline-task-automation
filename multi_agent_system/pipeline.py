from agents import HumanTaskAgent, DeveloperAgent, PlanAndSolveAgent

def setup_pipeline():
    human_task = HumanTaskAgent("Human Task")
    developer = DeveloperAgent("Developer")
    plan_and_solve = PlanAndSolveAgent("Plan and Solve")

    # Define the pipeline
    human_task.send_message("Describe Success Criteria", developer)
    developer.send_message("Code Developed", plan_and_solve)
    # Continue defining the pipeline

if __name__ == "__main__":
    setup_pipeline()
