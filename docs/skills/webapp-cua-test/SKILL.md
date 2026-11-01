---
name: webapp-cua-test
description: Run the pre-Tauri CUA click-through test (real browser, dev stack, OCR "Connected" wait, sidebar nav walk) for a fleet MCP server repo under D:\Dev\repos. Trigger when the user says "cua webapp test" or "webapp clickthrough" followed by a repo name, asks for an e2e click-through of a webapp, or asks whether a webapp boots and connects in a real browser. Not for the installed NSIS app (that is the nsis-build skill / cua-nsis-test) and not for DOM assertions (Playwright), and not for hunting fake data or dead buttons (fakefind).
---

# webapp-cua-test - dev-stack click-through in a real browser

Standard: `D:\Dev\repos\mcp-central-docs\standards\rules\cua_webapp_testing.md` (read it first on a
repo you have not run before). Recipe: `just cua-webapp-test`, defined in the vendored
`scripts/just/fleet.just`. Script: `scripts/cua-webapp-test.py`.

**This drives the user's desktop** (opens the default browser, clicks, screenshots). Say so before
running, and do not run it while the user is mid-task without asking.

## Phase 1 - Pre-flight (read-only; stop and report on any failure)

| Check | How |
|---|---|
| Files exist | `scripts/cua-webapp-test.py`, `scripts/just/cua-webapp-test.ps1`, `start.ps1`, config `scripts/cua-nsis-config.json` |
| Config keys | `frontend_port`, `backend_port`, `backend_health_path` set. No page list needed: script v2 discovers the sidebar (check the script prints `CUA Webapp Test v2`; a v1 copy walks only the stale `nav_routes`) |
| Recipe available | `just --list` shows `cua-webapp-test` (from `fleet.just` or a local recipe) |
| Python deps | `.venv` python OR global `py` can import `pywinauto`, `PIL`, `pytesseract`. Missing `.venv` is fine: the wrapper falls back to `py`, and `start.bat` regenerates venvs |
| Tesseract program | `C:\Program Files\Tesseract-OCR\tesseract.exe` exists (pytesseract needs the binary, not just the package) |
| Ports free, no service owns them | `Get-NetTCPConnection -LocalPort <backend>,<frontend> -State Listen` and `Get-Service` for the repo. The test frees these ports by killing the owner. If an NSSM service owns them, STOP: never kill an NSSM child, use `sc.exe stop/start` and verify a new PID (fleet rule) |
| Wrapper not stale | `scripts/just/cua-webapp-test.ps1` must NOT contain `Join-Path $PSScriptRoot ".." ".."` (BUG-057: fails under Windows PowerShell 5.1). Fix to `"..\.."` |

## Phase 2 - Run

```powershell
Set-Location "D:\Dev\repos\{repo}"
just cua-webapp-test
```

Allow several minutes (stack start, badge wait up to 60 s, six-plus page clicks). Capture output to a
file; do not re-run blind on failure.

## Phase 3 - Read the result critically

Nine phases print `V <name>` on pass: kill-stale, start-stack, backend-health, frontend-ready, browser,
connected-badge, nav-walk, diagnostics, cleanup. `Result: 9/9` is necessary, not sufficient:

- **Page count must match the app.** Compare `Discovered N sidebar pages` with the real sidebar (for a
  Vite app: the nav array in `src/Layout.tsx` or equivalent). v2 enforces that each page visibly differs
  from the previous one; on a v1 script check `cua-reports/webapp-*.png` sizes/hashes yourself.
- **`tools=0` is a red flag.** Phase 8 can pass with `Diagnostics: HTTP 200, tools=0`. A repo with tools
  reporting 0 passed a gate that examined nothing; report it as NOT verified.
- **Connected badge wait** is a retry loop, not an instant check: "Connecting..." is not an error.

## Phase 4 - Failure triage

| Symptom | Likely cause |
|---|---|
| `Join-Path ... positional parameter cannot be found` | BUG-057, stale wrapper under PS 5.1 |
| Fails at phase 2/3 | `start.ps1 -Headless` or backend crash: read the backend log, run `start.ps1` by hand |
| Stuck at phase 6 | Badge text differs from `connected_badge_text`, or the frontend never reaches the backend (CORS, port in `.env`) |
| Nav label not found | `nav_routes` labels do not match the visible sidebar text |
| Python import error | deps missing in both `.venv` and `py` |

## Phase 5 - Report

State: repo, `N/9`, which phases passed, screenshot sanity, diagnostics tool count, and an explicit
**NOT verified** list (for example: installed NSIS build, other browsers, content of the pages beyond
navigation). If the user asked for a write-up, follow `standards/WORK_REPORT_STANDARD.md`.
Fix only what blocks the run in the one repo you touched; a stale wrapper in other repos is a fleet-wide
finding to report, not to sweep without sign-off.
