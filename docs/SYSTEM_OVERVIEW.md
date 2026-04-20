# System Overview

High-level context for the system. Update this document when major changes occur (new integrations, deployment topology changes, architectural shifts).

## What the System Is

<!-- Replace with your application description -->

An AI agent web application that provides conversational AI with tool-use capabilities. Users interact with an AI agent through a chat interface; the agent can invoke tools, access data, and perform actions on the user's behalf.

### Core Capabilities

<!-- List the main things your system does -->

- Conversational AI with streaming responses
- Tool execution (agent can call registered functions)
- Background task processing
- User authentication and session management

## How It's Deployed

<!-- Fill in when you deploy -->

### Infrastructure

| Component | Technology | Location |
|-----------|-----------|----------|
| API Server | FastAPI + Uvicorn | <!-- e.g., Kubernetes pod --> |
| Background Worker | SAQ | <!-- e.g., Kubernetes pod --> |
| Database | PostgreSQL | <!-- e.g., managed instance --> |
| Cache/Queue | Redis | <!-- e.g., managed instance --> |
| Frontend | React (static) | <!-- e.g., CDN / nginx --> |

### Environments

| Environment | URL | Branch |
|-------------|-----|--------|
| Development | <!-- http://localhost:8000 --> | `dev` |
| Production | <!-- https://app.example.com --> | `main` |

### Deployment Pipeline

```
Push to dev -> CI checks -> Build image -> Deploy to dev
Push to main -> Promote image -> Deploy to production
```

## External Integrations

<!-- List all external services the system talks to -->

| Integration | Purpose | Auth Method |
|-------------|---------|-------------|
| Anthropic API | LLM provider (Claude) | API key |
| OpenAI API | LLM provider (GPT) | API key |
| Google OAuth | User authentication | OAuth 2.0 |
| <!-- Add more --> | | |

## Data Flow

### User Interaction

```
Browser -> API (FastAPI) -> Agent Facade -> LLM Provider
                                        -> Tool Execution -> Database
                         <- SSE Stream <- Agent Response
```

### Background Processing

```
API enqueues task -> Redis -> SAQ Worker -> Application Service -> Database
```

### Authentication

```
Browser -> /api/auth/login -> OAuth Provider -> Callback -> JWT issued -> Cookie set
```

## Key Data Stores

| Store | Contains | Retention |
|-------|----------|-----------|
| PostgreSQL | User data, conversations, application state | Permanent |
| Redis | Task queue, session cache | Ephemeral |

## Operational Notes

<!-- Add operational knowledge here as you learn it -->
<!-- Examples:
- Database backups run at 2am UTC via pg_dump cron
- Redis is ephemeral — losing it means in-flight tasks retry
- The SAQ worker must run with concurrency=1 for ordering-sensitive tasks
-->
