"""Module for manipulating Frame metadata files."""

import os

from git import Repo, InvalidGitRepositoryError
import requests

from .config import FRAME_METADATA_FILE_NAME, FRAME_METADATA_TEMPLATE_URL


class NotInsideGitRepositoryError(Exception):
    """Not inside a Git repository."""


class MetadataFileAlreadyExistsError(Exception):
    """Frame metadata file already exists."""


class MetadataTemplateFetchError(Exception):
    """Error fetching the metadata template."""


def get_metadata_file_path() -> str:
    """Return the path to the Frame metadata file in the current project.

    Raises:
        NotInsideGitRepositoryError: If the current directory is not a Git repository.
    """
    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise NotInsideGitRepositoryError

    return os.path.join(repo.working_tree_dir, FRAME_METADATA_FILE_NAME)


def create_metadata_file() -> None:
    """Create a new Frame metadata file at the root of the current project.

    Raises:
        NotInsideGitRepositoryError: If the current directory is not a Git repository.
    """
    metadata_file_path = get_metadata_file_path()

    if os.path.exists(metadata_file_path):
        raise MetadataFileAlreadyExistsError

    try:
        response = requests.get(FRAME_METADATA_TEMPLATE_URL)
    except Exception:
        raise MetadataTemplateFetchError

    if response.status_code != 200:
        raise MetadataTemplateFetchError

    with open(metadata_file_path, "w") as f:
        f.write(response.text)
