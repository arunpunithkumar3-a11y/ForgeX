import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from agents.prompts import PLANNER_PROMPT
from langchain_core.output_parsers import PydanticOutputParser
from agents.Schemas import ExecutionPlan

load_dotenv()

planner_llm = ChatOpenAI(
    model = os.getenv('OPEN_AI_MODEL'),
    base_url = os.getenv('MODEL_BASE_URL'),
    api_key = os.getenv('OPEN_AI_KEY'),
)

parser = PydanticOutputParser(pydantic_object=ExecutionPlan)

chain = (
    PLANNER_PROMPT.partial(
        format_instructions=parser.get_format_instructions()
    )
    | planner_llm
    | parser
)

if __name__ == '__main__':
    res = chain.invoke({
        'user_query': 'update the MetadataVisitor class in metadata_extractor.py to handle async functions',
        'project_snapshot': "root_path='C:\\Users\\DVS\\OneDrive\\Desktop\\hackerrank' files=[FileInfo(path='metadata_extractor.py', extension='.py', size_bytes=6563, lines_count=254)] directories=[] total_files=1 total_directories=0"
    })
    print(res)
