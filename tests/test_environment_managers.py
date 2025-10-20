import os
from pathlib import Path

import pytest

from frame_cli.environment_managers.environment_manager import get_environment_manager


@pytest.fixture
def temp_dir_without_python_env(tmp_path: Path) -> Path:
    """Get a temporary directory without any active Python environment."""

    os.environ.pop("VIRTUAL_ENV", None)
    os.environ.pop("CONDA_PREFIX", None)
    os.environ.pop("CONDA_DEFAULT_ENV", None)
    return tmp_path


class TestPython:
    def check_setup(self, dir: Path) -> None:
        """Check if the Python environment was set up correctly."""

        try:
            python_lib_path = os.listdir(dir / ".venv" / "lib")[0]
        except FileNotFoundError:
            pytest.fail("Python environment was not set up correctly: .venv/lib directory not found.")

        try:
            libs = os.listdir(dir / ".venv" / "lib" / python_lib_path / "site-packages")
        except FileNotFoundError:
            pytest.fail("Python environment was not set up correctly: site-packages directory not found.")

        assert any(lib.startswith("numpy") for lib in libs)

    def test_requirements(self, temp_dir_without_python_env: Path) -> None:
        """Test Python environment setup with requirements.txt file."""

        os.chdir(temp_dir_without_python_env)
        requirements_file_path = temp_dir_without_python_env / "requirements.txt"
        with open(requirements_file_path, "w") as f:
            f.write("numpy")

        environment_manager = get_environment_manager("python")
        assert environment_manager is not None

        file_paths = ["requirements.txt"]
        environment_manager.setup(str(temp_dir_without_python_env), file_paths)

        self.check_setup(temp_dir_without_python_env)

    def test_pyproject(self, temp_dir_without_python_env: Path) -> None:
        """Test Python environment setup with pyproject.toml file."""

        os.chdir(temp_dir_without_python_env)
        pyproject_file_path = temp_dir_without_python_env / "pyproject.toml"
        with open(pyproject_file_path, "w") as f:
            f.write("""[project]
                name = "test_project"
                version = "0.1.0"
                dependencies = ["numpy"]
            """)

        environment_manager = get_environment_manager("python")
        assert environment_manager is not None

        file_paths = ["pyproject.toml"]
        environment_manager.setup(str(temp_dir_without_python_env), file_paths)

        self.check_setup(temp_dir_without_python_env)
