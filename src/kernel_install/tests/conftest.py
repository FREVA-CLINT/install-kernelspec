"""Collection of test definitions."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

import pytest

import kernel_install


@pytest.fixture(scope="function")
def r_kernel() -> Iterator[Path]:
    """Set the name of the python kernel."""
    out = kernel_install.install.KERNEL_DIR / "r_test"
    yield out


@pytest.fixture(scope="function")
def bash_kernel() -> Iterator[Path]:
    """Set the name of the python kernel."""
    out = kernel_install.install.KERNEL_DIR / "bash_test"
    yield out


@pytest.fixture(scope="function")
def python_kernel() -> Iterator[Path]:
    """Set the name of the python kernel."""
    out = kernel_install.install.KERNEL_DIR / "python_test"
    yield out
    for r in out.rglob("*.*"):
        r.unlink()
    out.rmdir()
