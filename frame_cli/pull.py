"""Module for `frame pull` commands."""

from typing import Any

from .downloaders.git import GitDownloader
from .environment_managers.environment_manager import get_environment_manager
from .info import add_local_model_info
from .utils import retrieve_model_info, retrieve_component_info


def setup_environment(destination: str, environment: dict[str, Any]) -> None:
    environment_manager = get_environment_manager(environment["type"])

    if environment_manager is None:
        print(f"Cannot setup environment of type {environment['type']}. Skipping...")
        return

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


def pull_component(name: str, destination: str | None) -> None:
    """Download a component."""
    info, _ = retrieve_component_info(name)
    if info is None:
        return

    url = info.get("url", None)

    if url is None:
        print("Error retrieving the component URL.")
        return

    downloader = GitDownloader()
    destination = downloader.download(url, destination)
    # TODO: save info to local
