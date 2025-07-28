# cli_colors.py
# Lightweight CLI color printing for Stonehaven (ASCII-safe fallback)

import os

# Determine if colors should be used
USE_COLORS = os.environ.get("NO_COLOR") is None

# Attempt colorama integration
if USE_COLORS:
    try:
        from colorama import Fore, Back, Style, init as colorama_init
        colorama_init(autoreset=True)
    except Exception:
        USE_COLORS = False

# Fallback dummy class if colorama is unavailable or disabled
if not USE_COLORS:
    class _NoColor:
        def __getattr__(self, name):
            return ""
    Fore = Back = Style = _NoColor()

# ─────────────────────────────────────────────────────
# Styled Message Printers
# ─────────────────────────────────────────────────────

def print_info(msg, return_str=False):
    text = f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}" if USE_COLORS else f"[INFO] {msg}"
    return text if return_str else print(text)

def print_success(msg, return_str=False):
    text = f"{Fore.GREEN}[OK]{Style.RESET_ALL} {msg}" if USE_COLORS else f"[OK] {msg}"
    return text if return_str else print(text)

def print_warning(msg, return_str=False):
    text = f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {msg}" if USE_COLORS else f"[WARNING] {msg}"
    return text if return_str else print(text)

def print_error(msg, return_str=False):
    text = f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}" if USE_COLORS else f"[ERROR] {msg}"
    return text if return_str else print(text)

def print_debug(msg, return_str=False):
    text = f"{Fore.LIGHTBLACK_EX}[DEBUG]{Style.RESET_ALL} {msg}" if USE_COLORS else f"[DEBUG] {msg}"
    return text if return_str else print(text)

# ─────────────────────────────────────────────────────
# Banners and Section Headings
# ─────────────────────────────────────────────────────

def print_banner(title, width=60):
    """
    Print a banner with equal signs and centered title.
    """
    line = "=" * width
    print(f"\n{line}")
    print(title.center(width))
    print(f"{line}\n")

def print_section(title, width=60):
    """
    Print a section heading with underlines.
    """
    print()
    print(title.upper())
    print("-" * min(len(title), width))

# ─────────────────────────────────────────────────────
# Color Control
# ─────────────────────────────────────────────────────

def set_color_mode(enabled=True):
    """
    Enable or disable color globally.
    """
    global USE_COLORS
    USE_COLORS = bool(enabled)
