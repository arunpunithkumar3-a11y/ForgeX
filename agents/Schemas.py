from pydantic import BaseModel, Field
from typing import List, Literal,Dict,Optional,Union


from typing import List, Optional
from pydantic import BaseModel, Field
from typing_extensions import Literal

class PlanStep(BaseModel):
    step_number:int=Field(...,description="Sequential number of the step")
    title:str=Field(...,description="Short,descriptive title of the step")
    description:str=Field(...,description="Detailed explanation of what this step involves")
    depends_on:Optional[List[int]]=Field(default=None,description="List of step numbers this step depends on")
    success_criteria:Optional[List[str]]=Field(default=None,description="Conditions that define successful completion of this step")
    step_type:Optional[str]=Field(default="action",description="Type of step (e.g.,action,decision,validation)")

class ExecutionPlan(BaseModel):
    task_type:Literal["bug_fix","feature","refactor","analysis","documentation","unknown"]=Field(...,description="Category of the task being executed")
    objective:str=Field(...,description="High-level goal or purpose of the plan")
    complexity:Literal["low","medium","high"]=Field(...,description="Estimated complexity level of the task")
    likely_files:List[str]=Field(default_factory=list,description="Files most likely to be involved in this task")
    retrieval_queries:List[str]=Field(default_factory=list,description="Queries used to retrieve relevant context or code")
    steps:List[PlanStep]=Field(default_factory=list,description="Ordered list of steps required to execute the plan")
    requires_retrieval:bool=Field(...,description="Whether external retrieval is required")
    reasoning:str=Field(...,description="Explanation of why this plan was generated and its approach")


class SymbolInfo(BaseModel):
    name: str
    full_name: str
    symbol_type: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    parent_symbol: Optional[str] = None
    args: list[str] = Field(default_factory=list)
    return_type: Optional[str] = None
    decorators: list[str] = Field(default_factory=list)
    bases: list[str] = Field(default_factory=list)
    calls: list[str] = Field(default_factory=list)
    is_async: bool = False


class FileInfo(BaseModel):
    path: str
    extension: str
    size_bytes: int
    lines_count: int
    imports: list[str] = Field(default_factory=list)
    full_imports: list[str] = Field(default_factory=list)
    symbols: list[SymbolInfo] = Field(default_factory=list)



class ProjectSnapshot(BaseModel):
    root_path: str
    files: list[FileInfo] = Field(default_factory=list)
    directories: list[str] = Field(default_factory=list)
    total_files: int = 0
    total_directories: int = 0


