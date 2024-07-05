"""Main command line interface."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Callable, Dict, List, Optional, cast

from rich import print as pprint
from rich_argparse import ArgumentDefaultsRichHelpFormatter

from jupyter_kernel_install import __version__, install

from .install import __all__ as methods
from .logger import logger, logger_stream_handle


def parse_args(argv: Optional[List[str]]) -> Dict[str, str]:
    """Construct command line argument parser."""
    argp = argparse.ArgumentParser
    ap = argp(
        prog="jupyter-kernel-install",
        description="Install jupyter kernel specs of different languages.",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
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
        "-v", "--verbose", action="count", help="Verbosity level", default=0
    )
    ap.add_argument(
        "--version",
        "-V",
        help="Display version and exit",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args = ap.parse_args(argv)
    args.name = args.name or args.language
    log_level = max(
        logger.getEffectiveLevel() - 10 * args.verbose, logging.DEBUG
    )

    logger.setLevel(log_level)
    logger_stream_handle.setLevel(log_level)
    return {
        "language": args.language,
        "name": args.name,
        "display_name": args.display_name or args.name,
    }


def get_method(method: str) -> Callable[[str, str], Path]:
    """Get the correct install method."""

    return cast(Callable[[str, str], Path], getattr(install, method))


def cli(argv: Optional[List[str]] = None) -> None:
    """The main cli message."""
    config = parse_args(argv or sys.argv[1:])
    kernel_file = get_method(config["language"])(
        config["name"], config["display_name"]
    )
    pprint(f"Kernel has been successfully installed to [b]{kernel_file}[/b]")
