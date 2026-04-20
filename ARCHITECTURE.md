# Architecture

## Directory Layout

```
src/
  app/
    api/                    # HTTP layer — FastAPI routes, middleware, auth
      core/                 # Shared API infrastructure (schemas, exceptions, routing)
      routes.py             # Top-level router registry
      features/             # Feature-specific route modules
    agent/                  # AI agent layer — orchestration, tools, streaming
      adapters/             # LLM provider adapters (Anthropic, OpenAI, etc.)
      facade.py             # Single entry point for agent interactions
      interceptors/         # Request/response pipeline hooks
      streaming.py          # SSE streaming implementation
      tools/                # Agent-callable tool definitions
    core/                   # Domain layer — business logic, models, infrastructure
      application/          # Application services (use-case orchestration)
      database/             # SQLAlchemy models, repositories, migrations
        models/             # ORM models
        repositories/       # Data access repositories
        unit_of_work.py     # Transaction management
      config.py             # App configuration
      exceptions.py         # Domain exception hierarchy
      task_queue/           # Task queue interface (provider-agnostic)
    saq/                    # SAQ worker — background tasks, cron jobs
      config.py             # Queue definitions, DEFAULT_JOB_TIMEOUT
      tasks/                # Task implementations
      worker.py             # Worker startup and settings

ui/                         # Frontend — React + TypeScript + Vite
  src/
    features/               # Feature slices (components, hooks, stores, API)
    shared/                 # Shared components, services, utilities
      components/ui/        # Reusable UI components
      services/api.ts       # HTTP client (all API calls go through here)
    App.tsx                 # Root component
    main.tsx                # Entry point

migrations/                 # Alembic migrations
  versions/                 # Migration files

scripts/                    # Dev tooling
  ci_check_local.py         # Local CI runner
k8s/                        # Kubernetes manifests
docker-compose.yml          # Local development stack
```

## Layer Responsibilities

### API Layer (`app.api`)

- HTTP request/response handling
- Authentication and authorization middleware
- Request validation (Pydantic schemas)
- Error mapping (domain exceptions -> HTTP status codes)
- Route registration

**May import**: `app.agent`, `app.core`

### Agent Layer (`app.agent`)

- LLM provider communication via adapters
- Tool registration and execution
- Conversation orchestration
- Response streaming (SSE)
- Request/response interceptors

**May import**: `app.core`
**Must not import**: `app.api`

### Core Layer (`app.core`)

- Domain models and business logic
- Application services (use-case orchestration)
- Repository interfaces and implementations
- Database models and unit of work
- Domain exceptions
- Configuration

**Must not import**: `app.api`, `app.agent`

### SAQ Layer (`app.saq`)

- Background task definitions
- Cron job scheduling
- Worker configuration

**May import**: `app.core`
**Must not import**: `app.api`

## Data Flow

### Synchronous Request

```
Client
  |
  v
FastAPI Route (app.api)
  |  - validates input (Pydantic)
  |  - extracts auth context
  v
Application Service (app.core.application)
  |  - owns transaction boundary (UoW)
  |  - orchestrates domain logic
  v
Repository (app.core.database)
  |  - data access, flush (not commit)
  v
Database (PostgreSQL)
```

### Agent Interaction (Streaming)

```
Client (SSE connection)
  |
  v
FastAPI Route (app.api)
  |
  v
Agent Facade (app.agent.facade)
  |  - applies interceptors
  |  - selects adapter
  v
LLM Adapter (app.agent.adapters)
  |  - streams tokens from provider
  |  - executes tools as needed
  v
Tool Functions (app.agent.tools)
  |  - call application services
  v
Application Service (app.core.application)
  |
  v
SSE Stream -> Client
```

### Background Task

```
Application Service
  |  - enqueues task with timeout
  v
Redis Queue
  |
  v
SAQ Worker (app.saq)
  |  - picks up task
  |  - calls application service
  v
Application Service (app.core.application)
```

## Import Rules

Enforced by `import-linter` in `pyproject.toml`:

```
app.api  ->  app.agent  ->  app.core
              app.saq   ->  app.core
```

- Lower layers CANNOT import from higher layers
- `app.core` is the foundation — no upward dependencies
- `app.agent` and `app.saq` are peers at the middle layer
- `app.api` is the outermost layer

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `lazy="raise"` on all relationships | Prevents N+1 queries; forces explicit data loading |
| Unit of Work pattern | Single transaction boundary per use case; repositories don't commit |
| Provider-agnostic agent adapters | Swap LLM providers without touching business logic |
| SSE for streaming | Simple, HTTP-native, works through proxies; no WebSocket complexity |
| SAQ over Celery | Async-native, lightweight, Redis-only; fits single-team projects |
| Feature-slice UI architecture | Co-location reduces cognitive load; features are self-contained |
| Expand/contract migrations | Zero-downtime deployments; safe rollbacks |
| `ci-checks.json` as source of truth | Same checks run locally and in CI; no drift |
