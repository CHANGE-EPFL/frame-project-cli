from enum import Enum


class ComponentType(str, Enum):
    physics_based = "physics-based"
    machine_learning = "machine-learning"


def list_remote_hybrid_models() -> None:
    """List remote hybrid models."""
    raise NotImplementedError


def list_local_hybrid_models() -> None:
    """List installed hybrid models."""
    raise NotImplementedError


def list_remote_components(type: ComponentType | None) -> None:
    """List remote components."""
    raise NotImplementedError


def list_local_components(type: ComponentType | None) -> None:
    """List installed components."""
    raise NotImplementedError
