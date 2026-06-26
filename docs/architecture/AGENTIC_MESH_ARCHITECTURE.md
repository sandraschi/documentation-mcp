---
title: "MCP Agentic Mesh - Sampling Bridges and Inter-Server Orchestration"
category: architecture
status: active
audience: mcp-dev
skill_candidate: true
related:
  - architecture/AGENTIC_MESH_SECURITY.md
  - architecture/AGENTIC_MESH_robofang_INTEGRATION.md
  - fastmcp/sep-1577-sampling-with-tools.md
last_updated: 2026-02-23
---

# MCP Agentic Mesh â€” Sampling Bridges & Inter-Server Orchestration

**Status:** Design Reference  
**Date:** 2026-02-23  
**Owner:** Sandra Schi  
**Relates to:** [SEP-1577 Sampling with Tools](../fastmcp/sep-1577-sampling-with-tools.md), [robofang PRD](../../robofang/PRD.md)

---

## Concept

Each MCP server exposes tools. FastMCP 3.1.1+.1+ allows any tool to call `ctx.sample(tools=[...])` â€” the client LLM orchestrates using those tools. If the tools in that list are **bridge functions that call other MCP servers**, you get a mesh: servers delegating to servers, autonomously, with structured validated results at every hop.

This is not just convenient. It is a qualitative shift â€” from a set of isolated tools to a **multi-agent system** with no separate orchestration framework required.

---

## Architecture Layers

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  CLIENT (Claude Desktop / Cursor / robofang)                    â”‚
â”‚  Calls one meta-tool.  Receives one structured result.          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â”‚ ctx.sample(tools=[bridge_A, bridge_B, ...])
                            â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  ORCHESTRATOR SERVER  (e.g. advanced-memory-mcp / robofang)     â”‚
â”‚                                                                 â”‚
â”‚  agentic_content_workflow()                                     â”‚
â”‚    â”œâ”€â”€ search_knowledge_base()      â† local leaf tool           â”‚
â”‚    â”œâ”€â”€ bridge_filesystem()          â† calls filesystem-mcp      â”‚
â”‚    â”œâ”€â”€ bridge_local_llm()           â† calls local-llm-mcp       â”‚
â”‚    â””â”€â”€ bridge_camera()             â† calls devices-mcp      â”‚
â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
       â”‚                â”‚                â”‚
       â–¼                â–¼                â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚filesystem  â”‚  â”‚local-llm-mcp â”‚  â”‚devices-mcp   â”‚
â”‚-mcp        â”‚  â”‚              â”‚  â”‚                  â”‚
â”‚read_file   â”‚  â”‚infer()       â”‚  â”‚get_latest_clip() â”‚
â”‚write_file  â”‚  â”‚embed()       â”‚  â”‚trigger_recording â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Bridge Function Pattern

A bridge function is a plain Python async function that calls another MCP server's HTTP/stdio API and returns a string. It has a docstring â€” FastMCP generates a schema from it. It is passed as a callable to `ctx.sample(tools=[...])`.

```python
async def bridge_read_file(path: str) -> str:
    """
    Read a file from the local filesystem via filesystem-mcp.
    path: Absolute Windows path, e.g. D:/dev/repos/myproject/README.md
    Returns the file content as text, or an error string.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:10820/tools/read_file",
            json={"path": path},
            timeout=10.0,
        )
        return resp.json().get("content", f"ERROR: {resp.status_code}")
```

---

## Trust Model

| Tier | Servers | Can call |
|---|---|---|
| 0 â€” Read-only | advanced-memory-mcp (read) | Nothing physical |
| 1 â€” Local data | filesystem-mcp, advanced-memory-mcp (write) | Tier 0 only |
| 2 â€” Inference | local-llm-mcp | Tier 0-1 |
| 3 â€” Device control | devices-mcp | Tier 0-2, NOT Tier 4 |
| 4 â€” Physical actuation | robotics-mcp | ISOLATED â€” human gate required |

---

## Real Use Cases (Sandra's fleet)

**Camera event â†’ knowledge log:** motion detected â†’ classify scene â†’ log event with tags â†’ archive clip

**Research â†’ skill synthesis:** arxiv + github â†’ check existing notes â†’ synthesise draft â†’ save skill

**Robotics (with mandatory human confirmation gate):** sense â†’ plan â†’ HUMAN CONFIRM â†’ actuate â†’ log

---

See: [AGENTIC_MESH_robofang_INTEGRATION.md](AGENTIC_MESH_robofang_INTEGRATION.md)  
See: [AGENTIC_MESH_SECURITY.md](AGENTIC_MESH_SECURITY.md)

