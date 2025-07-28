# device_inspector_security.py
# Extracts security, debugging, and integrity-related metadata from an Android device

from Device_Analysis import device_inspector_core as core


def check_root_status(serial: str) -> str:
    output = core.adb_shell(serial, "id")
    if not output or "Error" in output:
        return "Unknown"
    if "uid=0" in output:
        return "Rooted"
    return "User Access Only"


def test_shell_access(serial: str) -> str:
    """
    Attempts to test basic shell responsiveness.

    Returns:
        str: 'Available', 'Restricted', or 'Unknown'
    """
    output = core.adb_shell(serial, "echo shell_test")
    if not output or "Error" in output:
        return "Unknown"
    return "Available" if "shell_test" in output else "Restricted"


def get_usb_debug_status(serial: str) -> str:
    """
    Alias for is_usb_debug_enabled(), renamed for readability.
    """
    return is_usb_debug_enabled(serial)


def is_usb_debug_enabled(serial: str) -> str:
    val = core.adb_shell(serial, "settings get global adb_enabled")
    if not val or "Error" in val:
        return "Unknown"
    return "Enabled" if val.strip() == "1" else "Disabled"


def is_developer_mode_enabled(serial: str) -> str:
    val = core.adb_shell(serial, "settings get global development_settings_enabled")
    if not val or "Error" in val:
        return "Unknown"
    return "Enabled" if val.strip() == "1" else "Disabled"


def check_play_protect(serial: str) -> str:
    output = core.adb_shell(serial, "pm list packages")
    if not output or "Error" in output:
        return "Unknown"
    return "Enabled" if "com.google.android.gms" in output else "Disabled"


def detect_custom_rom(serial: str) -> str:
    fingerprint = core.adb_shell(serial, "getprop ro.build.fingerprint")
    if not fingerprint or "Error" in fingerprint:
        return "Unknown"
    if any(x in fingerprint.lower() for x in ["lineage", "twrp", "dirty"]):
        return "Yes"
    if "release-keys" in fingerprint:
        return "No"
    return "Unknown"


def is_bootloader_unlocked(serial: str) -> str:
    status = core.adb_shell(serial, "getprop ro.boot.verifiedbootstate")
    if not status or "Error" in status:
        return "Unknown"
    return status.capitalize()


def get_selinux_status(serial: str) -> str:
    result = core.adb_shell(serial, "getenforce")
    return result if result else "Unknown"


def check_known_antivirus_apps(serial: str) -> str:
    """
    Scan installed packages for known antivirus or security tools.

    Returns:
        str: Comma-separated string of detected antivirus apps or 'None'
    """
    known_av = [
        "com.avast.android.mobilesecurity",
        "com.avg.android",
        "com.bitdefender.antivirus",
        "com.kms.free",
        "com.kaspersky.qscanner",
        "com.lookout",
        "com.mcafee.android",
        "com.symantec.mobilesecurity",
        "com.trustgo.mobile.security",
        "com.eset.ems2.gp",
        "com.psafe.msuite"
    ]

    output = core.adb_shell(serial, "pm list packages")
    if not output or "Error" in output:
        return "Unknown"

    found = [pkg for pkg in known_av if pkg in output]
    return ", ".join(found) if found else "None"
