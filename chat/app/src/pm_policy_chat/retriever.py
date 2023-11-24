from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.agents.agent_toolkits import (
    VectorStoreInfo,
    VectorStoreToolkit,
    create_vectorstore_agent,
)
from langchain.embeddings.openai import OpenAIEmbeddings

# Alternatively, you can create it from environment variables.
import os


def get_retriever():
    match os.environ.get("RETRIEVER_MODE", "langchain_retriever"):
        case "langchain_retriever":
            return get_retriever_langchain()
        case "llama_index_retriver":
            raise NotImplementedError


def get_retriever_langchain():
    PGVECTOR_CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver=os.environ.get("PGVECTOR_DRIVER", "psycopg2"),
        host=os.environ.get("PGVECTOR_HOST", "localhost"),
        port=int(os.environ.get("PGVECTOR_PORT", "5432")),
        database=os.environ.get("PGVECTOR_DATABASE", "postgres"),
        user=os.environ.get("PGVECTOR_USER", "postgres"),
        password=os.environ.get("PGVECTOR_PASSWORD", "postgres"),
    )

    embeddings = OpenAIEmbeddings()
    store = PGVector.from_existing_index(embedding=embeddings, kwargs={"connection_string": PGVECTOR_CONNECTION_STRING})

    vectorstore_info = VectorStoreInfo(
        name="credit_variable_architect",
        description="This tool provides help for Credit Variables engineer to build solutions for the team.",
        vectorstore=store,
    )

    return VectorStoreToolkit(vectorstore_info=vectorstore_info)

    # kwargs = {"connection_string": PGVECTOR_CONNECTION_STRING}
    # PGVector.from_existing_index(embedding=embeddings, **kwargs)
