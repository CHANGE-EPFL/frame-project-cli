"""Module containing the JuliaEnvironmentManager class."""

import os
import subprocess

from rich.console import Console
from rich.panel import Panel

from .environment_manager import EnvironmentManager


class JuliaEnvironmentManager(EnvironmentManager):
    """Environment manager for Julia."""

    type = "julia"

    def setup(self, destination: str, file_paths: list[str], *args, **kwargs) -> None:
        """Set up the environment for the hybrid model.

        Args:
            destination (str): Hybrid model destination directory where the environment is set up.
            file_paths (list[str]): List of paths to files that describe the environment.
        """
        os.chdir(destination)
        console = Console()
        console.print("Setting up Julia environment...")

        try:
            subprocess.run(["julia", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("Julia installation not found. Please install Julia to create an environment for this model.")
            return

        console.print("Setting up Julia environment using Project.toml...")
        subprocess.run(["julia", "-e", 'using Pkg; Pkg.activate("."); Pkg.instantiate()'])

        console.print("Julia environment setup complete. Use it from the model's root directory with")
        activation_message = f"cd {destination}\njulia --project=."
        console.print(Panel(activation_message))
