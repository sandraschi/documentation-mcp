# Fleet start.ps1 + start.bat Standard Template (SOTA 2026)

**Unicode:** EM DASH is **never allowed** in `start.ps1` / `start.bat`. Use ASCII `-` only. See [patterns/unicode_safety.md](./patterns/unicode_safety.md).

## Canonical location (full-stack webapps)

**Naked-PC launcher lives in `webapp/`** (or `web_sota/`, `web/`, `web-sota/`):

| File | Role |
|------|------|
| `webapp/start.ps1` | Full stack: winget bootstrap, `uv sync`, frontend install, vite guard, backend + Vite, browser |
| `webapp/start.bat` | Double-click wrapper next to that `start.ps1` |

Copy from [templates/start-webapp.bat](./templates/start-webapp.bat).

## Repo root (shortcut only)

Users clone and run `.\start.bat` from the repo root. Root **must delegate** to webapp:

**`start.bat`** - [templates/start-root.bat](./templates/start-root.bat)

**`start.ps1`** (optional thin delegate):

```powershell
param([switch]$Headless, [switch]$BackendOnly, [switch]$NoBrowser)
& (Join-Path $PSScriptRoot "webapp\start.ps1") @PSBoundParameters
exit $LASTEXITCODE
```

Do **not** duplicate the full naked-PC script at root and webapp. One implementation: **`webapp/start.ps1`**.

Reference: `libreoffice-mcp`, `chip-design-mcp` (after 2026-05-31 layout).

## `just-starts/` (MCD monorepo shortcuts)

| File | Points to |
|------|-----------|
| `{repo}-start.bat` | `..\..\{repo}\webapp\start.ps1` (full stack) |
| `{repo}-just.bat` | `..\..\{repo}` + `just` (recipe dashboard only) |
| `start-all.ps1` | Discovers all `D:\Dev\repos\*\start.ps1` (includes `webapp\start.ps1`) |

See [just-starts/README.md](../just-starts/README.md).

## Launch modes (dot-source `FleetStartMode.ps1`)

| Switch | Effect |
|--------|--------|
| *(none)* | **Both** - backend + frontend + browser |
| `-BackendOnly` | Backend only (no Vite) |
| `-Headless` | Hidden console + backend focus (fleet automation) |
| `-FrontendOnly` | Vite only (skip backend start) |
| `-NoBrowser` | Do not auto-open browser |

Shared helper: `mcp-central-docs/standards/FleetStartMode.ps1`

**Port preamble (required):** Define `$WebPort`, `$BackendPort`, and `$ProjectRoot` **before** dot-sourcing `FleetStartMode.ps1` and calling `Stop-FleetPortSquatters`. A common regression after adding FleetStartMode is stripping these lines — the probe then sees empty ports and Vite runs as `vite --port --host`. Restore from `start.ps1.bak.20260508_*` when present.

**Zombie kill:** Prefer `Stop-FleetPortSquatters` from `FleetStartMode.ps1` (two-pass `Stop-Process` + `taskkill /F` fallback). Fleet cold-start probe teardown uses the same fallback.

**Fleet probe:** Full manifest cold-start is documented in [FLEET_WEBAPP_PROBE.md](../docs/operations/FLEET_WEBAPP_PROBE.md). After manifest or port edits, run `scripts/sync-fleet-webapp-manifest-from-starts.ps1` then **Broken\*** in MetaMCP to re-test failures only.

## Legacy / stdio-only repos

Some repos keep a **root-only** `start.ps1` for stdio MCP (`uv run -m ...`) with no webapp. That is not the dashboard launcher. If a webapp exists, the SOTA full-stack script still belongs under **`webapp/`**.

## `web_sota/` scaffold

`mcp-central-docs/web_sota/start.ps1` is an older minimal template (ports 10794/10795). New repos should copy **naked-PC** scripts from `aiwatcher-mcp` or `chip-design-mcp/webapp/start.ps1`, not the old `web_sota` job-based sample.

## Key rules

1. **Ports** from [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md) - no 3000/5173/8000 defaults
2. **Vite** via `bun run dev` / `npm run dev` or explicit port in `package.json` scripts
3. **Vite guard** must accept `node_modules/.bin/vite.exe` (Bun on Windows) - see [NAKED_PC_INSTALL_STANDARD.md](./NAKED_PC_INSTALL_STANDARD.md)
4. **Zombie kill** on backend and frontend ports
5. **Import smoke-test** before health-wait loop
6. **`start.bat`**: `powershell.exe`, WindowsApps on PATH, pause on error
