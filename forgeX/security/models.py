from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel


@dataclass
class CommandRequest:
    executable: str
    args: list[str]
    cwd: Path
    working_directory: str


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
    duration_ms: float
