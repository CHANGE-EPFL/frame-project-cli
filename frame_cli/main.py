import typer

from frame_cli import listing, pull

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


@list_app.command("hybrid-models")
def list_hybrid_models(
    remote: bool = typer.Option(False, help="List remote hybrid models."),
) -> None:
    """List installed and remote hybrid models."""
    if remote:
        listing.list_remote_hybrid_models()
    else:
        listing.list_local_hybrid_models()


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
def pull_hybrid_model(
    name: str = typer.Argument(..., help="Hybrid model name."),
) -> None:
    """Download a hybrid model and seput environment."""
    pull.pull_hybrid_model(name)


@pull_app.command("component")
def pull_component(
    name: str = typer.Argument(..., help="Component name."),
    hybrid_model: str = typer.Argument(..., help="Associated local hybrid model name."),
) -> None:
    """Download a component."""
    pull.pull_component(name, hybrid_model)


if __name__ == "__main__":
    app()
