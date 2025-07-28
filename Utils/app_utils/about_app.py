# about_app.py
# Display application metadata and description for Stonehaven

from . import cli_colors
from . import app_config
from . import display_utils

def show_about():
    """Display structured application metadata and purpose screen."""
    cli_colors.print_banner(f"About {app_config.APP_NAME}")
    display_utils.print_thick_divider()

    # ──────────────────────────────────────────────────────────
    # Metadata Section
    # ──────────────────────────────────────────────────────────
    cli_colors.print_section("Application Metadata")

    display_kv("Name", app_config.APP_NAME)
    display_kv("Version", app_config.VERSION)
    display_kv("License", app_config.LICENSE)
    display_kv("Repository", app_config.REPOSITORY)
    display_kv("Documentation", app_config.DOCUMENTATION)

    display_utils.print_spacer()

    # ──────────────────────────────────────────────────────────
    # Purpose Section
    # ──────────────────────────────────────────────────────────
    cli_colors.print_section("Purpose")

    print("  Stonehaven is a modular command-line toolkit designed for")
    print("  Android security research and application inspection. It is")
    print("  built to support fieldwork, local audits, and CI-based scanning.")
    print()
    print("  Core capabilities include:")
    print("   - Static inspection of APK files")
    print("   - Android permission and manifest profiling")
    print("   - Hash integrity verification (SHA256)")
    print("   - Integration with ADB and platform-tools")
    print("   - Modular design for extensibility")

    display_utils.print_spacer()

    # ──────────────────────────────────────────────────────────
    # Extra Section (Optional)
    # ──────────────────────────────────────────────────────────
    cli_colors.print_section("Session Information")
    display_utils.print_timestamp("Session Time")

    display_utils.print_spacer()
    display_utils.print_thick_divider()
    print()

def display_kv(label: str, value: str):
    """
    Helper to print key-value metadata entries.
    """
    cli_colors.print_info(f"{label}:")
    print(f"  {value}")
    print()
