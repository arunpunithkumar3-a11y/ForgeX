from langgraph.prebuilt import ToolNode

from forgeX.core.agents.coder import CoderService
from forgeX.core.agents.planner import PlannerService
from forgeX.core.agents.scanner import ScannerService
from forgeX.core.engine.state import AgentState
from forgeX.tools.file_tools.delete_file import DeleteFileTool
from forgeX.tools.file_tools.edit_file import EditFileTool
from forgeX.tools.file_tools.list_dir_tool import ListDirectoryTool
from forgeX.tools.file_tools.read_file import ReadFileTool
from forgeX.tools.file_tools.write_file import WriteFileTool
from forgeX.tools.ripgrep_tool.tool import RipGrepSearchTool
from forgeX.tools.Terminal.terminal_tool import TerminalTool

tools = [
    ReadFileTool(),
    WriteFileTool(),
    DeleteFileTool(),
    ListDirectoryTool(),
    EditFileTool(),
    RipGrepSearchTool(),
    TerminalTool(),
]


planner_service = PlannerService()
coder_service = CoderService()


def scanner(state: AgentState) -> AgentState:
    print("Executing scanner node")
    scanner_service = ScannerService(root_dir=state["workspace"])
    return {"project_snapshot": scanner_service.invoke()}


def planner(state: AgentState) -> AgentState:
    print("Executing planner node")
    return {
        "execution_plan": planner_service.invoke(
            query=state["user_query"],
            snapshot=state["project_snapshot"],
        )
    }


def coder(state: AgentState) -> AgentState:
    print("Executing coder node")
    print(state["messages"])
    result = coder_service.invoke(
        user_query=state["user_query"],
        project_snapshot=state["project_snapshot"],
        plan=state["execution_plan"],
        conversation_history=state["messages"],
    )
    return {"messages": [result]}


tool_node = ToolNode(tools)
