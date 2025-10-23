"""Module for `frame pull` commands."""

from typing import Any

import requests

from .downloaders.git import GitDownloader
from .environment_managers.environment_manager import get_environment_manager
from .info import add_local_model_info
from .metadata import metadata_file_exists
from .utils import retrieve_model_info, retrieve_component_info
from .config import FRAME_METADATA_FILE_NAME, API_URL
from .logging import logger


def setup_environment(destination: str, environment: dict[str, Any]) -> None:
    environment_manager = get_environment_manager(environment["type"])

    if environment_manager is None:
        logger.info(f"Cannot setup environment of type {environment['type']}. Skipping...")
        return

    environment_manager.setup(
        destination,
        environment["file_paths"],
    )


def pull_metadata_file(model_id: str, model_version: str | None, dir_path: str) -> None:
    """Download FRAME metadata file."""
    url = f"{API_URL}/hybrid_models/metadata_file/{model_id}"
    if model_version is not None:
        url += f"?model_version={model_version}"

    response = requests.get(url)
    if response.status_code != 200:
        logger.error(f"Error retrieving FRAME metadata file. ({response.status_code}, {url})")
        return

    with open(f"{dir_path}/{FRAME_METADATA_FILE_NAME}", "wb") as f:
        f.write(response.content)


def pull_model(name: str, destination: str | None) -> None:
    """Download a hybrid model and setup environment."""
    info = retrieve_model_info(name)
    if info is None:
        return

    url = info.get("url", None)

    if url is None:
        logger.error("Error retrieving the model URL.")
        return

    downloader = GitDownloader()
    destination = downloader.download(url, destination)
    add_local_model_info(name, url, destination)

    computational_environment = info.get("computational_environment", [])
    if computational_environment:
        logger.info("Setting up computational environment...")
        for environment in computational_environment:
            setup_environment(destination, environment)

    if "documentation" in info and info["documentation"]:
        print("For further information about the hybrid model's usage, please refer to its documentation:")
        for link in info["documentation"]:
            print(link)

    if not metadata_file_exists():
        logger.info("Downloading FRAME metadata file...")
        pull_metadata_file(info.get("id", ""), info.get("version", None), destination)

    logger.info("Done!")


def pull_component(name: str, destination: str | None) -> None:
    """Download a component."""
    info, _ = retrieve_component_info(name)
    if info is None:
        return

    url = info.get("url", None)

    if url is None:
        logger.error("Error retrieving the component URL.")
        return

    downloader = GitDownloader()
    destination = downloader.download(url, destination)
