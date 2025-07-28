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
    Scans for connected Android devices and returns device info.

    Returns:
        list of dicts with keys:
        'serial', 'brand', 'model', 'android', 'abi'
    """
    if not os.path.isfile(ADB_PATH):
        cli_colors.print_error("adb.exe not found in Utils/Platform_Tools.")
        log_manager.log_error("adb.exe is missing. Cannot scan for devices.")
        return []

    try:
        result = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True, check=True)
        serials = _parse_serials(result.stdout.strip().splitlines())

        devices = []
        for serial in serials:
            props = _get_device_props(serial)
            devices.append({
                "serial": serial,
                "brand": props["brand"],
                "model": props["model"],
                "android": props["android"],
                "abi": props["abi"]
            })

        return devices

    except subprocess.CalledProcessError:
        cli_colors.print_error("ADB failed. Is the device authorized and USB debugging enabled?")
        log_manager.log_exception("ADB devices command failed.")
        return []
    except Exception as e:
        cli_colors.print_error("Unexpected error occurred during device scan.")
        log_manager.log_exception(str(e))
        return []

# ─────────────────────────────────────────────────────
# Helper: Extract Serial Numbers from ADB Output
# ─────────────────────────────────────────────────────

def _parse_serials(lines: list[str]) -> list[str]:
    return [
        line.split()[0]
        for line in lines[1:]  # skip header
        if line.strip() and "device" in line
    ]

# ─────────────────────────────────────────────────────
# Helper: Retrieve Device Properties via getprop
# ─────────────────────────────────────────────────────

def _get_device_props(serial: str) -> dict:
    def prop(key: str) -> str:
        try:
            result = subprocess.run([ADB_PATH, "-s", serial, "shell", "getprop", key],
                                    capture_output=True, text=True, timeout=3)
            return result.stdout.strip()
        except Exception:
            return "?"

    return {
        "brand": prop("ro.product.brand"),
        "model": prop("ro.product.model"),
        "android": prop("ro.build.version.release"),
        "abi": prop("ro.product.cpu.abi")
    }
