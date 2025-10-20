"""Module containing the CondaEnvironmentManager class."""

import os

from rich.console import Console

from .environment_manager import EnvironmentManager


class CondaEnvironmentManager(EnvironmentManager):
    """Environment manager for Conda."""

    type = "conda"

    def setup(self, destination: str, file_paths: list[str], *args, **kwargs) -> None:
        """Set up the environment for the hybrid model.

        Args:
            destination (str): Hybrid model destination directory where the environment is set up.
            file_paths (list[str]): List of paths to files that describe the environment.
        """
        os.chdir(destination)
        console = Console()
        console.print("Setting up of Conda environment not implemented. Skipping...")
