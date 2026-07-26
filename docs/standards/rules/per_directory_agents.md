# Per-Directory AGENTS.md (Agent Navigation Maps)

**Established**: 2026-07-23
**Inspiration**: Forks of `advanced-memory-mcp` using per-directory semantic entry files
**Cross-reference**: [AGENTS.md](../AGENTS.md), [CLAUDE.md](./claude_dot_md_sota.md), [Session Context Injection](./session_context_injection.md), [Workflow 2026](./workflow_2026.md)

## Problem

A single `AGENTS.md` at the repo root works for small-to-medium repos. For repos with 100+ files across 15+ directories (e.g., `calibre-mcp`: 130+ tool files, `advanced-memory-mcp`: layered DB/models/services/tools/rag), the root file either:
- Omits detail (agent doesn't know which file to touch)
- Becomes bloated (agent scrolls past walls of irrelevant text)

The agent wastes context re-discovering the same structure on every session.

## Solution

A tree of **per-directory `AGENTS.md` files** chained by dependency order. Each file answers: *"What lives in this directory, what are the entry points, and what should I read next?"*

This is the `AGENTS.md` variant of what the `CODEMAP.md` pattern does in the PRC dev community, using the established cross-tool filename (`AGENTS.md` is natively read by Claude Code, Copilot, OpenAI Codex — 60K+ repos).

## The Chain

```
repo-root/AGENTS.md           ← Entry: high-level map, reading order
├── src/pkg/AGENTS.md         ← Layer: files, key classes, cross-refs
│   ├── src/pkg/db/AGENTS.md  ← Sub-layer
│   ├── src/pkg/models/AGENTS.md
│   ├── src/pkg/services/AGENTS.md
│   ├── src/pkg/tools/AGENTS.md
│   └── src/pkg/rag/AGENTS.md
└── docs/AGENTS.md            ← Auxiliary
```

The root `AGENTS.md` MUST list a **reading order** — a numbered chain of directories the agent should read first, earliest dependency first. Each leaf `AGENTS.md` covers only its own directory.

## Format

Every per-directory `AGENTS.md` MUST follow this template:

```markdown
# {directory} — {1-line purpose}

## Key Files

| File | Purpose |
|------|---------|
| `foo.py` | Entry point for X. Key class: `Foo`. Depends on `bar.py`. |
| `bar.py` | Shared utilities. Called by `foo.py`, `baz.py`. |

## Entry Points

- `{module}.{function}` — what it does, when the agent should call it

## Next (reading order)

1. `{child_dir}/AGENTS.md` — {why read this next}
2. `{sibling_dir}/AGENTS.md` — {why read this next}
```

**Keep each file under 30 lines.** The purpose is orienting, not exhaustive.

## Relationship to Root AGENTS.md

The root `AGENTS.md` remains mandatory per fleet standards. Per-directory `AGENTS.md` files are **extensions**, not replacements. The root file's `## Reading Order` section points to the chain.

Root `AGENTS.md` addition:

```markdown
## Directory Map

This repo uses per-directory AGENTS.md for deep navigation.
Read in order:

1. `src/pkg/AGENTS.md` — Core layer (read first)
2. `src/pkg/db/AGENTS.md` — Database layer
3. `src/pkg/services/AGENTS.md` — Business logic
4. `src/pkg/tools/AGENTS.md` — MCP tools (read after models/services)
5. `src/pkg/rag/AGENTS.md` — RAG engine
```

## When to Use

| Repo size | Approach |
|-----------|----------|
| < 50 files, flat layout | Root `AGENTS.md` only — sufficient |
| 50-200 files, layered | Per-directory `AGENTS.md` for each layer directory |
| 200+ files, deep nesting | Per-directory `AGENTS.md` for every subdirectory with +10 files |

**Threshold (HARD RULE)**: Any directory with 15+ files or 3+ submodules MUST have its own `AGENTS.md`.

## Maintenance

Per-directory `AGENTS.md` files go stale fast if not treated as code:

- **Update on structural change**: New file, renamed module, moved entry point → update the relevant `AGENTS.md` in the same edit.
- **Update on agent discovery**: If an agent reads a directory and finds its `AGENTS.md` wrong, fix it immediately (same edit).
- **Audit**: The `assess and fix` SOP checks for stale `AGENTS.md` files when scanning a repo. See [repo-assess-and-fix.md](../../patterns/repo-assess-and-fix.md).

## Comparison Table

| Aspect | Single AGENTS.md | Per-directory AGENTS.md | INFO.md (fork pattern) |
|--------|-----------------|------------------------|------------------------|
| Tool support | Claude Code, Copilot, Codex native | Same — same filename | None — custom filename |
| Granularity | Coarse | Fine per layer | Fine per layer |
| Context cost | High (all content loaded) | Low (agent reads only needed dirs) | Low |
| Staleness risk | Moderate | Higher (more files) | Higher |
| Discovery | Agent must rely on root file or `fd` | Chain forces structured reading | Same |

## Verification

The pattern is working if:
- An agent new to a repo can navigate to the correct source file for a given bug or feature in under 5 reads
- Each `AGENTS.md` is < 30 lines
- No directory with 15+ files lacks an `AGENTS.md`
- The root `AGENTS.md` has a `## Reading Order` section linking the chain
