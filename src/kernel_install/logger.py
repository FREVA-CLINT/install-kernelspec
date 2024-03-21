"""Definition of the central logging system."""

import logging

import rich.logging

THIS_NAME: str = "install-kernel"
logger_format = logging.Formatter(
    "%(name)s - %(asctime)s - %(levelname)s: %(message)s",
    # datefmt="%Y-%m-%dT%H:%M:%S",
    datefmt="[%X]",
)

logger_stream_handle = rich.logging.RichHandler(rich_tracebacks=True)
logger_stream_handle.setLevel(logging.ERROR)

logger = logging.getLogger(THIS_NAME)
logger.setLevel(logging.ERROR)
logger.addHandler(logger_stream_handle)
