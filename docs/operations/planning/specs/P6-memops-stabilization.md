# P6 — MemOps stabilization & memory cottage industry audit

**Status:** Draft (session kickoff tomorrow)  
**Primary repo:** `D:\Dev\repos\advanced-memory-mcp`  
**Plane:** Memory (submarine) — see [FLEET_LANES.md](../FLEET_LANES.md)  
**Last updated:** 2026-06-05

---

## Problem

MemOps is the right **Memory plane** flagship but suffers from:

1. **Instability** — Cursor MCP errored; 79 tools / 12 namespaces = large blast radius  
2. **Webapp drift** — not fleet SOTA (`WEBAPP_STANDARDS.md`)  
3. **Mission creep** — `skills` portmanteau, inbox/audio, meta-MCP tooling inside a memory submarine  
4. **Cottage industry** — dozens of external memory MCP repos; fleet also has parallel memory-ish hulls (bookmarks, notion, calibre RAG, fleet-agent memory cards)

Without a **landscape audit** and **tiered RAG doctrine**, MemOps will keep accreting LCS features.

---

## Agreed direction

| Principle | Decision |
|-----------|----------|
| **One memory flagship** | MemOps owns remember / retrieve / link / ADN / export |
| **Filch, don't fork** | Assess external repos; adopt patterns, not whole codebases |
| **Spin out creep** | `skills-mcp` (separate spec) for skill synthesis/validation |
| **Delegate domain RAG** | Calibre, Immich, Plex keep their RAG; MemOps links metadata |
| **Long-term** | **Tiered, weeded, exportable** memory — not one flat vector dump |

---

## Cottage industry — external landscape (assess tomorrow)

Initial survey (2026-06-05). **Verify stars/ports before filch decisions.**

| Project | Stars (approx) | Storage model | Retrieval | MCP | Filch candidate? |
|---------|----------------|---------------|-----------|-----|------------------|
| **basic-memory** | ~3K | Markdown on disk | FTS + hybrid | Yes | **Export UX**, human-readable vault, Joplin/Obsidian I/O (we have fork in `external/basic-memory`) |
| **mem0** | ~50K+ | Vector + optional graph | Semantic | Cloud MCP (standalone repo **archived** Mar 2026) | Multi-scope memory (user/agent/app), dedup patterns — **not** cloud lock-in |
| **Zep / Graphiti** | ~25K | Temporal knowledge graph | Graph + hybrid | Yes (experimental) | Validity windows, entity edges for **T3** tier — heavy (Neo4j/FalkorDB) |
| **mcp-memory-service** | ~1.6K | Local + optional cloud | Semantic + KG | Yes | Pipeline/session memory patterns |
| **Engram** | ~2K | SQLite FTS5 | Full-text | Yes | Lightweight session memory for coding agents |
| **Chroma MCP** | small | Vector backends | Embedding | Yes | Pluggable vector backend abstraction |
| **Anthropic "official" memory** | n/a | JSONL | Text match | Built-in | Simplicity reference — too thin for Sandra fleet |
| **Cursor skills** | n/a | `SKILL.md` files | Host discovery | IDE-native | **Not MemOps** — `skills-mcp` or host only |

**Sandra already has:** `external/basic-memory`, `mcp-central-docs/projects/basic-memory`, fleet `basic-memory` entry.

### Assessment rubric (score 1–5 each)

| Criterion | Question |
|-----------|----------|
| **Local-first** | Works offline, no mandatory cloud? |
| **Export** | Markdown/JSONL/OPML portable out? |
| **Weeding** | Dedup, decay, archive, or temporal supersede? |
| **Tier fit** | Maps to T0–T3 (below)? |
| **MCP hygiene** | Portmanteau, FastMCP 3.2, capabilities endpoint? |
| **License** | AGPL/commercial OK for filch? |
| **Ops cost** | Docker graph DB vs SQLite? |

Deliverable: `research/notes/MEMORY_COTTAGE_INDUSTRY_AUDIT.md` with top 5 filch targets.

---

## Fleet-internal memory-ish hulls (delegate matrix)

| Hull | Role vs MemOps |
|------|----------------|
| `advanced-memory-mcp` | **Flagship** — ADN, zettel, Lance+FTS, export |
| `basic-memory` (fork) | Reference / filch source |
| `bookmarks-mcp` | Delegate — URL memory; MemOps `nav` links |
| `notion-mcp` / `onenote-mcp` / `obsidian-mcp` | **Connectors** — import once, canonical in MemOps |
| `calibre-mcp` / `immich-mcp` / `plex-mcp` RAG | **Domain libraries** — citation only |
| `fleet-agent-mcp` `memory_card_search` | **Client** — must call MemOps, not parallel store |
| `email-mcp` / digest archives | **Ingress** — intel lane → MemOps ADN |

---

## Long-term: tiered RAG (weeded, exportable)

```text
T0 Capture     raw ingest (inbox, email, OCR, fleet events, manual note)
      ↓ weed   dedup, nav-strip, prompt-injection scrub, expiry hints
T1 Canonical   zettel / ADN markdown on disk (source of truth, human-readable)
      ↓ index  FTS5 + Lance chunks (fleet-standard bge-small-en-v1.5)
T2 Retrieved   hybrid search, RRF, project-scoped queries, citations
      ↓ optional
T3 Graph       temporal entities (Graphiti-style validity) — ONLY if T0–T2 stable
```

### Weeding rules (proposed)

| Signal | Action |
|--------|--------|
| Duplicate title+summary (85%, 48h) | Merge or skip (aiwatcher pattern) |
| Low signal / LCS tags | Archive, exclude from index |
| Superseded ADN | New version; old → `archive/` with `superseded_by` |
| External vault import | One-way ingest; MemOps T1 wins on conflict |
| Prompt injection markers | `sanitize` boundary (arxiv-mcp pattern) |

### Export contract (proposed)

MemOps must always be able to emit:

| Format | Use |
|--------|-----|
| **Markdown tree** | Obsidian, git, human audit |
| **ADN JSONL** | Fleet automation, WF-001 memops node |
| **OPML** | Feed/bundle export |
| **Pandoc bundle** | PDF/DOCX deliverables (already in PRD) |
| **Lance snapshot** | Optional; regenerable from T1 — not sole source of truth |

**Rule:** T1 markdown is canonical; vectors are disposable cache.

---

## Tomorrow session — checklist

### Phase A — Stability (2–3 h)

- [ ] Reproduce Cursor `user-memops` / stdio-http failure
- [ ] Smoke: `adn_notes`, `notes_write`, `search`, reindex
- [ ] Add `advanced-memory-mcp` to `mcp-test-suite` golden (**Memory plane**)
- [ ] `start.ps1` backend readiness + `/api/capabilities`

### Phase B — Webapp SOTA (2 h)

- [ ] Fleet routes: `/tools` `/logs` `/apps` `/help` `/settings`
- [ ] Vault sync page uses capabilities (no hardcoded tool list)

### Phase C — Cottage audit (2–3 h)

- [ ] Run rubric on basic-memory, mem0 docs, Graphiti MCP README
- [ ] Clone/spike: 3 filch candidates (export, dedup, temporal metadata)
- [ ] Write `MEMORY_COTTAGE_INDUSTRY_AUDIT.md`

### Phase D — Scope cut (1 h)

- [ ] Mark `skills` namespace → **deprecate in MemOps**, spec `skills-mcp`
- [ ] PRD 1.9.0: core namespaces only (`notes`, `zettel`, `nav`, `search`, `knowledge`, `project`, `system`, `adn`)
- [ ] Tiered RAG section in PRD + ARCHITECTURE

---

## Spin-out: skills-mcp (P6b, not tomorrow unless time)

| Item | Notes |
|------|-------|
| Repo | `skills-mcp` (new) or `cursor-skills-mcp` |
| Tools | `skills_ops(operation=discover|validate|enhance|research|help)` |
| Migration | Move `make_skill_advanced`, agentskills validation from MemOps |
| Lane | **Office** + **Engineering** (MetaMCP scaffolds skills, skills-mcp runs them) |

---

## Success criteria (P6)

| Metric | Target |
|--------|--------|
| MCP smoke | Tier-1 pass in `mcp-test-suite` |
| Tool count | ≤ 40 tools in core namespaces (post-skills spin-out) |
| Webapp | Fleet SOTA pages + capabilities |
| Audit doc | ≥ 5 external repos scored; ≥ 3 filch decisions |
| Export | Documented T1→export path tested on sample vault |

---

## Related

- [FLEET_GAP_CLOSURE_ROADMAP.md](../FLEET_GAP_CLOSURE_ROADMAP.md)  
- [FLEET_LANES.md](../FLEET_LANES.md) — Memory plane  
- `advanced-memory-mcp/docs/PRD.md` (1.8.1)  
- `external/basic-memory` — enhanced fork for filch  
- [P5-fleet-trust-layer.md](P5-fleet-trust-layer.md) — smoke before features
