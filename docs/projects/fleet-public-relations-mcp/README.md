# fleet-public-relations-mcp

[![just](https://img.shields.io/badge/just-works-brightgreen)](https://github.com/casey/just)
[![ruff](https://img.shields.io/badge/ruff-linted-blue)](https://github.com/astral-sh/ruff)
[![python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![fastmcp](https://img.shields.io/badge/fastmcp-3.4%2B-orange)](https://github.com/jlowin/fastmcp)

Private MCP server for fleet public relations outreach -- automated thread monitoring,
LLM competency triage, and `admiral-mcp` escalation.

## Tools

| Tool | Description |
|------|-------------|
| `register_thread` | Start monitoring a forum/Reddit thread URL |
| `get_active_threads` | List all threads under surveillance |
| `scan_threads_now` | Force-trigger scraper + LLM evaluator loop |
| `get_pr_dashboard` | Feedback scores, alert metrics, active discussions |
| `show_pr_dashboard_card` | Rich in-chat Prefab card for the dashboard |
| `fleet_pr_help` | Help and usage reference |
| `fleet_pr_shutdown` | Graceful server shutdown |

## Webapp Dashboard

Port 11095 — Vite + React + Tailwind dashboard with:
- **Dashboard** — KPI cards (threads, comments, high-competency), backend status dot
- **Threads** — list monitored threads, register new URLs, trigger manual scans
- **Feedback** — scored comments table with competency badges
- **Settings** — backend + Ollama status, env var display

Launch: `.\start.bat` (clears ports, starts backend + frontend, opens browser)

## Claude Desktop Config

```json
{
  "mcpServers": {
    "fleet-public-relations-mcp": {
      "command": "uv",
      "args": ["run", "python", "-m", "fleet_public_relations_mcp.server"]
    }
  }
}
```

## Env Vars

| Variable | Default | Description |
|----------|---------|-------------|
| `FLEET_PR_LOG_LEVEL` | `INFO` | Python log level |
| `FLEET_PR_BACKEND_PORT` | `11094` | HTTP server port |
| `FLEET_PR_DATA_DIR` | `data/` | SQLite + log storage |
| `FLEET_PR_SAMPLING_BASE_URL` | `http://localhost:11434/v1` | LLM evaluator endpoint |
| `FLEET_PR_SAMPLING_MODEL` | `qwen3:14b` | Evaluator model name |
| `FLEET_PR_ADMIRAL_URL` | `http://127.0.0.1:11089/api/fleet/alert` | Admiral push target |
| `FLEET_PR_SCRAPE_INTERVAL_MINUTES` | `60` | Background poll interval |

## Stack

- **Backend**: FastMCP 3.4.2+ / Starlette / SQLite
- **Scraper**: httpx + curl_cffi (Cloudflare-resistant)
- **Evaluator**: OpenAI-compatible LLM endpoint (Ollama, vLLM, etc.)
- **Escalation**: `admiral-mcp` HTTP push
- **Frontend**: React 18 / Vite 6 / TailwindCSS / Lucide / Zustand / react-query
