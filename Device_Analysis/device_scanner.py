# device_scanner.py
# Core logic for scanning Android devices via ADB and extracting properties

import subprocess
import shutil
from Utils.logging_utils import log_manager
from Utils.app_utils.app_config import ADB_PATH
from Device_Analysis import device_inspector_core as core


# ─────────────────────────────────────────────────────
# DeviceScanner Class
# ─────────────────────────────────────────────────────


class DeviceScanner:
    """Scan connected Android devices via ADB."""

    def __init__(self, adb_path: str = ADB_PATH):
        self.adb_path = adb_path

    @log_manager.log_call("info")
    def scan(self) -> list[dict]:
        """Return a list of detected Android devices with basic properties."""
        if not shutil.which(self.adb_path):
            log_manager.log_error("ADB executable missing or not in PATH.")
            return []

        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                log_manager.log_error("ADB returned failure code.")
                return []

            serials = self._parse_serials(result.stdout.strip().splitlines())
            if not serials:
                log_manager.log_info("No active ADB devices found.")
                return []

            devices = []
            for serial in serials:
                props = self._get_device_props(serial)
                devices.append(
                    {
                        "serial": serial,
                        "brand": props.get("brand", "?"),
                        "model": props.get("model", "?"),
                        "android": props.get("android", "?"),
                        "abi": props.get("abi", "?"),
                    }
                )

            log_manager.log_info(
                f"{len(devices)} device(s) successfully scanned."
            )
            return devices

        except subprocess.TimeoutExpired:
            log_manager.log_exception("ADB timeout during device scan.")
            return []
        except Exception as e:
            log_manager.log_exception(f"Device scan exception: {e}")
            return []

    # ─────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────

    def _parse_serials(self, lines: list[str]) -> list[str]:
        """Parse output from ``adb devices`` and return online serial numbers."""
        serials = []
        for line in lines[1:]:  # Skip first line ("List of devices attached")
            parts = line.strip().split()
            if len(parts) == 2 and parts[1] == "device":
                serials.append(parts[0])
            elif len(parts) == 2 and parts[1] != "device":
                log_manager.log_warning(
                    f"Skipping device with state '{parts[1]}': {parts[0]}"
                )
        return serials

    def _get_device_props(self, serial: str) -> dict:
        """Retrieve basic device properties via ``adb getprop``."""
        return {
            "brand": core.adb_shell(serial, "getprop ro.product.brand"),
            "model": core.adb_shell(serial, "getprop ro.product.model"),
            "android": core.adb_shell(serial, "getprop ro.build.version.release"),
            "abi": core.adb_shell(serial, "getprop ro.product.cpu.abi"),
        }


def get_connected_devices() -> list[dict]:
    """Backward compatible wrapper for legacy imports."""
    return DeviceScanner().scan()
