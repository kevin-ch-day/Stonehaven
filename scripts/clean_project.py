# clean_project.py
# Purpose: Clean up .pyc, .log, and temp files in the Stonehaven project

import os
import fnmatch
import sys
from Utils.logging_utils import log_manager

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
LOG_DIR = os.path.join(PROJECT_ROOT, "Logs")

VERBOSE = "--verbose" in sys.argv

# File patterns to target
CLEANUP_TARGETS = {
    "*.pyc": "Python bytecode file",
    "*.log": "Log file",
    "*.tmp": "Temporary file",
    "*.bak": "Backup file",
    ".DS_Store": "macOS metadata file"
}

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
def log_action(message: str, level: str = "INFO"):
    """Log and optionally display cleanup actions."""
    level = level.upper()
    log_fn = {
        "INFO": log_manager.log_info,
        "WARN": log_manager.log_warning,
        "ERROR": log_manager.log_error,
    }.get(level, log_manager.log_info)
    log_fn(message)
    if VERBOSE:
        prefix = {
            "INFO": "[✔]",
            "WARN": "[!]",
            "ERROR": "[✖]",
        }.get(level, "[ ]")
        print(f"{prefix} {message}")

# ─────────────────────────────────────────────
# FILE CLEANING
# ─────────────────────────────────────────────
def delete_files_by_pattern(root_dir: str, pattern: str, description: str) -> int:
    count = 0
    for root, _, files in os.walk(root_dir):
        matched_files = fnmatch.filter(files, pattern)
        if not matched_files and not VERBOSE:
            continue
        for filename in matched_files:
            file_path = os.path.join(root, filename)
            try:
                os.remove(file_path)
                log_action(f"Deleted {description}: {file_path}")
                count += 1
            except Exception as e:
                log_action(f"Failed to delete {file_path}: {e}", "ERROR")
    return count

# ─────────────────────────────────────────────
# DIRECTORY CLEANING
# ─────────────────────────────────────────────
def delete_pycache_dirs(root_dir: str) -> int:
    removed_dirs = 0
    for root, dirs, _ in os.walk(root_dir):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                try:
                    for file in os.listdir(dir_path):
                        os.remove(os.path.join(dir_path, file))
                    os.rmdir(dir_path)
                    log_action(f"Removed directory: {dir_path}")
                    removed_dirs += 1
                except Exception as e:
                    log_action(f"Failed to remove {dir_path}: {e}", "ERROR")
    return removed_dirs

# ─────────────────────────────────────────────
# OUTPUT & EXECUTION
# ─────────────────────────────────────────────
def print_header():
    print("=" * 60)
    print(" 🧹 Stonehaven Project Cleanup Utility")
    print("=" * 60)
    print(f" Target Root  : {PROJECT_ROOT}")
    print(f" Verbose Mode : {'ON' if VERBOSE else 'OFF'}")
    print("-" * 60)

def print_summary(counts: dict, pycache_dirs: int):
    print("\n" + "-" * 60)
    print(" Cleanup Summary:")
    for pattern, count in counts.items():
        print(f"   - {pattern:<10} removed : {count}")
    print(f"   - __pycache__ folders   : {pycache_dirs}")
    print("-" * 60)

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
