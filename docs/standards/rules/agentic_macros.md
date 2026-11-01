---
title: "Agentic Macro Operations (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-15
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Agentic Macro Operations (SOTA 2026)

**Established**: 2026-07-02

Certain user utterances should expand to a defined set of operations rather than a literal single action. This prevents gaps where the agent does the bare minimum of what was said rather than what was intended.

## Repo Discovery (Read Before Any Subagent Task)

**Subagents exploring a repo MUST run `patterns/REPO_DISCOVERY_SOP.md` first** to locate the actual source root. The fleet has two layouts: `src/{package}/` (standard) and `{package}/` at root (legacy flat). A subagent checking only `src/` will falsely report flat-layout repos as "empty scaffold."

## SOP Chaining Convention

SOPs live in `mcp-central-docs/patterns/*.md`. Macros call SOPs by reference -- the expanded step reads `patterns/SOP_NAME.md` during execution:

```
1. Read `patterns/DOC_SYNC_SOP.md` -- full SOP
2. Execute Phase 1 (Inventory & Validate)
...
```

Conventions:
- **A macro's expanded steps may call `read patterns/{name}.md`** to load an external SOP. This avoids duplicating SOP text inside the macro definition.
- **A macro may also name a SOP inline** in its description as a reference for the agent to look up (e.g. `See patterns/DOC_SYNC_SOP.md`).
- **SOPs may reference other SOPs** by path -- the agent resolves them by reading at execution time.
- **No SOP file should be inlined into a macro.** If the same SOP appears in two macros, extract it.

## Standard Macros

### `fix all`

Trigger: user provides a list of issues (from meta-mcp, code review, audit, grader) and says "fix all".

Expands to:

1. **Read every flagged issue** -- understand each deficiency
2. **Fix each issue** in order of severity (HIGH → MEDIUM → LOW)
3. **Fix pre-existing gate failures found along the way** -- every lint error, typecheck error, test failure, broken import, syntax error encountered in files you touch or that block verification. See CLAUDE.md §5 "Fix Gates Before You Leave Them"
4. **Verify** -- run linter, typechecker, and test suite. Repeat until all pass
5. **Report** -- list what was fixed, what was out of scope and why

### `update docs`

Trigger: "update docs" or "update documentation" in the context of a repo.

Expands to:

1. Read `patterns/DOC_SYNC_SOP.md` -- full SOP
2. Execute Phases 1-5 (Inventory, MCD Page, Content Audit, FLEET_INDEX, Commit)
3. Run verification checklist at the end of the SOP

Scope: **files only.** It refreshes `HANDOVER.md` if the repo has a stale one, and it
stops at the commit. It does not post to Discord and does not message Fritz -- Phase 6 of
the SOP is deliberately not part of this macro. Use `report work` for that.

### `report work`

Trigger: "report work", "post the work report", "tell Fritz".

Expands to:

1. Discord -- `fleet_ops(operation="work_report", channel="fleet-{repo without -mcp}")`,
   or `python D:\Dev\repos\git-github-mcp\scripts\run_work_report.py --channel <name>`.
   Long reports split into alphabetic blocks under the 2000-char limit; never truncate
   with "... and N more".
2. Fritz -- `agent_send(to_entity="fritz", subject=..., body=...)` (fleet-agent-mcp hub
   inbox) when another agent has to act on the change, or a fleet-wide invariant moved
   (a port block, a gate, a hard rule).

Both are outward-facing. **Confirm before sending**, and say which channel. Routine
doc syncs and typo fixes do not earn a notification.

### `ship`

Trigger: "ship it" or "release" after work is complete.

Expands to:

1. Check `.nopublish` -- abort if present
2. Run all gates (lint, typecheck, tests) -- abort on fail
3. Run `just build-native` (if Tauri) or equivalent build
4. Verify artifact exists (NSIS exe, wheel, etc.)
5. `git add`, `git commit`, `git push`
6. Create GitHub release from tag (if version bumped)

### `nsis build`

Trigger: "nsis build <repo>" -- build NSIS installer + CUA smoke test.

Expands to:

1. `cd D:\Dev\repos\{repo}`
2. Pre-flight: verify `native/`, `tauri.conf.json` targets `["nsis"]`, resources are `.env.example` not `.env`. Fix if wrong.
3. Pre-flight CUA: verify `scripts/cua-smoke.py` has title-matching nav (`descendants(title=label)`) -- NOT coordinate-only; verify `scripts/cua-nsis-config.json` has `nav_routes` (else nav walk skips). Sync from `mcp-central-docs/templates/tauri-native/scripts/cua-smoke.py` (v3+) if missing. See `cua_nsis_smoke_testing.md` § Nav Click Strategy.
4. Build: `just build-native`
5. Gate: `native/target/release/bundle/nsis/*-setup.exe` >= 1 MB
6. Smoke: `just cua-nsis-test` -- **MUST pass the nav phase**: distinct screenshots per page (different byte sizes), live `/api/*` calls per page, no duplicate captures. Identical screenshot sizes = nav walk failed (fake pass).
 7. Webapp: `just cua-webapp-test` (if webapp/ exists) -- pre-Tauri browser walk: stack starts via `start.ps1 -Headless`, waits for the **Connected badge** (webapps show "Connecting..." while the backend boots -- wait with timeout + retry, not instant-fail), then title-matching nav walk in the browser. See `cua_webapp_testing.md`.
 8. Report: path, size, phase results
 9. Link (mother rule): run `mcp-central-docs/scripts/sync-tauri-starts.ps1`
    so `D:\Dev\Tauri starts\{repo}-setup.lnk` points at the fresh installer.
    A build without a linked shortcut is not shipped.

### `cuatest` (aliases: `cua-webapp-test`, `webapp test`)

Trigger: "cuatest <repo>" or "cua-webapp-test <repo>" -- run the pre-Tauri browser walk on any repo, no build needed.

Expands to:

1. `cd D:\Dev\repos\{repo}`
2. Pre-flight: verify `scripts/cua-webapp-test.py` + `scripts/just/cua-webapp-test.ps1` exist; verify config has `frontend_port` + `nav_routes` (sync from `mcp-central-docs/templates/tauri-native/` if missing). Missing config keys = nav walk skips -- fix before running.
3. Kill stale processes on the repo's backend/frontend ports (see `operations/WEBAPP_PORTS.md`)
4. Run: `just cua-webapp-test` -- stack via `start.ps1 -Headless` → backend health → frontend ready → browser → **Connected badge wait** (webapps show "Connecting..." while backend boots -- wait + retry up to `connected_timeout`, do NOT instant-fail) → title-matching nav walk → diagnostics
5. Verify: distinct per-page screenshots in `cua-reports/webapp-{page}.png` (different byte sizes, not N copies of the dashboard)
6. Cleanup: ports freed (script does this)
7. Report: phase results, screenshot list

Note: this is the dev-loop test -- no NSIS build. For the installed-app test use `cuatesttauri`.

### `cuatesttauri` (alias: `cua-nsis-test`)

Trigger: "cuatesttauri <repo>" or "cua-nsis-test <repo>" -- run the NSIS smoke test on an already-built installer.

Expands to:

1. `cd D:\Dev\repos\{repo}`
2. Pre-flight: verify `scripts/cua-smoke.py` has title-matching nav (`descendants(title=label)`, template v3+) and config has `nav_routes`; verify a built installer exists (`native/target/release/bundle/nsis/*-setup.exe` or `dist/`). Build it first with `just build-native` if missing (or the `nsis build` macro).
3. Run: `just cua-nsis-test` -- install → launch → backend health → **nav walk (MUST step through sidebar: distinct per-page screenshots, live `/api/*` calls)** → uninstall
4. Verify: distinct per-page screenshots (different byte sizes), no duplicate captures. Identical sizes = nav walk failed (fake pass) -- fix the smoke script before certifying.
5. Report: phase results, installer path

Note: this installs/uninstalls the app -- interactive desktop automation. For the pre-Tauri dev-loop use `cuatest`.

### `theworks`

Trigger: "theworks <repo>" -- the full repo pipeline: **assfix → fakefind → ghaudit → cuatest**.

Runs the four standalone macros in dependency order, each gated on its report artifact.
Sequencing rationale: assfix mutates + pushes first (so the later read-only audits and the
functional test see the fixed state); fakefind audits UI honesty against the fixed code;
ghaudit reads GitHub metadata/CI *after* the push so runs are fresh; cuatest proves the
webapp actually boots and walks.

Expands to:

1. `cd D:\Dev\repos\{repo}`
2. **assfix {repo}** -- full assess → fix → lint → docs → MCPB build → verify → push pipeline
   (see `patterns/repo-assess-and-fix.md`). The only mutating stage.
   > GATE: `reports/assess-*.md` exists with SOTA score; lint + pyright + tests pass; pushed (skip git if `.nopublish`).
   > If assfix fails a CRITICAL gate, STOP -- do not run the rest on a broken repo.
3. **fakefind {repo}** -- read-only webapp audit for mock data / dead buttons / fake stats
   (see `patterns/FAKEFIND_AUDIT_SOP.md`). Report only -- no auto-fix.
   > GATE: `reports/fakefind-*.md` exists.
4. **ghaudit {repo}** -- per-repo GitHub hygiene scan: issues, PRs, CI, topics, description,
   releases, bug cross-ref (see `patterns/GHAUDIT_SOP.md`). Report only.
   > GATE: `reports/ghaudit-*.md` exists + `.ghaudit-timestamp` written.
5. **cuatest {repo}** -- pre-Tauri browser walk: stack via `start.ps1 -Headless` → backend
   health → Connected badge wait → nav click-through → distinct per-page screenshots.
   > GATE: `cua-reports/webapp-*.png` distinct byte sizes (fake pass if all identical).
   > Skip gracefully if no `webapp/` or no `frontend_port` in config.
6. Optional: **cuatesttauri {repo}** -- installed-app cert if a built installer exists
   (heavy: install → nav walk → uninstall). Ask the user first.
7. Report: one summary table -- SOTA score, fakefind findings, ghaudit flags, cuatest phase results.

Anti-patterns:
- **Reordering**: fakefind/ghaudit before assfix audits the dirty state and ghaudit reads
  pre-push CI -- results are misleading. assfix must be first.
- **Skipping gates**: each stage writes a report artifact; if the artifact is missing, the
  stage did not run -- do not claim it passed.

### `vends`

Trigger: "vends <repo> [surfaces]" (aliases: "vendor <repo>", "vends <repo1>, <repo2>" -- hard cap 5 repos).
`surfaces` is an optional comma list from `apps,chat,llm,speech` (default `apps,llm`,
unchanged from the original two-surface tool). Non-opencode tools (Claude Code,
Cursor, "agy" -- anything without this text-macro trigger) get the same effect via
`just vends <repo> [surfaces] [dryrun=1]` from the mcp-central-docs root
(`scripts/just/vends.ps1`) -- it fully automates `apps` and `speech`, and for
`llm` prints the Phase 2 steps below instead of guessing at a merge.

Vendors the requested standard surfaces into a repo, one run. Full SOP:
`mcp-central-docs/patterns/VENDS_SOP.md` -- READ IT BEFORE EACH VENDS RUN.

Expands to:

1. `cd D:\Dev\repos\{repo}` + preflight (VENDS_SOP §0: layout, registry, git status,
   read APPS_PAGE_STANDARD §6 + SETTINGS_LLM rules).
2. **Phase 1 -- Apps** (if `apps` requested): `vendor-apps-page.ps1 -Target {repo}`
   (never `-All` here, never hand-copy). Close every WARNING it prints (route,
   API import, token, route wiring). Custom `/api/apps*` present → support
   modules only.
   **Phase 1b -- Chat** (if `chat` requested): same script with `-Pages chat`
   (route + presets seed; needs `/api/llm/chat` backend). Then hand work:
   rewrite personalities/presets for the repo (never ship the template's),
   drop voice buttons without a voice stack, diff before touching an
   existing Chat page.
   > GATE: re-run is a no-op (up-to-date/skips). A re-run that still copies or
   > wires is a script bug -- fix the script first, then continue.
3. **Phase 2 -- LLM** (if `llm` requested; merge, never overwrite): vendor
   `llm_engine.py`, adapt the `llm_ops` snippet (`list_models` stays
   repo-specific), merge `lib-llm.ts` helpers by diff, add
   `ActiveLlmCard`/`AiSettingsPage` as NEW files + route + nav, gap-fill
    backend endpoints reusing `llm_engine`, no-auto-pick audit (`models[0]` →
    empty-until-selected, BUG-030), cloud key save/clear/test.
    Then Phase 2b fold question (VENDS_SOP §2b): ask the owner whether the
    LLM cards fold into the repo's Settings now (default recommendation) or
    keep the separate AI page with a recorded reason -- never leave the
    separate page as an unasked default.
    > GATE: empty selection loads nothing; save switches VRAM with evict report;
    > kick-out + telemetry work. NEVER edit/delete the repo's existing Settings.
4. **Phase 3 -- Speech** (if `speech` requested; scripted, no merge judgment):
   copy `crossconnect_base.py`/`crossconnect.ts` (shared base, skipped if a
   prior peer's vends run already placed them) + `speech_crossconnect.py`/
   `speech_routes.py`/`speech.ts`/`SpeechControls.tsx`/`MicButton.tsx`/
   `WakeWordToggle.tsx` from `patterns/templates/speech-crossconnect/`
   (existing files back up first), register the routes, wire the components
   (`MicButton` is browser-only STT, no backend wiring needed;
   `WakeWordToggle` is NOT per-tab STT -- it's a machine-wide mic listener
   toggle, read its warning copy first). That template's README documents three real
   bugs already found in speech-mcp (Gemini voice_id="default" 500s on POST,
   Gemini's 10-20x latency vs SAPI needing a
   45s timeout, never hardcode a voice list) -- read it, don't rediscover them.
5. **Phase 4 -- Verify:** ruff, full pytest (+ endpoint tests per new route),
   biome, tsc, `bun run build`. NSSM-kind repos need a service bounce for new
   backend code -- say so explicitly.
6. Report: per-repo table (surfaces vendored / LLM gaps / no-auto-pick sites /
   keys / gates / bounce needed / manual click-tests) + template/script fixes made.

Anti-patterns:
- **Overwriting settings** to make room -- new files + new route only, or STOP.
- **Partial backend** (page without endpoints). Every frontend call resolves
  to a live route, proven by tests.

### `certify`

Trigger: "certify" or "certify the build".

Expands to:

1. `ruff check src/`
2. `uv run pyright src/` (+ `api/` when present)
3. `tsc --noEmit` (if webapp)
4. `uv run pytest` or `just test`
5. `just cua-nsis-test` (if native/) -- **verify the nav phase actually walked**: distinct per-page screenshots, not N copies of the dashboard
6. `just cua-webapp-test` (if webapp/) -- pre-Tauri walk: Connected badge wait + nav click-through
7. `npx playwright test` (if webapp/e2e)
8. Report pass/fail per gate

### `repconv` (aliases: `rustify`, `convert to rust`)

Trigger: "repconv <repo>" or "rustify <repo>" -- low-token, belt-and-suspenders ("Gürtel und Hosenträger") conversion of a legacy Python/FastMCP + React/Vite/Tailwind repository into a crashproof Pure-Rust ArtCraft 4-crate workspace (`D:\Dev\repos\rust-<repo>`).

Full SOP: `mcp-central-docs/patterns/REPCONV_SOP.md` and `mcp-central-docs/standards/rust-artcraft/FLEET_CONVERSION_STANDARD.md` -- READ BEFORE EACH REPCONV RUN.

Expands to:

1. **Phase 0 -- Forensic Due Diligence & `docs/CONVERSION_DOSSIER.md` Gate (MANDATORY BEFORE ANY `.rs` CODE):**
   - **100% Read-Only Legacy Fence:** Never edit, move, stop, or lock anything in `D:\Dev\repos\<repo>` during Shadow Mode conversion; record `git -C D:\Dev\repos\<repo> rev-parse --short HEAD`.
   - **TOKEN-MISER HARD RULE:** Never read `node_modules/`, `.venv/`, Tailwind configs, or FastAPI boilerplate. Do read `AGENTS.md`, `llms-full.txt` (or `server.py`), `.env.example`/`config.yaml`, `service/`/`native/`, the 1--4 core Python protocol files (or distill via local Ollama `gemma4:12b`), `sidebar.tsx`, each route file, and the one component that places that page's controls. Screenshot the running legacy webapp first (`docs/parity/legacy/`). A page list without those frames is not Phase 0.
   - **Write & Commit `docs/CONVERSION_DOSSIER.md` + `docs/CONVERSION_LOG.md` First:** Document (1) Bucket & privilege-split/binary audit, (2) live service/port/SQLite contention strategy (`SQLITE_OPEN_READ_ONLY` + `busy_timeout`), (3) legacy git SHA, (4) complete 1:1 MCP tool + portmanteau `operation=` mapping table, (5) `.env`/config/DB path inventory for `import.rs`, (6) write-safety/actuator guards, and (7) the oracle plan: every legacy page, every primary gesture, and the legacy screenshot path for each. See `standards/rust-artcraft/ORACLE_LOOP.md`.
2. **Phase 1 -- Mechanical Workspace Stamp (70% Reusable Kernel from `rust-devices-mcp`):**
   - Create `D:\Dev\repos\rust-<repo>` and copy the proven workspace skeleton (`Cargo.toml` with `deny(unwrap_used, expect_used, panic, todo, unimplemented)`, `justfile`, `installer/installer.nsi`, `HANDOVER.md`) and reusable modules (`bridge.rs`, `llm.rs` with `gemma4:12b` default, `error.rs`, `creds.rs`, `<domain>-store`, `vault.rs`, `registry.rs`, and the `egui` chrome shell in `app.rs`) from `D:\Dev\repos\rust-devices-mcp`. Log & commit Checkpoint 1.
3. **Phase 2 -- L1 Domain Protocol Transpilation (`crates/<domain>-core`):**
   - Transpile the wire essence from `docs/CONVERSION_DOSSIER.md` into zero-`unwrap` async Rust modules (`reqwest`, `rusqlite`, `tokio::net`, `tokio-serial`) enforcing the **10-Point Uncrashable Binary Contract** (`.get()`, char-boundary UTF-8 slicing, `with_timeout_secs`, 32 MiB payload caps, `SQLITE_OPEN_READ_ONLY` for shared DBs, `Vendor::Demo` fallback, and `import.rs` reading `../<repo>`).
   - Enforce `#[test] fn dispatch_future_is_send()`. Log & commit Checkpoint 2.
4. **Phase 3 -- L2 CLI (`--json`) + Dual-Aliased MCP `2024-11-05` Stdio Server (`crates/<domain>-mcp`):**
   - Install forensic panic hook (`%LOCALAPPDATA%\rust-<repo>\crash.log`).
   - Wire every `Command` variant to `clap` and `run_mcp_stdio()` (`stdout` pure JSON-RPC, logs strictly on `stderr`), supporting **both** `<domain>.<action>` / `<domain>_<action>` **and** legacy portmanteau `<legacy_tool>(operation=...)` aliases. Log & commit Checkpoint 3.
5. **Phase 4 -- L3 near-identical UI (`crates/<domain>-app`):**
   - Build one `Page` per legacy route, in legacy order, with legacy labels and the same primary gestures (click, drag, select, dialog). The devices shell is chrome only. Zero sync I/O on the UI thread. Zero `ctx.set_*` inside `ctx.input`.
   - Screenshot the Rust window to `docs/parity/rust/` and diff each frame against `docs/parity/legacy/`. Fix until the UI and the gesture match. Pixel-nil against Tailwind is not the bar. A missing control, a reordered group, or a gesture that does something else is a fail. Write each remaining exception in `docs/UI_PARITY.md`.
   - Only then lock `egui_kittest` goldens of the matching frames and `glyph_source_scan`. A golden of an unmatched first draft fails the phase. Log & commit Checkpoint 4.
6. **Phase 5 -- 6-Gate Certification, Live Probe & Audit Bundle:**
   - Run `cargo clippy --workspace --all-targets --all-features -- -D warnings`, `cargo test --workspace`, `cargo fmt --all --check`, MCP stdio JSON-RPC probe, and `--smoke`.
   - Run a read-only live probe against the real service/DB using imported credentials, verify `git -C D:\Dev\repos\<repo> status -s` is untouched, write `docs/PRD.md` and `docs/ASSESSMENT_<DATE>.md`, finalize `docs/CONVERSION_LOG.md` + `HANDOVER.md`, update `mcp-central-docs/projects/rust-<repo>/README.md`, commit, and push.


### `assess and fix` (aliases: `assfix`)

Trigger: "assess and fix <repo>" or "assfix <repo>" -- full repo audit, fix, docs sync, and MCPB build.

Expands to:

See `mcp-central-docs/patterns/repo-assess-and-fix.md` for full SOP with per-category checklists.

Full SOP with per-category checklists: `mcp-central-docs/patterns/repo-assess-and-fix.md`. READ IT BEFORE EACH ASSFIX RUN.

**Phase 1 -- Assess** (read-only). Catalog every gap, emit report with SOTA score.
> **PHASE GATE**: both `reports/assess-*.md` (gitignored working snapshot) AND
> `docs/assess-reports/YYYY-MM-DD.md` (identical content, COMMITTED registry copy
> for the Assess Reports page -- create the dir if missing) must exist before
> fixing, each containing the exact line `SOTA Score: {n}/100` near the top.
> A run that skips the committed copy leaves the timestamp saying "fixed" with
> no report behind it -- that is how the fleet ended up with 89 timestamps and
> almost no reports. Front-load score + one-paragraph summary (registry preview
> shows the first 500 chars), then full per-category findings with file:line
> evidence, fixed-vs-deferred, and gate outputs.
> **Pre-check**: Also verify `reports/` is in `.gitignore` (add if missing),
> verify `docs/assess-reports/` is NOT ignored (add a `!docs/assess-reports/`
> negation if a blanket pattern swallows it), and check `.ghaudit-timestamp`
> for ghaudit recency.
> **HARD RULE -- tool-availability claims require a positive test.** Before
> writing "X is not available" or deferring any check because a tool is missing,
> invoke X by its documented absolute path (`standards/AGENTS.md` §1) and read the
> result. `Get-Command x` returning nothing proves only that `x` is not on PATH --
> never that `x` is not installed; fleet tools (bun, uv, just, rg, fd) live
> off-PATH by design. No deferral without a failed positive attempt (the actual
> command run + its actual output in the report). If a tool cannot be found by any
> documented path, leave the finding OPEN and scored -- never convert it into
> "deferred with reason". (Incident 2026-10-05: "no bun on Goliath" from a bare
> `Get-Command bun`; bun was at `C:\Users\<user>\.bun\bin\bun.exe`, the false claim
> was committed and inherited by the Phase 6 rescore.)
> **HARD RULE -- scores must be cold-context.** A score is only trustworthy if the
> context that produced it did not also perform the fixes. When one session both
> fixes and re-scores in Phase 6, `score_after` drifts generous -- it rewards work
> done rather than checking it. So: (a) if one context fixes and scores, label the
> score `self-assessed (unverified)` in the report and set `score_after` as
> provisional; (b) prefer a fresh/cold context (subagent or new session) for the
> Phase 6 re-score; (c) when a cold score and a self-score disagree, the cold one is
> authoritative. (Incident 2026-10-05, comms-mcp: self-score 66 vs cold-context 34 --
> the gap was a waived HIGH and rows marked "fixed" that were not.)

**Phase 2 -- Fix** in severity order (CRITICAL → HIGH → MEDIUM → LOW).

**Phase 3 -- Lint + typecheck**. `ruff check --fix`, `ruff format`, `pyright src/`, then tsc/biome if webapp.
> **PHASE GATE**: `ruff check src/ && ruff format src/ --check && uv run pyright src/` must all pass.

**Phase 4 -- Docs**. `update docs` macro.

**Phase 5 -- Build**. MCPB pack (skip if `.nopublish`).

**Phase 6 -- Verify & push**. Write `.assess-fix-timestamp` as JSON with
`timestamp` (ISO-8601), `commit` (HEAD sha after commit), `host`, plus
`score_before` / `score_after` (re-run Phase 1 scoring after fixes -- required,
not optional; assessment-only runs set both equal) and `report`
(`docs/assess-reports/YYYY-MM-DD.md` path). Extra fields are additive; old
readers ignore them. Mint GitHub issues for every deferred finding first
(`assfix` label, banner `> Issue made by assfix ...`, max 3 per run, `ready`
only when bot-safe -- see GITHUB_HYGIENE_STANDARDS.md Bot-minted issues).
Commit, push (skip git if `.nopublish`).
> **TERMINAL GATE** -- run after Phase 6. Any FAIL means loop back to Phase 2:
> ```powershell
> $allPassed = $true
> if (Test-Path ".assess-fix-timestamp") {
>     try { $null = Get-Content ".assess-fix-timestamp" -Raw | ConvertFrom-Json; Write-Host "  [PASS] .assess-fix-timestamp exists and valid JSON" -ForegroundColor Green }
>     catch { Write-Host "  [FAIL] .assess-fix-timestamp not valid JSON" -ForegroundColor Red; $allPassed = $false }
> } else { Write-Host "  [FAIL] .assess-fix-timestamp missing" -ForegroundColor Red; $allPassed = $false }
> if (Get-ChildItem "docs/assess-reports/*.md" -ErrorAction SilentlyContinue) { Write-Host "  [PASS] committed report copy exists" -ForegroundColor Green }
> else { Write-Host "  [FAIL] docs/assess-reports/*.md missing (registry-visible copy)" -ForegroundColor Red; $allPassed = $false }
> # Also check ghaudit was run
> if (Test-Path ".ghaudit-timestamp") {
>     $gh = Get-Content ".ghaudit-timestamp" -Raw | ConvertFrom-Json
>     Write-Host "  [INFO] ghaudit last run: $($gh.timestamp)" -ForegroundColor Cyan
> } else {
>     Write-Host "  [INFO] ghaudit never run -- run 'ghaudit <repo>' for GitHub health check" -ForegroundColor Yellow
> }
> $dirty = git diff --stat
> if ($dirty) { Write-Host "  [FAIL] uncommitted changes:`n$dirty" -ForegroundColor Red; $allPassed = $false }
> else { Write-Host "  [PASS] working tree clean" -ForegroundColor Green }
> uv run ruff check src/ --quiet; if ($LASTEXITCODE -ne 0) { Write-Host "  [FAIL] ruff check" -ForegroundColor Red; $allPassed = $false }
> else { Write-Host "  [PASS] ruff check clean" -ForegroundColor Green }
> uv run ruff format src/ --check --quiet; if ($LASTEXITCODE -ne 0) { Write-Host "  [FAIL] ruff format" -ForegroundColor Red; $allPassed = $false }
> else { Write-Host "  [PASS] ruff format clean" -ForegroundColor Green }
> uv run pyright src/ --quiet; if ($LASTEXITCODE -ne 0) { Write-Host "  [FAIL] pyright" -ForegroundColor Red; $allPassed = $false }
> else { Write-Host "  [PASS] pyright clean" -ForegroundColor Green }
> if ($allPassed) { Write-Host "=== ASSFIX COMPLETE ===" -ForegroundColor Green }
> else { Write-Host "=== ASSFIX INCOMPLETE -- fix [FAIL] items, re-run gate ===" -ForegroundColor Yellow }
> ```

### `polish`

Trigger: "polish" or "clean up" at the end of a feature.

Expands to:

1. Fix all lint/type warnings (not just errors)
2. Add `data-testid` attributes to new UI elements
3. Verify dark theme consistency (no light backgrounds, color-scheme: dark)
4. Check for hardcoded tool lists (must be dynamic discovery)
5. Verify Prefab card coverage for list/status/stats tools
6. Run verification gates to confirm nothing broke

### `lint green`

Trigger: "lint green" -- make the linter pass across the complete repo.

Expands to:

1. `ruff check src/ --fix` -- Python lint + auto-fix
2. `biome check --write` -- JS/TS lint + auto-fix (if webapp present, Biome is the fleet JS/TS linter per `WEBAPP_SOTA_STANDARDS.md`)
3. Re-run both and report any remaining issues that need manual fix
4. If Biome is not available (not in repo), use `npx eslint` or the project's configured linter

### `types green`

Trigger: "types green" -- typecheck clean (Python pyright + TypeScript tsc).

Expands to:

1. `uv run pyright src/` (+ `api/` when present) -- Python types
2. `npx tsc --noEmit` in the webapp directory (if webapp present)
3. Iterate: read each error, fix, re-run until clean
4. Report what was fixed

### `gates green`

Trigger: "gates green" -- lint + typecheck + tests all green.

Expands to:

1. Run `lint green` macro -- until clean
2. Run `types green` macro -- until clean
3. Run `uv run pytest` or `just test` -- until all tests pass
4. Report: pass/fail per gate

### `start green`

Trigger: "start green" or "start environment" -- bring the full dev stack up.

Expands to:

1. Clear port zombies: `Get-NetTCPConnection` on the repo's ports → `Stop-Process`
2. Start backend: `uv run python -m {package}.server` (or `start.ps1` equivalent)
3. Health poll: poll `/api/v1/health` up to 60s
4. Start frontend: `npm --prefix webapp run dev` (or `bun run dev`)
5. Open browser to frontend URL
6. Report: URL, backend port, status

### `sync deps`

Trigger: "sync deps" or "update dependencies".

Expands to:

1. `uv sync` -- sync Python dependencies, lockfile
2. If webapp present: `bun install` or `npm install`
3. If lockfiles changed: `git add` the lockfiles
4. Report: any new/removed/changed deps

### `bump version`

Trigger: "bump version" -- increment project version across all version files.

Expands to:

1. Bump version in `pyproject.toml`
2. Bump version in `tauri.conf.json` (if native/)
3. Bump version in `glama.json` (if exists)
4. Add entry to `CHANGELOG.md`
5. `git add` the affected files

### `scan fleet`

Trigger: "scan fleet" -- after finding and fixing a bug in one repo, check all others.

Expands to:

1. Identify the antipattern or bug signature from the fix
2. Run `rg -l` across `D:\Dev\repos\` for the same pattern
3. List repos that match
4. For each: fix or file an issue
5. Update the relevant pitfalls doc in `mcp-central-docs` if the pattern is not documented
6. Report: repos scanned, matches found, actions taken

### `gh status`

Trigger: "gh status" -- quick GitHub pulse check.

Expands to:

1. `gh auth status` -- verify CLI is logged in
2. `gh api notifications --jq '.[:10] | .[] | "\(.repository.full_name) -- \(.subject.title)"'` -- unread notifications
3. `gh search issues --limit 5 --state=open "user:sandraschi"` -- or equivalent, flag open issues across fleet
4. `github_ops(operation="pr_list", owner="sandraschi", state="open")` -- check open PRs
5. Report: auth state, notification count, open PRs, any CI failures

### `zombie clean`

Trigger: "zombie clean" -- clean up stale processes and lock files.

Expands to:

1. Scan common fleet ports (Get-NetTCPConnection) for processes that have been running >4h on unused ports
2. Kill zombies by PID, escalate to taskkill /F when Stop-Process fails
3. Find and remove stale `.venv\.lock` files across `D:\Dev\repos\`
4. Find and remove `__pycache__` dirs (excluding `.venv` and `node_modules`)
5. Report: what was killed, what was cleaned

### `mcp pulse`

Trigger: "mcp pulse" -- check all MCP servers are alive.

Expands to:

1. Call `opencode_system(action="mcp_pulse")` on opencode-cli-mcp -- probes all configured MCP servers via psutil (local) or HTTP (remote)
2. Report: green check for alive, red X for dead, yellow for skipped

This replaces the old pattern of manually reading `~/.config/opencode/opencode.json` and probing each server.

### `assfixstat`

Trigger: "assfixstat" -- show which repos have been assessed/fixed and which haven't.

Expands to:

1. Scan fleet MCP repos for `.assess-fix-timestamp` (fixed) vs absent (unfixed). Filters to genuine project repos (has `pyproject.toml`, `package.json`, or `README.md` -- excludes hidden/system dirs):
   ```powershell
   $reposRoot = "D:\Dev\repos"
   $all = Get-ChildItem $reposRoot -Directory | Where-Object {
       $_.Name -notmatch '^[._]' -and $_.Name -notin @('build','dist','data','logs','temp','tmp','tools','scripts','profiles',
           'external','externals','backups','analysis','junk','quarantine','security_reports','security_tools','cua-reports',
           'tests','test','native','webapp','workspaces','_archives','_exchange','_junk','_workspaces','node_modules','.venv') -and
       (Test-Path (Join-Path $_.FullName "pyproject.toml") -PathType Leaf) -or
        (Test-Path (Join-Path $_.FullName "package.json") -PathType Leaf) -or
        (Test-Path (Join-Path $_.FullName "README.md") -PathType Leaf)
   } | Sort-Object Name
   $fixed = Get-ChildItem $reposRoot -Recurse -Filter ".assess-fix-timestamp" -Depth 3 | ForEach-Object {
       $r = $_.Directory.Name
       $c = Get-Content $_.FullName -Raw
       $isJson = $false; try { $null = $c | ConvertFrom-Json; $isJson = $true } catch {}
       $ts = if ($isJson) { ($c | ConvertFrom-Json).timestamp } else { ($c -split "`n" | Select-String "2026" | ForEach-Object { $_ -replace '.*?(2026[^\s,}]+).*','$1' } | Select-Object -First 1) }
       $reportDir = Join-Path $_.Directory "reports"
       $latest = if (Test-Path $reportDir) { Get-ChildItem $reportDir -Filter "*.md" | Sort-Object Name -Descending | Select-Object -First 1 }
       $score = if ($latest) { Select-String -Path $latest.FullName -Pattern "SOTA Score:" | ForEach-Object { $_.Line -replace '.*SOTA Score:\s*','' } }
       [PSCustomObject]@{ Repo = $r; Status = "fixed"; Date = $ts; Score = $score }
   }
   $fixedNames = $fixed | ForEach-Object { $_.Repo }
   $unfixed = $all | Where-Object Name -notin $fixedNames | ForEach-Object {
       [PSCustomObject]@{ Repo = $_.Name; Status = "unfixed"; Date = $null; Score = $null }
   }
   $result = $fixed + $unfixed
   $result | Sort-Object Status, Repo | Format-Table -AutoSize Repo, Status, @{N="Date";E={$_.Date}}, Score
   Write-Host "`nSummary: $($fixed.Count) fixed, $($unfixed.Count) unfixed / $($all.Count) total" -ForegroundColor Cyan
   ```
2. Report: table with columns Repo, Status (fixed/unfixed), Date, Score, summary line.

### `ocstat`

Trigger: "ocstat" -- full opencode status report.

Expands to:

1. Call `opencode_system(action="mcp_pulse")` -- probe all MCP servers for liveness
2. Call `opencode_system(action="config_drift")` -- check local server paths exist
3. Call `opencode_system(action="status")` -- server health, session count, config summary
4. Call `opencode_system(action="project")` -- active project context
5. Format a structured report:
   - opencode server: health check + version
   - Active project
   - MCP servers: alive/dead/skipped per-server breakdown
   - Config drift: stale paths that need cleanup
   - Known issues: list dead servers with recovery hints

### `list expansions` (alias: `list macros`)

Trigger: "list expansions", "list macros", or "what expansions do you have?".

Expands to:

Print all registered macros with their trigger phrases and a one-line summary. Current set:

| Macro | Trigger | Purpose |
|-------|---------|---------|
| `assess and fix` | "assess and fix <repo>" / "assfix <repo>" | Full repo assessment (11-category, read-only → structured report), fix in severity order, lint, docs, MCPB build, verify, push |
| `fix all` | "fix all" | Fix flagged issues, fix pre-existing gate failures, verify |
| `update docs` | "update docs" | Sync README, CHANGELOG, STATUS, PRD, llms-full.txt, HANDOVER, mcd project page. Files only -- no announcements |
| `report work` | "report work" / "tell Fritz" | Discord work report to the repo channel, and/or a hub-inbox message to Fritz. Confirm before sending |
| `ship` | "ship it" | Lint → test → build → verify → commit → push → release |
| `certify` | "certify" | Run all verification gates: ruff, tsc, pytest, cua, playwright |
| `nsis build` | "nsis build <repo>" | Pre-flight check, `just build-native`, verify .exe, `just cua-nsis-test` |
| `cuatest` | "cuatest <repo>" / "cua-webapp-test <repo>" | Pre-Tauri browser walk: stack + Connected badge + nav click-through (no build) |
| `cuatesttauri` | "cuatesttauri <repo>" / "cua-nsis-test <repo>" | NSIS smoke test on built installer: install → nav walk → uninstall |
| `theworks` | "theworks <repo>" | Full pipeline: assfix → fakefind → ghaudit → cuatest, each gated on its report artifact |
| `polish` | "polish" | Warnings, data-testid, dark theme, dynamic discovery, Prefab |
| `lint green` | "lint green" | ruff + biome to zero errors across repo |
| `types green` | "types green" | pyright + tsc --noEmit to zero errors |
| `gates green` | "gates green" | Lint + typecheck + tests all green |
| `start green` | "start green" | Kill zombies → start backend → health poll → start frontend → open |
| `sync deps` | "sync deps" | uv sync + bun install, commit lockfiles if changed |
| `bump version` | "bump version" | Bump pyproject.toml, tauri.conf.json, glama.json, CHANGELOG |
| `scan fleet` | "scan fleet" | Grep all repos for same antipattern, fix or file |
| `gh status` | "gh status" | GitHub auth, unread notifications, open PRs, CI pulse |
| `zombie clean` | "zombie clean" | Kill zombie processes on fleet ports, remove stale `.venv\.lock` files, purge `__pycache__` across repo |
| `mcp pulse` | "mcp pulse" | Check all MCP servers in opencode config are running and responding, report dead/hung ones |
| `assfixstat` | "assfixstat" | Show which repos have been assessed/fixed and which haven't |
| `ocstat` | "ocstat" | Full opencode status report -- server health, active project, MCP pulse per-server breakdown, config drift |
| `ghaudit` | "ghaudit" | Fleet-wide GitHub hygiene scan: issues, PRs, CI, topics, descriptions, stale branches, bug cross-ref |
| `spec` | "spec <feature>" | Spec-First Interview: ask clarifying questions, write SPEC.md, get approval before coding |
| `pr clean` | "pr clean" / "squash" | Squash fixup commits, rebase onto base, verify diff, push |
| `qualitycheck` | "qualitycheck <repo>" | Strategic quality assessment: originality, difficulty, wrappee, competition, tool surface, webapp, fleet integration, battlegroup fit → growth gaps |
| `audit deps` | "audit deps" | Check deps for CVEs, stale versions, incompatible licenses |
| `port check` | "port check <repo>" | Verify repo ports match fleet registry, detect conflicts |
| `env sync` | "env sync" | Sync .env.example with actual env vars used in source |
| `tag` | "tag <version>" | Create annotated git tag, push, verify CI triggered |
| `drift` | "drift" | Fleet-wide gap analysis: compare all repos against SOP without fixing |
| `wrappee drift` | "wrappee drift <repo>" / "capability audit <repo>" | Per-repo: diff tool surface against the wrapped software's current API and comparable wrappers' coverage. Report only, never fleet-wide |
| `fakefind` | "fakefind <repo>" / "find fakes <repo>" | Read-only audit of webapp for mock data, dead buttons, placeholder content, fake UI. Report only -- no auto-fix. |
| `gapfind` | "gapfind <repo>" | Read-only audit of backend REST routes + MCP tools the webapp never surfaces (and webapp calls to missing routes). Report + proposals only. |
| `onboard` | "onboard <repo>" | First-time setup: install deps, start stack, open browser |
| `template sync` | "template sync" | Compare boilerplate files against reference repos, show diffs |
| `ci check` | "ci check <repo>" | List recent CI workflow runs, identify failures, report pass/fail per workflow |
| `fork trawl` | "fork trawl <repo>" | Enumerate forks, classify real work vs autoscraped, extract patterns |
| `bench` | "bench <repo>" | Run pytest benchmarks, report regression vs last run |
| `vends` | "vends <repo> [surfaces]" | Vendor apps/llm/speech surfaces (default apps,llm) without touching repo settings -- non-opencode tools: `just vends <repo> [surfaces]` |

### `ghaudit`

Trigger: "ghaudit" -- fleet-wide GitHub hygiene scan.

Full SOP: `mcp-central-docs/patterns/GHAUDIT_SOP.md`

Expands to:

1. Follow GHAUDIT_SOP -- auth check, per-repo probes (issues, PRs, CI, metadata, stale branches, bug cross-ref), aggregate report
2. Report: fleet-wide table sorted by severity, summary counts
3. Do NOT fix anything -- present findings for user action

### `spec`

Trigger: "spec <feature>" -- Spec-First Interview for a new feature.

Full SOP: `mcp-central-docs/patterns/SPEC_INTERVIEW_SOP.md`

Expands to:

1. Follow the Spec-First Interview SOP: interview user on what/why/how/non-goals
2. Write `SPEC.md` to the repo root with: goal, requirements, non-goals, API contracts, open questions
3. Present the spec to the user for approval
4. Do NOT start coding until user explicitly approves the spec
5. Report: spec written, pending approval

### `pr clean`

Trigger: "pr clean" or "squash" -- clean up a PR branch before merging.

Expands to:

1. `git log --oneline origin/main..HEAD` -- count commits, check for fixup/squash messages
2. `git rebase -i origin/main` -- squash fixup commits, keep meaningful commit messages
3. `git diff --stat origin/main` -- verify the diff is clean and contains only intended changes
4. `git push --force-with-lease` -- push cleaned branch
5. Report: how many commits squashed, diff size, pushed

### `qualitycheck`

Trigger: "qualitycheck <repo>" -- strategic quality assessment beyond mechanical SOTA compliance.

Full SOP: `mcp-central-docs/patterns/QUALITY_CHECK_SOP.md`

Expands to:

1. Follow QUALITY_CHECK_SOP -- score 8 strategic dimensions (originality, difficulty, wrappee importance, competitive situation, tool surface, webapp quality, fleet integration, battlegroup fit)
2. **Docs quality check**: Read `patterns/DOC_SYNC_SOP.md` and execute Phase 3 (Content Audit) at minimum. Score the docs dimension (0-10) and report gaps. See DOC_SYNC_SOP for minimum standards per file.
3. Identify 3-5 growth gaps with impact ratings
4. Write report to `reports/quality-{repo}-{date}.md` + `.qualitycheck-timestamp`
5. Report: overall score, rating (Flagship/Strong/Good/Weak/Runt), top growth opportunities

### `audit deps`

Trigger: "audit deps" -- check all dependencies for security, freshness, and fleet compatibility.

Full SOP: `mcp-central-docs/patterns/DEP_AUDIT_SOP.md`

Expands to:

1. Follow DEP_AUDIT_SOP -- security scan, freshness check, license audit
2. Write report to `reports/deps-{date}.md` + `.deps-timestamp` (committed)
3. Report: security issues, stale deps, license flags. Do NOT auto-upgrade -- present findings for user decision.

### `port check`

Trigger: "port check <repo>" -- verify a repo's ports match the fleet registry.

Expands to:

1. Read `mcp-central-docs/operations/WEBAPP_PORTS.md` for the repo's registered ports
2. Grep the repo for hardcoded port numbers: `rg -n "109[0-9]{2}|108[0-9]{2}|107[0-9]{2}" src/ webapp/ -g "*.py" -g "*.ts" -g "*.tsx" -g "*.json"`
3. Check for zombie listeners: `Get-NetTCPConnection -LocalPort <port> -ErrorAction SilentlyContinue`
4. Verify `start.ps1`, `config.py`/`settings.py`, and `vite.config.ts` all use the registered ports
5. Report: registered ports, actual ports in code, mismatches, zombie processes

### `env sync`

Trigger: "env sync" -- sync `.env.example` with actual env vars used in source code.

Expands to:

1. Extract all `os.getenv("...")` / `os.environ.get("...")` calls from `src/` -- collect unique env var names
2. Extract all `import.meta.env.VITE_*` / `process.env.*` references from `webapp/src/` -- collect unique names
3. Read current `.env.example` -- list existing entries
4. Diff: find env vars in code but missing from `.env.example` (add them), and vars in `.env.example` but not in code (flag as possibly dead)
5. Add missing variables to `.env.example` with placeholder values and a comment describing what they do
6. Report: added X, flagged Y as possibly dead, total tracked

### `tag`

Trigger: "tag <version>" -- create and push a git tag for release.

Expands to:

1. Verify working tree is clean (`git diff --stat` must be empty)
2. Verify version in `pyproject.toml` matches `<version>` (or `tauri.conf.json` if native/)
3. `git tag -a v<version> -m "Release v<version>"` -- create annotated tag
4. `git push origin v<version>` -- push tag to trigger CI
5. Verify CI was triggered (check GitHub Actions via `gh` or browser)
6. Report: tag created, pushed, CI status

### `drift`

Trigger: "drift" -- fleet-wide gap analysis: compare every repo against the SOP checklist without fixing.

Full SOP: `mcp-central-docs/patterns/DRIFT_SCAN_SOP.md`

Expands to:

1. Follow DRIFT_SCAN_SOP -- enumerate repos, run lightweight probes, aggregate report
2. Write report to `reports/drift-{date}.md` + `.drift-timestamp` (committed)
3. Report: total repos scanned, pass rate, worst offenders, stale assessments

### `wrappee drift` (alias: `capability audit`)

Trigger: "wrappee drift <repo>", "capability audit <repo>", "check <repo> against <software>/competitors" -- per-repo only, never fleet-wide, never unprompted.

Full SOP: `mcp-central-docs/patterns/WRAPPEE_CAPABILITY_DRIFT_SOP.md`

Expands to:

1. Follow WRAPPEE_CAPABILITY_DRIFT_SOP Phases 1-4 for the named repo: this repo's current tool surface, the wrapped software's current real capability surface, comparable wrappers' coverage, then the diff
2. Write report to `reports/wrappee-drift-{repo}-{date}.md` (gitignored)
3. Report: gaps found (wrapped software moved / competitor covers), already-ahead items, explicitly note that nothing was built -- this macro produces a report, never a fix

Unlike `drift`, this never runs fleet-wide on its own trigger -- it always names one repo, because it requires real per-repo research (the wrapped software's actual current docs/API), not a cheap file-existence probe.

### `onboard`

Trigger: "onboard <repo>" -- interactive first-time setup for a repo you haven't run before.

Full SOP: `mcp-central-docs/patterns/ONBOARD_SOP.md`

Expands to:

1. Follow ONBOARD_SOP -- verify repo, install deps, check .env, start backend, health poll, start frontend, open browser
2. Report: ports, health status, dashboard URL, any missing config

### `template sync`

Trigger: "template sync" -- pull latest boilerplate from reference repos into this repo.

Expands to:

1. Identify which boilerplate files exist: `start.ps1`, `FleetStartMode.ps1`, `build.ps1`, `tauri.conf.json`, `hooks.nsh`, `{repo}-backend.spec`
2. For each file that exists, compare against the reference template:
   - `start.ps1` → compare with `pywinauto-mcp/webapp/start.ps1` or `email-mcp/webapp/start.ps1`
   - `FleetStartMode.ps1` → compare with `pywinauto-mcp/scripts/FleetStartMode.ps1`
   - `tauri.conf.json` → compare with `pywinauto-mcp/web_sota/src-tauri/tauri.conf.json`
   - `{repo}-backend.spec` → compare with `pywinauto-mcp/pywinauto-mcp-backend.spec`
3. Show diffs for each file that has drifted from the reference
4. Ask user which files to update -- do NOT overwrite without confirmation
5. Report: files checked, files drifted, files updated

### `ci check`

Trigger: "ci check <repo>" or "ci check <owner>/<repo>" -- check CI workflow status for a repo.

Full SOP: `mcp-central-docs/patterns/CI_CHECK_SOP.md`

Expands to:

1. Follow CI_CHECK_SOP -- list recent workflow runs, identify failures, extract failed step name and branch
2. For fleet repos, cross-reference: pre-existing failure or new? Infrastructure vs code failure?
3. Report: pass/fail table with workflow name, branch, status, failed step, age
4. Do NOT re-run, cancel, or open PRs to fix CI

### `fork trawl`

Trigger: "fork trawl <repo>" or "fork trawl <owner>/<repo>" -- classify forks of a repo by signal.

Full SOP: `mcp-central-docs/patterns/FORK_TRAWL_SOP.md`

Expands to:

1. Follow FORK_TRAWL_SOP -- enumerate forks, gather per-fork signals, classify (real work / autoscraped / derivative), extract findings from real-work forks
2. Report: table, counts, top 1-2 patterns worth investigating
3. Do NOT clone, open issues, or contact fork authors

### `bench`

Trigger: "bench <repo>" -- run performance benchmarks and report regression.

Expands to:

1. Check for existing benchmark config: `pytest.ini` has `--benchmark`, or `tests/benchmarks/` exists
2. If no bench config exists, report that and stop -- don't add benchmarks
3. Run `uv run pytest tests/ --benchmark-only -q` -- capture results
4. Compare against previous run if `.benchmark-last.json` exists in repo root
5. Report: pass/fail, regressions, improvements, save results to `.benchmark-last.json`
6. Do NOT fail CI over performance regressions -- just report them

### `fakefind`

Trigger: "fakefind <repo>" or "find fakes <repo>" -- audit a webapp for hardcoded mock data, dead buttons, placeholder content, and fake UI.

Expands to:

Full SOP: `mcp-central-docs/patterns/FAKEFIND_AUDIT_SOP.md`

1. Read `patterns/FAKEFIND_AUDIT_SOP.md` -- the full SOP
2. Execute all audit phases against the repo's webapp (read-only, no edits)
3. Write report to `reports/fakefind-{repo}-{date}.md` + `.fakefind-timestamp`
4. Present findings grouped by severity with file+line references
5. **Auto-fix endpoint mismatches**: For findings where the frontend calls a wrong port, missing URL path, or non-existent endpoint (e.g. `fetch('http://localhost:10787/...')` when registry says `10831`), fix the endpoint URL in the frontend directly -- these are objectively verifiable and safe to correct. Do NOT fabricate new API responses.
6. For all other findings (fake data, dead buttons, placeholder content), do NOT fix -- ask the user if they want fixes applied
7. If user approves, execute fixes per SOP severity order (CRITICAL→HIGH→MEDIUM)
7. Run linter and typecheck after any fixes

### `gapfind`

Trigger: "gapfind <repo>" - which backend capabilities (REST routes, MCP tools) does the
webapp never surface? The backend -> UI mirror of fakefind (UI -> backend).

Full SOP: `mcp-central-docs/patterns/GAPFIND_AUDIT_SOP.md`

Expands to:

1. Read `patterns/GAPFIND_AUDIT_SOP.md`
2. Run `uv run --project D:\Dev\repos\{repo} python D:\Dev\repos\mcp-central-docs\scripts\gapfind.py D:\Dev\repos\{repo} --out D:\Dev\repos\{repo}\reports\gapfind-{date}.md` (date from `Get-Date`)
3. Check the detection notes; 0 routes = detection failure -> rerun with `--app` / `--syspath`, never report it as clean
4. Classify every non-`used` row: SURFACE / HEADLESS / ADMIN / DEAD / DUPLICATE / REVERSE
5. Append classification + prioritized fix list to the report (existing endpoint needing only UI first)
6. Present findings; propose `.gapfind-headless` entries; do NOT fix without approval

## Adding New Macros

To add a macro, update this file and add a Domain Read List entry in
`CLAUDE.md` (global) pointing to it. Macros should be:

- **Named** with a short trigger phrase
- **Scoped** to a specific user intent
- **Listed** as concrete expanded steps (not vague)
- **Self-limiting** (stop conditions defined)

## Anti-Patterns

- **Under-expansion**: Treating "fix all" as fixing just the first issue. Expand fully.
- **Over-expansion**: Running `ship` when user only said "update docs". Start only what was said.
- **Silent expansion**: Not telling the user a macro expanded. Always report the expanded plan.
