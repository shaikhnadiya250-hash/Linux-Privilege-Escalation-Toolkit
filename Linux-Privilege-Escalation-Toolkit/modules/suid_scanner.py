#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

def scan_suid_files():
    print("\n=== SUID FILE PERMISSION SCANNER ===")
    print("Scanning for SUID files. Please wait...\n")

    try:
        result = subprocess.run(
            ["find", "/", "-type", "f", "-perm", "-4000"],
            capture_output=True,
            text=True,
            timeout=120
        )

        files = sorted(set(result.stdout.splitlines()))

        print(f"Total SUID files found: {len(files)}")

        for path in files:
            print(f"[SUID] {path}")

        os.makedirs("reports", exist_ok=True)

        with open("reports/suid_scan_report.txt", "w") as report:
            report.write("SUID SCAN REPORT\n")
            report.write(f"Date: {datetime.now()}\n")
            report.write(f"Total files found: {len(files)}\n\n")
            report.writelines(path + "\n" for path in files)

        print("\nReport saved to reports/suid_scan_report.txt")

        if result.stderr:
            print("Note: Some filesystem paths could not be accessed.")

    except subprocess.TimeoutExpired:
        print("Scan exceeded the 120-second time limit.")
    except OSError as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    scan_suid_files()
