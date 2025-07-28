# device_display.py
# Displays a formatted NSA-style table of connected Android devices

from Utils.app_utils import cli_colors, display_utils
import textwrap

# ─────────────────────────────────────────────────────
# Column Layout Settings
# ─────────────────────────────────────────────────────

COLUMN_WIDTHS = {
    "No.": 4,
    "Serial": 17,
    "Brand": 12,
    "Model": 25,
    "Android": 9,
    "ABI": 10
}

COLUMNS = ["No.", "Serial", "Brand", "Model", "Android", "ABI"]

# ─────────────────────────────────────────────────────
# Public Display Function
# ─────────────────────────────────────────────────────

def render_device_table(device_list: list[dict], title: str = "Connected Android Devices") -> None:
    """
    Render a formatted table of Android devices.

    Args:
        device_list (list): List of dictionaries with keys:
            'serial', 'brand', 'model', 'android', 'abi'
        title (str): Optional section header
    """
    if not device_list:
        cli_colors.print_warning("No devices to display.")
        return

    display_utils.print_spacer()
    cli_colors.print_banner(f"{title}")
    cli_colors.print_info(f"{len(device_list)} device(s) detected:\n")

    # Header + Divider
    header = " ".join(f"{col:<{COLUMN_WIDTHS[col]}}" for col in COLUMNS)
    divider = "-" * len(header)
    print(cli_colors.bold_green(header))
    print(cli_colors.green(divider))

    # Rows
    for idx, device in enumerate(device_list, start=1):
        row_data = {
            "No.": str(idx),
            "Serial": device.get("serial", "N/A"),
            "Brand": device.get("brand", "N/A"),
            "Model": _shorten(device.get("model", "N/A"), COLUMN_WIDTHS["Model"]),
            "Android": device.get("android", "N/A"),
            "ABI": device.get("abi", "N/A")
        }

        row = " ".join(f"{row_data[col]:<{COLUMN_WIDTHS[col]}}" for col in COLUMNS)
        print(cli_colors.cyan(row))

    display_utils.print_spacer()

# ─────────────────────────────────────────────────────
# Helper: Model Truncation if Too Long
# ─────────────────────────────────────────────────────

def _shorten(text: str, limit: int) -> str:
    """Trim text to fit within column width, append '…' if trimmed."""
    if len(text) <= limit:
        return text
    try:
        return textwrap.shorten(text, width=limit, placeholder="…")
    except Exception:
        return text[:limit - 1] + "…"
