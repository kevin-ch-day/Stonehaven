# app_config.py
# Global Application Configuration

# ─────────────────────────────────────────────────────
# Basic Application Metadata
# ─────────────────────────────────────────────────────
import os
import platform
APP_NAME = "Stonehaven"
VERSION = "0.0.1"
LICENSE = "MIT"

# ─────────────────────────────────────────────────────
# Project Repository and Documentation
# ─────────────────────────────────────────────────────
REPOSITORY = "https://github.com/kevin-ch-day/Stonehaven"
DOCUMENTATION = REPOSITORY + "/wiki"

# ─────────────────────────────────────────────────────
# Banner Text (Displayed on Launch)
# ─────────────────────────────────────────────────────
BANNER = f"{APP_NAME} - Android Security Toolkit (v{VERSION})"

# ─────────────────────────────────────────────────────
# Paths (if needed in future)
# ─────────────────────────────────────────────────────
DEFAULT_INPUT_DIR = "Input"
DEFAULT_OUTPUT_DIR = "Output"
DEFAULT_TOOL_DIR = "Utils\\Platform_Tools"

# ADB executable path. Can be overridden with the STONEHAVEN_ADB_PATH
# environment variable. Defaults to the bundled platform-tools on
# Windows or the system "adb" for other platforms.

ADB_PATH = os.environ.get(
    "STONEHAVEN_ADB_PATH",
    os.path.join("Utils", "Platform_Tools", "adb.exe")
    if platform.system() == "Windows"
    else "adb",
)

# ─────────────────────────────────────────────────────
# Debug Settings
# ─────────────────────────────────────────────────────
DEBUG_MODE = False  # Can be overridden in runtime
