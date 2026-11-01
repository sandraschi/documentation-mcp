# BUG-092 — Both-Kinds-`none` config makes `starts/*.bat` exit 0 in ~1s (silent flash-close)

**Date:** 2026-10-31 | **Severity:** P2 | **Component:** `Invoke-FleetWebappStart.ps1` + 4 `fleet-start.config.ps1` files
**Status:** Fixed — per-repo fixes + engine both-none guard (see below)

## Symptom

Double-clicking `pinokio-start.bat` (then `deepfang`, `toolbench-mcp`,
`multi-gpu-cluster-recipes`) flashed a console window that closed in ~1s.
No error, no pause — the `starts/*.bat` instacrash guard only fires on
`errorlevel 1`, and the engine exited **0**:

```
  pinokio-mcp
  BACKEND   http://127.0.0.1:11250    (REST /api, MCP /mcp)
  FRONTEND  http://127.0.0.1:11249   (webapp UI)

EXITCODE:0
```

Distinct from BUG-028/033/035/036/049/050 (all nonzero exits with a visible
error): here the banner prints, nothing launches, the window closes, and the
user reports a "crash".

## Root cause

`Start-FleetWebapp` skips the backend block when `Backend.Kind='none'`
(`Invoke-FleetWebappStart.ps1:476`), the frontend block when
`Frontend.Kind='none'` (`:611`), and the browser block (`:685`). With both
`none` there is nothing to do, but the engine prints the normal banner and
exits 0 instead of saying so. Four configs were in this state (fleet audit
2026-10-31: 223 `starts/*.bat` launchers scanned, 4 hits):

| Launcher | Why both-none | Fix applied |
|---|---|---|
| `pinokio-start.bat` | `web_sota/` holds only static `catalog.html`, no vite app | bat opens `catalog.html` directly |
| `deepfang-start.bat` | stale config; `dashboard/` IS a vite app (`dev: vite --port 10957`) | config: `WebRoot='dashboard'`, Frontend `vite-npm` + `InstallOnStart` (backend stays `none`: docker compose via `just up`) |
| `toolbench-mcp-start.bat` | repo DEPRECATED (superseded by scraper-mcp) | bat redirects to `scraper-mcp\webapp` |
| `multi-gpu-cluster-recipes-start.bat` | Docusaurus site; engine has no docusaurus kind (`npm run dev` path only) | bat runs `npm start` in `website/` directly |

Related trap: the config comment in `multi-gpu-cluster-recipes` claimed the
site "is served via the repo's own start.ps1" — but root `start.ps1` is the
same fleet template, so it served nothing. Comments asserting out-of-engine
serving must name the real mechanism.

## Rule

A `fleet-start.config.ps1` with both Kinds `none` behind a `starts/*.bat`
launcher is a bug, not a neutral state — either wire a real Kind, point the
launcher at something that runs (static opener, redirect, direct serve), or
delete the launcher. Engine-level guard LANDED 2026-10-31
(`Invoke-FleetWebappStart.ps1` §0.5): both-`none` prints a red WARNING naming
the config and exits 1 in interactive runs (so the `.bat` guard holds the
window open); probe/headless runs warn and continue with exit 0. Verified
with a sandbox both-none config (warning fires, no side effects) and a
PSParser syntax check; the interactive exit-1 path follows the file's
existing `UserInteractive` convention (code-reviewed, not e2e-run from a
headless session).

Manifest note: redirect/custom launchers confuse
`sync-fleet-webapp-manifest-from-starts.ps1` — the 2026-10-31 regen listed
`toolbench-mcp-start.bat` under BOTH `scraper-mcp` and a stale `toolbench-mcp`
entry (the BUG-089 twin pattern). The stale entry was deleted by hand;
`note`/`probeSkip` fields survive regen (`Merge-ManifestEntry` preserves
them), so non-engine launchers should carry a `note` + `probeSkip:true`
(pinokio and multi-gpu entries do).

## Fleet audit (2026-10-31)

All 223 launchers resolved to target + config Kinds; the only 4 both-none
hits are fixed above. Single-`none` configs (backend-only or frontend-only)
still launch something and are out of scope.
