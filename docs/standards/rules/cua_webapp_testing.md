---
title: "CUA Webapp Testing Standard (SOTA 2026)"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-10-02
# status: active -- verified 2026-10-02: `just cua-webapp-test` on learnbot-mcp passed 9/9
# (after fixing the stale wrapper, BUG-057). Only that one repo has been re-run since the bulk
# import; treat other repos' configs as unverified until run.
---
# CUA Webapp Testing Standard (SOTA 2026)

**Established**: 2026-08-02
**Reference impl**: `learnbot-mcp` — first 9/9 PASS (stack start → Connected badge → 6-page nav walk)
**Template**: `mcp-central-docs/templates/tauri-native/scripts/cua-webapp-test.py`
**Cross-refs**: [CUA-NSIS Smoke Testing](cua_nsis_smoke_testing.md) | [Playwright E2E](playwright_e2e_sota.md)

---

## Purpose

`cua-nsis-test` certifies the **installed** app (NSIS → Tauri WebView). But a 10-minute
installer build is the wrong feedback loop when you're iterating on the webapp itself, and
repos without a Tauri wrapper still need a click-through test.

`cua-webapp-test` fills the gap: **pre-Tauri, in the real browser**, same idea — spin up
the dev stack, wait for the UI to actually connect, click through the sidebar.

| | `cua-nsis-test` | `cua-webapp-test` |
|---|---|---|
| Target | Installed NSIS app | Dev stack (`start.ps1`) |
| Backend | Frozen PyInstaller exe | `uv run` source |
| Frontend | Tauri WebView2 | Real browser (Chrome/Edge) |
| Build needed | `just build-native` (~10 min) | None |
| Nav strategy | `descendants(title=label)` | Same (UIA over browser) |
| When | Pre-release cert | Dev loop / no-Tauri repos |

**Both are required** where applicable. Playwright covers dev-loop DOM assertions;
CUA-webapp covers "does the real stack actually boot and connect".

---

## Phases

```
just cua-webapp-test
```

1. **Kill stale** — free backend + frontend ports (temp PS script, no inline `-Command` with `$_`)
2. **Start stack** — `start.ps1 -Headless` (fleet standard switch); fallback: direct `uv run` spawn of `backend_module` from config
3. **Backend health** — poll `{backend_port}{health_path}` until 200 (default 30s)
4. **Frontend ready** — poll `{frontend_port}` until HTTP 200 (if configured)
5. **Open browser** — default browser to `http://127.0.0.1:{frontend_port}`
6. **Connected badge wait** — THE WRINKLE: webapps show "Connecting..." for several seconds
   while the backend boots. OCR the window until `connected` / `system online` / `ready`
   appears (default timeout 60s, retry every 2s). **Do not instant-fail.**
7. **Nav walk** — pages are **discovered from the live sidebar** each run (visible, labelled
   Hyperlinks sharing one x-extent, top to bottom) and each is navigated with UIA Invoke (no
   mouse, works for links scrolled out of view). Per-page screenshots go to
   `cua-reports/webapp-NN-{label}.png`. FAILS if no sidebar is found or a page's screenshot is
   identical to the previous page's (navigation had no visible effect). No page list to maintain:
   add or delete a sidebar entry and the test follows. The run also logs which pages were
   added/removed since the last run (`cua-reports/nav-last.json`).
8. **Diagnostics** — `GET /api/v1/diagnostics` (tool count)
9. **Cleanup** — free ports again

---

## Config

Reuses `scripts/cua-nsis-config.json`. Required additions:

| Key | Default | Notes |
|-----|---------|-------|
| `frontend_port` | 0 | Vite/dev port. 0 = skip frontend wait/browser |
| `nav_routes` | — | **Ignored by this test since v2** (pages are discovered). The NSIS smoke script (`cua-smoke.py`) reads it up to v13; v14 (template patched 2026-10-02, not yet rolled out or verified on an installed app) discovers pages too |
| `nav_must_include` | `[]` | Optional `["Label", ...]` guard: fail if a page that must exist is missing from the discovered sidebar (catches a broken sidebar, not deliberate deletions) |
| `connected_badge_text` | `connected` | OCR keyword for the connected state |
| `connected_timeout` | 60 | Seconds to wait for Connected (retry every 2s) |
| `backend_module` | — | Python module for direct-spawn fallback (`learnbot_mcp.api`) |

Accepts both `health_path`/`backend_health_path` and `window_title_re`/`window_title`
key variants (older configs).

---

## The Connected Badge (critical)

Fleet webapps show a status dot + label in the topbar: `Connecting...` →
`System Online` / `Connected` once the backend is reachable (see
`tauri_nsis_building.md` § backend-status pattern). The test MUST:

1. OCR the browser window in a loop (2s interval)
2. Accept `connected`, `system online`, `online`, `ready` (case-insensitive)
3. Keep waiting while `connecting...` is visible — it is NOT an error
4. Only fail after `connected_timeout`

This mirrors the exponential-backoff health poll in the frontend itself. Instant-fail
on first OCR would make every test flaky.

---

## Known pitfalls

- **Stale wrapper under PS 5.1 (BUG-057).** `fleet.just` runs `scripts/just/cua-webapp-test.ps1` with
  `powershell.exe` (5.1). A multi-argument `Join-Path $PSScriptRoot ".." ".."` is PS7-only and fails
  before anything runs. About 190 repo copies still have it; the mcd template is fixed.
- **A static page list goes stale silently (fixed in v2).** v1 walked only `nav_routes`; learnbot-mcp's
  config listed 6 of its 12 sidebar pages, and a repo with no `nav_routes` skipped the walk and PASSED.
  v1 also ignored each route's "expected" value and clicked with the mouse, so a click that missed
  (the tall sidebar's last entries sit below the window edge) still passed. Fleet audit 2026-10-02:
  of 170 repos carrying the script, 125 have no or empty `nav_routes` (walk skipped = vacuous pass)
  and only 44 have a list. v1 copies remain until the template is re-synced (needs sign-off).
- **Phase 8 can pass with `tools=0`.** The diagnostics gate accepts HTTP 200 regardless of tool count
  (seen on learnbot-mcp). A 9/9 with `tools=0` means that gate examined nothing: report it.
- **Missing `.venv` is fine.** The wrapper falls back to global `py`, which needs `pywinauto`, `Pillow`
  and `pytesseract`, plus the Tesseract program at `C:\Program Files\Tesseract-OCR`.
- **Ports are freed by killing their owner.** Never run it against a repo whose backend is an NSSM
  service (restart those with `sc.exe`, per the fleet rule).
- **Skill:** `skills/webapp-cua-test/SKILL.md` runs this flow end to end.

## Fleet Rollout Checklist

- [ ] `scripts/cua-webapp-test.py` present (copy from template)
- [ ] `scripts/just/cua-webapp-test.ps1` present
- [ ] `just cua-webapp-test` recipe available (fleet.just merge OR local recipe if no fleet.just import)
- [ ] Config: `frontend_port`, `connected_badge_text` (no page list needed from v2)
- [ ] Verify: `just cua-webapp-test` — watch phase 6 (Connected wait) and phase 7 (distinct per-page screenshots)
