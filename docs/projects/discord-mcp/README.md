# discord-mcp — Discord REST bridge (FastMCP 3.1)

**Central project documentation** for **discord-mcp** in MCP Central Docs.  
**Local clone:** `D:/Dev/repos/discord-mcp`

| Doc in this folder | Purpose |
|--------------------|---------|
| [README.md](./README.md) (this file) | Ports, transports, fleet links |
| [STATUS.md](./STATUS.md) | Maturity, features |
| [STRUCTURE.md](./STRUCTURE.md) | Layout vs central standards |
| [INTEGRATION.md](./INTEGRATION.md) | Cursor, starts launcher, Glama |

---

## What it is

**discord-mcp** exposes a **Discord bot** (REST API v10) to MCP hosts via:

- **Stdio** — Cursor / Claude Desktop (`discord`, `discord_help`, `discord_agentic_workflow`).
- **HTTP** — **Backend 10756:** REST `/api/v1/…`, OpenAPI `/docs`, MCP **streamable HTTP** at **`/mcp`**. **Frontend 10757:** Vite dashboard (proxy `/api` → 10756).

Stack: **FastMCP 3.1** (instructions, sampling handler, skills, prompts, resource `resource://discord-mcp/capabilities`), **python-dotenv** for repo-root `.env`, **LanceDB** optional RAG (`rag_ingest` / `rag_query`), **httpx** with **Discord 429** retry.

---

## Quick reference

| Item | Value |
|------|--------|
| Backend | `http://127.0.0.1:10756` — REST + **`/mcp`** |
| Dashboard | `http://127.0.0.1:10757` |
| Health | `GET /api/v1/health` |
| Meta | `GET /api/v1/meta` |
| Starts (fleet) | `mcp-central-docs/starts/discord-start.bat` |
| Fleet ports doc | [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) |
| Registry | [webapp-registry.json](../../operations/webapp-registry.json) (`discord-mcp-backend`, `discord-mcp-frontend`) |

Canonical technical detail: **source repo** `discord-mcp/docs/TECHNICAL.md` and `discord-mcp/docs/README.md` (next to the code).

---

## Standards alignment

- [AGENT_PROTOCOLS.md](../../standards/AGENT_PROTOCOLS.md), [SOTA_REQUIREMENTS.md](../../standards/SOTA_REQUIREMENTS.md)
- [WEBAPP_STANDARDS.md](../../standards/WEBAPP_STANDARDS.md) — ports **10756/10757**, `start.ps1`
- [starts/README.md](../../starts/README.md) — launcher pattern (symlink caveat; discord uses relative `cd`)
