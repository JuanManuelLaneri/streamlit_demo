import os
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language, Document
from langchain.document_loaders import TextLoader
from code_branch import CodeBranch
from embedder import Embedder


def crawl_documents(path: str) -> List[str]:
    """
    Function to crawl documents in the directory path provided
    Args:
        path (str): Directory path

    Returns:
        List[str]: List of document paths
    """
    documents: List[str] = []
    # Traverse the directories
    for root, _, files in os.walk(path):
        for file in files:
            # Append each file to the documents list
            documents.append(os.path.join(root, file))
    return documents


def get_document_chunks(doc_path: str) -> List[Document]:
    """
    Function to split documents into chunks
    Args:
        doc_path (str): Document path

    Returns:
        List[Document]: List of split Documents
    """
    # Load document from the path
    loader = TextLoader(doc_path, encoding="utf-8")
    docs = loader.load()

    # Initialize text splitter
    # splitter = RecursiveCharacterTextSplitter.from_language(
    #     language=Language.PYTHON, chunk_size=1000, chunk_overlap=200
    # )

    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=4000, chunk_overlap=200
    )



    # Split document into chunks
    return splitter.split_documents(docs)


def index_repository(repo_url: str, branch: str = "master") -> None:
    """
    Function to index repository
    Args:
        repo_url (str): Repository URL
        branch (str, optional): Branch name. Defaults to 'master'.
    """
    codes = CodeBranch(repo_url=repo_url, branch=branch)
    # Cleanup any existing data related to this repository
    codes.cleanup()
    # Clone the repository
    codes.clone()

    # Get all the documents in the cloned repository
    documents = crawl_documents(codes.get_cloned_repo_root())

    # Filter out Python source documents
    # python_documents = [
    #     doc for doc in documents if doc.endswith(".py")
    # ]

    sql_documents = [
        doc for doc in documents if doc.endswith(".sql")
    ]

    embedder = Embedder()
    # Process only top 3 documents
    # TODO: Consider extending functionality to index more than just the first document.
    total_documents = len(documents)

    # Filter out the secret-production.json and secrets-performance.json files
    filtered_documents = [
        doc for doc in documents if (
            doc.endswith((".py", ".json", "Jenkinsfile", ".Dockerfile", ".config", ".tf", '.txt', '.md', '.yml', '.sql')) and not (
            doc.endswith(("secrets/secrets-production.json", "secrets/secrets-performance.json",
                          "secrets/secrets-staging.json", ".gpg", ".git/index"))
        )
        )
    ]

    # print("documents", documents)
    for index, document in enumerate(sql_documents, start=1):
    # for index, document in enumerate(filtered_documents, start=1):
        print(
            f"Processing document {index}/{total_documents} at {document}",
        )
        chunks = get_document_chunks(document)
        embedder.embed(chunks)

        # TODO: Add functionality to save chunks (embedded documents) to a database.

    # Cleanup after indexing
    codes.cleanup()
