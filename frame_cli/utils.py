"""Set of functions used in multiple other modules."""


def get_unit_id_and_version(name: str) -> tuple[str, str | None]:
    """Extract unit ID and version from a name."""

    if ":" in name:
        unit_id, version = name.split(":", 1)

    else:
        unit_id, version = name, None

    return unit_id, version
