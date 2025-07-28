# log_engine.py
# Core logging class for Stonehaven with structured configuration

import os
import logging
from logging.handlers import RotatingFileHandler
from . import log_config

class LogEngine:
    """
    Central logging engine for Stonehaven.
    Provides a configurable and reusable logger with rotation and console support.
    """

    def __init__(self, logger_name="stonehaven_logger"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_config.LOG_LEVEL)
        self._setup_handlers()

    def _setup_handlers(self):
        """Attach file and optional console handlers to the logger."""
        if self.logger.handlers:
            return  # Prevent handler duplication on re-import

        os.makedirs(log_config.LOG_DIR, exist_ok=True)

        file_handler = self._create_file_handler()
        file_handler.setFormatter(self._get_formatter())
        self.logger.addHandler(file_handler)

        if log_config.LOG_TO_CONSOLE:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_config.LOG_LEVEL)
            console_handler.setFormatter(self._get_formatter())
            self.logger.addHandler(console_handler)

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

    def _get_formatter(self):
        """Return a log formatter using standard format and date format."""
        return logging.Formatter(
            fmt=log_config.LOG_FORMAT,
            datefmt=log_config.DATE_FORMAT
        )

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


# Optional accessor for shared logger instance
def get_default_logger():
    """Return a ready-to-use singleton logger instance."""
    return LogEngine().get_logger()
