# connect_to_device.py
# Handles selection and interaction with connected Android devices

import time
from Device_Analysis import device_scanner, device_display
from Utils.app_utils import cli_colors, display_utils, menu_utils
from Utils.logging_utils import log_manager

# ------------------------------------------------------------
# Device Interaction Menu Logic
# ------------------------------------------------------------

def run():
    """
    Display connected devices and allow user to select one.
    """
    display_utils.print_section_title("Connect to Device")
    display_utils.print_divider()
    display_utils.print_timestamp("Session Start")
    log_manager.log_info("User entered Connect to Device menu.")

    try:
        devices = device_scanner.get_connected_devices()

        if not devices:
            cli_colors.print_warning("No devices available for connection.")
            log_manager.log_warning("No connected devices found.")
            return

        cli_colors.print_info(f"{len(devices)} Android device(s) available.")
        device_display.render_device_table(devices)

        cli_colors.print_section("Device Selection")
        print("\nEnter device number to connect or 0 to return to main menu:")

        valid_choices = {str(i + 1) for i in range(len(devices))}
        valid_choices.add("0")

        choice = menu_utils.get_user_choice(valid_choices)

        if choice == "0":
            cli_colors.print_info("Returning to main menu.")
            return

        index = int(choice) - 1
        if index < 0 or index >= len(devices):
            cli_colors.print_warning("Invalid device selection.")
            return

        selected = devices[index]

        cli_colors.print_success(f"Connected to: {selected['model']} [{selected['serial']}]")
        log_manager.log_info(f"Device selected: {selected}")

        launch_device_menu(selected)

    except Exception as e:
        cli_colors.print_error("Failed to connect to device.")
        log_manager.log_exception(f"Exception in connect_to_device.run: {str(e)}")

# ------------------------------------------------------------
# Device-Specific Menu
# ------------------------------------------------------------

def launch_device_menu(device):
    """
    Display menu options for the selected device.
    """
    cli_colors.print_banner(f"Device Menu - {device['model']}")
    log_manager.log_info("Entered device-specific menu.")

    start_time = time.time()

    while True:
        options = {
            "1": "Show device summary",
            "2": "Perform APK scan [TODO]",
            "3": "Pull data from device [TODO]",
            "0": "Back to Main Menu"
        }

        menu_utils.display_menu("Device Interaction", options)
        choice = menu_utils.get_user_choice(set(options.keys()))

        match choice:
            case "1":
                display_utils.print_section_title(f"Device Summary - {device['model']}")
                for key in ["serial", "brand", "model", "android", "abi"]:
                    display_utils.print_status(key.capitalize(), device[key])
                display_utils.print_divider()
            case "2":
                cli_colors.print_info("APK scan coming soon.")
            case "3":
                cli_colors.print_info("Data pull coming soon.")
            case "0":
                elapsed = round(time.time() - start_time, 2)
                log_manager.log_info(f"Exited device menu after {elapsed} seconds.")
                cli_colors.print_info("Returning to main menu.")
                break
            case _:
                cli_colors.print_warning("Invalid choice. Try again.")
