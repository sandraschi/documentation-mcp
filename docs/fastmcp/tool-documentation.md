# FastMCP 3.2 Tool Documentation Standards

**Last Updated:** 2026-04-21
**Version:** 3.4.2 (originally written for 3.2.0 — docstring standards unchanged)

This document defines the **SOTA 2026 standards** for FastMCP tool implementation. All fleet servers must adhere to these patterns to ensure high-fidelity RAG discovery, agentic orchestration, and rich UI presentation.

---

## 1. The Docstring Overhaul (V1 -> V3)

FastMCP 3.2 formalizes the transition from legacy structured docstrings to **Schema-First Documentation**.

| Generation | Style | Characteristic | Status |
|---|---|---|---|
| **V1 (Legacy)** | Opaque | No structured args; prose description only. | ❌ Forbidden |
| **V2 (Structured)** | Verbose | Google/Numpy `Args:` blocks in the docstring. | ⚠️ Deprecated |
| **V3 (SOTA 2026)** | **Precise** | **3-4-100** prose + **Vanishing Args** (Schema-first). | ✅ **Standard** |

### The "Death of the Args Block" Rule
In SOTA 2026, the `Args:` (or `Parameters:`) section in the docstring is **EXPLICITLY FORBIDDEN** for any tool with more than 3 parameters. 
- **Why**: Duplicating parameter documentation in the docstring burns LLM context tokens and creates "no description" or "redundant description" noise in Cursor/Windsurf.
- **Solution**: Move all descriptions into **Annotated/Field** schemas (see Section 4).

---

## 2. The 3-4-100 Docstring Rule

FastMCP 3.2 enforces the **3-4-100** rule to ensure tool docstrings are semantically dense but concise.

1.  **3-Word Name**: Action_Object_Context (e.g., `search_knowledge_base`).
2.  **4-Word Summary**: The first line of the docstring.
3.  **100-Char Description**: Focused on *intent* and *impact*.

---

## 3. Background Tasks (`task=True`)

SEP-1686 allows operations to exceed 30 seconds. Use `task=True` for sync/watcher tools.
- **Non-blocking**: Returns a Task ID immediately.
- **Progress**: Use `ctx.report_progress(...)`.

---

## 4. Parameter Standards (Vanishing Args)

Move detailed parameter documentation into **`Annotated`** fields. This keeps the docstring clean for discovery while providing high-fidelity schema hints.

### Correct Pattern
```python
from typing import Annotated
from pydantic import Field

@mcp.tool()
async def invoke_agent_action(
    operation: Annotated[str, Field(description="Action: deploy, test, audit")],
    target: Annotated[str, Field(description="Target host ID")]
):
    """Execute fleet agent commands.
    
    Orchestrates infrastructure changes across the authorized fleet.
    """
    ...
```

---

## 5. GenerativeUI (Prefab App) Responses

For list-based or status results, you **MUST** provide a Prefab App presentation using `ToolResult`.
- **Text Summary**: Required for RAG and accessibility.
- **Structured Content**: `PrefabApp` for rich visual rendering in the host.

---

## 6. Return Standards (The Success Rule)

All tools must return a structured dictionary or Markdown.
- **Success Boolean**: Required for task tracking.
- **Recommendations**: Optional but encouraged for agentic chaining.

---

## 7. Migration Checklist (FastMCP 2.x/3.1 -> 3.2)

- [x] **Docstring**: No `Args:` block (V3 Standard).
- [x] **Args**: Uses `Annotated[T, Field(description="...")]`.
- [x] **Async**: All tools are `async def`.
- [x] **Task**: Long-running ops use `task=True`.
- [x] **Prefab**: List results return `ToolResult`.

---

## References
- [codemode-discovery.md](./codemode-discovery.md)
- [agentic-sampling.md](./agentic-sampling.md)
- [generative-ui-prefabs.md](./generative-ui-prefabs.md)
