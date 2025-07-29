# log_engine.py
# Core logging class for Stonehaven with structured configuration

import os
import logging
from logging.handlers import RotatingFileHandler
from Utils.app_utils import cli_colors
from . import log_config

class LogEngine:
    """
    Central logging engine for Stonehaven.
    Provides a configurable and reusable logger with rotation and console support.
    """

    def __init__(self, logger_name="stonehaven_logger"):
        self.logger = logging.getLogger(logger_name)
        self.console_handler = None
        self.file_handler = None
        self.logger.setLevel(log_config.LOG_LEVEL)
        self._setup_handlers()

    def _setup_handlers(self):
        """Attach file and optional console handlers to the logger."""
        if self.logger.handlers:
            return  # Prevent handler duplication on re-import

        os.makedirs(log_config.LOG_DIR, exist_ok=True)

        self.file_handler = self._create_file_handler()
        self.file_handler.setFormatter(self._get_formatter())
        self.file_handler.setLevel(self.logger.level)
        self.logger.addHandler(self.file_handler)

        if log_config.LOG_TO_CONSOLE:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setLevel(self.logger.level)
            self.console_handler.setFormatter(self._get_formatter(color=True))
            self.logger.addHandler(self.console_handler)

    def _create_file_handler(self):
        """Create a file or rotating file handler."""
        if log_config.ENABLE_ROTATION:
            return RotatingFileHandler(
                log_config.LOG_FILE_PATH,
                maxBytes=log_config.MAX_LOG_SIZE_MB * 1024 * 1024,
                backupCount=log_config.BACKUP_COUNT,
                encoding='utf-8'
            )
        return logging.FileHandler(log_config.LOG_FILE_PATH, encoding='utf-8')

    def _get_formatter(self, color: bool = False):
        """Return a log formatter. Colorized when requested."""
        base = logging.Formatter(
            fmt=log_config.LOG_FORMAT,
            datefmt=log_config.DATE_FORMAT
        )
        if not color or not cli_colors.USE_COLORS:
            return base

        class ColorFormatter(logging.Formatter):
            LEVEL_COLORS = {
                logging.DEBUG: cli_colors.dim_gray,
                logging.INFO: cli_colors.cyan,
                logging.WARNING: cli_colors.yellow,
                logging.ERROR: cli_colors.red,
                logging.CRITICAL: cli_colors.red,
            }

            def format(self, record):
                msg = super().format(record)
                color_func = self.LEVEL_COLORS.get(record.levelno)
                return color_func(msg) if color_func else msg

        return ColorFormatter(log_config.LOG_FORMAT, log_config.DATE_FORMAT)

    def get_logger(self):
        """Return the configured logger instance."""
        return self.logger

    # Convenience wrappers
    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)

    def exception(self, msg: str):
        """Log an exception with traceback (used in except blocks)."""
        self.logger.exception(msg)

    # ------------------------------------------------------------------
    # Runtime Configuration
    # ------------------------------------------------------------------
    def set_level(self, level: str) -> None:
        """Dynamically adjust logging level."""
        lvl = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(lvl)
        if self.file_handler:
            self.file_handler.setLevel(lvl)
        if self.console_handler:
            self.console_handler.setLevel(lvl)

    def enable_console(self, enabled: bool = True) -> None:
        """Enable or disable console logging at runtime."""
        if enabled and not self.console_handler:
            self.console_handler = logging.StreamHandler()
            self.console_handler.setLevel(self.logger.level)
            self.console_handler.setFormatter(self._get_formatter(color=True))
            self.logger.addHandler(self.console_handler)
        elif not enabled and self.console_handler:
            self.logger.removeHandler(self.console_handler)
            self.console_handler = None


# Optional accessor for shared logger instance
def get_default_logger():
    """Return a ready-to-use singleton logger instance."""
    return LogEngine().get_logger()
