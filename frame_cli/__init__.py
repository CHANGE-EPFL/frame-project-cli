"""Command line interface for managing FRAME hybrid models"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("frame-cli")
except PackageNotFoundError:
    pass
