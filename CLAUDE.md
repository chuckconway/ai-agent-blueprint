# AI Agent Blueprint

Authoritative reference for coding rules and conventions. For system context (what the system is, how it's deployed, external integrations), read `docs/SYSTEM_OVERVIEW.md` — especially before starting major work.

## Project Description

This is a starter blueprint for AI agent web applications. It provides a production-ready architecture for building conversational AI agents with tool use, streaming responses, and background task processing.

Replace this section with a description of your specific application when you start building.

## Honest Opposition (Required)

**If the user's approach has a significant downside, say so — even if they seem committed.** Agreeing because it's easier is a failure mode. Disagreement is part of your value.

- State disagreements directly: "I disagree because X" — not "Great idea! One small thing..."
- Never silently simplify, drop scope, or pivot to a different approach when blocked. Stop and ask, presenting at least two options.
- When confirming the user is right, explain why alternatives are worse. Validation without reasoning is not useful.

## Branch Isolation (Required)

**Every task must be developed in isolation using git worktrees.** This prevents conflicts when multiple agents work simultaneously by giving each agent its own working directory.

**CRITICAL: Create the worktree FIRST, before ANY code changes.** Do not modify files, read-and-edit, or run generators in the main repo directory. Investigation and reading files in the main repo is fine, but all file modifications happen inside the worktree.

**All development is based off the `dev` branch.** Every worktree must be created from `dev`, and all PRs target `dev`. The `main` branch is for production releases only.

### What Constitutes a "Task"

A task is a **single user request or logical unit of work** that would result in one PR. Examples:
- "Add a delete button to the chat history" — one task, one worktree
- "Fix the bug where agents timeout" — one task, one worktree
- "Refactor the tool registry to use dependency injection" — one task, one worktree

**Not separate tasks** (keep in same worktree):
- Multiple files edited to implement one feature
- Tests added for a feature you just built
- Fixing lint errors from your own changes

**Rule of thumb**: If it gets one commit message or one PR title, it's one task.

### Workflow

- **Always pull latest `dev` before starting work**:
  ```bash
  git fetch origin dev
  git checkout dev && git pull origin dev
  ```
- **One worktree per task**: Never commit unrelated changes to the same worktree.
- **Worktree naming**: Use `../<project>-<type>-<short-description>` (e.g., `../blueprint-feat-tool-registry`).
- **Creating worktrees**:
  ```bash
  git worktree add ../blueprint-feat-tool-registry -b feat/tool-registry origin/dev
  git worktree list
  git worktree remove ../blueprint-feat-tool-registry  # after merging
  ```
- **Never update an existing PR — always create a new one**: Once a PR has been created, do not push additional commits to it. If follow-up changes are needed, create a new worktree, new branch, and new PR. This keeps each PR an atomic, reviewable unit.
- **User bug reports mean the PR is merged**: When the user reports something doesn't work, assume the PR is already merged and deployed. Always create a new worktree for the fix.

## Architecture & Design

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the full package map, data flow diagrams, and layer descriptions.

### Principles

- **Layered architecture enforced by import-linter**: `app.api` -> `app.agent` -> `app.core`. Lower layers cannot import from higher layers.
- Apply Domain-Driven Design: speak the domain language in code, keep domain logic independent of frameworks, prefer value objects/entities over primitive obsession.
- Enforce SOLID: one reason to change per class, open/closed for extension, small interfaces, dependency inversion via factories/injection.
- Prefer composition over inheritance; extract strategies/factories/builders when behavior varies.

### Unit of Work (UoW)

Use `AsyncUnitOfWork` from `app.core.database.unit_of_work` to scope transactions. Application services own the transaction boundary; repositories receive the session and call `flush()` (not `commit()`). The UoW commits on clean exit and rolls back on exception.

```python
async with AsyncUnitOfWork() as uow:
    repo = ConversationRepository(uow.session)
    await repo.create(conversation)
```

Use `uow.flush()` to get generated IDs mid-transaction. Never call `commit()` inside a repository method.

### Repository Pattern

Every aggregate root gets its own repository. Repositories extend `BaseRepository[Model]` (or `SoftDeleteRepository[Model]` for soft-delete entities) and accept an `AsyncSession` in `__init__`. Add entity-specific queries as async methods on the subclass.

### Database Loading Strategy

**Never use SQLAlchemy lazy loading.** All relationships must use `lazy="raise"` or be explicitly eager-loaded.

- Use `selectinload()` or `joinedload()` in queries when you need related data
- Create PostgreSQL views for cross-domain data needs
- Map views to read-only SQLAlchemy models for typed access

```python
# CORRECT — explicit eager load
query = select(Conversation).options(joinedload(Conversation.messages))

# WRONG — lazy loading (default SQLAlchemy behavior)
conversation.messages  # implicit query, may N+1
```

### Exception Hierarchy

Raise domain exceptions from `app.core.exceptions` (`ResourceNotFoundError`, `DuplicateResourceError`, `ValidationError`, `AuthorizationError`, `ExternalServiceError`, etc.). The API layer maps them to HTTP responses automatically. Never import `app.api` exceptions from `app.core`.

### API Schema Conventions

- Name schemas `XxxBase` -> `XxxCreate`/`XxxUpdate` -> `XxxResponse` (Pydantic `BaseModel`).
- Response schemas use `model_config = ConfigDict(from_attributes=True)` when serializing ORM models.
- Wrap single-item responses in `ApiResponse[T]`; use `PaginatedResponse[T]` for lists with pagination metadata.

## FastAPI Routing Pattern

This codebase follows a **two-tier routing pattern** to ensure all routes have valid paths.

### The Rules

1. **Always use `/` for route paths, never empty string `""`**
2. **Routers included with prefix**: Use `@router.get("/")` for root
3. **Nested routers without prefix**: Use explicit paths like `@router.get("/items")`

### Tier 1: Top-level routers (in routes.py)

```python
# routes.py
api_router.include_router(chat_router, prefix="/chat")

# features/chat/api.py
router = APIRouter()

@router.get("/")       # -> /api/chat/
@router.post("/send")  # -> /api/chat/send
```

### Tier 2: Nested sub-routers

```python
# Router defines its own prefix
router.include_router(tools_router)

# features/agent/routers/tools.py
router = APIRouter(prefix="/tools")
@router.get("/")  # -> /api/agent/tools/
```

### Common Mistake

**Never do this** — causes "Prefix and path cannot be both empty":
```python
router.include_router(sub_router)  # No prefix
# sub.py
router = APIRouter()  # No prefix
@router.get("")  # Empty path = ERROR
```

## Agent Layer

The agent layer handles AI model interactions, tool orchestration, and response streaming.

- **Facade**: `app.agent.facade` — single entry point for agent interactions
- **Tools**: `@tool` decorator in `app.agent.tools/` — define callable functions for the agent
- **Interceptors**: `app.agent.interceptors/` — request/response pipeline for pre/post-processing
- **Adapters**: `app.agent.adapters/` — provider-agnostic via adapter pattern (Anthropic, OpenAI, etc.)
- **Streaming**: `app.agent.streaming` — SSE-based streaming responses to the frontend

### Tool Registration

```python
from app.agent.tools import tool

@tool(name="search_documents", description="Search user documents by query")
async def search_documents(query: str, limit: int = 10) -> list[dict]:
    """Search documents matching the query."""
    ...
```

## SAQ Task Queue

**SAQ (Simple Async Queue)** is the task queue for all background work. It uses Redis as its backend.

### Key Rule

**SAQ defaults to a 10-second job timeout** — far too short for I/O, LLM calls, or batch processing. Always specify `timeout=DEFAULT_JOB_TIMEOUT` (300s).

```python
from app.core.task_queue.interface import enqueue
from app.saq.config import DEFAULT_JOB_TIMEOUT

# CORRECT - explicit timeout
await enqueue("task_name", timeout=DEFAULT_JOB_TIMEOUT, user_id=user_id)

# WRONG - inherits SAQ's 10-second default, will timeout on any I/O
await enqueue("task_name", user_id=user_id)
```

### Adding New Tasks

1. Create task function in `src/app/saq/tasks/<module>.py`
2. Register it in `src/app/saq/tasks/__init__.py` by adding to `ALL_TASKS` dict
3. Enqueue via `app.core.task_queue.interface.enqueue()` with an explicit timeout

## Frontend Conventions

The UI is a React + TypeScript application in `ui/`.

### Stack

- **React 19** + **TypeScript** + **Vite**
- **Zustand** for state management
- **React Router v7** for navigation
- **Tailwind CSS v4** for styling

### Conventions

- **Feature-slice architecture**: features live in `ui/src/features/<name>/` with co-located components, hooks, stores, and API calls
- **Path-mapped imports**: use `@/`, `@features/`, `@shared/` (configured in `tsconfig.json`)
- **HTTP calls**: All API calls must go through `shared/services/api.ts`. Never use bare `fetch()`. Use `api.get/post/put/patch/delete` for standard calls, `api.fetchRaw()` for streaming/SSE.
- **No browser dialogs**: Never use `window.prompt()`, `window.confirm()`, or `window.alert()`. Use in-app modals from `@shared/components/ui`.
- **Custom hooks**: Name hooks `use<Domain>` or `use<Feature>`. Co-locate in a `hooks/` directory under their feature slice.
- **Zustand stores**: App-wide state in `useAppStore` (slice pattern). Feature-local state in standalone `use<Feature>Store`. Use local `useState` for ephemeral UI state.

## Code Quality

### Size Limits

- **Functions**: 20 lines or fewer, cyclomatic complexity 10 or fewer
- **Files**: Target 200-300 lines, hard limit 500 lines — decompose when exceeded
- **Principle**: Cohesion over small files. Don't split prematurely; split when a file clearly has multiple responsibilities.

### Type Safety

- Use explicit type hints on all public functions and methods
- Every public class, method, and function must have a docstring explaining **what** it does and **why** it exists
- Add inline comments only for non-obvious logic and "why" decisions
- Validate/sanitize inputs at boundaries; raise domain exceptions for business-rule violations
- No magic numbers; favor named constants/enums/value objects

### When to use `# noqa` vs. actually fix the problem

**`# noqa` is a last resort, not a shortcut.** Before suppressing any lint rule, first ask "can I fix this?" — most of the time, the answer is yes.

**The rule:**

1. **First, try to fix it.** Rewrite the code so the rule passes naturally.
2. **If fixing is disproportionate**, consider a **per-file-ignore** in `pyproject.toml` rather than scattering inline noqas.
3. **Inline `# noqa` is only appropriate when** the suppression is genuinely site-specific. The inline comment **must include a reason**: `# noqa: RULE - <reason>`.
4. **Never use `# noqa` to silence a warning you don't understand.** Read the rule documentation first.

**Anti-patterns:**
```python
# WRONG — blind suppression, no reason
except Exception:  # noqa: BLE001
    pass

# WRONG — suppressing a rule that has a clean fix
query = query.where(Model.is_active == True)  # noqa: E712
```

**Correct patterns:**
```python
# CORRECT — fixed the root cause
query = query.where(Model.is_active.is_(True))

# CORRECT — inline noqa with a specific reason
except Exception as exc:  # noqa: BLE001 - best-effort publish, fallback handles it
    logger.warning("publish failed", error=str(exc))
```

**Category-specific guidance:**

- **`E712`** (`== True`): Use `.is_(True)` / `.is_(False)` for SQLAlchemy. Do not suppress.
- **`BLE001`** (blind `except Exception`): Legitimate in four cases — task top-level handlers, best-effort side effects, logging-only handlers, outermost API boundaries. The noqa **must** name the category.
- **`PLR0913`** (too many arguments): Add file to per-file-ignores in `pyproject.toml`.
- **`F401`** (unused import): If re-export, add `__all__`. If side-effect import, use `# noqa: F401 - side effect: registers <what>`.

**When in doubt, fix it.** A noqa comment is a permanent annotation that future readers must evaluate.

## Database Migrations

**Always use the expand/contract pattern** for schema changes to enable zero-downtime deployments and safe rollbacks.

### Running Migrations

```bash
alembic upgrade head                              # Apply all pending
alembic revision --autogenerate -m "description"  # Create new migration
alembic current                                   # Check state
alembic heads                                     # Check for multiple heads
```

### The Expand/Contract Pattern

**Phase 1: Expand** (backward-compatible changes)
- Add new columns as `nullable` or with `server_default`
- Create new tables, add new indexes
- **Never**: drop columns, rename columns, add NOT NULL without defaults

```python
# GOOD - Expand migration (backward-compatible)
def upgrade():
    op.add_column("users", sa.Column("phone", sa.String(20), nullable=True))

# BAD - Breaking migration
def upgrade():
    op.add_column("users", sa.Column("phone", sa.String(20), nullable=False))
```

**Phase 2: Deploy & Verify** — deploy new code, monitor, confirm stability

**Phase 3: Contract** (in a later release)
- Backfill data, add constraints, drop deprecated columns

### Migration Checklist

Before writing a migration, ask:
1. Can the **old code** run against this schema? If no, split into expand/contract.
2. Does it add a NOT NULL column? Add with `server_default` or make nullable.
3. Does it drop/rename a column? Wait for contract phase.
4. Does it change a column type? Usually needs expand/contract with a new column.

## CI/CD Pipeline

### Architecture

`ci-checks.json` is the single source of truth for all CI checks. Three tiers:

- **Tier 1: Pre-commit** (~5 sec) — formatting, basic lint
- **Tier 2: Local CI** (~30-60 sec) — full lint, type check, unit tests, code health
- **Tier 3: Remote CI** (~3-5 min) — integration tests, build, deploy

### Running Checks Locally

```bash
# Run all checks
uv run python scripts/ci_check_local.py

# API or UI only
uv run python scripts/ci_check_local.py --api
uv run python scripts/ci_check_local.py --ui

# Auto-fix then validate
uv run python scripts/ci_check_local.py --fix

# Run specific checks
uv run python scripts/ci_check_local.py --check "Ruff lint" "Mypy"

# List available checks
uv run python scripts/ci_check_local.py --list
```

### Individual Checks

| Check | Command |
|-------|---------|
| Ruff lint | `ruff check src/ tests/` |
| Ruff format | `ruff format --check src/ tests/` |
| Type check | `uv run mypy --config-file pyproject.toml src/` |
| Unit tests | `uv run pytest tests/ -m "not integration" -v` |
| Migration heads | `alembic heads` |
| ESLint (UI) | `cd ui && npm run lint` |
| TypeScript (UI) | `cd ui && npx tsc --noEmit` |

## Testing

- Follow **FIRST** principles: Fast, Independent, Repeatable, Self-validating, Timely
- Use **Arrange/Act/Assert** style with clear fixture naming
- Mock external APIs and queues; real integrations live in integration tests
- Target >=80% coverage; add regression tests for every bug fix
- **Markers**: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e`, `@pytest.mark.slow`
- CI runs `pytest -m "not integration"` by default
- **Don't test what the type system guarantees**: Never write tests that merely verify type enforcement. Focus on runtime behavior, business logic, edge cases, and integration boundaries.

## Compound Learning

This project uses a **compound engineering loop** where lessons from debugging and development are systematically captured and fed back into future work.

### The Loop

1. **Consult** (during Planning): Before starting work, search `docs/lessons-learned/` for relevant prior knowledge.
2. **Capture** (after Debugging): After resolving any non-trivial bug, write a lesson-learned doc.
3. **Promote** (when a pattern recurs): If a lesson represents a universal rule, add it to this `CLAUDE.md` file.

### When to Write a Lesson

Write a `docs/lessons-learned/<topic>.md` when:
- A bug took significant investigation to diagnose
- The root cause was non-obvious or counter-intuitive
- The same mistake has been made more than once
- A pattern/anti-pattern emerged that future work should know about

### Searching Lessons

```bash
grep -r "keyword" docs/lessons-learned/
ls docs/lessons-learned/
```

## Tracer Bullets

When building features, build a tiny end-to-end slice first — wire through all layers (API route -> agent/service -> database/integration) — seek feedback, then expand. This ensures the architecture is sound before investing in full implementation.

## Committing Changes

**Always use the `/commit` skill** to commit changes. This ensures consistent formatting and linting.

Follow Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, etc. Keep commits focused.

```
/commit                              # Claude generates commit message
/commit fix: resolve timeout bug     # Use your own message
```

The `/commit` skill:
1. Runs `ci_check_local.py --fix` (the full CI validation suite with auto-fix)
2. Fixes any remaining failures until all checks pass
3. Stages, commits, and pushes changes
4. Creates a PR to `dev`

## Environment Configuration

All environment variables are documented in `env.example` at the project root. Copy it to `.env` and fill in required values.

Key categories: app configuration, database/Redis, authentication, LLM providers.

## Server & Infrastructure

<!-- Fill in when you deploy -->
<!-- Example:
| Host | IP | Role |
|------|-----|------|
| **app-server** | x.x.x.x | k8s cluster, application workloads |
| **db-server** | x.x.x.x | PostgreSQL |

### Namespaces
- `app-dev` — Development environment
- `app-prod` — Production environment
-->

## Skills

### Project Skills (`skills/`)

| Skill | Description | When to Use |
|-------|-------------|-------------|
| **[commit](skills/commit/)** | Commit with formatting, linting, PR | Every commit (`/commit`) |
| **[local-development](skills/local-development/)** | Run API and UI locally | Starting local dev, debugging |
| **[database-operations](skills/database-operations/)** | Connect to PostgreSQL, query data | Database debugging, schema exploration |

### Superpowers Plugin

Install the Superpowers plugin for methodology skills (TDD, systematic debugging, verification):

```bash
claude plugins install superpowers@claude-plugins-official
```

## Tooling

- **uv** for Python version management, virtualenvs, and dependency installs
- **npm** for frontend dependencies
- **Ruff** for Python linting and formatting
- **mypy** for type checking
- Run all checks: `uv run python scripts/ci_check_local.py`
- Run tests: `uv run pytest tests/ -m "not integration" -v`

## Security & Operations

- Secrets live in env vars or secret stores — never commit them
- Use parameterized queries and escape user input
- Apply least-privilege access for tokens/credentials
- Log actionable context (IDs, correlation IDs) at INFO, WARNING for recoverable issues, ERROR for failures
