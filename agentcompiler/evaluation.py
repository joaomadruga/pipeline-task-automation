import os
import json
import time  # Import time for latency measurement
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from compiler import AgentCompiler
from orchestrator import OrchestratorAgent

def update_test_case_results(test_case, answer, agent_calls, latency, activation_count, activations_made, token_count, cost_estimate):
    test_case["expected_answer"] = str(answer)
    test_case["expected_activations"] = [{"agent_name": activation["agent"].agent_name, "tool_result": activation["agent"].tool_result} for activation in activations_made]
    test_case["latency"] = str(latency)
    test_case["activation_count"] = str(activation_count)
    test_case["activations_made"] = [{"agent_name": activation["agent"].agent_name, "tool_result": activation["agent"].tool_result} for activation in activations_made]
    # test_case["token_count"] = token_count
    # test_case["cost_estimate"] = cost_estimate

if __name__ == "__main__":
    dataset_path = Path("dataset/" + os.getenv("AGENTS_FILE_NAME") + ".json")

    with dataset_path.open('r') as f:
        data = json.load(f)

    orchestrator = OrchestratorAgent()

    for test_case in data['test_cases']:
        task_description = test_case['question']
        plan = orchestrator.generate_plan(user_task=task_description)

        start = time.perf_counter()
        output = AgentCompiler(orchestration_plan=plan).execute_agents()
        latency_seconds = time.perf_counter() - start
        latency = f"{latency_seconds * 1000:.2f} ms"  # Convert latency to milliseconds with units
        final_answer = orchestrator.generate_final_answer(output, task_description)

        activation_count = len(plan.agent_execution_plan)
        activations_made = [{"agent": step.agent, "action": step.action_description} for step in plan.agent_execution_plan]

        token_count = "token_count_info"
        cost_estimate = "cost_estimate_info"

        answer = final_answer.final_answer

        update_test_case_results(test_case, answer, activations_made, latency, activation_count, activations_made, token_count, cost_estimate)

    with dataset_path.open('w') as f:
        json.dump(data, f, indent=2)
