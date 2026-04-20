# AI Agent Blueprint

**Build AI-powered web applications that work — and keep working as they grow.**

A production-ready starter template for AI agent applications. Clone it, point your AI coding assistant at it, and start building. The blueprint handles the architecture, quality guardrails, and infrastructure so you can focus on your idea.

## Getting Started

The easiest way to use this blueprint is to **tell your AI coding assistant to set it up for you.** If you're using [Claude Code](https://claude.ai/code), [Cursor](https://cursor.com), or a similar AI coding tool, just say:

> "Use https://github.com/chuckconway/ai-agent-blueprint as the template for my new project. Set it up and get it running."

Your AI assistant will read the blueprint, understand the structure, install what's needed, and get everything running. The [CLAUDE.md](CLAUDE.md) file in this repo is specifically designed to give AI assistants all the context they need to work within this project's conventions.

That's the recommended path. Your AI assistant knows how to handle the technical setup so you can focus on what you're building.

If you want to understand what's happening under the hood, or if your AI assistant needs a reference, the full manual setup instructions are below.

<details>
<summary><strong>Manual Setup Instructions</strong> (click to expand)</summary>

### What You'll Need to Install

Before you begin, you'll need a few tools on your computer. If any of these are new to you, don't worry — each link below has step-by-step installation guides for Windows, Mac, and Linux.

| Tool | What It Is | Where to Get It |
|------|-----------|----------------|
| **Git** | Version control — tracks changes to your code so you can undo mistakes and collaborate | [git-scm.com/downloads](https://git-scm.com/downloads) |
| **Docker** | Runs your app and its services (database, cache) in isolated containers so everything works the same on every computer | [docker.com/get-started](https://www.docker.com/get-started/) |
| **Node.js** | Runs the frontend (web interface) development tools. Installing Node.js also installs **npm**, which manages frontend code packages | [nodejs.org](https://nodejs.org/) — download the LTS (Long Term Support) version |
| **Python 3.12+** | The programming language the backend is written in | [python.org/downloads](https://www.python.org/downloads/) |
| **uv** | A fast tool for installing Python packages (similar to pip, but much faster) | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |

### Step 1: Create Your Project

On this GitHub page, click the green **"Use this template"** button near the top of the page, then click **"Create a new repository."** Give your project a name and click **Create repository**.

Now you need to download your new project to your computer. Open a **terminal** (on Mac: search for "Terminal" in Spotlight; on Windows: search for "Command Prompt" or "PowerShell" in the Start menu) and type:

```bash
git clone https://github.com/YOUR-USERNAME/my-project.git
cd my-project
```

Replace `YOUR-USERNAME/my-project` with whatever you named your repository.

### Step 2: Configure Your Settings

Your project needs a few settings — most importantly, an API key for the AI provider you want to use.

**What's an API key?** It's like a password that lets your application talk to an AI service (Claude, GPT, or Gemini). You get one by creating an account with the AI provider:
- **Anthropic (Claude)**: [console.anthropic.com](https://console.anthropic.com/)
- **OpenAI (GPT)**: [platform.openai.com](https://platform.openai.com/)
- **Google (Gemini)**: [aistudio.google.com](https://aistudio.google.com/)

Once you have your API key, run this in your terminal:

```bash
cp env.example .env
```

This creates a settings file called `.env` from the included example. Open `.env` in any text editor (even Notepad works) and fill in:

- **`LLM_PROVIDER`** — which AI to use: `anthropic`, `openai`, or `google`
- **The matching API key** — `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_API_KEY`

Everything else has sensible defaults that work out of the box.

### Step 3: Start the Backend

This one command starts your database, cache, API server, and background worker all at once:

```bash
docker compose up
```

The first time you run this, Docker downloads everything it needs. This can take a few minutes depending on your internet speed. After the first time, it starts in seconds.

You'll see a stream of log messages in the terminal. That's normal — it's showing you what each service is doing. Leave this terminal window open.

### Step 4: Start the Frontend

Open a **second terminal window** (keep the first one running) and type:

```bash
cd my-project/ui
npm install
npm run dev
```

- `npm install` downloads the frontend's code packages. You only need to do this once.
- `npm run dev` starts the web interface development server.

You'll see a message saying the server is running, usually at `http://localhost:5173`.

### Step 5: Open Your App

Open your web browser and go to **http://localhost:5173**

You'll see a login page. Enter:
- **Email**: `dev@example.com`
- **Password**: `dev`

You're in. You'll see a chat interface. Type a message and your AI agent will respond.

### Installing the Superpowers Plugin (Optional)

If you're using [Claude Code](https://claude.ai/code) as your AI coding assistant, the [Superpowers](https://github.com/obra/superpowers) plugin gives your assistant structured workflows for brainstorming, debugging, testing, and code review. To install it, run this in your terminal:

```bash
claude plugins install superpowers@claude-plugins-official
```

This is optional but recommended if you're using Claude Code for development.

</details>

---

## Why This Exists

Building with AI agents is deceptively easy to start and surprisingly hard to sustain. Here's what typically happens:

1. **Day 1**: You get a chat interface working. The AI responds. It feels magical.
2. **Week 2**: You add features. Things start breaking in unexpected ways. The AI agent calls the wrong tool. Responses are slow. You're not sure where to put new code.
3. **Month 2**: The codebase is a maze. Every change breaks something else. You're afraid to deploy. Your AI agent works great in testing and fails in production. Technical debt is piling up faster than features.

This isn't a skill problem — it's a structure problem. Without the right foundations, even experienced engineers end up with fragile, hard-to-change code. And if you're building with AI coding assistants (Claude Code, Cursor, Copilot), the problem compounds: **an AI assistant without guardrails will write working code that slowly becomes unworkable code.**

## What This Blueprint Gives You

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

<details>
<summary><strong>Project Structure</strong> (click to expand)</summary>

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

</details>

<details>
<summary><strong>Tech Stack</strong> (click to expand)</summary>

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

</details>

<details>
<summary><strong>Engineering Practices</strong> (click to expand)</summary>

You don't need to understand these to use the blueprint — they work automatically. But if you're curious about *why* it's structured the way it is:

- **Layered architecture** — Code is organized into layers with strict rules about which layer can talk to which. This prevents the tangled dependencies that make projects unmaintainable.
- **Quality ratchet** — Code quality metrics are tracked and can only improve, never degrade. Every commit leaves the codebase a little better than it found it.
- **Local CI = Remote CI** — The same checks run on your machine before you push and on the server after you push. No surprises.
- **Compound learning** — When you solve a hard problem, the solution is captured so the same mistake never happens twice.
- **Tracer bullets** — Build a thin slice through all layers first, verify it works, then expand. This catches problems early when they're cheap to fix.

These practices are documented in [CLAUDE.md](CLAUDE.md), which your AI coding assistant reads automatically. It follows the rules so you don't have to enforce them manually.

</details>

## Documentation

- **[CLAUDE.md](CLAUDE.md)** — The rules your AI assistant follows. This is the most important file in the project — it's what makes the guardrails work.
- **[ARCHITECTURE.md](ARCHITECTURE.md)** — How the pieces fit together. Read this if you want to understand the system design.
- **[docs/lessons-learned/](docs/lessons-learned/)** — A place to capture debugging insights so the same mistake never happens twice.

## Based On

This blueprint is built from patterns proven in production and documented in the [Agent Engineering Playbook](https://github.com/chuckconway/agent-engineering-playbook).

## License

MIT — use it for anything.
