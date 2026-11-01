# P0 RAG staleness fix — implementation plan

Date: 2026-08-29
Repo: mcp-central-docs (`docs_mcp`)
Backlog source: operations/docs-mcp/RAG_STALENESS_BACKLOG.md
Status: plan only — nothing implemented yet

## Environment finding (adjacent, not blocking)

`onnxruntime-gpu 1.29.0` is installed in `.venv`, but the only CUDA toolkit on
the box is v13.3 (driver 620.02). ORT's CUDA execution provider needs CUDA
12.x's cuBLAS ABI (`cublasLt64_12.dll`), which CUDA 13 restructured, so the
embedder silently falls back to CPU every sync. Confirmed via
`onnxruntime_gpu-1.29.0.dist-info` in site-packages + missing DLL error in
logs/rag-sync-20260829-050002.log. Not the staleness bug, but slows every
future ingest — fix is `pip install nvidia-cublas-cu12 nvidia-cudnn-cu12`
into the venv (runtime-only wheels, no toolkit reinstall). Not yet done.

## Current code state (as of this read)

- `src/docs_mcp/backend/config.py` — `DocsConfig` has no `rag_stale_cutoff_months`
  or `rag_quarantine_prefixes` fields yet. `EXCLUDE_DIRS` in `ingestor.py`
  already skips `junk`, `backup`, `backups`, `.venv`, etc. at the directory
  level but has no age-based or path-prefix quarantine logic.
- `ContentIngestor.process_file()` (ingestor.py) builds per-chunk metadata:
  `filename`, `relative_path`, `fm_title`, `fm_category`, `fm_status`,
  `fm_audience`, `fm_skill_candidate`, `fm_last_updated`. `fm_last_updated`
  is read from frontmatter if present but is never populated from git or
  mtime — most files have no frontmatter, so this field is empty for the
  bulk of the corpus today.
- `discover_recent_markdown()` already computes git-log + git-diff + mtime
  timestamps for the `sync-recent` incremental path, but that data is used
  only to decide *which files to re-embed*, not stored as retrievable
  metadata, and not used at all for `load_all_docs()` (full ingest).
- `mcd_exerciser.py` synthesis path (`context_parts`, line ~619-625) builds
  `SOURCE: {filename}\nCONTENT: {chunk}` with no date, then hands the
  concatenated `context_text` straight to `_get_llm_answer()`. No freshness
  signal reaches the model at all today.

## Plan, in landing order (matches backlog 1a-1e, made concrete)

### Step 1: mtime/git metadata on every chunk (prerequisite for everything else)
- In `ContentIngestor.process_file()`, add a `last_modified` field to
  `metadata`, populated by: frontmatter `last_updated` if present, else
  `git log -1 --format=%ct <path>` if the file is in a git repo, else
  `file_path.stat().st_mtime`. This reuses the same git-log pattern already
  written in `discover_recent_markdown()` / `_git_name_lines()` — extract
  that into a small shared helper (`_file_last_modified(path, repo_root)`)
  rather than duplicating it.
- Store as ISO date string in metadata (LanceDB-friendly), not a raw
  timestamp float.
- This alone unblocks steps 2 and 3 below. No filtering yet, no deletions.
- Verify: re-run `sync-recent`, spot-check a few chunks in LanceDB have a
  populated `last_modified`.

### Step 2: surface freshness in the synthesis prompt (backlog 1b)
- In `mcd_exerciser.py`, change the `context_parts.append(...)` line to
  include the date: `f"SOURCE: {sources[-1]} (updated: {r['metadata'].get('last_modified', 'unknown')})\nCONTENT: {r['content']}"`.
- Add one line to the system/instruction prompt passed to `_get_llm_answer`:
  prefer information updated in the last 6 months; if sources conflict,
  flag the conflict and say which is newer.
- No deletions, fully reversible, smallest-possible diff. This is the
  highest value-per-effort step since it fixes the actual symptom (stale
  info presented as current) without deleting any content.

### Step 3: ingest-time cutoff + quarantine prefixes (backlog 1a)
- Add to `DocsConfig`: `rag_stale_cutoff_months: int = 12`,
  `rag_quarantine_prefixes: list[str] = ["backups/", "_archive/", "docs/agentic chats/", "not-mcp-related/"]`.
- In `glob_markdown()` or `process_file()`, skip a file if its resolved
  `last_modified` (from step 1) is older than the cutoff AND its
  `relative_path` starts with a quarantine prefix. Cutoff alone, without
  the prefix match, is too blunt — some old docs are legitimately still
  correct (e.g. a stable protocol spec) and shouldn't vanish from search
  just for being old.
- Config-driven, not hardcoded, so it's adjustable without a code change.
- Verify: re-run `just mcd-sync` (or a full re-ingest), confirm chunk count
  drops, and confirm nothing outside the quarantine prefixes was dropped.

### Step 4: frontmatter deprecation flag (backlog 1c)
- In `parse_frontmatter()`, check for `status: archived` or
  `deprecated: true` and skip the file in `process_file()` before chunking.
- Fully reversible per-file (remove the frontmatter line to un-quarantine).
- Independent of step 3 — lands in either order.

### Step 5: triage list generation (backlog 1d)
- New script `scripts/rag_staleness_audit.py`: walk the same paths
  `glob_markdown()` covers, apply the same `last_modified` resolution from
  step 1, and flag files matching heuristics: `fastmcp\s*2\.`, `FastMCP 2`,
  `Q[1-4]\s*2025`, known-old model names (e.g. `gemma4:26b` pre-swap,
  `gemma3`, etc.).
- Output: `operations/RAG_STALENESS_TRIAGE_<date>.csv` with columns
  `path, mtime, git_last_commit, heuristic_matches, heuristic_score`.
- This is the tool a human (you) actually reads before manually deciding
  what goes behind `_archive/` in step 6 — not automated deletion.

### Step 6: move quarantine folders (backlog 1e)
- Candidates already named in the backlog: `backups/general-ai-2025-11-27_2246/**`,
  `docs/agentic chats/**`.
- Each move is a single `git mv`, no content edits, maintainer signoff
  required before each move (per backlog — this is a manual gate, not
  something to script blind).

## Sequencing rationale
Steps 1-2 are pure additive metadata + prompt changes — zero risk of losing
content, and step 2 alone fixes the symptom you actually hit (stale content
presented as current, undifferentiated). Steps 3-4 start actually excluding
content from the index, so they come after the freshness signal already
exists and has been sanity-checked. Steps 5-6 are the human-in-the-loop
triage and cleanup, deliberately last and deliberately manual-gated.

## Suggested first PR
Steps 1 + 2 together — smallest safe change that fixes the actual
"stale info displayed as current" symptom described in STATUS.md §5,
before touching what gets excluded at all.
