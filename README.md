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

Use this template and you get a production-grade application with everything already wired up:

### An AI Agent That Does Things (Not Just Chats)

Most AI demos stop at chat. Real AI applications need agents that can **take actions** — look up data, call APIs, run calculations, interact with your business logic. This blueprint includes:

- **Tool system**: Teach your agent new capabilities by writing a Python function and adding a decorator. That's it.
- **Streaming responses**: Users see the AI thinking and responding in real-time, not staring at a loading spinner.
- **Provider flexibility**: Start with Claude, switch to GPT, try Gemini — change one setting, not your codebase.
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

- **Docker** packages your entire application into a container that runs anywhere
- **Docker Compose** runs everything locally with one command
- **Kubernetes manifests** are included for when you're ready to deploy to production cloud infrastructure

## Who This Is For

- **Builders who work with AI coding assistants** — The guardrails keep your AI assistant productive without letting it create a mess.
- **Developers starting a new AI project** — Skip weeks of infrastructure setup. Start building features on day one.
- **Teams that want consistency** — Every project built from this blueprint follows the same conventions, making it easy to switch between projects or onboard new people.
- **Non-engineers building AI products** — You don't need to be a software engineer to use this. If you can work with an AI coding assistant, the blueprint provides the structure. You bring the ideas.

---

## Getting Started

There are two ways to use this blueprint: **point your AI assistant at it**, or **set it up yourself**. Most people will do the first.

### Option A: Let Your AI Assistant Handle It

If you're working with an AI coding assistant like [Claude Code](https://claude.ai/code), you can simply tell it:

> "Use https://github.com/chuckconway/ai-agent-blueprint as the template for my new project. Set it up and get it running."

Your AI assistant will read the blueprint, understand the structure, and set everything up for you. The [CLAUDE.md](CLAUDE.md) file in this repo is specifically designed to give AI assistants all the context they need to work within this project's conventions.

### Option B: Set It Up Yourself

If you prefer to set things up manually, here's what you need and how to get started.

#### What You'll Need to Install

| Tool | What It Is | Where to Get It |
|------|-----------|----------------|
| **Git** | Version control — tracks changes to your code | [git-scm.com/downloads](https://git-scm.com/downloads) |
| **Docker** | Runs your app and its services (database, cache) in containers | [docker.com/get-started](https://www.docker.com/get-started/) |
| **Node.js** | Runs the frontend development tools (includes npm) | [nodejs.org](https://nodejs.org/) — download the LTS version |
| **Python 3.12+** | The backend programming language | [python.org/downloads](https://www.python.org/downloads/) |
| **uv** | Fast Python package manager (replaces pip) | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |

Don't worry if some of these are unfamiliar. Each link has installation instructions for Windows, Mac, and Linux.

#### Step by Step

**1. Create your project from this template**

On this GitHub page, click the green **"Use this template"** button near the top, then **"Create a new repository."** Give it a name and create it.

Then open a terminal and download your new project:

```bash
git clone https://github.com/YOUR-USERNAME/my-project.git
cd my-project
```

Replace `YOUR-USERNAME/my-project` with the name you chose.

**2. Set up your configuration**

Your project needs a few settings — most importantly, an API key for the AI provider you want to use (Anthropic for Claude, OpenAI for GPT, or Google for Gemini).

```bash
cp env.example .env
```

This creates a `.env` file from the example template. Open it in any text editor and fill in at least:
- `LLM_PROVIDER` — which AI to use (`anthropic`, `openai`, or `google`)
- The matching API key (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY`)

Everything else has sensible defaults.

**3. Start the backend**

This one command starts your database, cache, API server, and background worker:

```bash
docker compose up
```

The first run downloads everything it needs, which takes a few minutes. After that, it starts in seconds.

**4. Start the frontend** (in a separate terminal window)

```bash
cd ui
npm install
npm run dev
```

`npm install` downloads the frontend dependencies (you only need to do this once). `npm run dev` starts the development server.

**5. Open your app**

Go to **http://localhost:5173** in your browser. You'll see a login page. Enter:
- Email: `dev@example.com`
- Password: `dev`

You're in. Start chatting with your AI agent.

#### Installing the Superpowers Plugin (Optional but Recommended)

If you're using [Claude Code](https://claude.ai/code) as your AI coding assistant, install the [Superpowers](https://github.com/obra/superpowers) plugin. It gives your assistant structured workflows for brainstorming, debugging, testing, and code review:

```bash
claude plugins install superpowers@claude-plugins-official
```

---

## What You'll Customize

The blueprint is opinionated but not rigid. Here's what you'll change as you build your product:

| What | Where | Example |
|------|-------|---------|
| Add agent capabilities | `src/app/agent/example_tools.py` | "Look up a customer", "Send an email", "Query our database" |
| Add pages | `ui/src/features/` | Dashboard, settings, admin panel |
| Add data models | `src/app/core/models/` | Products, orders, documents — whatever your app needs |
| Add API endpoints | `src/app/api/routes/` | New endpoints for your frontend |
| Add background jobs | `src/app/worker/tasks/` | Nightly reports, data sync, document processing |
| Switch authentication | `.env` → `AUTH_PROVIDER=google` | Google sign-in for real users |
| Switch AI provider | `.env` → `LLM_PROVIDER=openai` | Change with one line, no code changes |

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

## Tech Stack

For those who want the specifics:

| Layer | What It Does | Technology |
|-------|-------------|-----------|
| **API** | Handles web requests, authentication | Python, FastAPI |
| **Agent** | AI orchestration, tool calling, streaming | Agno SDK (supports Anthropic, OpenAI, Google) |
| **Database** | Stores your application data | PostgreSQL, SQLAlchemy |
| **Task Queue** | Background job processing | SAQ with Redis |
| **Frontend** | The web interface your users see | React, TypeScript, Tailwind CSS |
| **Quality** | Automated code checks | 18 tools that run silently before every commit |
| **CI/CD** | Automated testing and deployment | GitHub Actions, Docker |
| **Deployment** | Running in production | Docker Compose or Kubernetes |

## Engineering Practices

You don't need to understand these to use the blueprint — they work automatically. But if you're curious about *why* it's structured the way it is:

- **Layered architecture** — Code is organized into layers with strict rules about which layer can talk to which. This prevents the tangled dependencies that make projects unmaintainable.
- **Quality ratchet** — Code quality metrics are tracked and can only improve, never degrade. Every commit leaves the codebase a little better than it found it.
- **Local CI = Remote CI** — The same checks run on your machine before you push and on the server after you push. No surprises.
- **Compound learning** — When you solve a hard problem, the solution is captured so the same mistake never happens twice.
- **Tracer bullets** — Build a thin slice through all layers first, verify it works, then expand. This catches problems early when they're cheap to fix.

These practices are documented in [CLAUDE.md](CLAUDE.md), which your AI coding assistant reads automatically. It follows the rules so you don't have to enforce them manually.

## Documentation

- **[CLAUDE.md](CLAUDE.md)** — The rules your AI assistant follows. This is the most important file in the project — it's what makes the guardrails work.
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — How the pieces fit together. Read this if you want to understand the system design.
- **[docs/lessons-learned/](docs/lessons-learned/)** — A place to capture debugging insights so the same mistake never happens twice.

## Based On

This blueprint is built from patterns proven in production and documented in the [Agent Engineering Playbook](https://github.com/chuckconway/agent-engineering-playbook).

## License

MIT — use it for anything.
