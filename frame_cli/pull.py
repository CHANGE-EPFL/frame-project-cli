"""Module for `frame-cli pull` commands."""

from json import JSONDecodeError

import requests

from .config import API_URL
from .downloaders.git import GitDownloader
from .info import add_local_model_info


def retrieve_model_url(name: str) -> str | None:
    """Retrieve the URL of a hybrid model."""

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

    return info["url"]


def pull_model(name: str, destination: str | None) -> None:
    """Download a hybrid model and seput environment."""
    url = retrieve_model_url(name)
    if url is None:
        print("Error retrieving the model URL.")
        return

    # TODO: Detect which downloader to use
    downloader = GitDownloader()
    destination = downloader.download(url, destination)
    add_local_model_info(name, destination)


def pull_component(name: str, model: str) -> None:
    """Download a component."""
    # TODO: implement
    print("Feature not implemented.")
