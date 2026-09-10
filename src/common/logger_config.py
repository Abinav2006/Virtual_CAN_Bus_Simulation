import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """Configure consistent application logging."""

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    handler.setFormatter(formatter)

    root_logger = logging.getLogger()

    root_logger.setLevel(level)

    root_logger.handlers.clear()
    root_logger.addHandler(handler)
