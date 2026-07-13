import os
import sys
from typing import Any, Dict, Type

from pydantic import BaseModel

from forgeX.tools.file_tools.base_file_tool import BaseFileTool
from forgeX.tools.file_tools.tools_schema import DeleteFileInput

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)


class DeleteFileTool(BaseFileTool):
    name: str = "delete_file"
    description: str = "Delete a file from the workspace."
    args_schema: Type[BaseModel] = DeleteFileInput

    def _run(self, path: str, workspace: str = ".") -> Dict[str, Any]:
        print(f"Executing tool: {self.name} on {path}")
        try:
            resolved_path = self.resolve_path(path, workspace)
            if resolved_path.startswith("Access outside workspace"):
                return self.error_response(resolved_path)
            if not os.path.exists(resolved_path):
                return self.error_response(f"File '{path}' does not exist.")
            if not os.path.isfile(resolved_path):
                return self.error_response(
                    f"Path '{path}' is not a file and cannot be deleted by this tool."
                )
            os.remove(resolved_path)
            return self.success_response(
                message=f"File deleted successfully at '{path}'.", path=path
            )
        except Exception as e:
            return self.error_response(str(e))
