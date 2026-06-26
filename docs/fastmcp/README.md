# FastMCP 3.4: The Industrial SOTA Suite (2026)

**Fleet Baseline:** `fastmcp>=3.4.2,<4` (June 2026) — minimum **3.2.0** until fleet bump completes; target **3.4.2** for remote bridge, proxy hardening, and security floor.

**Latest release notes:** [3.4-features.md](3.4-features.md) (Remote Control, `fastmcp-remote`, returnable errors). Prior GA: [3.2-features.md](3.2-features.md).

This directory contains the authoritative documentation for the FastMCP stack used across the Antigravity fleet. All guides have been industrialized to reflect the **GA Standard**, moving beyond experimental 3.1 proposals.

---

## 1. Core Documentation Suite

| Topic | Guide | Key Standards |
|---|---|---|
| **Foundations** | **[tool-documentation.md](tool-documentation.md)** | 3-4-100, Vanishing Args (`Annotated`), Task=True. |
| **Persistence** | **[persistent-storage.md](persistent-storage.md)** | Async state, Probes, and DiskStore standards. |
| **Grouping** | **[portmanteau-v2-managed-namespaces.md](portmanteau-v2-managed-namespaces.md)** | Managed Namespaces (`mount`) for Arcade/Glama. |
| **Discovery** | **[codemode-discovery.md](codemode-discovery.md)** | Staged tool discovery for 50+ tool catalogs. |
| **Autonomy** | **[agentic-sampling.md](agentic-sampling.md)** | `ctx.sample()` and meta-tool orchestration (SEP-1577). |
| **Visualization** | **[generative-ui-prefabs.md](generative-ui-prefabs.md)** | Python DSL -> React cards and table Prefabs. |
| **Composition** | **[providers-and-transforms.md](providers-and-transforms.md)** | Sourcing from Filesystem, OpenAPI, and Proxy. |
| **Federation** | **[mcp-bridge-fleet-patterns.md](mcp-bridge-fleet-patterns.md)** | ProxyProvider fleet pairings, multi-hop, troubleshooting. |
| **Remote (3.4)** | **[3.4-features.md](3.4-features.md)** | `fastmcp-remote`, fail-loud proxies, `ToolResult(is_error=)`, OAuth idle tokens. |
| **Guidance** | **[skills-and-prompts.md](skills-and-prompts.md)** | Reusable system prompts and portable `skill://` packs. |

---

## 2. Decision Support

- **[fastmcp-32-fleet-capability-map.md](fastmcp-32-fleet-capability-map.md)**: **Authoritative Decision Matrix**. Use this to decide which 3.2 features your server requires (and which to avoid).
- **[migration-guide.md](migration-guide.md)**: Step-by-step path from 2.x through 3.2 to **3.4.2**.
- **[3.4-features.md](3.4-features.md)**: Remote bridge, proxy breaking change, returnable tool errors, 3.4.x patch notes.

---

## 3. High-Fidelity RAG Guidance

When using these docs for RAG or agentic synthesis, prioritize files based on the **3.2 SOTA Hierarchy**:
1.  **Fundamental Rules**: `tool-documentation.md` (3-4-100 rule is absolute).
2.  **Architectural Layout**: `portmanteau-v2-managed-namespaces.md`.
3.  **Specific Features**: Individual guide based on the capability ladder.

---

## 🚀 Quick Start

### 1. Install
```powershell
pip install "fastmcp>=3.4.2"
```

### 2. Create Server
```python
from fastmcp import FastMCP

# Initialize server
mcp = FastMCP("My Server")

# Add a tool (following 3-4-100 rule)
@mcp.tool()
async def greet_user(name: str) -> str:
    """Greet the user.
    
    Returns a personalized greeting in plain text.
    """
    return f"Hello, {name}!"

# Run it (Stdio default)
if __name__ == "__main__":
    mcp.run()
```

### 3. Test & Develop
```powershell
# Development loop with auto-reload
fastmcp dev server.py

# Inspect rich UI cards (GenerativeUI)
fastmcp dev apps server.py
```

---

## 🔧 Core Pillars of 3.2

### 1. Background Tasks (`task=True`)
Run long operations (migrations, watchers) without blocking the client.
```python
@mcp.tool(task=True)
async def start_reindex(ctx: Context):
    await do_heavy_work()
    return "Complete"
```

### 2. GenerativeUI (Prefab)
Return rich cards, tables, and buttons directly into the chat.
```python
from prefab_ui import PrefabApp, Card
return ToolResult(content="...", structured_content=PrefabApp(root=Card(...)))
```

### 3. Async State Persistence
Remember user context across server and OS restarts.
```python
await ctx.set_state("theme", "dark")
```

---

## 🎯 Pro-Tips for Fleet Maintainers

- **Use CodeMode**: If your server has >15 tools, enable CodeMode in the constructor to save tokens.
- **Portmanteau Transforms**: Use `mount(namespace="...")` to organize tools semantically.
- **Annotated Args**: Move parameter descriptions into `Annotated[T, Field(description="...")]` to keep docstrings lean.

---

## References
- [Official FastMCP Changelog](https://gofastmcp.com/changelog)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md)
