import subprocess
from pathlib import Path
from typing import Type, Optional

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from forgeX.tools.Terminal.security.models import (
    CommandArgument,
    CommandRequest,
    CommandResult,
    TerminalInput,
)
from forgeX.tools.Terminal.security.protection import SecurityManager


class TerminalTool(BaseTool):
    name: str = "terminal"
    description: str = "Execute shell commands"
    args_schema: Type[BaseModel] = TerminalInput
    workspace: str = "."

    def _run(
        self,
        executable: str,
        args: list[CommandArgument] = [],
        cwd: Optional[str] = None,
        timeout: int = 120,
    ) -> CommandResult | dict:
        try:
            workspace_path = Path(self.workspace).resolve()
            if cwd:
                cwd_path = Path(cwd)
                if not cwd_path.is_absolute():
                    cwd_path = (workspace_path / cwd_path).resolve()
                else:
                    cwd_path = cwd_path.resolve()
            else:
                cwd_path = workspace_path

            config = CommandRequest(
                executable=executable,
                args=args,
                cwd=cwd_path,
                workspace=workspace_path,
                timeout=timeout,
            )
            security_manager = SecurityManager()
            result = security_manager.validate(config)
            if result.allowed:
                command = [config.executable] + [arg.value for arg in config.args]
                result = subprocess.run(
                    command,
                    capture_output=True,
                    check=False,
                    cwd=config.cwd,
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
            else:
                return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _arun(self, *args, **kwargs) -> dict:
        raise NotImplementedError("Async execution is not implemented.")


if __name__ == "__main__":
    tool = TerminalTool()
    result = tool.invoke(
        {
            "executable": "python",
            "args": [{"value": "s.py", "is_path": True}],
            "cwd": "",
            "timeout": 120,
        }
    )
    print(result)

