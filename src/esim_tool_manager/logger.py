"""
Centralized logging system for eSim Tool Manager.
Logs actions, detections, installations, and diagnostics to both rotating log files and terminal.
"""

from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

DEFAULT_LOG_DIR = Path("logs")
DEFAULT_LOG_FILE = DEFAULT_LOG_DIR / "esim_manager.log"


def get_logger(name: str = "esim_manager", log_file: Path | None = None, verbose: bool = False) -> logging.Logger:
    """
    Configure and return a standardized logger instance.
    Writes structured logs to file and optionally to console.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured
        return logger

    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False

    # Standard formatter for file output
    file_formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Determine target log file path
    target_log_file = log_file or DEFAULT_LOG_FILE

    # Attempt to configure file handler
    try:
        target_log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            target_log_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except (OSError, PermissionError) as err:
        # If unable to write to log directory, add a fallback warning stream
        sys.stderr.write(f"[WARNING] Could not initialize log file at {target_log_file}: {err}\n")

    return logger
