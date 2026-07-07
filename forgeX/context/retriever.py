import os

from langchain_community.vectorstores import Chroma

from metadata_extractor import extract_metadata_from_file
from utils import IGNORE_DIRS, clean_file_metadata_for_vector_db, embeddings


class Retriever:
    def __init__(self, query: str, root_dir: str = "."):
        self.docs = []
        self.query = query
        self.root_dir = root_dir
        self.main_path = os.path.abspath(root_dir)

    def retriever_node(self):
        if os.path.exists("./chroma_db"):
            vector_store = Chroma(
                persist_directory="./chroma_db", embedding_function=embeddings
            )
        else:
            vector_store = Chroma.from_documents(
                self.docs, embeddings, persist_directory="./chroma_db"
            )
        return vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 6},
        )

    def build(self):
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                if not file.endswith(".py"):
                    continue
                file_abs_path = os.path.join(root, file)
                file_rel_path = os.path.relpath(file_abs_path, self.main_path).replace(
                    "\\", "/"
                )
            data = extract_metadata_from_file(file_abs_path)
            self.docs.extend(
                clean_file_metadata_for_vector_db(
                    data,
                    file_path=file_rel_path,
                )
            )
        retriever = self.retriever_node()
        final_docs = retriever.invoke(self.query)
        return final_docs
