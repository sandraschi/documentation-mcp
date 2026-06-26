# FastMCP CodeMode

**Last Updated:** 2026-03-23
**Status:** Experimental (core interface stable, discovery tool params may evolve)
**Applies to:** FastMCP 3.1+ (`fastmcp[code-mode]` extra required)
**Reference:** https://gofastmcp.com/servers/transforms/code-mode

---

## What Problem CodeMode Solves

Standard MCP has two scaling problems that hurt large servers:

**Problem 1 — Context bloat:** At session start, the full tool catalog is loaded into the
LLM's context. For a large server this can be tens of thousands of tokens before the LLM
reads a single word of user input. Every tool's name, description, and full JSON Schema
is included.

**Problem 2 — Sequential round-trips:** Each tool call is a round-trip through the context
window. The LLM calls a tool, the result flows back, the LLM reasons, calls the next tool.
Intermediate results that only exist to feed the next step still burn tokens every time.

**CodeMode's solution:** Replace the tool catalog with meta-tools. The LLM searches for
relevant tools on demand (BM25), inspects only the schemas it needs, then writes Python code
that chains all the tool calls in a sandbox. Intermediate results stay inside the sandbox —
they never touch the context window.

---

## How Claude Desktop Experiences CodeMode

> **This is the key operational insight for our fleet.**

When a FastMCP server uses CodeMode, Claude Desktop **does not see the underlying tools at
session start**. Instead it sees only the meta-tools — typically `Search` and `GetSchemas`.

**What this looks like in a Claude Desktop session:**

```
Standard server (no CodeMode):
  Session start → 43 tool schemas loaded into context → 8,000+ tokens consumed immediately

CodeMode server:
  Session start → 2-3 meta-tool schemas loaded → ~200 tokens consumed
  ...user asks something...
  Claude calls: tool_search(query="file operations")
  Server returns: [file_ops, dir_ops, repo_ops] schemas → loaded into context on demand
  Claude calls: fileops:file_ops(operation="read_file", ...)
```

**The `tool_search` call you see in Claude Desktop IS CodeMode in action.** It is not a
separate MCP feature, not lazy-loading at the protocol level, and not something Claude
Desktop does natively. It is the FastMCP 3.1 `Search` discovery tool being called by
Claude before it can use the actual tools.

### Why the call is necessary

Claude Desktop has no knowledge of what parameters `file_ops` takes until `tool_search`
(or `GetSchemas`) returns the schema. Without that call, any attempt to call `file_ops`
directly would be a hallucinated parameter list. The `tool_search` round-trip is the
price of not loading everything upfront — one extra call per topic area, paid once per
conversation rather than as permanent context.

### Naming note

FastMCP names the meta-tool `Search` internally. The tool name clients see depends on
how the server registers it — in our portmanteau servers (`fileops`, `memops`, `winops`,
`gitops` etc.) it appears as `tool_search`. This is the server author's chosen name, not
a FastMCP or MCP protocol name.

### Claude Desktop does not lazy-load tools natively

**Important vocabulary:** People often say “lazy loading” or “call `load_tools` first.”
In our stack, that behavior is **not** a Claude Desktop feature and **not** an MCP
protocol feature. It is **FastMCP CodeMode** exposing small **discovery meta-tools**
(typically `Search` / `tool_search`, and `GetSchemas` or an equivalent schema-fetch tool).

**What the model must do before calling a real tool:**

1. **Discover** — run the discovery tool (in our fleet this is usually `tool_search` with
   a natural-language query, which maps to CodeMode’s `Search`).
2. **Load schemas** — when parameters are not yet in context, fetch them via the schema
   tool CodeMode exposes (often named `GetSchemas` in FastMCP docs; some servers or clients
   surface this as schema retrieval — informally people say “load tools” or “load schemas”).
3. **Execute** — call the actual tool with real parameters, or run CodeMode’s code execution
   path if the server is configured for sandbox execution.

If step 1 or 2 is skipped, Claude has **no valid parameter schema** for the underlying tool
in the current context window. The failure mode is usually **hallucinated arguments** or a
client-side tool call error — not “MCP being slow.”

**Cursor / Antigravity:** Same protocol behavior; only UI visibility of the discovery calls
differs. See `integrations/cursor-ide/README.md` and `integrations/antigravity-ide/README.md`.

---

## How to Use It

### Install

```powershell
pip install "fastmcp[code-mode]"
# or with uv:
uv add "fastmcp[code-mode]"
```

### Basic usage — drop-in, zero tool changes

```python
from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import CodeMode

mcp = FastMCP("Server", transforms=[CodeMode()])

@mcp.tool
def add(x: int, y: int) -> int:
    """Add two numbers."""
    return x + y

@mcp.tool
def multiply(x: int, y: int) -> int:
    """Multiply two numbers."""
    return x * y
```

Your existing tool functions don't change. Clients connecting to this server no longer see
`add` and `multiply` directly — instead they see the CodeMode meta-tools for discovering
and executing code.

---

## Discovery Tools

CodeMode ships four built-in discovery tools. By default only **Search** and **GetSchemas**
are enabled — the 3-stage flow.

| Tool | Default | What it does |
|------|---------|-------------|
| `Search` | Enabled | BM25 natural-language query over tool names + descriptions |
| `GetSchemas` | Enabled | Fetch full parameter schemas for named tools |
| `GetTags` | Disabled | Browse tools by tag category |
| `ListTools` | Disabled | Dump full catalog at configurable verbosity |

### Detail levels (shared by all discovery tools)

| Level | Output |
|-------|--------|
| `brief` | Names + descriptions only — minimal tokens |
| `detailed` | Includes parameter schemas |
| `full` | Complete JSON Schema |

`Search` defaults to `brief`. `GetSchemas` defaults to `detailed`. The LLM can override
the detail level per call.

---

## Discovery Flows

### Default (3-stage) — best for large or complex servers

```
1. Search("natural language query") → list of candidate tools (brief)
2. GetSchemas(["tool_a", "tool_b"]) → parameter schemas (detailed)
3. Execute Python code using those tools in sandbox
```

Staged discovery minimises context: the LLM only pays for schemas it actually needs.

### 2-stage — for medium servers

Search returns schemas inline, skipping the separate GetSchemas step.

```python
from fastmcp.experimental.transforms.code_mode import CodeMode, Search

code_mode = CodeMode(
    discovery_tools=[Search(default_detail="detailed")],
)
```

### 4-stage — for complex tagged servers

```python
from fastmcp.experimental.transforms.code_mode import (
    CodeMode, GetTags, Search, GetSchemas
)

code_mode = CodeMode(
    discovery_tools=[GetTags(), Search(), GetSchemas()],
)
mcp = FastMCP("Server", transforms=[code_mode])
```

The LLM browses by tag, narrows to a category, searches within it, then inspects schemas.

### No discovery — for tiny servers

```python
from fastmcp.experimental.transforms.code_mode import CodeMode, ListTools

code_mode = CodeMode(discovery_tools=[ListTools()])
```

`ListTools` at `brief` is still far fewer tokens than a standard `tools/list` response
(which includes full JSON Schema for every tool).

---

## Sandbox Configuration

CodeMode uses Pydantic's **Monty** sandbox for secure Python execution.

```python
from fastmcp.experimental.transforms.code_mode import CodeMode, MontySandboxProvider

code_mode = CodeMode(
    sandbox=MontySandboxProvider(
        timeout=10,           # seconds
        memory_limit_mb=256,
        max_recursion_depth=50,
    )
)
```

The sandbox provider is replaceable — implement the `SandboxProvider` protocol to use
Docker, a remote execution service, or any other environment.

---

## Composability

CodeMode is a standard Transform in the FastMCP 3.0 architecture. It composes freely
with providers and other transforms.

### Apply to an entire server

```python
mcp = FastMCP("Server", transforms=[CodeMode()])
```

### Apply to just one provider

```python
mcp = FastMCP("Server")
mcp.add_provider(my_large_provider, transforms=[CodeMode()])
# other tools registered with @mcp.tool remain directly accessible
```

### Proxy a remote server + CodeMode

```python
from fastmcp import FastMCP
from fastmcp.server.providers import MCPClientProvider
from fastmcp.experimental.transforms.code_mode import CodeMode

mcp = FastMCP("Proxy")
mcp.add_provider(
    MCPClientProvider("https://some-remote-mcp-server/sse"),
    transforms=[CodeMode()],
)
```

### Chain with other transforms

```python
from fastmcp.server.transforms import PrefixTransform

mcp.add_provider(
    some_provider,
    transforms=[PrefixTransform("remote_"), CodeMode()],
)
```

---

## Custom search result serialization

```python
def my_serializer(results: list[dict]) -> str:
    return "\n".join(f"- {r['name']}: {r['description']}" for r in results)

code_mode = CodeMode(search_result_serializer=my_serializer)
```

---

## Relevance for Our Fleet

Our fleet uses two patterns for managing tool count:

**Pattern A — Portmanteau** (most of our servers): consolidate 30–43 operations into a
single tool with an `operation` string parameter. One tool schema in the catalog, all
operations documented in the docstring. Zero context overhead. No `tool_search` needed.

**Pattern B — CodeMode** (some of our portmanteau meta-servers): the portmanteau tool
itself IS a `tool_search` variant — clients call it to discover and load actual tool
schemas on demand. `fileops`, `memops`, `winops`, `gitops` use this pattern.

The two patterns are complementary, not competing. A large fleet of portmanteau servers
can further wrap itself in a CodeMode meta-server if needed.

### When each pattern is right

| Scenario | Pattern |
|----------|---------|
| New server, related operations | Portmanteau (`operation` param) |
| New server, diverse unrelated tools | CodeMode |
| Wrapping external/third-party server | CodeMode via MCPClientProvider proxy |
| OpenAPIProvider with many endpoints | CodeMode |
| Existing portmanteau server | No change needed |
| Large fleet, context still bloated | CodeMode meta-wrapper over fleet |

---

## Token Cost Comparison (illustrative)

| Approach | Tokens at session start | Per-task overhead |
|----------|------------------------|-------------------|
| Standard MCP, 43 tools | ~8,000–15,000 | 0 |
| Portmanteau, 1 tool | ~300–500 | 0 |
| CodeMode, default | ~200 | 1 `tool_search` call (~100 tokens) |
| CodeMode + portmanteau | ~200 | 1 `tool_search` call (~100 tokens) |

For a fleet with 20+ MCP servers, the difference between standard and portmanteau/CodeMode
at session start can be 100,000+ tokens vs ~5,000.

---

## References

- FastMCP CodeMode docs: https://gofastmcp.com/servers/transforms/code-mode
- Jlowin 3.1 announcement: https://www.jlowin.dev/blog/fastmcp-3-1-code-mode
- FastMCP 3.0 architecture: https://www.jlowin.dev/blog/fastmcp-3
- Claude Desktop client behaviour: `integrations/claude-desktop/README.md` ← see there
- 3.0 → 3.1 improvements: `fastmcp/3.0-to-3.1-improvements.md`
- Portmanteau pattern: `patterns/portmanteau.md`
