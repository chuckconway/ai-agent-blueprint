#!/usr/bin/env python3
"""Local CI check runner.

Reads ci-checks.json and executes checks locally with colored output.
Supports filtering by group (--api/--ui), running fix commands (--fix),
targeting specific checks (--check), and listing available checks (--list).
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_checks() -> list[dict]:
    """Load check definitions from ci-checks.json."""
    config_path = Path(__file__).parent.parent / "ci-checks.json"
    with open(config_path) as f:
        data = json.load(f)
    return data["checks"]


def run_command(command: str, cwd: Path) -> tuple[int, str]:
    """Run a shell command and return exit code + combined output."""
    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    return result.returncode, output


def print_result(name: str, passed: bool, duration: float, output: str) -> None:
    """Print a check result with color."""
    status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
    print(f"  {status}  {name} ({duration:.1f}s)")
    if not passed and output.strip():
        for line in output.strip().split("\n")[-20:]:
            print(f"        {line}")


def list_checks(checks: list[dict]) -> None:
    """Print all available checks."""
    print(f"\n{BOLD}Available checks:{RESET}\n")
    for check in checks:
        fix_indicator = " (has fix)" if check.get("fix_command") else ""
        print(f"  [{check['group']:>3}] {check['name']}{fix_indicator}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CI checks locally")
    parser.add_argument("--api", action="store_true", help="Run API checks only")
    parser.add_argument("--ui", action="store_true", help="Run UI checks only")
    parser.add_argument("--fix", action="store_true", help="Run fix commands first, then validate")
    parser.add_argument("--check", nargs="+", metavar="NAME", help="Run specific check(s) by name")
    parser.add_argument("--list", action="store_true", help="List all available checks")
    args = parser.parse_args()

    checks = load_checks()
    project_root = Path(__file__).parent.parent

    if args.list:
        list_checks(checks)
        return 0

    # Filter by group
    if args.api and not args.ui:
        checks = [c for c in checks if c["group"] == "api"]
    elif args.ui and not args.api:
        checks = [c for c in checks if c["group"] == "ui"]

    # Filter by name
    if args.check:
        selected_names = {name.lower() for name in args.check}
        checks = [c for c in checks if c["name"].lower() in selected_names]
        if not checks:
            print(f"{RED}No checks matched the given names.{RESET}")
            return 1

    if not checks:
        print(f"{YELLOW}No checks to run.{RESET}")
        return 0

    print(f"\n{BOLD}Running {len(checks)} check(s)...{RESET}\n")
    start_time = time.time()
    failures = []

    for check in checks:
        name = check["name"]
        command = check["command"]
        fix_command = check.get("fix_command")

        # Run fix command first if --fix is set and fix_command exists
        if args.fix and fix_command:
            run_command(fix_command, project_root)

        check_start = time.time()
        exit_code, output = run_command(command, project_root)
        duration = time.time() - check_start
        passed = exit_code == 0

        print_result(name, passed, duration, output)
        if not passed:
            failures.append(name)

    total_time = time.time() - start_time
    print(f"\n{'─' * 50}")

    if failures:
        print(f"{RED}{BOLD}FAILED{RESET} ({len(failures)} of {len(checks)} checks failed in {total_time:.1f}s)")
        for name in failures:
            print(f"  {RED}✗{RESET} {name}")
        print()
        return 1
    else:
        print(f"{GREEN}{BOLD}ALL PASSED{RESET} ({len(checks)} checks in {total_time:.1f}s)\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
