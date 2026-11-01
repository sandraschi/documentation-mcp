---
title: "MCP Central Docs Frontmatter Standard"
category: standard
status: active
audience: all
skill_candidate: false
last_updated: 2026-02-25
---

# MCP Central Docs Frontmatter Standard

**Version:** 1.0  
**Status:** Active  
**Applies to:** All substantive docs in mcp-central-docs (not stubs, not session logs)

---

## Purpose

YAML frontmatter enables:
1. **Better RAG retrieval** — the docs-mcp LanceDB ingestor surfaces `category`, `status`, `audience` as filterable metadata, improving search precision
2. **Skill extraction** — docs flagged `skill_candidate: true` are candidates for `.cursor/skills/` or Claude Skills packages
3. **Cross-linking** — `related:` list enables navigation and link-rot detection
4. **Freshness tracking** — `last_updated` enables the weekly weeding audit

---

## Schema

```yaml
---
title: "Human-readable title"           # required
category: standard                       # required — see Categories below
status: active                           # required — see Statuses below  
audience: mcp-dev                        # required — see Audiences below
skill_candidate: false                   # optional, default false
related:                                 # optional
  - path/to/related.md
  - path/to/other.md
last_updated: 2026-02-25                 # required, ISO date
---
```

### Categories

| Value | Meaning |
|-------|---------|
| `standard` | Rules, requirements, protocols (AGENT_PROTOCOLS, WEBAPP_SOTA_STANDARDS) |
| `pattern` | Reusable design patterns (PORTMANTEAU_CONCEPT, TOOL_EXPLOSION_FIX) |
| `architecture` | System/component design docs |
| `reference` | API docs, tool lists, capability matrices |
| `guide` | How-to and tutorial content |
| `integration` | Per-tool integration docs (blender, gimp, etc.) |
| `ecosystem` | IDE/platform ecosystem docs |
| `project` | Project status/overview docs |
| `research` | Exploratory, not yet actionable |

### Statuses

| Value | Meaning |
|-------|---------|
| `active` | Current, accurate, maintained |
| `draft` | Work in progress, may be incomplete |
| `review` | Needs accuracy check against current codebase |
| `obsolete` | Superseded — kept for history, not for guidance |

### Audiences

| Value | Meaning |
|-------|---------|
| `mcp-dev` | MCP server developers |
| `ops` | Deployment, fleet management |
| `all` | General, relevant to everyone |
| `internal` | Personal/system-specific, not for publication |

---

## Coverage Policy

**Apply frontmatter to:** Standards, patterns, architecture docs, reference docs, key integration guides.

**Skip frontmatter on:** README stubs (< 50 lines of real content), session logs, junk/, backups/, generated files.

**Minimum coverage target:** All files in `standards/`, `patterns/`, `architecture/`, `fastmcp/`, `ecosystem/mcp-protocol/`.

---

## Ingestor Integration

The docs-mcp RAG ingestor (`src/docs_mcp/backend/ingestor.py`) parses frontmatter via `python-frontmatter` and stores fields as LanceDB metadata columns. This enables filtered searches like:

- "Find all active standards" → filter `category=standard, status=active`
- "What are the skill candidates?" → filter `skill_candidate=true`
- "Show me docs that need review" → filter `status=review`

See: `src/docs_mcp/backend/ingestor.py`

---

## Weekly Maintenance

Run the doc freshness audit:
```powershell
.\scripts\audit-doc-freshness.ps1
```

Docs not updated in 60+ days with `status: active` should be reviewed and either updated or marked `status: review`.
