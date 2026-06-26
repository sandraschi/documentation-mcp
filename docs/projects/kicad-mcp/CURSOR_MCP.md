# KiCad MCP — Cursor MCP Configuration

**Updated:** 2026-05-29 (v0.3.0 hybrid)  
**Live file:** `C:\Users\sandr\.cursor\mcp.json`  
**Fleet canonical:** `D:\Dev\repos\mcp-central-docs\operations\MASTER_MCP_CONFIG.json`

---

## Active entry (stdio + hybrid env)

This is the production Cursor configuration for Sandra's machine as of 2026-05-29:

```json
"kicad-mcp": {
  "command": "C:/Users/sandr/.local/bin/uv.exe",
  "args": [
    "--directory",
    "D:/Dev/repos/kicad-mcp",
    "run",
    "--extra",
    "ipc",
    "python",
    "-m",
    "kicad_mcp.server",
    "--mode",
    "stdio"
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

### Why each field matters

| Field | Purpose |
|-------|---------|
| `--extra ipc` | Installs `kicad-python` (kipy) into the uv env for headless IPC |
| `KICAD_CLI_PATH` | **Stable 10.0.3** — all exports, DRC, ERC, library commands |
| `KICAD_IPC_CLI_PATH` | **11 nightly** — only used when installed; spawns `api-server` for CRUD |
| `KICAD_MCP_CRUD_BACKEND=auto` | Prefer IPC when nightly+kipy available; else TCP bridge; else none |
| `FASTMCP_BANNER=0` | Fleet standard — no startup banner noise in stdio |
| `--mode stdio` | Cursor MCP transport (not HTTP 11016) |

---

## Before first use

1. KiCad **10.0.x** stable installed (already on this machine).
2. KiCad **11 nightly** installed to `C:\Program Files\KiCad\11.0\` (or update `KICAD_IPC_CLI_PATH` if using `10.99`).
3. In repo:

```powershell
Set-Location D:\Dev\repos\kicad-mcp
uv sync --extra ipc
uv run python -m kicad_mcp.scripts.probe_ipc_headless
```

4. Restart Cursor MCP (or reload window) after editing `mcp.json`.

---

## Verify from Cursor chat

Ask the agent to call `kicad_status`. Interpret results:

| `crud_backend` | Meaning | Agent can… |
|----------------|---------|------------|
| `ipc` | Nightly + kipy working | Full headless CRUD (except place_component IPC gap) |
| `tcp` | `kc_bridge.py` running in KiCad GUI | Full CRUD via legacy bridge |
| `none` | Export lane only | DRC, Gerber, STEP, inspect via CLI; CRUD tools will error |

Other useful fields: `kicad_cli_path`, `kicad_ipc_cli_path`, `ipc_api_server`, `ipc_python_installed`.

---

## Override modes

### Force legacy GUI bridge only

Use when nightly is broken but KiCad 10 GUI + kc_bridge is running:

```json
"KICAD_MCP_CRUD_BACKEND": "tcp"
```

### Force IPC only (fail if nightly missing)

```json
"KICAD_MCP_CRUD_BACKEND": "ipc"
```

### Disable CRUD entirely (export-only agents)

```json
"KICAD_MCP_CRUD_BACKEND": "none"
```

### Disable IPC probe (e.g. during nightly upgrade)

```json
"KICAD_MCP_IPC_ENABLED": "0"
```

---

## HTTP mode (webapp, not Cursor)

Cursor uses stdio. For local dashboard development:

```powershell
Set-Location D:\Dev\repos\kicad-mcp
$env:KICAD_CLI_PATH = "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
$env:KICAD_IPC_CLI_PATH = "C:\Program Files\KiCad\11.0\bin\kicad-cli.exe"
uv run --extra ipc python -m kicad_mcp.server --mode dual --port 11016
```

Webapp: http://localhost:11017

---

## Path notes for Windows

- Use **forward slashes** in JSON paths (`C:/Program Files/...`) — avoids escape issues.
- `KICAD_IPC_CLI_PATH` can point at a not-yet-installed path; server starts fine but `crud_backend` stays `none` until the binary exists with `api-server`.
- If nightly installs as `10.99`, set:

```json
"KICAD_IPC_CLI_PATH": "C:/Program Files/KiCad/10.99/bin/kicad-cli.exe"
```

---

## Related docs

- [HYBRID_INSTALL.md](./HYBRID_INSTALL.md) — full hybrid guide
- Repo canonical: `kicad-mcp/docs/NIGHTLY_HEADLESS.md`
- [SETUP.md](D:/Dev/repos/kicad-mcp/docs/SETUP.md) — local dev bootstrap
