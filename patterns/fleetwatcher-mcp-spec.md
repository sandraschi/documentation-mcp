# fleetwatcher-mcp — Internal Fleet Pulse

**Status**: Draft Spec
**Author**: Sandra
**Date**: 2026-07-15
**Related**: aiwatcher-mcp (external intel), fleet-agent-mcp (orchestration)

---

## 1. Premise

aiwatcher watches *outward* — arXiv, HN, GitHub public. fleetwatcher watches *inward* — our own repos, sessions, standards changes, build outcomes.

Two logical services, one shared dashboard.

---

## 2. Data Sources

| Source | What it provides | Ingestion method |
|--------|-----------------|-----------------|
| **assfix timestamps** (`.assess-fix-timestamp` in each repo) | Last assessment, commit, host | File watcher or periodic scan of `D:\Dev\repos\*/.assess-fix-timestamp` |
| **git log** (all fleet repos) | Commits, branches, authors | `git log --all --since=<N>` per repo |
| **session docs** (`mcp-agent-session-summaries/data/sessions/`) | Session summaries, design decisions | Read directory, parse frontmatter |
| **BUILD_LOG.md** | NSIS build outcomes, failures | Per-repo watcher |
| **.nopublish / .ai-readiness** | Repo classification | Existence check |
| **CUA smoke test artifacts** (`scripts/cua-smoke.py` runs) | Test pass/fail, screenshots | Output dir watcher |

---

## 3. Architecture

```
                    ┌──────────────────┐
                    │   Fleet Pulse     │  ← React dashboard (port TBD)
                    │   (single page)   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │ aiwatcher  │ │fleetwatcher│ │ mcp-central │
       │ backend    │ │ backend    │ │ -docs files │
       │ (:10946)   │ │ (:10947)   │ │ (git)       │
       └────────────┘ └────────────┘ └────────────┘
```

Port reservation: **10918** for fleetwatcher backend, **10919** for Fleet Pulse dashboard (Vite frontend).

---

## 4. fleetwatcher MCP Tools

### Repo pulse

```
fleet_pulse(operation="recent", hours=24)
  → list of repos with recent activity (commits, assfix, builds)

fleet_pulse(operation="repo", path="arxiv-mcp")
  → status: last assfix, last commit, .nopublish? .ai-readiness? build log?

fleet_pulse(operation="dirty")
  → repos with uncommitted changes
```

### Build monitoring

```
build_watch(operation="recent", limit=20)
  → NSIS builds, pass/fail, size, duration

build_watch(operation="log", repo="pywinauto-mcp")
  → BUILD_LOG.md content
```

### Session awareness

```
session_scan(operation="recent", hours=48)
  → session summaries from the docs folder

session_scan(operation="search", query="context bomb")
  → full-text search across session docs
```

### Fleet graph

```
fleet_graph(operation="dependencies")
  → which MCP servers call which other MCP servers

fleet_graph(operation="port_map")
  → live port usage vs registered ports
```

---

## 5. Dashboard Sections (Fleet Pulse)

| Section | Data source | Columns |
|---------|------------|---------|
| **Fleet Status** | assfix timestamps + git log | Repo, last assessed, last commit, days since either, .nopublish badge |
| **Recent Activity** | git log (all repos, last 24h) | Repo, commit message, author, time |
| **Build Pipeline** | BUILD_LOG.md + CUA artifacts | Repo, last build, size, pass/fail |
| **Session Log** | session docs | Date, title, repo, tags from frontmatter |
| **Security** | .nopublish + .ai-readiness + threat doc edits | Repo, sentinels present, last threat doc update |
| **Port Audit** | live scan vs WEBAPP_PORTS.md | Port, expected, actual, conflict? |

---

## 6. Integration with aiwatcher

**Not merged, but co-presented.** The Fleet Pulse dashboard has two tabs:

| Tab | Backend | Content |
|-----|---------|---------|
| External Intel | aiwatcher (:10946) | Papers, code drops, HN mentions, fleet PR feedback |
| Internal Status | fleetwatcher (:10947) | Builds, commits, assfix results, session docs |

The React SPA fetches from both backends. No cross-coupling. A user lands on one page and sees both outward and inward signals.

---

## 7. MVP (doable this week)

| Step | What | Depends on |
|------|------|-----------|
| 1 | skeleton FastMCP server with `fleet_pulse` tool (repo, recent, dirty) | Nothing |
| 2 | `build_watch` tool — parse BUILD_LOG.md across fleet | Step 1 |
| 3 | `session_scan` tool — read session docs directory | Step 1 |
| 4 | Fleet Pulse dashboard (Vite + React, single page with tabs) | Steps 1-3 |
| 5 | Port audit tool — scan 10700-11500, diff against WEBAPP_PORTS.md | Step 1 |
| 6 | Fleet graph tool — parse opencode.jsonc for MCP interdependencies | Step 1 |

---

## 8. Open Questions

1. **How to handle repos that are local-only (no remote)?** fleetwatcher runs locally, reads the filesystem — no GitHub dependency needed.
2. **Should fleetwatcher push events to aiwatcher, or the dashboard poll both?** Poll both. Push creates coupling; the dashboard is just an SPA that calls two backends.
3. **What about repos that require elevation to read?** fleetwatcher runs as the user. If a repo needs admin, skip it — log the gap.
4. **Is this worth a standalone server, or a plugin to aiwatcher?** Standalone. aiwatcher's data model (paper, code drop, media mention) doesn't map to internal signals. A shared dashboard is the right level of integration.
