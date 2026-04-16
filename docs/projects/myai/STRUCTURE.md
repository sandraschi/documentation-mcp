# myai - Directory Structure

**Last Updated:** 2025-11-25  
**Source Repo:** `D:\Dev\repos\myai`

---

## Top-Level Layout

```
myai/
â”œâ”€â”€ core/
â”‚   â”œâ”€â”€ dashboard/          # FastAPI app + MCP server (port 3060)
â”‚   â”‚   â”œâ”€â”€ main.py         # FastAPI backend
â”‚   â”‚   â”œâ”€â”€ mcp_server.py   # MCP server (11 tools, FastMCP 3.1.1++)
â”‚   â”‚   â”œâ”€â”€ mcp_orphan_guard.py  # Zombie process prevention
â”‚   â”‚   â”œâ”€â”€ api/            # API routes (v1 structure)
â”‚   â”‚   â”œâ”€â”€ services/       # Business logic & MCP client
â”‚   â”‚   â”œâ”€â”€ static/         # Frontend assets (JS/CSS)
â”‚   â”‚   â””â”€â”€ templates/      # HTML templates (Jinja2)
â”‚   â”œâ”€â”€ llm_integration/    # LLM backend abstraction (Ollama, vLLM, etc.)
â”‚   â”œâ”€â”€ logging_system/     # Centralized logging
â”‚   â””â”€â”€ monitoring/         # Prometheus/Grafana/Loki configs
â”œâ”€â”€ projects/               # 10 AI microservices
â”‚   â”œâ”€â”€ bob_and_alice/      # AI dialogue (5188)
â”‚   â”œâ”€â”€ character_conversation/  # Multi-persona chat (5190)
â”‚   â”œâ”€â”€ document_viewer/    # PDF/doc analysis + Weaviate (5192)
â”‚   â”œâ”€â”€ future_you/         # Time capsule chat (5194)
â”‚   â”œâ”€â”€ stablediff_gradio/  # Image generation (5196, GPU)
â”‚   â”œâ”€â”€ talking_avatar/     # Voice + animation (5198, GPU)
â”‚   â”œâ”€â”€ teams_debate/       # Multi-AI debate (5200/5201)
â”‚   â”œâ”€â”€ gemini_tools/       # Google AI suite (5206/3501)
â”‚   â”œâ”€â”€ plex_plus/          # Media + AI (3020/3001)
â”‚   â””â”€â”€ calibre_plus/       # Ebook + AI (8000/9000)
â”œâ”€â”€ docker-compose.yml      # All services orchestration
â”œâ”€â”€ docs/                   # Documentation
â”œâ”€â”€ scripts/                # Maintenance & build scripts
â””â”€â”€ .cursorrules            # Cursor IDE rules
```

---

## Core Components

### Dashboard (`core/dashboard/`)
- **main.py** - FastAPI app, service management APIs
- **mcp_server.py** - MCP server with 11 tools
- **mcp_orphan_guard.py** - Prevents zombie processes
- **config.json** - Service configurations

### Microservice Pattern (`projects/{service}/`)
```
projects/{service}/
â”œâ”€â”€ app.py or main.py    # Service entry point
â”œâ”€â”€ Dockerfile           # Container definition
â”œâ”€â”€ requirements.txt     # Python dependencies
â”œâ”€â”€ frontend/            # React/vanilla JS (if split)
â”œâ”€â”€ backend/             # FastAPI/Flask backend (if split)
â””â”€â”€ README.md            # Service documentation
```

---

## Port Scheme

| Range | Purpose | Examples |
|-------|---------|----------|
| 3xxx | Frontends/Special | Dashboard 3060, Plex UI 3020 |
| 5xxx | AI Services | Bob&Alice 5188, DocViewer 5192 |
| 8xxx-9xxx | Split Backends | Calibre 8000/9000 |
| 3100/9xxx | Monitoring | Grafana 3100, Prometheus 9191 |


