import os

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from forgeX.core.agents.backend import ServiceClass
from forgeX.core.agents.prompts import CODER_PROMPT
from forgeX.core.agents.Schemas import ExecutionPlan, ProjectSnapshot

load_dotenv()

api_key = (
    os.environ.get("OPEN_AI_KEY") or os.environ.get("OPENAI_API_KEY") or "dummy_key"
)

LLM = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    api_key=api_key,
)


class CoderService(ServiceClass):
    def __init__(self):
        self.chain = CODER_PROMPT | LLM

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
