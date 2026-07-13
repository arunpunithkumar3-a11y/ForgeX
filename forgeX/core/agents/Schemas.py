from typing import List, Literal

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    title: str = Field(..., description="Short descriptive title of the step.")

    description: str = Field(
        ...,
        description="Detailed explanation of what the executor should do in this step.",
    )

    success_criteria: List[str] = Field(
        default_factory=list,
        description="Observable conditions that indicate this step has been completed successfully.",
    )


class ExecutionPlan(BaseModel):
    task_type: Literal[
        "bug_fix",
        "feature",
        "refactor",
        "analysis",
        "documentation",
        "unknown",
    ] = Field(..., description="High-level category of the user's request.")

    objective: str = Field(
        ..., description="Overall goal that the executor should accomplish."
    )

    complexity: Literal["low", "medium", "high"] = Field(
        ...,
        description="Estimated implementation complexity based on the current codebase.",
    )

    likely_files: List[str] = Field(
        default_factory=list,
        description="The files which can help for the project, which we get data from project_snapshot. Must contain ONLY file paths that are explicitly listed in the project snapshot.",
    )

    steps: List[PlanStep] = Field(
        default_factory=list,
        description="Ordered sequence of execution steps for completing the objective.",
    )

    strategy: str = Field(
        ...,
        description="Brief summary of the overall approach chosen to accomplish the task.",
    )


class FileInfo(BaseModel):
    path: str
    extension: str
    size_bytes: int
    lines_count: int


class ProjectSnapshot(BaseModel):
    root_path: str
    files: list[FileInfo] = Field(default_factory=list)
    directories: list[str] = Field(default_factory=list)
    total_files: int = 0
    total_directories: int = 0
