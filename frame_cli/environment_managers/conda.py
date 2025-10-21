"""Module containing the CondaEnvironmentManager class."""

import os
import subprocess

from rich.console import Console
from rich.panel import Panel

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

        conda_commands = ["conda", "mamba", "micromamba"]
        conda_command = None

        for conda_command in conda_commands:
            try:
                subprocess.run([conda_command, "--version"], check=True, capture_output=True)  # type: ignore
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                conda_command = None

        if conda_command is None:
            console.print(
                "No Conda (or equivalent) installation found. Please install Conda, Mamba, or Micromamba to create an environment for this model."
            )
            return

        console.print("Setting up Conda environment...")
        for file_path in file_paths:
            if not os.path.isfile(file_path):
                console.print(f"File {file_path} does not exist. Skipping...")
                continue
            if file_path.endswith((".yml", ".yaml")):
                subprocess.run([conda_command, "env", "create", "-f", file_path, "--prefix", "./.venv", "-y"])
                console.print(f"Conda environment setup from {file_path} complete. Skipping remaining files...")
                break
            else:
                console.print(f"Unsupported file {file_path}. Skipping...")

        console.print("Conda environment setup complete. Activate it from the model's root directory with")
        activation_message = f"cd {destination}\n{conda_command} activate ./.venv"
        console.print(Panel(activation_message))
