"""Definition of install methods."""

import json
import os
import shutil
from pathlib import Path
from subprocess import PIPE, CalledProcessError, run
from tempfile import TemporaryDirectory
from typing import Dict, Optional

import appdirs
from bash_kernel.install import kernel_json
from ipykernel.kernelspec import install as install_kernel
from jupyter_client.kernelspec import KernelSpecManager

__all__ = ["bash", "r", "python"]

KERNEL_DIR = Path(appdirs.user_data_dir("jupyter")) / "kernels"


def _install_rkernel(name: str, display_name: str) -> None:
    """Install the r kernel."""
    args = f'name="{name}", displayname="{display_name}", user=TRUE'
    cmd1 = ["Rscript", "-e", """'install.packages("IRkernel")'"""]
    cmd2 = [
        "Rscript",
        "--default-packages=IRkernel",
        "-e",
        f"""'IRkernel::installspec({args})'""",
    ]
    for cmd in (cmd1, cmd2):
        try:
            res = run(
                cmd, stdout=PIPE, stderr=PIPE, check=False, encoding="utf-8"
            )
            return_code = res.returncode
            stdout, stderr = res.stdout, res.stderr
        except (NotADirectoryError, FileNotFoundError):
            return_code = 1
            stdout, stderr = "", f"{cmd[0]}: No such file or directory"
        if return_code != 0:
            raise CalledProcessError(
                return_code,
                " ".join(cmd),
                output=stdout,
                stderr=stderr,
            )


def get_ld_library_path_from_bin(binary: str) -> Optional[str]:
    """Get the standard LD_LIBRARY_PATH from a binary."""
    bin_path = shutil.which(binary)
    if bin_path is None:
        return None
    for path in ("python", "python3"):
        python_path = Path(bin_path).parent / path
        if python_path.is_file():
            res = run(
                [str(python_path), "-c", "import sys; print(sys.exec_prefix)"],
                check=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            out = res.stdout.decode("utf-8").splitlines()[0]
            return str(Path(out) / "lib")
    return None


def get_env(*args: str) -> Dict[str, str]:
    """Get additional environment varialbes."""
    env = {}
    for arg in args:
        value = os.environ.get(arg, "")
        if value:
            env[arg] = value
    return env


def bash(name: str = "bash", display_name: Optional[str] = None) -> Path:
    """Install bash kernel spec."""

    name = name or "bash"
    kernel_json["display_name"] = display_name or name
    kernel_json["name"] = name
    env = get_env(
        "EVALUATION_SYSTEM_CONFIG_FILE", "EVALUATION_SYSTEM_CONFIG_DIR", "PATH"
    )
    kernel_json["env"] = env
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, "kernel.json"), "w", encoding="utf-8") as f:
            json.dump(kernel_json, f, sort_keys=True, indent=3)
        KernelSpecManager().install_kernel_spec(td, name, user=True)
    return KERNEL_DIR / name


def r(name: str = "r", display_name: Optional[str] = None) -> Path:
    """Install gnuR kernel spec."""
    name = name or "r"
    display_name = display_name or name
    env = get_env(
        "EVALUATION_SYSTEM_CONFIG_FILE",
        "EVALUATION_SYSTEM_CONFIG_DIR",
        "LD_LIBRARY_PATH",
    )
    ld_lib_path = get_ld_library_path_from_bin("R")
    if ld_lib_path and "LD_LIBRARY_PATH" not in env:
        env["LD_LIBRARY_PATH"] = ld_lib_path

    _install_rkernel(name, display_name)
    kernel = json.loads((KERNEL_DIR / name / "kernel.json").read_text())
    with (KERNEL_DIR / name / "kernel.json").open("w", encoding="utf-8") as f:
        kernel["env"] = env
        json.dump(kernel, f, indent=3)
    return KERNEL_DIR / name


def python(name: str = "python3", display_name: Optional[str] = None) -> Path:
    """Install python3 kernel spec."""
    env_kw = get_env(
        "EVALUATION_SYSTEM_CONFIG_FILE",
        "EVALUATION_SYSTEM_CONFIG_DIR",
    )
    path = install_kernel(
        user=True,
        kernel_name=name or "python3",
        display_name=display_name or name,
        env=env_kw,
    )
    return Path(path)
