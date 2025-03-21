"""Module for `frame-cli pull` commands."""

from json import JSONDecodeError
import os
import subprocess
from typing import Any

import requests
from rich.console import Console
from rich.panel import Panel

from .config import API_URL
from .downloaders.git import GitDownloader
from .info import add_local_model_info


def retrieve_model_info(name: str) -> dict[str, Any] | None:
    """Retrieve online info of a hybrid model."""

    url = f"{API_URL}/hybrid_models/{name}"
    response = requests.get(url)

    if response.status_code == 404:
        print(f'Remote hybrid model "{name}" not found.')
        return None

    if response.status_code != 200:
        print(f"Error fetching remote hybrid model ({response.status_code}). Check the API URL.")
        return None

    try:
        info = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return None

    return info


# TODO: Create a class for computational environments, with setup method
def setup_environment(environment: dict[str, Any]) -> None:
    console = Console()

    if environment["type"] == "python_requirements":
        console.print("Setting up Python environment...")
        subprocess.run(["uv", "venv"])
        subprocess.run(["uv", "pip", "install", "pip"])
        for requirement_path in environment["file_paths"]:
            subprocess.run(["uv", "pip", "install", "-r", requirement_path])

        console.print("Python environment setup complete. Activate it from the model's root directory with")
        console.print(Panel("source .venv/bin/activate"))


def pull_model(name: str, destination: str | None) -> None:
    """Download a hybrid model and setup environment."""
    info = retrieve_model_info(name)
    if info is None:
        return

    url = info.get("url", None)

    if url is None:
        print("Error retrieving the model URL.")
        return

    # TODO: Detect which downloader to use
    downloader = GitDownloader()
    destination = downloader.download(url, destination)
    add_local_model_info(name, destination)

    computational_environment = info.get("computational_environment", [])
    if computational_environment:
        os.chdir(destination)
        print("Setting up computational environment...")
        for environment in computational_environment:
            setup_environment(environment)


def pull_component(name: str, model: str) -> None:
    """Download a component."""
    # TODO: implement
    print("Feature not implemented.")
