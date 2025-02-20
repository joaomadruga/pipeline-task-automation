from typing import Annotated
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import docker
from pathlib import Path


@tool
def shell_execution_tool(
    command: Annotated[str, "The command to run"]
) -> str:
    """Tool for executing shell commands in a sandboxed environment."""
    docker_client = docker.from_client()
    container = docker_client.containers.run(
        "python:3.9-slim",
        command="tail -f /dev/null",
        detach=True,
        remove=True,
        mem_limit="512m",
        cpu_period=100000,
        cpu_quota=50000,
        working_dir="/workspace",
        volumes={
            str(Path.cwd() / "workspace"): {
                'bind': '/workspace',
                'mode': 'rw'
            }
        }
    )
    try:
        exit_code, output = container.exec_run(
            command,
            workdir="/workspace",
            demux=True
        )
        stdout = output[0].decode('utf-8') if output[0] else ""
        stderr = output[1].decode('utf-8') if output[1] else ""
        result_str = f"Exit Code: {exit_code}\nOutput:\n{stdout}\nErrors:\n{stderr}"
    except BaseException as e:
        result_str = f"Failed to execute. Error: {repr(e)}"
    finally:
        container.stop()
    return result_str + "\n\nIf you have completed all tasks, respond with FINAL ANSWER."

@tool
def documentation_tool(
    query: Annotated[str, "The search query"]
) -> str:
    """Tool for accessing and searching documentation"""
    # Implement RAG logic here
    return f"Documentation results for: {query}"

@tool
def plan_and_solve_tool(
    query: Annotated[str, "The query related to the plan_and_solve article"]
) -> str:
    """Tool for accessing and processing the plan_and_solve article."""
    # Implement logic specific to the plan_and_solve article here
    return f"Plan and Solve results for: {query}"

@tool
def database_tool(
    query: Annotated[str, "The query to run against the mocked database"]
) -> str:
    """Tool for interacting with a mocked database."""
    # Implement mocked database logic here
    mock_data = {
        "user_1": {"name": "Alice", "age": 30},
        "user_2": {"name": "Bob", "age": 25},
        "user_3": {"name": "Charlie", "age": 35}
    }
    result = mock_data.get(query, "No data found for the given query")
    return f"Mocked Database results for '{query}': {result}"

