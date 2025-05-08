"""Module for `frame init` command."""

import os

from git import Repo, InvalidGitRepositoryError
import requests

from .config import FRAME_METADATA_FILE_NAME, FRAME_METADATA_TEMPLATE_URL


def init() -> None:
    """Create a new Frame metadata file at the root of the current project."""

    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        print("Not inside a git repository. Please run this command inside a git repository.")
        return

    metadata_file_path = os.path.join(repo.working_tree_dir, FRAME_METADATA_FILE_NAME)

    if os.path.exists(metadata_file_path):
        print(f"{FRAME_METADATA_FILE_NAME} already exists in the project's root directory.")
        return

    try:
        response = requests.get(FRAME_METADATA_TEMPLATE_URL)
    except Exception:
        print("Error fetching the template metadata file. Check the URL.")
        return

    if response.status_code != 200:
        print("Error fetching the template metadata file. Check the URL.")
        return

    with open(metadata_file_path, "w") as f:
        f.write(response.text)

    print(f"Created {FRAME_METADATA_FILE_NAME} in the project's root directory.")
