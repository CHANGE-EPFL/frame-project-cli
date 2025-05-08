"""Module containing the GitDownloader class."""

from git import Repo
from rich.status import Status

from ..logging import logger
from .downloader import Downloader


class GitDownloader(Downloader):
    """Downloader for Git repositories."""

    def download(
        self,
        url: str,
        destination: str | None = None,
        branch: str | None = None,
    ) -> str:
        """Download the content at the given URL (https or git protocol).

        Args:
            url (str): URL of the content to download.
            destination (str): Destination directory to save the content to. Defaults to None, which infers the
                destination from the URL (repository name).
            branch (str): Branch to checkout after cloning. Defaults to None, which checks out the default
                branch.

        Returns:
            str: The destination directory.

        Raises:
            GitCommandError: The Git command failed.
        """
        if destination is None:
            destination = url.split("/")[-1].replace(".git", "")

        message = f'Cloning "{url}" into "{destination}"...'
        logger.debug(message)
        with Status(message):
            Repo.clone_from(url, destination, branch=branch)

        logger.info(f'Cloned "{url}" into "{destination}"')

        return destination
