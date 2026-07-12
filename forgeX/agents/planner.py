import os

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from forgeX.agents.prompts import PLANNER_PROMPT
from forgeX.agents.Schemas import ExecutionPlan, ProjectSnapshot

load_dotenv()

# Set a fallback dummy key if not present in environment to prevent import-time failure
api_key = (
    os.environ.get("OPEN_AI_KEY") or os.environ.get("OPENAI_API_KEY") or "dummy_key"
)

planner_llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
    api_key=api_key,
)


class Planner:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=ExecutionPlan)
        self.chain = PLANNER_PROMPT | planner_llm | self.parser

    def plan(self, query: str, snapshot: ProjectSnapshot):
        try:
            return self.chain.invoke(
                {"user_query": query, "project_snapshot": snapshot}
            )
        except Exception:
            return None
