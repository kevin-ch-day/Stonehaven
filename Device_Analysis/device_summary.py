# device_summary.py
# Display detailed analytical summary for a selected Android device

from Utils.app_utils import display_utils, cli_colors

def show_device_summary(device: dict):
    """
    Display analytical summary information for a connected Android device.

    Args:
        device (dict): Device metadata including serial, brand, model, android version, ABI, and system insights.
    """
    model_name = device.get("model", "Unknown")
    display_utils.print_section_title(f"Device Summary — {model_name}")

    # ─────────────────────────────
    # [1] Basic Device Identification
    # ─────────────────────────────
    cli_colors.print_section("Identification")
    display_utils.print_status("Serial Number", device.get("serial", "N/A"))
    display_utils.print_status("Brand", device.get("brand", "N/A"))
    display_utils.print_status("Model", model_name)
    display_utils.print_status("Android Version", device.get("android", "N/A"))
    display_utils.print_status("ABI (Arch)", device.get("abi", "N/A"))
    display_utils.print_status("API Level", device.get("api_level", "N/A"))
    display_utils.print_status("Build Fingerprint", device.get("build_fingerprint", "Unknown"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # [2] Security Posture & System Flags
    # ─────────────────────────────
    cli_colors.print_section("Security & System Integrity")
    display_utils.print_status("Root Access", device.get("root_status", "Unknown"))
    display_utils.print_status("Bootloader Unlocked", device.get("bootloader", "Unknown"))
    display_utils.print_status("USB Debugging Enabled", device.get("usb_debug", "Unknown"))
    display_utils.print_status("Developer Mode", device.get("developer_mode", "Unknown"))
    display_utils.print_status("Play Protect Status", device.get("play_protect", "Unknown"))
    display_utils.print_status("Custom ROM", device.get("custom_rom", "Unknown"))
    display_utils.print_status("SELinux Status", device.get("selinux", "Unknown"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # [3] Network & Connectivity
    # ─────────────────────────────
    cli_colors.print_section("Network & Connectivity")
    display_utils.print_status("IP Address", device.get("ip_address", "Unknown"))
    display_utils.print_status("MAC Address", device.get("mac_address", "Unknown"))
    display_utils.print_status("WiFi Status", device.get("wifi_status", "Unknown"))
    display_utils.print_status("Mobile Data Enabled", device.get("mobile_data", "Unknown"))
    display_utils.print_status("WiFi SSID", device.get("wifi_ssid", "Unknown"))
    display_utils.print_status("Signal Strength", device.get("signal_strength", "Unknown"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # [4] Installed Software & Storage
    # ─────────────────────────────
    cli_colors.print_section("Installed Software & Storage")
    display_utils.print_status("Installed App Count", device.get("app_count", "N/A"))
    display_utils.print_status("Known Antivirus Apps", device.get("antivirus_detected", "Unknown"))
    display_utils.print_status("Storage Mount Point", device.get("storage_mount", "Unknown"))
    display_utils.print_status("Storage Used", device.get("storage_used", "Unknown"))
    display_utils.print_status("Storage Free", device.get("storage_free", "Unknown"))
    display_utils.print_status("Raw Storage Info", device.get("storage", "Unavailable"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # [5] Battery & Power Health
    # ─────────────────────────────
    cli_colors.print_section("Battery & Power")
    display_utils.print_status("Battery Level", device.get("battery_level", "Unknown"))
    display_utils.print_status("Charging Status", device.get("charging", "Unknown"))
    display_utils.print_status("Battery Health", device.get("battery_health", "Unknown"))
    display_utils.print_status("Temperature (°C)", device.get("battery_temp", "Unknown"))
    display_utils.print_status("Raw Battery Info", device.get("battery", "Unavailable"))
    display_utils.print_spacer()

    # ─────────────────────────────
    # [6] Runtime Forensics
    # ─────────────────────────────
    cli_colors.print_section("Runtime & Debugging")
    display_utils.print_status("Shell Access", device.get("shell_access", "Unknown"))
    display_utils.print_status("ADB State", device.get("adb_state", "Unknown"))
    display_utils.print_status("Logcat Access", device.get("logcat", "Unknown"))
    display_utils.print_status("Time Zone", device.get("timezone", "Unknown"))
    display_utils.print_status("Locale", device.get("locale", "Unknown"))

    display_utils.print_thick_divider()
