from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field



@dataclass
class CommandArgument:
    value: str
    is_path: bool = False


class CommandRequest(BaseModel):
    executable: str
    args: List[CommandArgument]
    cwd: Path
    workspace: Path
    timeout: int = Field(default=120, gt=0, lt=600)


class TerminalInput(BaseModel):
    executable: str = Field(description="The executable command to run (e.g., git, python).")
    args: List[CommandArgument] = Field(default=[], description="Arguments for the command.")
    cwd: Optional[str] = Field(default=None, description="Relative working directory path within the workspace.")
    timeout: int = Field(default=120, gt=0, lt=600, description="Command execution timeout in seconds.")


@dataclass
class ValidationResult:
    allowed: bool
    reason: str | None = None


class CommandResult(BaseModel):
    success: bool
    command: List[str] | str
    exit_code: int
    stdout: str
    stderr: str

