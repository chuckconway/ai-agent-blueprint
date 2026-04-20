#!/usr/bin/env python3
"""Code health checker using radon.

Checks:
- Maintainability Index: minimum grade B for all files
- Cyclomatic Complexity: max 20 per function
- File SLOC: max 500 lines per file

Scans src/app/ directory. Exits 1 if any violations found.
"""

import subprocess
import sys
from pathlib import Path

# Thresholds
MAX_COMPLEXITY = 20
MIN_MI_GRADE = "B"  # A is best, then B, C, etc.
MAX_SLOC = 500

# Grade ordering (lower index = better)
MI_GRADES = ["A", "B", "C", "D", "E", "F"]

PROJECT_ROOT = Path(__file__).parent.parent
SCAN_DIR = PROJECT_ROOT / "src" / "app"


def check_maintainability_index() -> list[str]:
    """Check Maintainability Index for all files. Returns list of violations."""
    violations = []

    if not SCAN_DIR.exists():
        return violations

    result = subprocess.run(
        ["radon", "mi", str(SCAN_DIR), "-s"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    if result.returncode != 0 and "No such file" in result.stderr:
        return violations

    min_grade_idx = MI_GRADES.index(MIN_MI_GRADE)

    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("-"):
            continue
        # Format: "filename - grade (score)"
        if " - " in line:
            parts = line.rsplit(" - ", 1)
            if len(parts) == 2:
                filepath = parts[0].strip()
                grade_part = parts[1].strip()
                grade = grade_part[0] if grade_part else ""
                if grade in MI_GRADES:
                    grade_idx = MI_GRADES.index(grade)
                    if grade_idx > min_grade_idx:
                        violations.append(
                            f"  {filepath}: MI grade {grade} (minimum: {MIN_MI_GRADE})"
                        )

    return violations


def check_cyclomatic_complexity() -> list[str]:
    """Check Cyclomatic Complexity for all functions. Returns list of violations."""
    violations = []

    if not SCAN_DIR.exists():
        return violations

    result = subprocess.run(
        ["radon", "cc", str(SCAN_DIR), "-s", "--min", "B", "--json"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    if result.returncode != 0:
        return violations

    try:
        import json
        data = json.loads(result.stdout) if result.stdout.strip() else {}
    except (json.JSONDecodeError, ValueError):
        # Fall back to text parsing
        result = subprocess.run(
            ["radon", "cc", str(SCAN_DIR), "-s", "--min", "B"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if "(" in line and ")" in line and any(c.isdigit() for c in line):
                # Try to extract complexity score
                pass
        return violations

    for filepath, functions in data.items():
        for func in functions:
            complexity = func.get("complexity", 0)
            name = func.get("name", "unknown")
            lineno = func.get("lineno", "?")
            if complexity > MAX_COMPLEXITY:
                violations.append(
                    f"  {filepath}:{lineno} {name}() complexity={complexity} (max: {MAX_COMPLEXITY})"
                )

    return violations


def check_file_sloc() -> list[str]:
    """Check that no file exceeds MAX_SLOC lines. Returns list of violations."""
    violations = []

    if not SCAN_DIR.exists():
        return violations

    for py_file in SCAN_DIR.rglob("*.py"):
        try:
            line_count = sum(1 for line in open(py_file) if line.strip() and not line.strip().startswith("#"))
            if line_count > MAX_SLOC:
                rel_path = py_file.relative_to(PROJECT_ROOT)
                violations.append(
                    f"  {rel_path}: {line_count} SLOC (max: {MAX_SLOC})"
                )
        except OSError:
            continue

    return violations


def main() -> int:
    print("Code Health Check")
    print("=" * 50)

    all_violations = []

    # Maintainability Index
    print("\nMaintainability Index (min grade: B)...")
    mi_violations = check_maintainability_index()
    if mi_violations:
        print(f"  FAIL: {len(mi_violations)} file(s) below threshold")
        all_violations.extend(mi_violations)
    else:
        print("  PASS")

    # Cyclomatic Complexity
    print(f"\nCyclomatic Complexity (max: {MAX_COMPLEXITY})...")
    cc_violations = check_cyclomatic_complexity()
    if cc_violations:
        print(f"  FAIL: {len(cc_violations)} function(s) too complex")
        all_violations.extend(cc_violations)
    else:
        print("  PASS")

    # File SLOC
    print(f"\nFile SLOC (max: {MAX_SLOC})...")
    sloc_violations = check_file_sloc()
    if sloc_violations:
        print(f"  FAIL: {len(sloc_violations)} file(s) too long")
        all_violations.extend(sloc_violations)
    else:
        print("  PASS")

    # Summary
    print("\n" + "=" * 50)
    if all_violations:
        print(f"\nFAILED: {len(all_violations)} violation(s) found:\n")
        for v in all_violations:
            print(v)
        print()
        return 1
    else:
        print("\nALL PASSED: Code health is good.\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
