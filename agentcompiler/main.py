import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from compiler import AgentCompiler
from orchestrator import OrchestratorAgent

if __name__ == "__main__":
    task_description = "Hi, my user_id is 123 i've been trying to get in touch with customer support for 3 days now and i'm not getting any response. Can you help me?"
    orchestrator = OrchestratorAgent()
    plan = orchestrator.generate_plan(user_task=task_description)
    output = AgentCompiler(orchestration_plan=plan).execute_agents()
    final_answer = orchestrator.generate_final_answer(output, task_description)
    print("\n\n\n Last answer:")
    print(final_answer.final_answer)
