# AI Agent Blueprint

A production-ready starter template for AI agent web applications. This blueprint provides a layered architecture with FastAPI, React, SQLAlchemy, and SAQ — pre-configured for AI agent development with tool use, streaming responses, and background task processing. Designed for AI-assisted development with Claude Code.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI, Pydantic, Uvicorn |
| Agent | Provider-agnostic adapters (Anthropic, OpenAI), SSE streaming |
| Database | PostgreSQL, SQLAlchemy 2.0 (async), Alembic |
| Task Queue | SAQ (Redis-backed) |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, Zustand |
| Testing | pytest, Jest, React Testing Library |
| CI | Ruff, mypy, ESLint, ci-checks.json |

## Quick Start

### 1. Clone

```bash
git clone <repository-url>
cd ai-agent-blueprint
```

### 2. Install Superpowers (Claude Code plugin)

```bash
claude plugins install superpowers@claude-plugins-official
```

### 3. Configure Environment

```bash
cp env.example .env
# Edit .env with your API keys and database credentials
```

### 4. Start Services

```bash
docker compose up
```

This starts:
- **API server** at http://localhost:8000 (with hot-reload)
- **SAQ worker** for background tasks
- **PostgreSQL** database
- **Redis** for task queue

### 5. Start the Frontend (separate terminal)

```bash
cd ui
npm install
npm run dev
```

Frontend available at http://localhost:5173.

### 6. Run Migrations

```bash
alembic upgrade head
```

### 7. Login

Navigate to http://localhost:5173. With `AUTH_PROVIDER=dev`, log in with `dev@example.com` / `dev`.

## Project Structure

```
src/app/
  api/          # HTTP routes, middleware, auth
  agent/        # AI agent orchestration, tools, streaming
  core/         # Domain logic, models, repositories, services
  worker/       # Background task worker (SAQ)

ui/             # React frontend
migrations/     # Alembic database migrations
scripts/        # Dev tooling (CI runner, code health)
skills/         # Claude Code skill definitions
k8s/            # Kubernetes deployment manifests
docs/           # System overview, plans, lessons learned
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed layer descriptions and data flow diagrams.

## Available Commands

```bash
# Run all CI checks locally
uv run python scripts/ci_check_local.py

# Run with auto-fix
uv run python scripts/ci_check_local.py --fix

# Run tests
uv run pytest tests/ -m "not integration" -v

# Lint and format
ruff check src/ tests/
ruff format src/ tests/

# Type check
uv run mypy --config-file pyproject.toml src/

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"

# Frontend
cd ui && npm run dev      # Dev server
cd ui && npm run lint     # ESLint
cd ui && npx tsc --noEmit # Type check
```

## Documentation

- [CLAUDE.md](CLAUDE.md) — Project rules and conventions (read by AI agents)
- [ARCHITECTURE.md](ARCHITECTURE.md) — Package map, layers, data flow
- [docs/SYSTEM_OVERVIEW.md](docs/SYSTEM_OVERVIEW.md) — Deployment and integration context
- [docs/lessons-learned/](docs/lessons-learned/) — Debugging insights and patterns

## Development Workflow

This project uses **worktree-based isolation** for all development. Each task gets its own worktree branched from `dev`. See the Branch Isolation section in [CLAUDE.md](CLAUDE.md) for details.

Commits use the `/commit` skill which runs the full CI suite locally before pushing.

## License

MIT
