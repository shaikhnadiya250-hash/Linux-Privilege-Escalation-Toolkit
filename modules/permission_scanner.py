#!/usr/bin/env python3

import os
import stat
from datetime import datetime


def scan_permissions():
    print("\n=== LINUX FILE PERMISSION SCANNER ===")

    scan_path = input(
        "Directory to scan [test_data]: "
    ).strip() or "test_data"

    scan_path = os.path.abspath(
        os.path.expanduser(scan_path)
    )

    if not os.path.isdir(scan_path):
        print("Error: Directory does not exist.")
        return

    findings = []
    scanned = 0

    for root, dirs, files in os.walk(
        scan_path, followlinks=False
    ):
        dirs[:] = [
            d for d in dirs
            if not os.path.islink(os.path.join(root, d))
        ]

        for name in dirs + files:
            path = os.path.join(root, name)

            try:
                info = os.lstat(path)
                if not (
                    stat.S_ISREG(info.st_mode)
                    or stat.S_ISDIR(info.st_mode)
                ):
                    continue

                scanned += 1
                mode = stat.S_IMODE(info.st_mode)
                issues = []

                if mode & stat.S_IWOTH:
                    issues.append("WORLD-WRITABLE")

                if mode & stat.S_IWGRP:
                    issues.append("GROUP-WRITABLE")

                if issues:
                    findings.append(
                        (path, format(mode, "04o"), ", ".join(issues))
                    )

            except OSError:
                print(f"[SKIPPED] Cannot read: {path}")

    print(f"\nItems scanned: {scanned}")
    print(f"Potential findings: {len(findings)}")

    for path, permissions, issue in findings:
        print(f"[REVIEW] {path} | {permissions} | {issue}")

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/file_permission_report.txt",
        "w",
        encoding="utf-8"
    ) as report:
        report.write("FILE PERMISSION SCAN REPORT\n")
        report.write(f"Date: {datetime.now()}\n")
        report.write(f"Directory: {scan_path}\n")
        report.write(f"Items scanned: {scanned}\n")
        report.write(f"Findings: {len(findings)}\n\n")

        for path, permissions, issue in findings:
            report.write(
                f"{path} | {permissions} | {issue}\n"
            )

    print("\nReport saved to reports/file_permission_report.txt")


if __name__ == "__main__":
    scan_permissions()
