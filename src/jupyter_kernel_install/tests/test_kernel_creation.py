"""Tests for creating the kernel."""

import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import mock
import pytest

from jupyter_kernel_install import bash, python, r
from jupyter_kernel_install.install import get_ld_library_path_from_bin


def test_ld_library_path() -> None:
    """Test the ld library path recognition."""
    with TemporaryDirectory() as temp_dir:
        env = os.environ.copy()
        env["PATH"] = temp_dir
        (Path(temp_dir) / "foo").touch(mode=0o755)
        with mock.patch.dict(os.environ, env, clear=True):
            assert get_ld_library_path_from_bin("foo") is None
        assert isinstance(get_ld_library_path_from_bin("python"), str)


def test_r(r_kernel: Path) -> None:
    """Test the creation of a python kernel."""
    r(name=r_kernel.name)
    assert (r_kernel / "kernel.json").is_file()


def test_failed_r() -> None:
    """Test failing of the r kernel."""
    env = os.environ.copy()
    env["PATH"] = "/foo"
    with mock.patch.dict(os.environ, env, clear=True):
        with pytest.raises(subprocess.CalledProcessError):
            r()


def test_python(python_kernel: Path) -> None:
    """Test the creation of a python kernel."""
    python(name=python_kernel.name)
    assert (python_kernel / "kernel.json").is_file()


def test_bash(bash_kernel: Path) -> None:
    """Test the creation of a python kernel."""
    bash(name=bash_kernel.name)
    assert (bash_kernel / "kernel.json").is_file()
