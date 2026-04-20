#!/usr/bin/env bash
# UI code health checks:
# - No files over 500 lines in ui/src/
# - No bare fetch() calls (must use api client)
# - No window.alert, window.confirm, window.prompt

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
UI_SRC="$PROJECT_ROOT/ui/src"

FAILURES=0

echo "UI Code Health Check"
echo "=================================================="

# Check 1: File length
echo ""
echo "[File length (max 500 lines)]"
if [ -d "$UI_SRC" ]; then
    LONG_FILES=""
    while IFS= read -r -d '' file; do
        lines=$(wc -l < "$file")
        if [ "$lines" -gt 500 ]; then
            rel_path="${file#$PROJECT_ROOT/}"
            LONG_FILES="${LONG_FILES}  ${rel_path}: ${lines} lines\n"
        fi
    done < <(find "$UI_SRC" -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" | tr '\n' '\0')

    if [ -n "$LONG_FILES" ]; then
        echo "  FAIL: Files exceeding 500 lines:"
        echo -e "$LONG_FILES"
        FAILURES=$((FAILURES + 1))
    else
        echo "  PASS"
    fi
else
    echo "  SKIP: ui/src/ directory not found"
fi

# Check 2: Bare fetch() calls
echo ""
echo "[No bare fetch() calls]"
if [ -d "$UI_SRC" ]; then
    # Look for fetch( but exclude api client files and test files
    BARE_FETCH=$(grep -rn "\\bfetch(" "$UI_SRC" \
        --include="*.ts" --include="*.tsx" \
        --exclude="*api.ts" --exclude="*api-client*" \
        --exclude="*.test.*" --exclude="*.spec.*" \
        2>/dev/null || true)

    if [ -n "$BARE_FETCH" ]; then
        echo "  FAIL: Bare fetch() calls found (use api client instead):"
        echo "$BARE_FETCH" | head -10 | sed 's/^/  /'
        FETCH_COUNT=$(echo "$BARE_FETCH" | wc -l | tr -d ' ')
        if [ "$FETCH_COUNT" -gt 10 ]; then
            echo "  ... and $((FETCH_COUNT - 10)) more"
        fi
        FAILURES=$((FAILURES + 1))
    else
        echo "  PASS"
    fi
else
    echo "  SKIP: ui/src/ directory not found"
fi

# Check 3: Browser dialogs
echo ""
echo "[No browser dialogs (window.alert/confirm/prompt)]"
if [ -d "$UI_SRC" ]; then
    DIALOGS=$(grep -rn "window\.\(alert\|confirm\|prompt\)" "$UI_SRC" \
        --include="*.ts" --include="*.tsx" \
        --exclude="*.test.*" --exclude="*.spec.*" \
        2>/dev/null || true)

    if [ -n "$DIALOGS" ]; then
        echo "  FAIL: Browser dialog calls found (use modal components instead):"
        echo "$DIALOGS" | sed 's/^/  /'
        FAILURES=$((FAILURES + 1))
    else
        echo "  PASS"
    fi
else
    echo "  SKIP: ui/src/ directory not found"
fi

# Summary
echo ""
echo "=================================================="
if [ "$FAILURES" -gt 0 ]; then
    echo "FAILED: $FAILURES check(s) failed."
    exit 1
else
    echo "ALL PASSED: UI code health is good."
    exit 0
fi
