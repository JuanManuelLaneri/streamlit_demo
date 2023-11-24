import os
import subprocess
import shutil
from typing import Optional

# Root directory for all staged repositories
STAGING_ROOT = "../.git_staging"


class CodeBranch:
    def __init__(self, repo_url: str, branch: str = "master") -> None:
        """
        Construct a new 'CodeBranch' object.

        :param repo_url: The URL of the Git repository
        :param branch: The specific branch of the Git repository to work with
        """
        self.repo_url = repo_url
        self.branch = branch

        # The identifier uniquely identifies the repository and branch,
        # it's derived from the last part of the repo_url and the branch name
        self.identifier = f"{repo_url.split('/')[-1].replace('.git', '')}_{branch}"

        self.staging_area = os.path.join(os.path.abspath(STAGING_ROOT), self.identifier)

        # Ensures the staging directory exists
        os.makedirs(self.staging_area, exist_ok=True)

    def clone(self) -> Optional[str]:
        """
        Clone the Git repository on the specific branch to the staging area.

        :return: The local path to the cloned repository or None if cloning fails
        """
        try:
            # Cloning the Git repository to target staging_area directly
            print(self.branch)
            print(self.repo_url)
            print(self.staging_area)

            subprocess.run(
                ["git", "clone", "-b", self.branch, self.repo_url, self.staging_area],
                check=True,
            )
            print(f"Repository cloned to {self.staging_area}")
            return self.staging_area
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository: {e}")
            return None

    def get_cloned_repo_root(self) -> str:
        """
        Returns the local path to the root of the cloned repository.

        :return: The local path to the cloned repository
        """
        return self.staging_area

    def cleanup(self) -> None:
        """
        Cleans up (deletes) the locally cloned repository if it exists.
        """
        if os.path.exists(self.staging_area):
            shutil.rmtree(self.staging_area)
            print(f"Cleaned up {self.staging_area}")
        else:
            print(f"{self.staging_area} does not exist")


# Example usage:
# branch = CodeBranch('https://github.com/someuser/somerepo.git', 'main')
# repo_dir = branch.clone()
# print(branch.get_cloned_repo_root())  # prints the root path of the cloned directory
# branch.cleanup()
