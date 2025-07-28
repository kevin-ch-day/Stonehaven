# menu_utils.py
# ASCII-only CLI menu utility for Stonehaven with color support

from . import cli_colors

# ─────────────────────────────────────────────────────
# Convenience Constants
# ─────────────────────────────────────────────────────

RETURN_OPTION_KEY = "0"
RETURN_OPTION_LABEL = "Return to Previous Menu / Exit"

# ─────────────────────────────────────────────────────
# Main Menu Display Function
# ─────────────────────────────────────────────────────

def display_menu(title, options, style="fancy"):
    """
    Display a formatted CLI menu.

    Args:
        title (str): Title of the menu screen.
        options (dict): Mapping of keys to option labels.
        style (str): 'fancy' (default) or 'simple'
    """
    if RETURN_OPTION_KEY not in options:
        options = {**options, RETURN_OPTION_KEY: RETURN_OPTION_LABEL}

    cli_colors.print_banner(title)
    if style.lower() == "fancy":
        _display_fancy_menu(options)
    else:
        _display_simple_menu(title, options)

# ─────────────────────────────────────────────────────
# Simple Menu Layout
# ─────────────────────────────────────────────────────

def _display_simple_menu(title, options):
    """Flat, minimal layout for compact display."""
    print("-" * 60)
    cli_colors.print_info(title)
    print("-" * 60)
    for key in sorted(options):
        print(f"[{key}] {options[key]}")
    print("-" * 60)

# ─────────────────────────────────────────────────────
# Fancy Centered Menu Layout
# ─────────────────────────────────────────────────────

def _display_fancy_menu(options):
    """Centered and boxed layout with spacing."""
    width = 60
    border = "=" * width
    print(border)
    for key in sorted(options):
        label = f"[{key}] {options[key]}"
        print(label.center(width))
    print(border)

# ─────────────────────────────────────────────────────
# User Input Handler
# ─────────────────────────────────────────────────────

def get_user_choice(valid_choices, prompt="Enter choice: "):
    """
    Prompt the user until a valid menu choice is selected.

    Args:
        valid_choices (list or set): Valid option keys (as strings).
        prompt (str): Input prompt to show the user.

    Returns:
        str: Validated user input.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input in valid_choices:
            return user_input
        cli_colors.print_warning("Invalid selection. Please try again.")
