# History of FastMCP

**Document type**: Reference / Background  
**Last updated**: 2026-03-14  
**Scope**: Comprehensive technical history of the FastMCP ecosystem from 2024 to present  

---

## Overview

FastMCP is the dominant framework for building Model Context Protocol (MCP) servers in Python. What started as a single developer's quality-of-life wrapper grew into a 1 million downloads/day infrastructure layer powering the majority of the MCP ecosystem. Its history involves two complete ownership transfers, a major corporate acquisition, and a pivot from an Anthropic side-effect to a Prefect platform pillar â€” all within roughly 18 months.

---

## Part 1: Origins â€” The MCP Protocol (Late 2024)

### Anthropic's Model Context Protocol

In November 2024, Anthropic published the **Model Context Protocol** (MCP) specification â€” an open standard for connecting AI models to external tools, data sources, and services. The core idea: instead of every LLM integration being bespoke glue code, define a standard wire protocol (JSON-RPC over stdio/SSE/HTTP) so tools and models can interoperate.

Anthropic shipped a reference implementation in the `mcp` Python package, which provides:
- Low-level protocol machinery (JSON-RPC serialization, session management)
- A `FastMCP` class (version 1.0) that wraps the protocol in a decorator-based API
- TypeScript/Python SDKs

The `FastMCP` class in the official `mcp` SDK was genuinely good for its time â€” `@mcp.tool()` decorators, automatic schema generation from type hints, lifespan context managers. But it was still low-level in places, required verbose boilerplate for complex servers, and had limited composability.

---

## Part 2: FastMCP 1.0 â€” The Community Version (Late 2024)

### Jeremiah Lowin's Standalone Package

Shortly after Anthropic's release, **Jeremiah Lowin** â€” founder and CEO of [Prefect](https://prefect.io), a data pipeline orchestration company â€” built and published a standalone `fastmcp` package on PyPI. His version took the good ideas from Anthropic's `FastMCP` class and significantly extended them:

- **Simpler server composition**: `mcp.mount()` for composing multiple sub-servers
- **Resource templates**: Dynamic URIs like `resource://{user_id}/profile`
- **Context injection**: `ctx: Context` parameter auto-injection into tools
- **Better error handling**: More informative error messages and type coercion
- **Client utilities**: `fastmcp.Client` for testing servers without a full MCP host

This package lived at `jlowin/fastmcp` on GitHub. It was immediately popular in the MCP developer community because it solved real ergonomic problems the official SDK didn't address.

### The Naming Situation

This created an intentional but initially confusing naming situation:

| Package | PyPI name | GitHub | Maintained by | Status |
|---------|-----------|--------|---------------|--------|
| Anthropic SDK | `mcp` | `modelcontextprotocol/python-sdk` | Anthropic | Active (protocol layer) |
| Community version | `fastmcp` | `jlowin/fastmcp` â†’ `PrefectHQ/fastmcp` | Lowin/Prefect | Active (application layer) |

The `mcp` package internally contains a `FastMCP` class (imported as `from mcp.server.fastmcp import FastMCP`). The standalone `fastmcp` package provides `from fastmcp import FastMCP`. They are **different implementations** with different APIs, though they share conceptual DNA. Anthropic's version is frozen at 1.0 semantics; the standalone continues to evolve.

> **Import rule for our fleet**: Always use `from fastmcp import FastMCP` â€” never `from mcp.server.fastmcp import FastMCP`. The latter is the frozen Anthropic version.

---

## Part 3: FastMCP 2.x â€” Maturation and Explosion (Earlyâ€“Mid 2025)

### Rapid Feature Development

Throughout 2025, the standalone `fastmcp` package under Lowin's stewardship went through rapid iteration. Major 2.x milestones:

**2.0 â€“ Compositing Architecture**
- `mount()` API stabilized with prefix routing
- Sub-server composition: build large servers by mounting smaller ones
- `FileSystemProvider` for directory-based tool discovery (tools defined in separate files, auto-discovered at startup)
- Proper async context managers for lifespan events

**2.5 â€“ Sampling API**
- `ctx.sample()` introduced as the idiomatic way for servers to call back to the connected LLM
- This enabled "agentic" server patterns: a tool could ask Claude a question mid-execution
- `ctx.session.create_message()` deprecated in favor of `ctx.sample()`

**3.1.1+ â€“ Transport Layer**
- Multiple transport backends stabilized: stdio (for Claude Desktop), HTTP/SSE (for web clients), WebSocket
- `fastmcp serve` CLI for running servers in HTTP mode without writing a FastAPI app

**3.1.1+ â€“ Resource System**
- Resource templates with URI pattern matching
- Binary resource support (images, files)
- Resource subscriptions for real-time updates

**3.1.1+ â€“ Portmanteau Pattern / Tool Explosion Mitigation**
- Recognition that MCP clients (especially Claude Desktop) degrade severely with 40+ tools
- Community-developed "portmanteau" pattern: consolidate many operations behind a single tool with an `operation` discriminator parameter
- `fastmcp 3.1.1+.5` was the last stable 2.x release before the 3.0 restructuring

### Ecosystem Growth

By mid-2025, `fastmcp` had become **the** way to build MCP servers in Python. The number of servers on the Glama.ai marketplace, GitHub, and npm grew from dozens to thousands. FastMCP-based servers were being used for:
- Database access (PostgreSQL, SQLite, MongoDB)
- File system operations
- Web scraping and search
- Smart home control (Tapo, Philips Hue, MQTT)
- Code execution environments
- Local LLM routing (Ollama, LM Studio)
- IoT and robotics (ROS integration)

The `mcp` (Anthropic) package saw relatively slower adoption for new servers because `fastmcp` was simply more productive. Anthropic's SDK remained important as the protocol reference implementation and for TypeScript servers.

---

## Part 4: The Prefect Acquisition (Late 2025)

### Corporate Context

Jeremiah Lowin, having built FastMCP as an individual project, made a strategic decision: move the project under the Prefect organization. This was formalized by transferring the GitHub repository from `jlowin/fastmcp` to `PrefectHQ/fastmcp`.

The rationale was clear in retrospect:
- FastMCP had grown too large to maintain as a solo side project
- Prefect's core business is workflow orchestration â€” MCP servers are workflow triggers/executors
- The two products had strong natural integration: Prefect flows could be exposed as MCP tools, and MCP tools could be orchestrated as Prefect tasks
- Corporate resources (engineering, testing, documentation, support) could be applied

### What Changed at Transfer

The transfer was not just administrative:
- CI/CD moved to Prefect's infrastructure
- Documentation moved to `docs.prefect.io/fastmcp` 
- Release cadence formalized with proper changelogs and semver discipline
- Community Discord integrated with Prefect's community channels
- Enterprise support contracts became possible

The Python package on PyPI continued to be `fastmcp` (no rename). Import paths did not change. Existing servers required no modification just because of the org transfer.

---

## Part 5: FastMCP 3.0 and 3.1

### 3.0 GA â€” February 18, 2026

FastMCP 3.0 released as GA on **February 18, 2026**. Current 3.0 release: **3.0.2**.

This was a significant release, not just a version bump. Key themes:

**1. API Cleanup**
- 16 deprecated `FastMCP()` constructor kwargs removed (mostly rarely-used config params from 1.x era)
- `ctx.set_state()` and `ctx.get_state()` made properly async (were accidentally sync-returning awaitables in 2.x)
- `mount(prefix=...)` renamed to `mount(namespace=...)` â€” semantically clearer

**2. Sampling as First-Class**
- `ctx.sample()` is now the only supported way to call back to LLMs
- `ctx.session.create_message()` removed entirely
- Sampling supports streaming responses via `ctx.sample_stream()`
- Sampling tools integration: a server can specify tools available to the LLM during sampling

**3. `fastmcp discover` CLI**
- Scans Claude Desktop, Windsurf, Cursor config files and reports all registered MCP servers
- Shows status, transport type, and tool count for each
- Useful for fleet auditing: `fastmcp discover --client claude` gives a full inventory

**4. Performance**
- Async I/O throughout â€” no more sync blocking in path resolution or file operations
- Connection pooling for HTTP transport
- Lazy loading for `FileSystemProvider`-based servers

**5. Prefect Horizon Integration**
- FastMCP 3.0 is a core pillar of Prefect's "Horizon" platform
- MCP servers can be deployed as Prefect work pool workers
- Prefect flows can be exposed as MCP tools with one decorator
- Observability: MCP tool calls appear in Prefect's run history

### 3.1 â€” March 2026

3.1 added new capabilities on top of the 3.0 foundation with no new breaking changes:

- **`@mcp.prompt` decorator** â€” Server-defined reusable prompt templates with optional parameters. Clients call `get_prompt(name, arguments)` and inject the returned messages into the conversation.
- **`SkillsDirectoryProvider`** â€” Exposes a directory of skill folders as MCP resources under the `skill://` URI scheme. Also provides `ClaudeSkillsProvider`, `CursorSkillsProvider` for platform-native skill dirs.
- **`OpenAPIProvider`** â€” Auto-generates MCP tools from any OpenAPI 3.x / Swagger spec. A REST API with 50 endpoints becomes 50 MCP tools in ~3 lines of code.
- **`ctx.sample_stream()`** â€” Streaming variant of `ctx.sample()` for LLM responses that benefit from progressive delivery.
- **Improved `fastmcp discover`** â€” JSON output mode, more detail per server, better error reporting.

The fleet standard was updated to `fastmcp>=3.1.0` in March 2026. See `fastmcp/3.1-features.md` and `fastmcp/3.0-to-3.1-improvements.md` for full details.

### Download Scale

By early 2026, FastMCP was at **~1 million downloads per day** on PyPI, making it one of the fastest-growing Python packages in history. It powers an estimated 70% of all Python MCP servers by volume. The combination of Anthropic's MCP adoption push and FastMCP's developer ergonomics created a flywheel: more Claude Desktop users â†’ more MCP server developers â†’ more FastMCP usage.

---

## Part 6: Breaking Changes Across Versions

For migration purposes, here is the complete breaking change map:

### 1.x â†’ 2.x (Anthropic `mcp` â†’ standalone `fastmcp`)
These are conceptual breaks â€” the packages are independent:
- Import path: `from mcp.server.fastmcp import FastMCP` â†’ `from fastmcp import FastMCP`
- Different tool registration internals (not API-visible for basic use)
- Sampling: `ctx.session.create_message()` (mcp) vs `ctx.sample()` (fastmcp 2.5+)

### 2.x â†’ 3.0 (standalone package upgrade)
| Change | Impact | Action needed |
|--------|--------|---------------|
| `ctx.set_state()` now async | Servers using state management | Add `await` |
| `ctx.get_state()` now async | Servers using state management | Add `await` |
| `mount(prefix=...)` â†’ `mount(namespace=...)` | Composite servers | Rename kwarg |
| 16 constructor kwargs removed | Servers using obscure config | Remove kwargs |
| `ctx.session.create_message()` removed | Servers using sampling in 2.x style | Use `ctx.sample()` |
| Decorator returns original function | Servers treating result as `FunctionTool` | Update references |

For our fleet (~132 servers): ~60% need only a version bump, ~30% need `ctx.sample()` migration, ~10% need `await` additions for state calls.

---

## Part 7: Relationship to Anthropic

A common point of confusion: **Anthropic did not build FastMCP 2.x/3.x**. The relationship is:

- Anthropic created the MCP **protocol specification** and reference SDK (`mcp` package)
- Anthropic's SDK contains a `FastMCP` class (version 1.0 semantics, frozen)
- The standalone `fastmcp` package (2.x, 3.x) was community-built, is independently maintained, and is now a Prefect product
- Anthropic endorses FastMCP as the recommended Python framework for building MCP servers but does not control its development
- Claude Desktop, Cursor, Windsurf etc. all support MCP via the protocol specification â€” they don't care whether you used `mcp` or `fastmcp` to build your server

This means:
- Anthropic breaking changes â†’ affect the protocol wire format, not FastMCP's Python API
- FastMCP breaking changes â†’ affect Python server code, not the wire protocol
- The two can evolve somewhat independently

---

## Part 8: Timeline Summary

| Date | Event |
|------|-------|
| Nov 2024 | Anthropic publishes MCP protocol spec + reference `mcp` SDK |
| Nov 2024 | Jeremiah Lowin publishes standalone `fastmcp` 1.x on PyPI |
| Dec 2024 | FastMCP 2.0 â€” compositing, `mount()`, `FileSystemProvider` |
| Q1 2025 | FastMCP 2.5 â€” `ctx.sample()` sampling API introduced |
| Q2 2025 | FastMCP 3.1.1+ â€” transport layer stabilized (stdio/SSE/WebSocket) |
| Q3 2025 | FastMCP 3.1.1+ â€” resource templates, binary resources |
| Q4 2025 | FastMCP 3.1.1+ â€” portmanteau pattern, tool explosion mitigation |
| Q4 2025 | FastMCP 3.1.1+.5 â€” last 2.x release |
| Late 2025 | Repository transferred: `jlowin/fastmcp` â†’ `PrefectHQ/fastmcp` |
| Feb 18 2026 | FastMCP 3.0 GA â€” API cleanup, proper async, Prefect Horizon integration |
| Feb 2026 | v3.0.2 current; ~1M downloads/day |
| Mar 2026 | FastMCP 3.1 â€” Prompts, SkillsProvider, OpenAPIProvider, sample_stream |
| Mar 2026 | Fleet standard updated to `fastmcp>=3.1.0` |

---

## Part 9: Practical Guidance for Our Fleet

### Which version to use

**Fleet standard as of March 2026**: `fastmcp>=3.1.0`

Update `pyproject.toml` for all servers. 3.1 is backward-compatible with 3.0 â€” no code changes required unless you want to use the new 3.1 features.

### Which import to use

```python
# CORRECT â€” standalone fastmcp (3.0+)
from fastmcp import FastMCP

# WRONG â€” frozen Anthropic version (1.0 semantics, no updates)
from mcp.server.fastmcp import FastMCP
```

### How to tell which you have

```powershell
# Check what's installed in a server's venv
.venv\Scripts\python.exe -c "import fastmcp; print(fastmcp.__version__)"
# Should print 3.1.x or higher

# Check for wrong import in source
Select-String -Path "src\**\*.py" -Pattern "from mcp.server.fastmcp"
# Should return nothing â€” if it does, fix the import
```

### Sampling pattern (3.0 style)

```python
# 3.0+ correct
@mcp.tool
async def analyze_with_llm(data: str, ctx: Context) -> str:
    result = await ctx.sample(f"Analyze this: {data}")
    return result.text

# 2.x style â€” REMOVED in 3.0
# result = await ctx.session.create_message(...)
```

### State management (3.0 style)

```python
# 3.0+ â€” state operations are async
@mcp.tool
async def stateful_tool(ctx: Context) -> str:
    await ctx.set_state("key", "value")   # note: await required
    val = await ctx.get_state("key")       # note: await required
    return val
```

---

## References

- FastMCP GitHub: https://github.com/PrefectHQ/fastmcp
- FastMCP PyPI: https://pypi.org/project/fastmcp/
- Prefect Horizon docs: https://docs.prefect.io/fastmcp
- Anthropic MCP spec: https://modelcontextprotocol.io
- Anthropic `mcp` SDK: https://github.com/modelcontextprotocol/python-sdk
- Our fleet upgrade strategy: `standards/FASTMCP3_UPGRADE_STRATEGY.md`
- Glama.ai marketplace: https://glama.ai/mcp/servers?query=sandraschi

