from agents.orchestrator import generate_orchestration_plan
from agents.abstract_agent import run_list_of_agents


def main():
    task_description = "Generate a website layout for a personal blog with a header, footer, and a main content section. Also it should has tests and be written in react"
    plan_result = generate_orchestration_plan(task_description)
    print("Orchestration Plan:", plan_result.agent_execution_plan)
    run_list_of_agents(plan_result)


if __name__ == "__main__":
    main()
