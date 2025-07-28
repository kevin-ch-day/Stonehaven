# about_app.py
# Display application metadata and description for Stonehaven

from . import cli_colors
from . import app_config

def show_about():
    """Display structured application metadata and purpose."""
    cli_colors.print_banner(f"About {app_config.APP_NAME}")

    print("".ljust(60, "-"))
    cli_colors.print_info("Application Name:")
    print(f"  {app_config.APP_NAME}\n")

    cli_colors.print_info("Version:")
    print(f"  {app_config.VERSION}\n")

    cli_colors.print_info("License:")
    print(f"  {app_config.LICENSE}\n")

    cli_colors.print_info("Repository:")
    print(f"  {app_config.REPOSITORY}\n")

    cli_colors.print_info("Documentation:")
    print(f"  {app_config.DOCUMENTATION}\n")

    cli_colors.print_info("Purpose:")
    print("  Stonehaven is a modular command-line application designed")
    print("  for security researchers and analysts. Its core functionality")
    print("  includes static inspection of Android applications, permission")
    print("  profiling, and hash-based integrity verification using ADB and")
    print("  native Android platform tools.\n")

    print("".ljust(60, "-"))
    print()
