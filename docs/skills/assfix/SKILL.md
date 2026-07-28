---
name: assfix
description: Full repo assessment, fix, docs sync, and package build for a fleet MCP server repo under D:\Dev\repos. Trigger this whenever the user says "assess and fix" followed by a repo name, "assfix" followed by a repo name, "assfixstat", or asks for a full SOTA compliance pass on a repo (not just "run lint" or "fix this bug" — this is the whole audit-to-push pipeline). This is the Claude Desktop/Cowork port of the opencode assfix macro; always defer to the canonical checklist in mcp-central-docs rather than inventing checks.
---

# assfix — assess and fix a fleet repo

This is the Claude Desktop / Cowork equivalent of the opencode `assess and fix` macro
(`mcp-central-docs/standards/rules/agentic_macros.md`). Same intent, same checklist,
different execution: this skill maps every step onto the tools actually available in
this environment (`Read`, `Grep`, `Glob`, `Edit`, `Write`, `winops_cmd_powershell`,
`gitops`) instead of opencode's `rg`/`just`/bash-native flow.

**Canonical checklist — read before every run:**
`D:\Dev\repos\mcp-central-docs\patterns\repo-assess-and-fix.md`

**New scaffolds:** Agents building a repo from scratch must follow
`D:\Dev\repos\mcp-central-docs\standards\NEW_REPO_BUILD_COMPLETE.md` so the **first**
assfix finds nothing CRITICAL/HIGH. Assfix is for drift — not day-one runt cleanup.

That file owns the full per-category checklist (19 categories: required files, tool
surface, testing, webapp SOTA, REST endpoints, CORS, security, Tauri/native, FastMCP
features, bad-pattern scanning, error handling, CI/CD, ports, container stacks,
**Dashboard & LLM elicitation** (hardcoded ports/versions, hero section, GPU detection,
opportunity prompt), **Session context injection** (Claude Code hooks, Cursor rules,
Windsurf, Copilot, OpenCode skills, Antigravity skills), and **font/contrast** checks)
with severity weights and standard references. Do not duplicate it here and do not
improvise new checks — if the checklist doesn't cover something, that's a gap to flag
to the user for a checklist update, not something to silently invent. This SKILL.md
only covers *how to execute that checklist with this environment's tools* and the
things that differ from the opencode version.

## Why this exists

The opencode macro assumes `just`, `rg`, and a shell where hangs/quoting bugs don't
happen. In this environment: `git status`/`git commit` can hang indefinitely on some
repos (confirmed on `mcp-central-docs` specifically), `Set-Content -Encoding UTF8`
silently BOMs files under Windows PowerShell 5.1 (see `TRAPS_AND_PITFALLS.md` #13),
and PowerShell here-string templating is a frequent source of malformed output. This
skill routes around all three by preferring the native file tools over PowerShell
templating wherever possible, and by having an explicit fallback for git hangs.

## Phase 0 — Pre-flight

1. Confirm the repo path: `D:\Dev\repos\{repo-name}`. If it doesn't exist, stop and
   ask — do not guess a similar name.
2. Detect repo type via `Glob`/`Read`: `pyproject.toml` with a `fastmcp` dependency →
   Standard MCP Server; `docker-compose.yml`/`Dockerfile` with no `pyproject.toml` →
   Container Stack; `pyproject.toml` without `fastmcp` → Infrastructure Daemon.
   Default to Standard MCP Server if ambiguous. This determines which `[if:...]`
   checklist rows apply.
3. Check for `.nopublish` at repo root (`Glob` for it). If present: assessment still
   runs in full, but Phase 5 (package build) and the git parts of Phase 6 are skipped.
   Say so up front so the user isn't surprised later.
4. Check ghaudit status: `Glob` for `.ghaudit-timestamp` at repo root. If absent,
   note "ghaudit never run on this repo." If present, `Read` the file and note
   how recent it is — older than 30 days = stale, older than 7 days = fresh but
   should be re-run before release.
5. Verify `reports/` is in `.gitignore`. If not, add it.
   Same reasoning as the opencode macro — report files are regenerable snapshots,
   not source code. The `.assess-fix-timestamp` file is the committed audit trail.
6. Read `README.md`, `llms-full.txt` (if present), and the primary config file to
   understand what the server does before auditing it — context prevents false
   positives (e.g. flagging a missing webapp page on a repo that has no webapp).

## Phase 1 — Assess (read-only, no edits)

Work through every category in `repo-assess-and-fix.md` §1A–1S using `Grep`/`Glob`/
`Read` for the pattern checks (the checklist gives literal `rg` patterns — `Grep`
takes the same regex, just swap the tool). For gate commands (`ruff check`, `pytest`,
`tsc --noEmit`, `uv lock --check`), run them via `winops_cmd_powershell` since those
need a real interpreter, not a text search.

**Do not fix anything in this phase.** Catalog every gap with its severity.

Compute the score exactly as specified: base 100, CRITICAL -15, HIGH -8, MEDIUM -4,
LOW -1, INFO 0. >=80 SOTA, 60-79 needs work, <60 fails the fleet bar. Conditional
rows (`[if:...]`) only count when their condition is true.

**Emit the report in chat** using the exact template from §1Q of the checklist, then
**write it to the repo** at `reports/assess-YYYY-MM-DD.md` using the `Write`
tool directly (not `Set-Content` — avoids the BOM trap and any here-string quoting
issue with a multi-hundred-line report body). Use today's date from the environment
context, not a hardcoded value.

**Phase gate:** do not proceed to Phase 2 until the report file exists on disk. If
`Write` reports success, that's sufficient confirmation — no need to re-read it back.

## Phase 2 — Fix (severity order: CRITICAL → HIGH → MEDIUM → LOW)

Use `Edit` for targeted changes and `Write` only for new files or full rewrites.
Fix pre-existing gate failures encountered along the way (a lint error in a file
you're already touching, a broken import blocking `pytest --collect-only`) even if
they weren't the primary target — leaving them for someone else to hit later is a
false economy.

If the assessed score was <60 (runt), prioritize reaching >=60 first: clear every
CRITICAL and HIGH before touching MEDIUM/LOW. If time or scope is tight, say so and
propose stopping at a specific severity tier rather than silently doing a partial
pass and calling it done.

Sections 2A–2I of the checklist give the concrete fix patterns per category (CORS,
tool surface, testing, webapp, Tauri, error handling). Follow those, not ad hoc
judgment — they encode standards decisions made elsewhere in the fleet docs.

## Phase 3 — Lint + typecheck

Via `winops_cmd_powershell`, from the repo root:

```powershell
uv run ruff check src/ --fix
uv run ruff format src/
```

If a webapp exists: `npx tsc --noEmit` and, if Biome is configured,
`npx biome check --write webapp/src/` (fall back to `npx eslint` if Biome isn't set
up). Iterate — re-run, read the remaining errors, fix, repeat — until clean. Don't
report this phase done on the first pass if errors remain.

## Phase 4 — Docs sync (`update docs` macro)

Same target list as the opencode macro: `README.md`, `CHANGELOG.md`, `STATUS.md` (if
it exists), `PRD.md` (if it exists), `llms-full.txt` (regenerate if tools/endpoints
changed), and `mcp-central-docs/projects/{repo}/README.md` if that project page
exists. Skip files that don't already exist — this phase syncs, it doesn't scaffold
new doc files unless the user separately asked for that.

## Phase 5 — Package build (skip if `.nopublish`)

Per `PACKAGING_STANDARDS.md`. Verify `manifest.json` (identifier, version, asset
paths), confirm `assets/icon.png` exists at 256x256, confirm `glama.json` is excluded
from the bundle. The user packages MCP bundles via the Anthropic DXT desktop app
(`validate` then `pack` — never `init` or `publish`, per standing instruction) — if
that app isn't scriptable from this session, run the equivalent CLI if one is on
PATH (`npx @anthropic-ai/mcpb pack . dist/{name}-v{version}.mcpb` or similar), and if
neither is available, stop here and tell the user the package still needs a manual
pack pass rather than silently skipping it.

## Phase 6 — Verify & push

1. Run the full gate set again (lint, format --check, tests) and confirm all pass.
2. Write `.assess-fix-timestamp` at the repo root **using the `Write` tool directly**
   as valid JSON — do not build this via PowerShell string interpolation, which is
   exactly the class of bug that produced literal `$(Get-Date)` leaks in the past
   (see `agentic_macros.md` §assfix Phase 6 note). Content:
   ```json
   {"timestamp": "ISO-8601 timestamp here", "commit": "HEAD sha, filled in after commit", "host": "Goliath"}
   ```
   Get the timestamp and current HEAD sha via `winops_cmd_powershell`
   (`Get-Date -Format "o"`, `git rev-parse HEAD`) first, then write the file with
   those values substituted in directly — no template execution inside the file
   write itself.
3. If `.nopublish` is present: stop here. Report "NOPUBLISH — timestamp written, no
   git operations" and do not attempt to add/commit/push.
4. Otherwise, stage and commit:
   ```powershell
   git add -A
   git status --porcelain   # review before committing — never blind-commit unrelated changes
   git commit -m "assfix {repo}: {one-line summary of what changed}"
   git push
   ```
   **If `git commit` (or `git status`) hangs** — confirmed reproducible on at least
   one fleet repo (`mcp-central-docs`) — do not wait it out repeatedly. Fall back to
   the plumbing sequence instead:
   ```powershell
   git add -A
   $tree = git write-tree
   $parent = git rev-parse HEAD
   # write the commit message to a file with Write tool first (avoids BOM/quoting), then:
   $newCommit = git commit-tree $tree -p $parent -F $msgFile
   git update-ref refs/heads/main $newCommit $parent
   ```
   Use `"HEAD^{tree}"` and `"HEAD^"` as quoted strings if you ever need to amend this
   way — bare `HEAD^{tree}` gets parsed as a PowerShell script-block literal and
   silently mangles the revision, not an error you'll immediately recognize.
5. Report: what was assessed (score before), what was fixed (score after, re-run
   Phase 1's scoring if the user wants a delta), what was deferred and why, the
   report file path, and whether the push actually reached the remote (pushing from
   a sandboxed session may not always succeed — confirm, don't assume).

## Batch mode

To run this across several repos, say "assess plus fix" (not "assess and fix") to
avoid re-triggering per-repo, or explicitly name a wildcard set. Process repos one at
a time — do not write a script that batch-edits files across multiple repos in one
pass; see `TRAPS_AND_PITFALLS.md` #7 ("Batch Scripts Wreck Files"). One repo fully
through Phase 6 before starting the next.

## `assfixstat`

"assfixstat" (or "show me which repos are fixed") — read the fleet for
`.assess-fix-timestamp` presence and report fixed vs. unfixed, matching the opencode
macro's output shape (Repo, Status, Date, Score). Run the PowerShell block from
`agentic_macros.md` §assfixstat via `winops_cmd_powershell` — it's read-only and safe
to run as-is, no adaptation needed since it doesn't write anything.

## What NOT to do

- Don't skip Phase 1 and jump to fixing — the report is the phase gate, not optional
  paperwork.
- Don't invent checklist items not in `repo-assess-and-fix.md`. If something seems
  missing, flag it to the user as a possible checklist gap rather than silently
  applying your own standard.
- Don't run `mcpb pack` / package build on a `.nopublish` repo.
- Don't blind `git add -A && git commit` without reading `git status --porcelain`
  first — a repo mid-way through unrelated work (another session's in-flight edits)
  can have staged changes that have nothing to do with this assfix run.
