import os

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser

from forgeX.core.agents.backend import ServiceClass
from forgeX.core.agents.prompts import PLANNER_PROMPT
from forgeX.core.agents.Schemas import ExecutionPlan, ProjectSnapshot

load_dotenv()
from langchain_openai import ChatOpenAI

api_key = (
    os.environ.get("OPEN_AI_KEY") or os.environ.get("OPENAI_API_KEY") or "dummy_key"
)


planner_llm = ChatOpenAI(
    base_url="https://models.github.ai/inference",
    model="openai/gpt-4.1",
    api_key=api_key,
)


class PlannerService(ServiceClass):
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=ExecutionPlan)
        self.chain = PLANNER_PROMPT | planner_llm | self.parser

    def invoke(self, query: str, snapshot: ProjectSnapshot):
        return self.chain.invoke(
            {
                "user_query": query,
                "project_snapshot": snapshot,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
