# menu_utils.py
# CLI menu utility for Stonehaven – Matrix / NSA ASCII-style interface

from . import cli_colors

# ─────────────────────────────────────────────────────
# Menu Visual Constants
# ─────────────────────────────────────────────────────

RETURN_OPTION_KEY = "0"
RETURN_OPTION_LABEL = "Exit Application"

BORDER_CHAR = "#"
BULLET_CHAR = ">>"
PADDING_WIDTH = 64

# ─────────────────────────────────────────────────────
# Main Menu Entry Point
# ─────────────────────────────────────────────────────

def display_menu(title: str, options: dict, style: str = "fancy"):
    """
    Display a formatted CLI menu screen.

    Args:
        title (str): Section header text.
        options (dict): Key-value menu mapping.
        style (str): Layout style: 'fancy' (default) or 'simple'.
    """
    if RETURN_OPTION_KEY not in options:
        options[RETURN_OPTION_KEY] = RETURN_OPTION_LABEL

    _print_banner(title)

    if style.lower() == "fancy":
        _display_fancy_menu(options)
    else:
        _display_simple_menu(title, options)

# ─────────────────────────────────────────────────────
# Fancy NSA-Inspired Left-Aligned Menu Layout
# ─────────────────────────────────────────────────────

def _display_fancy_menu(options: dict):
    """NSA-style CLI layout, left-aligned with ASCII bullets."""
    print(cli_colors.green(BORDER_CHAR * PADDING_WIDTH))

    sorted_keys = sorted(options, key=lambda k: (k == RETURN_OPTION_KEY, k))
    for key in sorted_keys:
        label = f"{BULLET_CHAR} [{key}] {options[key]}"
        print(cli_colors.bold_green(label.ljust(PADDING_WIDTH)))

    print(cli_colors.green(BORDER_CHAR * PADDING_WIDTH))
    print()

# ─────────────────────────────────────────────────────
# Minimal Layout (Optional Alternative)
# ─────────────────────────────────────────────────────

def _display_simple_menu(title: str, options: dict):
    """Flat text-based layout, useful for narrow terminals."""
    print("-" * PADDING_WIDTH)
    cli_colors.print_info(title)
    print("-" * PADDING_WIDTH)

    for key in sorted(options, key=lambda k: (k == RETURN_OPTION_KEY, k)):
        print(f"[{key}] {options[key]}")

    print("-" * PADDING_WIDTH)
    print()

# ─────────────────────────────────────────────────────
# Banner with Bold Cyber Flair
# ─────────────────────────────────────────────────────

def _print_banner(title: str):
    """Center-aligned section header with Matrix-style ASCII borders."""
    print()
    print(cli_colors.bold_green("=" * PADDING_WIDTH))
    print(cli_colors.bold_green(title.center(PADDING_WIDTH)))
    print(cli_colors.bold_green("=" * PADDING_WIDTH))
    print()

# ─────────────────────────────────────────────────────
# Menu Choice Handler
# ─────────────────────────────────────────────────────

def get_user_choice(valid_choices: set, prompt: str = ">>> Select Option: ") -> str:
    """
    Prompt until a valid menu option is selected.

    Args:
        valid_choices (set): Acceptable keys (as strings).
        prompt (str): CLI input prompt.

    Returns:
        str: Validated user selection.
    """
    while True:
        try:
            user_input = input(cli_colors.cyan(prompt)).strip()
            if user_input in valid_choices:
                return user_input
            cli_colors.print_warning("Invalid selection. Try again.")
        except KeyboardInterrupt:
            cli_colors.print_error("Keyboard interrupt detected. Returning to menu.")
            return RETURN_OPTION_KEY
