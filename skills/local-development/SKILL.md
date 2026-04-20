# Local Development Skill

Run the project locally with hot-reload for development and debugging.

## Trigger

Activated when the user wants to start local development, run the app, or debug locally.

## Full Stack (Docker Compose)

The simplest way to run everything:

```bash
docker compose up
```

This starts:
- **API server** (port 8000) — FastAPI with hot-reload via volume mount
- **SAQ worker** — background task processor
- **PostgreSQL** (port 5432) — application database
- **Redis** (port 6379) — task queue backend

### Frontend (separate terminal)

```bash
cd ui
npm install
npm run dev
```

Frontend dev server runs at http://localhost:5173 with HMR.

## Individual Services

### API Only

```bash
# Start dependencies
docker compose up postgres redis -d

# Run API with hot-reload
uv run uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
```

### SAQ Worker Only

```bash
# Start dependencies
docker compose up postgres redis -d

# Run worker
uv run saq app.saq.worker.settings
```

### Frontend Only

```bash
cd ui
npm run dev
```

Expects the API at http://localhost:8000 (configured in `ui/vite.config.ts` proxy).

## Database Setup

```bash
# Apply migrations
alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "description of change"

# Reset database (destructive)
alembic downgrade base && alembic upgrade head
```

## Environment Variables

Copy `env.example` to `.env`:

```bash
cp env.example .env
```

For local development:
- `DEBUG=true` — enables debug logging and detailed error responses
- `AUTH_PROVIDER=dev` — bypasses real authentication (any email works)
- Database/Redis URLs point to localhost (Docker exposes the ports)

## Common Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8000
# Kill it
kill -9 <PID>
```

### Database Connection Refused

Ensure PostgreSQL is running:
```bash
docker compose up postgres -d
docker compose logs postgres
```

### Redis Connection Refused

```bash
docker compose up redis -d
```

### Migrations Out of Sync

```bash
# Check current state
alembic current

# If multiple heads exist
alembic heads
alembic merge heads -m "merge migration heads"
```

### Frontend Can't Reach API

Check that:
1. API is running on port 8000
2. Vite proxy config in `ui/vite.config.ts` points to `http://localhost:8000`
3. No CORS issues (API should allow localhost origins in dev)

### Hot-Reload Not Working

- **API**: Ensure you're running with `--reload` flag and the source is volume-mounted in Docker
- **UI**: Vite HMR requires the WebSocket connection; check browser console for errors

## Useful Commands During Development

```bash
# Run tests
uv run pytest tests/ -m "not integration" -v

# Run a specific test
uv run pytest tests/test_specific.py::test_function -v

# Check types
uv run mypy --config-file pyproject.toml src/

# Lint and fix
ruff check --fix src/ tests/
ruff format src/ tests/

# Full CI check
uv run python scripts/ci_check_local.py
```
