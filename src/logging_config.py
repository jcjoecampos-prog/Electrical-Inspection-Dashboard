import logging

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

def configure_logging() -> None:
    """
    Configure application-wide logging.
    """
    logging.basicConfig(
        level = logging.INFO,
        format  =LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S"
    )