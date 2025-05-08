"""Check installation and API access."""

from json import JSONDecodeError
import shutil

import requests

from .config import API_URL


def check() -> None:
    """Check installation and API access."""
    check_api()
    check_uv()
    check_git()


def check_api() -> None:
    """Check API access."""

    url = f"{API_URL}/healthz"
    try:
        response = requests.get(url)
    except Exception:
        print("API is not accessible. Check the API URL.")
        return

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
            "uv is not installed. Please install it to use Frame CLI:\nhttps://docs.astral.sh/uv/getting-started/installation/"
        )
    else:
        print("uv is installed.")


def check_git() -> None:
    """Check that git is installed."""

    if shutil.which("git") is None:
        print("git is not installed.")
    else:
        print("git is installed.")
