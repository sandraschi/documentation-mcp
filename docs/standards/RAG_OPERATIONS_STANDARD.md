---
title: "Fleet RAG & Index Operations Standard"
category: standards
status: active
audience: fleet
last_updated: 2026-09-12
---

# Fleet RAG & Index Operations Standard

This standard establishes uniform architecture, API contracts, webapp UX patterns, and MCP tool interfaces for all repositories maintaining vector embeddings, neural retrieval, and document indices.

---

## 1. Executive Summary & Fleet Landscape

Multiple MCP servers across the fleet maintain LanceDB vector stores and FastEmbed pipelines. Historically, their implementations grew independently, creating operational friction, UI timeouts, and API contract drift:

| Repository | Search Engine | MCP Sweep Tool | Webapp Control Plane | Status & Key Finding |
|---|---|---|---|---|
| **`mcp-central-docs`** | LanceDB + FastEmbed | `reindex_docs()` | Scattered across 3 pages (Documents, Semantic Search, Settings). Calls `GET /api/reindex`. | **Functional but fragmented UI.** Blocking sync call. |
| **`documentation-mcp`** | LanceDB + FastEmbed | `reindex_docs()` | Scattered across 3 pages. Backend uses async job queue (`POST /api/reindex` + `/api/reindex/{job_id}`). | **Fixed:** Removed 10s fetch timeout footgun; wired background polling. |
| **`advanced-memory-mcp`** (`memops`) | LanceDB + FastEmbed GPU + SQLite | ❌ None | **Dedicated `VaultSync.tsx` (`/system/sync`)** with timer, project picker, extra roots, and status polling. | **Best UI/UX, but critical tool gap:** No MCP tool exists to trigger a vector sweep. |
| **`plex-mcp`** | LanceDB + FastEmbed GPU / `rag_core` | `plex_rag(operation="sync_metadata" / "sync_subtitles")` | Semantic Search & Settings tabs. | **High potential, underutilized:** Powerful subtitle dialogue neural search depends on `mcd`'s `docs_mcp.backend.rag_core`. |
| **`calibre-mcp`** | LanceDB + FastEmbed | `rag_index_build()` | Prefab cards & webapp RAG tab. | Compliant with portmanteau tool patterns. |

---

## 2. Critical Anti-Patterns & Lessons Learned

### Anti-Pattern 1: The Client-Side Abort Timeout Footgun
* **The Problem**: Webapps attaching arbitrary short timeouts (e.g. `AbortSignal.timeout(10000)`) to reindexing endpoints. In vector retrieval, embedding hundreds of documents typically takes 15–120 seconds.
* **The Failure**: The frontend aborts the fetch after 10s and reports *"Request failed"* or *"Could not reach backend"*, even though the backend process is running successfully in the background. The user re-clicks the button, spawning concurrent duplicate indexing threads that lock the database.
* **The Fleet Rule**: **Reindexing endpoints MUST return immediately with an asynchronous job ID (`job_id`).** The frontend must poll `/api/reindex/{job_id}` or listen on Server-Sent Events (SSE), showing a continuous progress indicator rather than aborting.

### Anti-Pattern 2: HTTP Method Inconsistency (`GET` vs `POST`)
* **The Problem**: Some servers exposed reindexing as `GET /api/reindex` (violating HTTP idempotency and safety), while others used `POST /api/reindex`. This led to frontends calling `GET` and receiving `405 Method Not Allowed`.
* **The Fleet Rule**: Sweep and reindex mutations must always accept `POST`. Backends should provision defensive fallback aliases for `GET` during deprecation transitions.

### Anti-Pattern 3: MCP Tool Absence on Memory Hubs
* **The Problem**: `memops` (`advanced-memory-mcp`) is the central knowledge base of the fleet, yet agents operating via Claude Desktop, Cursor, or Antigravity could not trigger a vector reindex through MCP tools.
* **The Fleet Rule**: Any server that stores semantic embeddings must expose a mutating tool to rebuild or synchronize the index.

---

## 3. The Standard Specification

### A. Backend API Contract

Every RAG-enabled MCP server must expose the following three endpoints:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        RAG REST API CONTRACT                           │
├───────────────────────┬─────────┬──────────────────────────────────────┤
│ Endpoint              │ Method  │ Purpose                              │
├───────────────────────┼─────────┼──────────────────────────────────────┤
│ /api/rag/sweep        │ POST    │ Triggers background indexing task.   │
│                       │         │ Body: { mode, hours, paths }         │
│                       │         │ Returns: { success, job_id, status } │
├───────────────────────┼─────────┼──────────────────────────────────────┤
│ /api/rag/status/{id}  │ GET     │ Polls status of active job.          │
│                       │         │ Returns: { status, chunks, error }   │
├───────────────────────┼─────────┼──────────────────────────────────────┤
│ /api/rag/stats        │ GET     │ Returns vector store metrics.        │
│                       │         │ Returns: { total_vectors, model, ...}│
└───────────────────────┴─────────┴──────────────────────────────────────┘
```

#### Legacy Backward-Compatibility
For servers already using `/api/reindex`:
* `POST /api/reindex` and `GET /api/reindex` must redirect to or wrap the same background worker and return `{ "success": true, "job_id": str, "message": str }`.
* `GET /api/reindex/{job_id}` must return `{ "status": "queued" | "running" | "complete" | "error", "chunks": int }`.

---

### A.1 Normative Job Pattern (reference: tvtropes-mcp 2026-10)

Anti-pattern §2.1 says *what* (return a `job_id` immediately); this is *how*:

1. **Queue endpoint** (`POST /api/vector/rebuild`): creates `job_id` (uuid hex),
   stores `{job_id, status: "queued", started, finished: None, result: None, error: None}`,
   schedules the worker with `asyncio.create_task`, returns `{success, job_id, status}` at once.
2. **Worker** (`_run_vector_rebuild(job_id)`): sets `status: running`, runs the embedding loop, writes `result` + `status: done` — or `status: failed` + `error` string in `except`, with `finished` timestamp in `finally`.
3. **Public view**: the status endpoint MUST project each job through a JSON-safe view that drops the task handle (a leaked `Task` object 500s the poll while the job runs fine). Never serialize the raw job dict.
4. **Status endpoint** (`GET /api/vector/rebuild/status[?job_id]`): single job by id, or the full job list when omitted. Status vocabulary is exactly `queued | running | done | failed`.
5. **Frontend**: poll on an interval (1–2 s) with elapsed timer + counts; never `AbortSignal.timeout()` the sweep call. A read-only MCP observe tool (`vector_status`: counts + jobs) lets agents watch without triggering multi-hour rebuilds — the *trigger* stays REST/dashboard-gated behind human approval.

### B. Dedicated Webapp View Spec (`RAG / Index Operations`)

Rather than scattering buttons across Settings and Search tabs, each RAG server should maintain a dedicated **Operations / Sync Hub** (e.g. `pages/system/VaultSync.tsx` in `advanced-memory-mcp` or `features/RagOperations.tsx` in `docs-mcp`):

1. **Telemetry & KPI Header**:
   * **Total Indexed Chunks**: Live count from the database.
   * **Embedding Engine**: Active model name and accelerator (e.g. `bge-small-en-v1.5` on `CUDA 12 / ONNXRuntime-GPU`).
   * **Vector Dimensions**: 384 or 768.
   * **Last Sweep Timestamp**: ISO datetime of the most recent completed run.

2. **Sweep Mode Actions**:
   * **Incremental Sweep (Recommended)**: Scans only documents modified within the lookback window (default: 4 hours).
   * **Full Sweep (Deep)**: Wipes table state and re-chunks all discovered roots.
   * **Scoped Sweep**: Re-indexes a single folder or selected project repository.

3. **Active Job Terminal & Progress**:
   * Live elapsed time counter (`T+00:14s`).
   * Phase indicator badge: `Scanning Files` → `Chunking AST` → `Computing Embeddings` → `Upserting LanceDB`.
   * Result banner with exact chunk count and error trace if failed.

4. **Directory Roots Table**:
   * Visual list of primary roots and extra paths (`DOCS_EXTRA_PATHS`).
   * Add/Remove directory inputs with validation status.

---

### C. MCP Tooling Standard

All RAG-enabled servers must expose standardized tool interfaces:

```python
@mcp.tool()
async def rag_sweep(
    mode: str = "incremental",
    hours: int = 4,
    target_path: str | None = None,
    ctx: Context = None,
) -> dict:
    """Trigger an incremental or full semantic index sweep.
    
    Args:
        mode: 'incremental' (modified files only) or 'full' (complete rebuild).
        hours: Lookback window in hours for incremental mode (default: 4).
        target_path: Optional repo-relative or absolute path to scope the sweep.
    """
    ...
```

* **Progress Reporting**: In stdio or SSE mode, tools must call `ctx.report_progress(current, total)` so client UIs (Claude Desktop, Antigravity) render native progress bars during long embedding cycles.

---

## 4. Immediate Roadmap & Implementation Priorities

### Step 1: Fix Frontend 10s Timeouts (COMPLETED)
- `documentation-mcp`: Removed `AbortSignal.timeout(10000)` from `Settings.tsx` and `Documents.tsx`. Implemented 1.2s polling of `/api/reindex/{job_id}` until completion. Fixed `SemanticSearch.tsx` and `Search.tsx` to use `POST` instead of `GET`.

### Step 2: Implement MCP Reindex Tooling in `memops` (`advanced-memory-mcp`)
- Update `adn_system` or `adn_search` to support:
  ```python
  adn_system(operation="sync_vector_store", mode="full")
  ```
  or a dedicated `adn_rag(operation="sweep")` tool, linking directly into `scripts/rag_reindex.py` and `advanced_memory.search.vector_store`.

### Step 3: Standardize `mcp-central-docs` Webapp (`web_sota`)
- Adopt the background job queue in `mcd` backend (`src/docs_mcp/server.py`).
- Consolidate reindex buttons into an operational view matching `advanced-memory-mcp`'s `VaultSync.tsx`.

### Step 4: Elevate `plex-mcp` Dialogue RAG
- `plex-mcp`'s subtitle neural search (`sync_subtitles`) allows semantic matching over spoken movie dialogue.
- Ensure `PYTHONPATH` resolution for `docs_mcp.backend.rag_core` is automated in `just` recipes and startup scripts across Goliath/desktop environments.
