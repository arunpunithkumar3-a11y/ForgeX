import os
from typing import Dict, Any
from langchain_core.tools import BaseTool

class BaseFileTool(BaseTool):
    workspace: str = "."

    def resolve_path(self, path: str, workspace: str = None) -> str:
        target_workspace = workspace if workspace is not None else self.workspace
        abs_workspace = os.path.abspath(target_workspace)
        abs_target = os.path.abspath(os.path.join(abs_workspace, path))
        try:
            common = os.path.commonpath([abs_workspace, abs_target])
        except ValueError:
            return f"Access outside workspace is not allowed: '{path}'"
        if common != abs_workspace:
            return f"Access outside workspace is not allowed: '{path}'"
        return abs_target

    def success_response(self, message: str, **kwargs: Any) -> Dict[str, Any]:
        res = {"success": True, "message": message}
        res.update(kwargs)
        return res

    def error_response(self, error_message: str) -> Dict[str, Any]:
        return {"success": False, "error": error_message}

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        return "Async execution is not implemented."
