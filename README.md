# Install Kernelspec

This code installs jupyter kernels for different languages in the user space.

## Installation
```python
python3 -m pip install git+https://gitlab.dkrz.de/k204230/install-kernelspec.git
```

## Usage

### Using the command line interface (cli):

```bash
kernel-install --help
usage: kernel-install [-h] [--name NAME] [--display-name DISPLAY_NAME] language

Install jupyter kernel specs of different languages.

positional arguments:
  language              The programming language

options:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  The name of the kernel (default: None)
  --display-name DISPLAY_NAME, -d DISPLAY_NAME
                        The display name of the kernel (default: None)
```

currently supported kernels are:
- python3
- gnuR
- bash

Example for installing a gnuR kernel:

```bash
kernel-install r --name r-regiklim --display-name "R for Regiklim"
```

### Using the python library

Example for programatically installing a bash kernel:

```python
import kernel_install as ki
ki.bash(name="bash-regiklim", display_name="bash kernel")
```

