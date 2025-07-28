# device_inspector_network.py
# Extracts network-related metadata from a connected Android device via ADB

from Device_Analysis import device_inspector_core as core

def get_ip_address(serial: str) -> str:
    """
    Extract the device's IP address from the routing table.

    Args:
        serial (str): Device serial number.

    Returns:
        str: IP address or 'Unknown'
    """
    output = core.adb_shell(serial, "ip route")
    try:
        return output.split()[8]
    except Exception:
        return "Unknown"

def get_mac_address(serial: str) -> str:
    """
    Extract the device's MAC address from Wi-Fi interface.

    Args:
        serial (str): Device serial number.

    Returns:
        str: MAC address or 'Unknown'
    """
    output = core.adb_shell(serial, "cat /sys/class/net/wlan0/address")
    return output if output and ":" in output else "Unknown"

def get_wifi_ssid(serial: str) -> str:
    """
    Extract the Wi-Fi SSID using dumpsys netstats or other fallback.

    Args:
        serial (str): Device serial number.

    Returns:
        str: SSID name or 'Unknown'
    """
    output = core.adb_shell(serial, "dumpsys netstats | grep -m 1 'iface=wlan0'")
    return output if output else "Unknown"

def get_mobile_data_status(serial: str) -> str:
    """
    Determine if mobile data is currently enabled on the device.

    Args:
        serial (str): Device serial number.

    Returns:
        str: 'Enabled' or 'Disabled'
    """
    output = core.adb_shell(serial, "dumpsys telephony.registry | grep mDataConnectionState")
    return "Enabled" if "mDataConnectionState=2" in output else "Disabled"

def get_wifi_status(serial: str) -> str:
    """
    Check whether Wi-Fi is currently enabled and connected.

    Args:
        serial (str): Device serial number.

    Returns:
        str: Wi-Fi status string.
    """
    state = core.adb_shell(serial, "dumpsys wifi | grep 'Wi-Fi is '")
    return state if state else "Unknown"

def get_signal_strength(serial: str) -> str:
    """
    Retrieve the current signal strength (mobile network).

    Args:
        serial (str): Device serial number.

    Returns:
        str: Signal strength info or 'Unknown'
    """
    output = core.adb_shell(serial, "dumpsys telephony.registry | grep mSignalStrength")
    return output if output else "Unknown"
