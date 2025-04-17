"""Module containing the ZenodoDownloader class."""

import os
import signal
import zipfile
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import requests
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.status import Status

from ..logging import logger
from .downloader import Downloader

ZENODO_DOI_PREFIX = "10.5281"
ZENODO_SANDBOX_PREFIX = "10.5072"
THREADS = 4


class ZenodoDownloader(Downloader):
    """Downloader for Zenodo repositories."""

    def download(
        self,
        url: str,
        destination: str | None = None,
    ) -> str:
        f"""Download the Zenodo dataset with the given DOI.

        Args:
            url (str): URL or DOI of the content to download, ending in "{ZENODO_DOI_PREFIX}/zenodo.XXXX" for
                Zenodo datasets or "{ZENODO_SANDBOX_PREFIX}/zenodo.XXXX" for Zenodo sandbox datasets.
            destination (str): Destination directory to save the content to. Defaults to None, which infers the
                destination from the URL (dataset ID).

        Returns:
            str: The destination directory.

        Raises:
            FileExistsError: The destination directory already exists.
            NotADirectoryError: The destination is not a directory.
            ZenodoError: Zenodo download fails.
        """
        host, dataset_id = _get_host_and_id_from_url(url)
        url = f"https://{host}/api/records/{dataset_id}"

        # Scan record
        response = requests.get(url)
        _check_request_response(response, f'getting Zenodo record "{dataset_id}"')
        record = response.json()

        # Create destination folder if it does not exist
        if destination is None:
            destination = dataset_id
        if not os.path.exists(destination):
            os.makedirs(destination)
        if os.listdir(destination):
            raise FileExistsError(f'Destination directory "{destination}" is not empty.')

        # Download files
        _download_files(record, destination)

        return destination


class ZenodoError(Exception):
    """Custom exception for Zenodo errors."""


def _check_request_response(
    response: requests.Response,
    task_description: str,
    expected_status: int = 200,
) -> None:
    """Check the status of the given request.

    Args:
        response (requests.Response): Response object from the request.
        task_description (str): Description of the task being performed.
        expected_status (int): Expected status code. Defaults to 200.

    Raises:
        ZenodoError: The request failed.
    """
    if response.status_code != expected_status:
        raise ZenodoError(f"Error {task_description}: {response.status_code}, {response.text}")


def _get_host_and_id_from_url(url: str) -> tuple[str, str]:
    """Get the host and study ID from the given URL.

    Args:
        url (str): URL to parse, ending in "10.XXXX/zenodo.[ID]".

    Returns:
        host (str): Either "zenodo.org" or "sandbox.zenodo.org".
        id (str): Dataset ID extracted from the DOI.

    Raises:
        ValueError: The URL is not a valid Zenodo DOI or URL.
    """
    ids = url.split("/")[-2:]

    if ids[0] == ZENODO_DOI_PREFIX:
        host = "zenodo.org"

    elif ids[0] == ZENODO_SANDBOX_PREFIX:
        host = "sandbox.zenodo.org"

    else:
        raise ValueError(
            (
                f'Invalid Zenodo URL or DOI: "{url}". Must end in "{ZENODO_DOI_PREFIX}/zenodo.XXXX" or '
                f'"{ZENODO_SANDBOX_PREFIX}/zenodo.XXXX".'
            )
        )

    dataset_id = ids[1].split(".")[1]

    return host, dataset_id


def _download_files(record: dict, destination: str) -> None:
    """Download all files from the given Zenodo record.

    Args:
        record (dict): Zenodo record information.
        destination (str): Destination directory to save the files to.
    """
    # Download files
    n_files = len(record["files"])
    key = ""
    path = ""

    stop_event.clear()
    logger.info(f'Downloading {n_files} file{"s" if n_files > 1 else ""} into "{destination}"...')
    with Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        DownloadColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
    ) as progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for i in range(n_files):
                file = record["files"][i]
                url = file["links"]["self"]
                key = file["key"]
                path = os.path.join(destination, key)

                # Download file
                logger.debug(f"({i + 1}/{n_files}) Downloading {key}...")
                task_id = progress.add_task("({i+1}/{n_files}) {key}", filename=key, start=False)
                pool.submit(_download_file, url, key, path, progress, task_id)

    # If only one file which is a zip, unzip it and remove the zip
    if n_files == 1 and key.endswith(".zip") and not stop_event.is_set():
        message = f'Unzipping "{key}"...'
        logger.debug(message)
        with zipfile.ZipFile(path, "r") as zip_ref, Status(message):
            zip_ref.extractall(destination)
        os.remove(path)
        logger.info(f'Unzipped "{key}".')


def _download_file(url: str, key: str, path: str, progress: Progress, task_id: TaskID) -> None:
    """Download the file from the given URL.

    Args:
        url (str): URL of the file to download.
        key (str): Name of the file.
        path (str): Path to save the file to.
        progress (Progress): Rich progress tracker.
        task_id (TaskID): Rich task ID.
    """
    # Create directory if necessary
    os.makedirs(os.path.dirname(path), exist_ok=True)

    response = requests.get(url, stream=True)
    _check_request_response(response, f"downloading {key}")
    size = int(response.headers.get("content-length", 0))
    progress.update(task_id, total=size)

    with open(path, "wb") as file:
        progress.start_task(task_id)

        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
            progress.update(task_id, advance=len(chunk))

            if stop_event.is_set():
                return


# Handle termination


def handle_sigint(sig, frame):
    stop_event.set()
    logger.warning("Download interrupted.")


stop_event = Event()
signal.signal(signal.SIGINT, handle_sigint)
