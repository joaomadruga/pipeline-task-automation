import os
import json
import time
import sys
import re
from io import StringIO
from dotenv import load_dotenv
from pathlib import Path
from customer_support_crew import CustomerSupportCrew
from research_crew import ResearchCrew
from agentcompiler.orchestrator import OrchestratorAgent

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def update_test_case_results(test_case, answer, latency, activation_count, activations_made):
    test_case["expected_answer"] = answer  # Now storing structured JSON
    test_case["latency"] = latency
    test_case["activation_count"] = activation_count
    test_case["activations_made"] = activations_made

def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def parse_log_output(log_output):
    """Extract structured information from the captured logs."""
    entries = []
    current_entry = None

    lines = log_output.strip().split("\n")
    cleaned_lines = [remove_ansi_escape_sequences(line) for line in lines]

    for line in cleaned_lines:
        line = line.strip()

        if line.startswith("# Agent:"):
            if current_entry:  # Salva o agente anterior antes de iniciar um novo
                entries.append(current_entry)
            current_entry = {"agent": line.replace("# Agent:", "").strip(), "tools": []}

        elif current_entry is not None:  # Garante que um agente está definido antes de processar
            if line.startswith("## Task:"):
                current_entry["task"] = line.replace("## Task:", "").strip()

            elif line.startswith("## Thought:"):
                current_entry["thought"] = line.replace("## Thought:", "").strip()

            elif line.startswith("## Using tool:"):
                tool_name = line.replace("## Using tool:", "").strip()
                current_entry["tools"].append({"name": tool_name, "input": None, "output": None})

            elif line.startswith("## Tool Input:"):
                match = re.search(r'## Tool Input:\s*(.*)', line)
                if match and current_entry["tools"]:
                    tool_input = match.group(1)
                    try:
                        current_entry["tools"][-1]["input"] = json.loads(tool_input)
                    except json.JSONDecodeError:
                        current_entry["tools"][-1]["input"] = tool_input.strip()

            elif line.startswith("## Tool Output:"):
                match = re.search(r'## Tool Output:\s*(.*)', line)
                if match and current_entry["tools"]:
                    tool_output = match.group(1)
                    try:
                        current_entry["tools"][-1]["output"] = json.loads(tool_output)
                    except json.JSONDecodeError:
                        current_entry["tools"][-1]["output"] = tool_output.strip()

            elif line.startswith("## Final Answer:"):
                match = re.search(r'## Final Answer:\s*(.*)', line)
                if match:
                    final_answer = match.group(1)
                    try:
                        current_entry["final_answer"] = json.loads(final_answer)
                    except json.JSONDecodeError:
                        current_entry["final_answer"] = final_answer.strip()

    if current_entry:  # Adiciona o último agente processado
        entries.append(current_entry)

    return entries

if __name__ == "__main__":
    dataset_path = Path("dataset/" + os.getenv("AGENTS_FILE_NAME") + ".json")

    with dataset_path.open('r') as f:
        data = json.load(f)

    for test_case in data['test_cases']:
        task_description = test_case['topic']

        # Capture logs by redirecting stdout
        stdout_backup = sys.stdout
        sys.stdout = StringIO()

        start = time.perf_counter()
        # crew_comparison = CustomerSupportCrew()
        crew_comparison = ResearchCrew()
        output = crew_comparison.crew().kickoff(inputs={'topic': task_description})

        execution_logs = sys.stdout.getvalue()  # Get all printed logs

        sys.stdout = stdout_backup

        latency_seconds = time.perf_counter() - start
        latency = f"{latency_seconds * 1000:.2f} ms"

        # Extract structured data from logs
        extracted_data = parse_log_output(execution_logs)
        # print(execution_logs)

        activation_count = len(extracted_data)
        activations_made = extracted_data

        # Update test case with structured log results
        orchestrator = OrchestratorAgent()
        final_answer = orchestrator.generate_final_answer(str(output), task_description)
        update_test_case_results(test_case, final_answer.final_answer, latency, activation_count, activations_made)

    with dataset_path.open('w') as f:
        json.dump(data, f, indent=2)
