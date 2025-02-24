import json
import csv
import sys

def flatten_activations(activations):
    """Helper function to flatten the activations made."""
    flattened = []
    for activation in activations:
        agent_name = activation.get("agent_name", "")
        # Handle nested results based on the agent type
        if "tool_result" in activation:
            result = activation["tool_result"]
            if "emails" in result:
                for email in result["emails"]:
                    flattened.append({
                        "agent_name": agent_name,
                        "email_id": email.get("id", ""),
                        "email_subject": email.get("subject", ""),
                        "email_body": email.get("body", ""),
                        "type": "email"
                    })
            elif "sentiment" in result:
                for sentiment in result["sentiment"]:
                    flattened.append({
                        "agent_name": agent_name,
                        "email_id": sentiment.get("email_id", ""),
                        "sentiment": sentiment.get("sentiment", ""),
                        "type": "sentiment"
                    })
            elif "responses" in result:
                for response in result["responses"]:
                    flattened.append({
                        "agent_name": agent_name,
                        "email_id": response.get("email_id", ""),
                        "response": response.get("response", ""),
                        "type": "response"
                    })

    return flattened

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
            # Flatten activations
            activations = flatten_activations(case.get("activations_made", []))
            main_row = [
                case["topic"], case["question"], case["expected_answer"],
                case["latency"], case["activation_count"]
            ]

            # If there are no activations, we just write the main row
            if not activations:
                writer.writerow(main_row + [""] * 5)  # Empty entries for agent details
                continue

            # Write each activation
            for activation in activations:
                if activation["type"] == "email":
                    writer.writerow(main_row + [
                        activation["agent_name"],
                        activation["email_id"],
                        activation["email_subject"],
                        activation["email_body"],
                        "", ""  # No sentiment or response for emails
                    ])
                elif activation["type"] == "sentiment":
                    writer.writerow(main_row + [
                        activation["agent_name"],
                        activation["email_id"],
                        "", "",  # No subject or body for sentiment
                        activation["sentiment"], ""
                    ])
                elif activation["type"] == "response":
                    writer.writerow(main_row + [
                        activation["agent_name"],
                        activation["email_id"],
                        "", "",  # No subject or body for response
                        "", activation["response"]
                    ])

    print(f"CSV file '{csv_file}' created successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python json_to_csv.py input.json output.csv")
    else:
        json_to_csv(sys.argv[1], sys.argv[2])
