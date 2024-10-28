"""Module containing the Downloader abstract base class."""

from abc import ABC, abstractmethod
from typing import Optional


class Downloader(ABC):
    """Abstract base class for downloaders."""

    @abstractmethod
    def download(
        self,
        url: str,
        *args,
        dest: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Download the content at the given URL.

        Args:
            url (str): URL of the content to download.
            dest (str): Destination directory to save the content to. Defaults to None, which creates a new
                directory from the repository name.
        """
