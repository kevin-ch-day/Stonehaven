# Stonehaven Android Security Toolkit

Stonehaven is a command-line suite for inspecting Android devices and APK files. It provides basic device interrogation via ADB and modular helpers for future static application analysis.

## Features

- Detect and list connected Android devices
- Collect detailed device metadata (OS version, security posture, networking info)
- Display device summaries in a readable table format
- Structured logging with optional console output

## Requirements

- Python 3.10+
- [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools) (ADB) available in your `PATH` or under `Utils/Platform_Tools`
- `colorama` Python package (installed via `requirements.txt`)

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main launcher:
   ```bash
   python main.py
   ```
3. Use the menu to scan for devices or connect to a device for a detailed summary.

## Project Layout

```
App_Analysis/      # Placeholder modules for APK scanning
Database/          # Future database support
Device_Analysis/   # Core device interaction modules
Utils/             # CLI helpers and logging utilities
Wiki/              # Additional text documentation
```

## Roadmap

Stonehaven is an academic prototype. Planned improvements include:

- Static APK permission analysis and hashing
- Database integration for result storage
- Expanded network and forensic collection
- CI-ready test suite and packaging

Contributions and research collaborations are welcome.
