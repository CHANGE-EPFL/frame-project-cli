"""Module containing the Downloader abstract base class."""

from abc import ABC, abstractmethod
from typing import Optional


class Downloader(ABC):
    """Abstract base class for downloaders."""

    @abstractmethod
    def download(
        self,
        url: str,
        dest: Optional[str] = None,
    ) -> None:
        """Download the content at the given URL.

        Args:
            url (str): The URL of the content to download.
            dest (str): The destination directory to save the content to. Defaults to None, which creates a new
                directory from the repository name.
        """
        pass
