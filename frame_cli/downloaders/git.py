"""Module containing the GitDownloader class."""

from typing import Optional

from git import Repo

from ..logging import logger
from .downloader import Downloader


class GitDownloader(Downloader):
    """Downloader for Git repositories."""

    def download(
        self,
        url: str,
        dest: Optional[str] = None,
        branch: Optional[str] = None,
    ) -> None:
        """Download the content at the given URL (https or git protocol).

        Args:
            url (str): The URL of the content to download.
            dest (str): The destination directory to save the content to. Defaults to None, which infers the
                destination from the URL.
            branch (str): The branch to checkout after cloning. Defaults to None, which checks out the default
                branch.

        Raises:
            GitCommandError: If the Git command fails.
        """
        if dest is None:
            dest = url.split("/")[-1].replace(".git", "")

        logger.debug(f'Cloning "{url}" into "{dest}"')
        Repo.clone_from(url, dest, branch=branch)
