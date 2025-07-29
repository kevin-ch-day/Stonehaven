# apk_scanner.py
# Orchestrates static analysis checks on a decompiled APK directory

import os
import csv
from Utils.logging_utils import log_manager
from Utils.app_utils import cli_colors, display_utils
from Utils.security_utils import cvss
from . import apk_permission_analysis as perm
from . import security_misconfig as misconfig

# ----------------------------------------------------------------------
# CVSS Vectors for Common Findings
# ----------------------------------------------------------------------
API_KEY_VECTOR = "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"
CLEARTEXT_VECTOR = "AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N"
INSECURE_STORAGE_VECTOR = "AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"
WEAK_CRYPTO_VECTOR = "AV:N/AC:H/PR:N/UI:N/S:U/C:M/I:N/A:N"
EXCESSIVE_PERMISSION_VECTOR = "AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N"


@log_manager.log_call("info")
def scan_directory(directory: str) -> dict:
    """Run all static checks on the specified APK folder."""
    report = {"findings": []}
    manifest = os.path.join(directory, "AndroidManifest.xml")

    # Permissions -----------------------------------------------------
    perms = perm.extract_permissions(manifest)
    report["permissions"] = perm.classify_permissions(perms)
    freq = perm.build_permission_frequency(directory)
    report["rare_permissions"] = perm.identify_outliers(freq)
    scores = {p: perm.permission_risk_score(p, freq.get(p, 0)) for p in perms}
    report["permission_scores"] = scores

    dangerous_count = perm.count_dangerous_permissions(perms)
    combos = perm.detect_dangerous_combinations(perms)
    if dangerous_count > 10 or combos:
        score, level = cvss.calculate_base_score(EXCESSIVE_PERMISSION_VECTOR)
        report["findings"].append(
            {
                "issue": "Excessive or risky permission usage",
                "vector": EXCESSIVE_PERMISSION_VECTOR,
                "score": score,
                "severity": level,
                "evidence": {"dangerous_count": dangerous_count, "combos": combos},
            }
        )

    # API Keys -------------------------------------------------------
    api_keys = misconfig.detect_api_keys(directory)
    if api_keys:
        score, level = cvss.calculate_base_score(API_KEY_VECTOR)
        report["findings"].append(
            {
                "issue": "API keys exposed",
                "vector": API_KEY_VECTOR,
                "score": score,
                "severity": level,
                "evidence": api_keys,
            }
        )

    # Cleartext Traffic ---------------------------------------------
    if misconfig.detect_cleartext_traffic(manifest, directory):
        score, level = cvss.calculate_base_score(CLEARTEXT_VECTOR)
        report["findings"].append(
            {
                "issue": "Cleartext traffic enabled",
                "vector": CLEARTEXT_VECTOR,
                "score": score,
                "severity": level,
            }
        )

    # Insecure Storage ----------------------------------------------
    storage = misconfig.detect_insecure_storage(directory)
    if storage:
        score, level = cvss.calculate_base_score(INSECURE_STORAGE_VECTOR)
        report["findings"].append(
            {
                "issue": "Insecure local storage",
                "vector": INSECURE_STORAGE_VECTOR,
                "score": score,
                "severity": level,
                "evidence": storage,
            }
        )

    # Weak Encryption ------------------------------------------------
    crypto = misconfig.detect_weak_encryption(directory)
    if crypto:
        score, level = cvss.calculate_base_score(WEAK_CRYPTO_VECTOR)
        report["findings"].append(
            {
                "issue": "Weak encryption algorithms",
                "vector": WEAK_CRYPTO_VECTOR,
                "score": score,
                "severity": level,
                "evidence": crypto,
            }
        )

    return report


def print_report(report: dict) -> None:
    """Pretty-print scan results to the console."""
    display_utils.print_section_title("APK Scan Report")
    cli_colors.print_info(f"Permissions found: {len(report.get('permissions', {}) )}")

    for perm_name, ptype in report.get("permissions", {}).items():
        score = report.get("permission_scores", {}).get(perm_name, 0)
        display_utils.print_key_value(
            perm_name,
            f"{ptype} (risk {score}/10)",
            color="white",
        )
    if report.get("rare_permissions"):
        cli_colors.print_warning("Rare permissions: " + ", ".join(report["rare_permissions"]))

    display_utils.print_spacer()
    cli_colors.print_banner("Findings")
    if not report["findings"]:
        cli_colors.print_success("No major misconfigurations detected.")
        return
    for finding in report["findings"]:
        cli_colors.print_error(
            f"{finding['issue']} (CVSS {finding['score']} {finding['severity']})"
        )
        if evidence := finding.get("evidence"):
            if isinstance(evidence, list):
                for path in evidence:
                    display_utils.print_key_value("-", path, color="yellow")
            else:
                display_utils.print_key_value("-", str(evidence), color="yellow")
    display_utils.print_spacer()


def export_markdown(report: dict, path: str) -> None:
    """Save the report to a Markdown file."""
    try:
        with open(path, "w", encoding="utf-8") as md:
            md.write("# APK Scan Report\n\n")
            md.write("## Permissions\n")
            for perm_name, ptype in report.get("permissions", {}).items():
                score = report.get("permission_scores", {}).get(perm_name, 0)
                md.write(f"- **{perm_name}** ({ptype}, risk {score}/10)\n")

            if report.get("findings"):
                md.write("\n## Findings\n")
                for f in report["findings"]:
                    md.write(
                        f"- **{f['issue']}** (CVSS {f['score']} {f['severity']})\n"
                    )
                    if evidence := f.get("evidence"):
                        if isinstance(evidence, list):
                            for path in evidence:
                                md.write(f"  - {path}\n")
                        else:
                            md.write(f"  - {evidence}\n")
    except Exception as e:
        log_manager.log_exception(f"Failed to export Markdown report: {e}")


def export_csv(report: dict, path: str) -> None:
    """Save the report to a CSV file for spreadsheet use."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Permission", "Type", "Risk Score"])
            for perm_name, ptype in report.get("permissions", {}).items():
                score = report.get("permission_scores", {}).get(perm_name, 0)
                writer.writerow([perm_name, ptype, score])

            writer.writerow([])
            writer.writerow(["Issue", "CVSS Score", "Severity", "Evidence"])
            for f in report.get("findings", []):
                evidence = "; ".join(f.get("evidence", [])) if isinstance(f.get("evidence"), list) else f.get("evidence", "")
                writer.writerow([f["issue"], f["score"], f["severity"], evidence])
    except Exception as e:
        log_manager.log_exception(f"Failed to export CSV report: {e}")


@log_manager.log_call("info")
def run_scan_menu() -> None:
    """CLI wrapper for scanning a user-supplied directory."""
    display_utils.print_section_title("Static APK Analyzer")
    path = input(cli_colors.cyan("Enter path to decompiled APK directory: ")).strip()
    if not path:
        cli_colors.print_warning("No directory provided.")
        return
    if not os.path.isdir(path):
        cli_colors.print_error("Invalid directory path.")
        return

    log_manager.log_info(f"Scanning APK directory: {path}")
    report = scan_directory(path)
    print_report(report)
    save = input(cli_colors.cyan("Save report to file? (y/N): ")).strip().lower()
    if save == "y":
        out_base = input(cli_colors.cyan("Enter output file path (without extension): ")).strip()
        if out_base:
            export_markdown(report, f"{out_base}.md")
            export_csv(report, f"{out_base}.csv")
            cli_colors.print_success(f"Report saved to {out_base}.md and {out_base}.csv")
        else:
            cli_colors.print_warning("No output path provided. Skipping save.")
    log_manager.log_info("APK scan completed")
