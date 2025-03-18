"""CLI entry point."""

import typer

from . import __version__, check as check_module, listing, pull, show, update as update_module

app = typer.Typer(
    help="Frame CLI tool to download hybrid models and setup environments.",
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

show_app = typer.Typer(
    help="Show information about a hybrid model or component.",
    no_args_is_help=True,
)
app.add_typer(show_app, name="show")

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


def version_callback(value: bool) -> None:
    if value:
        print(f"Frame CLI {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        help="Show the current version of Frame CLI.",
    ),
) -> None:
    pass


@app.command()
def check() -> None:
    """Check installation and API access."""
    check_module.check()


@app.command()
def version() -> None:
    """Show the current version of Frame CLI."""
    version_callback(True)


@app.command()
def update() -> None:
    """Update Frame CLI, assuming it has been installed with `uv tool install`."""
    update_module.update()


@show_app.command("hybrid-model")
def show_model(
    name: str = typer.Argument(..., help="Hybrid model name."),
    remote: bool = typer.Option(False, help="Show remote hybrid model info."),
) -> None:
    """Show information about a hybrid model."""
    if remote:
        show.show_remote_model(name)
    else:
        show.show_local_model(name)


@show_app.command("component")
def show_component(
    name: str = typer.Argument(..., help="Component name."),
    hybrid_model: str | None = typer.Argument(None, help="Associated local hybrid model name."),
    remote: bool = typer.Option(False, help="Show remote component info."),
) -> None:
    """Show information about a component."""
    if remote:
        if hybrid_model:  # show error
            print("Remote components are not associated with a local hybrid model. Remove the HYBRID_MODEL argument.")
            return
        show.show_remote_component(name)
    else:
        if not hybrid_model:
            print("Local components are associated with a local hybrid model. Add the HYBRID_MODEL argument.")
            return
        show.show_local_component(name, hybrid_model)


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
    destination: str | None = typer.Argument(None, help="Destination folder."),
) -> None:
    """Download a hybrid model and seput environment."""
    pull.pull_model(name, destination)


@pull_app.command("component")
def pull_component(
    name: str = typer.Argument(..., help="Component name."),
    hybrid_model: str = typer.Argument(..., help="Associated local hybrid model name."),
) -> None:
    """Download a component."""
    pull.pull_component(name, hybrid_model)


if __name__ == "__main__":
    app()
