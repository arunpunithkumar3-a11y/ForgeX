import os
import sys
from typing import Any, Dict, Type

from pydantic import BaseModel

from forgeX.tools.file_tools.base_file_tool import BaseFileTool
from forgeX.tools.file_tools.tools_schema import CreateFileInput

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)


class CreateFileTool(BaseFileTool):
    name: str = "create_file"
    description: str = "Create a new file inside the workspace. Fails if file exists unless overwrite is True."
    args_schema: Type[BaseModel] = CreateFileInput

    def _run(
        self, path: str, content: str = "", overwrite: bool = False
    ) -> Dict[str, Any]:
        try:
            resolved_path = self.resolve_path(path)
            if resolved_path.startswith("Access outside workspace"):
                return self.error_response(resolved_path)
            if os.path.exists(resolved_path):
                if not overwrite:
                    return self.error_response(
                        f"File '{path}' already exists. Set overwrite=True to overwrite."
                    )
                if os.path.isdir(resolved_path):
                    return self.error_response(
                        f"Path '{path}' is a directory and cannot be overwritten as a file."
                    )
            parent_dir = os.path.dirname(resolved_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            with open(resolved_path, "w", encoding="utf-8") as f:
                f.write(content)
            return self.success_response(
                message=f"File created successfully at '{path}'.", path=path
            )
        except Exception as e:
            return self.error_response(str(e))
