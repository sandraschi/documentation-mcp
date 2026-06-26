# KiCad MCP — Hybrid Install (Fleet Mirror)

**Canonical source:** `D:\Dev\repos\kicad-mcp\docs\NIGHTLY_HEADLESS.md`  
**Version:** kicad-mcp 0.3.0 (2026-05-29)  
**Audience:** Fleet operators, Cursor MCP config, CI agents

This page mirrors the repo guide for mcp-central-docs discovery. When the repo doc and this file diverge, **trust the repo file** and update this mirror on the next fleet doc pass.

---

## Summary

Run **two KiCad installs** on the same Windows machine:

| Role | Version | Path (Sandra dev machine) | Env var |
|------|---------|---------------------------|---------|
| Export / DRC / ERC | 10.0.3 stable | `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` | `KICAD_CLI_PATH` |
| Headless PCB CRUD | 11.x nightly | `C:\Program Files\KiCad\11.0\bin\kicad-cli.exe` (after install) | `KICAD_IPC_CLI_PATH` |

Python side:

```powershell
Set-Location D:\Dev\repos\kicad-mcp
uv sync --extra ipc
```

---

## Routing diagram

```
                    kicad-mcp MCP tool
                           │
           ┌───────────────┴───────────────┐
           │                               │
    Export / inspect lane            PCB CRUD lane
    (always prefer 10.x)             (auto pick)
           │                               │
           ▼                               ▼
   KICAD_CLI_PATH                  crud_router.py
   subprocess kicad-cli                  │
   Gerber STEP DRC ERC              ┌────┴────┐
                                   ▼         ▼
                              ipc (11+)   tcp (:11018)
                              kipy        kc_bridge GUI
```

---

## Environment variables

| Variable | Default | Values | Purpose |
|----------|---------|--------|---------|
| `KICAD_CLI_PATH` | auto: highest stable without `api-server` | path to `kicad-cli.exe` | Manufacturing exports, DRC, ERC, library CLI |
| `KICAD_IPC_CLI_PATH` | auto: nightly with `api-server` | path to nightly `kicad-cli.exe` | Spawns headless `api-server` for IPC |
| `KICAD_MCP_CRUD_BACKEND` | `auto` | `auto`, `ipc`, `tcp`, `none` | Force or disable CRUD backend |
| `KICAD_MCP_IPC_ENABLED` | `auto` | `auto`, `1`, `0` | Hard disable IPC even if nightly present |
| `KC_BRIDGE_PORT` | `11018` | port | Legacy TCP bridge |

Discovery implementation: `kicad-mcp/src/kicad_mcp/kicad_install.py`.

---

## Install KiCad 11 nightly (one-time)

1. [KiCad Windows nightlies](https://downloads.kicad.org/kicad/windows/explore/nightlies) — download full x64 installer.
2. Install beside 10.0, e.g. `C:\Program Files\KiCad\11.0\`.
3. Verify:

```powershell
& "C:\Program Files\KiCad\11.0\bin\kicad-cli.exe" version
& "C:\Program Files\KiCad\11.0\bin\kicad-cli.exe" api-server --help
```

Help text must mention **headless** IPC api-server. If missing, download a newer nightly build.

**Do not uninstall KiCad 10.0.3.**

Nightlies use separate `%APPDATA%\kicad\<version>\` settings — they do not clobber 10.0 config.

---

## Verify kicad-mcp hybrid stack

```powershell
Set-Location D:\Dev\repos\kicad-mcp
uv sync --extra ipc
uv run python -m kicad_mcp.scripts.probe_ipc_headless
uv run pytest tests -q
```

Call MCP tool `kicad_status` after Cursor restart. Expected when fully configured:

| Field | Expected |
|-------|----------|
| `kicad_cli_path` | 10.0 stable path |
| `kicad_ipc_cli_path` | 11 nightly path |
| `ipc_api_server` | `true` |
| `ipc_python_installed` | `true` |
| `crud_backend` | `ipc` |

**Current machine state (2026-05-29):** stable 10.0.3 only — `crud_backend` stays `none` until nightly + kipy installed. Exports still work.

---

## CRUD capability matrix (v0.3.0)

| Tool | IPC headless | TCP bridge | Stable CLI only |
|------|:------------:|:----------:|:---------------:|
| pcb_load, pcb_info, list * | ✅ | ✅ | partial |
| pcb_get_component | ✅ | ✅ | ❌ |
| pcb_add_track, pcb_add_via | ✅ | ✅ | ❌ |
| pcb_save, pcb_set_board_outline | ✅ / ⚠️ | ✅ | ❌ |
| pcb_place_component | ❌ (v0.3.0) | ✅ | ❌ |
| pcb_drc, all pcb_export_* | — | fallback | ✅ preferred |

DRC and all manufacturing exports intentionally stay on **stable** `KICAD_CLI_PATH`.

---

## File format warning

Boards saved by KiCad 11 nightly may use a format **newer than 10.0.3**.

- Keep production golden projects on 10.x until 11.0 stable (~Jan 2027).
- Agent work should use **copies** under `%TEMP%\kicad_mcp_work\uploads\`.
- Never overwrite the only production `.kicad_pcb` without backup.

---

## Troubleshooting quick reference

| Symptom | Fix |
|---------|-----|
| `crud_backend: none`, exports OK | Install 11 nightly + `uv sync --extra ipc` |
| `No module named 'kipy'` | `uv sync --extra ipc` |
| `api-server` not found | Nightly too old or wrong binary in `KICAD_IPC_CLI_PATH` |
| protobuf / check_version errors | Upgrade nightly installer + `uv pip install --upgrade kicad-python` |
| Need place_component now | Open KiCad 10 GUI, run `kc_bridge.py`, set `KICAD_MCP_CRUD_BACKEND=tcp` |
| IPC session stuck | Restart MCP server (kills api-server child) |

API log (optional): `%APPDATA%\kicad\<version>\logs\api.log` with `EnableAPILogging=1` in kicad advanced settings.

---

## Module map (implementation)

| File | Responsibility |
|------|----------------|
| `kicad_install.py` | Scan `Program Files\KiCad\*\bin\kicad-cli.exe`; probe `api-server --help` |
| `ipc_backend.py` | `IpcHeadlessBackend` — thread-safe kipy session, method handlers mirroring kc_bridge |
| `crud_router.py` | `crud_send()` — dispatch by `state["crud_backend"]` |
| `server.py` | Lifespan: resolve CLIs, init IPC, set state, shutdown |
| `tools/pcb.py` | CRUD tools call `crud_send`; exports call `run_kicad_cli` |
| `scripts/probe_ipc_headless.py` | Operator diagnostic CLI |

---

## Fleet cross-references

- Cursor config: [CURSOR_MCP.md](./CURSOR_MCP.md)
- Project page: [README.md](./README.md)
- Status: [STATUS.md](./STATUS.md)
- Ports: [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — 11016/17/18
- Master MCP JSON: [MASTER_MCP_CONFIG.json](../../operations/MASTER_MCP_CONFIG.json) — `kicad-mcp` key
- Chip/EDA SOTA: [chip_design_cad_sota.md](../../standards/rules/chip_design_cad_sota.md)

---

## References

- [KiCad IPC API](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/index.html)
- [Master kicad-cli api-server](https://docs.kicad.org/master/en/cli/cli.html)
- [kicad-python docs](https://docs.kicad.org/kicad-python-main/)
- [SWIG removal schedule](https://forum.kicad.info/t/migration-schedule-from-the-old-swig-api-to-the-ipc-api/69437)
