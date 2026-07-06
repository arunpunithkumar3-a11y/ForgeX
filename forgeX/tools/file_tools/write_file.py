import os
import sys
from typing import Type, Dict, Any
from pydantic import BaseModel

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)

from base_file_tool import BaseFileTool
from tools_schema import WriteFileInput

class WriteFileTool(BaseFileTool):
    name: str = "write_file"
    description: str = (
        "Completely overwrite a file with new content. Creates the file if it does not exist."
    )
    args_schema: Type[BaseModel] = WriteFileInput

    def _run(self, path: str, content: str) -> Dict[str, Any]:
        try:
            resolved_path = self.resolve_path(path)
            if resolved_path.startswith("Access outside workspace"):
                return self.error_response(resolved_path)
            if os.path.exists(resolved_path) and os.path.isdir(resolved_path):
                return self.error_response(f"Path '{path}' is a directory and cannot be overwritten as a file.")
            parent_dir = os.path.dirname(resolved_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(resolved_path, "w", encoding="utf-8") as f:
                f.write(content)
            return self.success_response(
                message=f"File written successfully at '{path}'.",
                path=path
            )
        except Exception as e:
            return self.error_response(str(e))
