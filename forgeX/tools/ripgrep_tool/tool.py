from typing import Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel

from forgeX.tools.ripgrep_tool.models import SearchRequest


class RipGrepSearchTool(BaseTool):
    name = "ripgrep_search_tool"
    description = "Ripgrep (rg) is a fast, line-oriented search tool that recursively searches your filesystem for a regex pattern"
    args_schema: Type[BaseModel] = SearchRequest

    def _run(
        pattern: str,
        root: str,
    ):
        pass
