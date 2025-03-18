"""Management of `.frame-cli` directories."""

import os

import yaml

from .config import FRAME_DIR_NAME, INFO_FILE_NAME


def get_home_info_path() -> str:
    """Return the path to the `.frame-cli` directory in the user's home directory."""

    return os.path.join(os.path.expanduser("~"), FRAME_DIR_NAME)


def get_closest_info_path() -> str | None:
    """Return the path to the `.frame-cli` directory at the root of the current repository, if it exists."""

    home_path = os.path.expanduser("~")
    current_dir = os.getcwd()

    while current_dir != "/":
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

    for path in list(global_info["local_models"].keys()):
        if not os.path.exists(path):
            del global_info["local_models"][path]

    set_global_info(global_info)
    return global_info["local_models"]


def set_local_model_info(model_path: str, info: dict) -> None:
    """Set the local hybrid model info dictionary."""

    model_frame_path = os.path.join(model_path, FRAME_DIR_NAME)
    info_path = os.path.join(model_frame_path, INFO_FILE_NAME)

    if not os.path.exists(model_frame_path):
        os.makedirs(model_frame_path)

    with open(info_path, "w") as file:
        yaml.dump(info, file)


def add_local_model_info(name: str, path: str) -> None:
    """Add a local hybrid model info to global dictionary and local model dictionary."""

    set_local_model_info(path, {"name": name})

    global_info = get_global_info()
    if "local_models" not in global_info:
        global_info["local_models"] = {}

    global_info["local_models"][os.path.abspath(path)] = {"name": name}
    set_global_info(global_info)
