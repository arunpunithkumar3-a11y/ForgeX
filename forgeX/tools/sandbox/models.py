from enum import Enum
from pydantic import BaseModel
from pathlib import Path

from pydantic import BaseModel, Field


class SandboxConfig(BaseModel):
    """
    Configuration for a sandbox instance.
    """

    workspace: Path = Field(
        description="Path to the project that will be mounted into the sandbox."
    )

    image: str = Field(
        default="python:3.12-slim",
        description="Docker image used for the sandbox."
    )

    container_name: str | None = Field(
        default=None,
        description="Optional custom container name."
    )

    working_directory: str = Field(
        default="/workspace",
        description="Working directory inside the container."
    )

    auto_remove: bool = Field(
        default=True,
        description="Automatically remove the container after it is stopped."
    )

    timeout: int = Field(
        default=300,
        ge=1,
        description="Default command timeout in seconds."
    )

class SandboxStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"
    REMOVED = "removed"
    ERROR = "error"

class CommandResult(BaseModel): 
    success: bool
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float


class SandboxInfo(BaseModel):
    session_id: str
    container_id: str
    workspace: str
    status: SandboxStatus

