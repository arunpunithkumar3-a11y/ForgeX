from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, Field


@dataclass
class CommandArgument:
    value: str
    is_path: bool = False


@dataclass
class CommandRequest:
    executable: str
    args: list[CommandArgument]
    cwd: Path
    workspace: Path
    timeout: int = Field(gt=0, lt=600)


@dataclass
class ValidationResult:
    allowed: bool
    reason: str | None = None


class CommandResult(BaseModel):
    success: bool
    command: str
    exit_code: int
    stdout: str
    stderr: str
