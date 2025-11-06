"""Module containing the EnvironmentManager abstract base class."""

import importlib
import inspect
import os
import pkgutil
from abc import ABC, abstractmethod


class EnvironmentManager(ABC):
    """Abstract base class for environment managers."""

    type: str

    @abstractmethod
    def setup(self, destination: str, file_paths: list[str], *args, **kwargs) -> None:
        """Set up the environment for the hybrid model.

        Args:
            destination (str): Hybrid model destination directory where the environment is set up.
            file_paths (list[str]): List of paths to files that describe the environment.
        """


def _get_environment_manager_subclasses() -> dict[str, type[EnvironmentManager]]:
    package_path = os.path.dirname(__file__)
    subclasses = {}

    for module_info in pkgutil.iter_modules([package_path]):
        if module_info.ispkg:
            continue

        module = importlib.import_module(f"{__package__}.{module_info.name}")

        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, EnvironmentManager) and obj is not EnvironmentManager:
                subclasses[obj.type] = obj

    return subclasses


_environment_manager_subclasses: dict | None = None


def get_environment_manager(environment_type: str) -> EnvironmentManager | None:
    """Get an instance of environment manager for the given type."""
    global _environment_manager_subclasses

    if _environment_manager_subclasses is None:
        _environment_manager_subclasses = _get_environment_manager_subclasses()

    manager_class = _environment_manager_subclasses.get(environment_type)

    if manager_class is not None:
        return manager_class()

    return None
