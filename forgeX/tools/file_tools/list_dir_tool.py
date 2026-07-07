import os
import sys
from typing import Any, Dict, Type

from pydantic import BaseModel

from forgeX.tools.file_tools.base_file_tool import BaseFileTool
from forgeX.tools.file_tools.tools_schema import ListDirectoryInput
from utils import IGNORE_DIRS, IGNORE_EXTENSIONS, IGNORE_FILES

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)

project_root = os.path.abspath(os.path.join(sibling_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class ListDirectoryTool(BaseFileTool):
    name: str = "List_directory_tool"
    description: str = "Gives all the folder and files in the workspace"
    args_schema: Type[BaseModel] = ListDirectoryInput

    def _run(self, path: str = ".") -> Dict[str, Any]:
        try:
            resolved_path = self.resolve_path(path)
            if resolved_path.startswith("Access outside workspace"):
                return self.error_response(resolved_path)
            if not os.path.exists(resolved_path):
                return self.error_response(f"Directory '{path}' does not exist.")
            if not os.path.isdir(resolved_path):
                return self.error_response(f"Path '{path}' is not a directory.")
            folders = []
            files = []
            ws_path = os.path.abspath(self.workspace)
            for root, dirs, filenames in os.walk(resolved_path):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                for d in dirs:
                    abs_dir = os.path.join(root, d)
                    res_path = self.resolve_path(os.path.relpath(abs_dir, ws_path))
                    if res_path.startswith("Access outside workspace"):
                        continue
                    rel_dir = os.path.relpath(abs_dir, ws_path).replace("\\", "/")
                    folders.append(rel_dir)
                for f in filenames:
                    if f in IGNORE_FILES:
                        continue
                    ext = os.path.splitext(f)[1].lower()
                    if ext in IGNORE_EXTENSIONS:
                        continue
                    abs_file = os.path.join(root, f)
                    res_path = self.resolve_path(os.path.relpath(abs_file, ws_path))
                    if res_path.startswith("Access outside workspace"):
                        continue
                    rel_file = os.path.relpath(abs_file, ws_path).replace("\\", "/")
                    files.append(rel_file)
            folders.sort()
            files.sort()
            return self.success_response(
                message=f"Listed directory '{path}' successfully.",
                directory=path,
                folder_count=len(folders),
                file_count=len(files),
                folders=folders,
                files=files,
            )
        except Exception as e:
            return self.error_response(str(e))
