# FastMCP Providers & Transforms: Server Composition

**Last Updated:** 2026-04-21
**Standard:** FastMCP 3.4.2 (originally written for 3.2.0)

FastMCP 3.2 moves away from purely manual registration towards **Declarative Composition**. Using **Providers** (sources) and **Transforms** (middleware), you can assemble complex servers from multiple sources without duplicating code.

---

## 1. Providers: Standard Sourcing

Providers bring tools, resources, and prompts into a server from an external source.

| Provider | Usage |
|---|---|
| `FileSystemProvider` | Scans a directory for Python scripts and converts them into tools. |
| `ProxyProvider` | Mirrors another MCP server (SSE or stdio). Key for **Federation**. |
| `OpenAPIProvider` | Generates tools automatically from a Swagger/OpenAPI spec. |
| `SkillsProvider` | Exposes local skill directories as `skill://` resources. |

### Example: The Composite Hub
```python
from fastmcp import FastMCP
from fastmcp.providers import FileSystemProvider, ProxyProvider

mcp = FastMCP("FleetHub")

# 1. Source local scripts
mcp.add_provider(FileSystemProvider(root="./scripts"))

# 2. Proxy a remote server
mcp.add_provider(ProxyProvider(url="http://obs-mcp:10711/sse"))
```

---

## 2. Transforms: The Middleware Layer

Transforms modify or filter components after they are sourced but before they reach the client.

| Transform | Usage |
|---|---|
| `NamespaceTransform` | Prefix components: `list` -> `fs:list`. (Recommended for composite hubs). |
| `RenameTransform` | Map legacy names to a new standard. |
| `VisibilityTransform` | Hide specific tools based on auth or environment. |
| `ArgTransform` | Rename or hide tool parameters. |

---

## 3. Mounting: The Managed Portmanteau

In the 3.2 GA suite, we use `mount()` to combine sub-servers into a unified namespace. This is the **Portmanteau V2** standard.

```python
from .audio_service import audio_subapp # A separate FastMCP instance

# mount() handles registration and namespace prefixing in one call
mcp.mount(audio_subapp, namespace="adn")
```
*Creates: `adn:dictate`, `adn:speak`, `adn:listen`.*

---

## 4. Federated Discovery

By combining `ProxyProvider` with `NamespaceTransform`, you can build a **Central Intelligence Hub** that exposes tools from dozens of distributed micro-servers while maintaining a clean, hierarchical catalog.

```python
mcp.add_provider(
    ProxyProvider(url="..."),
    transforms=[NamespaceTransform(prefix="remote")]
)
```

---

## References
- [MCP Bridge Fleet Patterns](./mcp-bridge-fleet-patterns.md) — concrete fleet pairings with speech-mcp, memops, davinci, osc-mcp, and more
- [tool-documentation.md](./tool-documentation.md)
- [codemode-discovery.md](./codemode-discovery.md)
- [portmanteau-v2-managed-namespaces.md](./portmanteau-v2-managed-namespaces.md)
