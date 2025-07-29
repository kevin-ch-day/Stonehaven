"""Utilities for computing APK hashes.

These helpers are primarily used to detect whether an APK file has
changed between versions. Calculating and comparing SHA-256 digests is
often easier than parsing version metadata from the manifest.
"""

from __future__ import annotations

import hashlib
import os
from typing import Dict

from Utils.logging_utils import log_manager


def _hash_file(path: str) -> str:
    """Return the SHA-256 hash for a single file."""
    if not os.path.isfile(path):
        log_manager.log_warning(f"File not found: {path}")
        return ""

    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        log_manager.log_exception(f"Failed to hash {path}: {e}")
        return ""


@log_manager.log_call("info")
def calculate_apk_hash(path: str) -> str:
    """Compute the SHA-256 hash of an APK file."""
    return _hash_file(path)


@log_manager.log_call("info")
def apk_changed(path: str, known_hash: str) -> bool:
    """Return ``True`` if the APK hash differs from ``known_hash``."""
    current = calculate_apk_hash(path)
    return current != known_hash


@log_manager.log_call("info")
def hash_apk_directory(directory: str) -> Dict[str, str]:
    """Recursively hash all APK files under ``directory``.

    The returned mapping can be stored to compare against future builds
    or to correlate hashes with specific manifest versions.
    """
    hashes: Dict[str, str] = {}
    for root_dir, _dirs, files in os.walk(directory):
        for name in files:
            if name.lower().endswith(".apk"):
                file_path = os.path.join(root_dir, name)
                hashes[file_path] = _hash_file(file_path)
    return hashes
