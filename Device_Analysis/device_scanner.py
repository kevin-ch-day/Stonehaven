# device_scanner.py
# Core logic for scanning Android devices via ADB and extracting properties

import subprocess
import os
from Utils.app_utils import cli_colors
from Utils.logging_utils import log_manager

ADB_PATH = os.path.join("Utils", "Platform_Tools", "adb.exe")

# ─────────────────────────────────────────────────────
# Main Scanner Interface
# ─────────────────────────────────────────────────────

def get_connected_devices() -> list[dict]:
    """
    Scans for connected Android devices and extracts basic info.

    Returns:
        list of dicts with keys:
        'serial', 'brand', 'model', 'android', 'abi'
    """
    if not os.path.isfile(ADB_PATH):
        cli_colors.print_error("ADB not found at expected path.")
        log_manager.log_error("adb.exe is missing in Platform_Tools.")
        return []

    try:
        result = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            cli_colors.print_error("ADB returned a non-zero exit code.")
            log_manager.log_error("ADB returned failure code.")
            return []

        serials = _parse_serials(result.stdout.strip().splitlines())
        if not serials:
            cli_colors.print_warning("No online Android devices detected.")
            log_manager.log_info("No active ADB devices found.")
            return []

        devices = []
        for serial in serials:
            props = _get_device_props(serial)
            devices.append({
                "serial": serial,
                "brand": props.get("brand", "?"),
                "model": props.get("model", "?"),
                "android": props.get("android", "?"),
                "abi": props.get("abi", "?")
            })

        cli_colors.print_success(f"{len(devices)} device(s) successfully scanned.")
        return devices

    except subprocess.TimeoutExpired:
        cli_colors.print_error("ADB command timed out.")
        log_manager.log_exception("ADB timeout during device scan.")
        return []
    except Exception as e:
        cli_colors.print_error("Unexpected error occurred during ADB scan.")
        log_manager.log_exception(f"Device scan exception: {e}")
        return []

# ─────────────────────────────────────────────────────
# Helper: Extract Serial Numbers from ADB Output
# ─────────────────────────────────────────────────────

def _parse_serials(lines: list[str]) -> list[str]:
    """
    Parse output lines from `adb devices` and extract valid online serials.

    Args:
        lines (list): ADB output lines

    Returns:
        list: Serial numbers for online devices
    """
    serials = []
    for line in lines[1:]:  # Skip first line ("List of devices attached")
        parts = line.strip().split()
        if len(parts) == 2 and parts[1] == "device":
            serials.append(parts[0])
        elif len(parts) == 2 and parts[1] != "device":
            cli_colors.print_warning(f"Skipping device with state '{parts[1]}': {parts[0]}")
    return serials

# ─────────────────────────────────────────────────────
# Helper: Retrieve Device Properties via ADB getprop
# ─────────────────────────────────────────────────────

def _get_device_props(serial: str) -> dict:
    """
    Query essential device properties using ADB getprop.

    Args:
        serial (str): Serial number of the device

    Returns:
        dict: Device property dictionary
    """
    return {
        "brand": _getprop(serial, "ro.product.brand"),
        "model": _getprop(serial, "ro.product.model"),
        "android": _getprop(serial, "ro.build.version.release"),
        "abi": _getprop(serial, "ro.product.cpu.abi")
    }

def _getprop(serial: str, key: str) -> str:
    """
    Helper function to call adb getprop.

    Args:
        serial (str): Serial number
        key (str): Property key

    Returns:
        str: Property value or '?'
    """
    try:
        result = subprocess.run([ADB_PATH, "-s", serial, "shell", "getprop", key],
                                capture_output=True, text=True, timeout=3)
        return result.stdout.strip() if result.returncode == 0 else "?"
    except Exception as e:
        log_manager.log_warning(f"getprop failed for {serial}:{key} - {e}")
        return "?"
