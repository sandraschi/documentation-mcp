# Documentation MCP

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://fastmcp.com"><img src="https://img.shields.io/badge/FastMCP-3.4-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

Documentation server with semantic search, RAG, fleet registry, and a React dashboard.
Indexes the full fleet corpus for cross-repo document retrieval and learning.

**Ports:** Frontend `11032` · Backend (FastAPI + MCP) `11033`

---

## Learning paths

New to MCP? Follow one of these paths from first page to last.

| Path | Start | Goal |
|------|-------|------|
| **📖 MCP fundamentals** | `docs/getting-started/` → `docs/protocol/` → `docs/fastmcp/` | Build your first server |
| **⚙️ Fleet standards** | `docs/core/` → `docs/standards/` → `docs/patterns/` | Ship production-grade servers |
| **🛡️ Safety & hardening** | `docs/safety/` → `docs/troubleshooting/` → `docs/deployment/` | Secure, reliable deployments |
| **🔌 Integrations** | `docs/ecosystem/` → `docs/integrations/` → `docs/monitoring/` | Connect IDEs, tools, observability |
| **🏗️ Fleet tour** | `docs/projects/` (pick a repo) → `docs/reference/` → `docs/operations/` | Understand the 136+ repo fleet |

**Not sure where to start?** Read `docs/getting-started/` first — it assumes nothing.

## Quick start

```powershell
uv sync
cd web_sota && npm install && cd ..
./start.ps1
```

Opens at `http://localhost:11032`.

## Documentation library

Every major directory has a `README.md` acting as a chapter introduction:

| Directory | What you'll learn |
|-----------|------------------|
| [`docs/getting-started/`](docs/getting-started/) | MCP concepts, first server in 5 minutes |
| [`docs/protocol/`](docs/protocol/) | Transports, JSON-RPC, capability negotiation |
| [`docs/fastmcp/`](docs/fastmcp/) | FastMCP 3.x: tools, resources, prompts, skills |
| [`docs/core/`](docs/core/) | Fleet standards bar: repo layout, packaging, ports |
| [`docs/standards/`](docs/standards/) | Detailed standards: tool design, webapps, CORS, security |
| [`docs/patterns/`](docs/patterns/) | Reusable architecture: portmanteau, orphan guard, CORS |
| [`docs/safety/`](docs/safety/) | AI security: prompt injection, guardrails, CVEs |
| [`docs/ecosystem/`](docs/ecosystem/) | IDE integration: Cursor, Zed, Claude Desktop, Antigravity |
| [`docs/integrations/`](docs/integrations/) | External services: LLMs, media, home automation, robotics |
| [`docs/projects/`](docs/projects/) | Fleet repo index: README, STATUS, PRD for every server |
| [`docs/reference/`](docs/reference/) | Glossary, acronyms, dev notebook, tool reference |
| [`docs/troubleshooting/`](docs/troubleshooting/) | Bug depot, debugging playbooks, common fixes |
| [`docs/deployment/`](docs/deployment/) | Production deployment, security hardening |
| [`docs/monitoring/`](docs/monitoring/) | Observability stack: Grafana, Loki, Prometheus |
| [`docs/operations/`](docs/operations/) | Port registry, control plane, fleet ops |
| [`docs/skills/`](docs/skills/) | Agent skills: assess-and-fix, fleet-doctor, ship |

## Stack

| Layer | Tech |
|-------|------|
| Backend | FastMCP 3.4, FastAPI, uvicorn, SQLite, LanceDB |
| Frontend | React 18, Vite, Tailwind, Zustand, Framer Motion |
| LLM | Ollama / OpenAI-compatible (auto-discovery) |
| Desktop | Tauri 2.0, NSIS installer, PyInstaller backend |
| CI | Ruff, Biome, tsc, pytest (GitHub Actions) |

## Quick reference

- **Search the docs**: `http://localhost:11032` → Search page
- **RAG chat**: Chat page with Ollama auto-discovery
- **Fleet apps**: Dashboard → Apps Hub
- **Reindex**: Settings → Reindex or call `reindex_docs` tool
- **MCP for IDEs**: `uv run documentation-mcp` (stdio) or `MCP_TRANSPORT=http` (HTTP)
