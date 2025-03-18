"""Module for updating Frame CLI."""

import subprocess


def update() -> None:
    """Update Frame CLI, assuming it has been installed with `uv tool install`."""
    print("Updating Frame CLI.")
    subprocess.run(["uv", "tool", "update", "frame-cli"])
