# opencode-cli-mcp

**Type:** MCP Server + Webapp  
**Status:** Active — Functional Skeleton  
**Version:** 0.1.0  
**Ports:** Frontend **10950** / Backend **10951** / opencode serve **4096**  
**Repo:** `D:\Dev\repos\opencode-cli-mcp`  
**GitHub:** https://github.com/sandraschi/opencode-cli-mcp  
**Last assessed:** 2026-05-01

---

## Description

MCP server wrapping the [opencode](https://opencode.ai/) agentic coding CLI (`opencode serve`) into FastMCP tools. Lets Claude Desktop delegate complex multi-file coding tasks to the opencode agent as a subprocess or via its HTTP session API. Includes a FastAPI REST bridge and a Vite/React/Tailwind dashboard.

Sibling to `goose-mcp` (same pattern, different upstream CLI).

---

## Architecture

```
Claude Desktop
  └── FastMCP server (opencode-cli-mcp)
        └── OpencodeClient (httpx → opencode serve :4096)
FastAPI backend (:10951)
  ├── /api/opencode/*  proxy to opencode serve
  ├── /api/fleet       TCP-probe fleet ports
  ├── /api/system      psutil metrics
  └── /api/tools       tool catalogue
Vite frontend (:10950)  proxies /api → :10951
```

---

## MCP Tools (9)

| Tool | Purpose |
|------|---------|
| `opencode_run_agent` | Run agent non-interactively via `opencode run` (300s timeout) |
| `opencode_list_sessions` | List active/recent sessions |
| `opencode_get_session` | Get session metadata and state |
| `opencode_export_session` | Export session as JSON |
| `opencode_send_message` | Continue conversation in a session |
| `opencode_get_messages` | Retrieve message history |
| `opencode_server_status` | Health + session count + config |
| `opencode_list_providers` | List configured LLM providers |
| `opencode_get_project` | Get active project context |

Prompt: `agent_instructions` — workflow guide for LLM consumers.

---

## Start

```powershell
# All-in-one
.\start.ps1

# Manual
uv run -m opencode_cli_mcp.server   # MCP server
uv run -m api.main                   # FastAPI backend :10951
cd web_sota && npm run dev           # Vite frontend :10950
```

Requires `opencode` CLI installed: `npm i -g opencode-ai`

---

## Known Issues (as of 2026-05-01)

See `docs/ASSESSMENT.md` for full detail.

**P1:**
- `fleet.py` port→label map hardcoded, covers only 8/85 ports, will drift — needs to read from `mcp-central-docs` canonical source
- `ensure_server()` never called — tools will throw raw exceptions if opencode isn't running
- GPU detection uses deprecated `wmic` — replace with `Get-CimInstance`

**P2:**
- `opencode_run_agent` uses blocking `subprocess.run` — should be `asyncio.create_subprocess_exec`
- `/api/tools` hardcodes the tool list — will diverge silently

**P3:**
- `asyncio_mode = "auto"` missing from `pyproject.toml` — async pytest may fail
- `start.ps1` zombie-kill pattern needs audit

---

## Stack

| Component | Version |
|-----------|---------|
| Python | 3.13 |
| fastmcp | 3.2.4 |
| fastapi | 0.136.1 |
| starlette | 1.0.0 |
| pydantic | 2.13.3 |
| httpx | 0.28.1 |
| React | 18.3.1 |
| Vite | 5.4.x |
| Tailwind | 3.4.x |
| Zustand | 4.5.4 |

---

## Tags

`[opencode-cli-mcp, fastmcp, agent-orchestration, coding-agent, active, webapp]`
