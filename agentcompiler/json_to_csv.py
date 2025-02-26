import json
import csv
import sys

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if "test_cases" not in data or not data["test_cases"]:
        print("Empty or invalid JSON file.")
        return

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        # Prepare the CSV writer
        writer = csv.writer(f)
        writer.writerow([
            "topic", "question", "expected_answer", "latency", "activation_count",
            "agent_name", "email_id", "email_subject", "email_body", "sentiment", "response"
        ])

        # Process each test case
        for case in data["test_cases"]:
            # Print topic, question, expected_answer, latency, activation_count
            topic = case["topic"]
            question = case["question"]
            expected_answer = case["expected_answer"]
            latency = case["latency"]
            activation_count = case["activation_count"]

            # Initialize the agent details as empty strings
            agent_name = ""
            email_id = ""
            email_subject = ""
            email_body = ""
            sentiment = ""
            response = ""

            # You can choose to include the first activation details if there are any
            if case.get("activations_made"):
                first_activation = case["activations_made"][0]  # Get first activation
                agent_name = first_activation.get("agent_name", "")
                if "tool_result" in first_activation:
                    tool_result = first_activation["tool_result"]

                    if "emails" in tool_result:
                        if tool_result["emails"]:
                            email = tool_result["emails"][0]  # Get the first email
                            email_id = email.get("id", "")
                            email_subject = email.get("subject", "")
                            email_body = email.get("body", "")

                    if "sentiment" in tool_result:
                        if tool_result["sentiment"]:
                            sentiment = tool_result["sentiment"][0].get("sentiment", "")

                    if "responses" in tool_result:
                        if tool_result["responses"]:
                            response = tool_result["responses"][0].get("response", "")

            # Write the combined row
            writer.writerow([
                topic, question, expected_answer, latency, activation_count,
                agent_name, email_id, email_subject, email_body, sentiment, response
            ])

    print(f"CSV file '{csv_file}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python json_to_csv.py input.json output.csv")
    else:
        json_to_csv(sys.argv[1], sys.argv[2])
