from prompts import PLANNER_PROMPT
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from agents.Schemas import FileInfo,ProjectSnapshot
from agents.Schemas import ExecutionPlan
parser = PydanticOutputParser(pydantic_object=ExecutionPlan)
import os 

planner_llm   = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

class Planner:
    def __init__(
        self,
        query: str,
        snapshot: ProjectSnapshot,
    ):
        self.query = query
        self.snapshot =  snapshot

        self.chain = (
            PLANNER_PROMPT.partial(
                format_instructions=
                parser.get_format_instructions()
            )
            | planner_llm
            | parser
        )

    def plan(self):
        try:
            return self.chain.invoke(
                {
                    "user_query": self.query,
                    "project_snapshot": self.snapshot,
                }
            )

        except Exception as e:
            return e

