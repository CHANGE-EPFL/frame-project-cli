"""Module for `frame init` command."""

from .config import FRAME_METADATA_FILE_NAME
from .metadata import (
    create_metadata_file,
    NotInsideGitRepositoryError,
    MetadataFileAlreadyExistsError,
    MetadataTemplateFetchError,
)


def init() -> None:
    """Create a new Frame metadata file at the root of the current project."""

    try:
        create_metadata_file()
        print(f"Created {FRAME_METADATA_FILE_NAME} in the project's root directory.")
    except NotInsideGitRepositoryError:
        print("Not inside a git repository. Please run this command inside a git repository.")
    except MetadataFileAlreadyExistsError:
        print(f"{FRAME_METADATA_FILE_NAME} already exists in the project's root directory.")
    except MetadataTemplateFetchError:
        print("Error fetching the template metadata file. Check the URL.")
