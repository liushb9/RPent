"""Unified run logger — prints to stdout + records to a log file.

Usage::

    from physical_agent.utils.logging import init_run_logging, get_logger

    # Call once at startup, e.g. after make_log_dir():
    init_run_logging(log_dir)

    # Then anywhere:
    logger = get_logger("agent")
    logger.info("driver ready in %.1fs", elapsed)
    logger.error("driver exited before becoming ready")

The logger writes human-readable messages to stdout and timestamped,
machine-parseable records to ``<log_dir>/run.log``.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Singleton state
# ---------------------------------------------------------------------------

_log_initialized = False
_log_dir: Path | None = None


class _ColourFormatter(logging.Formatter):
    """Minimal colour formatter for stdout (no external deps)."""

    _COLOURS = {
        logging.DEBUG: "\033[90m",     # grey
        logging.INFO: "",
        logging.WARNING: "\033[93m",   # yellow
        logging.ERROR: "\033[91m",     # red
        logging.CRITICAL: "\033[95m",  # magenta
    }
    _RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        colour = self._COLOURS.get(record.levelno, "")
        record.levelname = f"{colour}{record.levelname}{self._RESET}"
        return super().format(record)


def init_run_logging(log_dir: str | Path | None = None) -> None:
    """Initialise the run logger.

    Must be called once (typically at process start).  Subsequent calls
    are no-ops.

    Parameters
    ----------
    log_dir:
        Directory that receives ``run.log``.  When *None* only stdout
        logging is active.
    """
    global _log_initialized, _log_dir

    if _log_initialized:
        return

    root = logging.getLogger()  # the Python root logger
    root.setLevel(logging.DEBUG)
    root.handlers.clear()

    # -- stdout handler (INFO and above) ----------------------------------
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(
        _ColourFormatter("[%(name)s] %(message)s")
    )
    root.addHandler(stdout_handler)

    # -- file handler (DEBUG and above, timestamped) ---------------------
    if log_dir is not None:
        _log_dir = Path(log_dir)
        _log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(
            str(_log_dir / "run.log"), encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        root.addHandler(file_handler)

    _log_initialized = True


def get_logger(name: str = "") -> logging.Logger:
    """Return a logger with the given name.

    The logger inherits handlers from the root logger configured by
    ``init_run_logging``.  Passing an empty string returns the root
    logger itself.

    Typical usage::

        logger = get_logger("agent")
        logger.info("driver ready in %.1fs", elapsed)

    or with a dotted name::

        logger = get_logger("cerebrum.anthropic")
    """
    if name:
        return logging.getLogger(name)
    return logging.getLogger()


def get_log_dir() -> Path | None:
    """Return the log directory set by the last ``init_run_logging`` call."""
    return _log_dir