# assfix — Fleet Repo Assess & Fix

**The single highest-leverage workflow in the fleet.** One trigger audits a repo against every fleet standard, fixes in severity order, lints, syncs docs, builds packages, and pushes.

---

## Origin: How assfix was built

assfix wasn't designed — it was **grown**. The process reveals something about how LLM-powered development works at scale.

### The problem

For three years, repos drifted. Each one started from a different template, at a different FastMCP version, with different conventions. Manual reviews caught the same issues over and over: hardcoded ports, missing `.env.example`, CORS misconfigurations, stale `llms-full.txt` files. The gap between "what the standards say" and "what the repo actually has" was never closed systematically — it was closed repo-by-repo, by hand, when someone had time.

### The scaffold: macro expansion

The breakthrough was realising that **text expansion macros** (`agentic_macros.md`) are the natural scaffolding for LLM-driven workflows. A macro is just a named trigger that expands to a defined set of operations — but because the LLM interprets it at runtime, the expansion is not a rigid script. It adapts to the repo's actual state, reads files, makes judgments, handles errors. It's a script that can think.

assfix started as a single macro definition in July 2026:

```
"assess and fix <repo>" → read every standard → check the repo → fix what's wrong → verify → push
```

That was the seed. The macro definition was ~20 lines. It pointed at the SOP document.

### The growth loop

The SOP document is the **canonical checklist** — 19 categories with severity weights and standard references. The macro says "read the checklist, execute it." So improving assfix doesn't require changing the macro — it requires changing the checklist.

The growth loop:

1. **A bug is found in one repo** → fixed locally
2. **The fleet is scanned** for the same antipattern (`scan fleet` macro)
3. **A new check is added** to the SOP (`repo-assess-and-fix.md`) so all future assfix runs catch it
4. **The macro doesn't change** — it already says "run every check in the SOP"

This is why assfix grew from 11 to 19 categories in two weeks without any macro changes. The macro just points at the checklist. Improve the checklist, improve every future run.

### What assfix taught us

- **Don't hardcode the workflow in the macro.** The macro is a pointer. The SOP is the source of truth. This separation means you can add categories, reweight severities, and update standard references without touching the trigger.
- **Phase gates are essential.** assfix won't proceed from Phase 1 (assessment) to Phase 2 (fixing) until the report file exists on disk. This prevents the agent from skipping straight to fixing without understanding the full scope.
- **The same SOP works across IDEs.** The opencode macro uses `just`/`rg`/bash. The Claude Desktop skill uses `Read`/`Grep`/`Glob`/`Edit`. The Antigravity skill is auto-loaded from `.agents/skills/`. The checklist stays the same; only the execution layer changes.
- **assfixstat closed the loop.** Without fleet-wide visibility into which repos have been assessed and at what score, assfix runs were islands. `assfixstat` scans `.assess-fix-timestamp` markers across `D:\Dev\repos` and reports fixed vs. unfixed with scores and dates. This turned assfix from a tool into a **program**.

---

## Compatibility

| IDE | Mechanism | assfix support | How to trigger |
|-----|-----------|---------------|----------------|
| **opencode** | Text expansion macro in `agentic_macros.md` (loaded via `~/.claude/CLAUDE.md`) | ✅ **Full** | Say `assess and fix <repo>` or `assfix <repo>` |
| **Claude Code** | Same as opencode — reads same `CLAUDE.md` + `agentic_macros.md` | ✅ **Full** | Say `assess and fix <repo>` or `assfix <repo>` |
| **Claude Desktop** | `assfix` skill at `skills/assfix/SKILL.md` — maps SOP to `Read`/`Grep`/`Glob`/`Edit`/`Write` | ⚠️ **Full** (load skill first) | Load skill, then `assess and fix <repo>` |
| **Antigravity** | `.agents/skills/assfix/SKILL.md` with `config.json` auto_load | ✅ **Full** (auto-loaded) | Say `assess and fix <repo>` |
| **Cursor** | `.cursorrules` — no macro expansion system | ❌ **No macro** | Must manually follow SOP |
| **Windsurf** | `.windsurfrules` — no macro expansion | ❌ **No macro** | Must manually follow SOP |
| **Zed** | No skill/plugin/macro system | ❌ **Not supported** | — |
| **GitHub Copilot** | `.github/copilot-instructions.md` — prompt injection only | ❌ **Instructions only** | No trigger mechanism |

### Phase runnability

| Phase | What | Runnable from webapp? |
|-------|------|----------------------|
| Phase 0 — Pre-flight | Detect repo type, check `.nopublish`, gather context | No (needs file access) |
| Phase 1 — Assess | 19-category read-only audit → report → `docs/assess-reports/` | ✅ meta-mcp Assfix SOP page |
| Phase 2 — Fix | CRITICAL → HIGH → MEDIUM → LOW severity order | No (needs LLM reasoning) |
| Phase 3 — Lint | `ruff`, `tsc`, `biome` — iterate until clean | Partial (lint can be triggered) |
| Phase 4 — Docs | README, CHANGELOG, `llms-full.txt` sync | No (needs LLM reasoning) |
| Phase 5 — Build | MCPB pack, verify manifest/assets | No (needs shell) |
| Phase 6 — Push | Write `.assess-fix-timestamp`, git add/commit/push | No (needs git) |

---

## Annex: The Fleet Macro Library

assfix is one of 19 macros defined in `agentic_macros.md`. Each is a named trigger that expands to a defined workflow. Together they form the fleet's operations layer — a scriptable command set for LLM-driven development.

### Current macros

| Macro | Trigger | What it does |
|-------|---------|-------------|
| `assess and fix` / `assfix` | `assess and fix <repo>` | Full repo audit (19 categories) → fix in severity order → lint → docs → build MCPB → push |
| `assfixstat` | `assfixstat` | Show all repos: fixed/unfixed, scores, dates — scans `.assess-fix-timestamp` across fleet |
| `fix all` | `fix all` | Fix flagged issues + pre-existing gate failures → verify → report |
| `update docs` | `update docs` | Sync README, CHANGELOG, STATUS, PRD, `llms-full.txt`, MCD project page |
| `ship` | `ship it` / `release` | Lint → test → build → verify → commit → push → GitHub release |
| `certify` | `certify` | Run all verification gates: ruff, tsc, pytest, CUA, Playwright |
| `nsis build` | `nsis build <repo>` | Pre-flight → `just build-native` → verify .exe → `just cua-nsis-test` |
| `polish` | `polish` | Fix warnings, add `data-testid`, verify dark theme, dynamic discovery, Prefab |
| `lint green` | `lint green` | `ruff --fix` + `biome check --write` to zero errors |
| `types green` | `types green` | `tsc --noEmit` to zero errors |
| `gates green` | `gates green` | Lint + typecheck + tests all green |
| `start green` | `start green` | Kill zombies → start backend → health poll → start frontend → open browser |
| `sync deps` | `sync deps` | `uv sync` + `bun install`, commit lockfiles |
| `bump version` | `bump version` | Bump `pyproject.toml`, `tauri.conf.json`, `glama.json`, `CHANGELOG.md` |
| `scan fleet` | `scan fleet` | Grep all repos for same antipattern, fix or file, update pitfalls doc |
| `gh status` | `gh status` | GitHub auth check, unread notifications, open PRs, CI pulse |
| `zombie clean` | `zombie clean` | Kill zombie processes on fleet ports, remove stale lockfiles, purge `__pycache__` |
| `mcp pulse` | `mcp pulse` | Probe all MCP servers — report alive/dead/skipped |
| `ocstat` | `ocstat` | Full opencode status: server health, active project, MCP pulse, config drift |

### Macros as a pattern

The key insight is that **macros are cheap to create and expensive to maintain well**. The barrier to entry is low (add a trigger + expansion in `agentic_macros.md` and a Domain Read List entry in `CLAUDE.md`). The cost is keeping the expansion accurate as the codebase evolves.

Good macros share three properties:

1. **Self-limiting** — they stop when their condition is met. `certify` doesn't fix; it reports pass/fail.
2. **Gated** — they check prerequisites before acting. `ship` checks `.nopublish` before building.
3. **Composable** — they call each other. `gates green` calls `lint green` + `types green` + tests. `ship` calls `certify` first.

### Macro design anti-patterns

| Anti-pattern | Example | Why it fails |
|-------------|---------|-------------|
| **Under-expansion** | `fix all` fixes just the first issue | User expects comprehensive fix, gets partial |
| **Over-expansion** | `ship` runs when user said `update docs` | Does work user didn't ask for |
| **Silent expansion** | Macro expands without telling user | User doesn't know what happened |
| **Brittle steps** | Macro hardcodes file paths | Breaks when repo structure changes |
| **No phase gate** | Macro skips assessment, goes straight to fixing | Fixes the wrong things or misses scope |
| **Too many triggers** | Macro fires on common words | Annoying false positives |

### Recently added macros (July 2026)

The following macros were added in the same session as assfix itself — demonstrating how cheap macro creation is when the pattern is understood:

| Macro | Trigger | What it does | Value |
|-------|---------|-------------|-------|
| `ghaudit` | `ghaudit` | Fleet-wide GitHub hygiene: issues, PRs, CI, topics, descriptions, stale branches, bug cross-ref | Full fleet visibility without a browser |
| `qualitycheck` | `qualitycheck <repo>` | 8-dimension strategic score (originality, difficulty, wrappee, competition, tools, webapp, fleet integration, battlegroup) → growth gaps → report | Separates gems from gravel |
| `spec` | `spec <feature>` | Spec-First Interview: ask clarifying questions, write `SPEC.md`, get approval before coding | Prevents building wrong thing |
| `pr clean` | `pr clean` / `squash` | Review PR commits, squash fixup commits, rebase onto base, verify diff, push | Keeps PR history readable |
| `audit deps` | `audit deps` | Check deps for CVEs, outdated versions, incompatible licenses, flag — never auto-upgrade | Security hygiene |
| `port check` | `port check <repo>` | Verify repo ports match fleet registry, detect zombie listeners, flag mismatches | Prevents port collisions |
| `env sync` | `env sync` | Extract `os.getenv()` calls from src/, compare with `.env.example`, add missing, flag dead | Prevents "missing env var" errors |
| `tag` | `tag <version>` | Create annotated git tag, push, verify CI triggered | One-step release tagging |
| `drift` | `drift` | Compare all repos against SOP checklist — find gaps, DO NOT fix, report | Fleet-wide gap analysis |
| `onboard` | `onboard <repo>` | Verify repo exists → install deps → check .env → start backend → health poll → start frontend → open browser | Cuts new-dev friction |
| `template sync` | `template sync` | Compare `start.ps1`, `build.ps1`, `tauri.conf.json` against reference repos, show diffs, ask before overwriting | Keeps boilerplate fresh |
| `bench` | `bench <repo>` | Run `pytest --benchmark`, report regression vs last run, save results — don't fail CI | Performance regression detection |

The more complex macros each have their own SOP in `patterns/` — same principle as assfix: the macro is the trigger, the SOP is the step-by-step checklist.

| Macro SOP | Location | Report | Timestamp |
|-----------|----------|--------|-----------|
| Assess & Fix | `patterns/repo-assess-and-fix.md` | `reports/assess-{date}.md` | `.assess-fix-timestamp` |
| GitHub Fleet Audit | `patterns/GHAUDIT_SOP.md` | `reports/ghaudit-{date}.md` | `.ghaudit-timestamp` |
| Fleet Drift Scan | `patterns/DRIFT_SCAN_SOP.md` | `reports/drift-{date}.md` | `.drift-timestamp` |
| Dependency Audit | `patterns/DEP_AUDIT_SOP.md` | `reports/deps-{date}.md` | `.deps-timestamp` |
| Spec-First Interview | `patterns/SPEC_INTERVIEW_SOP.md` | `SPEC.md` (repo root) | — (living document) |
| Onboard New Repo | `patterns/ONBOARD_SOP.md` | — (chat output) | — |

This pattern scales: **macro triggers the workflow, SOP owns the detail, the LLM executes at runtime**. Adding a new workflow costs one macro definition + one SOP document. The LLM bridges the gap between them.

---

## Source files

| File | Location | Purpose |
|------|----------|---------|
| SOP checklist | `patterns/repo-assess-and-fix.md` | Canonical 19-category audit with severity scoring |
| Macro definitions | `standards/rules/agentic_macros.md` | All 19 fleet macros |
| Skill (Claude Desktop) | `skills/assfix/SKILL.md` | Maps SOP to `Read`/`Grep`/`Glob`/`Edit`/`Write` tools |
| Skill (Antigravity) | `.agents/skills/assfix/SKILL.md` | Auto-loaded copy for Antigravity IDE |
| Webapp page | meta-mcp webapp → Assfix SOP | SOP viewer + repo selector + read-only assessment runner |
| Webapp justfile page | meta-mcp webapp → Fleet Justfile | Justfile recipe browser + command copier |

## Quick reference

```powershell
assess and fix libreoffice-mcp     # full pipeline on one repo
assfix libreoffice-mcp             # same thing (short alias)
assfixstat                         # show all repos: fixed/unfixed, scores, dates
assess plus fix libreoffice-mcp    # explicit: do NOT trigger per-word
list expansions                    # show all 19 fleet macros
```
