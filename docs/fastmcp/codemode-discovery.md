# FastMCP CodeMode & Semantic Discovery

**Last Updated:** 2026-06-06  
**Standard:** FastMCP 3.4.2 (GA target); 3.2.0 minimum

CodeMode is the primary scaling pattern for servers with massive tool catalogs. It replaces the traditional "full catalog dump" with a **staged discovery** process that saves up to 90% of initial context tokens.

---

## 1. The Scaling Problem

Standard MCP loads the entire tool catalog (names, descriptions, full JSON Schemas) at session start. 
- **Small Servers (1-15 tools)**: ~1,000 tokens. (Manageable).
- **Industrial Servers (100+ tools)**: ~20,000+ tokens. (Context bloat).

**CodeMode** solves this by exposing only 2-3 **Meta-Tools** that the LLM uses to "find" and "learn" tools on demand.

---

## 2. Meta-Tool Architecture

When CodeMode is enabled, the host (Cursor/Claude) sees a simplified tool list:

| Tool | Purpose |
|---|---|
| `Search` | BM25 natural-language search over the tool catalog. |
| `GetSchemas` | Retrieve the specific JSON schemas for selected tools. |
| `Execute` | (Optional) Multi-step Python execution in the Monty sandbox. |

### The 3rd Turn Workflow
1. **Discover**: LLM calls `Search(query="process audio")` -> returns tool names + brief summaries.
2. **Retrieve**: LLM calls `GetSchemas(tools=["adn:dictate"])` -> returns the full parameter schema.
3. **Execute**: LLM calls the actual tool (or writes Python to call multiple tools).

---

## 3. Implementation

CodeMode is implemented as a **Transform** in FastMCP.

### Basic Setup
```python
from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import CodeMode

mcp = FastMCP("IndustrialServer")
mcp.add_transform(CodeMode())

# All tools registered below are hidden behind meta-discovery
@mcp.tool()
async def heavy_logic_a(...): ...
```

### Advanced: Scoped CodeMode
You can apply CodeMode to specific providers while keeping core tools globally visible.

```python
mcp.add_provider(
    OpenAPIProvider(spec="legacy_api.json"),
    transforms=[CodeMode()]
)
```

---

## 4. Discovery Thresholds

| Tool Count | Pattern | Rationale |
|---|---|---|
| **< 15** | Standard (`@mcp.tool`) | Low overhead, immediate availability. |
| **15 - 50** | Namespaces (`mount`) | Clean UI grouping, partial RAG discovery. |
| **> 50** | **CodeMode** | **Required**. Prevents session-start context crashes. |

---

## 5. Security: The Monty Sandbox

CodeMode uses the **Monty Sandbox** for Python execution. It is:
- **Stateless**: Each execution starts fresh.
- **Resource constrained (3.4+ defaults)**: `MontySandboxProvider()` without explicit limits uses **30s duration** and **100 MB memory**; CodeMode caps **50 tool calls** per `execute` block. Opt out with `limits=None` and `max_tool_calls=None` only when required.
- **Legacy docs note:** Pre-3.4 examples cited 256 MB / 10s — verify against your pinned version after upgrade.
- **Tool-gated**: Code can *only* call tools registered on the server.

See [3.4-features.md](3.4-features.md) §5 for fleet upgrade notes (blender-mcp and other CodeMode servers).

---

## References
- [3.4-features.md](./3.4-features.md)
- [tool-documentation.md](./tool-documentation.md)
- [providers-and-transforms.md](./providers-and-transforms.md)
- [fastmcp-32-fleet-capability-map.md](./fastmcp-32-fleet-capability-map.md)
