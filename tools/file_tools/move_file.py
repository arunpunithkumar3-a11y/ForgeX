import os
import sys
import shutil
from typing import Type, Dict, Any
from pydantic import BaseModel

sibling_dir = os.path.dirname(__file__)
if sibling_dir not in sys.path:
    sys.path.insert(0, sibling_dir)

from base_file_tool import BaseFileTool
from tools_schema import MoveFileInput

class MoveFileTool(BaseFileTool):
    name: str = "move_file"
    description: str = (
        "Move or rename a file inside the workspace. "
        "Creates destination directories if necessary, and optionally overwrites existing destination."
    )
    args_schema: Type[BaseModel] = MoveFileInput

    def _run(self, source: str, destination: str, overwrite: bool = False) -> Dict[str, Any]:
        try:
            resolved_source = self.resolve_path(source)
            if resolved_source.startswith("Access outside workspace"):
                return self.error_response(resolved_source)
            resolved_dest = self.resolve_path(destination)
            if resolved_dest.startswith("Access outside workspace"):
                return self.error_response(resolved_dest)
            if not os.path.exists(resolved_source):
                return self.error_response(f"Source file '{source}' does not exist.")
            if not os.path.isfile(resolved_source):
                return self.error_response(f"Source '{source}' is not a file (MoveFileTool does not move directories).")
            if os.path.exists(resolved_dest):
                if not overwrite:
                    return self.error_response(f"Destination '{destination}' already exists. Set overwrite=True to overwrite.")
                if os.path.isdir(resolved_dest):
                    return self.error_response(f"Destination '{destination}' is a directory and cannot be overwritten by a file.")
                os.remove(resolved_dest)
            dest_parent = os.path.dirname(resolved_dest)
            if dest_parent:
                os.makedirs(dest_parent, exist_ok=True)
            shutil.move(resolved_source, resolved_dest)
            return self.success_response(
                message=f"Successfully moved '{source}' to '{destination}'.",
                source=source,
                destination=destination
            )
        except Exception as e:
            return self.error_response(str(e))
