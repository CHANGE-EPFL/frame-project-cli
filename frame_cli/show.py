"""Module for `frame show` commands."""

from rich.console import Console
from rich.panel import Panel

from .utils import retrieve_component_info, retrieve_model_info


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
    info = retrieve_model_info(name)
    if info is None:
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


def show_remote_component(name: str) -> None:
    """Show information about a remote component."""
    info, component_type = retrieve_component_info(name)
    if info is None:
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
