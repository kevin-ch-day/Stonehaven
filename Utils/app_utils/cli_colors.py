# cli_colors.py
# Terminal color formatting utility for Stonehaven (NSA/Matrix style)
# ASCII-safe fallback using colorama (if available)

import os

# ─────────────────────────────────────────────────────
# Global Color Toggle and Setup
# ─────────────────────────────────────────────────────

USE_COLORS = os.environ.get("NO_COLOR") is None

try:
    if USE_COLORS:
        from colorama import Fore, Back, Style, init as colorama_init
        colorama_init(autoreset=True)
except Exception:
    USE_COLORS = False

# Dummy fallback for colorless environments
if not USE_COLORS:
    class _NoColor:
        def __getattr__(self, attr): return ""
    Fore = Back = Style = _NoColor()

# ─────────────────────────────────────────────────────
# Base Color Wrappers
# ─────────────────────────────────────────────────────

def green(text): return f"{Fore.GREEN}{text}{Style.RESET_ALL}" if USE_COLORS else text
def bold_green(text): return f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}" if USE_COLORS else text
def dim_gray(text): return f"{Style.DIM}{Fore.LIGHTBLACK_EX}{text}{Style.RESET_ALL}" if USE_COLORS else text
def cyan(text): return f"{Fore.CYAN}{text}{Style.RESET_ALL}" if USE_COLORS else text
def yellow(text): return f"{Fore.YELLOW}{text}{Style.RESET_ALL}" if USE_COLORS else text
def red(text): return f"{Fore.RED}{text}{Style.RESET_ALL}" if USE_COLORS else text
def white(text): return f"{Fore.WHITE}{text}{Style.RESET_ALL}" if USE_COLORS else text
def blue(text): return f"{Fore.BLUE}{text}{Style.RESET_ALL}" if USE_COLORS else text

# ─────────────────────────────────────────────────────
# Message Style Printers (Log Style)
# ─────────────────────────────────────────────────────

def print_info(msg, return_str=False):
    text = f"{cyan('[INFO]')} {msg}"
    return text if return_str else print(text)

def print_success(msg, return_str=False):
    text = f"{green('[ OK ]')} {msg}"
    return text if return_str else print(text)

def print_warning(msg, return_str=False):
    text = f"{yellow('[WARN]')} {msg}"
    return text if return_str else print(text)

def print_error(msg, return_str=False):
    text = f"{red('[FAIL]')} {msg}"
    return text if return_str else print(text)

def print_debug(msg, return_str=False):
    text = f"{dim_gray('[DEBUG]')} {msg}"
    return text if return_str else print(text)

# ─────────────────────────────────────────────────────
# Title and Section Formatters
# ─────────────────────────────────────────────────────

def print_banner(title, width=60):
    """
    Prints a Matrix-style title banner.
    """
    border = "=" * width
    print()
    print(bold_green(border))
    print(bold_green(title.center(width)))
    print(bold_green(border))
    print()

def print_section(title, width=60):
    """
    Prints a section heading with underline.
    """
    print()
    print(bold_green(title.upper()))
    print(bold_green("-" * min(len(title), width)))

def print_subheading(text, width=60):
    """
    Prints a dim, subtle subheading.
    """
    print(dim_gray(text.ljust(width)))

# ─────────────────────────────────────────────────────
# CLI Enhancers
# ─────────────────────────────────────────────────────

def prompt_symbol():
    """
    Returns a stylized prompt prefix.
    """
    return bold_green(">>> ")

def matrix_highlight(msg):
    """
    NSA-style visual highlight.
    """
    return bold_green(f"» {msg}")

def matrix_border(width=60):
    return bold_green("■" * width)

# ─────────────────────────────────────────────────────
# Dynamic Toggle for Color Mode
# ─────────────────────────────────────────────────────

def set_color_mode(enabled=True):
    global USE_COLORS
    USE_COLORS = bool(enabled)

