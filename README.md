# Stonehaven Android Security Toolkit

Stonehaven is a command-line suite for inspecting Android devices and APK files. It provides device interrogation via ADB and extensible modules for static application analysis and forensic research.

## Features

- Detect and list connected Android devices
- Collect detailed device metadata (OS version, security posture, networking info)
- Capture advanced network metrics (gateway, DNS servers, connection type)
- Display device summaries in a readable table format
- Human-readable storage size formatting
- Static APK permission extraction and risk scoring
- Detection of excessive or suspicious permission combinations
- Security misconfiguration detection (API keys, cleartext traffic, storage)
- Fast SHA-256 hashing of APK files for integrity checks
- CVSS-scored static scans of decompiled APK directories
- CVSS v3.0 scoring utilities for reported issues
- Export scan reports to Markdown and CSV
- Structured logging with colorized console output
- Easy function tracing via `log_manager.log_call` decorator
- Runtime log level adjustments via `log_manager.set_log_level`
- Toggle console logging with `log_manager.enable_console_logging`

## Requirements

- Python 3.10+
- [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools) (ADB) available in your `PATH` or under `Utils/Platform_Tools`
- Optionally set `STONEHAVEN_ADB_PATH` to specify a custom ADB executable
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
4. Compute an APK hash:
   ```bash
   python -c "from App_Analysis.apk_hashing import calculate_apk_hash; print(calculate_apk_hash('myapp.apk'))"
   ```
   The digest can be stored alongside your build or manifest version
   number to quickly detect unexpected changes in future releases.


## Project Layout

```
App_Analysis/      # APK static analysis modules
Database/          # Future database support
Device_Analysis/   # Core device interaction modules
Utils/             # CLI and security utilities
Wiki/              # Additional text documentation
```

## Roadmap

Stonehaven is an academic prototype. Planned improvements include:

- Dynamic device traffic inspection
- Database integration for result storage
- Expanded network and forensic collection
- CI-ready test suite and packaging

Contributions and research collaborations are welcome.
