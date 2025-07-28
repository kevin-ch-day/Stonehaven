# log_config.py
# Centralized log configuration for Stonehaven logging engine

import os
from datetime import datetime

# ─────────────────────────────────────────────────────
# Log Directory & Naming
# ─────────────────────────────────────────────────────
LOG_DIR = "Logs"

# Date: MM-DD-YYYY | Time: HH:MM AM/PM
DATE_STAMP = datetime.now().strftime("%m-%d-%Y")
TIME_STAMP = datetime.now().strftime("%I-%M %p")

# Example: stonehaven_05-15-2025_12-45_PM.log
LOG_FILENAME = f"stonehaven_{DATE_STAMP}_{TIME_STAMP}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILENAME)

# ─────────────────────────────────────────────────────
# Logging Format
# ─────────────────────────────────────────────────────
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
DATE_FORMAT = "%m-%d-%Y %I:%M:%S %p"

# ─────────────────────────────────────────────────────
# Log Level
# Available: DEBUG, INFO, WARNING, ERROR, CRITICAL
# ─────────────────────────────────────────────────────
LOG_LEVEL = os.environ.get("STONEHAVEN_LOG_LEVEL", "DEBUG").upper()

# ─────────────────────────────────────────────────────
# Console Log Toggle
# Set to True if you want logs shown in console too
# ─────────────────────────────────────────────────────
LOG_TO_CONSOLE = True

# ─────────────────────────────────────────────────────
# Log File Rotation (Future Enhancement Support)
# ─────────────────────────────────────────────────────
MAX_LOG_SIZE_MB = 5           # Optional max size before rotation
BACKUP_COUNT = 3              # Number of rotated log files to keep
ENABLE_ROTATION = False       # Set to True if rotating log files is desired
