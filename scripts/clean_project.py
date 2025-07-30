# clean_project.py
# Purpose: Clean up .pyc, .log, .tmp, and other temp files in the Stonehaven project

import os
import fnmatch
import sys

# ─────────────────────────────────────────────
# Path Configuration
# ─────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
LOG_DIR = os.path.join(PROJECT_ROOT, "Logs")
VERBOSE = "--verbose" in sys.argv

# ─────────────────────────────────────────────
# File Patterns and Labels
# ─────────────────────────────────────────────
CLEANUP_TARGETS = {
    "*.pyc": "Python bytecode file",
    "*.log": "Log file",
    "*.tmp": "Temporary file",
    "*.bak": "Backup file",
    ".DS_Store": "macOS metadata file"
}

# ─────────────────────────────────────────────
# Logging Function (ASCII-safe)
# ─────────────────────────────────────────────
def log_action(message: str, level: str = "INFO"):
    """Print cleanup actions based on verbosity and log level."""
    level = level.upper()
    prefix = {
        "INFO": "[OK] ",
        "WARN": "[!] ",
        "ERROR": "[ERR]"
    }.get(level, "[   ]")
    if VERBOSE or level != "INFO":
        print(f"{prefix} {message}")

# ─────────────────────────────────────────────
# File Deletion Logic
# ─────────────────────────────────────────────
def delete_files_by_pattern(root_dir: str, pattern: str, description: str) -> int:
    count = 0
    for root, _, files in os.walk(root_dir):
        matched = fnmatch.filter(files, pattern)
        if not matched and not VERBOSE:
            continue
        for filename in matched:
            try:
                file_path = os.path.join(root, filename)
                os.remove(file_path)
                log_action(f"Deleted {description}: {file_path}")
                count += 1
            except Exception as e:
                log_action(f"Failed to delete {file_path}: {e}", "ERROR")
    return count

# ─────────────────────────────────────────────
# Remove __pycache__ Directories
# ─────────────────────────────────────────────
def delete_pycache_dirs(root_dir: str) -> int:
    removed_dirs = 0
    for root, dirs, _ in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                try:
                    for f in os.listdir(dir_path):
                        os.remove(os.path.join(dir_path, f))
                    os.rmdir(dir_path)
                    log_action(f"Removed folder: {dir_path}")
                    removed_dirs += 1
                except Exception as e:
                    log_action(f"Failed to remove {dir_path}: {e}", "ERROR")
    return removed_dirs

# ─────────────────────────────────────────────
# Output Formatting
# ─────────────────────────────────────────────
def print_header():
    print("=" * 60)
    print("             Stonehaven Project Cleanup Utility")
    print("=" * 60)
    print(f" Target Root   : {PROJECT_ROOT}")
    print(f" Verbose Mode  : {'ON' if VERBOSE else 'OFF'}")
    print("-" * 60)

def print_summary(file_counts: dict, pycache_count: int):
    print("\n Cleanup Results:")
    print(" " + "-" * 59)
    print(" | {0:<20} | {1:<22} | {2:>7} |".format("File Type", "Description", "Removed"))
    print(" " + "-" * 59)
    for pattern, count in file_counts.items():
        desc = CLEANUP_TARGETS.get(pattern, "Unknown")
        print(" | {0:<20} | {1:<22} | {2:>7} |".format(pattern, desc, count))
    print(" " + "-" * 59)
    print(" | {0:<43} | {1:>7} |".format("__pycache__ folders", pycache_count))
    print(" " + "-" * 59)

# ─────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────
def main() -> int:
    print_header()
    removed_counts = {}

    for pattern, description in CLEANUP_TARGETS.items():
        target_dir = LOG_DIR if pattern.endswith(".log") else PROJECT_ROOT
        count = delete_files_by_pattern(target_dir, pattern, description)
        removed_counts[pattern] = count

    pycache_dirs = delete_pycache_dirs(PROJECT_ROOT)
    print_summary(removed_counts, pycache_dirs)

    total_removed = sum(removed_counts.values()) + pycache_dirs
    return 0 if total_removed > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
