# BUG-028: Fleet launcher instacrash + module-serve health-path drift

**Discovered:** 2026-08-30 (Goliath)
**Severity:** P1 (launcher fails to start; silent)
**Component:** `FleetStartMode.ps1` consumers — the fleet `start.ps1` → `Invoke-FleetWebappStart.ps1` engine and each repo's `fleet-start.config.ps1`
**Status:** Fixed (vendored into goliath + 5 repos; module-serve drift corrected)

## Symptom

- Double-clicking a `mcp-central-docs/starts/{repo}-start.bat` (or the repo's own
  `start.bat`) makes a console window flash and close instantly — "instacrash" — with
  **no visible error** (the `powershell -File` window closes before the user can read it).
- Related: a repo launches but logs `WARN: backend health not ready at <HealthPath>`
  even though the server is up, because the `fleet-start.config.ps1` `HealthPath`
  doesn't match what the launched process actually serves.

## Root cause

The fleet launcher engine requires a **vendored per-repo copy** of
`scripts/FleetStartMode.ps1`. `Invoke-FleetWebappStart.ps1`:

```powershell
$fleetStartPath = Join-Path $paths.RepoRoot 'scripts\FleetStartMode.ps1'
if (-not (Test-Path -LiteralPath $fleetStartPath)) {
    Write-Host "ERROR: Missing vendored launcher helper: $fleetStartPath" -ForegroundColor Red
    Write-Host 'Run repair-fleet-unified-start.ps1 to vendor FleetStartMode.ps1.' -ForegroundColor Yellow
    exit 1
}
```

If the file is missing, the engine `exit 1`s. Because the `.bat` runs
`powershell -File start.ps1` with no `pause`, the window closes instantly. The
engine is designed to be vendored per repo (no `mcp-central-docs` runtime path), so a
repo scaffolded without the vendored copy silently ships a launcher that cannot start.

The related module-serve drift has two sub-causes:

1. **HealthPath mismatch**: `fleet-start.config.ps1` declares a `HealthPath` (e.g.
   `/api/health`) that the launched backend does not actually expose (e.g. it serves
   `/health` via the transport, or only serves `/mcp`). The probe 404s → the engine
   only emits a WARN (it `Wait-FleetBackendHealthy` then continues), so the launcher
   "works" but the webapp's REST surface and readiness dot are broken.
2. **module-serve that never binds a port**: `module-serve` runs
   `python -m <Module> <ServeArgs>` (default `--serve`). Some modules' entry points
   read an env var (e.g. `MCP_TRANSPORT`) or expect a different flag (`--http`,
   `--mode http`) instead of consuming `--serve`/argv, so the process runs **stdio**
   and never listens on the backend port at all.

## Diagnosis recipe

```powershell
# 1. Which repos have a fleet-start.config but NO vendored helper (the instacrash set)?
$repos = Get-ChildItem D:\Dev\repos -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'fleet-start.config.ps1') }
$repos | Where-Object { -not (Test-Path (Join-Path $_.FullName 'scripts\FleetStartMode.ps1')) } | Select-Object -ExpandProperty Name

# 2. Which repos use the fragile module-serve kind?
Select-String -Path (Get-ChildItem D:\Dev\repos -Directory -Filter fleet-start.config.ps1).FullName -Pattern "Kind\s*=\s*'module-serve'"

# 3. Confirm what the launched module actually serves:
#    - module-serve => `uv run python -m <Module> <ServeArgs>`; check the entry point
#      consumes ServeArgs and serves the declared HealthPath (FastAPI route / FastMCP http_app / health route).
#    - uvicorn-web-app => `uv run uvicorn <UvicornTarget>`; confirm UvicornTarget is the real ASGI object
#      (`:app` vs `:http_app`/`:web_app`/`:asgi_app` — see BUG-012) and that HealthPath resolves.
```

## Resolution / fix

- **Vendor the helper** into every repo that uses the fleet engine but lacks it:
  copy `mcp-central-docs/scripts/FleetStartMode.ps1` → `<repo>/scripts/FleetStartMode.ps1`
  (create `scripts/` if absent). Canonical fleet fix tooling: `repair-fleet-unified-start.ps1`,
  `vendor-fleet-startmode-all.ps1`, `sync-fleet-startmode.ps1`.
- **HealthPath/backend-kind consistency** (`fleet-start.config.ps1`): make the declared
  `HealthPath` match what the launched module actually serves, and prefer
  `Kind = 'uvicorn-web-app'` with the real `UvicornTarget` (`<pkg>.app:app` / `:http_app`)
  over `module-serve` when the module exposes a FastAPI app — module-serve is only correct
  when its entry point consumes `ServeArgs` and serves the health path.

Applied 2026-08-30:

| Repo | Defect | Fix |
|------|--------|-----|
| goliath-repo-context-mcp | Missing vendored helper + `module-serve` ran FastMCP-HTTP-only (no `/api/*`) | Vendored helper; `Kind=uvicorn-web-app`, `UvicornTarget=goliath_repo_context.app:app`, `HealthPath=/api/health` |
| cline-mcp, ms-graph-mcp, safety-mcp, zoji-mcp | Missing vendored helper (instacrash) | Vendored helper |
| huggingface-mcp | `Args` key (wrong — engine reads `ServeArgs`), module reads `MCP_TRANSPORT` env not argv → ran stdio, never bound :11152 | `Kind=uvicorn-web-app`, `UvicornTarget=huggingface_mcp.http_app:web_app` |
| winrar-mcp | `HealthPath=/api/health` but `--http` transport serves `/health` | `HealthPath=/health` |
| glama-status-mcp, invokeai-mcp, depot-mcp | None — `ServeArgs` correctly drives a real HTTP app that serves the declared path | No change (verified) |

## SOTA Impact

- Add an assfix gate: `scripts/FleetStartMode.ps1` present when `start.ps1` uses the
  fleet engine, and `fleet-start.config.ps1` HealthPath/backend-kind consistency with
  what the module actually serves (see `patterns/repo-assess-and-fix.md` §1A).
- Scaffolders (New Repo Gate): a repo with a fleet `start.ps1` MUST vendor
  `scripts/FleetStartMode.ps1` at build time, or its launcher instacrashes on day one.
