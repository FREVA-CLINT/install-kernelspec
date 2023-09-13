import argparse
from pathlib import Path
from typing import Dict, List, Optional, Callable
import sys
from .install import __all__ as methods
from ._version import __version__


def parse_args(argv: Optional[List[str]]) -> Dict[str, str]:
    """Construct command line argument parser."""
    argp = argparse.ArgumentParser
    ap = argp(
        prog="jupyter-kernel-install",
        description="Install jupyter kernel specs of different languages.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument(
        "language",
        metavar="language",
        type=str,
        help="The programming language",
        choices=methods,
    )
    ap.add_argument(
        "--name", "-n", help="The name of the kernel", type=str, default=None
    )
    ap.add_argument(
        "--display-name",
        "-d",
        help="The display name of the kernel",
    )
    ap.add_argument(
        "--version",
        "-V",
        help="Display version and exit",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )
    args = ap.parse_args(argv)
    args.name = args.name or args.language
    return dict(
        language=args.language,
        name=args.name,
        display_name=args.display_name or args.name,
    )


def get_method(method: str) -> Callable[str, Path]:
    """Get the correct install method."""

    from kernel_install import install

    return getattr(install, method)


def cli(argv: Optional[List[str]] = None):
    config = parse_args(argv or sys.argv[1:])
    kernel_file = get_method(config["language"])(config["name"], config["display_name"])
    print(f"Kernel has been successfully installed to {kernel_file}")


if __name__ == "__main__":
    cli()
