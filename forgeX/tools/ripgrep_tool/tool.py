import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from forgeX.tools.ripgrep_tool.models import SearchRequest
from forgeX.tools.ripgrep_tool.parser import build_rg_command


def _get_text(field: dict) -> str:
    return field.get("text") or ""


class RipGrepSearchTool(BaseTool):
    name: str = "ripgrep_search_tool"
    description: str = (
        "Search for text or regular expressions in files using ripgrep (rg)."
    )
    args_schema: Type[BaseModel] = SearchRequest
    workspace: str = "."

    def _run(
        self,
        pattern: str,
        root: str = ".",
        literal: bool = True,
        case_sensitive: bool = False,
        whole_word: bool = False,
        include_hidden: bool = False,
        file_globs: list[str] | None = None,
        exclude_globs: list[str] | None = None,
        max_results: int = 200,
    ) -> Dict[str, Any]:
        workspace_path = Path(self.workspace).resolve()

        root_path = Path(root)
        if not root_path.is_absolute():
            root_path = workspace_path / root_path
        root_path = root_path.resolve()

        try:
            root_path.relative_to(workspace_path)
        except ValueError:
            return {
                "success": False,
                "error": f"Access outside workspace is not allowed: '{root}'",
            }

        if not root_path.exists():
            return {
                "success": False,
                "error": f"Root path '{root}' does not exist.",
            }

        try:
            command = build_rg_command(
                SearchRequest(
                    pattern=pattern,
                    root=root_path,
                    literal=literal,
                    case_sensitive=case_sensitive,
                    whole_word=whole_word,
                    include_hidden=include_hidden,
                    file_globs=file_globs,
                    exclude_globs=exclude_globs,
                    max_results=max_results,
                )
            )
        except ValueError as e:
            return {"success": False, "error": str(e)}

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
                shell=False,
            )
        except FileNotFoundError:
            return {
                "success": False,
                "error": "ripgrep (rg) executable is not installed or not found in PATH.",
            }

        if result.returncode >= 2:
            return {
                "success": False,
                "error": result.stderr.strip()
                or f"ripgrep failed with exit code {result.returncode}",
            }

        parsed_results = []

        for line in result.stdout.splitlines():
            if not line:
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("type") != "match":
                continue

            data = event["data"]

            path_str = _get_text(data["path"])

            parsed_results.append(
                {
                    "path": path_str,
                    "lines": _get_text(data["lines"]),
                    "line_number": data["line_number"],
                    "submatches": [
                        {
                            "text": _get_text(match["match"]),
                            "start": match["start"],
                            "end": match["end"],
                        }
                        for match in data["submatches"]
                    ],
                }
            )

        return {
            "success": True,
            "results": parsed_results,
        }

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Async execution is not implemented.")
