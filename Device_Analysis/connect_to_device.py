# connect_to_device.py
# Main interface for connecting and interacting with Android devices

import time
from Device_Analysis import (
    device_scanner,
    device_display,
    device_summary,
    device_data_collector,
)
from Utils.app_utils import cli_colors, display_utils, menu_utils
from Utils.logging_utils import log_manager


@log_manager.log_call("info")
def run():
    _print_header()
    log_manager.log_info("User entered Connect to Device menu.")

    try:
        scanner = device_scanner.DeviceScanner()
        devices = scanner.scan()

        if not devices:
            cli_colors.print_warning("No Android devices found.")
            log_manager.log_warning("Device scan returned 0 results.")
            return

        cli_colors.print_success(f"[ OK ] {len(devices)} device(s) successfully scanned.\n")
        cli_colors.print_info(f"[INFO] {len(devices)} Android device(s) detected:\n")
        device_display.render_device_table(devices)

        cli_colors.print_section("DEVICE SELECTION")
        print("Enter the number of the device to connect, or 0 to return to main menu.")
        print("-" * 60)

        valid_choices = _get_valid_choices(devices)
        user_choice = menu_utils.get_user_choice(valid_choices)

        if user_choice == "0":
            cli_colors.print_info("Returning to main menu.")
            return

        selected_index = int(user_choice) - 1
        selected_device = devices[selected_index]

        log_manager.log_info(f"Selected device: {selected_device}")
        cli_colors.print_success(
            f"[ OK ] Connected to {selected_device['model']} [{selected_device['serial']}]"
        )

        # Enrich metadata
        cli_colors.print_info("[INFO] Collecting detailed device info...")
        start = time.time()
        full_device = device_data_collector.collect_full_device_info(selected_device)
        elapsed = round(time.time() - start, 2)

        log_manager.log_info(f"Collected metadata for device: {full_device}")
        cli_colors.print_info(f"[INFO] Metadata collected in {elapsed} seconds.\n")

        _launch_device_menu(full_device)

    except Exception as e:
        cli_colors.print_error("[ERROR] Failed to connect to device.")
        log_manager.log_exception(f"Exception in connect_to_device.run: {str(e)}")


# ─────────────────────────────────────────────────────────────
# UI/Display Helpers
# ─────────────────────────────────────────────────────────────

def _print_header():
    display_utils.print_section_title("Connect to Device")
    display_utils.print_divider()
    display_utils.print_timestamp("Session Start")


def _get_valid_choices(devices):
    return {str(i + 1) for i in range(len(devices))}.union({"0"})


def _launch_device_menu(device):
    cli_colors.print_banner(f"Device Menu - {device['model']}")
    log_manager.log_info("Launched device-specific menu.")
    session_start = time.time()

    while True:
        options = {
            "1": "Show device summary",
            "2": "Perform APK scan [TODO]",
            "3": "Pull data from device [TODO]",
            "0": "Back to Main Menu"
        }

        menu_utils.display_menu("Device Interaction", options)
        user_choice = menu_utils.get_user_choice(set(options.keys()))

        match user_choice:
            case "1":
                log_manager.log_info("Option: Show device summary selected.")
                device_summary.show_device_summary(device)

            case "2":
                cli_colors.print_info("[INFO] APK scan feature coming soon.")
                log_manager.log_info("Option: APK scan selected. (TODO)")

            case "3":
                cli_colors.print_info("[INFO] Data extraction coming soon.")
                log_manager.log_info("Option: Pull data from device selected. (TODO)")

            case "0":
                elapsed = round(time.time() - session_start, 2)
                log_manager.log_info(f"Exited device menu after {elapsed} seconds.")
                cli_colors.print_info("Returning to main menu.")
                break

            case _:
                cli_colors.print_warning("Invalid choice. Please try again.")
