# device_inspector_core.py
# Provides core ADB command execution and essential device information access

import subprocess
import os
import platform

# ─────────────────────────────────────────────
# ADB CONFIGURATION (Cross-Platform)
# ─────────────────────────────────────────────
ADB_PATH = os.path.join("Utils", "Platform_Tools", "adb.exe") if platform.system() == "Windows" else "adb"
DEFAULT_VALUE = "Unknown"

# ─────────────────────────────────────────────
# UTILITY: Execute ADB shell command
# ─────────────────────────────────────────────
def adb_shell(serial: str, command: str) -> str:
    """
    Execute an ADB shell command on the specified device.

    Args:
        serial (str): Device serial number.
        command (str): ADB shell command to run.

    Returns:
        str: Output of the command or DEFAULT_VALUE on failure.
    """
    try:
        result = subprocess.run(
            [ADB_PATH, "-s", serial, "shell", command],
            capture_output=True,
            text=True,
            timeout=6
        )
        return result.stdout.strip() if result.returncode == 0 else DEFAULT_VALUE
    except subprocess.TimeoutExpired:
        return "Timeout"
    except Exception:
        return DEFAULT_VALUE

# ─────────────────────────────────────────────
# CORE DEVICE INFORMATION
# ─────────────────────────────────────────────
def get_adb_state(serial: str) -> str:
    try:
        result = subprocess.run(
            [ADB_PATH, "-s", serial, "get-state"],
            capture_output=True,
            text=True,
            timeout=4
        )
        return result.stdout.strip() or DEFAULT_VALUE
    except Exception:
        return DEFAULT_VALUE

def get_device_name(serial: str) -> str:
    return adb_shell(serial, "getprop ro.product.device")

def get_api_level(serial: str) -> str:
    return adb_shell(serial, "getprop ro.build.version.sdk")

def get_build_fingerprint(serial: str) -> str:
    return adb_shell(serial, "getprop ro.build.fingerprint")

def get_uptime(serial: str) -> str:
    output = adb_shell(serial, "cat /proc/uptime")
    try:
        seconds = float(output.split()[0])
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02} (hh:mm:ss)"
    except (ValueError, IndexError):
        return DEFAULT_VALUE

# ─────────────────────────────────────────────
# SYSTEM LOCALE & DEBUGGING
# ─────────────────────────────────────────────
def get_timezone(serial: str) -> str:
    return adb_shell(serial, "getprop persist.sys.timezone")

def get_locale(serial: str) -> str:
    locale = adb_shell(serial, "getprop persist.sys.locale")
    return locale if locale != DEFAULT_VALUE else adb_shell(serial, "getprop ro.product.locale")

def test_logcat_access(serial: str) -> str:
    output = adb_shell(serial, "logcat -d -t 1")
    if "--------- beginning of" in output or len(output.strip()) > 0:
        return "Available"
    return "Unavailable"

# ─────────────────────────────────────────────
# BATTERY / POWER STATUS
# ─────────────────────────────────────────────
def get_battery_status(serial: str) -> dict:
    output = adb_shell(serial, "dumpsys battery")
    try:
        return {
            "level": _parse_dumpsys(output, "level"),
            "charging": _parse_dumpsys(output, "AC powered") == "true",
            "health": _parse_dumpsys(output, "health"),
            "temp": f"{int(_parse_dumpsys(output, 'temperature')) / 10.0:.1f} °C"
        }
    except Exception:
        return {
            "level": DEFAULT_VALUE,
            "charging": DEFAULT_VALUE,
            "health": DEFAULT_VALUE,
            "temp": DEFAULT_VALUE
        }

def _parse_dumpsys(output: str, key: str) -> str:
    for line in output.splitlines():
        if key in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return DEFAULT_VALUE

# ─────────────────────────────────────────────
# STORAGE INFORMATION
# ─────────────────────────────────────────────
def get_storage_info(serial: str) -> dict:
    output = adb_shell(serial, "df /data")
    try:
        lines = output.strip().splitlines()
        if len(lines) >= 2:
            values = lines[1].split()
            return {
                "mount": values[0] if len(values) > 0 else DEFAULT_VALUE,
                "used": values[2] if len(values) > 2 else DEFAULT_VALUE,
                "free": values[3] if len(values) > 3 else DEFAULT_VALUE
            }
        return {"mount": DEFAULT_VALUE, "used": DEFAULT_VALUE, "free": DEFAULT_VALUE}
    except Exception:
        return {"mount": DEFAULT_VALUE, "used": DEFAULT_VALUE, "free": DEFAULT_VALUE}

# ─────────────────────────────────────────────
# INSTALLED APPLICATIONS
# ─────────────────────────────────────────────
def count_installed_apps(serial: str) -> int:
    """
    Count the total number of installed packages on the device.

    Args:
        serial (str): Device serial number.

    Returns:
        int: Number of installed packages, or -1 if error occurs.
    """
    output = adb_shell(serial, "pm list packages")
    if output == DEFAULT_VALUE:
        return -1
    try:
        return len(output.splitlines())
    except Exception:
        return -1
