import os
import sys
from typing import Type, Dict, Any
from pydantic import BaseModel

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)

from base_file_tool import BaseFileTool
from tools_schema import ReadFileInput

class ReadFileTool(BaseFileTool):
    name: str = "read_file"
    description: str = "Read the contents of a file from the workspace."
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(self, path: str) -> Dict[str, Any]:
        try:
            resolved_path = self.resolve_path(path)
            if not os.path.exists(resolved_path):
                return self.error_response(f"File '{path}' does not exist.")
            if not os.path.isfile(resolved_path):
                return self.error_response(f"Path '{path}' is not a file.")
            with open(resolved_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return self.success_response(
                message=f"Successfully read file '{path}'.",
                path=path,
                content=content
            )
        except Exception as e:
            return self.error_response(str(e))
