"""Module containing the GitDownloader class."""

from typing import Optional

from git import Repo
from rich.status import Status

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
            url (str): URL of the content to download.
            dest (str): Destination directory to save the content to. Defaults to None, which infers the
                destination from the URL (repository name).
            branch (str): Branch to checkout after cloning. Defaults to None, which checks out the default
                branch.

        Raises:
            GitCommandError: The Git command failed.
        """
        if dest is None:
            dest = url.split("/")[-1].replace(".git", "")

        message = f'Cloning "{url}" into "{dest}"...'
        logger.debug(message)
        with Status(message):
            Repo.clone_from(url, dest, branch=branch)

        logger.info(f'Cloned "{url}" into "{dest}"')
