"""Logging configuration."""

import logging

from rich.logging import RichHandler

from .config import LOGGING_LEVEL

FORMAT = "%(message)s"
logging.basicConfig(level=LOGGING_LEVEL, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger(__name__)
