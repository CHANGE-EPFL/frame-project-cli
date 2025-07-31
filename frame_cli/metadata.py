"""Module for manipulating FRAME metadata files."""

import os

from git import Repo, InvalidGitRepositoryError
import requests
from typing import TYPE_CHECKING
import yaml

from .config import FRAME_METADATA_FILE_NAME, FRAME_METADATA_TEMPLATE_URL
from .logging import logger
from .update import install_api_package, CannotInstallFRAMEAPIError


if TYPE_CHECKING:
    from api.models.metadata_file import MetadataFromFile


class NotInsideGitRepositoryError(Exception):
    """Not inside a Git repository."""


class MetadataFileAlreadyExistsError(Exception):
    """FRAME metadata file already exists."""


class MetadataTemplateFetchError(Exception):
    """Error fetching the metadata template."""


class MetadataFileNotFoundError(Exception):
    """FRAME metadata file not found."""


class InvalidMetadataFileError(yaml.YAMLError):
    """Invalid metadata file."""


def get_metadata_file_path() -> str:
    """Return the path to the FRAME metadata file in the current project.

    Raises:
        NotInsideGitRepositoryError: If the current directory is not a Git repository.
    """
    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise NotInsideGitRepositoryError

    return os.path.join(repo.working_tree_dir, FRAME_METADATA_FILE_NAME)


def create_metadata_file() -> None:
    """Create a new FRAME metadata file at the root of the current project.

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
    """Return the FRAME metadata dictionary from the metadata file.

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


def show_fair_level(metadata: "MetadataFromFile") -> None:
    from operator import attrgetter
    from api.models.hybrid_model import HybridModel
    from api.services.metadata import compute_fair_level, FAIR_LEVEL_PROPERTIES

    model = HybridModel(
        **metadata.hybrid_model.model_dump(),
        compatible_physics_based_component_ids=[],
        compatible_machine_learning_component_ids=[],
        data=metadata.data,
    )

    fair_level = compute_fair_level(model)
    max_fair_level = len(FAIR_LEVEL_PROPERTIES)
    logger.info(f"FAIR level of the hybrid model: {fair_level}/{max_fair_level}")

    if fair_level < max_fair_level:
        logger.info(
            f"To get to a FAIR level of {fair_level + 1}/{max_fair_level},"
            " make sure to fill in all the following properties: "
        )
        for prop in FAIR_LEVEL_PROPERTIES[fair_level]:
            filled = True
            try:
                value = attrgetter(prop)(model)
                if value is None:
                    filled = False
                if isinstance(value, list) and len(value) == 0:
                    filled = False
            except AttributeError:
                filled = False

            logger.info(f"- {prop} ({'OK' if filled else 'MISSING'})")

    else:
        logger.info("Well done!")


def validate() -> bool:
    from pydantic import ValidationError

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
        except CannotInstallFRAMEAPIError:
            logger.info("Error installing FRAME API package. Please check your internet connection.")
            return False
        from api.models.metadata_file import MetadataFromFile

    try:
        metadata = MetadataFromFile(**metadata)
    except ValidationError as e:
        logger.info("Validation error in metadata file:")
        for error in e.errors():
            logger.info(f"- {error['loc']}: {error['msg']}")
        return False
    except Exception as e:
        logger.info(f"Unexpected error during validation: {e}")
        return False

    try:
        show_fair_level(metadata)
    except ImportError:
        logger.info("Could not compute the FAIR level of the hybrid model. Please update FRAME CLI.")

    return True
