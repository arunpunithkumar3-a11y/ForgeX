from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document

from forgeX.tools.sandbox.docker_backend import DockerBackend
from forgeX.tools.sandbox.models import SandboxConfig

load_dotenv()
"""
embeddings = OpenAIEmbeddings(
    model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
    openai_api_key=os.environ.get("OPEN_AI_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    encoding_format="float",
    check_embedding_ctx_length=False,
)
"""


def clean_file_metadata_for_vector_db(
    file_metadata,
    file_path: str = "unknown",
):
    documents = []

    if not file_metadata or not file_metadata.symbols:
        return documents

    for symbol in file_metadata.symbols:
        name = symbol.full_name or symbol.name
        symbol_type = symbol.symbol_type or ""

        args = symbol.args or []
        calls = symbol.calls or []

        decorators = symbol.decorators or []
        bases = symbol.bases or []

        parent_symbol = symbol.parent_symbol or ""
        return_type = symbol.return_type or ""

        docstring = symbol.docstring or ""
        code = (symbol.code or "").strip()

        if not code or len(code) < 20:
            continue

        code = code[:1500]

        text = f"""
Name: {name}
Type: {symbol_type}
File: {file_path}

Parent Symbol: {parent_symbol}

Arguments:
{", ".join(args)}

Return Type:
{return_type}

Decorators:
{", ".join(decorators)}

Base Classes:
{", ".join(bases)}

Calls:
{", ".join(calls)}

Description:
{docstring}

Code:
{code}
""".strip()

        metadata = {
            "name": name,
            "type": symbol_type,
            "file": file_path,
            "parent_symbol": parent_symbol,
            "return_type": return_type,
            "decorators": ",".join(decorators),
            "bases": ",".join(bases),
            "calls": ",".join(calls),
            "line_start": symbol.line_start,
            "line_end": symbol.line_end,
        }

        documents.append(
            Document(
                page_content=text,
                metadata=metadata,
            )
        )

    return documents


IGNORE_DIRS = [
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "dist",
    "build",
    ".next",
    ".pytest_cache",
    ".mypy_cache",
    "site-packages",
    ".idea",
    ".vscode",
    "coverage",
    ".tox",
    "target",
    "vendor",
    ".cache",
    "egg-info",
]

IGNORE_FILES = [
    ".env",
    ".env.local",
    ".env.production",
]

IGNORE_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".exe",
    ".dll",
    ".so",
    ".bin",
]


def Activate_Container(image_name: str):
    """
    Activate the Docker container for the sandbox environment.
    This function checks if the container is already running and starts it if necessary.
    """

    config = SandboxConfig(
        image=image_name,
        container_name="sandbox_container",
        working_directory="/workspace",
        workspace=Path.cwd(),
        auto_remove=True,
    )
    backend = DockerBackend(config)
    backend.start()
    return None


if __name__ == "__main__":
    Activate_Container("python:3.12-slim")
