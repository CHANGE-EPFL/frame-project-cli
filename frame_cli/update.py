"""Module for updating Frame CLI."""

import subprocess
import sys

from .logging import logger


class CannotInstallFrameAPIError(Exception):
    """Error installing the Frame API package."""


def install_api_package():
    """Install the Frame API package.

    The API package cannot be put in the pyproject.toml because it prevents publishing in PyPI.
    """

    logger.info("Installing Frame API package.")
    ret = subprocess.run(
        f"uv pip install --python {sys.executable} -U git+https://github.com/CHANGE-EPFL/frame-project#subdirectory=backend".split(),
        capture_output=True,
    )

    if ret.returncode != 0:
        raise CannotInstallFrameAPIError


def update() -> None:
    """Update Frame CLI, assuming it has been installed with `uv tool install`."""

    logger.info("Updating Frame CLI.")

    ret = subprocess.run(["uv", "tool", "update", "frame-cli"])
    if ret.returncode != 0:
        return

    install_api_package()
