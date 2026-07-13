from typing import Annotated, List, TypedDict

from core.agents.Schemas import ExecutionPlan, ProjectSnapshot
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    user_query: str
    messages: Annotated[List[BaseMessage], add_messages]
    workspace: str
    project_snapshot: ProjectSnapshot
    execution_plan: ExecutionPlan
