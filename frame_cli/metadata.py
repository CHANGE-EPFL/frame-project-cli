"""Module for manipulating FRAME metadata files."""

import os
from typing import TYPE_CHECKING

import requests
import yaml
from git import InvalidGitRepositoryError, Repo

from .config import FRAME_METADATA_FILE_NAME, FRAME_METADATA_TEMPLATE_URL
from .logging import logger
from .update import CannotInstallFRAMEAPIError, install_api_package

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


def get_metadata_file_path(base_dir: str | None = None) -> str:
    """Return the path to the FRAME metadata file in the current project."""
    try:
        repo = Repo(search_parent_directories=True)
        metadata_file_path = os.path.join(repo.working_tree_dir, FRAME_METADATA_FILE_NAME)

    except InvalidGitRepositoryError:
        if base_dir is None:
            base_dir = os.getcwd()
        metadata_file_path = os.path.join(base_dir, FRAME_METADATA_FILE_NAME)

    return metadata_file_path


def create_metadata_file() -> None:
    """Create a new FRAME metadata file at the root of the current project."""
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


def metadata_file_exists(base_dir: str | None = None) -> bool:
    """Check if the FRAME metadata file exists in the current project."""
    metadata_file_path = get_metadata_file_path(base_dir)
    return os.path.exists(metadata_file_path)


def get_metadata() -> dict:
    """Return the FRAME metadata dictionary from the metadata file.

    Raises:
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
    from api.services.metadata import FAIR_LEVEL_PROPERTIES, compute_fair_level

    model = HybridModel(
        **metadata.hybrid_model.model_dump(),
        compatible_physics_based_component_ids=[],
        compatible_machine_learning_component_ids=[],
        data=metadata.data,
    )

    fair_level = compute_fair_level(model)
    max_fair_level = len(FAIR_LEVEL_PROPERTIES)
    print(f"FAIR level of the hybrid model: {fair_level}/{max_fair_level}")

    if fair_level < max_fair_level:
        print(
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
                if isinstance(value, str) and value.strip() == "":
                    filled = False
            except AttributeError:
                filled = False

            print(f"- {prop} ({'OK' if filled else 'MISSING'})")

        print("More details about FAIR levels on https://frame.epfl.ch/#/about\n")

    else:
        print("Well done!")


def validate() -> bool:
    from pydantic import ValidationError

    try:
        metadata = get_metadata()

    except MetadataFileNotFoundError:
        print("Metadata file not found. Please run `frame init` to create one.")
        return False

    except InvalidMetadataFileError:
        print("Invalid yaml file.")
        return False

    try:
        from api.models.metadata_file import MetadataFromFile
    except ImportError:
        try:
            install_api_package()
        except CannotInstallFRAMEAPIError:
            print("Error installing FRAME API package. Please check your internet connection.")
            return False
        from api.models.metadata_file import MetadataFromFile

    try:
        metadata = MetadataFromFile(**metadata)
    except ValidationError as e:
        print("Validation error in metadata file:")
        for error in e.errors():
            print(f"- {error['loc']}: {error['msg']}")
        return False
    except Exception as e:
        print(f"Unexpected error during validation: {e}")
        return False

    try:
        show_fair_level(metadata)
    except ImportError:
        print("Could not compute the FAIR level of the hybrid model. Please update FRAME CLI.")

    return True
