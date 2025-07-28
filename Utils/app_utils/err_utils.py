# err_utils.py
# Global error handling and warnings for the Stonehaven project

from . import cli_colors
import sys
import traceback

# ─────────────────────────────────────────────────────
# General-Purpose Error Handler
# ─────────────────────────────────────────────────────

def handle_exception(exc: Exception, context: str = "Unhandled Exception"):
    """
    Central handler for uncaught exceptions.

    Args:
        exc (Exception): The caught exception object.
        context (str): Optional description of where the error occurred.
    """
    cli_colors.print_error(f"{context}: {str(exc)}")
    traceback_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
    for line in traceback_lines:
        sys.stderr.write(line)

# ─────────────────────────────────────────────────────
# Warning Handler
# ─────────────────────────────────────────────────────

def warn(msg: str):
    """
    Print a formatted warning message.

    Args:
        msg (str): Warning message text.
    """
    cli_colors.print_warning(msg)

# ─────────────────────────────────────────────────────
# Critical Error Handler
# ─────────────────────────────────────────────────────

def critical_exit(msg: str, exit_code: int = 1):
    """
    Show an error message and terminate the application.

    Args:
        msg (str): Error message to display.
        exit_code (int): Optional exit code (default = 1).
    """
    cli_colors.print_error(msg)
    sys.exit(exit_code)
