# FastMCP Agentic Sampling: Autonomous Workflows

**Last Updated:** 2026-04-21
**Standard:** FastMCP 3.4.2 (originally written for 3.2.0 — `ctx.sample()` API unchanged)

Agentic Sampling (SEP-1577) allows an MCP server to **borrow the client's LLM** to orchestrate multi-step workflows. This transforms the server from a passive "endpoint" into an active "agent" capable of reasoning and chaining tools autonomously.

---

## 1. The Core Primitive: `ctx.sample()`

Inside any tool function, you can invoke `ctx.sample()` to request a completion from the client's model.

### Key Capabilities
- **Tool Chaining**: Pass a list of sub-tools the LLM can call during the sample.
- **Context Access**: The LLM sees the current session history and any specific messages you provide.
- **Structured Validation**: Use `result_type` to force the LLM to return a validated Pydantic model.

---

## 2. Implementation Pattern

### The "Autonomous Researcher"
```python
from fastmcp import Context
from pydantic import BaseModel

class Decision(BaseModel):
    action: str
    rationale: str

@mcp.tool()
async def smart_archive(ctx: Context, project_id: str):
    """Reason about and archive a project.
    
    Uses sampling to decide if the project is 'stale' before archiving.
    """
    # 1. Borrow the LLM
    result = await ctx.sample(
        messages=[{"role": "user", "content": f"Investigate project {project_id}"}],
        tools=[get_project_logs, search_git_history],
        result_type=Decision
    )
    
    # 2. Act on the decision
    decision: Decision = result.result
    if decision.action == "archive":
        await do_archive(project_id)
        
    return f"Resolution: {decision.rationale}"
```

---

## 3. Streaming Sampling (`ctx.sample_stream()`)

FastMCP 3.2 introduces streaming support for long-form reasoning. Use this when the agent is generating significant text or logic steps.

```python
async for chunk in ctx.sample_stream(messages=...):
    await ctx.report_progress(chunk.content)
```

---

## 4. Sampling Strategy: Meta-tools vs. Leaf Tools

To maintain high ME scores on platforms like **Arcade** and **Glama**, follow the prefix convention:

| Type | Prefix | Description |
|---|---|---|
| **Meta-Tool** | `agentic_` | Uses `ctx.sample()` to coordinate other tools. |
| **Workflow** | `workflow_` | Pre-defined sequence with LLM-gated decision points. |
| **Leaf Tool** | (None) | Simple, atomic operation. Never calls `ctx.sample()`. |

---

## 5. Security & Safety

- **Sample Budgeting**: Clients (Cursor/Claude) may impose limits on the number of samples a server can request.
- **Tool Constraints**: Only pass "Safe-to-Execute" tools to the sampling call. Avoid passing high-privilege `delete_*` tools unless the user has explicitly authorized the agentic workflow.

---

## References
- [tool-documentation.md](./tool-documentation.md)
- [codemode-discovery.md](./codemode-discovery.md)
- [fastmcp-32-fleet-capability-map.md](./fastmcp-32-fleet-capability-map.md)
