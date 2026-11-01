# RAG staleness and ingest hygiene

**Priority:** P0  
**Repo:** mcp-central-docs (`docs_mcp`, ingestor, exerciser)  
**Status:** Not started  
**See also:** [STATUS.md §5](../../STATUS.md)

## Problem

The retriever has no freshness signal. Docs from early 2025 (FastMCP 2.0 era, pre-Gemma-4, pre-2026 standards) rank equally with 2026 material and get spliced into `just report` answers as if current.

Land in order — each step is independently useful.

---

## 1a. Staleness filter in the ingestor

- In `src/docs_mcp/backend/ingestor.py` (or equivalent `ContentIngestor`), add a configurable cutoff: skip files whose `git log -1 --format=%ct <path>` is older than N months *and* whose path matches a quarantine prefix list.
- Default quarantine prefixes: `backups/`, `**/_archive/`, `docs/agentic chats/`, `not-mcp-related/`.
- Config in `src/docs_mcp/data/webapp_settings.json`: `rag_stale_cutoff_months` (default 12), `rag_quarantine_prefixes` (list).
- Re-run `just mcd-sync`; confirm chunk count drops meaningfully.

## 1b. Surface source dates in the synthesis prompt

- In `_get_llm_answer` (`scripts/mcd_exerciser.py`) and server-side equivalent, include each chunk's `modified_at` in the context block.
- System-prompt clause: prefer information modified within the last 6 months; flag conflicts and cite newer sources.
- No deletions required.

## 1c. Frontmatter-based deprecation

- Filter at ingest: YAML `status: archived` or `deprecated: true`.
- Reversible by removing frontmatter.

## 1d. Triage list generation

- Script `scripts/rag_staleness_audit.py`: CSV `path, mtime, git_last_commit, …, heuristic_score`.
- Heuristics: `fastmcp\s*2\.`, `FastMCP 2`, `Q[1-4]\s*2025`, old model names, etc.
- Output: `operations/RAG_STALENESS_TRIAGE_<date>.csv`.

## 1e. Move quarantine folders behind `_archive/`

- Candidates (maintainer signoff before `git mv`):
  - `backups/general-ai-2025-11-27_2246/**`
  - `docs/agentic chats/**`
- Each move is a single `git mv`; no content edits.
