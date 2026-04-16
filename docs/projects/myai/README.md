# MyAI Platform

**By FlowEngineer sandraschi**

Dual-mode AI microservices platform that ships a FastAPI control plane, an MCP server with production-grade tooling, and a fleet of AI applications orchestrated with Docker, Traefik, and a full monitoring stack.

---

## ðŸ“Œ Highlights
- **FastAPI Dashboard (port 3060)** with service lifecycle management, health probes, and MCP orchestration.
- **MCP Server (FastMCP 3.1.1++)** exposing eleven operational tools with comprehensive docstrings and portmanteau patterns.
- **Thirteen AI microservices** (LLM chat, document RAG, Gemini multimodal suite, Stable Diffusion, talking avatar, **HunyuanWorld 3D modeling**, **Wan2.2 video generation**, etc.) following a shared service contract.
- **Infrastructure-ready Docker Compose** including Traefik, Prometheus, Grafana, Loki, Portainer, PostgreSQL, Weaviate, and GPU workloads.
- **Security first**: non-root containers, read-only Docker socket, API key enforcement, strict CORS, and resource limits across the stack.

---

## ðŸ—ï¸ Architecture Overview

```
myai/
â”œâ”€â”€ core/
â”‚   â”œâ”€â”€ dashboard/        # FastAPI app + MCP server + service APIs
â”‚   â”œâ”€â”€ llm_integration/  # Shared LLM adapters (Ollama, vLLM, Gemini, etc.)
â”‚   â”œâ”€â”€ logging_system/   # Central logging configuration & helpers
â”‚   â””â”€â”€ monitoring/       # Prometheus/Grafana/Loki provisioning
â”œâ”€â”€ projects/
â”‚   â”œâ”€â”€ bob_and_alice/        # Multi-persona LLM chat (5188)
â”‚   â”œâ”€â”€ character_conversation/# Role-based ensemble chat (5190)
â”‚   â”œâ”€â”€ document_viewer/      # Document RAG + Weaviate (5192)
â”‚   â”œâ”€â”€ future_you/           # Future self simulator (5194)
â”‚   â”œâ”€â”€ stablediff_gradio/    # Stable Diffusion UI (5196)
â”‚   â”œâ”€â”€ talking_avatar/       # Voice + animation (5198, GPU)
â”‚   â”œâ”€â”€ teams_debate/         # Multi-agent debate (5200/5201)
â”‚   â”œâ”€â”€ gemini_tools/         # Google Gemini multimodal suite (5206)
â”‚   â”œâ”€â”€ plex_plus/            # Plex AI extensions (3020/3001)
â”‚   â””â”€â”€ calibre_plus/         # Calibre AI extensions (8000/9000)
â”œâ”€â”€ docker-compose.yml        # Full platform orchestration (18+ services)
â”œâ”€â”€ docs/                     # Standards, patterns, status reports
â””â”€â”€ scripts/                  # Diagnostics, maintenance, automation
```

Traefik fronts user traffic, while internal services communicate over the `ai-network` bridge. Monitoring agents collect metrics/logs for every container, feeding the Grafana dashboards that ship with the repo.

---

## ðŸ”¢ Service Matrix

| Service | Description | Tech Stack | Ports |
| --- | --- | --- | --- |
| Dashboard | Control plane + MCP server + REST API | FastAPI, FastMCP, Uvicorn | 3060 |
| Bob & Alice | Character conversation playground | FastAPI, React, Ollama/vLLM | 5188 |
| Character Conversation | Role-rotating dialogue engine | FastAPI, Workers, LLM adapters | 5190 |
| Document Viewer | AI-powered document RAG | FastAPI, Weaviate, React | 5192 |
| Future You | Time-capsule LLM experience | FastAPI, React | 5194 |
| StableDiff Gradio | Image generation UI | Gradio, Diffusers | 5196 |
| Talking Avatar | Voice + animation pipeline | FastAPI, TTS, GPU runtime | 5198 |
| Teams Debate | Multi-agent debate | FastAPI, Celery | 5200 (API) / 5201 (ws) |
| Gemini Tools | Google Gemini multimodal suite | FastAPI, React, Google AI APIs | 5206 (API) / 3501 (UI) |
| HunyuanWorld Bridge | Interactive 3D world modeling | FastAPI, React, Tencent HunyuanWorld 1.5 | 5202 |
| Wan2.2 Video Bridge | Advanced video generation | FastAPI, React, Alibaba Wan2.2 MoE models | 5218 |
| Plex Plus | Plex AI extensions | FastAPI, React, PostgreSQL | 3001 (API) / 3020 (UI) |
| Calibre Plus | Calibre AI assistant | FastAPI, React, PostgreSQL | 9000 (API) / 8000 (UI) |

Supporting infrastructure: Traefik (80/8080), Prometheus (9091), Grafana (3100), Loki (3199), Portainer (9001), Weaviate (8081), PostgreSQL (5432 internal), vLLM GPU workloads, and HunyuanWorld model volumes.

---

## ðŸš€ Getting Started

### Prerequisites
- Docker Engine 24+
- Docker Compose v2
- Python 3.11 (for CLI utilities)
- Node.js 18+ (only if rebuilding React frontends)
- NVIDIA GPU + drivers (for talking_avatar, stablediff_gradio, vLLM)

### Clone & Configure
```powershell
git clone https://github.com/your-org/myai.git
cd myai
Copy-Item .env.example .env           # update secrets/API keys
Copy-Item core/dashboard/config.sample.json core/dashboard/config.json
```

### Run the Platform
```powershell
docker compose pull                 # optional: fetch latest images
docker compose up -d                # start dashboard, microservices, monitoring
docker compose ps                   # verify all containers are healthy
```

### Verify
- Dashboard UI: http://localhost:3060
- Grafana monitoring: http://localhost:3100 (default creds in docs/monitoring/)
- Traefik dashboard (if enabled): http://localhost:8080
- MCP server: configure Claude Desktop with `python core/dashboard/mcp_server.py`

Stop everything with `docker compose down` (add `-v` to wipe volumes).

---

## ðŸ§‘â€ðŸ’» Development Workflows

### Dashboard + MCP Server
```powershell
cd core/dashboard
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py                      # serves FastAPI dashboard on 3060
python mcp_server.py                # run MCP server (stdio)
```
Lint, format, and type-check before committing:
```powershell
ruff check core/dashboard/
ruff format core/dashboard/
pyright core/dashboard/
```

### Microservice
```powershell
cd projects/<service>
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Ensure `core/dashboard/config.json` and `docker-compose.yml` stay in sync when changing ports.

### Docker Builds (Optimized)
Use smart caching for fast incremental builds:
```powershell
# Fast build (code changes only) - 2-5 seconds
.\scripts\docker-build.ps1

# Quick update (build + restart)
.\scripts\docker-update.ps1

# Single service update
.\scripts\docker-update.ps1 -Service dashboard

# Full rebuild (when dependencies change) - 90-185 seconds
.\scripts\docker-build.ps1 -NoCache
```
**Performance**: Regular builds are 18-90x faster than `--no-cache` for code-only changes. See `scripts/DOCKER_BUILD_GUIDE.md` for details.

### React Frontends (Gemini Tools, Plex Plus, Calibre Plus)
```powershell
cd projects/<service>/ui
npm install
npm run dev         # or npm run build for production bundle
```

---

## ðŸ“ˆ Monitoring & Operations
- **Prometheus** scrapes application metrics at `http://localhost:9091`.
- **Grafana** dashboards are preloaded under `monitoring/grafana/`. Import them after the first startup.
- **Loki + Promtail** centralize logs (`docker compose logs -f` for raw output).
- **Portainer** (`http://localhost:9001`) provides a UI for Docker hosts.
- **Health Endpoints**: each service exposes `/health` or `/api/health`; the dashboard aggregates everything at `/api/v1/health/status`.

---

## ðŸ” Security Baselines
- Containers run as non-root (`user: 1000:999`), and the Docker socket is mounted read-only (`/var/run/docker.sock:ro`).
- Dashboard APIs require `DASHBOARD_API_KEY` via the `X-API-Key` header (see `core/dashboard/main.py`).
- CORS is locked to known origins (3060, 3020, 8000); never widen to `*`.
- Secrets live in `.env` and service-specific settings. Never commit credentials.
- GPU services auto-detect devices; disable or tighten access if GPUs are unavailable.

---

## ðŸ“š Documentation Map
- `docs/MCP_SERVER_DEVELOPMENT_PATTERNS.md` â€“ FastMCP 3.1.1++ tool standards and portmanteau patterns.
- `docs/HUNYUANWORLD_TECHNICAL_INTEGRATION.md` â€“ Complete technical guide to HunyuanWorld 1.5 integration, architecture, performance, and comparison with WorldLabs.ai.
- `docs/WAN2.2_TECHNICAL_INTEGRATION.md` â€“ Complete technical guide to Wan2.2 video generation integration, MoE architecture, multi-modal capabilities, and performance benchmarks.
- `docs/MYAI_STATUS_REPORT_*.md` â€“ weekly status, service health, improvement targets.
- `docs/monitoring/` â€“ Prometheus, Grafana, Loki configuration and dashboards.
- `docs/tools-reference.md` â€“ MCP tool catalog.
- `docs/integration-guide.md` (todo) â€“ Claude Desktop integration recipe for the MCP server.

---

## ðŸ¤ Contributing
1. Follow MCP docstring and error-handling requirements (50+ lines per tool, structured error returns).
2. Run `ruff`, `pyright`, and relevant unit tests before opening PRs.
3. Update `CHANGELOG.md` and docs when behaviour or configuration changes.
4. Coordinate major service additions via `docs/MYAI_STATUS_REPORT_*` and central standards.

---

## ðŸ†˜ Support
- Platform questions: open issues in this repo.
- MCP standards: `D:\Dev\repos\mcp-central-docs\STANDARDS.md`.
- Incidents & hotfixes: track in `docs-private/` (git-ignored) and propagate summaries to `docs/`.

---

Built for production-ready AI experimentation with rock-solid operational guardrails. Enjoy exploring the platform!


## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx myai-start
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "myai-start": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/myai", "run", "myai-start"]
  }
}
```

