"""Module for `frame push` command."""

import os
import subprocess
import yaml

import git
import github
from github.AuthenticatedUser import AuthenticatedUser
from github.Repository import Repository as GithubRepository

from .config import FRAME_REPO, FRAME_REPO_NAME, EXTERNAL_REFERENCES_PATH
from .info import get_github_token, get_home_info_path, get_local_model_info
from .logging import logger
from .metadata import validate as validate_metadata_file


class MissingModelURLError(Exception):
    """Exception raised when the model URL is missing in the metadata file."""


class ModelAlreadyTrackedError(Exception):
    """Exception raised when the model is already tracked by the Frame repository."""


def create_frame_fork(upstream_repo: GithubRepository, github_user: AuthenticatedUser) -> GithubRepository:
    return github_user.create_fork(upstream_repo)


def get_local_frame_repo(github_client: github.Github, github_user: AuthenticatedUser):
    local_repo_path = os.path.join(get_home_info_path(), FRAME_REPO_NAME)
    logger.debug("Getting local Frame repository")

    try:
        local_repo = git.Repo(local_repo_path)
        logger.debug(f"Found cloned Frame repository at {local_repo_path}")
    except git.NoSuchPathError:
        upstream_repo = github_client.get_repo(FRAME_REPO)
        try:
            fork = github_user.get_repo(FRAME_REPO_NAME)
            logger.debug(f"Found fork of {upstream_repo.clone_url} for user {github_user.login}")
        except github.UnknownObjectException:
            logger.info(f"Creating fork of {upstream_repo.clone_url} for user {github_user.login}")
            fork = create_frame_fork(upstream_repo, github_user)

        logger.info(f"Cloning {fork.clone_url} into {local_repo_path}")
        local_repo = git.Repo.clone_from(fork.clone_url, local_repo_path)
        local_repo.remotes.origin.set_url(
            fork.clone_url.replace("://", f"://{github_user.login}:{get_github_token()}@")
        )
        local_repo.create_remote("upstream", url=upstream_repo.clone_url)

    logger.debug("Fetching upstream repository")
    local_repo.remotes.upstream.fetch()
    return local_repo


def get_model_name() -> str:
    model_info = get_local_model_info()
    if "name" not in model_info:
        raise ValueError("Model name not found in local model info.")

    return model_info["name"]


def get_model_url() -> str:
    model_info = get_local_model_info()
    if "url" not in model_info:
        raise ValueError("Model URL not found in local model info.")
    if not model_info["url"]:
        raise MissingModelURLError

    return model_info["url"]


def generate_branch_name() -> str:
    model_name = get_model_name()
    return f"feat-{model_name}"


def add_model_to_local_frame_repo(local_repo: git.Repo):
    branch_name = generate_branch_name()

    logger.debug("Checking out main branch")
    local_repo.git.checkout("main")

    try:
        logger.debug(f"Creating branch {branch_name} from upstream/main")
        local_repo.git.branch("-f", branch_name, "upstream/main")
    except git.GitCommandError:
        pass

    logger.debug(f"Checking out branch {branch_name}")
    local_repo.git.checkout(branch_name)

    external_references_path = os.path.join(str(local_repo.working_tree_dir), EXTERNAL_REFERENCES_PATH)
    with open(external_references_path, "r") as file:
        external_references = yaml.safe_load(file) or []

    model_url = get_model_url()
    if model_url in external_references:
        raise ModelAlreadyTrackedError("Model URL already in external references.")

    external_references.append(model_url)
    with open(external_references_path, "w") as file:
        yaml.dump(external_references, file)

    local_repo.git.add(EXTERNAL_REFERENCES_PATH)
    model_name = get_model_name()
    local_repo.git.commit(m=f"feat(metadata): add {model_name} to external references")


def push_to_frame_fork(local_repo: git.Repo):
    logger.info("Pushing changes to Frame fork")
    local_repo.git.push("origin", generate_branch_name(), force_with_lease=True)


def create_pull_request(github_client: github.Github, github_user: AuthenticatedUser):
    branch_name = generate_branch_name()
    upstream_repo = github_client.get_repo(FRAME_REPO)

    logger.info(f"Creating pull request from {github_user.login}:{branch_name} to {upstream_repo.full_name}:main")
    try:
        pull_request = upstream_repo.create_pull(
            title=f'feat(metadata): Add "{get_model_name()}" to external references',
            body="",
            head=f"{github_user.login}:{branch_name}",
            base="main",
        )
    except github.GithubException as e:
        for error in e.data["errors"]:
            logger.error(error["message"])
        print("Error creating pull request.")
        return

    print(f"Pull request created: {pull_request.html_url}")


def validate_integration() -> bool:
    """Validate metadata file and absence of conflicts with other Frame models."""
    logger.info("Validating integration with Frame repository")

    frame_api_path = os.path.join(get_home_info_path(), FRAME_REPO_NAME, "backend")

    logger.info("Creating virtual environment using uv")
    ret = subprocess.run("uv venv".split(), cwd=frame_api_path, capture_output=True)
    if ret.returncode != 0:
        print(
            "Error creating virtual environment using uv. Please check that uv and a recent version of Python are installed."
        )
        return False

    logger.info("Installing dependencies")
    ret = subprocess.run("uv pip install -e .[test]".split(), cwd=frame_api_path, capture_output=True)
    if ret.returncode != 0:
        print("Error installing dependencies.")
        return False

    logger.info("Running integration tests")
    ret = subprocess.run("uv run pytest --disable-warnings".split(), cwd=frame_api_path)
    if ret.returncode != 0:
        print("Integration tests failed.")
        return False

    logger.info("Integration tests passed")
    return True


def push(use_new_token: bool = False):
    """Submit a pull request to the Frame project with new/updated metadata."""

    if not validate_metadata_file():
        print("Metadata file does not follow schema.")
        return

    github_client = github.Github(get_github_token(use_new_token))
    github_user = github_client.get_user()
    try:
        logger.info(f'Accessing GitHub API as "{github_user.login}"')
    except github.BadCredentialsException:
        print(
            "Invalid GitHub token. Please check whether your token is still valid, or run the command with the --use-new-token option."
        )
        return

    local_repo = get_local_frame_repo(github_client, github_user)
    try:
        add_model_to_local_frame_repo(local_repo)
    except MissingModelURLError:
        print("Model URL is empty. Please set the model URL to the remote repository URL in the metadata file.")
        return
    except ModelAlreadyTrackedError:
        print("Model URL already tracked in external references.")
        return

    if not validate_integration():
        print("Validation failed. Please check the metadata file and resolve any conflicts.")
        return

    push_to_frame_fork(local_repo)
    create_pull_request(github_client, github_user)
