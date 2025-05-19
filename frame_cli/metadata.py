"""Module for manipulating Frame metadata files."""

import os

from git import Repo, InvalidGitRepositoryError
import requests
import yaml

from .config import FRAME_METADATA_FILE_NAME, FRAME_METADATA_TEMPLATE_URL
from .logging import logger
from .update import install_api_package, CannotInstallFrameAPIError


class NotInsideGitRepositoryError(Exception):
    """Not inside a Git repository."""


class MetadataFileAlreadyExistsError(Exception):
    """Frame metadata file already exists."""


class MetadataTemplateFetchError(Exception):
    """Error fetching the metadata template."""


class MetadataFileNotFoundError(Exception):
    """Frame metadata file not found."""


class InvalidMetadataFileError(yaml.YAMLError):
    """Invalid metadata file."""


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


def get_metadata() -> dict:
    """Return the Frame metadata dictionary from the metadata file.

    Raises:
        NotInsideGitRepositoryError: If the current directory is not a Git repository.
        YAMLError: If the metadata file is not a valid YAML file.
    """
    metadata_file_path = get_metadata_file_path()

    if not os.path.exists(metadata_file_path):
        raise MetadataFileNotFoundError

    with open(metadata_file_path, "r") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise InvalidMetadataFileError(f"Invalid metadata file: {e}")


def get_model_name() -> str:
    """Return the model name (unique id) from the metadata file.

    Raises:
        NotInsideGitRepositoryError: If the current directory is not a Git repository.
        YAMLError: If the metadata file is not a valid YAML file.
    """
    metadata = get_metadata()
    return metadata["hybrid_model"]["id"]


def get_model_url() -> str | None:
    """Return the model URL from the metadata file.

    Raises:
        NotInsideGitRepositoryError: If the current directory is not a Git repository.
        YAMLError: If the metadata file is not a valid YAML file.
    """
    metadata = get_metadata()
    return metadata["hybrid_model"].get("url", None)


def validate() -> bool:
    # TODO: use frame-project schemas to validate yaml
    try:
        metadata = get_metadata()

    except MetadataFileNotFoundError:
        logger.info("Metadata file not found. Please run `frame init` to create one.")
        return False

    except InvalidMetadataFileError:
        logger.info("Invalid yaml file.")
        return False

    try:
        from api.models.metadata_file import MetadataFromFile
    except ImportError:
        try:
            install_api_package()
        except CannotInstallFrameAPIError:
            logger.info("Error installing Frame API package. Please check your internet connection.")
            return False
        from api.models.metadata_file import MetadataFromFile

    try:
        MetadataFromFile(**metadata)
    except Exception as e:
        logger.info(f"Invalid metadata file: {e}")
        return False

    return True
