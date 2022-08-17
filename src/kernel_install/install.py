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

def get_env(*args):
    """Get additional environment varialbes."""
    env = {}
    for arg in args:
        value = os.environ.get(arg, "")
        if value:
            env[arg] = value
    if env:
        return dict(env=env)
    return {}

def bash(name: str = "bash", display_name: Optional[str] = None) -> Path:
    """Install bash kernel spec."""
    from bash_kernel.install import kernel_json
    from jupyter_client.kernelspec import KernelSpecManager
    name = name or "bash"
    kernel_json["display_name"] = display_name or name
    kernel_json["name"] = name
    env = get_env("EVALUATION_SYSTEM_CONFIG_FILE")
    if env:
        kernel_json["env"] = env["env"]
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
             json.dump(kernel_json, f, sort_keys=True, indent=3)
        KernelSpecManager().install_kernel_spec(td, name, user=True)
    return KERNEL_DIR / name


def r(name: str = "r", display_name: Optional[str] = None) -> Path:
    """Install gnuR kernel spec."""
    name = name or "r"
    display_name = display_name or name
    cmd = (
            "Rscript "
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
    eval_conf = os.environ.get("EVALUATION_SYSTEM_CONFIG_FILE", "")
    env_kw = get_env("EVALUATION_SYSTEM_CONFIG_FILE")
    path = install_kernel(
        user=True,
        kernel_name=name or "python3",
        display_name=display_name or name,
        **env_kw
    )
    return Path(path)
