from forgeX.core.agents.coder import CoderService
from forgeX.core.agents.planner import PlannerService
from forgeX.core.agents.scanner import ScannerService
from forgeX.core.engine.state import AgentState

scanner_service = ScannerService()
planner_service = PlannerService()
coder_service = CoderService()


def scanner(state: AgentState) -> AgentState:
    return {"project_snapshot": scanner_service.invoke(root_dir=state["workspace"])}


def planner(state: AgentState) -> AgentState:
    return {
        "execution_plan": planner_service.invoke(
            query=state["user_query"],
            snapshot=state["project_snapshot"],
        )
    }


def coder(state: AgentState) -> AgentState:
    return {
        "messages": [
            coder_service.invoke(
                user_query=state["user_query"],
                project_snapshot=state["project_snapshot"],
                plan=state["execution_plan"],
                conversation_history=state["messages"],
            )
        ]
    }
