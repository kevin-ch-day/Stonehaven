# cli_colors.py
# Terminal color formatting utility for Stonehaven (NSA/Matrix style)
# ASCII-safe fallback using colorama (if available)

import os

# ------------------------------------------------------------
# Global Color Toggle and Setup
# ------------------------------------------------------------

USE_COLORS = os.environ.get("NO_COLOR") is None

try:
    if USE_COLORS:
        from colorama import Fore as _Fore, Back as _Back, Style as _Style, init as colorama_init
        colorama_init(autoreset=True)
        Fore, Back, Style = _Fore, _Back, _Style
    else:
        raise ImportError
except Exception:
    USE_COLORS = False

if not USE_COLORS:
    class _NoColor:
        def __getattr__(self, attr):
            return ""

    Fore = Back = Style = _NoColor()

# ------------------------------------------------------------
# Color Formatters (Wrappers)
# ------------------------------------------------------------

def green(text: str) -> str:
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}" if USE_COLORS else text

def bold_green(text: str) -> str:
    return f"{Style.BRIGHT}{Fore.GREEN}{text}{Style.RESET_ALL}" if USE_COLORS else text

def dim_gray(text: str) -> str:
    return f"{Style.DIM}{Fore.LIGHTBLACK_EX}{text}{Style.RESET_ALL}" if USE_COLORS else text

def cyan(text: str) -> str:
    return f"{Fore.CYAN}{text}{Style.RESET_ALL}" if USE_COLORS else text

def yellow(text: str) -> str:
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}" if USE_COLORS else text

def red(text: str) -> str:
    return f"{Fore.RED}{text}{Style.RESET_ALL}" if USE_COLORS else text

def white(text: str) -> str:
    return f"{Fore.WHITE}{text}{Style.RESET_ALL}" if USE_COLORS else text

def blue(text: str) -> str:
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}" if USE_COLORS else text

# ------------------------------------------------------------
# Log-Style Print Helpers
# ------------------------------------------------------------

def print_info(msg: str, return_str: bool = False):
    text = f"{cyan('[INFO]')} {msg}"
    return text if return_str else print(text)

def print_success(msg: str, return_str: bool = False):
    text = f"{green('[ OK ]')} {msg}"
    return text if return_str else print(text)

def print_warning(msg: str, return_str: bool = False):
    text = f"{yellow('[WARN]')} {msg}"
    return text if return_str else print(text)

def print_error(msg: str, return_str: bool = False):
    text = f"{red('[FAIL]')} {msg}"
    return text if return_str else print(text)

def print_debug(msg: str, return_str: bool = False):
    text = f"{dim_gray('[DEBUG]')} {msg}"
    return text if return_str else print(text)

# ------------------------------------------------------------
# Banner and Section Headings
# ------------------------------------------------------------

def print_banner(title: str, width: int = 60):
    """
    Prints a stylized banner box.
    """
    border = "=" * width
    print()
    print(bold_green(border))
    print(bold_green(title.center(width)))
    print(bold_green(border))
    print()

def print_section(title: str, width: int = 60):
    """
    Prints a section title with underline.
    """
    print()
    print(bold_green(title.upper()))
    print(bold_green("-" * min(width, len(title))))

def print_subheading(text: str, width: int = 60):
    """
    Prints a dim-style subheading padded to width.
    """
    print(dim_gray(text.ljust(width)))

# ------------------------------------------------------------
# CLI Prompts and Symbols
# ------------------------------------------------------------

def prompt_symbol() -> str:
    return bold_green(">>> ")

def matrix_highlight(msg: str) -> str:
    return bold_green(f"> {msg}")

def matrix_border(width: int = 60) -> str:
    return bold_green("#" * width)

# ------------------------------------------------------------
# Toggle Color Support
# ------------------------------------------------------------

def set_color_mode(enabled: bool = True) -> None:
    global USE_COLORS
    USE_COLORS = bool(enabled)
