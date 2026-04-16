# Meta MCP Enterprise 🚀

**MetaMCP Enterprise** is the complete **"Argh-Coding" bloop-buster** — a comprehensive enterprise-grade management platform for MCP (Model Context Protocol) ecosystems.

**Version**: 3.2.1 (SOTA Compliant, FastMCP 3.1+) — canonical narrative lives in the repo: `D:/Dev/repos/meta_mcp` ([README](file:///D:/Dev/repos/meta_mcp/README.md), [CHANGELOG](file:///D:/Dev/repos/meta_mcp/CHANGELOG.md)).

## Fleet ports (web)

Registered in [operations/WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md):

| Port | Role |
|------|------|
| **10718** | Backend (FastAPI, REST, `/mcp`, static `web_sota/dist` when built) |
| **10719** | Vite dev (`web_sota`; proxies `/api` → 10718) |

Set `PORT` / `HOST` when running `uv run meta-mcp` to match fleet.

## Recent platform notes (2026-03)

- **Tool Lab** (`web_sota`): Sidebar page — pick any registered tool, JSON Schema form or raw JSON, run via **`POST /api/v1/tools/execute`**.
- **Catalog API**: **`GET /api/v1/mcp/catalog`** — tool names + parameter schemas for the UI.
- **`meta_dev` suite**: Fleet probes, `MASTER_MCP_CONFIG` snippets, diffs, audits — see repo [docs/tools/meta-dev.md](file:///D:/Dev/repos/meta_mcp/docs/tools/meta-dev.md).
- **Automation**: Repo root **`justfile`** (`just sync`, `just fix`, `just web-build`, `just tools`, …).
- **Lint**: Ruff in dev dependency group; `uv run ruff check src` / `uv run ruff format src`.

## 🎯 The Mission

We prevent developer pain points:

- **Unicode** logging crashes (EmojiBuster / safe scanning)
- **Docker** confusion and miswired transports
- **Framework** assumption errors (FastMCP 3.1+ alignment)
- **MCPB** packaging friction

## 🏗️ Core capabilities (modular suites)

See the repo [docs/tools/README.md](file:///D:/Dev/repos/meta_mcp/docs/tools/README.md) — includes **scheduler**, **heartbeat**, **meta_dev**, and the standard domains (server management, tool execution, diagnostics, toolchains, scaffolding, …).

## Quick start (clone)

```bash
cd D:/Dev/repos/meta_mcp
uv sync --group dev
uv run meta-mcp
# Optional: PORT=10718 HOST=127.0.0.1
```

Frontend dev:

```bash
cd web_sota
npm install
npm run dev
# Opens 10719 → proxies API to 10718
```

## Documentation (repo)

- [README.md](file:///D:/Dev/repos/meta_mcp/README.md) (short), [docs/README.md](file:///D:/Dev/repos/meta_mcp/docs/README.md) (index)
- [docs/INSTALL.md](file:///D:/Dev/repos/meta_mcp/docs/INSTALL.md), [docs/ARCHITECTURE.md](file:///D:/Dev/repos/meta_mcp/docs/ARCHITECTURE.md), [docs/TOOLS.md](file:///D:/Dev/repos/meta_mcp/docs/TOOLS.md)
- [docs/tools/README.md](file:///D:/Dev/repos/meta_mcp/docs/tools/README.md), [docs/tools/meta-dev.md](file:///D:/Dev/repos/meta_mcp/docs/tools/meta-dev.md)
- [CHANGELOG.md](file:///D:/Dev/repos/meta_mcp/CHANGELOG.md), [PRD.md](file:///D:/Dev/repos/meta_mcp/PRD.md), [STANDARDS.md](file:///D:/Dev/repos/meta_mcp/STANDARDS.md)

## License

MIT — see upstream repo.
