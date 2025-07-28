# log_manager.py
# Centralized logging manager for Stonehaven

import os
from . import log_config, log_engine

# ─────────────────────────────────────────────────────
# Ensure Logs Directory Exists
# ─────────────────────────────────────────────────────
os.makedirs(log_config.LOG_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────
# Initialize Singleton Logger
# ─────────────────────────────────────────────────────
_logger_instance = log_engine.LogEngine()
logger = _logger_instance.get_logger()

# ─────────────────────────────────────────────────────
# Global Logging Utility Functions
# ─────────────────────────────────────────────────────

def get_logger():
    """
    Retrieve the configured Stonehaven logger instance.

    Returns:
        logging.Logger: Logger with handlers and formatting applied.
    """
    return logger

def log_debug(msg: str):
    """Log a debug-level message."""
    logger.debug(msg)

def log_info(msg: str):
    """Log an informational message."""
    logger.info(msg)

def log_warning(msg: str):
    """Log a warning message."""
    logger.warning(msg)

def log_error(msg: str):
    """Log an error message."""
    logger.error(msg)

def log_critical(msg: str):
    """Log a critical error message."""
    logger.critical(msg)

def log_exception(msg: str):
    """
    Log an error message with full exception traceback.

    Should be called inside an `except` block.
    """
    logger.exception(msg)

def log_banner(msg: str):
    """
    Log a centered section header with banner borders.

    Args:
        msg (str): The section title to highlight in the log.
    """
    border = "=" * 60
    logger.info(border)
    logger.info(msg.center(60))
    logger.info(border)
