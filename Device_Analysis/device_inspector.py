# device_inspector.py
# Provides advanced inspection and metadata extraction from a connected Android device

import subprocess
from Utils.app_utils import cli_colors, display_utils

def show_advanced_insights(serial: str):
    """
    Perform deeper inspection of the Android device for research and cybersecurity purposes.

    Args:
        serial (str): Device serial number for targeting via ADB.
    """
    display_utils.print_section_title("Advanced Device Insights")

    shell_access = test_shell_access(serial)
    ip_address = get_ip_address(serial)
    app_count = count_installed_apps(serial)
    battery = get_battery_status(serial)
    storage = get_storage_info(serial)

    display_utils.print_status("Shell Access", shell_access)
    display_utils.print_status("IP Address", ip_address)
    display_utils.print_status("App Count", app_count)
    display_utils.print_status("Battery", battery)
    display_utils.print_status("Storage", storage)

    display_utils.print_divider()

def adb_shell(serial, command):
    """
    Helper to execute ADB shell commands.
    """
    try:
        result = subprocess.run(
            ["Utils\\Platform_Tools\\adb.exe", "-s", serial, "shell", command],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def test_shell_access(serial):
    """Check if shell access is available (root or user)."""
    output = adb_shell(serial, "id")
    return "yes (root)" if "uid=0" in output else ("yes (user)" if output else "no")

def get_ip_address(serial):
    """Attempt to extract device IP address."""
    output = adb_shell(serial, "ip route")
    try:
        return output.split()[8]
    except:
        return "Unavailable"

def count_installed_apps(serial):
    """Count total installed packages."""
    output = adb_shell(serial, "pm list packages")
    return str(len(output.splitlines())) if output else "0"

def get_battery_status(serial):
    """Parse battery level or power status."""
    output = adb_shell(serial, "dumpsys battery")
    for line in output.splitlines():
        if "level" in line.lower():
            return line.strip()
    return "Unavailable"

def get_storage_info(serial):
    """Return /data partition usage (total/used/available)."""
    output = adb_shell(serial, "df /data")
    lines = output.splitlines()
    if len(lines) >= 2:
        return lines[1]
    return "Unavailable"
