# Fleet Upgrade Strategy: FastMCP 3.5 Integration

**Last Updated:** 2026-07-20  
**Status:** Approved  
**Target Pin:** `fastmcp>=3.5.0,<4`  

This document outlines how the **Sandra SOTA Fleet** of MCP servers will leverage the caching, persistent storage, and OAuth features introduced in FastMCP 3.5.0, detailing target repositories and potential integration pitfalls.

---

## 1. Which Repositories Benefit Most?

We group our fleet servers by feature profiles to show which ones profit from specific 3.5 upgrades:

### Profile A: Subprocess & CLI Wrappers (Profit: Response Caching)
*   **Target Repos**: [podman-mcp](file:///d:/Dev/repos/podman-mcp), `sysinternals-mcp`, `autohotkey-mcp`, `reaper-mcp`.
*   **Why they benefit**: Spawning shell processes natively or via WSL2 (e.g. `podman ps`, `pslist.exe`) is CPU-expensive on Windows. Caching responses prevents duplicate executions when LLM agents poll state in quick succession.
*   **Implementation**: Add `cache_ttl=10` to status card endpoints to cache status for 10 seconds.

### Profile B: Web scrapers & Remote APIs (Profit: Response Caching)
*   **Target Repos**: `browser-mcp`, `scraper-mcp`, `arxiv-mcp`, `git-github-mcp`.
*   **Why they benefit**: Reduces outbound API calls and network latency. If an agent calls a tool to search for papers or read page content multiple times in a loop, cached responses bypass network calls entirely.
*   **Implementation**: Add `cache_ttl=300` (5 minutes) for search or content extraction tools.

### Profile C: Stateful Config & Memory Engines (Profit: Pluggable Storage)
*   **Target Repos**: `advanced-memory-mcp`, `bookmarks-mcp`, `edge-bookmark-mcp-server`, `quicknotes-mcp`, `obsidian-mcp`.
*   **Why they benefit**: Previously, stateful servers had to implement their own SQLite or JSON writing logic. 3.5's pluggable storage abstracts key-value persistence, making it easier to run in ephemeral containers (by swapping from local SQLite to Redis/Remote storage).
*   **Implementation**: Migrate ad-hoc JSON/SQLite config files to `ctx.server.storage.get()` and `set()`.

### Profile D: Auth-Broker Clients (Profit: OAuth PKCE & Introspection)
*   **Target Repos**: `tailscale-mcp`, `email-mcp`, `authentik`, `google-ai-mcp`.
*   **Why they benefit**: These servers use OAuth tokens to access remote services. Token introspection (RFC 7662) and storage ensure that access keys are validated securely at runtime and refreshed automatically.

---

## 2. Implementation Guide & Patterns

### Pattern A: Implementing Subprocess Caching (e.g., Podman Status)
For read-only tools that execute local processes:
```python
# Caches machine status for 15 seconds to avoid spawning wsl.exe repeatedly
@mcp.tool(cache_ttl=15)
async def podman_machine_status_card():
    # Runs "podman machine list" under the hood
    result = await manage_system(operation="status")
    return build_machine_status_card(result)
```

### Pattern B: Using Pluggable Storage for User Settings
For stateful servers that store credentials, paths, or prompt guidelines:
```python
@mcp.tool()
async def save_editor_path(path: str, ctx: Context) -> str:
    # Namespace preferences by key
    await ctx.server.storage.set("editor_path", path)
    return "Editor path updated successfully."

@mcp.tool()
async def get_editor_path(ctx: Context) -> str:
    path = await ctx.server.storage.get("editor_path")
    return path or "Not configured"
```

---

## 3. Breaking Changes & Migration Pitfalls

When upgrading your server files from `3.4.x` to `3.5.0`, watch out for the following details:

### A. The `mcp<1.17` Dependency Locking
*   **The Issue**: FastMCP 3.5.0 pins `mcp<1.17`. If any of your servers depend on features introduced in the Python MCP SDK v1.17+ (such as certain client-side multiplexing APIs), the upgrade will conflict.
*   **Mitigation**: For local fleet servers, standard tool and prompt registrations are completely compatible with the pinned version. Do not manually override the `mcp` version constraint in `pyproject.toml`.

### B. Storage Lifecycle Conflict (Persistent State Locks)
*   **The Issue**: When using the pluggable SQLite backend for storage, concurrent client instances (e.g., Cursor and Claude Desktop running at the same time) might trigger SQLite database lock contentions (`database is locked`).
*   **Mitigation**: If your server uses a persistent storage backend, you must implement the **Stdio Proxy Pattern** (run the FastAPI backend as a single HTTP daemon on port `10807` and have the clients connect via stdio proxies) to prevent lock conflicts.
*   **Client Compatibility (OpenCode & Agy)**: Since this pattern relies on a standard local stdio subprocess redirecting to an HTTP socket (via `fastmcp-remote`), it is fully supported by all SOTA fleet clients including **OpenCode** (configured in its workspace gateways settings) and **Agy** (allowing concurrent agentic planning sessions without database read/write locks).

### C. Caching Mutating Operations
*   **The Issue**: Applying `cache_ttl` to tools that modify state (e.g., `manage_containers(operation="start")`) will cause incorrect reports. The tool might return a cached success message from a previous run without actually starting the container.
*   **Rule of Thumb**: Only apply `cache_ttl` to read-only tools (annotated with `readonly=True` or visual card outputs). Never cache mutating operations.

---

## 4. Fleet Adoption & Bumping Timeline (Do Not Rush!)

> [!WARNING]
> FastMCP `3.5.0` introduces significant new middleware (caching, sqlite key-value backend, dependency pinning). Early adoption across the entire fleet presents a high regression risk. Fools rush in.

### The Phased Rollout Schedule:

1.  **Phase 1: The Guinea Pig Sandbox (Active Now)**
    *   **Action**: Pinned **`podman-mcp`** to `fastmcp>=3.5.0,<4` as our local testbed.
    *   **Why**: It is stateless and wraps local subprocess CLI commands. This allows us to test the stability of 3.5's packaging, uvicorn configurations, and log structures without risking persistent application data.
2.  **Phase 2: Freeze the Rest of the Fleet (Wait 10-14 Days)**
    *   **Action**: Keep all other production servers pinned to `fastmcp>=3.4.4,<4`. Do **NOT** upgrade high-traffic repos (such as `advanced-memory-mcp` or `tailscale-mcp`).
    *   **Why**: Wait to see if `3.5.1` is tagged to address early-adopter issues (such as SQLite database write locks under concurrent client access, or uncached JWT validation bugs).
3.  **Phase 3: Gradual Upgrade (Post-3.5.1 / Safe Window)**
    *   **Action**: Once `3.5.1` is stable or no major regressions are reported for 2 weeks, begin upgrading Profile A and B (read-only and subprocess servers) followed finally by Profile C (stateful databases).

---

## 5. Early Community Reactions & Field Reports

Based on developer forums, issue trackers, and GitHub release discussions within the first 48 hours:

### A. Relief Over SDK Pinning (`mcp<1.17`)
*   **Reaction**: **Highly Positive**.
*   **Details**: The Python MCP SDK `1.17` release introduced route shifts for `.well-known` configuration metadata. This broke reverse proxies, OAuth brokers, and Tauri desktop shells running composite apps. The pinning in `3.5.0` resolved this instantly, allowing existing custom auth setups to remain functional.

### B. Caching Praise & Mutation Warnings
*   **Reaction**: **Mixed / Cautionary**.
*   **Details**: While developers have praised the `@mcp.tool(cache_ttl=...)` response hashing middleware for accelerating slow external API or local subprocess commands (like server stats), many early bugs have been logged due to developers accidentally caching state-modifying operations (like starting or stopping containers). This has led to stale status reports.

### C. SQLite Concurrency Contention
*   **Reaction**: **Concerning**.
*   **Details**: When running the new pluggable SQLite storage backend under concurrent environments (e.g. Claude Desktop and Cursor initiating handshake queries simultaneously), some developers have encountered `database is locked` write errors. This reinforces our fleet policy to mandate the Stdio Proxy Pattern for all stateful servers utilizing `3.5.0` storage backends.

### D. Package Mismatches & Starlette Floors
*   **Reaction**: **Resolved via Workaround**.
*   **Details**: Some teams reported dependency collisions with Starlette/Uvicorn during the upgrade. The community has verified that executing a force reinstallation clears any half-removed points:
    ```bash
    pip install --force-reinstall fastmcp
    ```
