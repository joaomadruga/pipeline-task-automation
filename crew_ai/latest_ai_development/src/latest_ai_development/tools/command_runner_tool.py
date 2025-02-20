import subprocess
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class CommandRunnerToolInput(BaseModel):
    """Input schema for CommandRunnerTool."""
    command: str = Field(..., description="The command to run on the computer.")

class CommandRunnerTool(BaseTool):
    name: str = "Command Runner Tool"
    description: str = "Tool to run commands on the computer."
    args_schema: Type[BaseModel] = CommandRunnerToolInput

    def _run(self, command: str) -> str:
        input(f"Do you want to run the command {command}? Press Enter to continue.")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
