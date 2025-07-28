# device_summary.py
# Display analytical summary details for a selected Android device

from Utils.app_utils import display_utils, cli_colors


def show_device_summary(device: dict):
    """
    Display analytical summary information for a connected Android device.

    Args:
        device (dict): Device metadata including serial, brand, model, android version, ABI, and optional system insights.
    """
    model_name = device.get("model", "Unknown")
    display_utils.print_section_title(f"Device Summary - {model_name}")

    # ─────────────────────────────
    # Basic Device Identification
    # ─────────────────────────────
    cli_colors.print_section("Identification")
    display_utils.print_status("Serial", device.get("serial", "N/A"))
    display_utils.print_status("Brand", device.get("brand", "N/A"))
    display_utils.print_status("Model", device.get("model", "N/A"))
    display_utils.print_status("Android", device.get("android", "N/A"))
    display_utils.print_status("ABI", device.get("abi", "N/A"))
    display_utils.print_status("API Level", device.get("api_level", "N/A"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # Security-Relevant Attributes
    # ─────────────────────────────
    cli_colors.print_section("Security & System Attributes")
    display_utils.print_status("Root Access", device.get("root_status", "Unknown"))
    display_utils.print_status("USB Debugging", device.get("usb_debug", "Unknown"))
    display_utils.print_status("Play Protect", device.get("play_protect", "Unknown"))
    display_utils.print_status("Custom ROM", device.get("custom_rom", "Unknown"))
    display_utils.print_status("SELinux", device.get("selinux", "Unknown"))
    display_utils.print_status("Bootloader Unlocked", device.get("bootloader", "Unknown"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # Network & Access Insights
    # ─────────────────────────────
    cli_colors.print_section("Network & Connectivity")
    display_utils.print_status("IP Address", device.get("ip_address", "Unknown"))
    display_utils.print_status("MAC Address", device.get("mac_address", "Unknown"))
    display_utils.print_status("WiFi Status", device.get("wifi_status", "Unknown"))
    display_utils.print_status("Mobile Data", device.get("mobile_data", "Unknown"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # Installed Software & Storage
    # ─────────────────────────────
    cli_colors.print_section("Installed Software & Storage")
    display_utils.print_status("Installed Apps", device.get("app_count", "N/A"))
    display_utils.print_status("Antivirus Found", device.get("antivirus_detected", "Unknown"))
    display_utils.print_status("Internal Storage (Used)", device.get("storage_used", "Unknown"))
    display_utils.print_status("Internal Storage (Free)", device.get("storage_free", "Unknown"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # Battery & Power State
    # ─────────────────────────────
    cli_colors.print_section("Battery & Power")
    display_utils.print_status("Battery Level", device.get("battery_level", "Unknown"))
    display_utils.print_status("Charging Status", device.get("charging", "Unknown"))
    display_utils.print_status("Battery Health", device.get("battery_health", "Unknown"))
    display_utils.print_spacer()
    display_utils.print_thick_divider()
