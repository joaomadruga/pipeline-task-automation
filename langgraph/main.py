import os
import json
import aiofiles
import asyncio
from IPython.display import Image, display
from graph import workflow
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

async def read_txt_file(file_path: str) -> str:
    """
    Reads the content of a .txt file asynchronously.

    Args:
    - file_path (str): The path to the .txt file to be read.

    Returns:
    - str: The content of the file.
    """
    async with aiofiles.open(file_path, 'r') as file:
        content = await file.read()
    return content

def main():
    repository = asyncio.run(read_txt_file("repo.txt"))
    task_description = f"Create a folder named 'pipeline-task-automation'. you should cloning using this as knowledge base '{repository}' and a new file within it that prints 'Hello, World!'"
    graph = workflow.compile()

    try:
        image_path = os.path.expanduser("~/Downloads/graph.png")
        graph.get_graph().draw_mermaid_png(output_file_path=image_path)
        print(f"Graph saved to {image_path}")
        print(task_description)
        events = graph.stream(
        {
            "messages": [
                (
                    "user",
                    task_description,
                )
            ],
        },
        # Maximum number of steps to take in the graph
        {"recursion_limit": 5},
        )
        for s in events:
            print(s)
            print("----")
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    main()
