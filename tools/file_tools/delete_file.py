import os
import sys
from typing import Type, Dict, Any
from pydantic import BaseModel

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)

from base_file_tool import BaseFileTool
from tools_schema import DeleteFileInput

class DeleteFileTool(BaseFileTool):
    name: str = "delete_file"
    description: str = (
        "Delete a file inside the workspace safely. Returns success if the file is already absent. "
        "Will never delete directories."
    )
    args_schema: Type[BaseModel] = DeleteFileInput

    def _run(self, path: str) -> Dict[str, Any]:
        try:
            resolved_path = self.resolve_path(path)
            if not os.path.exists(resolved_path):
                return self.success_response(
                    message=f"File '{path}' is already absent.",
                    path=path
                )
            if os.path.isdir(resolved_path):
                return self.error_response(f"Path '{path}' is a directory. DeleteFileTool cannot delete directories.")
            os.remove(resolved_path)
            return self.success_response(
                message=f"File '{path}' deleted successfully.",
                path=path
            )
        except Exception as e:
            return self.error_response(str(e))
