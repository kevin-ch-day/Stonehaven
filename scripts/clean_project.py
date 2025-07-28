# clean_project.py
# Purpose: Clean up .pyc and .log files in the Stonehaven project

import os
import fnmatch
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, os.pardir))
LOG_DIR = os.path.join(PROJECT_ROOT, "Logs")

VERBOSE = "--verbose" in sys.argv

def log_action(message, level="INFO"):
    prefix = {
        "INFO": "[OK] ",
        "ERROR": "[ERR]",
        "WARN": "[WARN]"
    }.get(level, "[INFO]")
    print(f"{prefix} {message}")

def delete_files_by_pattern(root_dir, pattern, description):
    count = 0
    for root, _, files in os.walk(root_dir):
        matched_files = sorted(fnmatch.filter(files, pattern))
        if not matched_files and not VERBOSE:
            continue
        for filename in matched_files:
            file_path = os.path.join(root, filename)
            try:
                os.remove(file_path)
                log_action(f"Deleted {description}: {file_path}", "INFO")
                count += 1
            except Exception as e:
                log_action(f"Failed to delete {file_path}: {str(e)}", "ERROR")
    return count

def delete_pycache_dirs(root_dir):
    removed_dirs = 0
    for root, dirs, _ in os.walk(root_dir):
        for dir_name in sorted(dirs):
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                try:
                    for f in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, f)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(dir_path)
                    log_action(f"Removed directory: {dir_path}", "INFO")
                    removed_dirs += 1
                except Exception as e:
                    log_action(f"Failed to remove {dir_path}: {str(e)}", "ERROR")
    return removed_dirs

def print_header():
    print("-" * 60)
    print(" Stonehaven Project Cleanup Utility")
    print("-" * 60)
    print(" Target Root :", PROJECT_ROOT)
    print(" Verbose Mode:", "ON" if VERBOSE else "OFF")
    print("-" * 60)
    print("")

def print_summary(pyc_count, log_count, pycache_dirs):
    print("\n" + "-" * 60)
    print(" Cleanup Summary:")
    print(f"   - .pyc files removed         : {pyc_count}")
    print(f"   - Log files removed          : {log_count}")
    print(f"   - __pycache__ folders removed: {pycache_dirs}")
    print("-" * 60)

def main():
    print_header()
    pyc_count = delete_files_by_pattern(PROJECT_ROOT, "*.pyc", ".pyc file")
    log_count = delete_files_by_pattern(LOG_DIR, "*.log", ".log file")
    pycache_dirs = delete_pycache_dirs(PROJECT_ROOT)
    print_summary(pyc_count, log_count, pycache_dirs)
    return 0 if (pyc_count + log_count + pycache_dirs) > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
