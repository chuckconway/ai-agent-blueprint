# Commit Skill

Commit changes with formatting, linting, PR creation, and worktree cleanup.

## Trigger

Activated by `/commit` or `/commit <message>`.

## Workflow

### 1. Run CI Checks with Auto-Fix

```bash
uv run python scripts/ci_check_local.py --fix
```

This runs all checks defined in `ci-checks.json`:
- Ruff lint + format (with auto-fix)
- mypy type checking
- Unit tests
- ESLint + TypeScript (UI)
- Code health checks

### 2. Fix Remaining Failures

If any checks still fail after `--fix`:
- Read the error output
- Fix the underlying issues (not just suppress warnings)
- Re-run `uv run python scripts/ci_check_local.py` until clean

### 3. Stage and Commit

```bash
git add <changed-files>
git commit -m "<type>: <description>"
```

Follow Conventional Commits format:
- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `refactor:` — code change that neither fixes a bug nor adds a feature
- `test:` — adding or updating tests
- `chore:` — maintenance tasks

If the user provided a message with `/commit`, use it. Otherwise, generate a concise message from the staged changes.

### 4. Push and Create PR

```bash
git push -u origin <branch-name>
```

Create a PR targeting `dev`:
- Title: the commit message (without the type prefix if too long)
- Body: summary of changes, test plan

### 5. Report

Output the PR URL and a brief summary of what was committed.

## Rules

- **Never skip CI checks.** The whole point is to catch issues before they reach remote CI.
- **Fix errors in the affected files** — not just those caused by your immediate changes.
- **One commit per PR.** If you have multiple logical changes, they should be in separate worktrees.
- **Never amend an existing commit** unless explicitly asked. Create new commits.
- **Never force-push** unless explicitly asked.

## Example

```
User: /commit

Agent:
1. Runs ci_check_local.py --fix
2. Fixes 2 ruff warnings (unused import, missing type hint)
3. Re-runs checks — all pass
4. Commits: "feat: add document search tool to agent"
5. Pushes and creates PR
6. Reports: "PR #42 created: feat/document-search -> dev"
```
