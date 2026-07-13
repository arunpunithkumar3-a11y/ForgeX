import os

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from forgeX.core.agents.backend import ServiceClass
from forgeX.core.agents.prompts import CODER_PROMPT
from forgeX.core.agents.Schemas import ExecutionPlan, ProjectSnapshot
from forgeX.tools.file_tools.delete_file import DeleteFileTool
from forgeX.tools.file_tools.edit_file import EditFileTool
from forgeX.tools.file_tools.list_dir_tool import ListDirectoryTool
from forgeX.tools.file_tools.read_file import ReadFileTool
from forgeX.tools.file_tools.write_file import WriteFileTool
from forgeX.tools.ripgrep_tool.tool import RipGrepSearchTool
from forgeX.tools.Terminal.terminal_tool import TerminalTool

load_dotenv()

api_key = (
    os.environ.get("OPEN_AI_KEY") or os.environ.get("OPENAI_API_KEY") or "dummy_key"
)

model_name = os.getenv("OPEN_AI_MODEL") or "openrouter/free"

NEW_LLM = ChatOpenAI(
    base_url="https://models.github.ai/inference",
    model="openai/gpt-4.1",
    api_key=api_key,
)


class CoderService(ServiceClass):
    def __init__(self):
        tools = [
            ReadFileTool(),
            WriteFileTool(),
            DeleteFileTool(),
            ListDirectoryTool(),
            EditFileTool(),
            RipGrepSearchTool(),
            TerminalTool(),
        ]
        self.chain = CODER_PROMPT | NEW_LLM.bind_tools(tools)

    def invoke(
        self,
        user_query: str,
        project_snapshot: ProjectSnapshot,
        plan: ExecutionPlan,
        conversation_history: list[BaseMessage],
    ):
        return self.chain.invoke(
            {
                "user_query": user_query,
                "project_snapshot": project_snapshot,
                "plan": plan,
                "history": conversation_history,
            }
        )
