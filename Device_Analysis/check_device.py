# check_device.py
# Entrypoint for checking connected Android devices via ADB

from Device_Analysis import device_scanner, device_display
from Utils.app_utils import cli_colors, display_utils
from Utils.logging_utils import log_manager

# ─────────────────────────────────────────────────────
# Main Entry Point for Device Scan
# ─────────────────────────────────────────────────────

def run_device_check():
    """
    Scan and display connected Android devices using ADB.
    Useful for pre-analysis staging and selection menus.
    """
    display_utils.print_section_title("Device Check")
    display_utils.print_timestamp("Check Started")
    log_manager.log_info("Initiating Android device check...")

    try:
        devices = device_scanner.get_connected_devices()

        if not devices:
            cli_colors.print_warning("No Android devices detected.")
            log_manager.log_warning("No devices reported by ADB.")
            return

        device_display.render_device_table(devices)

    except KeyboardInterrupt:
        cli_colors.print_warning("Device check cancelled by user.")
        log_manager.log_warning("User interrupted device check.")
    
    except Exception as e:
        cli_colors.print_error("An error occurred during device scan.")
        log_manager.log_exception(f"run_device_check() failed: {str(e)}")

