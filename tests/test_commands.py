import pytest
from typer.testing import CliRunner

from frame_cli.main import app

runner = CliRunner()


@pytest.mark.parametrize(
    "subcommand",
    [
        "",
        "check",
        "version",
        "update",
        "init",
        "validate",
        "push",
        "list",
        "show",
        "pull",
    ],
)
def test_help(subcommand: str):
    """Test help messages for CLI commands."""
    result = runner.invoke(app, [*subcommand.split(), "--help"])
    assert result.exit_code == 0
