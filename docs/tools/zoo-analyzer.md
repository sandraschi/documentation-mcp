# MCP Zoo Runt Analyzer ðŸ¦

**Location:** `mcp-studio/runt_api.py`  
**Dashboard:** http://localhost:8888  
**Version:** 2.2.1 (2025-11-29)

A standalone dashboard for analyzing MCP server quality across your repository collection.

## Quick Start

```powershell
cd D:\Dev\repos\mcp-studio
python runt_api.py
```

## Features

- **Real-time progress** with SSE streaming
- **Zoo classification**: ðŸ˜ Jumbo, ðŸ¦ Large, ðŸ¦Š Medium, ðŸ° Small, ðŸ¿ï¸ Chipmunk
- **Status ratings**: âœ… SOTA, âš ï¸ Improvable, ðŸ› Runt, ðŸ’€ Critical
- **Tool counting**: Portmanteau tools, operations, individual tools
- **Detail modal** (click any card):
  - 6-stat header: FastMCP, Portmanteaus, Operations, Individual, CI/CD, Zoo Class
  - Structure badges: âœ“/âœ— for src/, tests/, scripts/, tools/, portmanteau
  - Side-by-side Issues (ðŸš¨) and Recommendations (ðŸ’¡) panels
  - Collapsible README preview
  - Organized tool list: ðŸ“¦ Portmanteaus with ops, ðŸ”¹ Individual tools
  - Expandable docstrings per tool

## Zoo Classification

| Animal | Emoji | Tool Count | Examples |
|--------|-------|------------|----------|
| Jumbo | ðŸ˜ | 20+ or specialized | database, virtualization, video |
| Large | ðŸ¦ | 10-19 tools | |
| Medium | ðŸ¦Š | 5-9 tools | |
| Small | ðŸ° | 2-4 tools | |
| Chipmunk | ðŸ¿ï¸ | 0-1 tools | simple utilities |

## Status Classification

| Status | Emoji | Meaning |
|--------|-------|---------|
| SOTA | âœ… | State of the art, no issues |
| Improvable | âš ï¸ | Minor issues, functional |
| Minor Runt | ðŸ£ | 1-2 issues |
| Runt | ðŸ› | 3-4 issues |
| Critical | ðŸ’€ | 5+ issues |

## Analysis Criteria

### Runt Triggers (hard failures)
- FastMCP <= 3.1.1+.0 (runt - upgrade required)
- No `src/` AND no package directory
- No CI/CD (for repos with 10+ tools)
- ALL tools use non-FastMCP registration

### Improvable Triggers (warnings)
- FastMCP 3.1.1+-3.1.1+ (upgrade to 3.1.1++ required for SOTA)
- No `tests/` (for repos with 10+ tools)
- No `tools/` subdirectory (for repos with 20+ tools)
- Some non-FastMCP registration patterns

## Tool Classification

### Portmanteau Tools (ðŸ“¦)
Tools in `*_tool.py`, `*_tools.py`, or `portmanteau/` directories.
Consolidated tools exposing multiple operations via action parameters.

```python
@app.tool
async def blender_mesh(action: Literal["create", "delete", "modify"], ...):
    """Portmanteau tool with 3 operations."""
```

### Portmanteau Operations
Individual operations within a portmanteau, counted from `Literal[...]` types.
These are what Claude actually sees as capabilities.

### Individual Tools (ðŸ”¹)
Simple standalone tools like `help`, `status`, `health_check`.
Fine to keep separate - don't need portmanteau consolidation.

## Example Output

```
17:21:40 | [66/81] Scanning devices-mcp...
17:21:40 |   ðŸ˜ âš ï¸ v3.1.1+.0 15(134)+5 [!reg:41]
```

Format: `zoo status version portmanteau(ops)+individual [flags]`

- `15(134)+5` = 15 portmanteau tools with 134 operations, 5 individual tools
- `[!reg:41]` = 41 non-conforming registrations detected

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard HTML |
| `GET /api/runts/` | Full scan results |
| `GET /api/repo/{name}` | Detailed single repo |
| `GET /api/progress` | Current progress |
| `GET /api/progress/stream` | SSE stream |
| `GET /api/logs` | Scan logs |

## Typical Results

From scanning ~80 MCP repos:

| Category | Count | % |
|----------|-------|---|
| SOTA âœ… | 21 | 41% |
| Improvable âš ï¸ | 18 | 35% |
| Runts ðŸ› | 12 | 24% |

## Related Docs

- [PORTMANTEAU_CONCEPT.md](../../patterns/PORTMANTEAU_CONCEPT.md) - Why consolidate tools
- [MCP_PORTMANTEAU_BEST_PRACTICES.md](../../patterns/MCP_PORTMANTEAU_BEST_PRACTICES.md) - How to do it
- [WHAT_CLAUDE_SEES.md](../../patterns/WHAT_CLAUDE_SEES.md) - Tool visibility


