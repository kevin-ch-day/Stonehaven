# display_utils.py
# Shared visual display helpers for Stonehaven CLI output

import datetime
from . import cli_colors

# ─────────────────────────────────────────────────────
# Timestamp Utilities
# ─────────────────────────────────────────────────────

def get_timestamp() -> str:
    """
    Return current timestamp in 12-hour format: MM-DD-YYYY HH:MM AM/PM
    """
    return datetime.datetime.now().strftime("%m-%d-%Y %I:%M %p")


def print_timestamp(prefix: str = "Timestamp"):
    """
    Print a timestamp with an optional label.
    """
    ts = get_timestamp()
    cli_colors.print_info(f"{prefix}: {ts}")

# ─────────────────────────────────────────────────────
# Section + Divider Utilities
# ─────────────────────────────────────────────────────

def print_divider(char: str = "-", width: int = 60):
    """
    Print a simple horizontal divider.
    """
    print(char * width)


def print_thick_divider(width: int = 60):
    """
    Print a solid Matrix-style divider using █.
    """
    print(cli_colors.bold_green("█" * width))


def print_spacer(lines: int = 1):
    """
    Print vertical spacing (blank lines).
    """
    for _ in range(lines):
        print()


def print_section_title(title: str, width: int = 60):
    """
    Print a section title with underline.
    """
    cli_colors.print_banner(title, width)

# ─────────────────────────────────────────────────────
# Status Output Helpers
# ─────────────────────────────────────────────────────

def print_status(key: str, value: str, width: int = 60):
    """
    Print a key-value status entry with fixed spacing.

    Example:
        Device ID   : emulator-5554
    """
    formatted = f"{key:<20}: {value}"
    print(cli_colors.green(formatted))


def print_inline_result(label: str, result: str, status: str = "OK"):
    """
    Print a labeled result in-line with optional color for status.

    Example:
        APK Size: 34.2MB [OK]
    """
    status_color = {
        "OK": cli_colors.green,
        "FAIL": cli_colors.red,
        "WARN": cli_colors.yellow,
        "INFO": cli_colors.cyan
    }

    color_func = status_color.get(status.upper(), cli_colors.white)
    status_tag = f"[{status.upper()}]"
    print(f"{cli_colors.cyan(label)}: {cli_colors.green(result)} {color_func(status_tag)}")
