"""Management of `.frame-cli` directories."""

import os

import yaml

from .config import FRAME_DIR_NAME, INFO_FILE_NAME
from .metadata import get_model_name, get_model_url, get_metadata_file_path


def get_home_info_path() -> str:
    """Return the path to the `.frame-cli` directory in the user's home directory."""

    return os.path.join(os.path.expanduser("~"), FRAME_DIR_NAME)


def get_closest_info_path() -> str | None:
    """Return the path to the `.frame-cli` directory at the root of the current repository, if it exists."""

    home_path = os.path.expanduser("~")
    current_dir = os.getcwd()

    while current_dir != os.path.dirname(current_dir):
        frame_path = os.path.join(current_dir, FRAME_DIR_NAME)

        if current_dir != home_path and os.path.exists(frame_path) and os.path.isdir(frame_path):
            return frame_path

        current_dir = os.path.dirname(current_dir)

    return None


def get_global_info() -> dict:
    """Return the global (home) info dictionary."""

    home_frame_path = get_home_info_path()
    global_info_path = os.path.join(home_frame_path, INFO_FILE_NAME)

    if not os.path.exists(home_frame_path):
        os.makedirs(home_frame_path)

    if not os.path.exists(global_info_path):
        with open(global_info_path, "w") as file:
            file.write("")

    with open(global_info_path, "r") as file:
        return yaml.safe_load(file) or {}


def set_global_info(info: dict) -> None:
    """Set the global (home) info dictionary."""

    home_frame_path = get_home_info_path()
    global_info_path = os.path.join(home_frame_path, INFO_FILE_NAME)

    if not os.path.exists(home_frame_path):
        os.makedirs(home_frame_path)

    with open(global_info_path, "w") as file:
        yaml.dump(info, file)


def get_local_models_info() -> dict:
    """Return the local hybrid models info dictionary."""

    global_info = get_global_info()

    if "local_models" not in global_info:
        global_info["local_models"] = {}

    for path in list(global_info["local_models"].keys()):
        if not os.path.exists(path):
            del global_info["local_models"][path]

    set_global_info(global_info)
    return global_info["local_models"]


def get_local_model_info() -> dict:
    """Return the local hybrid model info dictionary."""

    model_frame_path = get_closest_info_path()
    if model_frame_path is None:
        try:
            metadata_file_path = get_metadata_file_path()
        except Exception:
            return {}
        model_path = os.path.dirname(metadata_file_path)
        model_frame_path = os.path.join(model_path, FRAME_DIR_NAME)
        set_local_model_info({}, model_path)

    info_path = os.path.join(model_frame_path, INFO_FILE_NAME)

    with open(info_path, "r") as file:
        model_info = yaml.safe_load(file)

    updated_model_info = model_info.copy()

    try:
        model_name = get_model_name()
        updated_model_info["name"] = model_name
    except Exception:
        pass

    try:
        model_url = get_model_url()
        if model_url is not None:
            updated_model_info["url"] = model_url
    except Exception:
        pass

    if updated_model_info != model_info:
        set_local_model_info(updated_model_info)

    return updated_model_info


def set_local_model_info(info: dict, model_path: str | None = None) -> None:
    """Set the local hybrid model info dictionary."""

    if model_path is None:
        model_frame_path = get_closest_info_path()
        if model_frame_path is None:
            raise ValueError("Could not find local model.")
    else:
        model_frame_path = os.path.join(model_path, FRAME_DIR_NAME)

    info_path = os.path.join(model_frame_path, INFO_FILE_NAME)

    if not os.path.exists(model_frame_path):
        os.makedirs(model_frame_path)

    with open(info_path, "w") as file:
        yaml.dump(info, file)


def add_local_model_info(name: str, url: str, model_path: str | None = None) -> None:
    """Add a local hybrid model info to global dictionary and local model dictionary."""

    set_local_model_info(
        {
            "name": name,
            "url": url,
        },
        model_path,
    )

    global_info = get_global_info()
    if "local_models" not in global_info:
        global_info["local_models"] = {}

    global_info["local_models"][os.path.abspath(model_path)] = {"name": name}
    set_global_info(global_info)


def get_github_token(use_new_token: bool = False) -> str:
    """Return the GitHub token from the global info dictionary."""

    global_info = get_global_info()

    if "github_token" not in global_info or use_new_token:
        print("Create a GitHub token with `repo` scope: https://github.com/settings/tokens/new")
        github_token = input("GitHub token: ")
        global_info["github_token"] = github_token
        set_global_info(global_info)

    return global_info["github_token"]
