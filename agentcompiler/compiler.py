from models.orchestrator import OrchestrationPlan

def compiler(orchestration_plan: OrchestrationPlan):
    """
    This is a very simple implentation of this function, the idea here is to improve this to have a more compiler way of running the agents.
    Since we already have all the steps in a list, we could make this very fast.
    """
    last_answer = ""
    for agent in orchestration_plan.agent_execution_plan:
        last_answer = agent.agent.run(f"Here is last agent answer {last_answer}", )
        print("Agent:", agent.agent.agent_name)
        print("Action Description:", agent.action_description)
        print(last_answer.content)
        print()
