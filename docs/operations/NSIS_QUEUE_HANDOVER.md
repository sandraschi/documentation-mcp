# NSIS Build Queue — Handover

**Last updated**: 2026-09-20
**For**: whoever picks this up next — opencode, Antigravity, Cursor, another Claude session, or the human
**Purpose**: continue an in-progress effort to build and genuinely-verify NSIS desktop installers for the fleet's Tauri-wrapped MCP repos.

This is a **separate, topic-specific handover** from the root `HANDOVER.md` (which as of 2026-09-20 covers a different active effort — fleet-gate verification tooling). Both are current; read whichever matches what you're picking up. This one is entirely about `operations/nsis-build-queue.json` and the Tauri/NSIS/CUA build pipeline.

Read this whole file before touching the queue. Several fleet-wide bugs were found and fixed across two sessions (2026-09-17 and 2026-09-20); repeating the mistakes below wastes hours re-discovering them.

---

## TL;DR state right now

- **Queue file**: `operations/nsis-build-queue.json` — single source of truth for done/pending/failed.
- **Genuinely done** (real GUI automation, real nav-walk — but see the CRITICAL caveat below): `gitee-mcp`, `teleoperator-mcp`, `bilibili-mcp`, `pdf-mcp`, `benny-the-dog-mcp`, and now `browser-mcp` (see "browser-mcp: resolved" below — this was NOT the sandboxing bug the CRITICAL section originally suspected).
- **`kicad-mcp`**: someone did manual work here (commit `1253b6b` "fix: NSIS build gaps found during manual queue run") but `BUILD_LOG.md` was never updated and there are uncommitted build artifacts. Needs a proper re-verification pass, not just trusting the commit exists.
- **56 other repos** have `pywinauto`/`pillow`/`pytesseract` added as dev deps and import-verified, but **NOT build-tested**.
- User-requested priority order (as of 2026-09-20): `kicad-mcp` → `chip-design-mcp` → `logic-analyzer-mcp` → `oscilloscope-mcp` → `database-operations-mcp` → `virtualization-mcp`, then the rest of the queue.
- A local scheduled task **`nsis-build-queue-nightly`** exists (fires hourly 22:00–06:00 Europe/Vienna, pops one `pending` repo per fire, self-defers if the user is actively at the machine). Confirmed still correctly deferring as of 2026-09-20.

---

## CRITICAL (2026-09-20): CUA "passes" may not prove what you think they prove

**Read this before trusting ANY CUA report, including the 5 "genuinely done" repos above.**

OCR-based nav-walk verification (the core of `cua-smoke.py`) checks whether a page's *title* renders after clicking its sidebar link. In a client-side-routed SPA, the title renders via React Router **regardless of whether that page's data-loading `fetch()` actually succeeded**. So "Page 'Bookmarks': OK (found 'Bookmarks')" proves the page component mounted — it proves nothing about whether its API call reached the backend.

On `browser-mcp` (2026-09-20), instrumenting the backend to log every request it actually receives proved that during a 10-page nav-walk, only 2 pages generated real backend traffic — yet all 10 passed OCR and the script printed "12/12 phases passed, ALL PHASES PASSED." Likely root cause: the installed app was launched from within this session, itself running inside Claude Desktop's own AppContainer sandbox — confirmed via the installed app's files carrying ACLs scoped to an `S-1-15-3-...` Application Package Authority SID, and Windows Task Scheduler (a genuinely separate, unsandboxed context) being unable to even see the installed exe. The exact isolation mechanism (AppContainer loopback blocking vs. something else) wasn't fully root-caused, but the effect is real, severe, and was completely invisible to OCR-only verification.

**The fix**: `cua-smoke.py` v8 adds a "Backend-receipt proof" phase. It requires the target backend to expose `GET /api/v1/request-log` (an in-memory ring buffer of recent requests, populated by HTTP middleware — reference implementation in `browser-mcp/src/browser_mcp/app.py`, added 2026-09-20). The phase queries this endpoint directly (a plain HTTP call, immune to whatever's isolating the webview) before and after the nav-walk and checks whether real traffic was generated. `new_count == 0` is a hard fail; `new_count < len(nav_routes)` is a warning; it skips cleanly (not a failure) if the repo hasn't adopted the endpoint yet.

**Action needed**: the 5 "done" repos before browser-mcp (`gitee-mcp`, `teleoperator-mcp`, `bilibili-mcp`, `pdf-mcp`, `benny-the-dog-mcp`) were verified *before* this instrumentation existed. Their UI navigation was genuinely tested (real mouse automation, real window detection), but their actual data-fetch connectivity is technically unconfirmed. Consider re-running their CUA tests after adding the request-log endpoint to each, to get a real confirmation — or at minimum, don't treat their "done" status as proof that in-app data loading works end-to-end.

**When building/fixing any repo going forward**: add the request-log endpoint (copy the pattern from `browser-mcp/src/browser_mcp/app.py`) as part of Phase 1 pre-flight, not as an afterthought — it's cheap (a ~20-line middleware + one endpoint) and makes every subsequent CUA run on that repo trustworthy in a way OCR alone can't be.

---

## `browser-mcp`: resolved (2026-09-20) — the sandboxing theory above was WRONG

The paragraph above (written earlier the same day) theorized Windows AppContainer sandboxing as the reason most of browser-mcp's fetches never reached the backend. **That theory was wrong.** The user reported the bug live ("browser-mcp tauri webapp fails completely, no contact to backend"), which prompted going further than the request-log instrumentation alone: attaching Chrome DevTools Protocol to the installed app's WebView2 process (`WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=<port>` env var + a Python `websockets` CDP client) to get ground-truth Network/Console visibility inside the actual webview.

**Real root cause**: every page used a *relative* `fetch('/api/...')`. Inside the Tauri webview, a relative fetch resolves against the webview's own origin, `http://tauri.localhost` — not the backend at `http://127.0.0.1:<port>`. Tauri's asset-protocol server has a silent **SPA fallback**: any unmatched path (including an API path) gets `index.html` back with a `200 OK`. So the fetch "succeeded," parsed as HTML where JSON was expected, and every page either crashed (`Skills.tsx`, the only one that visibly broke) or silently kept stale/empty state (the other 7). The Topbar's "Online" health badge had been a false positive the entire time, because `r.ok` is `true` for that 200-with-HTML response too.

There was a **second, compounding bug**: once the webapp source was fixed, the installed app kept showing old behavior. Cargo/Tauri was not detecting `webapp/dist/` content changes as a rebuild trigger for asset embedding — `npx tauri build` reported success and genuinely recompiled Rust each time, but embedded the stale JS bundle. Confirmed via CDP by observing the installed app was still loading a JS bundle with an old content hash. Fix: `cargo clean` (removed 1.4GB / 3418 files) + full rebuild (3m09s, vs. a suspiciously-fast ~1m30s for the "cached" builds that weren't actually re-embedding assets).

**Fix applied**: `webapp/src/lib/api.ts` exports `API_BASE` (absolute `http://127.0.0.1:10780` in prod, empty string in dev where Vite's proxy already handles it) — applied to all 8 fetch-using files (`Skills`, `Apps`, `Bookmarks`, `Chat`, `Dashboard`, `Logs`, `Settings`, `Topbar`). Verified post-fix via CDP that `/health` and `/api/skills` now resolve to the real backend, and via the request-log endpoint that a 10-page nav-walk generates 20 genuine backend requests (up from 2). Commit `714b774` in `browser-mcp`.

**Lesson for the rest of the queue**: if a repo's request-log instrumentation shows near-zero backend traffic during nav-walk, check for relative `fetch()` calls in the webapp BEFORE assuming it's sandboxing/isolation. Tauri's SPA-fallback masking is cheap to check (`grep -rn "fetch('/" webapp/src`) and should probably be step zero, ahead of reaching for CDP. This is now also documented as CRITICAL PITFALL #2's companion finding in `standards/rules/cua_nsis_smoke_testing.md`.

---

## Bugs discovered and fixed (2026-09-17 session — read before repeating them)

### 1. `uv run pyinstaller` resolves to the wrong environment
`uv run pyinstaller` runs in the isolated global uv-tool environment, not the project's own venv. Symptom: `PackageNotFoundError` for some package at runtime, from a build with no build-time errors. **Fixed fleet-wide** (89 files, 57 repos) — `pyinstaller`/`pefile`/`altgraph` added as dev deps, build scripts invoke `.venv\Scripts\pyinstaller.exe` directly. Canonical template: `templates/tauri-native/native/build.ps1`. ~158 repos outside the queue still have this bug untouched.

### 2. CUA smoke tests silently skip ALL GUI verification if `pywinauto` is missing
`cua_available()` checks `import pywinauto` in **the target repo's own venv**. Missing it means every GUI phase silently skips, but the old script still printed "ALL PHASES PASSED." **Fixed** (`CUA_SMOKE_VERSION` 6+): loud warning + refuses false "ALL PHASES PASSED." `pywinauto`/`pillow`/`pytesseract` added to 59 repos, import-verified but not all build-tested.

### 3. CUA test *config* bugs look exactly like app bugs
Always check `nav_routes`/`bridge_ok_text` in `cua-nsis-config.json` against the REAL sidebar component source before concluding a failure is an app bug. Hit on `teleoperator-mcp` and `benny-the-dog-mcp` — both had guessed/stale labels causing fake failures.

### 4. Recurring PyInstaller packaging bug family (missing/stripped metadata, missing binaries)
Any `ImportError`/`ModuleNotFoundError`/`PackageNotFoundError` from a frozen exe that works fine unfrozen is almost always: (a) `SKIP` binary-exclusion list over-stripping a genuinely-needed package, (b) missing `copy_metadata()` for a package needing `importlib.metadata` at import time, (c) missing `hiddenimports`/`collect_submodules`. **Always test the standalone frozen exe directly** (`PYTHONUNBUFFERED=1 ./resources/{repo}-backend.exe --mode http --port <free>`) before rebuilding the full Tauri bundle each iteration — much faster.

**2026-09-20 addition (browser-mcp)**: a subtler variant — the spec correctly called `copy_metadata()` to inject dist-info, but a dist-info-stripping block ran **after** it and deleted what it had just added, making the injection a structural no-op. Also: `copy_metadata()` returns the dist-info **directory** as one TOC entry, but PyInstaller's `datas` TOC needs individual **file** entries — must `os.walk()` and expand. Also hit: `fastmcp.FastMCP` uses a `TYPE_CHECKING`-guarded export that breaks when frozen (use `from fastmcp.server.server import FastMCP` instead); `mcp.types` needs an eager import in the entry point before `fastmcp` touches it.

### 5. Missing `--mode http` / env-var translation
`backend.rs` may set `PORT` but the PyInstaller entry point might not translate that into HTTP mode, causing silent stdio fallback. Check whether the spec's entry point (`__main__.py` vs `run_server.py`) actually does this translation.

### 6. `.gitignore`'s bare `*.spec` rule can catch hand-maintained PyInstaller specs
Found on `bilibili-mcp`. Check `git ls-files | grep spec` before assuming it's tracked.

### 7. Background subagents don't get woken up automatically
A subagent that backgrounds a Rust compile and ends its turn saying "I'll wait for completion" is wrong — it just stops. The parent session must explicitly resume it. Tell agents explicitly to arm a real `Monitor` (or equivalent) and check actual state, not assume re-invocation.

### 8. `just` on Windows runs each recipe LINE as its own PowerShell process
`$LASTEXITCODE` does NOT persist across lines in a multi-line recipe — chain a check and its action with `;` on the same line. Don't wrap lines in a redundant nested `powershell -NoProfile -Command "..."` (the line already runs under PowerShell; nesting causes `$`-variable double-interpolation).

---

## Fleet standard docs to read for full detail

- `standards/TAURI_PRODUCTION_PITFALLS.md` sec 13 #13 — the `uv run pyinstaller` bug.
- `standards/rules/cua_nsis_smoke_testing.md` — both CRITICAL PITFALL sections (missing pywinauto; OCR false-pass + backend-receipt-proof), Requirements table, Backend Request-Log Instrumentation section.
- `standards/rules/tauri_nsis_building.md` — canonical `just tauri` / `just tauri-preflight` composite recipe (justfile recipes section).
- `templates/tauri-native/native/build.ps1`, `templates/tauri-native/scripts/cua-smoke.py` (`CUA_SMOKE_VERSION = 8`) — canonical templates.
- `reports/drift-2026-09-17.md` — the original 54-repo drift scan the queue was built from.
- `CHANGELOG.md` — dated entries for both sessions.

## Exact next steps

1. **Add the request-log endpoint to `kicad-mcp` and every repo you touch next** — it's the difference between a trustworthy CUA pass and one that only proves UI rendering.
2. **`kicad-mcp` first** (user priority): re-verify properly — check what the "manual queue run" commit actually did, clean up uncommitted build artifacts, update `BUILD_LOG.md`, run a genuine CUA pass with the request-log instrumentation.
3. Then `chip-design-mcp`, `logic-analyzer-mcp`, `oscilloscope-mcp`, `database-operations-mcp`, `virtualization-mcp` (the latter two aren't in the original drift scan — they were added to the queue 2026-09-17, have `native/`+`src-tauri/` scaffolding, dev deps already added).
4. Then the rest of the queue, one repo at a time: `assfix` → `nsis-build` (with the request-log-equipped `cua-smoke.py` v8+) → genuine verification.
5. Consider a lower-priority pass to add request-log instrumentation retroactively to the 5 "done" repos and re-verify their data-fetch connectivity.
6. **Commit discipline unchanged**: each repo's fix stays uncommitted until that repo's own build+CUA run proves it works. Batch Mutation Safety hard rule: max 5 files per operation/commit; `.bak` backups before any 3+ file scripted edit.
