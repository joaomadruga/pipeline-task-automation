import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from compiler import AgentCompiler
from orchestrator import OrchestratorAgent

if __name__ == "__main__":
    task_description = "Por favor sempre me responda em português. Meu nome é João, queria saber do que você é capaz"
    plan = OrchestratorAgent().generate_plan(user_task=task_description)
    print("Plan generated:")
    print(plan)
    print("\n\n\nAgent Execution Plan:")
    print(plan.agent_execution_plan)
    print("\n\n\nCommunication Structure:")
    print(plan.communication_structure)
    output = AgentCompiler(orchestration_plan=plan).execute_agents()
    print(output)
