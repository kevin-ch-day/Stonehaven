"""Minimal CVSS v3.0 base score calculator."""
from __future__ import annotations

import math

# Metric weight mappings based on the official specification
AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}
AC = {"L": 0.77, "H": 0.44}
UI = {"N": 0.85, "R": 0.62}
SCORES_CIA = {"H": 0.56, "L": 0.22, "N": 0.0}

PR_U = {"N": 0.85, "L": 0.62, "H": 0.27}
PR_C = {"N": 0.85, "L": 0.68, "H": 0.5}

SEVERITY_RANGES = [
    (0.0, 0.0, "None"),
    (0.1, 3.9, "Low"),
    (4.0, 6.9, "Medium"),
    (7.0, 8.9, "High"),
    (9.0, 10.0, "Critical"),
]


def _round_up(value: float) -> float:
    return math.ceil(value * 10) / 10.0


def parse_vector(vector: str) -> dict[str, str]:
    parts = vector.split("/")
    metrics = {}
    for part in parts:
        if not part:
            continue
        key, val = part.split(":")
        metrics[key] = val
    return metrics


def calculate_base_score(vector: str) -> tuple[float, str]:
    m = parse_vector(vector)
    scope = m.get("S", "U")
    av = AV[m.get("AV", "N")]
    ac = AC[m.get("AC", "L")]
    pr = (PR_C if scope == "C" else PR_U)[m.get("PR", "N")]
    ui = UI[m.get("UI", "N")]
    c = SCORES_CIA[m.get("C", "N")]
    i = SCORES_CIA[m.get("I", "N")]
    a = SCORES_CIA[m.get("A", "N")]

    iss = 1 - (1 - c) * (1 - i) * (1 - a)
    if scope == "U":
        impact = 6.42 * iss
    else:
        impact = 7.52 * (iss - 0.029) - 3.25 * pow(iss - 0.02, 15)

    exploit = 8.22 * av * ac * pr * ui

    if impact <= 0:
        score = 0.0
    else:
        if scope == "U":
            score = _round_up(min(impact + exploit, 10))
        else:
            score = _round_up(min(1.08 * (impact + exploit), 10))

    for low, high, label in SEVERITY_RANGES:
        if low <= score <= high:
            return score, label
    return score, "None"

