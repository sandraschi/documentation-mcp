# KiCad MCP — Status

**As of:** 2026-05-29  
**Current version:** 0.3.0  
**Status:** Active development. Hybrid IPC path implemented; nightly install pending on dev machine.

## Current State

FastMCP 3.2 server + FastAPI backend + Vite/React frontend + **three-lane KiCad integration**:

1. **Stable export lane** — `KICAD_CLI_PATH` → KiCad 10.0.3 on this machine ✅
2. **Headless IPC CRUD lane** — `KICAD_IPC_CLI_PATH` → 11 nightly + `kicad-python` ⚠️ code ready; nightly not installed yet
3. **Legacy TCP bridge** — `kc_bridge.py` on port 11018 when KiCad GUI is open

### Infrastructure

- **Backend FastAPI:** `http://localhost:11016/api/*`
- **FastMCP MCP/SSE:** `http://localhost:11016/mcp` + `/sse`
- **Frontend Vite:** `http://localhost:11017`
- **KiCad Bridge TCP (legacy):** `127.0.0.1:11018`
- **Work directory:** `%TEMP%\kicad_mcp_work` (uploads/, outputs/)
- **GitHub:** `https://github.com/sandraschi/kicad-mcp`

### Stdio transport (Cursor)

```powershell
uv sync --extra ipc
uv run python -m kicad_mcp.server --mode stdio
```

Configured in `C:\Users\sandr\.cursor\mcp.json` with hybrid env vars (see [CURSOR_MCP.md](./CURSOR_MCP.md)).

### Probe hybrid install

```powershell
Set-Location D:\Dev\repos\kicad-mcp
uv run python -m kicad_mcp.scripts.probe_ipc_headless
```

Expected on this machine today:

| Check | Result |
|-------|--------|
| Stable CLI | `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` (10.0.3) |
| IPC CLI + api-server | Not found until 11 nightly installed |
| kicad-python (kipy) | Install via `uv sync --extra ipc` |
| `crud_backend` at runtime | `none` until IPC lane complete; exports still work |

## Tool Surface

39 FastMCP 3.2 tools — unchanged count; CRUD routing improved in v0.3.0.

### CRUD backend selection (`auto`)

```
IPC CLI + api-server + kipy  →  crud_backend = ipc
else TCP bridge on :11018    →  crud_backend = tcp
else                         →  crud_backend = none (export-only)
```

Override: `KICAD_MCP_CRUD_BACKEND=ipc|tcp|none`.

## Recent Releases

- **v0.3.0 (2026-05-29):** Hybrid KiCad install, headless IPC backend, CRUD router,
  `kicad_install.py`, probe script, optional `ipc` extra, fleet + Cursor MCP config,
  expanded docs, 14 pytest tests
- **v0.2.0 (2026-05-25):** Full kicad-cli export coverage, PCB CRUD via TCP bridge,
  demo page, 3D viewer, KiCad 10.0, Tauri wrapper
- **v0.1.1 (2026-05-25):** Port migration, Playwright e2e, CI/CD
- **v0.1.0 (2026-05-23):** Initial release

## Roadmap

1. ~~**IPC API integration**~~ — **v0.3.0 basic headless CRUD** ✅
2. **Full `pcb_place_component` via IPC** — library footprint API on nightlies
3. **Schematic CRUD** — S-expression file editing (no eeschema API)
4. **Interactive routing** — push-and-shove via IPC when stable
5. **Zone/pour operations** — copper zones via IPC
6. **Retire TCP bridge default** — after KiCad 11.0 stable + proven headless path

## Known Issues

- **Nightly required for headless CRUD.** Stable 10.0.3 has no `api-server` subcommand.
- **File format risk.** Saving with 11 nightly may upgrade board format beyond 10.0.3 — use copies.
- **`pcb_place_component` IPC** not wired; use TCP bridge or wait for next release.
- **Schematic:** still no Python API; export-only via kicad-cli.
- **Marketplace:** GitHub rate limits, SnapEDA API key optional.

## Repositories

- Main: `D:\Dev\repos\kicad-mcp`
- Fleet docs: `D:\Dev\repos\mcp-central-docs\projects\kicad-mcp\`
- Public: `https://github.com/sandraschi/kicad-mcp`

---

*Status maintained by Sandra Schipal. Updated 2026-05-29 for v0.3.0 hybrid IPC.*
