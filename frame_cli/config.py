"""Configuration variables."""

import os

from dotenv import load_dotenv

load_dotenv()

LOGGING_LEVEL = os.getenv("FRAME_CLI_LOGGING_LEVEL", "INFO")
API_URL = os.getenv("FRAME_CLI_API_URL", "https://frame-dev.epfl.ch/api/")
FRAME_DIR_NAME = ".frame-cli"
INFO_FILE_NAME = "info.yaml"
FRAME_METADATA_FILE_NAME = "frame_metadata.yaml"
FRAME_METADATA_TEMPLATE_URL = (
    "https://raw.githubusercontent.com/CHANGE-EPFL/frame-project/"
    "refs/heads/main/backend/api/metadata_files/template.yaml"
)
FRAME_REPO_OWNER = "CHANGE-EPFL"
FRAME_REPO_NAME = "frame-project"
FRAME_REPO = f"{FRAME_REPO_OWNER}/{FRAME_REPO_NAME}"
EXTERNAL_REFERENCES_PATH = os.path.join("backend", "api", "metadata_files", "external_references.yaml")
