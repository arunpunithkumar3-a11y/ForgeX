import subprocess
from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from forgeX.tools.Terminal.security.models import CommandRequest, CommandResult


class TerminalTool(BaseTool):
    name: str = "terminal"
    description: str = "Execute shell commands"
    args_schema: Type[BaseModel] = CommandRequest

    def _run(self, config: CommandRequest) -> CommandResult:
        try:
            command = [config.executable] + [arg.value for arg in config.args]
            result = subprocess.run(
                command,
                capture_output=True,
                check=True,
                text=True,
                shell=False,
                timeout=config.timeout,
            )
            return CommandResult(
                success=True,
                command=result.args,
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _arun(self, *args, **kwargs) -> dict:
        raise NotImplementedError("Async execution is not implemented.")


if __name__ == "__main__":
    tool = TerminalTool()
    result = tool.invoke(
        {
            "command": "python Agent.py",
            "timeout": 120,
        }
    )
    print(result)
