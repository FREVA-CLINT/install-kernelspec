#!/usr/bin/env python3
"""Setup script for packaging checkin."""

from pathlib import Path
import re
from setuptools import setup, find_packages


NAME = "kernel_install"


def read(*parts):
    """Read the content of a file."""
    script_path = Path(__file__).parent
    with script_path.joinpath(*parts).open() as f:
        return f.read()


def find_version(*parts):
    """The the version in a given file."""
    vers_file = read(*parts)
    match = re.search(r'^__version__ = "(\d+.\d+.\d+)"', vers_file, re.M)
    if match is not None:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name=NAME,
    version=find_version("src", "kernel_install", "_version.py"),
    author="Martin Bergemann",
    author_email="bergemann@dkrz.de",
    maintainer="Martin Bergemann",
    url="https://gitlab.dkrz.de/k204230/install-kernelspec",
    description="utility to install various jupyter kernel specs.",
    long_description=read("README.md"),
    license="GPLv3",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": ["jupyter-kernel-install = kernel_install.cli:cli"]
    },
    install_requires=["argparse", "bash_kernel", "ipykernel"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
