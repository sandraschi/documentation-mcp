# KiCad MCP — Project Page

**Status**: Active development — hybrid IPC path landed in v0.3.0  
**Version**: 0.3.0  
**Updated**: 2026-05-29  
**Repo**: `D:\Dev\repos\kicad-mcp`  
**GitHub**: `https://github.com/sandraschi/kicad-mcp`  
**Fleet docs**: `D:\Dev\repos\mcp-central-docs\projects\kicad-mcp\`

## What It Is

KiCad MCP is a FastMCP 3.2 server for AI-driven PCB/schematic automation on KiCad EDA.
It exposes **39 MCP tools** across 6 categories for inspection, manufacturing export,
and live board editing.

As of **v0.3.0**, the server supports a **hybrid KiCad install** on Windows:

| Lane | KiCad | Binary env | Purpose |
|------|-------|------------|---------|
| **Export** | 10.0.x stable | `KICAD_CLI_PATH` | Gerber, STEP, DRC/ERC, BOM, library CLI, schematic exports |
| **CRUD** | 11.x dev nightly | `KICAD_IPC_CLI_PATH` | Headless PCB load/save, tracks, vias via `kicad-cli api-server` + `kicad-python` |
| **Legacy fallback** | 10 GUI | TCP :11018 | `kc_bridge.py` SWIG bridge when nightly/IPC unavailable |

See **[HYBRID_INSTALL.md](./HYBRID_INSTALL.md)** (fleet mirror of repo `docs/NIGHTLY_HEADLESS.md`).

## Execution Architecture (v0.3.0)

```
MCP / REST tool call
    │
    ├─ Export / DRC / ERC / library / schematic CLI
    │      └─ stable kicad-cli subprocess (10.x)
    │
    └─ PCB CRUD (load, info, tracks, vias, save, outline)
           ├─ IPC headless (11 nightly + kipy)     ← preferred in auto mode
           ├─ TCP kc_bridge (KiCad 10 GUI)       ← legacy fallback
           └─ none (export-only; CRUD tools error with guidance)
```

Backend selection env: `KICAD_MCP_CRUD_BACKEND=auto|ipc|tcp|none`.

## Key Infrastructure

| Component | Port | Technology |
|-----------|------|------------|
| Backend | 11016 | FastAPI + FastMCP 3.2 |
| Frontend | 11017 | Vite 6 + React 19 + Tailwind 3.4 |
| KiCad Bridge (legacy) | 11018 | TCP JSON-RPC (pcbnew SWIG in GUI) |
| IPC api-server | ephemeral | Child of nightly `kicad-cli` (headless) |

## Tool Surface

| Category | Count | Tools |
|----------|-------|-------|
| PCB | 17 | load, info, list components/nets/tracks, get component, DRC, export (STEP/Gerber/POS/DXF/SVG/PDF/VRML/GLB/IPC-2581/ODB++), place component, add track/via, save, set board outline |
| Schematic | 8 | load, info, ERC, export (netlist/BOM/PDF/SVG/DXF) |
| BOM | 1 | grouped JSON/CSV generation |
| Library | 6 | list/search footprints/symbols, fp/sym SVG export |
| Marketplace | 5 | search GitHub/Kitspace/SnapEDA, download, find parts |
| System | 2 | status, supported commands |

CRUD tools (place, track, via, save, outline) require `crud_backend` of `ipc` or `tcp`.
Read/export tools work on stable CLI alone.

## Cursor MCP Configuration

Active entry in `C:\Users\sandr\.cursor\mcp.json` (2026-05-29):

```json
"kicad-mcp": {
  "command": "C:/Users/sandr/.local/bin/uv.exe",
  "args": [
    "--directory", "D:/Dev/repos/kicad-mcp",
    "run", "--extra", "ipc",
    "python", "-m", "kicad_mcp.server", "--mode", "stdio"
  ],
  "cwd": "D:/Dev/repos/kicad-mcp",
  "env": {
    "PYTHONUNBUFFERED": "1",
    "FASTMCP_BANNER": "0",
    "FASTMCP_UPDATE_CHECK": "0",
    "KICAD_CLI_PATH": "C:/Program Files/KiCad/10.0/bin/kicad-cli.exe",
    "KICAD_IPC_CLI_PATH": "C:/Program Files/KiCad/11.0/bin/kicad-cli.exe",
    "KICAD_MCP_CRUD_BACKEND": "auto",
    "KICAD_MCP_IPC_ENABLED": "auto"
  }
}
```

Fleet canonical copy: `mcp-central-docs/operations/MASTER_MCP_CONFIG.json` (`kicad-mcp` key).

**Before CRUD works:** install KiCad 11 nightly, run `uv sync --extra ipc`, verify with:

```powershell
Set-Location D:\Dev\repos\kicad-mcp
uv run python -m kicad_mcp.scripts.probe_ipc_headless
```

On Sandra's machine (2026-05-29): stable **10.0.3** detected; IPC nightly **not yet installed** — export lane works; `crud_backend` will be `none` until nightly + kipy are present.

## Webapp Frontend

9 pages: Dashboard (hybrid status KPIs), PCB (+ 3D GLB), Schematic (+ SVG), BOM,
Library, Marketplace, Files, Demo (12-step pipeline), Status.

## Fleet Standards Compliance

| Standard | Status |
|----------|--------|
| Port allocation (10700-11500) | ✅ 11016/17/18 registered |
| Hybrid KiCad documented | ✅ NIGHTLY_HEADLESS + fleet HYBRID_INSTALL |
| MASTER_MCP_CONFIG entry | ✅ v0.3.0 hybrid env |
| Playwright e2e tests | ✅ 12 tests |
| pytest unit tests | ✅ 14 tests (incl. install + router) |
| FastMCP 3.2 + stdio | ✅ |
| Optional ipc extra | ✅ kicad-python |
| llms.txt | ✅ updated v0.3.0 |

## KiCad Version Support (updated 2026-05-29)

| KiCad | kicad-cli export | pcbnew SWIG | IPC (GUI) | Headless IPC (api-server) | kicad-mcp lane |
|-------|------------------|-------------|-----------|---------------------------|----------------|
| 10.0.x stable | ✅ production | ✅ deprecated | ✅ | ❌ | **Export default** |
| 11.x nightly | ✅ experimental | ❌ removed | ✅ | ✅ | **CRUD default (when installed)** |
| 11.0 stable (~Jan 2027) | ✅ | ❌ | ✅ | ✅ | Target production CRUD |

## Related Fleet Projects

- **freecad-mcp** — enclosure design from STEP exports
- **qcad-mcp** — DXF/STL mechanical path
- **chip-design-mcp** — broader EDA/CAD orchestration (see chip_design_cad_sota.md)

## Documentation Index

| Doc | Location |
|-----|----------|
| Hybrid install (detailed) | `kicad-mcp/docs/NIGHTLY_HEADLESS.md` |
| Fleet hybrid mirror | [HYBRID_INSTALL.md](./HYBRID_INSTALL.md) |
| Cursor MCP | [CURSOR_MCP.md](./CURSOR_MCP.md) |
| Status | [STATUS.md](./STATUS.md) |
| Changelog | [CHANGELOG.md](./CHANGELOG.md) |
| PRD | [PRD.md](./PRD.md) |
