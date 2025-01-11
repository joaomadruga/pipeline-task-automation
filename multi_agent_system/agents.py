class Agent:
    def __init__(self, name):
        self.name = name

    def send_message(self, message, recipient):
        print(f"{self.name} sends message to {recipient.name}: {message}")

    def receive_message(self, message, sender):
        print(f"{self.name} received message from {sender.name}: {message}")

class HumanTaskAgent(Agent):
    def perform_task(self):
        # Logic for human task
        pass

class DeveloperAgent(Agent):
    def perform_task(self):
        # Logic for developer task
        pass

class PlanAndSolveAgent(Agent):
    def perform_task(self):
        # Logic for planning and solving
        pass

# Add other agents as needed
