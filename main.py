
import os
import platform
import getpass
import subprocess
from datetime import datetime


def get_command_output(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
            check=False
        )
        return (
            result.stdout.strip()
            or result.stderr.strip()
            or "No output"
        )
    except (subprocess.TimeoutExpired, OSError) as error:
        return f"Unable to run command: {error}"


def collect_system_information():
    print("\n" + "=" * 55)
    print("SYSTEM INFORMATION")
    print("=" * 55)

    print(f"Date and time: {datetime.now()}")
    print(f"Username: {getpass.getuser()}")
    print(f"Operating system: {platform.system()}")
    print(f"OS release: {platform.release()}")
    print(f"Machine architecture: {platform.machine()}")

    print("\nHostname:")
    print(get_command_output(["hostname"]))

    print("\nCurrent user and groups:")
    print(get_command_output(["id"]))

    print("\nOS release information:")
    print(get_command_output(["cat", "/etc/os-release"]))

    if os.getuid() == 0:
        print("\nPrivilege level: Running as root")
    else:
        print("\nPrivilege level: Running as a regular user")

    print("\n" + "=" * 55)
    print("System information collection completed.")
    print("=" * 55)


def main():
    while True:
        print("\n" + "=" * 55)
        print(" LINUX PRIVILEGE ESCALATION AUTOMATION TOOLKIT")
        print("=" * 55)
        print("1. Collect System Information")
        print("2. Run SUID Scanner")
        print("3. Run File Permission Scanner")
        print("4. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            collect_system_information()

        elif choice == "2":
            subprocess.run(
                ["python3", "modules/suid_scanner.py"],
                check=False
            )

        elif choice == "3":
            subprocess.run(
                ["python3", "modules/permission_scanner.py"],
                check=False
            )

        elif choice == "4":
            print("Exiting toolkit. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()

