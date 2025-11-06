"""Module for `frame push` command."""

import os
import shutil
import subprocess

import git
import github
import yaml
from github.AuthenticatedUser import AuthenticatedUser
from github.Repository import Repository as GithubRepository
from rich.prompt import Prompt

from .config import EXTERNAL_REFERENCES_PATH, FRAME_PYTHON_VERSION, FRAME_REPO, FRAME_REPO_NAME, METADATA_DIR_PATH
from .info import get_github_token, get_home_info_path, get_local_model_info
from .logging import logger
from .metadata import get_metadata_file_path
from .metadata import validate as validate_metadata_file


class MissingModelURLError(Exception):
    """Exception raised when the model URL is missing in the metadata file."""


class ModelAlreadyTrackedError(Exception):
    """Exception raised when the model is already tracked by the FRAME repository."""


class ModelAlreadyIntegratedError(Exception):
    """Exception raised when the model is already integrated in the FRAME repository."""


def create_frame_fork(upstream_repo: GithubRepository, github_user: AuthenticatedUser) -> GithubRepository:
    return github_user.create_fork(upstream_repo)


def get_local_frame_repo(github_client: github.Github, github_user: AuthenticatedUser):
    local_repo_path = os.path.join(get_home_info_path(), FRAME_REPO_NAME)
    logger.debug("Getting local FRAME repository")

    try:
        local_repo = git.Repo(local_repo_path)
        logger.debug(f"Found cloned FRAME repository at {local_repo_path}")
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


def add_model_to_local_frame_repo(local_repo: git.Repo, as_reference: bool) -> str:
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

    if as_reference:
        return add_model_to_local_frame_repo_as_reference(local_repo)
    else:
        return add_model_to_local_frame_repo_as_integrated(local_repo)


def add_model_to_local_frame_repo_as_reference(local_repo: git.Repo) -> str:
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
    commit_message = f'feat(metadata): add "{model_name}" to external references'
    local_repo.git.commit(m=commit_message)
    return commit_message


def add_model_to_local_frame_repo_as_integrated(local_repo: git.Repo) -> str:
    model_name = get_model_name()
    new_metadata_path = os.path.join(str(local_repo.working_tree_dir), METADATA_DIR_PATH, f"{model_name}.yaml")
    replace = False

    if os.path.exists(new_metadata_path):
        with open(new_metadata_path, "r") as file:
            existing_metadata = yaml.safe_load(file)

        print(f"A metadata file for a model with id '{model_name}' already exists in the FRAME repository.\n")
        print("Model full name:", existing_metadata.get("hybrid_model", {}).get("name", "N/A"))
        print(f"Contributors: {', '.join(existing_metadata.get('hybrid_model', {}).get('contributors', []))}")
        replace = Prompt.ask("\nDo you want to replace it?", choices=["yes", "no"], default="no") == "yes"
        if not replace:
            raise ModelAlreadyIntegratedError("Model metadata file already exists in FRAME repository.")

    local_metadata_path = get_metadata_file_path()
    shutil.copyfile(local_metadata_path, new_metadata_path)
    local_repo.git.add(os.path.join(METADATA_DIR_PATH, f"{model_name}.yaml"))
    commit_message = f"feat(metadata): {'update' if replace else 'add'} {model_name} metadata file"
    local_repo.git.commit(m=commit_message)
    return commit_message


def push_to_frame_fork(local_repo: git.Repo):
    logger.info("Pushing changes to FRAME fork")
    local_repo.git.push("origin", generate_branch_name(), force_with_lease=True)


def create_pull_request(github_client: github.Github, github_user: AuthenticatedUser, message: str):
    branch_name = generate_branch_name()
    upstream_repo = github_client.get_repo(FRAME_REPO)

    logger.info(f"Creating pull request from {github_user.login}:{branch_name} to {upstream_repo.full_name}:main")
    try:
        pull_request = upstream_repo.create_pull(
            title=message,
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
    """Validate metadata file and absence of conflicts with other FRAME models."""
    logger.info("Validating integration with FRAME repository")

    frame_api_path = os.path.join(get_home_info_path(), FRAME_REPO_NAME, "backend")

    logger.info("Creating virtual environment using uv")
    ret = subprocess.run(f"uv venv --python {FRAME_PYTHON_VERSION}".split(), cwd=frame_api_path, capture_output=True)
    if ret.returncode != 0:
        print(
            "Error creating virtual environment using uv. Please check that uv and a recent version of Python are installed."
        )
        return False

    logger.info("Installing dependencies")
    env_virtual_env = os.environ.pop("VIRTUAL_ENV", "")  # Ensure we use correct uv's virtual environment
    ret = subprocess.run("uv pip install -e .[test]".split(), cwd=frame_api_path, capture_output=True)
    if ret.returncode != 0:
        print("Error installing dependencies.")
        os.environ["VIRTUAL_ENV"] = env_virtual_env
        return False

    logger.info("Running integration tests")
    ret = subprocess.run("uv run pytest --disable-warnings".split(), cwd=frame_api_path)
    os.environ["VIRTUAL_ENV"] = env_virtual_env
    if ret.returncode != 0:
        print("Integration tests failed.")
        return False

    logger.info("Integration tests passed")
    return True


def push(use_new_token: bool = False):
    """Submit a pull request to the FRAME project with new/updated metadata."""

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

    add_as_reference = (
        Prompt.ask(
            "Where do you want the FRAME metadata file to be pushed?\n"
            "1: Add to FRAME repository (recommended, default).\n"
            "2: Keep in your model's repository and only link it in FRAME. You need push access to the model's repository.",
            choices=["1", "2"],
            default="1",
        )
        == "2"
    )

    if add_as_reference:
        if (
            Prompt.ask(
                "Have you already pushed the FRAME metadata file to your model's repository?",
                choices=["yes", "no"],
            )
            == "no"
        ):
            print("Please push the FRAME metadata file to your model's repository and try again.")
            return

    local_repo = get_local_frame_repo(github_client, github_user)
    try:
        commit_message = add_model_to_local_frame_repo(local_repo, add_as_reference)
    except MissingModelURLError:
        print("Model URL is empty. Please set the model URL to the remote repository URL in the metadata file.")
        return
    except ModelAlreadyTrackedError:
        print("Model URL already tracked in FRAME's external references. No changes made.")
        return
    except ModelAlreadyIntegratedError:
        print("Model already integrated in FRAME repository. No changes made.")
        return

    if not validate_integration():
        print("Validation failed. Please check the metadata file and resolve any conflicts.")
        return

    push_to_frame_fork(local_repo)
    create_pull_request(github_client, github_user, commit_message)
