"""Module containing the EnvironmentManager abstract base class."""

from abc import ABC, abstractmethod


class EnvironmentManager(ABC):
    """Abstract base class for environment managers."""

    type: str

    @abstractmethod
    def setup(self, destination: str, file_paths: list[str], *args, **kwargs) -> None:
        """Set up the environment for the hybrid model.

        Args:
            destination (str): Hybrid model destination directory where the environment is set up.
            file_paths (list[str]): List of paths to files that describe the environment.
        """
