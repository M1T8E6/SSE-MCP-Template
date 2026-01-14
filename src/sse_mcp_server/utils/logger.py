# pylint: disable=C0116
"""
Enhanced logging module that provides functionality to create and configure loggers.
It supports console logging with rich formatting and optional file logging.
Log levels and formats are configurable.
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, Union

from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme


class StructuredLogger:
    """Wrapper for logging.Logger that accepts structured keyword arguments."""

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def _format(self, msg: str, kwargs: dict) -> str:
        if kwargs:
            try:
                props = " " + str(kwargs)
            except (TypeError, ValueError):
                props = ""
            return f"{msg}|{props}"
        return msg

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(self._format(msg, kwargs), *args)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(self._format(msg, kwargs), *args)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(self._format(msg, kwargs), *args)

    warn = warning

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.error(self._format(msg, kwargs), *args)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._logger.critical(self._format(msg, kwargs), *args)

    # Provide access to underlying logger methods if needed
    def get_underlying(self) -> logging.Logger:
        return self._logger


# Dictionary to store created loggers to prevent duplicates
_LOGGER_CACHE: Dict[str, StructuredLogger] = {}


def get_console_logger(
    name: str | None = "default",
    level: Union[int, str] = logging.DEBUG,
    log_file: str | Path | None = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    use_rich: bool = True,
) -> StructuredLogger:
    """
    Retrieves or creates a logger with the specified configuration.

    Args:
        name (str, optional): The name of the logger. Defaults to "default".
        level (Union[int, str], optional): The logging level. Defaults to logging.DEBUG.
        log_file (Optional[Union[str, Path]], optional): Path to a log file. If provided, logs
            will be written to this file.
        log_format (str, optional): Format string for log messages.
        use_rich (bool, optional): Whether to use rich formatting for console output.
            Defaults to True.

    Returns:
        logging.Logger: The configured logger.
    """

    # Ensure name is always a string
    if name is None:
        name = "default"

    # Check if logger with this name already exists in cache
    if name in _LOGGER_CACHE:
        return _LOGGER_CACHE[name]

    # Get or create logger
    base_logger = logging.getLogger(name)

    # Only configure if no handlers exist
    if not base_logger.handlers:
        # Convert string level to int if needed
        if isinstance(level, str):
            level = logging.getLevelName(level.upper())

        base_logger.setLevel(level)
        base_logger.propagate = False  # Prevent duplicate logs

        # Console handler with optional Rich formatting
        if use_rich:
            # Create a custom theme for rich console
            custom_theme = Theme(
                {
                    "info": "green",
                    "warning": "yellow",
                    "error": "bold red",
                    "critical": "bold white on red",
                }
            )
            console = Console(theme=custom_theme)
            console_handler = RichHandler(
                console=console,
                rich_tracebacks=True,
                markup=True,
                show_time=False,  # Time will be in the formatter
            )
        else:
            console_handler = logging.StreamHandler()

        console_handler.setLevel(level)
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        base_logger.addHandler(console_handler)

        # File handler (if log_file is provided)
        if log_file:
            log_path = Path(log_file)

            # Create directory if it doesn't exist
            os.makedirs(log_path.parent, exist_ok=True)

            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(level)
            file_formatter = logging.Formatter(log_format)
            file_handler.setFormatter(file_formatter)
            base_logger.addHandler(file_handler)

    wrapped = StructuredLogger(base_logger)
    _LOGGER_CACHE[name] = wrapped
    return wrapped


def clear_logger_cache():
    """Clears the logger cache, useful for testing or reconfiguration."""
    _LOGGER_CACHE.clear()
