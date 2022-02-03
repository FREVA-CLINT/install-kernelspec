

import argparse
from typing import Dict, List, Optional
import sys
import install

def parse_args(argv: Optional[List[str]]) -> Dict[str, str]:
    """Construct command line argument parser."""
    argp = argparse.ArgumentParser
    ap = argp(prog="kernel-installer",
              description="Install jupyter kernel specs of different languages.",
              formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("language",
                    metavar="language",
                    type=str,
                    help="The programming language",
                    choices=install.__all__
    )
    ap.add_argument("--name", "-n",
                    help="The name of the kernel",
                    type=str,
                    default=None
    )
    ap.add_argument("--display-name", "-d",
                    help="The display name of the kernel",
    )
    args = ap.parse_args(argv)
    args.name = args.name or args.language
    return dict(language=args.language,
                name=args.name,
                display_name=args.display_name or args.name
    )


def cli(argv: Optional[List[str]] = None):

    config = parse_args(argv or sys.argv[1:])
    kernel_file = getattr(install, config["language"])(config["name"],
                                                       config["display_name"])
    print(f"Kernel has been successfully installed to {kernel_file}")


if __name__ == "__main__":
    cli()
