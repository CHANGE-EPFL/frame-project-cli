"""Module for `frame show` commands."""

from json import JSONDecodeError

import requests
from rich.console import Console
from rich.panel import Panel

from .config import API_URL
from .utils import get_unit_id_and_version


def print_keywords(console: Console, keywords: list[str], style: str) -> None:
    """Print keywords in a Rich Console."""
    text = ""
    current_column = 0

    for keyword in keywords:
        width = len(keyword) + 3

        if current_column + width > console.width and text:
            console.print(text)
            text = ""
            current_column = 0

        text += f"[{style}] {keyword} [/] "
        current_column += width

    if text:
        console.print(text)


def print_pull_command(console: Console, command: str) -> None:
    console.print(Panel(command))


def show_remote_model(name: str) -> None:
    """Show information about a remote hybrid model."""
    id, version = get_unit_id_and_version(name)
    url = f"{API_URL}/hybrid_models/{id}"
    if version is not None:
        url += f"?model_version={version}"
    response = requests.get(url)

    if response.status_code == 404:
        print(f'Remote hybrid model "{name}" not found.')
        return

    if response.status_code != 200:
        print(f"Error fetching remote hybrid model ({response.status_code}). Check the API URL.")
        return

    try:
        info = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return

    console = Console()
    console.print("")
    console.print(info["name"], style="bold underline")
    console.print("Hybrid model")
    console.print("")
    console.print(", ".join(info["contributors"]))
    console.print("")
    console.print(info["description"])
    console.print("")
    print_keywords(console, info["keywords"], style="white on red")
    console.print("")

    if "created" in info and info["created"]:
        console.print(f"📅 Created on: {info['created']}")

    if "license" in info and info["license"]:
        console.print(f"📜 License: {info['license']}")

    console.print("")
    print_pull_command(console, f"frame pull model {name}")


def show_local_model(name: str) -> None:
    """Show information about a local hybrid model."""
    # TODO: implement
    print("Feature not implemented.")


def show_remote_component(name: str) -> None:
    """Show information about a remote component."""
    id, version = get_unit_id_and_version(name)
    url_physics_based = f"{API_URL}/components/physics_based/{id}"
    url_machine_learning = f"{API_URL}/components/machine_learning/{id}"
    if version is not None:
        url_physics_based += f"?component_version={version}"
        url_machine_learning += f"?component_version={version}"

    response = requests.get(url_physics_based)
    component_type = "Physics-based"

    if response.status_code == 404:
        response = requests.get(url_machine_learning)
        component_type = "Machine learning"

    if response.status_code == 404:
        print(f'Remote component "{name}" not found.')
        return

    if response.status_code != 200:
        print(f"Error fetching remote component ({response.status_code}). Check the API URL.")
        return

    try:
        info = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return

    console = Console()
    console.print("")
    console.print(info["name"], style="bold underline")
    console.print(f"{component_type} component")
    console.print("")
    console.print(", ".join(info["contributors"]))
    console.print("")
    console.print(info["description"])
    console.print("")
    print_keywords(
        console, info["keywords"], style="white on blue" if component_type == "Physics-based" else "white on cyan"
    )
    console.print("")

    if "created" in info and info["created"]:
        console.print(f"📅 Created on: {info['created']}")

    if "license" in info and info["license"]:
        console.print(f"📜 License: {info['license']}")

    console.print("")
    print_pull_command(console, f"frame pull component {name}")


def show_local_component(name: str, hybrid_model: str) -> None:
    """Show information about a local component."""
    # TODO: implement
    print("Feature not implemented.")
