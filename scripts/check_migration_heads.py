#!/usr/bin/env python3
"""Check that Alembic has exactly one migration head.

Multiple heads indicate a migration branch conflict that must be resolved
before merging. Exits 1 if multiple heads detected.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def main() -> int:
    result = subprocess.run(
        ["alembic", "heads"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )

    if result.returncode != 0:
        print(f"ERROR: alembic heads failed:\n{result.stderr}")
        return 1

    heads = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]

    if len(heads) == 0:
        print("WARNING: No migration heads found (is alembic configured?)")
        return 0
    elif len(heads) == 1:
        print(f"OK: Single migration head: {heads[0]}")
        return 0
    else:
        print(f"ERROR: Multiple migration heads detected ({len(heads)}):")
        for head in heads:
            print(f"  - {head}")
        print("\nResolve by creating a merge migration:")
        print("  alembic merge heads -m \"merge migration branches\"")
        return 1


if __name__ == "__main__":
    sys.exit(main())
