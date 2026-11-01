---
title: "Fleet Hygiene Standards"
category: standard
status: active
audience: mcp-dev
related:
  - patterns/ANTIPATTERN_DIALOGIC_TOOL_FLUFF.md
  - standards/AGENTS.md
last_updated: 2026-09-25
---

# Fleet Hygiene Standards

**Status**: Active — first pass complete 2026-09-25, remediation ongoing
**Scope**: README.md, docs/*.md, help pages, and dashboard copy across all repos under `D:\Dev\repos\`

---

## 1. What this covers (and what it doesn't)

This is the prose-quality sibling of [`patterns/ANTIPATTERN_DIALOGIC_TOOL_FLUFF.md`](../patterns/ANTIPATTERN_DIALOGIC_TOOL_FLUFF.md). That doc governs **tool return values and error messages** — machine-facing text an LLM client has to act on. This doc governs **human-facing marketing prose** — README ledes, status badges, dashboard headers, help text. Same root complaint (words that don't carry information), different surface.

**Rule**: README/docs/dashboard prose states what the software does and its actual verified status, in plain register. It does not use unearned superlatives, breathless sci-fi framing, or checkmark-emoji bullet trains to imply completeness that hasn't been verified.

**Not covered here**: `SOTA` as a literal fleet-standard name (`WEBAPP_SOTA_STANDARDS.md`, `web_sota/` directory convention) is exempt — it's this fleet's own naming convention for "current stack version," not a marketing claim, and stripping it would just break cross-references. The problem is **`SOTA` used as a vibes-adjective** ("Industrial SOTA Dashboard", "SOTA-compliant, premium") stacked with other fluff, not the bare directory/version-tag usage.

## 2. The specific patterns to cut

| Pattern | Example (found in this fleet) | Why it fails |
|---|---|---|
| Unearned status claims | "Production Ready", "100% type coverage", "Zero issues" | Reads as a fact. [`Honesty in Fleet-Wide Answers`](AGENTS.md) applies to what we tell users too — a status claim needs the same "traced or tested" bar as [`mixxxxx`'s `docs/STATUS.md`](../../mixxxxx/docs/STATUS.md) uses. If it hasn't been verified this way, don't claim it. |
| Breathless adjectives | "Industrialized", "Revolutionizing acoustic smart home orchestration", "enterprise-grade", "world-class" | Says nothing a reader can act on. Doesn't tell them what the tool does, what state it's in, or what to try first. |
| Vibes-badges | "Premium dashboard", "Industrial Dashboard" | A dashboard either has features or it doesn't — list them. "Premium" is not a feature. |
| Emoji bullet trains | 🚀💎🏆🎯⚡ as list-item prefixes throughout a README | Fine sparingly for visual scanning (a single 🔴/🟢 status dot is legitimate signal); a full emoji-per-bullet README reads as unfiltered enthusiasm rather than documentation, and some MCP clients choke on emoji in rendered output. |
| "Next-gen" / "cutting-edge" / "state-of-the-art" (as adjective, not the `SOTA` proper noun) | "Next-gen frontend linting" (Biome is just... a linter) | Dates instantly and is unfalsifiable. |

## 3. Fleet-wide audit (2026-09-25)

Scanned 286 repo READMEs (excludes `mcp-central-docs` itself) for the term list in §2 plus a fixed emoji set (🚀👑✨🔥🎯💎⚡🌟🏆). **39 repos (~14%) flagged.** This is a first-pass regex sweep, not a semantic read — false positives exist (e.g. `empower\w*` matches inside "disempowerment"; manually verify before editing). Ranked by hit count:

| Rank | Repo | Hits | Sample offending line |
|---|---|---|---|
| 1 | `obs-mcp` | 9 (terms) | "Industrialized FastMCP 3.2.0 server... **Current Status: INDUSTRIALIZED - SOTA v1.5.0**" |
| 2 | `worldlabs-mcp` | 6 (emoji) | Full 🚀💎🏆🎯⚡ bullet train in the doc-links list — lower severity, emoji-only, no false-status prose |
| 3 | `nest-protect-mcp` | 5 | "The Nest Protect MCP Server is a **production-ready**... offers... **seamless** integration" |
| 4 | `handbrake-mcp` | 5 | "Industrial SOTA Dashboard (v13.1), enterprise-grade CI/CD, and robust... for maximum stability" |
| 5 | `vrchat-mcp` | 4 | "industrialized automation layer... Clone the **industrialized repository**" |
| 5 | `stripe-mcp` | 4 (emoji) | — |
| 5 | `on-ai-takeover` | 4 | **Likely false positive** — regex matched inside "Disempowerment" (a Kulveit et al. citation), not marketing copy. Skip. |
| 5 | `publictransport-mcp` | 4 | "**Status:** Production Ready \| SOTA Compliant \| Fully Operational... **The application is now production-ready with complete... all features functional!**" |
| 5 | `filesystem-mcp` | 4 | "enterprise-grade security... **Fastest Installation - Production Ready**" |
| 10 | `ring-mcp` | 3 | "**production-ready**: Used across all MCP projects" (unverifiable, fleet-wide claim about a single repo) |
| 10 | `alexa-mcp` | 3 | "*Revolutionizing acoustic smart home orchestration.*" |
| — | 29 more repos | 1–3 each | Full list in `operations/fluff-audit-2026-09-25.txt` if needed for a second pass — not reproduced here to keep this doc scannable |

## 4. Remediation priority

1. **`obs-mcp`** first — worst offender, and it's a live crossconnect dependency for `mixxxxx`/`mixx-dj-mcp`'s AV rig (see [`patterns/FLEET_MESHING_PHILOSOPHY.md`](../patterns/FLEET_MESHING_PHILOSOPHY.md)). Rewrite the status line and feature bullets to `mixxxxx/docs/STATUS.md`-style plain register (Works / Partial / Absent) before it's trusted as a dependency.
2. **Repos with unverifiable "production-ready"/"100% coverage" claims** (`nest-protect-mcp`, `publictransport-mcp`, `filesystem-mcp`, `ring-mcp`) — either verify the claim (test coverage report, uptime log) or downgrade the language to match actual status.
3. **Emoji-only offenders** (`worldlabs-mcp`, `stripe-mcp`, `myvrworlds`, `prc-shopping-mcp`) — lower priority, cosmetic; thin the bullet trains to one status glyph max.
4. Everything else in the 1–3 hit tail — fix opportunistically when touching that repo for other reasons, not a dedicated sweep.

Per [`Batch Mutation Safety`](../../../.claude/CLAUDE.md) — this is prose editing across many files, not a scripted regex replace, so the `.bak`-before-mutating rule applies per file touched if more than 2 are edited in one sitting; do these one repo at a time regardless, since each needs a human read for tone, not a mechanical find/replace.

## 5. Root cause (why this keeps happening)

New repos are frequently bootstrapped by telling an LLM session to "match the style of `<older repo>`" or "lift the dashboard pattern from X." The LLM matches tone as faithfully as it matches structure — if the source repo's README leans promotional, the derived one inherits the same register, and it compounds each generation. This is the same mechanism that produces the architectural duplication tracked in [`FLEET_MESHING_PHILOSOPHY.md`](../patterns/FLEET_MESHING_PHILOSOPHY.md) §4 (parallel OSC bridge implementations) — copy-by-example propagates whatever it's shown, good or bad, with no shared source of truth to converge on. There's no mechanical fix for this beyond periodic audits like this one; `docs/STATUS.md`-style repos (verification-gated status tables) don't drift this way because the format itself makes an unverified claim structurally awkward to write.

## 6. Adding this to the read list

Not yet added to the global `CLAUDE.md` Domain Read List — that file is outside this repo. Suggested row for whenever a README/docs/help-text edit is in scope:

| Task domain | Read |
|---|---|
| README / docs / dashboard prose editing | `standards/FLEET_HYGIENE_STANDARDS.md` (this doc) |

## 7. Data tables: generated or dated

Prose rules do not stop a table from lying. A version column, a status cell, or a
"measured at" note goes stale the moment the software moves - observed twice in
`standards/rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md`, whose S2 compat table was
five rows wrong within 48 hours of being hand-edited (the launcher writes new builds
hours before GitHub publishes the tags).

**Rule**: a table with versions, dates, counts or statuses is either

- **generated** by a script in the same repo (checked into `scripts/`, run by `just`,
  output committed or rendered at build time), or
- **dated**: a "measured <YYYY-MM-DD> with <exact command>" line directly above the
  table, so the next reader can re-run it instead of trusting it.

A table with neither is a rumor with borders. Fix it or delete it.
