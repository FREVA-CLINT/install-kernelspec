"""Tests for the CLI."""

from pathlib import Path

from jupyter_kernel_install.cli import cli


def test_cli(python_kernel: Path) -> None:
    """Tests for the cli."""
    cli(["python", "--name", f"{python_kernel.name}"])
    assert (python_kernel / "kernel.json").is_file()
