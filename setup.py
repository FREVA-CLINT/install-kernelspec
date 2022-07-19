#!/usr/bin/env python3
"""Setup script for packaging checkin."""

import json
from pathlib import Path
from setuptools import setup, find_packages


NAME = "kernel_install"


def read(*parts):
    """Read the content of a file."""
    script_path = Path(__file__).parent
    with script_path.joinpath(*parts).open() as f:
        return f.read()


def find_version(pck_name: str = "kernel_install"):
    vers_file = Path(__file__).parent / "src" / pck_name / "__init__.py"
    with vers_file.open() as f:
        for line in f.readlines():
            if "__version__" in line:
                return json.loads(line.split("=")[-1].strip())


setup(
    name=NAME,
    version=find_version(NAME),
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
