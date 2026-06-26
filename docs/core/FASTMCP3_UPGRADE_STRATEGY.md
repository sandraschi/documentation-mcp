# FastMCP 3.x Fleet Upgrade Strategy

**Date:** 2026-06-06 (updated)  
**Original trigger:** FastMCP 3.0 GA released February 18, 2026  
**Fleet standard:** `fastmcp>=3.4.2,<4` (June 2026 SOTA) — minimum **3.2.0** until batch bump completes  
**Status:** docs-mcp on 3.2 ✅ | unity3d-mcp on 3.2 ✅ | Remaining fleet: SOTA Bash in progress | **3.4 docs:** [../fastmcp/3.4-features.md](../fastmcp/3.4-features.md)

---

## Background — The FastMCP Family Tree

```
FastMCP 1.0 (jlowin, 2024)
    │
    ├──► Anthropic absorbed into mcp Python SDK (frozen there as "official")
    │    Package: mcp  (pip install mcp)
    │    This is what Claude Desktop / Cursor use internally.
    │    Not what our servers use directly.
    │
    └──► Standalone continued by jlowin → 2.x series
         2.x → ... → 2.14.5  (last 2.x)
         Package: fastmcp  (pip install fastmcp)

FastMCP 2.14.5 (last 2.x, Dec 2025)
    │
    └──► FastMCP 3.0 (PrefectHQ/fastmcp, GA Feb 18 2026)
         Repo moved: jlowin/fastmcp → PrefectHQ/fastmcp
         PyPI unchanged, imports unchanged
         3.0.2 was current at GA

FastMCP 3.0.2
    │
    └──► FastMCP 3.1 (Mar 2026)
         Adds: Prompts, SkillsProvider, OpenAPIProvider, sample_stream
    │
    └──► FastMCP 3.1.1 (Mar 14 2026)
         Adds: CodeMode (BM25 tool discovery), Prefab integration
               (Python DSL → React UI), SearchTools, MultiAuth,
               PropelAuth, lazy imports
    │
    └──► FastMCP 3.2.0 (Mar 30 2026)
         Adds: GenerativeUI provider (prefab-ui 0.14.0),
               `fastmcp dev apps` browser preview command
         Fixes: SSRF path traversal (GHSA-vv7q-7jx5-f767),
                skill download path traversal,
                PyJWT CVE-2026-32597, OAuthProxy scopes
    │
    └──► FastMCP 3.3.x (May 2026)
         Adds: fastmcp-slim, AzureB2CProvider, run_in_thread=False,
               OAuth proxy hardening, OTEL list instrumentation
    │
    └──► FastMCP 3.4.2 (Jun 2026) ← FLEET TARGET
         Adds: fastmcp-remote, ToolResult(is_error=),
               fastmcp_access_token_expiry_seconds, Code Mode safe defaults
         Breaking: proxy initialize forwarded upstream (fail-loud bridges)
         Fixes: starlette>=1.0.1 (CVE-2026-48710), Clerk JWT headers (3.4.2)
```

**Key point:** The "official Anthropic" FastMCP is version 1.0, frozen in the `mcp` SDK.
FastMCP 2.x, 3.0, and 3.x are the actively maintained standalone framework — not "official" but
the de facto standard (70% of all MCP servers, 1M downloads/day).

---

## Fleet Standard: `fastmcp>=3.4.2,<4`

All servers' `pyproject.toml` should target:

```toml
[project]
dependencies = [
    "fastmcp>=3.4.2,<4",
    # ... other deps
]
```

Until the fleet batch bump completes, **`>=3.2.0`** remains the documented minimum. Prioritize **3.4.2** for any server using proxies, OAuth HTTP transport, CodeMode, or Clerk-style JWTs.

**Do NOT** pin an upper bound like `<3.5.0` unless you have a specific reason — the 3.x line
has been stable and upper-bound pinning creates unnecessary maintenance overhead.

---

## What Changed in 3.0 — Relevance to Our Fleet

### Breaking changes

| Change | Impact | Action |
|---|---|---|
| `@mcp.tool()` decorator returns original function (not component object) | Low | None for our servers |
| `ctx.set_state()` / `ctx.get_state()` now async | Medium | Add `await` |
| 16 deprecated `FastMCP()` constructor kwargs removed | Low | Remove stale kwargs |
| `mount(subserver, prefix=...)` → `mount(subserver, namespace=...)` | Low | Rename kwarg in composite servers |
| `mcp.add_tool_transformation()` → `mcp.add_transform()` | Low | Rename if used |
| `FastMCP.as_proxy()` → `create_proxy()` | Low | Update proxy servers |
| `ctx.session.create_message()` removed | Medium | Use `ctx.sample()` |
| `_fastmcp` metadata namespace → `fastmcp` | Very low | Internal only |

### Non-breaking improvements in 3.0

| Feature | Benefit |
|---|---|
| `ctx.sample()` as the only sampling API | Cleaner, officially supported |
| `FileSystemProvider` | Tools from directory with hot-reload |
| `fastmcp discover` CLI | Scans Claude Desktop/Cursor configs, inventory |
| `fastmcp list` / `fastmcp call` CLI | Debug any server without Claude Desktop |
| `run_stdio_async()` still exists | No change to our entry points |

---

## What Changed in 3.1 — New Capabilities

3.1 adds features rather than removing things. No new breaking changes from 3.0.

| Feature | What it is |
|---|---|
| `@mcp.prompt` decorator | Server-defined reusable prompt templates with parameters |
| `SkillsDirectoryProvider` | Expose skill directories as `skill://` MCP resources |
| `ClaudeSkillsProvider` / `CursorSkillsProvider` | Platform-native skill directories |
| `OpenAPIProvider` | Auto-generate MCP tools from any OpenAPI/Swagger spec |
| `ctx.sample_stream()` | Streaming sampling responses |
| Improved `fastmcp discover` output | More detail, JSON mode |

## What Changed in 3.1.1 — Additive

| Feature | What it is |
|---|---|
| **CodeMode** | BM25 tool discovery — agent writes and executes code without knowing tool names upfront |
| **Prefab integration** | Python DSL compiles to React UI rendered directly in conversation |
| **SearchTools** | Standalone transform for adding search across tool results |
| **MultiAuth** | Multiple auth providers per server |
| **PropelAuth** | PropelAuth provider out of the box |
| **Lazy imports** | Heavy deps deferred until first use; faster cold start |

### 3.1.1 SOTA: The 3-4-100 Standard

All tools MUST follow the **3-4-100** docstring standard for zero-prompt discovery:
- **3-word** command name (action_object_context)
- **4-word** one-line summary (Verb Object Context Detail)
- **100-character** detailed description (Context, Side Effects, Constraints)

Full details: `standards/MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md`

---

## What Changed in 3.2 — Security + GenerativeUI

3.2.0 released March 30, 2026. Primarily security fixes and the GenerativeUI provider.
No breaking changes from 3.1.x.

| Change | Type | Detail |
|---|---|---|
| **GenerativeUI provider** | Feature | `prefab-ui>=0.14.0` — stream UI components from tool results |
| **`fastmcp dev apps`** | Feature | Browser preview command for app development |
| SSRF path traversal | Security fix | GHSA-vv7q-7jx5-f767 |
| Skill download path traversal | Security fix | — |
| PyJWT CVE-2026-32597 | Security fix | JWT validation bypass |
| OAuthProxy scopes | Bug fix | Scopes not forwarded correctly |

**All servers should be on 3.2.0 for the security fixes alone.** Target **3.4.2** for proxy, OAuth, and Starlette CVE fixes.

To use GenerativeUI:
```toml
dependencies = [
    "fastmcp>=3.4.2,<4",
    "prefab-ui>=0.14.0",  # only if using GenerativeUI
]
```

---

## What Changed in 3.4 — Remote Control (June 2026)

Full guide: [../fastmcp/3.4-features.md](../fastmcp/3.4-features.md)

| Change | Type | Detail |
|---|---|---|
| **`fastmcp-remote`** | Feature | stdio bridge to HTTP MCP servers; OAuth auto for HTTPS |
| **Proxy `initialize` forward** | **Breaking** | Bridges fail at handshake if upstream missing or misconfigured |
| **`ToolResult(is_error=True)`** | Feature | Structured tool errors without raising |
| **`fastmcp_access_token_expiry_seconds`** | Feature | OAuth proxy tokens survive idle beyond short upstream TTL |
| **Code Mode defaults** | Security | 30s / 100MB sandbox; 50 tool calls per execute |
| **starlette>=1.0.1** | Security (3.4.1) | CVE-2026-48710 |
| **JWT private headers** | Fix (3.4.2) | Clerk and similar providers |

**All HTTP/OAuth servers should plan for 3.4.1+.** Proxy-heavy servers should adopt 3.4.0+ behavior and remove silent bridge registration errors.

## New Pattern: Startup Connectivity Probes (3.1+ lifespan)

Servers that depend on external resources (databases, APIs, filesystems) should probe
connectivity in `server_lifespan` before the `yield`, so Claude Desktop marks them as
failed with an actionable error rather than silently starting a broken server.

Full pattern and template: `standards/fastmcp-3.2-startup-probes.md`

Reference implementation: `calibre-mcp/src/calibre_mcp/server.py` → `_probe_calibre_connectivity()`

Quick summary:
```python
@asynccontextmanager
async def server_lifespan(mcp_instance: FastMCP):
    log = logging.getLogger("myserver.lifespan")
    await _probe_connectivity(log)   # raises RuntimeError if unreachable
    yield
```

---

## Migration Effort Classification (for 2.x → 3.2)

### Group A: Version bump only (~60% of fleet)
Servers using only `@mcp.tool()`, basic FastMCP, no ctx.set_state, no proxy mounting.

```powershell
# Edit pyproject.toml: fastmcp>=3.2.0
# Then:
uv sync
```

**Estimated effort:** 5 minutes per server.

### Group B: Minor code changes (~30% of fleet)
Servers using `ctx.session.create_message()` → replace with `ctx.sample()`.
Servers using `ctx.set_state()` / `ctx.get_state()` → add `await`.

**Estimated effort:** 15–30 minutes per server.
**Servers to check:** advanced-memory-mcp, local-llm-mcp

### Group C: Moderate changes (~10% of fleet)
Servers using `mount(prefix=...)` → rename to `namespace=`.
Servers using removed `FastMCP()` constructor kwargs.

**Estimated effort:** 30–60 minutes per server.
**Servers to check:** mcp-federation-hub (done ✅), dark-app-factory

---

## Fleet Upgrade Plan (April 2026)

### Phase 1 — Standards update ✅ (2026-04-02)
- Fleet standard updated to `fastmcp>=3.2.0`
- REPO_SOTA_BASH.md created as the authoritative modernization recipe.

### Phase 2 — Core SOTA Bash Implementation
1. `docs-mcp` — ✅ Done (Markdown output overhaul + Ruff 120)
2. `unity3d-mcp` — ✅ Done (Dual-mode bridge + Ruff 120)
3. `advanced-memory-mcp` — status: check FLEET_INDEX.md

### Phase 3 — Batch upgrade Group A servers
```powershell
# Find all repos with old fastmcp pin
Select-String -Path "D:\Dev\repos\*\pyproject.toml" -Pattern "fastmcp>=[0-9]" -Recurse |
    Where-Object { $_.Line -notmatch "3\.[2-9]" } |
    Select-Object Path, Line

# For each: edit pyproject.toml, run uv sync, test
```

### Phase 4 — Group B/C individual fixes
Handle ctx.sample() migrations and namespace renames server by server.

---

## One-Line Test for Any Server

After bumping the version and running `uv sync`:

```powershell
# Test stdio startup (Ctrl+C to exit)
& "D:\Dev\repos\<server>\.venv\Scripts\python.exe" -m <server_module>
```

If it starts without ImportError or TypeError → Group A complete.
If it errors → check the breaking changes table above.

```powershell
# Also useful: inspect the server without Claude Desktop
fastmcp list "D:\Dev\repos\<server>\src\<package>\server.py"
fastmcp discover --client claude
```

---

## What We Do NOT Need to Do

- Change `from fastmcp import FastMCP` imports — correct in all servers
- Update the `mcp` package separately — fastmcp manages it as a dependency
- Migrate to `FileSystemProvider` — decorator-based tools still work identically
- Remove `@mcp.tool()` parentheses — both forms still work

---

## References

- FastMCP 3.0 GA: https://www.jlowin.dev/blog/fastmcp-3-launch
- FastMCP changelog: https://gofastmcp.com/changelog
- Upgrade guide: https://gofastmcp.com/development/upgrade-guide
- GitHub: https://github.com/PrefectHQ/fastmcp
- PyPI: https://pypi.org/project/fastmcp/
- History of FastMCP: `standards/HISTORY_OF_FASTMCP.md`
- Startup probes pattern: `standards/fastmcp-3.2-startup-probes.md`
- Concurrency safety: `standards/fastmcp-3.2-concurrency.md`
