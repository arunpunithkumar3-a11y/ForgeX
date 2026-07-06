from metadata_extractor import extract_metadata_from_file
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from utils import embeddings

from langchain_core.documents import Document


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




def build_index(root_dir: str = "."):
    docs = []

    main_path = os.path.abspath(root_dir)

    IGNORE_DIRS = {
        ".git",
        "__pycache__",
        "venv",
        ".venv",
        "node_modules",
        "chroma_db",
    }

    for root, dirs, files in os.walk(root_dir):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for file in files:

            if not file.endswith(".py"):
                continue

            file_abs_path = os.path.join(root, file)

            file_rel_path = (
                os.path.relpath(
                    file_abs_path,
                    main_path
                )
                .replace("\\", "/")
            )

            data = extract_metadata_from_file(
                file_abs_path
            )

            docs.extend(
                clean_file_metadata_for_vector_db(
                    data,
                    file_path=file_rel_path,
                )
            )

    vector_store = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="./chroma_db",
    )

    return vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 6},
    )
if __name__ =="__main__":
    r = build_index()
    print(r.invoke("i need nodes.py"))
