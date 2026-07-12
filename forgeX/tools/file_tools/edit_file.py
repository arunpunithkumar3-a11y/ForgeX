import os
import sys
from typing import Any, Dict, Type

from pydantic import BaseModel

from forgeX.tools.file_tools.base_file_tool import BaseFileTool
from forgeX.tools.file_tools.tools_schema import EditFileInput

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)


class EditFileTool(BaseFileTool):
    name: str = "edit_file"
    description: str = "Replace old_text with new_text inside a file."
    args_schema: Type[BaseModel] = EditFileInput

    def _run(
        self,
        path: str,
        old_text: str,
        new_text: str,
        replace_all: bool = False,
        workspace: str = ".",
    ) -> Dict[str, Any]:
        try:
            resolved_path = self.resolve_path(path, workspace)
            if resolved_path.startswith("Access outside workspace"):
                return self.error_response(resolved_path)
            if not os.path.exists(resolved_path):
                return self.error_response(f"File '{path}' does not exist.")
            if not os.path.isfile(resolved_path):
                return self.error_response(f"Path '{path}' is not a file.")
            with open(resolved_path, "r", encoding="utf-8") as f:
                content = f.read()
            count = content.count(old_text)
            if count == 0:
                return self.error_response(
                    f"Target text '{old_text}' not found in '{path}'."
                )
            limit = -1 if replace_all else 1
            new_content = content.replace(old_text, new_text, limit)
            with open(resolved_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return self.success_response(
                message=f"Successfully replaced {count if replace_all else 1} occurrence(s) in '{path}'.",
                path=path,
                replacements=count if replace_all else 1,
            )
        except Exception as e:
            return self.error_response(str(e))
