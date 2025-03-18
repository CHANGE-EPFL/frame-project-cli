"""Check installation and API access."""

from json import JSONDecodeError
import shutil

import requests

from .config import API_URL


def check() -> None:
    """Check installation and API access."""
    check_api()
    check_uv()


def check_api() -> None:
    """Check API access."""

    url = f"{API_URL}/healthz"
    response = requests.get(url)
    if response.status_code != 200:
        print("API is not accessible. Check the API URL.")
        return

    try:
        data = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return

    if "status" not in data or data["status"] != "OK":
        print("API is not healthy.")
        return

    print("API is healthy.")


def check_uv() -> None:
    """Check that uv is installed."""

    if shutil.which("uv") is None:
        print(
            "uv is not installed. Please install it to use Frame CLI:\nhttps://docs.astral.sh/uv/guides/install-python/"
        )
    else:
        print("uv is installed.")
