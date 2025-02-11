from json import JSONDecodeError

import requests
import typer

from . import listing, pull
from .config import API_URL

app = typer.Typer(
    help="Frame tool to download hybrid models and setup environments.",
    no_args_is_help=True,
)

list_app = typer.Typer(
    help="List hybrid models or components.",
    no_args_is_help=True,
)
app.add_typer(list_app, name="list")

pull_app = typer.Typer(
    help="Download hybrid models or components and setup environment.",
    no_args_is_help=True,
)
app.add_typer(pull_app, name="pull")


@app.command()
def check() -> None:
    """Check the API access."""
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


@list_app.command("hybrid-models")
def list_models(
    remote: bool = typer.Option(False, help="List remote hybrid models."),
) -> None:
    """List installed and remote hybrid models."""
    if remote:
        listing.list_remote_models()
    else:
        listing.list_local_models()


@list_app.command("components")
def list_components(
    remote: bool = typer.Option(False, help="List remote components."),
    type: listing.ComponentType | None = typer.Option(None, help="Filter by component type."),
) -> None:
    """List installed and remote components."""
    print("Listing components.")
    if remote:
        listing.list_remote_components(type)
    else:
        listing.list_local_components(type)


@pull_app.command("hybrid-model")
def pull_model(
    name: str = typer.Argument(..., help="Hybrid model name."),
) -> None:
    """Download a hybrid model and seput environment."""
    pull.pull_model(name)


@pull_app.command("component")
def pull_component(
    name: str = typer.Argument(..., help="Component name."),
    hybrid_model: str = typer.Argument(..., help="Associated local hybrid model name."),
) -> None:
    """Download a component."""
    pull.pull_component(name, hybrid_model)


if __name__ == "__main__":
    app()
