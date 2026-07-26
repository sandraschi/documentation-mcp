# [HISTORICAL] Portmanteau V2: Managed Namespaces

**Last Updated:** 2026-04-21  
**Status:** HISTORICAL — never adopted fleet-wide. Current SOTA is Industrial Portmanteau (see `TOOL_DESIGN_STANDARDS.md` §1).
**Standard:** FastMCP 3.2+
**Pattern:** Sub-server Composition (Managed Namespaces)

In the 2025 Antigravity fleet, we standardized on the **Portmanteau Tool** (the "God Tool")—a single function using an `operation` enum to dispatch logic. While clean in code, this pattern is suboptimal for the 2026 agentic ecosystem.

FastMCP 3.2 introduces **Portmanteau V2 (Managed Namespaces)**, which provides the organizational benefits of grouping while exposing high-fidelity metadata to clients and evaluators.

---

## 1. The Conflict: V1 vs. V2

| Feature | Portmanteau V1 (Legacy) | Managed Namespaces (V2) |
|---------|-------------------------|-------------------------|
| **Structure** | Single tool: `adn_audio(operation=...)` | Individual tools: `adn:dictate`, `adn:speak` |
| **LLM Visibility** | Opaque (requires dispatch reasoning) | **Transparent** (dedicated schema per tool) |
| **ME Score** | Low (harder to sample correctly) | **High** (direct tool mapping) |
| **Arcade/Toolbench** | ❌ Hated (confuses benchmarks) | ✅ Preferred (atomic schemas) |
| **Glama Assessment** | ⚠️ Limited (meta-depth is low) | ✅ Expert (rich per-tool metadata) |
| **Cursor UX** | Basic | **Premium** (namespaced autocomplete) |

---

## 2. Why V2 Wins in 2026

### A. Arcade & Toolbench Effectiveness (ME)
Third-party evaluators like `toolbench.arcade.dev` score tools based on the model's ability to select the correct function and provide valid parameters in a single turn. 
- **V1 Problem**: The model sees a single `adn_audio` tool. It must first "guess" or "find" the `operation` enum. If the enum has 10 values, the prompt for that single tool becomes massive and confusing.
- **V2 Solution**: Each operation is a distinct tool with its own **3-4-100 docstring**. The LLM ranks the atomic tools and picks exactly what it needs with zero ambiguity.

### B. Glama Assessment & Discovery
Glama and other MCP registries index servers by their tool surfaces. 
- **V1**: The server appears as a "Single Tool Utility."
- **V2**: The server appears as a "Comprehensive Suite." This significantly improves the **Glama Quality Score** and discoverability in public indices.

### C. Cursor & Windsurf UX
In Cursor, typing `mcp:adn:` immediately triggers a filtered autocomplete of the namespaced tools. In V1, you just get `adn_audio` and have to manually discover the `operation` parameter, which is a significant friction point for "Vibe Coding."

---

## 3. Implementation Pattern

Instead of one "God Tool," define specialized sub-servers and `mount` them into a central server using a namespace.

### Step 1: Define Sub-Servers
```python
# audio_subserver.py
audio_app = FastMCP("Audio")

@audio_app.tool()
async def dictate(ctx: Context, duration: int):
    """Record and transcribe audio.
    
    Starts a microphone session for the specified duration.
    """
    ...
```

### Step 2: Mount with Namespace
```python
# main.py
from fastmcp import FastMCP
from .audio_subserver import audio_app

mcp = FastMCP("ADN Hub")

# Mount becomes the "Portmanteau"
mcp.mount(audio_app, namespace="adn")
```

**Result for the Client:**
- `adn:dictate`
- `adn:speak`
- `adn:listen`

---

## 4. Advisability: When to Upgrade?

| Severity | Context | Recommendation |
|----------|---------|----------------|
| **P0** | Public-facing / Published servers | **Upgrade Immediately**. V1 tools fail most modern ME benchmarks. |
| **P1** | Complex internal tools (>5 ops) | **Upgrade**. The Cursor UX benefits alone save significant dev-time. |
| **P2** | Simple utilities (1-2 ops) | **Keep V1**. Don't over-engineer simple scripts. |

---

## References
- [fastmcp-31-fleet-capability-map.md](./fastmcp-31-fleet-capability-map.md)
- [tool-documentation.md](./tool-documentation.md)
- [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md)
