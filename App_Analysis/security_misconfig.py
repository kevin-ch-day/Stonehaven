import os
import re
from typing import Generator
from Utils.logging_utils import log_manager

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _iter_source_files(directory: str) -> Generator[str, None, None]:
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            if fname.endswith(
                ('.java', '.kt', '.xml', '.smali', '.txt', '.gradle')
            ):
                yield os.path.join(root, fname)


def _read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        log_manager.log_exception(f"Failed to read {path}: {e}")
        return ""


# ----------------------------------------------------------------------
# Detection Routines
# ----------------------------------------------------------------------

API_KEY_REGEX = re.compile(
    r"(?i)(api[_-]?key|secret|token)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9-_]{16,})"
)
HTTP_REGEX = re.compile(r"http://")
WEAK_ENCRYPT_REGEX = re.compile(
    r"(MD5|SHA1|DES|RC2|RC4|BASE64)", re.IGNORECASE
)


def detect_api_keys(directory: str) -> list[str]:
    findings: list[str] = []
    for path in _iter_source_files(directory):
        text = _read_file(path)
        if API_KEY_REGEX.search(text):
            findings.append(path)
    return findings


def detect_cleartext_traffic(manifest_path: str, directory: str) -> bool:
    try:
        with open(manifest_path, 'r', encoding='utf-8', errors='ignore') as f:
            manifest = f.read()
            if 'usesCleartextTraffic="true"' in manifest:
                return True
    except Exception as e:
        log_manager.log_exception(
            f"Failed to read manifest for cleartext check: {e}"
        )

    for path in _iter_source_files(directory):
        if HTTP_REGEX.search(_read_file(path)):
            return True
    return False


def detect_insecure_storage(directory: str) -> list[str]:
    patterns = [r"SharedPreferences", r"MODE_WORLD_READABLE", r"openDatabase"]
    regex = re.compile('|'.join(patterns))
    findings: list[str] = []
    for path in _iter_source_files(directory):
        if regex.search(_read_file(path)):
            findings.append(path)
    return findings


def detect_weak_encryption(directory: str) -> list[str]:
    findings: list[str] = []
    for path in _iter_source_files(directory):
        if WEAK_ENCRYPT_REGEX.search(_read_file(path)):
            findings.append(path)
    return findings
