# main.py
# Entry point for the Stonehaven Android Security Toolkit

import sys
import time

from Utils.app_utils import cli_colors, menu_utils, about_app
from Utils.logging_utils import log_manager
from Device_Analysis import check_device

# ─────────────────────────────────────────────────────
# Global Configuration
# ─────────────────────────────────────────────────────

DEBUG = False
APP_TITLE = "Stonehaven - Static Android Security Toolkit"

# ─────────────────────────────────────────────────────
# Startup and Menu Logic
# ─────────────────────────────────────────────────────

def print_header():
    cli_colors.print_banner(APP_TITLE)
    log_manager.log_info("Application launched.")

def parse_args():
    global DEBUG
    if "--debug" in sys.argv:
        DEBUG = True
        cli_colors.print_debug("Debug mode enabled.")
        log_manager.log_info("Debug mode enabled.")

def handle_option(choice: str):
    """
    Execute selected menu option.
    """
    match choice:
        case "1":
            log_manager.log_info("User selected: Check for attached Devices")
            check_device.run_device_check()
        case "2":
            cli_colors.print_info("Connect to device — [TODO]")
            log_manager.log_info("User selected: Connect to device")
        case "3":
            cli_colors.print_info("Analyze Project Data — [TODO]")
            log_manager.log_info("User selected: Analyze Project Data")
        case "4":
            cli_colors.print_info("Application Utils — [TODO]")
            log_manager.log_info("User selected: Application Utils")
        case "5":
            log_manager.log_info("User selected: About Application")
            about_app.show_about()
        case "0":
            cli_colors.print_success("Exiting Stonehaven. Goodbye.")
            log_manager.log_info("Application exited by user.")
            sys.exit(0)
        case _:
            cli_colors.print_warning("Invalid option selected.")
            log_manager.log_warning(f"Invalid menu selection: {choice}")

def main_menu():
    """
    Display and process the main menu loop.
    """
    while True:
        options = {
            "1": "Check for attached Devices",
            "2": "Connect to device",
            "3": "Analyze Project Data",
            "4": "Application Utils",
            "5": "About Application",
            "0": "Exit"
        }

        menu_utils.display_menu("Main Menu", options, style="fancy")

        # ✅ Cast to set to match expected type
        valid_choices = set(options.keys())
        choice = menu_utils.get_user_choice(valid_choices)

        handle_option(choice)
        time.sleep(0.4)  # Soft pause after each operation

# ─────────────────────────────────────────────────────
# Entrypoint
# ─────────────────────────────────────────────────────

if __name__ == "__main__":
    parse_args()
    print_header()
    main_menu()
