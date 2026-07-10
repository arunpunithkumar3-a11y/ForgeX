from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    pattern: str = Field(description="The search pattern/query.")
    root: Path = Field(
        default=Path("."), description="The root directory to search in."
    )

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


@dataclass(slots=True)
class SearchResult:
    file: str  # Kept as str/Path, but str is easier to serialize. We can keep it Path or str.
    line: int
    column: int
    text: str


@dataclass(slots=True)
class SearchResponse:
    results: list[SearchResult]
    total_matches: int
    searched_path: str
