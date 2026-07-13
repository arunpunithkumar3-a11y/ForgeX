import os
import sys
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel

from forgeX.tools.file_tools.base_file_tool import BaseFileTool
from forgeX.tools.file_tools.tools_schema import ReadFileInput

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)


class ReadFileTool(BaseFileTool):
    name: str = "read_file"
    description: str = "Read the contents of a file from the workspace."
    args_schema: Type[BaseModel] = ReadFileInput

    def _run(
        self,
        path: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
        workspace: str = ".",
    ) -> Dict[str, Any]:
        print(f"Executing tool: {self.name} on {path}")
        try:
            resolved_path = self.resolve_path(path, workspace)
            if resolved_path.startswith("Access outside workspace"):
                return self.error_response(resolved_path)
            if not os.path.exists(resolved_path):
                return self.error_response(f"File '{path}' does not exist.")
            if not os.path.isfile(resolved_path):
                return self.error_response(f"Path '{path}' is not a file.")

            with open(resolved_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            total_lines = len(lines)

            if start_line is not None or end_line is not None:
                start = start_line if start_line is not None else 1
                end = end_line if end_line is not None else total_lines

                start_idx = max(0, start - 1)
                end_idx = min(total_lines, end)

                if start_idx >= total_lines:
                    return self.error_response(
                        f"start_line ({start}) exceeds total file lines ({total_lines})."
                    )
                if start_idx > end_idx:
                    return self.error_response(
                        f"start_line ({start}) cannot be greater than end_line ({end})."
                    )

                content = "".join(lines[start_idx:end_idx])
                message = f"Successfully read lines {start_idx+1} to {end_idx} of file '{path}' (total lines: {total_lines})."
            else:
                content = "".join(lines)
                message = f"Successfully read file '{path}' (total lines: {total_lines})."

            return self.success_response(
                message=message, path=path, content=content
            )
        except Exception as e:
            return self.error_response(str(e))
