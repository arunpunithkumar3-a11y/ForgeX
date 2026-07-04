from langchain_core.tools import BaseTool
from docker_backend import DockerBackend
from models import SandboxConfig
from pathlib import Path
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
        backend = DockerBackend(config)
        result = backend.execute(command=command,timeout=timeout)

        return {"success": True, "result": result}

    async def _arun(self, *args, **kwargs) -> dict:
        raise NotImplementedError("Async execution is not implemented.")

if __name__=="__main__":
    tool = TerminalTool()
    result = tool.invoke({
        "command":"python testing.py",
        "timeout":120,
    })
    print(result)