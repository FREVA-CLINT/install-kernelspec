import json
import os
from pathlib import Path
from subprocess import CalledProcessError
import shlex
import sys
from tempfile import TemporaryDirectory
from typing import Optional

__all__ = ["bash", "r", "python"]

KERNEL_DIR = Path('~/.local/share/jupyter/kernels').expanduser()

def bash(name: str = "bash", display_name: Optional[str] = None) -> Path:
    """Install bash kernel spec."""
    from bash_kernel.install import kernel_json
    from jupyter_client.kernelspec import KernelSpecManager
    name = name or "bash"
    kernel_json["display_name"] = display_name or name
    kernel_json["name"] = name
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
             json.dump(kernel_json, f, sort_keys=True)
        KernelSpecManager().install_kernel_spec(td, name, user=True)
    return KERNEL_DIR / name


def r(name: str = "r", display_name: Optional[str] = None) -> Path:
    """Install gnuR kernel spec."""
    name = name or "r"
    display_name = display_name or name
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


def python(name: str = "python3", display_name: Optional[str] = None) -> Path:
    """Install python3 kernel spec."""
    from ipykernel.kernelspec import install as install_kernel
    path = install_kernel(
        user=True,
        kernel_name=name or "python3",
        display_name=display_name or name
    )
    return Path(path)
