---
title: "Wrappee Capability Drift — SOP"
category: pattern
status: active
audience: mcp-dev
related:
  - patterns/DRIFT_SCAN_SOP.md
  - patterns/QUALITY_CHECK_SOP.md
last_updated: 2026-09-25
---

# Wrappee Capability Drift — SOP

**Trigger**: explicit, per-repo, on request — e.g. "audit blender-mcp's tool coverage against current Blender"
**Scope**: One named repo at a time. Read-only research and a gap report. Never auto-implement.

---

## Why this exists, and why it's different from `drift-scan`

`DRIFT_SCAN_SOP.md` answers "does this repo follow current fleet standards" — file structure, ports, CLAUDE.md, the things this fleet controls. That's internal drift.

This SOP answers a different question: **has the software we're wrapping moved, or has a competing wrapper covered ground we haven't, while our tool list stood still?** A repo can pass every fleet-standard check in `drift-scan` and still be quietly behind — the wrapped software (Blender's Python API, a REST API, a CLI) gained features, or a competing MCP server for the same software shipped tools ours doesn't have, and nothing in this fleet's own tooling would ever notice, because "the server works as expected" and "the server covers what the wrapped software can do" are different, unrelated facts.

**This gap is real and was found directly, not theorized**: earlier the same day this SOP was written, `advanced-memory-mcp`'s own `adn_system` tool had three fully-implemented operations (`inter_server`, `sampling_status`, `batch_process`) with zero route from the actual MCP tool surface — a year-old internal version of exactly this problem, just within one repo instead of against an external wrappee. See `TAURI_PRODUCTION_PITFALLS.md` and the `test_adn_system_operation_coverage.py` test added the same session. That was mechanically detectable (AST diff of two files in the same repo). Wrappee drift is not mechanically detectable the same way — it requires actually going and looking at the wrapped software, which is why this needs to be a deliberate, named task rather than something to run unprompted or on a schedule.

**Rule, same as drift-scan**: this SOP produces a report, not a fix. Building what it finds is a separate, explicitly-scoped follow-up task.

---

## Phase 1 — Establish what the wrapper currently exposes

Enumerate the repo's actual MCP tool surface as an LLM sees it, not the underlying implementation:

- List every `@mcp.tool`-decorated function and, for portmanteau tools, every `operation` value actually reachable (not just implemented — see the internal-drift case above; check for orphaned operations here too while you're in the code).
- Read each tool's docstring for what it claims to cover.
- Note the wrapped software's version this repo currently targets (pinned dependency version, or a version check in the code).

---

## Phase 2 — Establish what the wrapped software can actually do, at its current version

This is the step that requires real research, not a repo scan:

- The wrapped software's own official docs/API reference/changelog, for the version this repo targets **and** the current latest version (the delta between them is exactly what's most likely missing).
- For a library/SDK wrappee (e.g. Blender's `bpy`, a Python package): its actual current API surface. `python -c "import bpy; help(bpy)"`-style introspection where feasible, or the official API docs.
- For a service/CLI wrappee: its current REST API reference or `--help` output, current version vs. what this repo was built against.

Write down concretely: what exists in the wrapped software now that didn't exist (or wasn't documented) when this repo's tool list was last touched.

---

## Phase 3 — Establish what comparable wrappers cover

Search for other MCP servers (or other kinds of integrations/plugins) wrapping the same software:

- GitHub search, the MCP server registries this fleet already tracks (`mcp-registry` search tools), awesome-mcp-servers-style lists.
- For each comparable one found, list its advertised tool/operation surface from its own README or tool docs.
- Note capabilities they expose that this repo doesn't. Note the reverse too (capabilities this repo has that they don't) — this SOP is a gap report, not a one-directional deficiency hunt, and knowing what's already ahead is useful context for the same report.

---

## Phase 4 — Gap report

Write the findings as a report (not a fix), structured like:

```
# Wrappee Capability Drift — <repo-name> (<date>)

## Wrapped software: <name> <version this repo targets> (current: <latest version>)

## Gaps found (wrapped software moved, we didn't)
- <capability> — available since <version>, not in our tool list — [severity/effort guess]

## Gaps found (a comparable wrapper covers this, we don't)
- <capability> — seen in <competitor repo/link> — [severity/effort guess]

## Already ahead (found for completeness, not action)
- <capability we have that comparables don't>

## Not recommended to build (and why)
- <capability that exists but doesn't fit this repo's scope/audience>
```

Persist to `reports/wrappee-drift-<repo-name>-<date>.md` (gitignored, same convention as `drift-scan`'s reports).

---

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| **Running this unprompted, fleet-wide** | Expensive real research per repo (not a file-existence check like `drift-scan`); doing it for 150+ repos without being asked is exactly the scope-creep this fleet's agent guidance says not to do |
| **Building what's found during the same pass** | Conflates research with implementation; a gap report should be reviewable and prioritizable before any code changes, same reasoning as `drift-scan`'s "never fix during a scan" |
| **Trusting training-data knowledge of the wrapped software instead of checking current docs** | The whole point is catching drift since this repo was last touched — an LLM's own memory of "what Blender can do" is exactly as stale as the repo's tool list, possibly staler |
| **Treating every gap as worth building** | Not everything a competitor or the wrapped software supports fits this repo's scope or audience; the report's job is to surface options, not mandate coverage parity |
