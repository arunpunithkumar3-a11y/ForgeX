from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Literal, Annotated
from langgraph.prebuilt import InjectedState

from pydantic import BaseModel, Field



@dataclass
class CommandArgument:
    value: str
    is_path: bool = False


class CommandRequest(BaseModel):
    command:str
    cwd: Path
    workspace: Path
    timeout: int = Field(default=120, gt=0, lt=600)


class TerminalInput(BaseModel):
    command:str=Field(description="command needed to execute")
    cwd: Optional[str] = Field(default=None, description="Relative working directory path within the workspace.")
    timeout: int = Field(default=120, gt=0, lt=600, description="Command execution timeout in seconds.")
    workspace: Annotated[str, InjectedState("workspace")] = "."



class ValidationResult(BaseModel):
    allowed: bool
    requires_confirmation: bool
    risk: Literal["low", "medium", "high", "critical"]
    reason: str

class CommandResult(BaseModel):
    success: bool
    command: List[str] | str
    exit_code: int
    stdout: str
    stderr: str

