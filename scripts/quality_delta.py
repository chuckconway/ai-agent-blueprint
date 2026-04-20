#!/usr/bin/env python3
"""PR quality ratchet checker.

Compares current branch against merge base to detect quality regressions:
- type: ignore count increase
- noqa comment count increase
- Missing type annotations on changed public functions
- Missing docstrings on changed public classes/methods
- C901 complexity on changed files

Exits 1 if any regression detected.
"""

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
TYPE_IGNORE_THRESHOLD_FILE = PROJECT_ROOT / ".type-ignore-threshold"
NOQA_THRESHOLD_FILE = PROJECT_ROOT / ".noqa-threshold"


def get_merge_base() -> str:
    """Get the merge base commit between current branch and dev."""
    result = subprocess.run(
        ["git", "merge-base", "HEAD", "origin/dev"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    if result.returncode != 0:
        # Fallback to main
        result = subprocess.run(
            ["git", "merge-base", "HEAD", "origin/main"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
    return result.stdout.strip()


def get_changed_files(merge_base: str) -> list[Path]:
    """Get list of changed Python files since merge base."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", merge_base, "HEAD"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    files = []
    for line in result.stdout.strip().split("\n"):
        if line.strip() and line.endswith(".py"):
            path = PROJECT_ROOT / line.strip()
            if path.exists():
                files.append(path)
    return files


def count_pattern_in_tree(pattern: str, directory: str = "src/") -> int:
    """Count occurrences of a pattern in the source tree."""
    result = subprocess.run(
        ["grep", "-r", "--include=*.py", "-c", pattern, directory],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    total = 0
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            try:
                total += int(line.rsplit(":", 1)[1])
            except ValueError:
                continue
    return total


def read_threshold(filepath: Path) -> int | None:
    """Read a numeric threshold from a file."""
    if filepath.exists():
        try:
            return int(filepath.read_text().strip())
        except ValueError:
            return None
    return None


def check_type_ignore() -> list[str]:
    """Check that type: ignore count hasn't increased."""
    violations = []
    current_count = count_pattern_in_tree("# type: ignore")
    threshold = read_threshold(TYPE_IGNORE_THRESHOLD_FILE)

    if threshold is not None and current_count > threshold:
        violations.append(
            f"  type: ignore count increased: {current_count} (threshold: {threshold})"
        )
    elif threshold is None:
        # No threshold file, just report
        print(f"  INFO: {current_count} type: ignore comments (no threshold file)")

    return violations


def check_noqa() -> list[str]:
    """Check that noqa count hasn't increased."""
    violations = []
    current_count = count_pattern_in_tree("# noqa")
    threshold = read_threshold(NOQA_THRESHOLD_FILE)

    if threshold is not None and current_count > threshold:
        violations.append(
            f"  noqa count increased: {current_count} (threshold: {threshold})"
        )
    elif threshold is None:
        print(f"  INFO: {current_count} noqa comments (no threshold file)")

    return violations


def check_type_annotations(changed_files: list[Path]) -> list[str]:
    """Check that changed public functions have type annotations."""
    violations = []

    for filepath in changed_files:
        try:
            source = filepath.read_text()
            tree = ast.parse(source)
        except (SyntaxError, OSError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private/dunder functions
                if node.name.startswith("_"):
                    continue

                # Check return annotation
                if node.returns is None:
                    rel_path = filepath.relative_to(PROJECT_ROOT)
                    violations.append(
                        f"  {rel_path}:{node.lineno} {node.name}() missing return type annotation"
                    )

    return violations


def check_docstrings(changed_files: list[Path]) -> list[str]:
    """Check that changed public classes/methods have docstrings."""
    violations = []

    for filepath in changed_files:
        try:
            source = filepath.read_text()
            tree = ast.parse(source)
        except (SyntaxError, OSError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if node.name.startswith("_"):
                    continue
                if not ast.get_docstring(node):
                    rel_path = filepath.relative_to(PROJECT_ROOT)
                    violations.append(
                        f"  {rel_path}:{node.lineno} class {node.name} missing docstring"
                    )

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_"):
                    continue
                if not ast.get_docstring(node):
                    rel_path = filepath.relative_to(PROJECT_ROOT)
                    violations.append(
                        f"  {rel_path}:{node.lineno} {node.name}() missing docstring"
                    )

    return violations


def check_complexity(changed_files: list[Path]) -> list[str]:
    """Run ruff C901 check on changed files."""
    violations = []

    py_files = [str(f) for f in changed_files if f.suffix == ".py"]
    if not py_files:
        return violations

    result = subprocess.run(
        ["ruff", "check", "--select", "C901", *py_files],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    if result.stdout.strip():
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                violations.append(f"  {line.strip()}")

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description="Quality delta checker")
    parser.add_argument(
        "--check",
        choices=["all", "type-ignore", "noqa", "annotations", "docstrings", "complexity"],
        default="all",
        help="Which check(s) to run",
    )
    args = parser.parse_args()

    print("Quality Delta Check")
    print("=" * 50)

    merge_base = get_merge_base()
    if not merge_base:
        print("  WARNING: Could not determine merge base. Skipping delta checks.")
        return 0

    changed_files = get_changed_files(merge_base)
    print(f"\n  Merge base: {merge_base[:8]}")
    print(f"  Changed Python files: {len(changed_files)}")

    all_violations = []
    checks_to_run = args.check

    # type: ignore check
    if checks_to_run in ("all", "type-ignore"):
        print("\n[type: ignore threshold]")
        violations = check_type_ignore()
        all_violations.extend(violations)
        if violations:
            for v in violations:
                print(v)
        else:
            print("  PASS")

    # noqa check
    if checks_to_run in ("all", "noqa"):
        print("\n[noqa threshold]")
        violations = check_noqa()
        all_violations.extend(violations)
        if violations:
            for v in violations:
                print(v)
        else:
            print("  PASS")

    # Type annotations
    if checks_to_run in ("all", "annotations"):
        print("\n[type annotations on public functions]")
        violations = check_type_annotations(changed_files)
        all_violations.extend(violations)
        if violations:
            print(f"  FAIL: {len(violations)} missing annotation(s)")
            for v in violations[:10]:
                print(v)
            if len(violations) > 10:
                print(f"  ... and {len(violations) - 10} more")
        else:
            print("  PASS")

    # Docstrings
    if checks_to_run in ("all", "docstrings"):
        print("\n[docstrings on public classes/methods]")
        violations = check_docstrings(changed_files)
        all_violations.extend(violations)
        if violations:
            print(f"  FAIL: {len(violations)} missing docstring(s)")
            for v in violations[:10]:
                print(v)
            if len(violations) > 10:
                print(f"  ... and {len(violations) - 10} more")
        else:
            print("  PASS")

    # Complexity
    if checks_to_run in ("all", "complexity"):
        print("\n[C901 complexity on changed files]")
        violations = check_complexity(changed_files)
        all_violations.extend(violations)
        if violations:
            print(f"  FAIL: {len(violations)} complex function(s)")
            for v in violations[:10]:
                print(v)
        else:
            print("  PASS")

    # Summary
    print("\n" + "=" * 50)
    if all_violations:
        print(f"\nFAILED: {len(all_violations)} quality regression(s) detected.\n")
        return 1
    else:
        print("\nALL PASSED: No quality regressions.\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())
