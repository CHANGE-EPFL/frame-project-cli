from enum import Enum
from json import JSONDecodeError

import requests
from rich.console import Console
from rich.table import Table

from .config import API_URL


class ComponentType(str, Enum):
    physics_based = "physics-based"
    machine_learning = "machine-learning"


def list_remote_models() -> None:
    """List remote hybrid models."""
    url = f"{API_URL}/hybrid_models/ids/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching remote hybrid models ({response.status_code}). Check the API URL.")
        return

    try:
        models = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return

    title = "Remote hybrid models"
    table = Table(title=title, min_width=len(title) + 4)
    table.add_column("Name")
    for model in models:
        table.add_row(model)

    console = Console()
    console.print("")
    console.print(table)


def list_local_models() -> None:
    """List installed hybrid models."""
    # TODO: implement
    print("Feature not implemented.")
    print("Run with `--remote` to list remote hybrid models.")


def list_remote_components(type: ComponentType | None) -> None:
    """List remote components."""
    url = f"{API_URL}/components/"
    match type:
        case None:
            url += "ids/"
        case ComponentType.physics_based:
            url += "physics_based_ids/"
        case ComponentType.machine_learning:
            url += "machine_learning_ids/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching remote components ({response.status_code}). Check the API URL.")
        return

    try:
        models = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return

    match type:
        case None:
            title = "Remote components"
        case ComponentType.physics_based:
            title = "Remote physics-based components"
        case ComponentType.machine_learning:
            title = "Remote machine-learning components"
    table = Table(title=title, min_width=len(title) + 4)
    table.add_column("Name")
    for model in models:
        table.add_row(model)

    console = Console()
    console.print("")
    console.print(table)


def list_local_components(type: ComponentType | None) -> None:
    """List installed components."""
    # TODO: implement
    print("Feature not implemented.")
    print("Run with `--remote` to list remote components.")
