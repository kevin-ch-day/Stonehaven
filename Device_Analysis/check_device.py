# check_device.py
# Entrypoint for checking connected Android devices via ADB

from Device_Analysis import device_scanner, device_display
from Utils.app_utils import cli_colors, display_utils
from Utils.logging_utils import log_manager

# ─────────────────────────────────────────────────────
# Main Entry Point for Device Scan
# ─────────────────────────────────────────────────────

@log_manager.log_call("info")
def run_device_check() -> int:
    """
    Scan and display connected Android devices using ADB.

    Returns:
        int: Exit code (0 = success, 1 = failure or no devices)
    """
    display_utils.print_section_title("Device Check")
    display_utils.print_timestamp("Check Started")
    log_manager.log_info("Initiating Android device check...")

    try:
        scanner = device_scanner.DeviceScanner()
        devices = scanner.scan()

        if not devices:
            cli_colors.print_warning("No Android devices detected.")
            log_manager.log_warning("No devices reported by ADB.")
            return 1

        cli_colors.print_success(f"{len(devices)} device(s) successfully scanned.")
        device_display.render_device_table(devices)
        log_manager.log_info(f"{len(devices)} device(s) displayed.")
        display_utils.print_timestamp("Check Finished")
        return 0

    except KeyboardInterrupt:
        cli_colors.print_warning("Device check cancelled by user.")
        log_manager.log_warning("User interrupted device check.")
        return 1

    except Exception as e:
        cli_colors.print_error("An unexpected error occurred during device scan.")
        log_manager.log_exception(f"run_device_check() failed: {str(e)}")
        return 1
