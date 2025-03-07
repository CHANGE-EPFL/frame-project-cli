"""Configuration variables."""

import os

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = os.getenv("FRAME_CLI_LOGGING_LEVEL", "INFO")
API_URL = os.getenv("FRAME_CLI_API_URL", "https://frame-dev.epfl.ch/api/")
FRAME_DIR_NAME = ".frame-cli"
INFO_FILE_NAME = "info.yaml"
