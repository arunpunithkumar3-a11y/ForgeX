from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from forgeX.agents.Schemas import ExecutionPlan, ProjectSnapshot


class AgentState(TypedDict):
    query: str
    messages: Annotated[List[BaseMessage], add_messages]
    plan: Optional[ExecutionPlan]
    scanner: Optional[ProjectSnapshot]
