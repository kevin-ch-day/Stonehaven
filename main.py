# main.py
# Entry point for the Stonehaven Android Security Toolkit

import sys
import time

from Utils.app_utils import cli_colors, menu_utils, about_app, display_utils
from Utils.logging_utils import log_manager
from Device_Analysis import check_device, connect_to_device

# ------------------------------------------------------------
# Global Configuration
# ------------------------------------------------------------

DEBUG = False
APP_TITLE = "Stonehaven - Static Android Security Toolkit"

# ------------------------------------------------------------
# Startup and Session Initialization
# ------------------------------------------------------------

def print_header():
    display_utils.print_divider("=")
    print("  Stonehaven CLI Launcher")
    display_utils.print_divider("-")
    cli_colors.print_banner(APP_TITLE)
    log_manager.log_info("Application launched.")

def parse_args():
    global DEBUG
    if "--debug" in sys.argv:
        DEBUG = True
        cli_colors.print_debug("Debug mode enabled.")
        log_manager.log_info("Debug mode enabled.")

def graceful_exit(message: str = "Exiting Stonehaven. Goodbye."):
    """
    Exit handler to ensure clean shutdown.
    """
    cli_colors.print_success(message)
    log_manager.log_info("Application exited by user.")
    display_utils.print_spacer()
    display_utils.print_thick_divider()
    sys.exit(0)

# ------------------------------------------------------------
# Menu Handling
# ------------------------------------------------------------

def handle_option(choice: str):
    """
    Execute selected menu option.
    """
    try:
        match choice:
            case "1":
                log_manager.log_info("User selected: Check for attached Devices")
                check_device.run_device_check()

            case "2":
                log_manager.log_info("User selected: Connect to device")
                connect_to_device.run()

            case "3":
                log_manager.log_info("User selected: Analyze Project Data")
                cli_colors.print_info("Analyze Project Data — [TODO]")

            case "4":
                log_manager.log_info("User selected: Application Utils")
                cli_colors.print_info("Application Utils — [TODO]")

            case "5":
                log_manager.log_info("User selected: About Application")
                about_app.show_about()

            case "0":
                graceful_exit()

            case _:
                cli_colors.print_warning("Invalid option selected.")
                log_manager.log_warning(f"Invalid menu selection: {choice}")

    except Exception as e:
        cli_colors.print_error("An error occurred while processing your selection.")
        log_manager.log_exception(f"Exception in handle_option: {str(e)}")

def main_menu():
    """
    Display and process the main menu loop.
    """
    options = {
        "1": "Check for attached Devices",
        "2": "Connect to device",
        "3": "Analyze Project Data",
        "4": "Application Utils",
        "5": "About Application",
        "0": "Exit"
    }

    valid_choices = set(options.keys())

    while True:
        try:
            display_utils.print_thick_divider()
            menu_utils.display_menu("Main Menu", options, style="fancy")
            choice = menu_utils.get_user_choice(valid_choices)
            handle_option(choice)
            time.sleep(0.4)

        except KeyboardInterrupt:
            cli_colors.print_error("[FAIL] Keyboard interrupt detected. Returning to menu.")
            log_manager.log_warning("Keyboard interrupt during menu interaction.")
            display_utils.print_spacer()

# ------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------

if __name__ == "__main__":
    try:
        parse_args()
        print_header()
        main_menu()

    except KeyboardInterrupt:
        cli_colors.print_info("\n[INFO] Keyboard interrupt received at top level.")
        log_manager.log_info("Application terminated via keyboard interrupt.")
        graceful_exit()
