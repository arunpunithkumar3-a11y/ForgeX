import os
import sys

# Add the project root to sys.path to resolve module imports when run directly as a script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from forgeX.agents.prompts import PLANNER_PROMPT
from forgeX.agents.Schemas import ExecutionPlan, ProjectSnapshot
from forgeX.tools.sandbox.docker_image import get_image
from utils import Activate_Container

parser = PydanticOutputParser(pydantic_object=ExecutionPlan)

planner_llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    model="Qwen/Qwen3-Coder-30B-A3B-Instruct",
    api_key=os.environ.get("OPEN_AI_KEY"),
)


class Planner:
    def __init__(
        self,
        query: str,
        snapshot: ProjectSnapshot,
    ):
        self.query = query
        self.snapshot = snapshot

        self.chain = (
            PLANNER_PROMPT.partial(format_instructions=parser.get_format_instructions())
            | planner_llm
            | parser
        )

    def plan(self):
        try:
            result = self.chain.invoke(
                {
                    "user_query": self.query,
                    "project_snapshot": self.snapshot,
                }
            )
            image_name = get_image(language=result.Environment)
            Activate_Container(image_name=image_name)

            return result

        except Exception:
            return None


if __name__ == "__main__":
    plan = Planner(
        query="update the MetadataVisitor class in metadata_extractor.py to handle async functions",
        snapshot="root_path='C:\\Users\\DVS\\OneDrive\\Desktop\\hackerrank' files=[FileInfo(path='metadata_extractor.py', extension='.py', size_bytes=6563, lines_count=254)] directories=[] total_files=1 total_directories=0",
    )
    print(plan.plan())
