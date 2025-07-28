import os
import xml.etree.ElementTree as ET
from collections import Counter
from Utils.logging_utils import log_manager

# ----------------------------------------------------------------------
# Permission Extraction and Classification
# ----------------------------------------------------------------------

# Reference lists of common Android permissions. This is not exhaustive but
# provides basic classification for research prototypes.
DANGEROUS_PERMISSIONS = {
    "android.permission.READ_CALENDAR",
    "android.permission.WRITE_CALENDAR",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_PHONE_STATE",
    "android.permission.CALL_PHONE",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "android.permission.ADD_VOICEMAIL",
    "android.permission.USE_SIP",
    "android.permission.PROCESS_OUTGOING_CALLS",
    "android.permission.BODY_SENSORS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_SMS",
    "android.permission.RECEIVE_WAP_PUSH",
    "android.permission.RECEIVE_MMS",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
}

NORMAL_PERMISSIONS = {
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.WAKE_LOCK",
    "android.permission.ACCESS_WIFI_STATE",
    "android.permission.CHANGE_WIFI_STATE",
    "android.permission.REQUEST_INSTALL_PACKAGES",
}

SIGNATURE_PERMISSIONS = {
    "android.permission.ACCESS_CACHE_FILESYSTEM",
}


def extract_permissions(manifest_path: str) -> list[str]:
    """Parse an AndroidManifest.xml file and extract all permission names."""
    perms: list[str] = []
    if not os.path.isfile(manifest_path):
        return perms
    try:
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        for elem in root.findall("uses-permission"):
            name = elem.get("{http://schemas.android.com/apk/res/android}name")
            if name:
                perms.append(name)
    except Exception as e:
        log_manager.log_exception(f"Failed to parse permissions from {manifest_path}: {e}")
    return perms


def classify_permission(name: str) -> str:
    """Return the classification type for a permission."""
    if name in DANGEROUS_PERMISSIONS:
        return "dangerous"
    if name in NORMAL_PERMISSIONS:
        return "normal"
    if name in SIGNATURE_PERMISSIONS:
        return "signature"
    if name.startswith("android.permission"):
        return "unknown"
    return "custom"


def classify_permissions(perms: list[str]) -> dict[str, str]:
    return {p: classify_permission(p) for p in perms}


# ----------------------------------------------------------------------
# Permission Frequency Analysis
# ----------------------------------------------------------------------

def build_permission_frequency(directory: str) -> Counter:
    """Walk a directory of decompiled APKs and count permission occurrences."""
    counts: Counter = Counter()
    for root_dir, _dirs, files in os.walk(directory):
        if "AndroidManifest.xml" in files:
            manifest = os.path.join(root_dir, "AndroidManifest.xml")
            perms = extract_permissions(manifest)
            counts.update(perms)
    return counts


def identify_outliers(counts: Counter, threshold: int = 1) -> list[str]:
    """Return permissions that appear less than or equal to threshold times."""
    return [perm for perm, c in counts.items() if c <= threshold]


# ----------------------------------------------------------------------
# Context-Aware Risk Scoring
# ----------------------------------------------------------------------

TYPE_SCORE = {
    "dangerous": 7,
    "signature": 6,
    "normal": 2,
    "custom": 5,
    "unknown": 3,
}


def permission_risk_score(
    name: str, freq: int, app_category: str = "generic"
) -> float:
    """Assign a simple risk score based on type and rarity."""
    ptype = classify_permission(name)
    base = TYPE_SCORE.get(ptype, 3)
    rarity = 5 if freq <= 1 else 0
    category_bonus = 1 if (
        app_category in {"messaging", "media"} and ptype == "dangerous"
    ) else 0
    score = base + rarity + category_bonus
    return min(score, 10)


def count_dangerous_permissions(perms: list[str]) -> int:
    """Return the number of permissions classified as dangerous."""
    return sum(1 for p in perms if classify_permission(p) == "dangerous")


def detect_dangerous_combinations(perms: list[str]) -> list[str]:
    """Identify suspicious permission combinations that may indicate abuse."""
    perm_set = set(perms)
    combos = []
    if {"android.permission.SEND_SMS", "android.permission.READ_SMS"} <= perm_set:
        combos.append("SMS read/send")
    if {
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.READ_CONTACTS",
    } <= perm_set:
        combos.append("Location + Contacts")
    if {"android.permission.CAMERA", "android.permission.RECORD_AUDIO"} <= perm_set:
        combos.append("Camera + Microphone")
    return combos
