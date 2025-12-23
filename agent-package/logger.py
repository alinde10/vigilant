# logger.py
"""
Logging utility
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

NAME = "vigilant"
LOG_DIR_PATH = Path(__file__).parent / "logs"


def setup_logger(name=NAME, log_dir_path=LOG_DIR_PATH, level=logging.INFO):
    """
    Set up simple logger with console and file output

    Args:
        name: Logger name
        log_dir_path: Path object for directory for log files
        level: Logging level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers?
    if logger.handlers:
        return logger

    log_dir_path.mkdir(exist_ok=True)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", "%H:%M:%S"
    )
    console_handler.setFormatter(console_format)

    # File handler (rotating, max 10MB, keep 3 backups)
    file_handler = RotatingFileHandler(
        log_dir_path / f"{name}.log", maxBytes=10 * 1024 * 1024, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(funcName)s | %(message)s"
    )
    file_handler.setFormatter(file_format)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
