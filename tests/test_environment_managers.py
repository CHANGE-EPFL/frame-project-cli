import os
from pathlib import Path

import pytest

from frame_cli.environment_managers.environment_manager import get_environment_manager


@pytest.fixture
def model_dir_path(tmp_path: Path) -> Path:
    """Get a temporary directory without any active Python environment."""

    os.chdir(tmp_path)
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

    def test_requirements_txt(self, model_dir_path: Path) -> None:
        """Test Python environment setup with requirements.txt file."""

        requirements_file_path = model_dir_path / "requirements.txt"
        with open(requirements_file_path, "w") as f:
            f.write("numpy")

        environment_manager = get_environment_manager("python")
        assert environment_manager is not None

        file_paths = ["requirements.txt"]
        environment_manager.setup(str(model_dir_path), file_paths)

        self.check_setup(model_dir_path)

    def test_pyproject_toml(self, model_dir_path: Path) -> None:
        """Test Python environment setup with pyproject.toml file."""

        pyproject_file_path = model_dir_path / "pyproject.toml"
        with open(pyproject_file_path, "w") as f:
            f.write("""[project]
name = "test_model"
version = "0.1.0"
dependencies = ["numpy"]""")

        environment_manager = get_environment_manager("python")
        assert environment_manager is not None

        file_paths = ["pyproject.toml"]
        environment_manager.setup(str(model_dir_path), file_paths)

        self.check_setup(model_dir_path)


class TestConda:
    def check_setup(self, dir: Path) -> None:
        """Check if the Conda environment was set up correctly."""

        try:
            libs = os.listdir(dir / ".venv" / "lib")
        except FileNotFoundError:
            pytest.fail("Conda environment was not set up correctly: .venv/lib directory not found.")

        try:
            python_lib_path = [lib for lib in libs if lib.startswith("python")][0]
        except IndexError:
            pytest.fail("Conda environment was not set up correctly: Python lib directory not found.")

        try:
            libs = os.listdir(dir / ".venv" / "lib" / python_lib_path / "site-packages")
        except FileNotFoundError:
            pytest.fail("Conda environment was not set up correctly: site-packages directory not found.")

        assert any(lib.startswith("numpy") for lib in libs)

    def test_environment_yml(self, model_dir_path: Path) -> None:
        """Test Conda environment setup with environment.yml file."""

        environment_file_path = model_dir_path / "environment.yml"
        with open(environment_file_path, "w") as f:
            f.write("""name: test-env
channels:
  - defaults
dependencies:
  - python=3.13
  - numpy""")

        environment_manager = get_environment_manager("conda")
        assert environment_manager is not None

        file_paths = ["environment.yml"]
        environment_manager.setup(str(model_dir_path), file_paths)

        self.check_setup(model_dir_path)
