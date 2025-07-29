# device_inspector_network.py
# Extracts network-related metadata from a connected Android device via ADB

from Device_Analysis import device_inspector_core as core
import re

DEFAULT = core.DEFAULT_VALUE

def get_ip_address(serial: str) -> str:
    """Return the current Wi-Fi IPv4 address."""
    # Prefer ip addr which is available on modern Android builds
    output = core.adb_shell(serial, "ip addr show wlan0 | grep 'inet '")
    match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', output)
    if match:
        return match.group(1)

    # Fallback to routing table parsing
    route = core.adb_shell(serial, "ip route")
    match = re.search(r'src (\d+\.\d+\.\d+\.\d+)', route)
    return match.group(1) if match else "Unknown"

def get_mac_address(serial: str) -> str:
    """Return the Wi-Fi MAC address."""
    address = core.adb_shell(serial, "cat /sys/class/net/wlan0/address")
    if address and ":" in address:
        return address

    # Some devices restrict direct file access; try ip link as fallback
    alt = core.adb_shell(serial, "ip addr show wlan0 | grep 'link/ether'")
    match = re.search(r'link/ether\s+([0-9a-f:]{17})', alt)
    return match.group(1) if match else "Unknown"

def get_wifi_ssid(serial: str) -> str:
    """
    Extract the Wi-Fi SSID using dumpsys netstats or other fallback.

    Args:
        serial (str): Device serial number.

    Returns:
        str: SSID name or 'Unknown'
    """
    output = core.adb_shell(serial, "dumpsys netstats | grep -m 1 'iface=wlan0'")
    if not output:
        return "Unknown"
    # Attempt to extract just the SSID name from the complex dumpsys output
    match = re.search(r'wifiNetworkKey=\"([^\"]+)', output)
    if match:
        return match.group(1)
    return output.strip()

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
    if not state:
        return "Unknown"
    if "Wi-Fi is enabled" in state:
        return "Enabled"
    if "Wi-Fi is disabled" in state:
        return "Disabled"
    return state.strip()

def get_signal_strength(serial: str) -> str:
    """
    Retrieve the current signal strength (mobile network).

    Args:
        serial (str): Device serial number.

    Returns:
        str: Signal strength info or 'Unknown'
    """
    output = core.adb_shell(serial, "dumpsys telephony.registry | grep mSignalStrength")
    if not output:
        return "Unknown"

    # Typical output contains a large string with multiple metrics. Extract the
    # first RSSI value and level if present to present a concise summary.
    rssi = None
    level = None
    rssi_match = re.search(r'rssi=?(-?\d+)', output)
    if rssi_match:
        rssi = int(rssi_match.group(1))

    level_match = re.search(r'(?:mLevel|level)=(\d)', output)
    if level_match:
        level = int(level_match.group(1))

    parts = []
    if rssi is not None:
        parts.append(f"RSSI {rssi} dBm")
    if level is not None:
        parts.append(f"level {level}")

    return ", ".join(parts) if parts else output.strip()


def get_default_gateway(serial: str) -> str:
    """Return the default gateway IP address."""
    output = core.adb_shell(serial, "ip route")
    if not output:
        return "Unknown"
    for line in output.splitlines():
        if line.startswith("default"):
            parts = line.split()
            if "via" in parts:
                try:
                    return parts[parts.index("via") + 1]
                except Exception:
                    continue
    return "Unknown"


def get_dns_servers(serial: str) -> str:
    """Return configured DNS servers (comma separated)."""
    dns1 = core.adb_shell(serial, "getprop net.dns1")
    dns2 = core.adb_shell(serial, "getprop net.dns2")
    servers = [dns for dns in [dns1, dns2] if dns and dns != DEFAULT]
    # Remove duplicates while preserving order
    unique = []
    for s in servers:
        if s not in unique:
            unique.append(s)
    return ", ".join(unique) if unique else "Unknown"


def get_network_type(serial: str) -> str:
    """Return current mobile network type (e.g., LTE, NR)."""
    output = core.adb_shell(serial, "getprop gsm.network.type")
    if output and output != DEFAULT:
        return output.strip()
    alt = core.adb_shell(
        serial,
        "dumpsys telephony.registry | grep -m 1 dataNetworkType"
    )
    match = re.search(r'dataNetworkType=(\S+)', alt)
    return match.group(1) if match else "Unknown"


def get_wifi_link_speed(serial: str) -> str:
    """Return the connected Wi-Fi link speed if available."""
    output = core.adb_shell(serial, "dumpsys wifi | grep 'Link speed'")
    if not output:
        return "Unknown"
    match = re.search(r'Link speed:\s*(\d+)\s*Mbps', output)
    if match:
        return f"{match.group(1)} Mbps"
    return output.strip()
