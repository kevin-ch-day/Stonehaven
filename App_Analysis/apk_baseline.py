import os
import csv
from collections import Counter
from typing import Dict, List

from Utils.logging_utils import log_manager
from Utils.app_utils import cli_colors, display_utils

from . import apk_permission_analysis as perm


TEXT_REPORT_PATH = os.path.join("Output", "Text", "permission_baseline.txt")
CSV_REPORT_PATH = os.path.join("Output", "Excel", "permission_baseline.csv")
XLSX_REPORT_PATH = os.path.join("Output", "Excel", "permission_baseline.xlsx")


class APKPermissionBaselineAnalyzer:
    """Aggregate permission statistics across many decompiled APKs."""

    def __init__(self, apk_dir: str):
        self.apk_dir = apk_dir
        self.apk_details: Dict[str, Dict] = {}
        self.permission_frequency: Counter = Counter()
        self.average_permissions: float = 0.0
        self.rare_permissions: List[str] = []

    # ------------------------------------------------------------------
    def scan_apks(self) -> None:
        """Parse manifests from each project and collect permissions."""
        if not os.path.isdir(self.apk_dir):
            return
        for entry in sorted(os.scandir(self.apk_dir), key=lambda e: e.name):
            if not entry.is_dir():
                continue
            manifest = os.path.join(entry.path, "AndroidManifest.xml")
            perms = perm.extract_permissions(manifest)
            self.permission_frequency.update(perms)
            self.apk_details[entry.name] = {"permissions": perms}

    # ------------------------------------------------------------------
    def compute_statistics(self) -> None:
        """Calculate averages, rare permissions and excessive apps."""
        num_apps = len(self.apk_details)
        if num_apps == 0:
            return
        counts = [len(info["permissions"]) for info in self.apk_details.values()]
        self.average_permissions = sum(counts) / num_apps

        self.rare_permissions = [
            perm_name
            for perm_name, cnt in self.permission_frequency.items()
            if (cnt / num_apps) < 0.10
        ]

        for info in self.apk_details.values():
            perms = info["permissions"]
            info["dangerous_count"] = perm.count_dangerous_permissions(perms)
            info["rare_permissions"] = [p for p in perms if p in self.rare_permissions]
            info["excessive"] = len(perms) > 1.5 * self.average_permissions

    # ------------------------------------------------------------------
    def display_summary(self) -> None:
        """Show analysis results in the terminal."""
        display_utils.print_section_title("APK Baseline Report")
        cli_colors.print_info(f"APKs scanned: {len(self.apk_details)}")
        cli_colors.print_info(
            f"Total unique permissions: {len(self.permission_frequency)}"
        )
        cli_colors.print_info(
            f"Average permissions per app: {self.average_permissions:.2f}"
        )
        cli_colors.print_info(
            f"Rare permissions found: {len(self.rare_permissions)}"
        )
        excessive = sum(1 for i in self.apk_details.values() if i.get("excessive"))
        cli_colors.print_info(f"Apps with excessive permissions: {excessive}")
        display_utils.print_spacer()

    # ------------------------------------------------------------------
    def generate_txt_report(self, output_path: str = TEXT_REPORT_PATH) -> None:
        """Write a text summary to disk."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            with open(output_path, "w", encoding="utf-8") as txt:
                txt.write("APK Permission Baseline\n\n")
                txt.write(f"APKs scanned: {len(self.apk_details)}\n")
                txt.write(
                    f"Average permissions per app: {self.average_permissions:.2f}\n\n"
                )
                txt.write("Permission Frequency\n")
                for perm_name, count in self.permission_frequency.most_common():
                    txt.write(f"{perm_name}: {count}\n")

                txt.write("\nApplication Details\n")
                for name, info in self.apk_details.items():
                    txt.write(
                        f"\n{name} - {len(info['permissions'])} permissions\n"
                    )
                    if info.get("excessive"):
                        txt.write("  * Excessive permission count\n")
                    txt.write(
                        "  Permissions: " + ", ".join(info["permissions"]) + "\n"
                    )
                    if info.get("rare_permissions"):
                        txt.write(
                            "  Rare perms: "
                            + ", ".join(info["rare_permissions"])
                            + "\n"
                        )
        except Exception as e:
            log_manager.log_exception(f"Failed to write txt report: {e}")

    # ------------------------------------------------------------------
    def generate_csv_report(self, output_path: str = CSV_REPORT_PATH) -> None:
        """Export data to CSV format."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Permission", "Frequency"])
                for perm_name, count in self.permission_frequency.most_common():
                    writer.writerow([perm_name, count])

                writer.writerow([])
                writer.writerow(
                    ["App", "PermissionCount", "Excessive", "RarePermissions"]
                )
                for name, info in self.apk_details.items():
                    writer.writerow(
                        [
                            name,
                            len(info["permissions"]),
                            info["excessive"],
                            ";".join(info.get("rare_permissions", [])),
                        ]
                    )
        except Exception as e:
            log_manager.log_exception(f"Failed to write CSV report: {e}")

    # ------------------------------------------------------------------
    def generate_excel_report(self, output_path: str = XLSX_REPORT_PATH) -> None:
        """Save results to an Excel workbook if openpyxl is available."""
        try:
            from openpyxl import Workbook
        except Exception as e:  # pragma: no cover - optional dependency
            log_manager.log_exception(f"openpyxl unavailable: {e}")
            return

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        wb = Workbook()
        freq_ws = wb.active
        freq_ws.title = "PermissionFreq"
        freq_ws.append(["Permission", "Frequency"])
        for perm_name, count in self.permission_frequency.most_common():
            freq_ws.append([perm_name, count])

        app_ws = wb.create_sheet("Apps")
        app_ws.append(["App", "PermissionCount", "Excessive", "RarePermissions"])
        for name, info in self.apk_details.items():
            app_ws.append(
                [
                    name,
                    len(info["permissions"]),
                    info["excessive"],
                    ";".join(info.get("rare_permissions", [])),
                ]
            )
        try:
            wb.save(output_path)
        except Exception as e:
            log_manager.log_exception(f"Failed to write XLSX report: {e}")

    # ------------------------------------------------------------------
    def run_baseline_analysis(self) -> None:
        """Perform full analysis and output standard reports."""
        self.scan_apks()
        self.compute_statistics()
        self.display_summary()
        self.generate_txt_report()
        self.generate_csv_report()
        self.generate_excel_report()


@log_manager.log_call("info")
def run_baseline_menu() -> None:
    """Prompt the user for a directory and run baseline analysis."""
    display_utils.print_section_title("APK Baseline Analyzer")
    path = input(
        cli_colors.cyan("Enter path to directory containing APK projects: ")
    ).strip()
    if not path:
        cli_colors.print_warning("No directory provided.")
        return
    if not os.path.isdir(path):
        cli_colors.print_error("Invalid directory path.")
        return

    log_manager.log_info(f"Running baseline analysis on: {path}")
    analyzer = APKPermissionBaselineAnalyzer(path)
    analyzer.run_baseline_analysis()
    cli_colors.print_success(
        "Reports saved to Output/Text and Output/Excel directories"
    )
    log_manager.log_info("Baseline analysis completed")
