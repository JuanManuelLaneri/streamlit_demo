import os
from dotenv import load_dotenv
from code_indexer import index_repository

load_dotenv()



def main() -> None:
    # List of repository URLs you want to process
    repo_urls = [

        # ... add any other repo URLs here
    ]

    # Loop over each repository URL and call index_repository
    for repo_url in repo_urls:
        index_repository(
            repo_url=repo_url,
            branch="master",
        )

if __name__ == "__main__":
    main()
