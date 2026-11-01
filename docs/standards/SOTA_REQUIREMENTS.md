---
title: "SOTA Requirements (Service-Oriented Thinking Architecture)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# SOTA Requirements (Service-Oriented Thinking Architecture)

## 1. Core Principles

To maintain peer technical contributor status, all MCP servers must adhere to the SOTA v12.0 core principles:

1.  **Architecture**: Strict modularity, dual-transport support (STDIO/HTTP), and clean separation of concerns.
2.  **Behavior**: High-quality tool documentation (including the [agentic checklist & pagination](./TOOL_DESIGN_STANDARDS.md) §4–§9) and iterative sampling patterns.
3.  **Operations**: Complete lifecycle management (Lifespans) and correlation tracing.
4.  **Strategy**: Adherence to the [Container Orchestration Strategy](../patterns/CONTAINER_ORCHESTRATION_STRATEGY.md) (Docker Compose vs. K8s).
5.  **Networking**: MANDATORY port reservoir in [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md) for all webapps (currently 10700-12000 — check the file, do not hardcode the range). Frontend and Backend ports MUST be kept together (Adjacent Rule). See [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md) and [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) for full specifications.
    - [Bugs Depot](../troubleshooting/BUGS_DEPOT.md) - Registry of critical bugs and race conditions.
    - [React Hardening Standards](./REACT_HARDENING.md) - Proactive stability patterns.
    - [REPO_SOTA_BASH](./REPO_SOTA_BASH.md) - Official recipe for repo modernization sprints.

---

## 2. FastMCP 3.4+ Standards

### 2.1. Feature Set
- **Prompts**: Context-aware instruction sets registered via `@mcp.prompt()`.
- **Resources**: Dynamic data streams via `@mcp.resource()`.
- **Async Sampling**: Non-blocking tool orchestration using `ctx.sample()`.
  > ⚠️ **`ctx.sample()` is deprecated by the MCP 2026-07-28 spec**, which moves to a
  > stateless core and replaces sampling and roots with **MRTR** (Multi Round-Trip
  > Requests). FastMCP 4 ships first-class support. Do not build new work on
  > `ctx.sample()`; see [fastmcp/2026-07-28-spec-migration.md](../fastmcp/2026-07-28-spec-migration.md)
  > and the FastMCP row in [JUNE_2026_STANDARDS_BAR.md](./JUNE_2026_STANDARDS_BAR.md).
  > Existing servers keep working until FastMCP 4 lands.
- **Skills Provider**: Ability to register and discover local skill directories.
- **Vibe Coding XR**: Approved rapid-prototyping workflow for spatial interactions (Gemini + XR Blocks) — **[VIBE_CODING_XR.md](./VIBE_CODING_XR.md)**.

### 2.2. MCP Apps and Prefab UI (fleet mandatory)

**Packaging:** Declare **`prefab-ui>=0.14.0`** in **`[project.dependencies]`** (core dependency) on every Python **`*-mcp`** repo — not only an optional extra. Operators may still set a **per-server env flag** (e.g. `*_PREFAB_APPS=0`) to **skip registering** App tools in CI or headless images; the package remains installable and importable.

**Tool coverage (MUST):** Any tool whose job is primarily **listing** (collections, search results, directories, inventories), **status** (health, connectivity, readiness), **statistics** (counts, aggregates, dashboards), or **multi-row / multi-field summaries** MUST ship a **Prefab** surface: either a dedicated **`@mcp.tool(app=True)`** (e.g. `show_*_prefab_card`, `*_status_app`) or the same operation returning **`ToolResult`** with **`structured_content=PrefabApp(...)`**, following **[MCP Apps, Prefab UI, and FastMCP](../fastmcp/mcp-apps-prefab-ui.md)** and **[Tool Design §3.3 / §4](./TOOL_DESIGN_STANDARDS.md)**. **Always** set **`content`** to a full plain-text summary for hosts that do not render Apps.

**Exceptions** are allowed only when **documented in the repo PRD** (e.g. embedded-only, no chat surface). Single-value or trivially tiny responses may remain dict-only.

**Plain-text fallbacks** remain mandatory for accessibility; Prefab is the **default SOTA** presentation for list/status-class outputs in chat.

Strategic comparison to standalone webapps: **[prefab-vs-webapps.md](../fastmcp/prefab-vs-webapps.md)**. **Use cases and examples:** **[mcp-apps-prefab-use-cases-and-examples.md](../fastmcp/mcp-apps-prefab-use-cases-and-examples.md)**.

---

### 2.3. HTTP Daemon + Stdio Proxy Pattern (fleet mandatory)

Servers with persistent state (SQLite, LanceDB, file watchers) MUST implement this pattern to prevent database contention from concurrent stdio instances spawned by multiple clients.

**Premise:** A long-running HTTP daemon owns the database. All stdio MCP clients (Claude Desktop, opencode, Cursor) connect via a lightweight proxy that forwards tool calls to the HTTP daemon — no second DB connection, no lock contention, no stale lockfiles.

```
HTTP daemon (owns DB, runs 24/7) ←→ Stdio proxies (zero DB, forward only)
                                          ├── Claude Desktop
                                          ├── opencode
                                          └── Cursor
```

**Implementation (add to `main()` in the stdio entry point before any initialization):**

```python
import os, httpx
from fastmcp.server import create_proxy

HTTP_URL = os.getenv("SERVER_API_URL", "http://127.0.0.1:10946")  # per-repo default
MCP_URL = f"{HTTP_URL}/mcp"

def main():
    try:
        r = httpx.post(MCP_URL, json={"jsonrpc":"2.0","id":1,"method":"initialize",
            "params":{"protocolVersion":"2025-11-25","capabilities":{},
                      "clientInfo":{"name":"probe","version":"1"}}},
            headers={"Accept":"application/json, text/event-stream"}, timeout=3)
        if r.status_code == 200:
            proxy = create_proxy(MCP_URL, name="server-name-mcp")
            asyncio.run(proxy.run_stdio_async(show_banner=False))
            return  # HTTP daemon handles all tool calls
    except Exception:
        pass  # No HTTP daemon — start normally

    # ... full initialization (DB, tools, sync) ...
```

**Env var:** `SERVER_API_URL` overrides the default HTTP endpoint (so the same binary works in dev and production).

**Reference implementations:**
- `advanced-memory-mcp`: `src/advanced_memory/cli/commands/mcp.py` — probes 127.0.0.1:10732/mcp
- `aiwatcher-mcp`: `src/aiwatcher_mcp/server.py` — probes 127.0.0.1:10946/mcp

**When NOT to probe:**
- Stateless servers (fetch, playwright, git-github) — no DB, no contention
- Single-client servers that never run a 24/7 HTTP daemon

**NSSM + stdio duality (fleet ops):** When the same repo runs as an NSSM HTTP daemon **and** as a Cursor stdio server, the stdio path MUST proxy to the daemon whenever it is reachable. Never run two full stacks against one SQLite/LanceDB path. For LocalSystem services, NSSM `AppEnvironment` MUST pin `USERPROFILE` and any repo home env (`ADVANCED_MEMORY_HOME`, etc.) to match the interactive user; otherwise MCP can report success while the webapp shows an empty index. See `advanced-memory-mcp/docs/troubleshooting/BUG_REPORT_NSSM_SPLIT_BRAIN.md`, `mcp-central-docs/scripts/Start-MemopsDaemon.ps1`, and [NEW_REPO_BUILD_COMPLETE.md](./NEW_REPO_BUILD_COMPLETE.md) §G.

**Assess severity:** Missing probe when the repo has persistent state = MEDIUM; missing probe **with** a documented NSSM HTTP service for the same binary = HIGH (`repo-assess-and-fix.md` §1B).

### 2.4. Native Desktop Installer (NSIS/Tauri)

Any repo shipping a Tauri desktop wrapper MUST follow **[rules/tauri_nsis_building.md](rules/tauri_nsis_building.md)** — the single-source standard for:
- **Directory layout**: `native/` or `web_sota/src-tauri/`
- **Embedded backend**: PyInstaller → `bundle.resources` (NOT `externalBin`)
- **Spec file**: `strip=False, upx=False` (mandatory — `strip=True` corrupts the PKG on Windows)
- **Binary SKIP list**: Controls installer size (filters `a.binaries`, leaves `a.pure` intact)
- **Build script**: `native/build.ps1` handles the full pipeline (frontend → PyInstaller → Tauri → NSIS)
- **NSIS hooks**: PREINSTALL/PREUNINSTALL kill both operator and backend processes

Every repo with a `native/` directory MUST pass `just cua-nsis-test` before release — see [rules/cua_nsis_smoke_testing.md](rules/cua_nsis_smoke_testing.md).

## 3. Repository scaffold (Python MCP — build & distribution)

In addition to FastMCP behavior, Python fleet servers SHOULD ship:

- **`uv`** + **`pyproject.toml`** + committed **`uv.lock`**
- Root **`justfile`** (run, test, lint; optional MCPB pack recipe)
- Root **`llms.txt`** + **`llms-full.txt`** (LLM index + full corpus, **both required**) — [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) §1 · [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md)
- Root **`glama.json`** (Glama discovery)
- **`mcpb pack`** for **`.mcpb`** when Claude Desktop distribution is in scope — see **[PACKAGING_STANDARDS.md §5](./PACKAGING_STANDARDS.md#5-python-mcp-repo-uv-justfile-llmstxt-glama-mcpb-pack)** and **[MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md)**
- **Pre-commit + Ruff** (`.pre-commit-config.yaml`) and **`ty` in CI** (`continue-on-error: true` until green) — **[PACKAGING_STANDARDS.md §6](./PACKAGING_STANDARDS.md#6-optional-ergonomics-pre-commit-ruff-ty-in-ci-non-blocking)** and **[CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md)**
- **Industrialization**: See **[REPO_SOTA_BASH.md](./REPO_SOTA_BASH.md)** for the definitive modernization recipe.
