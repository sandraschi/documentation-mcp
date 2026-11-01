---
title: "CUA-NSIS Smoke Testing Standard (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-17
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# CUA-NSIS Smoke Testing Standard (SOTA 2026)

> **Cross-references**: [Tauri 2.0 Build](tauri_nsis_building.md) | [Playwright E2E](playwright_e2e_sota.md) | [Fleet Build Pipeline](../FLEET_BUILD_TEST_PIPELINE.md)

## Rationale

Unit tests and Playwright E2E catch regressions in dev. They do **not** catch:

- Backend unreachable after install (wrong port, missing `.exe`, cache path errors)
- WebView2 loading before backend is ready (timing race, no retry logic)
- CSP or CORS misconfiguration blocking API calls
- Silent install failures
- Registry cleanup on uninstall

The CUA-NSIS test fills this gap by installing the real NSIS build, launching it, and verifying it works via pywinauto.

## Pipeline

```
just build-native    # PyInstaller → Rust → NSIS
just cua-nsis-test   # install → launch → verify → uninstall
```

## Requirements

| Tool | Version | Notes |
|------|---------|-------|
| Rust toolchain | `rustc` 1.70+ | `rustup.rs` |
| MSVC Build Tools | VS 2022+ | `cl.exe`, `link.exe` |
| Tauri CLI | 2.x | `npx @tauri-apps/cli` |
| Tesseract OCR | 5.x | `C:\Program Files\Tesseract-OCR\tesseract.exe` |
| Python deps | — | `pywinauto`, `Pillow`, `pytesseract` — **MUST be added as project dev dependencies** (`uv add --dev pywinauto pillow pytesseract`), not assumed globally available. See pitfall below. |

### CRITICAL PITFALL (discovered 2026-09-17, gitee-mcp + teleoperator-mcp): silent false-pass on missing pywinauto

`cua-smoke.py` is invoked as `uv run python scripts/cua-smoke.py`, which resolves `pywinauto` from **the target repo's own venv/lockfile**, not any shared/global environment. If a repo's `pyproject.toml` never had `pywinauto`/`Pillow`/`pytesseract` added as dev dependencies, `import pywinauto` fails, `cua_available()` returns `False`, and every GUI-driven phase (window verify, screenshot, WebView OCR, nav click-through) is **silently skipped** — the old script version (`CUA_SMOKE_VERSION` < 6) still printed `"Result: N/N phases passed"` and `"ALL PHASES PASSED"` with no indication that the actual UI was never touched. This produced a **false pass** on both `gitee-mcp` and `teleoperator-mcp` on 2026-09-17 — the queue was marked `done` for both before anyone caught that no mouse ever moved.

**Fixed in the template (`CUA_SMOKE_VERSION = 6`)**: the script now prints a loud upfront warning if `pywinauto` isn't importable, and the final summary refuses to print "ALL PHASES PASSED" (and exits non-zero) if any phase failed OR `pywinauto` was unavailable — a silently-degraded run can no longer look identical to a genuine pass.

**Before trusting ANY historical `"done"` queue entry or prior CUA report**, check whether the run's log shows the `!!! WARNING: pywinauto is not importable !!!` banner, or predates 2026-09-17 — if so, treat it as unverified and re-run after confirming `pywinauto` is a real dev dependency of that repo.

**Fleet-wide status (updated 2026-09-17, later same day)**: `pywinauto`/`pillow`/`pytesseract` have been added as dev deps and import-verified (`uv run python -c "import pywinauto"` succeeds) in all 59 repos then in `operations/nsis-build-queue.json`'s pending queue, plus `mcp-federation-hub/bridge/` (its `pyproject.toml` lives in a subdirectory, not repo root). **Import succeeding is not the same as a genuine CUA pass** — only `gitee-mcp` and `teleoperator-mcp` have actually had a full smoke-test re-run and passed for real; the other 57 have the dependency in place but have NOT been build-tested yet. Each still needs its own `nsis-build` run before its queue entry can honestly say `done`. `audiotool-nexus-mcp` is a Node.js/TypeScript project with no Python backend at all — this dependency pattern doesn't apply to it; its CUA testing approach needs separate consideration. Repos outside the current queue (~155 more in the fleet) are still untouched.

### CRITICAL PITFALL #2 (discovered 2026-09-20, browser-mcp): OCR nav-walk passes even when EVERY webview fetch silently fails

Fixing pitfall #1 (missing `pywinauto`) is necessary but **not sufficient** — a genuinely-running GUI automation pass can *still* be a false positive. `_verify_page_ocr()` checks the screenshot's OCR text for the page's expected header/title string. But in a client-side-routed SPA, the page component renders its own `<h1>PageName</h1>` **regardless of whether its `useEffect` data fetch succeeded** — a broken `fetch()` just leaves the data section empty or shows an error the OCR check doesn't specifically look for. So "Page 'Bookmarks': OK (found 'Bookmarks')" proves the *page* loaded; it proves nothing about whether the *data* loaded.

On `browser-mcp`, instrumenting the backend (see below) proved that during a full nav-walk of 10 pages, only 2 pages' fetches ever reached the backend — yet all 10 passed their OCR title check and the script printed "12/12 phases passed, ALL PHASES PASSED." The likely root cause: the installed app was launched from within this session, itself running inside Claude Desktop's own AppContainer sandbox (confirmed: the app's own files carry ACLs scoped to an `S-1-15-3-...` Application Package Authority SID, and Windows Task Scheduler — a genuinely separate, unsandboxed context — could not even see the installed exe). Whether this is specifically AppContainer loopback isolation or something else in the sandbox wasn't fully root-caused; what matters is it's real, severe, and completely invisible to OCR-only verification.

**Fix (`CUA_SMOKE_VERSION = 8`)**: added a backend-side request-log instrumentation pattern and a new "Backend-receipt proof" phase that queries it directly (bypassing the webview and whatever might be blocking its network path) to confirm the nav-walk actually generated backend traffic. See "Backend Request-Log Instrumentation" below for the pattern. This phase gracefully skips (doesn't fail) on repos that haven't adopted the pattern yet, so it's safe to roll out incrementally.

**Before trusting ANY CUA report, including ones from 2026-09-17 that already had pywinauto and genuinely-moving-mouse GUI automation**: if it predates 2026-09-20 or doesn't show a "Backend-receipt proof" phase in its log, the nav-walk's OCR passes prove UI rendering only, not that any page's actual data fetch worked. This includes the repos marked `done` earlier tonight (`gitee-mcp`, `teleoperator-mcp`, `bilibili-mcp`, `pdf-mcp`, `benny-the-dog-mcp`) — none of them had this instrumentation at the time they were verified, so their data-fetch connectivity is technically unconfirmed even though their UI navigation was genuinely tested.

## Backend Request-Log Instrumentation (MANDATORY going forward)

Every fleet backend with a webapp SHOULD expose `GET /api/v1/request-log` — an in-memory ring buffer (e.g. `collections.deque(maxlen=200)`) of recent requests (method, path, origin header, client host, timestamp, status), populated by a small FastAPI/Starlette HTTP middleware. This is the ground-truth oracle for "did the webview's fetch actually reach the backend" — checkable via a direct HTTP call that bypasses whatever might be isolating the webview's own network path.

Reference implementation: `browser-mcp/src/browser_mcp/app.py` (`_REQUEST_LOG` + `_log_requests` middleware + `/api/v1/request-log` endpoint, added 2026-09-20).

`cua-smoke.py` v8+ automatically captures a request count baseline before `nav_click_through` and checks the delta afterward in a new "Backend-receipt proof" phase — `new_count == 0` is a hard fail (the webview never reached the backend at all), `new_count` below the number of pages visited (v14: the discovered sidebar pages; older: `len(nav_routes)`) is a warning (some pages' fetches aren't landing), and it skips cleanly (not a failure) if the endpoint 404s, so repos without this instrumentation yet aren't broken by the check.

## Justfile Recipes

Every repo with a Tauri wrapper MUST have these recipes:

```justfile
# Build the PyInstaller backend .exe and copy to Tauri resources
build-sidecar:
    pwsh -NoProfile -File web_sota\build-sidecar.ps1

# Build the Tauri NSIS desktop installer
build-native: build-sidecar
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
    $vcvars = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
    $envOutput = cmd /c "`"$vcvars`" > nul & set" | Where-Object { $_ -match '^(INCLUDE|LIB|LIBPATH|VCToolsVersion|WindowsSdkDir|UniversalCRTSdkDir|UCRTVersion)=' }
    foreach ($line in $envOutput) { $parts = $line.Split('=', 2); Set-Item -Path "env:$($parts[0])" -Value $parts[1] -ErrorAction SilentlyContinue }
    Set-Location '{{justfile_directory()}}\web_sota\src-tauri'
    npx @tauri-apps/cli build --bundles nsis

# Run the CUA smoke test against the installed NSIS app
cua-nsis-test:
    uv run python scripts/cua-smoke.py
```

## CUA Smoke Script Structure

Every repo MUST have `scripts/cua-smoke.py` with these 7 phases:

| Phase | What it does | Verifies |
|-------|-------------|----------|
| 1. Kill stale | `Stop-Process` + `taskkill` (by name, by port, then UAC-elevated fallback) | Clean start |
| 2. Install | `setup.exe /S` silent | Exit code 0 |
| 3. Launch | Start `{product}-operator.exe` | Backend health 200 |
| 4. Window | pywinauto `find_window` | Window visible, sized |
| 5. Screenshot | `win.capture_as_image()` | Non-empty PNG |
| 6. Diagnostics | `GET /api/v1/diagnostics` | Tools registered, Tesseract, window |
| 7. Uninstall | `uninstall.exe /S` | Registry clean |

The script includes a built-in version check (`CUA_SMOKE_VERSION` constant) that warns
when the template at `mcp-central-docs/templates/tauri-native/scripts/cua-smoke.py` is
newer — preventing template drift across the fleet.

All phase failures MUST be non-fatal (continue to next phase) except install/launch.

## CORS Requirement (MANDATORY)

Every fleet webapp MUST follow the CORS standard at `mcp-central-docs/standards/CORS_STANDARD.md`:

- `allow_origins` MUST include `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost` for Tauri WebView access
- `allow_origin_regex` MUST be set **unconditionally** (not gated on `{REPO}_TAURI`) and cover Tailscale `*.ts.net`, LAN IPs (`192.168.x.x`, `10.x.x.x`), Tailscale CGNAT (`100.x.x.x`), localhost, and `127.0.0.1`
- FastMCP HTTP servers MUST NOT use `run_http_async()` — use `uvicorn.Server` on `mcp.http_app()` with CORS middleware attached

The Rust `backend.rs` (or `main.rs`) MUST set the env var when spawning the backend:
```rust
.env("REPO_TAURI", "1")
```

## Dashboard Requirements

See [tauri_nsis_building.md](./tauri_nsis_building.md#backend-health-api--dashboard-kpis-fleet-wide-pattern) for the full standard. Every dashboard MUST have:

1. **Exponential backoff retry** on health check — 1s, 2s, 4s, 8s, 16s (not a single 45s interval)
2. **`data-testid` attributes** on all KPIs and status badges
3. **`GET /api/v1/diagnostics` endpoint** returning:
   - Backend status/version/uptime/port
   - System CPU/memory/disk
   - Registered tool count
   - Tesseract availability
   - Window presence
4. **Tauri `backend-status` event listener** in the frontend for instant refresh

## Playwright + CUA — When to Use Which

| | Playwright | CUA (pywinauto) |
|---|---|---|
| Speed | Fast (headless) | Slow (real browser) |
| Precision | `data-testid` selectors | OCR + coordinates |
| Catches | Route errors, rendering | Install failures, CSP, CORS |
| Runs in | Dev (Vite proxy) | Prod (NSIS install) |
| CI friendly | Yes | Windows only |

**Both are required.** Playwright for dev loop; CUA for pre-release certification.

## WebView Accessibility Standard (UIA Element Discovery)

For the CUA test to find nav items via UIA elements (rather than fragile screen coordinates),
every fleet webapp MUST render its sidebar navigation links with accessible labels that UIA can
discover. This is also a requirement for accessibility compliance.

### Requirements

1. **Sidebar nav `<a>` elements** MUST have an `aria-label` or visible text content that matches
   the page route name (e.g., `<a href="/app/books/" aria-label="Books">`)
2. **`data-testid` attributes** SHOULD also be present on nav links for Playwright parity
3. **Tauri WebView2** MUST have the `"accessible"` permission enabled in `capabilities/default.json`:
   ```json
   {
     "identifier": "default",
     "windows": ["main"],
     "permissions": ["core:default", "core:window:allow-set-focus", ...]
   }
   ```
4. **Window MUST be maximized** before nav click-through (`win.maximize()`) to ensure sidebar
   click coordinates are at predictable positions across displays

### Audit

Check if a repo's sidebar nav renders accessible UIA elements:

```python
# In pywinauto, after connecting to window:
elements = win.descendants(control_type="Hyperlink")
nav_elements = [e for e in elements if e.rectangle().left < 200]  # sidebar region
print(f"Found {len(nav_elements)} UIA nav elements")
```

Repos without UIA-accessible nav will fall back to coordinate-based clicking, which is
fragile and depends on window size, DPI scaling, and theme.

### Nav Click Strategy — Title Matching FIRST (SOTA 2026-08-02)

**The fleet nav-click order of precedence (template v3, all repos synced 2026-08-02):**

1. **`win.descendants(title=label)`** — pywinauto `title=` is the UIA **Name** criteria.
   Matches the sidebar link by its accessible text. This is the primary strategy and the one
   that finally made the nav walk actually step through webapps (first proven on learnbot-mcp:
   all 12 pages clicked, screenshots captured, live `/api/*` calls per page).
2. **`descendants(control_type="Hyperlink")` + window_text match** — fallback when `title=`
   finds nothing.
3. **Positional Hyperlink index** — fallback (fragile: sidebar order may differ from `nav_routes`).
4. **Pane + left-region filter** — WebView variant fallback.
5. **Coordinate click** (`sidebar_click_x/first_y/step_y` from config) — last resort.

**PITFALL — invalid pywinauto criteria:** `win.descendants(text=...)` is **invalid** —
`build_condition()` does not accept `text=`; it throws `IUIA.build_condition() got an
unexpected keyword argument 'text'` and the nav walk silently degrades to fallbacks (or worse,
the exception path skips screenshots entirely, producing 12 identical screenshots of the
dashboard that LOOK like a pass). UIA Name maps to `title=`. This exact bug shipped in
learnbot-mcp's standalone script and in every repo whose nav used `text=`; a fleet sweep on
2026-08-02 replaced coordinate-first clicking with title-first matching in 144 template-family
repos and added the nav phase to 14 repos that had none.

**Every repo with a Tauri wrapper MUST have a nav walk** — the old 6-phase scripts
(kill → install → launch → window → screenshot → uninstall) never clicked the sidebar and
could pass while the installed app was completely broken. The nav phase is now mandatory:
click each sidebar item, screenshot the page, verify no error keywords.

## Implementation Phases

| Phase | Status | What | Gap IDs |
|-------|--------|------|---------|
| **1 — Core** | ✅ **Done** (pywinauto-mcp) | Kill → install → launch → health → screenshot → diagnostics → uninstall | G3, G4, G6, G8 |
| **2 — Cert gate** | ✅ **Done** (pywinauto-mcp) | WebView bridge OCR proof, feature-route smoke, config-driven | G1 |
| **2b — CORS gate** | ✅ **Done** (fleet-wide) | Tauri CORS origins + TAURI env var in backend + Rust spawn | — |
| **3 — Nav + page verification** | ✅ **Done** (plex-mcp) | Sidebar nav click-through, screenshot each page, OCR verify (404/timeout/error/blank) | G5 |
| **3b — Title-matching nav** | ✅ **Done** (fleet-wide 2026-08-02) | `title=`-first click strategy in template v3; 144 repos patched; 14 repos gained the nav phase; all configs gained `nav_routes` | — |
| **3c — Discovered nav (v14)** | 🟡 **Template patched 2026-10-02, NOT yet verified on an installed app, fleet rollout pending** | Pages are discovered from the live sidebar (UIA Hyperlinks), navigated with Invoke; the nav phase now FAILS on no sidebar / no window / unchanged screenshot / error or blank OCR. Reason: the 3b claim above ("all configs gained `nav_routes`") was wrong: an audit found 125 of 170 repos with no or empty `nav_routes`, so their nav walk fell back to a hardcoded 4-page default, and the phase could not fail anyway (OCR result discarded, errors logged non-fatal) | — |
| **4 — Fleet** | 🔜 Planned | CI workflow, fleet parameterization | G7 |

## Reference Implementation (Canary)

- **Repo**: `pywinauto-mcp` (v0.5.5)
  - `scripts/cua-smoke.py` — 9-phase config-driven smoke test
  - `scripts/cua-nsis-config.json` — fleet-reusable config
  - `just build-native` + `just cua-nsis-test`
  - `GET /api/v1/diagnostics` — full endpoint
  - Dashboard with `data-testid` + exponential backoff retry + Tauri event listener

### Fleet Rollout Checklist

- [ ] Copy `scripts/cua-smoke.py` + `scripts/cua-nsis-config.json` to target repo (template v3+ — title-matching nav)
- [ ] Add `just cua-nsis-test` to justfile
- [ ] Edit config JSON: port, product name, NSIS glob, window title, feature route
- [ ] **No page list needed from `cua-smoke.py` v14**: the sidebar is discovered at run time, so there is nothing to keep in sync. (v13 and older read `nav_routes`: array of `["Sidebar Label", "Expected Header"]` pairs; without it the walk fell back to a hardcoded default.) Optional `nav_must_include: ["Label", ...]` fails the run if a page that must exist is missing from the discovered sidebar.
- [ ] Add `GET /api/v1/diagnostics` endpoint to backend
- [ ] Add `data-testid` to dashboard KPIs and bridge status
- [ ] Add exponential backoff retry to dashboard health check
- [ ] Verify: `just build-native && just cua-nsis-test` passes — **watch the nav phase**: distinct screenshots per page (different byte sizes), no duplicate captures

## Mouse Safety Rules (Critical)

The CUA script clicks sidebar nav items at absolute screen coordinates. This
interferes with the user's mouse. Follow these rules to prevent stuck input:

| Rule | Implementation |
|------|---------------|
| **Warn user first** | `_show_automation_warning()` — prints big red banner + 3s delay before any clicking |
| **`_release_mouse()` after every click** | Releases left/right/middle button via `mouse_event(MOUSEEVENTF_*)` |
| **`_release_mouse()` in `finally`** | Ensures cleanup even on Ctrl+C, crash, or timeout |
| **No driver commands** | Never use `sc.exe`, `pnputil`, `mouclass`, or any kernel/driver commands |
| **`set_focus` only after warning** | Window brought to front only after user has been told automation is starting |
| **`win.maximize()` before clicking** | Maximize window so sidebar click positions are consistent across displays |

The `_release_mouse()` helper:
```python
def _release_mouse():
    try:
        import ctypes
        for flag in (0x0004, 0x0010, 0x0040):  # left, right, middle up
            ctypes.windll.user32.mouse_event(flag, 0, 0, 0, 0)
    except Exception:
        pass
```

## Page Verification via OCR

After clicking a nav item, the script screenshots the page and runs OCR to verify:

| Check | What it catches |
|-------|----------------|
| Keyword scan | `404`, `not found`, `error`, `timeout`, `internal server error` |
| Empty OCR | Blank page, white screen, loading hang |
| Expected header | Page loaded the right route (header text found in OCR) |

Pattern (`_verify_page_ocr`):
```python
fail_keywords = ["404", "not found", "error", "timeout", "internal server error", "bad gateway"]
for kw in fail_keywords:
    if kw in text.lower():
        return False
if not text.strip():
    return False
if expected.lower() in text.lower():
    return True
```

## Dark Mode Only (MANDATORY)

CUA smoke tests **MUST run in dark mode only**. This is the fleet identity and
the OCR/screenshot baseline: every screenshot, OCR check, and nav click-through
assumes the dark theme.

Webapps that ship the optional light-mode toggle (CSS invert hack,
`chat_skills_prefab_standard.md` §7.1) MUST be forced back to dark before any
verification step. If a test machine has a persisted light choice, the toggle
persists it — reset it:

```python
# Before any screenshot/OCR in the CUA script:
import json, subprocess

# (a) localStorage reset via the app's own settings API where available, or
# (b) force .dark on the document before capture (Playwright init script):
#   page.add_init_script("document.documentElement.classList.add('dark')")
```

Two enforcement points:

1. **`data/testid` + OCR assertions**: run with dark theme active. Light-mode
   screenshots render differently (inverted palette) and will fail OCR keyword
   scans or expected-header matches for no real reason.
2. **Playwright e2e (dev loop)**: `page.addInitScript` forcing
   `document.documentElement.classList.add('dark')` in `playwright.config.ts`
   or per-spec — screenshots for README Preview and e2e assertions must be
   dark-consistent regardless of any localStorage on the runner.

Reference: `opencode-cli-mcp` ships the light toggle (`ocmcp-light-mode`
localStorage key) — its CUA/Playwright runs reset `.dark` first.
