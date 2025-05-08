"""Module containing the HydroshareDownloader class."""

import os
import tempfile
import zipfile

import requests
from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn, TimeRemainingColumn, TransferSpeedColumn
from rich.status import Status

from ..logging import logger
from .downloader import Downloader


class HydroshareDownloader(Downloader):
    """Downloader for Hydroshare datasets."""

    def download(
        self,
        url: str,
        destination: str | None = None,
    ) -> str:
        """Download the content at the given URL.

        Returns:
            str: The destination directory.

        Args:
            url (str): URL of the content to download.
            destination (str): Destination directory to save the content to. Defaults to None, which saves to the
                current working directory.

        Raises:
        """
        _check_url(url)
        resource_id = url.split("/")[-1]
        archive_url = f"https://www.hydroshare.org/hsapi/resource/{resource_id}/"

        if destination is None:
            destination = "."

        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = _download_archive(archive_url, temp_dir)

            # Extract archive
            logger.debug(f'Extracting "{archive_path}" to "{destination}"...')
            with Status(f"Extracting to {destination}..."), zipfile.ZipFile(archive_path, "r") as archive:
                archive.extractall(destination)

        logger.info("Done!")

        return destination


def _check_url(url: str) -> None:
    """Check that the url has the format "http://www.hydroshare.org/resource/XXXX".

    Args:
        url (str): URL to check.

    Raises:
        ValueError: The URL does not have the correct format.
    """

    if "://www.hydroshare.org/resource/" not in url:
        raise ValueError(f'Invalid Hydroshare URL: "{url}"')


def _download_archive(url: str, dir_path: str) -> str:
    """Download the archive from the given URL to the given directory.

    Args:
        url (str): URL of the archive to download.
        dir_path (str): Directory to save the archive to.

    Returns:
        archive_path (str): Path to the downloaded archive.
    """

    archive_path = os.path.join(dir_path, "archive.zip")

    logger.debug(f'Requesting archive creation at "{url}"...')
    with Status("Requesting archive creation..."):
        response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise ValueError(f"Error downloading {url}: {response.status_code}, {response.text}")

    size = int(response.headers.get("content-length", 0))

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
        logger.debug(f'Downloading "{url}"...')
        task_id = progress.add_task("downloading", filename=url.split("/")[-1], total=size)

        with open(archive_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                progress.update(task_id, advance=len(chunk))

    return archive_path
