# Install Kernel Specifications into userspace

[![Pipeline](https://github.com/FREVA-CLINT/install-kernelspec/actions/workflows/ci_job.yml/badge.svg)](https://github.com/FREVA-CLINT/install-kernelspec/actions)
[![codecov](https://codecov.io/gh/FREVA-CLINT/install-kernelspec/graph/badge.svg?token=90RyY5I9AI)](https://codecov.io/gh/FREVA-CLINT/install-kernelspec)
[![BSD](https://anaconda.org/conda-forge/freva/badges/license.svg)](https://github.com/FREVA-CLINT/install-kernelspec/LICENSE)

This code installs jupyter kernels for different languages into the user space.
Once the kernel has been installed it can be used on the [jupyter-hub server](https://jupyterhub.dkrz.de/)
of DKRZ.

## Installation
```python
python3 -m pip install kernel-install
```

## Usage

### Using the command line interface (cli):

```console
jupyter-kernel-install --help
```

```bash
Usage: jupyter-kernel-install [-h] [--name NAME] [--display-name DISPLAY_NAME] [--version] language

Install jupyter kernel specs of different languages.

Positional Arguments:
  language              The programming language

Options:
  -h, --help            show this help message and exit
  --name, -n NAME       The name of the kernel (default: None)
  --display-name, -d DISPLAY_NAME
                        The display name of the kernel (default: None)
  --version, -V         Display version and exit
```
Alternatively you can use:

```console
python -m jupyter_kernel_install --help
```

The following kernel specifications are supported:
- python3
- gnuR
- bash

Example for installing a gnuR kernel:

```console
kernel-install r --name r-regiklim --display-name "R for Regiklim"
```

### Using the python library

Example for programmatically installing a bash kernel:

```python
import kernel_install as ki
kernel_path = ki.bash(name="bash-regiklim", display_name="bash kernel")
```

## Contributing
Any contributions are welcome. To start developing we recommend creating a new
[mini conda environment](https://docs.conda.io/projects/conda/en/latest/index.html).

```console
conda env create -f environment.yml; conda activate install-kernelspec
```
Unit tests, building the documentation, type annotations and code style tests
are done with [tox](https://tox.wiki/en/latest/). To run all tests, linting
in parallel simply execute the following command:

```console
tox -p 3
```
You can also run the each part alone, for example to only check the code style:

```console
tox -e lint
```
available options are ``lint``, ``types`` and ``test``.

Tox runs in a separate python environment to run the tests in the current
environment use:

```console
pytest
```
