# Beyond Compare MCP (fleet project page)

**Repo:** `D:/Dev/repos/beyondcompare-mcp`  
**Canonical technical doc (next to code):** `beyondcompare-mcp/docs/FLEET_GATEWAY.md` — update **both** when ports, env vars, or HTTP paths change.

## One-line summary

MCP server driving **Scooter Beyond Compare** for file/folder compare and sync, plus multimedia and dev-workspace tools — now with a **FastMCP 3.2.x unified gateway** (FastAPI + MCP in one process), REST health/capabilities/logs, MCP prompts, a **skill** resource, and **agentic** sampling tools.

## Ports

| Port | Role |
|------|------|
| **10840** | Vite dashboard (`web_sota`); dev server proxies `/api` and `/mcp` to **10841** |
| **10841** | Production-style gateway: **uvicorn** on the FastAPI app (REST + MCP streamable, default path `/mcp`) |

Env: `MCP_HOST`, `MCP_PORT`, `MCP_PATH`, `BEYOND_COMPARE_PATH`, `BC_SCRIPTS_DIR`, `OLLAMA_BASE_URL`.

## Start (development)

```powershell
# Terminal 1 — gateway
cd D:\Dev\repos\beyondcompare-mcp
uv run python -m beyondcompare_mcp.server --http --port 10841

# Terminal 2 — UI
cd D:\Dev\repos\beyondcompare-mcp\web_sota
npm run dev
```

Browse: `http://127.0.0.1:10840`. Health for probes: `http://127.0.0.1:10841/api/v1/health`.

## REST (fleet automation)

- `GET /api/v1/health` — process + BC executable detection + uptime  
- `GET /api/capabilities` — tool names and endpoint map  
- `GET /api/v1/logs` — recent gateway request ring  
- `GET|POST /api/v1/llm/settings`, `GET /api/v1/llm/models` — in-process prefs + Ollama tag list  

## MCP

- **13** legacy atomic tools (compare, sync, multimedia, repo utilities).  
- **Prompts:** `beyondcompare_quick_start`, `beyondcompare_backup_sync`, `beyondcompare_multimedia_inventory`.  
- **Resource:** `skill://beyondcompare-mcp/SKILL.md`.  
- **Agentic:** `beyondcompare_agentic_workflow` (uses `Context.sample` when the host supports SEP-1577), `beyondcompare_sampling_hint`.

## Packaging

MCPB manifest includes new tools and `prompts_generated: true`. Pack from the repo root with your standard `mcpb` workflow.

## Tests

Repo: `just test` or `uv run python -m pytest tests -q --ignore=tests/test_integration.py`. Gateway coverage: `tests/test_gateway.py`.

## Related fleet files

- `mcp-central-docs/projects/FLEET_INDEX.md` — table row for this repo  
- `mcp-central-docs/operations/WEBAPP_PORTS.md` — port table  
- `mcp-central-docs/operations/fleet-registry.json` — machine-readable entry  
- `mcp-central-docs/scripts/fleet-webapp-manifest.json` — health path must match **`/api/v1/health`**
