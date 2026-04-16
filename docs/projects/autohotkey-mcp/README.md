# autohotkey-mcp – AutoHotkey Scriptlets MCP Server

**FastMCP 3.1 · Script depot (autohotkey-test) · Sampling-first generation · Fleet SPA (Chat, Running)**

> MCP server for AutoHotkey v2 scriptlets: list, run, stop, source/metadata, running instances; optional AI generation into `scriptlets/ai_generated/`. Uses ScriptletCOMBridge (**10744**) and autohotkey-test as the depot. Backend **10746**, user-facing SPA **10747**.

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\autohotkey-mcp` |
| **Backend port** | **10746** |
| **SPA port** | **10747** (fleet user-facing) |
| **Protocol** | FastMCP 3.1; HTTP `GET /status`, `POST /tool`; stdio when stdin is a pipe (Cursor) |
| **Start** | `uv run autohotkey-mcp`, `.\start.ps1`, **`just run`**, or **`.\web_sota\start.ps1`** (backend + SPA + browser) |
| **Glama** | `glama.json` at repo root (name/version/description) |
| **Depot** | autohotkey-test (`AUTOHOTKEY_SCRIPT_DEPOT`, default `d:/dev/repos/autohotkey-test`) |
| **Bridge** | ScriptletCOMBridge on **10744** (`AUTOHOTKEY_BRIDGE_URL`) |

---

## Tools

- **list_generation_prompts** / **refine_ahk_prompt** – Preset library and prompt refinement (sampling-first).
- **list_scriptlets** / **run_scriptlet** / **stop_scriptlet** – Bridge or direct depot run; optional **pid** for multi-instance stop.
- **list_running_scriptlets** – Running PIDs with depot metadata (`@hotkeys`, `@description`).
- **get_scriptlet_source** / **get_scriptlet_metadata** – Depot file content and headers.
- **generate_scriptlet** – Sandbox generation (sampling + localhost OpenAI-compatible fallback); validation + repair pass.
- **ahk_help** / **show_help** – Markdown help levels and URLs for mini-help vs full SPA.

---

## MCP resources (agents)

- `ahk://prompts/catalog` – Full JSON prompt list.
- `ahk://prompts/categories` – Categories.
- `ahk://prompts/{prompt_id}` – Single entry.

---

## Webapp

- **Pages:** Overview, Help, **Chat** (personas, presets, refine; SSE streaming via `POST /api/chat` + `stream: true`), Scriptlets, **Running** (`GET /api/running`, `POST /api/stop_scriptlet`), Status.
- **Mini-help:** `GET http://127.0.0.1:10746/help` — server-rendered HTML without npm.
- **Health:** `GET http://127.0.0.1:10746/health` (SPA proxies `/health`).

---

## Cursor / RoboFang

- **Standalone repo:** Not under RoboFang `hands/`. Point Cursor MCP or fleet at `http://127.0.0.1:10746` when using HTTP mode.
- **Prerequisites:** ScriptletCOMBridge (e.g. autohotkey-test) for bridge list/run/stop when desired; depot path must contain `scriptlets/`.

---

## Documentation (in repo)

- **README.md** – Config, tools, ports, `just` / Glama.
- **CHANGELOG.md** / **docs/PRD.md** – Product and release notes.
- **Help content** – `src/autohotkey_mcp/help_content.py`.

---

## Fleet

- **Ports:** 10746 (API), 10747 (SPA) — see robofang `docs/standards/WEBAPP_PORTS.md`.
- **Manifest:** Register with backend URL `http://127.0.0.1:10746`, user-facing **10747**.

**Last updated:** 2026-03-20
