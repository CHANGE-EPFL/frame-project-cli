"""Module for `frame pull` commands."""

from json import JSONDecodeError
from typing import Any

import requests

from .config import API_URL
from .downloaders.git import GitDownloader
from .environment_managers.python_requirements import PythonRequirementsEnvironmentManager
from .info import add_local_model_info
from .utils import get_unit_id_and_version


def retrieve_model_info(name: str) -> dict[str, Any] | None:
    """Retrieve online info of a hybrid model."""

    id, version = get_unit_id_and_version(name)
    url = f"{API_URL}/hybrid_models/{id}"
    if version is not None:
        url += f"?model_version={version}"
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


def setup_environment(destination: str, environment: dict[str, Any]) -> None:
    # TODO: Automate choice of environment manager subclass from environment["type"]
    if environment["type"] == "python_requirements":
        environment_manager = PythonRequirementsEnvironmentManager()
        environment_manager.setup(
            destination,
            environment["file_paths"],
        )


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
    add_local_model_info(name, url, destination)

    computational_environment = info.get("computational_environment", [])
    if computational_environment:
        print("Setting up computational environment...")
        for environment in computational_environment:
            setup_environment(destination, environment)

    if "documentation" in info and info["documentation"]:
        print("For further information about the hybrid model's usage, please refer to its documentation:")
        for link in info["documentation"]:
            print(link)


def pull_component(name: str, model: str) -> None:
    """Download a component."""
    # TODO: implement
    print("Feature not implemented.")
