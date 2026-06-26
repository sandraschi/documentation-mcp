# FastMCP 3.2 Advanced Patterns

**Last Updated:** 2026-04-21
**Version:** 3.2.0 (April 2026 SOTA)
**Applies to:** FastMCP 3.x, standard fleet servers (`*-mcp`)

Advanced implementation patterns for building mission-critical, agentic MCP servers with FastMCP 3.2.

---

## 1. GenerativeUI & App Orchestration

FastMCP 3.2 and `prefab-ui` allow servers to push rich, interactive components into the host's conversation area.

### Pattern: The Dashboard App
Use `ToolResult` to return both a text summary (for RAG) and a rich UI (for the user).

```python
from mcp.types import ToolResult
from prefab_ui import PrefabApp, Card, Text, Button

@mcp.tool(app=True)
async def get_system_dashboard(ctx: Context) -> ToolResult:
    """Generate a rich system health dashboard.
    
    Provides real-time visualization of VRAM, CPU, and Task queue.
    """
    stats = await get_telemetry()
    
    app = PrefabApp(
        title="Fleet Dashboard",
        root=Card(
            content=[
                Text(f"VRAM Usage: {stats.vram_gb}GB"),
                Button(label="Clear Cache", action="clear_cache_tool")
            ]
        )
    )
    
    return ToolResult(
        content="Dashboard generated. VRAM at 80%.",
        structured_content=app
    )
```

---

## 2. CodeMode & Semantic Discovery

For servers with hundreds of tools, use **CodeMode** to hide raw tools and provide semantic discovery via meta-tools.

### Configuration
```python
from fastmcp.experimental.transforms import CodeModeTransform

mcp = FastMCP(
    "KnowledgeHub",
    transforms=[CodeModeTransform()]
)
```

### Pattern: The Searchable Catalog
CodeMode projects `search_tools` and `get_tool_schema` to the client. The agent calls these instead of receiving a massive "tool explosion" at session start. This saves 50%++ of initial context tokens.

---

## 3. Background Task Orchestration (`task=True`)

SEP-1686 allows tools to run persistently. In 3.2, you can orchestrate these tasks with status reporting.

### Pattern: The Long-Running Auditor
```python
@mcp.tool(task=True)
async def security_audit(ctx: Context, target_dir: str):
    """Run a deep security audit (Background).
    
    Performs static analysis and vulnerability scanning.
    """
    files = list_files(target_dir)
    for i, file in enumerate(files):
        # Report progress through the context
        await ctx.report_progress(current=i, total=len(files))
        await audit_file(file)
        
    return "Audit complete. No critical vulnerabilities found."
```

---

## 4. Multi-Protocol Authentication

FastMCP 3.2 supports complex auth flows, including PropelAuth and generic OAuth2.

### Pattern: Tiered Access
```python
from fastmcp.auth import OAuth2Provider, APIKeyProvider

mcp = FastMCP(
    "EnterpriseServer",
    auth=[
        OAuth2Provider(issuer="https://auth.acme.com"),
        APIKeyProvider(name="X-Internal-Key")
    ]
)
```

---

## 5. Agentic Sampling (SEP-1577)

Sampling remains a core power of FastMCP 3.2, allowing the server to "borrow" the client's LLM.

### Pattern: The Autonomous Researcher
```python
@mcp.tool()
async def smart_resolve(ctx: Context, incident_id: str):
    """Autonomously resolve an incident using client sampling."""
    
    # Let the LLM decide which sub-tools to call
    result = await ctx.sample(
        messages=[{"role": "user", "content": f"Fix incident {incident_id}"}],
        tools=["get_logs", "restart_service", "notify_channel"]
    )
    
    return result.content
```

---

## 6. Connectivity Probes

New in 3.2: define probes to verify server health and dependency availability during startup.

```python
@mcp.probe("database_connectivity")
async def check_db():
    return await db.ping()
```

---

## Summary Checklist
- [ ] **GenerativeUI**: Used for any list/status response.
- [ ] **CodeMode**: Used if the tool count > 15.
- [ ] **Background Tasks**: Used for any op > 30s.
- [ ] **Auth**: Multiple providers used where appropriate.
- [ ] **Sampling**: Used for multi-step reasoning.

---

## References
- [3.2-features.md](./3.2-features.md)
- [tool-documentation.md](./tool-documentation.md)
- [mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md)
