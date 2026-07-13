from pathlib import Path
from typing import Annotated

from langgraph.prebuilt import InjectedState
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    pattern: str = Field(description="The search pattern/query.")
    root: Path = Field(
        default=Path("."), description="The root directory to search in."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

    literal: bool = Field(
        default=True,
        description="Whether to search for a literal string instead of a regular expression.",
    )
    case_sensitive: bool = Field(
        default=False, description="Whether the search is case-sensitive."
    )
    whole_word: bool = Field(
        default=False, description="Whether to match whole words only."
    )
    include_hidden: bool = Field(
        default=False, description="Whether to search in hidden files and directories."
    )

    file_globs: list[str] | None = Field(
        default=None,
        description="Optional list of glob patterns to include (e.g., ['*.py']).",
    )
    exclude_globs: list[str] | None = Field(
        default=None,
        description="Optional list of glob patterns to exclude (e.g., ['tests/*']).",
    )

    max_results: int = Field(
        default=200, description="Maximum number of results to return."
    )


class RipGrepResult(BaseModel):
    path: Path = Field(..., description="The file path where the match was found")
    lines: str = Field(..., description="The full line of text containing the match")
    line_number: int = Field(
        ..., description="The line number in the file where the match occurred"
    )
