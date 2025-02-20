#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crew import LatestAiDevelopment

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'Solve tic tac toe task: Create a Tic Tac Toe game using HTML, CSS, and JavaScript. Initialize a new Git repository in a new folder and make structured commits showing progress. Expected output: A fully functional Tic Tac Toe game with a clean and responsive design. The Git repository should have a clear commit history showing the development progress.',
        'current_year': str(datetime.now().year)
    }
    
    try:
        print("running")
        LatestAiDevelopment().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        LatestAiDevelopment().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LatestAiDevelopment().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        LatestAiDevelopment().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
