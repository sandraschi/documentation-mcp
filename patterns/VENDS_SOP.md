# VENDS SOP — vendor standard Apps + LLM + Speech surfaces into a repo

**Macro:** `vends <repo> [surfaces]` (see `standards/rules/agentic_macros.md` §vends).
**Scope:** one repo per run, or a comma list (hard cap: 5 repos — batch rule).
**Provenance:** built 2026-09-06 vendoring arxiv-mcp (Apps hub + LLM switch/telemetry/templates). Speech surface + `-Surfaces` param added 2026-09-15 (extracted from japanophile-mcp's speech-mcp crossconnect).

**Surfaces param** (comma list, default `apps,llm` — unchanged from the original two-surface tool):

| Surface | Automation | What it does |
|---|---|---|
| `apps` | Fully scripted | Phase 1 below — `vendor-apps-page.ps1` |
| `chat` | Scripted page, hand content | Phase 1 below — `vendor-apps-page.ps1 -Pages chat` (route + presets seed; personalities/presets/skills-in-preprompt rewritten per repo, never verbatim) |
| `llm` | Merge only, not scripted | Phase 2 below — needs agent/human judgment, never blind-copied |
| `speech` | Fully scripted | Phase 3 below — `patterns/templates/speech-crossconnect/` |

**For tools without opencode's text-macro trigger** (Claude Code, Cursor, "agy",
anything that can't type `vends X` and have it expand): `just vends <repo>
[surfaces] [dryrun=1]` from the mcp-central-docs root runs the same thing —
see `scripts/just/vends.ps1`. It fully automates `apps` and `speech` (pure
mechanical copy, no judgment needed) and, for `llm`, prints the Phase 2 steps
and template paths instead of guessing at a merge — the same content an agent
following the macro would read, just surfaced as script output instead of a
prompt expansion.

## 0. Preflight (read-only)

1. `cd D:\Dev\repos\{repo}` — confirm layout: `web/` or `web_sota/` + python `src/`.
   No webapp → STOP (nothing to vend into; say so).
2. Registry entry exists (`fleet-registry.json` + `WEBAPP_PORTS.md`); note ports.
3. `git status` — dirty tree is OK but REPORT it (vendoring on top of uncommitted
   work is allowed; losing track of whose change is whose is not).
4. Read `standards/APPS_PAGE_STANDARD.md` §6 (vendor contract) and
   `templates/llm/SETTINGS_LLM.md` (the six LLM rules). Do not rely on memory.

## 1. Phase 1 — Apps page (scripted)

1. Run the vendor script (never hand-copy):
   `pwsh -File D:\Dev\repos\mcp-central-docs\scripts\vendor-apps-page.ps1 -Target {repo}`
   (omit `-From` unless the reference moved; never `-All` inside a vends run).
    Additional standard pages ship from the same script via `-Pages`:
    `-Pages logs` (template `templates/logging/`, needs `/api/logs` backend),
    `-Pages chat` (template `templates/chat/`, needs `/api/llm/chat` + stream;
    presets seed once, never overwrite; personalities/WELCOME_MSG/chips and
    skills-in-preprompt are PER-REPO — rewrite, never copy verbatim, see the
    godot drift exhibit in the template header; MicButton/SpeakButton are
    optional, delete without a voice stack; never vendor over a repo's own
    Chat page blindly, diff first). Run each, close every WARNING.
2. Read its output line by line and close every WARNING it prints:
   - "route patch skipped" → wire `/apps` manually (import + `<Route>`, standard
     App.tsx only; OnboardingGate layouts stay manual — say so and stop there).
   - "fix the API_BASE import by hand" → point the page at the repo's own client.
   - "add gh-green by hand" → add the token (CSS var + tailwind color).
   - "wire register_apps_routes by hand" → add the one-line call (never paste
     the whole module; it lives in `services/apps_routes.py`).
3. If the script reports "custom /api/apps* already present", it copied support
   modules only — verify the custom endpoints still satisfy §4.2 of the standard
   (`/api/apps`, `/api/apps/health`, `/api/apps/ensure` shapes).

> GATE: script ends `vendor done`, `py_compile` clean, and a re-run is a
> no-op (up-to-date/skips only). A re-run that still copies or wires is a
> script bug — fix the script first (see 2026-09-06: wiring fired despite
> custom-routes skip; `${var.prop}` display bug).

## 2. Phase 2 — LLM surfaces (merge, never overwrite)

Inventory FIRST: what LLM surface exists? (`/api/llm/*`, settings file,
provider cards, key inputs, chat proxy.) Then fill gaps — additive only:

1. **Backend engine:** vendor `templates/llm/llm_engine.py`
   (switch/unload/loaded/vram — stdlib+httpx, no repo deps). Target:
   `<pkg>/services/llm_engine.py`.
2. **llm_ops tool:** adapt `templates/llm/llm_ops_snippet.py` (2-line header).
   `list_models` stays repo-specific — never template the registry/keystore.
3. **Frontend lib:** sync `templates/llm/lib-llm.ts` helpers INTO the repo's
   own client (selection broadcast/subscribe, unload, loaded, switch types).
   Merge by diff — never overwrite the repo's client (API paths differ).
4. **AI settings page:** add `ActiveLlmCard` + `AiSettingsPage` as NEW files
   only (`templates/llm/*.tsx`, fix the 3 import lines). Add route + nav entry.
   NEVER edit or delete the repo's existing Settings content to make room —
   AI settings move by repo-owner decision, not by vendoring.
5. **Backend endpoints** (gap-fill against the card header contract):
   settings get/save, providers, models, gpus, loaded, unload, install,
   onboarding, chat/stream. Reuse `llm_engine` — no second implementation.
6. **No-auto-pick audit:** grep `models[0]` + hardcoded model defaults in the
   webapp (`{,web_sota}/src`). Every hit must become empty-until-selected
   (BUG-030). Quote each fixed site in the report.
7. **Cloud keys:** provider cards must have per-provider key save/clear/test
   wired to the backend keystore. Keys in localStorage/env dumps = STOP item.

> GATE: no `models[0]` fallback remains; empty selection loads nothing;
> save switches VRAM and reports evicted/warmed; kick-out + telemetry work.

## 2b. Phase 2b — Fold-in (repo-owner decision, same run or follow-up)

Phase 2 deliberately lands AI settings on a SEPARATE page (`AiSettingsPage` +
route + nav) and never touches the repo's existing Settings. That separation
is scaffolding, not the end-state: left unasked, it fossilizes (inkscape-mcp
kept a standalone AI Settings page nobody asked for — local + cloud cards
belong on the normal Settings page). So every vends run MUST ask the
repo owner one question before closing Phase 2:

**"Fold the LLM cards into Settings now, or keep the separate AI page?"**

- **Fold (default recommendation):** move `ActiveLlmCard` +
  `LlmProviderCards` into the repo's `settings.tsx` (replacing any
  link-card that points at `/ai-settings`), update the Settings header copy,
  remove the `/ai-settings` route + nav entry, repoint deep links
  (`LlmOnboarding` banner buttons, chat empty-state links) at `/settings`,
  delete the `ai-settings.tsx` page file. Keep every `llm-*` card-level
  testid; the page-level `ai-settings-page` testid goes away with the page.
  Onboarding banners (`LlmOnboarding mode="banner"`) stay where they are —
  only the `full` composition moves.
- **Keep separate (owner explicitly says so):** record the reason in the
  report. Revisit next time the repo's Settings is touched anyway.

> GATE: exactly ONE place hosts the provider cards (Settings XOR AI page,
> never both, never a link-card pointing at a page that no longer exists);
> `tsc --noEmit` + `biome check` clean; no dead `/ai-settings` links
> (`grep ai-settings webapp/src` returns only history/docs or nothing).

## 3. Phase 3 — Speech (scripted, only when `speech` is in -Surfaces)

Pure mechanical copy — no merge judgment needed, unlike LLM. Full detail and
the three bugs already found (so you don't rediscover them) live in
`patterns/templates/speech-crossconnect/README.md`.

1. Run `just vends {repo} speech` (or `-Surfaces speech` directly via
   `scripts/just/vends.ps1`). It copies `crossconnect_base.py` (skipped if
   already present from a prior peer's vends run) + `speech_crossconnect.py` +
   `speech_routes.py` into `src/<pkg>/services/`, and `crossconnect.ts`
   (same skip rule) + `speech.ts` + `SpeechControls.tsx` + `MicButton.tsx` +
   `WakeWordToggle.tsx` into `webapp/src/lib/` + `webapp/src/components/`.
   Existing files of the same name get a timestamped `.bak` first.
2. Close the printed NEXT STEPS: register `register_speech_routes(app)` in
   your app factory, fix the `../lib/speech` import path if your alias setup
   differs, drop `<SpeechControls>` wherever you want a Listen button, and
   `<MicButton>` wherever you want voice input (browser-only — no backend
   wiring needed for that one, it never calls speech-mcp). `WakeWordToggle`
   is NOT per-tab STT — it starts a background mic listener on the machine
   running speech-mcp; read its warning copy before wiring it up.
3. If the repo has no single `src/<pkg>/` directory or no `webapp/`, the
   script warns and skips that half — do it by hand from the template dir.

> GATE: `ruff check` / `tsc --noEmit` clean on the copied files; a manual
> click of the Listen button actually plays audio (or shows the graceful
> "speech-mcp not reachable" message if speech-mcp isn't running — not a
> traceback either way).

## 4. Phase 4 — Verify

1. `ruff check` + `ruff format --check` (backend incl. new services/utils).
2. `pytest -q` full suite (add endpoint tests for every new route:
   hub lists, health closed-port false, ensure-unknown fails safe,
   unload/unloaded shapes, non-ollama 400s).
3. `biome check` + `tsc --noEmit` + `bun run build` in the webapp.
4. Backend delivery note: NSSM-kind repos reuse healthy backends — new code
   needs a service bounce (`sc stop/start`, UAC). Say so explicitly.
5. Manual click-test checklist for the user (cannot be done headless):
   Apps card stop→click→spinner→green→browser; Settings save→evict message;
   Kick→VRAM drains within ~5s; fresh profile selects nothing until picked.

## Anti-patterns

- **Overwriting settings:** the fastest way to destroy trust. New files + new
  route only. If the repo has no clean seam, STOP and ask.
- **Separate AI page fossilizing:** Phase 2 lands a standalone AI page and
  Phase 2b asks the fold question every run. A vends report that never
  records the owner's fold/keep decision is incomplete — the page stays
  separate by default, which is scaffolding, not a decision.
- **Hand-copying** Apps/LLM code instead of the script/templates (drift on day one).
- **Partial backend:** page without endpoints (the pre-v4 failure — dead UI).
  Every frontend call must resolve to a live route; prove with tests.
- **Batch > 5:** one vends run = max 5 repos. Fanout uses the script's `-All -Batch 5`.
- **Skipping the re-run:** the idempotency re-run IS the verification. If it
  still changes files, something is wrong with the script or the wire-up.

## Report

Table per repo: Apps (script output summary) / LLM gaps filled / no-auto-pick
sites fixed / keys OK / gates (ruff, pytest x/y, biome, tsc, build) / backend
bounce needed? / manual click-tests for the user. Plus: template/script fixes
made along the way (file + what). Plus: the Phase 2b fold/keep decision and
the owner's reason.
