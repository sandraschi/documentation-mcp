# The CUA-NSIS Saga — How the Smoke Test Finally Learned to Walk

**Era:** 2026-07-16 → 2026-08-02
**First truly successful run:** 2026-08-02, learnbot-mcp — **ALL 6/6 PASS**
**Cross-refs:** [CUA-NSIS Smoke Testing Standard](../standards/rules/cua_nsis_smoke_testing.md) · [Tauri production pitfalls](../standards/TAURI_PRODUCTION_PITFALLS.md) · [PyInstaller gotchas](../standards/rules/tauri_nsis_building.md)

---

## The Lie at the Heart of "It Passed"

For weeks, the fleet's CUA-NSIS smoke test reported green. Repos shipped installers
"certified" by a 6-phase script: kill stale → install → launch → window → screenshot →
uninstall. Every phase passed. Installers went out the door.

The test was **not testing the app**. It was testing that *a window appeared*.

Phase 5 took one screenshot of the dashboard. If the WebView rendered an error page,
a blank canvas, or `ERR_CONNECTION_REFUSED`, the screenshot was still "non-empty"
and the phase passed. The sidebar was never clicked. The 12 pages behind the sidebar
were never visited. An installer whose UI could not talk to its own backend passed
certification.

The damage was real and concrete: learnbot-mcp's v0.5.0 installer shipped with a
frontend that fetched **relative `/api` paths from the `tauri://localhost` webview
origin** — the UI could never reach its backend. The smoke test said PASS. The app
was broken on day one, and nobody knew until a user reported "no webapp started"
on 2026-08-02.

---

## Chapter 1 — The First Real Walk (2026-08-02, learnbot-mcp)

The day started with a simple report: `learnbot-start.bat` fails, no webapp started.

The launcher was fine. The backend started. The port was listening. But the frontend
was on `::1` (IPv6) only — `http://127.0.0.1:11102` refused connections because
`vite.config.ts` had no `host:` key. Vite's default `localhost` resolved IPv6-first
on this box. One-line fix (`host: "127.0.0.1"`), then the hunt for the next layer.

**Layer 2 — the smoke test itself.** The learnbot `cua-smoke.py` had a nav phase,
but it used `win.descendants(text=item)` — which is **not valid pywinauto**. The
UIA criteria parameter is `title=`, not `text=`; `text=` throws
`IUIA.build_condition() got an unexpected keyword argument 'text'`. The exception
path skipped the fallback, took a screenshot anyway, and logged "12 screenshots
captured". All 12 were the dashboard. A pass that was a pass in name only.

Fix: `win.descendants(title=item)`. Suddenly — real navigation. The smoke test
clicked **Dashboard, Chat, Personas, Safety, Compliance, Audit, Demos, Japanese,
Lessons, Avatar, Voices, Help**, and each page made its live `/api/*` calls:
`GET /api/personas`, `GET /api/safety/rules` — 200s, per page, in the installed app.

That was the moment the smoke test learned to walk. Sandra's words: *"I was very
happy when I finally saw it working and stepping through the webapp."*

---

## Chapter 2 — What Else the Walk Uncovered

The working nav walk exposed two more production bugs that the dashboard screenshot
had been hiding for weeks:

1. **The relative-`/api` trap (learnbot v0.5.0, shipped broken).** The Tauri webview
   loads embedded `dist/` at `tauri://localhost`. The frontend's `api.ts` used
   `BASE = "/api"` — relative — so every fetch went to `tauri://localhost/api/...`,
   which served the SPA's index.html, not the backend. Fix: the `VITE_API_ORIGIN`
   env pattern (absolute origin in prod, relative in dev via the Vite proxy).
   `native/build.ps1` now sets `VITE_API_ORIGIN=http://127.0.0.1:{port}` before
   `bun run build`. This is the fleet-standard pattern from pywinauto-mcp's `api.ts`.
2. **The IPv6-only Vite bind.** No `host:` in `vite.config.ts` → `bun run dev`
   served on `::1` only → `127.0.0.1` refused. Already documented in
   `TRAPS_AND_PITFALLS.md #8` (reverse direction now added 2026-08-02). Fleet-wide:
   47 repos patched the same day.

---

## Chapter 3 — The Fleet Sweep (2026-08-02)

The learnbot fix became the template. `mcp-central-docs/templates/tauri-native/
scripts/cua-smoke.py` bumped **v2 → v3** with the title-first nav strategy:

```
1. win.descendants(title=label)          ← UIA Name criteria — primary
2. descendants(control_type="Hyperlink") + window_text match
3. Positional Hyperlink index
4. Pane + left-region filter
5. Coordinate click (last resort)
```

A fleet-wide audit found **162 repos** with `cua-smoke.py`:

| Family | Count | Condition |
|--------|-------|-----------|
| Coordinate-nav (template-family) | 144 | Had a nav walk, but coordinate-based only |
| Old 6-phase (no nav at all) | 14 | Never clicked the sidebar — the "passes" were fake |
| Other (plex/docker/podman/learnbot) | 4 | Individual handling |

**The 144** got a surgical insert: title-matching first, coordinate fallback
preserved — batched ≤5 files per operation, timestamped `.bak` per file, every
file syntax-validated after (162/162 OK).

**The 14** got the nav phase added entirely — they had never walked. Each also
received `nav_routes` in its `cua-nsis-config.json`, derived from the repo's actual
sidebar component (labels, not page filenames — filenames lie, `label:` strings
don't).

---

## Lessons Learned (the actual value)

1. **A screenshot is not a verification.** A non-empty screenshot proves pixels,
   not functionality. The nav walk + per-page live API calls prove the app works.
   Never ship an installer whose smoke test only screenshots the dashboard.
2. **`text=` is not a pywinauto criterion.** UIA Name maps to `title=`. If you see
   `build_condition() got an unexpected keyword argument 'text'`, the nav walk
   silently degraded — and every screenshot after it is the same page.
3. **Same-size screenshots are the tell.** 12 screenshots of ~identical byte size
   = the walk failed and you're looking at 12 copies of one page. Distinct sizes =
   real pages.
4. **The smoke test is the last gate before "certified".** It caught what the
   browser dev loop cannot: the embedded webview's origin, the frozen binary's
   transport, the installed app's real ports. Trust it, and make it walk.
5. **Version drift is silent until the walk.** `CUA_SMOKE_VERSION` warns when the
   template is newer — but only if the script runs. A 6-phase script that skips the
   walk never fires the warning. The walk is the tripwire.

---

## Status

- **Template v3** (title-first nav) — canonical, in `templates/tauri-native/`
- **144 repos** — title-matching inserted, syntax-validated
- **14 repos** — nav phase added + `nav_routes` configs populated
- **learnbot-mcp v0.6.0** — first fleet installer whose CUA run truly walked the
  app (6/6 PASS, 12 pages, live API data), released 2026-08-02
- **Doc** — standard updated with title-first strategy + the `text=` pitfall
- **cua-webapp-test** (2026-08-02) — pre-Tauri sibling test: `start.ps1 -Headless`
  stack + Connected-badge wait + browser nav walk. Template + helper + fleet.just
  recipe merged add-only into 160 repos (no repo content clobbered); first 9/9 PASS
  on learnbot-mcp. See `cua_webapp_testing.md`.
