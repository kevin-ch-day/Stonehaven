# device_data_collector.py
# Aggregates and enriches Android device metadata for analysis and summary display

from Device_Analysis import (
    device_inspector_core as core,
    device_inspector_security as sec,
    device_inspector_network as net,
)
from Utils.logging_utils import log_manager

def collect_full_device_info(base_device: dict) -> dict:
    """
    Enriches the base metadata of an Android device with advanced runtime,
    system, security, and network information.

    Args:
        base_device (dict): Dictionary with minimal device info (serial, model, brand, etc.)

    Returns:
        dict: Fully enriched device info dictionary for analysis and reporting.
    """
    serial = base_device.get("serial", "")
    device = base_device.copy()

    # ─────────────────────────────────────────────
    # OS & Build Info (Core)
    # ─────────────────────────────────────────────
    _safe_set(device, {
        "api_level": core.get_api_level,
        "build_fingerprint": core.get_build_fingerprint,
        "device_name": core.get_device_name,
        "uptime": core.get_uptime,
        "adb_state": core.get_adb_state,
        "logcat": core.test_logcat_access,
        "timezone": core.get_timezone,
        "locale": core.get_locale,
    }, serial)

    # ─────────────────────────────────────────────
    # Security & Integrity Features
    # ─────────────────────────────────────────────
    _safe_set(device, {
        "shell_access": sec.test_shell_access,
        "root_status": sec.check_root_status,
        "usb_debug": sec.get_usb_debug_status,
        "developer_mode": sec.is_developer_mode_enabled,
        "play_protect": sec.check_play_protect,
        "custom_rom": sec.detect_custom_rom,
        "selinux": sec.get_selinux_status,
        "bootloader": sec.is_bootloader_unlocked,
    }, serial)

    # ─────────────────────────────────────────────
    # Networking & Wireless
    # ─────────────────────────────────────────────
    _safe_set(device, {
        "ip_address": net.get_ip_address,
        "mac_address": net.get_mac_address,
        "wifi_status": net.get_wifi_status,
        "mobile_data": net.get_mobile_data_status,
        "wifi_ssid": net.get_wifi_ssid,
        "signal_strength": net.get_signal_strength,
    }, serial)

    # ─────────────────────────────────────────────
    # Installed Apps & Storage
    # ─────────────────────────────────────────────
    try:
        device["app_count"] = core.count_installed_apps(serial)
        device["antivirus_detected"] = sec.check_known_antivirus_apps(serial)

        storage = core.get_storage_info(serial)
        if isinstance(storage, dict):
            device["storage_mount"] = storage.get("mount", "Unknown")
            device["storage_used"] = storage.get("used", "Unknown")
            device["storage_free"] = storage.get("free", "Unknown")
        else:
            device["raw_storage_info"] = storage
    except Exception:
        device.update({
            "app_count": "N/A",
            "antivirus_detected": "Unknown",
            "storage_mount": "Unknown",
            "storage_used": "Unknown",
            "storage_free": "Unknown"
        })

    # ─────────────────────────────────────────────
    # Battery / Power
    # ─────────────────────────────────────────────
    try:
        battery = core.get_battery_status(serial)
        if isinstance(battery, dict):
            device["battery_level"] = battery.get("level", "Unknown")
            device["charging"] = battery.get("charging", "Unknown")
            device["battery_health"] = battery.get("health", "Unknown")
            device["battery_temp"] = battery.get("temp", "Unknown")
        else:
            device["raw_battery_info"] = battery
    except Exception:
        device.update({
            "battery_level": "Unknown",
            "charging": "Unknown",
            "battery_health": "Unknown",
            "battery_temp": "Unknown"
        })

    return device


def _safe_set(device: dict, function_map: dict, serial: str):
    """
    Utility to safely call inspection functions and store results.

    Args:
        device (dict): Device info to enrich
        function_map (dict): Keys = property names, values = function references
        serial (str): Device serial for ADB command targeting
    """
    for key, func in function_map.items():
        try:
            device[key] = func(serial)
        except Exception as e:
            device[key] = "Unknown"
            log_manager.log_exception(f"Failed to collect {key}: {e}")
