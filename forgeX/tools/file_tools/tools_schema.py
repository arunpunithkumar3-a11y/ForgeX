from pydantic import BaseModel, Field
from typing import List, Annotated
from langgraph.prebuilt import InjectedState

class ReadFileInput(BaseModel):
    path: str = Field(
        description="Relative path of the file to read."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class ListDirectoryInput(BaseModel):
    path: str = Field(
        default=".",
        description="Relative directory path inside the workspace."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class ReadMultipleFilesInput(BaseModel):
    paths: List[str] = Field(
        description="List of relative file paths to read."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class CreateFileInput(BaseModel):
    path: str = Field(
        description="Relative path of the new file to create."
    )
    content: str = Field(
        default="",
        description="Initial contents of the file."
    )
    overwrite: bool = Field(
        default=False,
        description="Whether to overwrite if the file already exists."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class WriteFileInput(BaseModel):
    path: str = Field(
        description="Relative path of the file to write to."
    )
    content: str = Field(
        description="The entire content to write to the file."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class EditFileInput(BaseModel):
    path: str = Field(
        description="Relative path of the file to edit."
    )
    old_text: str = Field(
        description="The exact block of text to be replaced."
    )
    new_text: str = Field(
        description="The block of text to replace old_text with."
    )
    replace_all: bool = Field(
        default=False,
        description="If True, replaces all occurrences of old_text. If False, only replaces the first occurrence."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class DeleteFileInput(BaseModel):
    path: str = Field(
        description="Relative path of the file to delete."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class MoveFileInput(BaseModel):
    source: str = Field(
        description="Relative path of the source file to move/rename."
    )
    destination: str = Field(
        description="Relative path of the destination file."
    )
    overwrite: bool = Field(
        default=False,
        description="Whether to overwrite the destination if it already exists."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."

class CopyFileInput(BaseModel):
    source: str = Field(
        description="Relative path of the source file to copy."
    )
    destination: str = Field(
        description="Relative path of the destination file."
    )
    overwrite: bool = Field(
        default=False,
        description="Whether to overwrite the destination if it already exists."
    )
    workspace: Annotated[str, InjectedState("workspace")] = "."