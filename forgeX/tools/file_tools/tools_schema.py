from typing import Annotated, Optional

from langgraph.prebuilt import InjectedState
from pydantic import BaseModel, Field


class ReadFileInput(BaseModel):
    path: str = Field(description="Relative path of the file to read.")
    start_line: Optional[int] = Field(
        default=None,
        description="Optional starting line number (1-indexed, inclusive) to read from.",
    )
    end_line: Optional[int] = Field(
        default=None,
        description="Optional ending line number (1-indexed, inclusive) to read to.",
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."


class ListDirectoryInput(BaseModel):
    path: str = Field(
        default=".", description="Relative directory path inside the workspace."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."


class CreateFileInput(BaseModel):
    path: str = Field(description="Relative path of the new file to create.")
    content: str = Field(default="", description="Initial contents of the file.")
    overwrite: bool = Field(
        default=False, description="Whether to overwrite if the file already exists."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."


class WriteFileInput(BaseModel):
    path: str = Field(description="Relative path of the file to write to.")
    content: str = Field(description="The entire content to write to the file.")
    workspace: Annotated[str, InjectedState("workspace")] = "."


class EditFileInput(BaseModel):
    path: str = Field(description="Relative path of the file to edit.")
    old_text: str = Field(description="The exact block of text to be replaced.")
    new_text: str = Field(description="The block of text to replace old_text with.")
    replace_all: bool = Field(
        default=False,
        description="If True, replaces all occurrences of old_text. If False, only replaces the first occurrence.",
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."


class DeleteFileInput(BaseModel):
    path: str = Field(description="Relative path of the file to delete.")
    workspace: Annotated[str, InjectedState("workspace")] = "."
