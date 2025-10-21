"""Module containing the PythonEnvironmentManager class."""

import os
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel

from .environment_manager import EnvironmentManager


class PythonEnvironmentManager(EnvironmentManager):
    """Environment manager for Python."""

    type = "python"

    def setup(self, destination: str, file_paths: list[str], *args, **kwargs) -> None:
        """Set up the environment for the hybrid model.

        Args:
            destination (str): Hybrid model destination directory where the environment is set up.
            file_paths (list[str]): List of paths to files that describe the environment.
        """
        os.chdir(destination)
        console = Console()
        console.print("Setting up Python environment...")
        subprocess.run(["uv", "venv"])
        subprocess.run(["uv", "pip", "install", "pip"])

        for file_path in file_paths:
            if not os.path.isfile(file_path):
                console.print(f"File {file_path} does not exist. Skipping...")
                continue
            if file_path == "pyproject.toml":
                subprocess.run(["uv", "pip", "install", "-e", "."])
            elif file_path.endswith(".txt"):
                subprocess.run(["uv", "pip", "install", "-r", file_path])
            else:
                console.print(f"Unsupported file {file_path}. Skipping...")

        console.print("Python environment setup complete. Activate it from the model's root directory with")
        activation_message = f"cd {destination}\n"

        if sys.platform == "win32":
            activation_message += ".venv\\Scripts\\activate"
        else:
            activation_message += "source .venv/bin/activate"

        console.print(Panel(activation_message))
