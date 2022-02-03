import os
from pathlib import Path
from subprocess import CalledProcessError
import shlex
import sys
from typing import Optional

__all__ = ["r", "python"]

KERNEL_DIR = Path('~/.local/share/jupyter/kernels').expanduser()

def r(name="r", display_name: Optional[str] = None) -> Path:
    """Install gnuR kernel spec."""
    cmd = (
            f"{Path(sys.executable).parent / 'Rscript'} "
            "--default-packages=IRkernel "
            "-e "
            f"""'IRkernel::installspec(name="{name}", displayname="{display_name}")'"""
    )
    res = os.system(cmd)
    if res != 0:
        raise CalledProcessError(res, cmd)
    return KERNEL_DIR / name

def python(name="python3", display_name: Optional[str] = None) -> Path:
    """Install python3 kernel spec."""
    from ipykernel.kernelspec import install as install_kernel
    path = install_kernel(
        user=True,
        kernel_name=name,
        display_name=display_name or name
    )
    return Path(path)
