"""Set of functions used in multiple other modules."""

from json import JSONDecodeError
from typing import Any

import requests

from .config import API_URL, REQUESTS_TIMEOUT


def get_unit_id_and_version(name: str) -> tuple[str, str | None]:
    """Extract unit ID and version from a name."""

    if ":" in name:
        unit_id, version = name.split(":", 1)

    else:
        unit_id, version = name, None

    return unit_id, version


def retrieve_model_info(name: str) -> dict[str, Any] | None:
    """Retrieve online info of a hybrid model."""

    id, version = get_unit_id_and_version(name)
    url = f"{API_URL}/hybrid_models/{id}"
    if version is not None:
        url += f"?model_version={version}"
    response = requests.get(url, timeout=REQUESTS_TIMEOUT)

    if response.status_code == 404:
        print(f'Remote hybrid model "{name}" not found.')
        return None

    if response.status_code != 200:
        print(f"Error fetching remote hybrid model ({response.status_code}). Check the API URL.")
        return None

    try:
        info = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return None

    return info


def retrieve_component_info(name: str) -> tuple[dict[str, Any] | None, str | None]:
    """Retrieve online info of a component."""

    id, version = get_unit_id_and_version(name)
    url_physics_based = f"{API_URL}/components/physics_based/{id}"
    url_machine_learning = f"{API_URL}/components/machine_learning/{id}"
    if version is not None:
        url_physics_based += f"?component_version={version}"
        url_machine_learning += f"?component_version={version}"

    response = requests.get(url_physics_based, timeout=REQUESTS_TIMEOUT)
    component_type = "Physics-based"

    if response.status_code == 404:
        response = requests.get(url_machine_learning, timeout=REQUESTS_TIMEOUT)
        component_type = "Machine learning"

    if response.status_code == 404:
        print(f'Remote component "{name}" not found.')
        return None, None

    if response.status_code != 200:
        print(f"Error fetching remote component ({response.status_code}). Check the API URL.")
        return None, None

    try:
        info = response.json()
    except JSONDecodeError:
        print("Error decoding JSON. Check the API URL.")
        return None, None

    return info, component_type
