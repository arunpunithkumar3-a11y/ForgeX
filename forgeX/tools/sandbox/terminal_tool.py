from pathlib import Path

from langchain_core.tools import BaseTool

from forgeX.tools.sandbox.docker_backend import DockerBackend
from forgeX.tools.sandbox.models import SandboxConfig

config = SandboxConfig(
    image="python:3.12-slim",
    container_name="sandbox_container",
    working_directory="/workspace",
    workspace=Path.cwd(),
    auto_remove=True,
)


class TerminalTool(BaseTool):
    name: str = "terminal"
    description: str = "Execute shell commands in a sandboxed environment."

    def _run(self, command: str, timeout: int | None = None) -> dict:
        try:
            backend = DockerBackend(config)
            result = backend.execute(command=command, timeout=timeout)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _arun(self, *args, **kwargs) -> dict:
        raise NotImplementedError("Async execution is not implemented.")


if __name__ == "__main__":
    tool = TerminalTool()
    result = tool.invoke(
        {
            "command": "python testing.py",
            "timeout": 120,
        }
    )
    print(result)
