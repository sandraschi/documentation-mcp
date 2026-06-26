# KiCad MCP — Changelog

## v0.3.0 (2026-05-29)

### Added — Hybrid install + headless IPC CRUD

- Hybrid KiCad routing: **stable 10.x** (`KICAD_CLI_PATH`) for exports/DRC/ERC; **11 nightly** (`KICAD_IPC_CLI_PATH`) for headless PCB CRUD via `kicad-python` / `kipy`
- Modules: `kicad_install.py`, `ipc_backend.py`, `crud_router.py`, `scripts/probe_ipc_headless.py`
- Optional PyPI extra: `uv sync --extra ipc` installs `kicad-python>=0.7`
- Env: `KICAD_MCP_CRUD_BACKEND` (`auto`|`ipc`|`tcp`|`none`), `KICAD_MCP_IPC_ENABLED`
- Doc: `docs/NIGHTLY_HEADLESS.md` (repo) + fleet mirror `HYBRID_INSTALL.md`
- Tests: CLI discovery + CRUD router (14 pytest total)
- Cursor/fleet MCP config: `--extra ipc`, hybrid env vars in `MASTER_MCP_CONFIG.json`

### Changed

- `crud_backend` replaces `bridge_mode` as primary status field (`bridge_mode` kept as alias)
- `kicad_status` exposes both CLI paths, IPC capability flags, active backend
- PCB mutating tools use CRUD router (IPC preferred over TCP bridge in `auto` mode)
- Webapp dashboard/status API surfaces hybrid install state
- Version bump 0.2.0 → 0.3.0

### Partial / upcoming in v0.3.x

- `pcb_place_component` via IPC library API (still TCP-only today)
- IPC export lane deferred — manufacturing exports stay on stable kicad-cli

## v0.2.0 (2026-05-25)