# 🐛 Bugs Depot (Master Index)

A centralized, performance-optimized registry of critical bugs, race conditions, and architectural failures.

## 📋 Schema
- **ID**: `BUG-XXX`
- **Severity**: 
    - `P0`: Critical (System Crash, Data Loss, Security)
    - `P1`: High (Major Feature Failure, Infinite Loops)
    - `P2`: Medium (UI Malformation, Non-blocking Functional Bugs)
    - `P3`: Low (Minor Glitches, Minor Dependency Issues)
- **Repo/Component**: The specific repository and component affected.
- **Symptom**: Observed behavior.
- **Root Cause**: The underlying technical failure.
- **Resolution**: How it was fixed or mitigated.
- **Log Snippet**: Relevant terminal/console output (Tail).
- **SOTA Impact**: Changes made to [AGENT_PROTOCOLS.md](../standards/AGENT_PROTOCOLS.md).

---

## 🗃️ Bug Registry

| ID | Sev | Date | Component | Symptom | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **[BUG-001](./details/BUG-001_OCR_Infinite_Loop.md)** | `P1` | 2026-03-18 | `ocr-mcp` | Infinite render loop in ScanViewer | ✅ Fixed |
| **[BUG-002](./details/BUG-002_Static_Input_Constraint.md)** | `P2` | 2026-03-18 | Webapp Inputs | Non-expanding/non-scrolling textboxes | ✅ Applied |
| **[BUG-003](./details/BUG-003_Malformed_Media_Scaling.md)** | `P2` | 2026-03-18 | Media Players | Video UI scaling (too small/large) | ✅ Applied |
| **[BUG-004](./details/BUG-004_Browser_Debug_Loop.md)** | `P1` | 2026-03-18 | Browser Subagent | Interaction with DOM-less/crashed pages | ✅ Guarded |
| **[BUG-005](./details/BUG-005_MCP_Server_Startup.md)** | `P3` | 2026-03-18 | MCP Tooling | Server startup race or missing dep | ✅ Resolved |
| **[BUG-006](./details/BUG-006_LMStudio_Missing_v1_Prefix.md)** | `P2` | 2026-06-23 | Plex-mcp, Calibre-mcp, AiWatcher-mcp | LLM chat fails `"Unexpected endpoint"` with LMStudio | 🔧 Active |
| **BUG-007** | `P2` | 2026-07-12 | Fleet-wide (94 files) | `mcp.http_app()` default `path="/mcp"` + `app.mount("/mcp")` creates double prefix → all MCP HTTP calls return 404 | ✅ Fixed |
| **[BUG-008](details/BUG-008_http_app_double_prefix.md)** | `P2` | 2026-07-12 | Fleet-wide | FastMCP `http_app()` double-prefix when mounted at `/mcp` | ✅ Fixed |
| **[BUG-007](./details/BUG-007_Tauri_Zoom_Dev_Broken.md)** | `P2` | 2026-06-25 | **14 fleet repos** | Ctrl+scroll zoom broken in dev browser — `e.preventDefault()` kills native zoom, Tauri API fails silently, nothing happens | ✅ Fixed |
| **[BUG-008](./details/BUG-008_Stale_llms_txt_Copypaste.md)** | `P3` | 2026-07-03 | **5 fleet repos** | `llms.txt` references "notepadpp-mcp" via automated template copypaste | ✅ Fixed |

---

## 📋 Registry Guidelines
- **Granularity**: One file per major bug in the `details/` directory.
- **Naming**: `BUG-XXX_[Descriptive_Title].md`
- **SOTA Impact**: Every bug MUST link to its corresponding hardening standard in `standards/`.
