import os
from typing import Iterable

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.schema.vectorstore import VectorStoreRetriever
from langchain.vectorstores.pgvector import PGVector


class Embedder:
    def __init__(self) -> None:
        return

    def embed(self, texts: Iterable[Document]) -> VectorStoreRetriever:
        texts_without_nulls = []
        for text in texts:
            if '\0' in text.page_content:
                print(f"String contains a NUL character, discarding it. {text.page_content}")
            else:
                texts_without_nulls.append(text)

        print(f"About to embed {len(texts_without_nulls)} documents/chunks")
        # embed
        connection_string = PGVector.connection_string_from_db_params(
            driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
            host=os.environ.get("PGVECTOR_HOST", "localhost"),
            port=int(os.environ.get("PGVECTOR_PORT", "5432")),
            database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
            user=os.environ.get("PGVECTOR_USER", "postgres"),
            password=os.environ.get("PGVECTOR_PASSWORD", "example"),
        )
        db = PGVector.from_documents(texts_without_nulls,
                                     OpenAIEmbeddings(disallowed_special=()),
                                     connection_string=connection_string)
        return db.as_retriever(
            search_type="mmr",  # Also test "similarity"
            search_kwargs={"k": 5},
        )

