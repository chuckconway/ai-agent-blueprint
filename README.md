# AI Agent Blueprint

**Build AI-powered web applications that work — and keep working as they grow.**

You have an idea for an AI-powered app. Maybe it's a customer support agent, a research assistant, a content generator, or something nobody's built yet. You know AI can do incredible things. But between "I have an idea" and "I have a working product," there's a canyon of infrastructure decisions, architectural patterns, and engineering practices that can make or break your project.

This blueprint bridges that canyon.

## The Problem

Building with AI agents is deceptively easy to start and surprisingly hard to sustain. Here's what typically happens:

1. **Day 1**: You get a chat interface working. The AI responds. It feels magical.
2. **Week 2**: You add features. Things start breaking in unexpected ways. The AI agent calls the wrong tool. Responses are slow. You're not sure where to put new code.
3. **Month 2**: The codebase is a maze. Every change breaks something else. You're afraid to deploy. Your AI agent works great in testing and fails in production. Technical debt is piling up faster than features.

This isn't a skill problem — it's a structure problem. Without the right foundations, even experienced engineers end up with fragile, hard-to-change code. And if you're building with AI coding assistants (Claude Code, Cursor, Copilot), the problem compounds: **an AI assistant without guardrails will write working code that slowly becomes unworkable code.**

## What This Blueprint Gives You

Clone this template and you get a production-grade application with everything already wired up:

### An AI Agent That Does Things (Not Just Chats)

Most AI demos stop at chat. Real AI applications need agents that can **take actions** — look up data, call APIs, run calculations, interact with your business logic. This blueprint includes:

- **Tool system**: Teach your agent new capabilities by writing a Python function and adding a decorator. That's it.
- **Streaming responses**: Users see the AI thinking and responding in real-time, not staring at a loading spinner.
- **Provider flexibility**: Start with Claude, switch to GPT, try Gemini — change one environment variable, not your codebase.
- **Interceptor pipeline**: Add logging, content filtering, or usage tracking without touching your agent logic.

### Quality Guardrails That Run Automatically

This is where the blueprint pays for itself. When you're building with AI coding assistants, the assistant doesn't inherently know your project's rules. It will write code that works *right now* but violates patterns that matter *over time*. The blueprint includes **18 automated checks** that run before every commit:

- **Code formatting and style** — enforced automatically, not by code review arguments
- **Type safety** — catches bugs before they reach production
- **Architecture enforcement** — prevents the spaghetti code that makes projects unmaintainable
- **Dead code detection** — keeps the codebase lean
- **Quality ratchet** — code quality can only improve over time, never degrade

Here's the thing: **you don't need to understand any of these tools.** They run silently in the background. If your AI assistant tries to write code that breaks the rules, the checks catch it and the assistant fixes it before you ever see it. It's like having a senior engineer reviewing every line, 24/7.

**Without these guardrails**, AI-assisted code tends to accumulate shortcuts — unused imports, untyped functions, circular dependencies, overly complex logic. Each one is small. Together, after a few months, they make the codebase hostile to change. The blueprint prevents that drift from day one.

### A Web Application, Not Just a Backend

You get a complete, working application:

- **Login page** → authenticate → **Chat interface** → talk to your AI agent
- Built with React, TypeScript, and Tailwind CSS — the same stack used by most modern web applications
- Mobile-friendly, dark theme, clean design
- Ready to extend with your own pages and features

### A Database and Background Jobs

Most AI apps need to remember things and do work in the background. Included:

- **PostgreSQL** for storing users, conversations, and your application data
- **Safe database changes** — a migration system that lets you update your database without breaking your running application
- **Background task queue** — for long-running operations that shouldn't block a user's request (sending emails, processing documents, calling slow APIs)

### Deployment-Ready Infrastructure

When you're ready to go live:

- **Docker** — package your entire application into a container that runs anywhere
- **Docker Compose** — run everything locally with one command (`docker compose up`)
- **Kubernetes manifests** — deploy to production cloud infrastructure when you're ready to scale

## Who This Is For

- **Builders who work with AI coding assistants** — The guardrails keep your AI assistant productive without letting it create a mess.
- **Developers starting a new AI project** — Skip weeks of infrastructure setup. Start building features on day one.
- **Teams that want consistency** — Every project built from this blueprint follows the same conventions, making it easy to switch between projects or onboard new people.
- **Non-engineers building AI products** — You don't need to be a software engineer to use this. If you can work with an AI coding assistant, the blueprint provides the structure. You bring the ideas.

## Quick Start

### 1. Create Your Project

Click **"Use this template"** on GitHub, or:

```bash
gh repo create my-project --template chuckconway/ai-agent-blueprint --public
cd my-project
```

### 2. Configure

```bash
cp env.example .env
# Open .env and add your API key (Anthropic, OpenAI, or Google)
```

### 3. Install Development Tools

```bash
claude plugins install superpowers@claude-plugins-official
```

This installs [Superpowers](https://github.com/obra/superpowers), a development methodology plugin that gives your AI assistant structured workflows for brainstorming, debugging, testing, and code review.

### 4. Start Everything

```bash
docker compose up
```

This launches your database, cache, API server, and background worker.

### 5. Start the Frontend

```bash
cd ui
npm install
npm run dev
```

### 6. Open Your App

Navigate to **http://localhost:5173**. Log in with `dev@example.com` / `dev`. Start chatting with your AI agent.

That's it. You have a working AI application.

## What You'll Customize

The blueprint is opinionated but not rigid. Here's what you'll change as you build your product:

| What | Where | Example |
|------|-------|---------|
| Add agent tools | `src/app/agent/example_tools.py` | "Look up a customer", "Send an email", "Query our database" |
| Add pages | `ui/src/features/` | Dashboard, settings, admin panel |
| Add data models | `src/app/core/models/` | Products, orders, documents, whatever your app needs |
| Add API endpoints | `src/app/api/routes/` | REST endpoints for your frontend |
| Add background jobs | `src/app/worker/tasks/` | Nightly reports, data sync, document processing |
| Switch auth | `.env` → `AUTH_PROVIDER=google` | Google OAuth for real users |
| Switch AI provider | `.env` → `LLM_PROVIDER=openai` | Change with one line, no code changes |

## Tech Stack

For those who want the specifics:

| Layer | Technology |
|-------|-----------|
| API | Python, FastAPI, Pydantic, Uvicorn |
| Agent | Agno SDK, provider-agnostic adapters (Anthropic, OpenAI, Google) |
| Database | PostgreSQL, SQLAlchemy 2.0 (async), Alembic migrations |
| Task Queue | SAQ (Redis-backed), background workers |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS v4, Zustand |
| Quality | Ruff, mypy, import-linter, radon, vulture, deptry |
| Testing | pytest, Jest, React Testing Library |
| CI/CD | GitHub Actions, Gitea Actions, Docker |
| Deployment | Docker Compose (local/simple), Kubernetes (production) |

## Project Structure

```
src/app/
  api/          # Web endpoints, authentication, request handling
  agent/        # AI agent: tools, streaming, provider adapters
  core/         # Your business logic, data models, database
  worker/       # Background tasks and scheduled jobs

ui/             # React web application
migrations/     # Database schema changes
scripts/        # Quality checks and development tools
skills/         # AI assistant workflow definitions
k8s/            # Production deployment manifests
docs/           # Architecture docs, lessons learned
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed descriptions of each layer and how data flows through the system.

## Engineering Practices (For the Curious)

You don't need to understand these to use the blueprint, but if you're interested in *why* it's structured the way it is:

- **Layered architecture** — Code is organized into layers with strict rules about which layer can talk to which. This prevents the tangled dependencies that make projects unmaintainable.
- **Quality ratchet** — Code quality metrics are tracked and can only improve, never degrade. Every commit leaves the codebase a little better than it found it.
- **Local CI = Remote CI** — The same checks run on your machine before you push and on the server after you push. No surprises.
- **Compound learning** — When you solve a hard problem, the solution is captured in `docs/lessons-learned/` so the same mistake never happens twice.
- **Tracer bullets** — Build a thin slice through all layers first, verify it works, then expand. This catches architecture problems early when they're cheap to fix.

These practices are documented in [CLAUDE.md](CLAUDE.md), which your AI coding assistant reads automatically. It follows the rules so you don't have to enforce them manually.

## Commands Reference

```bash
# Run all quality checks
uv run python scripts/ci_check_local.py

# Auto-fix issues then validate
uv run python scripts/ci_check_local.py --fix

# Run tests
uv run pytest tests/ -m "not integration" -v

# Database migrations
alembic upgrade head                            # Apply changes
alembic revision --autogenerate -m "add orders" # Create new migration

# Frontend
cd ui && npm run dev      # Development server
cd ui && npm run lint     # Check for issues
cd ui && npx tsc --noEmit # Type check
```

## Documentation

- [CLAUDE.md](CLAUDE.md) — The rules your AI assistant follows (the most important file in the project)
- [ARCHITECTURE.md](ARCHITECTURE.md) — How the pieces fit together
- [docs/SYSTEM_OVERVIEW.md](docs/SYSTEM_OVERVIEW.md) — Deployment and integration context
- [docs/lessons-learned/](docs/lessons-learned/) — Captured debugging insights and patterns

## Based On

This blueprint is built from patterns proven in production at [Conway's Personal Assistant](https://github.com/chuckconway/pa) and the [Agent Engineering Playbook](https://github.com/chuckconway/agent-engineering-playbook). The AI agent infrastructure is inspired by [DCAF](https://github.com/chuckconway/dcaf) (DuploCloud Agent Framework).

## License

MIT — use it for anything.
