# OneNote MCP Server Alternatives

## Problem with microsoft-365-mcp

- **Too many tools**: Exceeds Cursor's 50-tool limit
- **Gaps**: Cannot read OneNote note text in MCP-client-understandable format
- **Complexity**: Overwhelming for focused OneNote use cases

## Recommended Alternatives

### 1. **danosb/onenote-mcp** â­ (Best Open Source Option)

**GitHub**: https://github.com/danosb/onenote-mcp

**Features**:
- âœ… **Reads complete note content** in readable format
- âœ… **Focused toolset** (likely < 10 tools)
- âœ… Open source and self-hostable
- âœ… Supports accessing notebooks, sections, and pages
- âœ… Create new pages
- âœ… Search notes
- âœ… Compatible with Cursor and Claude Desktop

**Setup**: Straightforward Python-based MCP server

**Why it's better**:
- Purpose-built for OneNote (not trying to cover all Microsoft 365)
- Likely uses portmanteau pattern to keep tool count low
- Specifically addresses reading note content

### 2. **Activepieces Microsoft OneNote MCP** (Hosted)

**URL**: https://www.activepieces.com/mcp/microsoft-onenote

**Features**:
- âœ… Free hosted solution
- âœ… Create notebooks, sections, notes, and pages
- âœ… Manage images within notes
- âœ… Integrates with Claude Desktop, Cursor, Windsurf

**Considerations**:
- Hosted (not self-hosted)
- May have tool count issues if not well-designed
- Requires Activepieces account

### 3. **CData OneNote MCP Server** (Enterprise)

**URL**: https://www.cdata.com/drivers/onenote/mcp/

**Features**:
- âœ… Enterprise-grade performance
- âœ… Real-time connections
- âœ… Secure data controls
- âœ… Natural language querying

**Considerations**:
- Commercial solution (may require license)
- Enterprise-focused (may be overkill for personal use)

### 4. **viaSocket Microsoft OneNote MCP** (Hosted)

**URL**: https://www.viasocket.com/mcp/onenote

**Features**:
- âœ… Create notes and image notes
- âœ… Append content to existing notes
- âœ… Simplified integration

**Considerations**:
- Hosted solution
- Limited feature set

## Build Your Own (Recommended for Control)

### Why Build?

1. **Full control** over tool count (use portmanteau pattern)
2. **Focused functionality** - only what you need
3. **Proper note reading** - format content for MCP clients
4. **FastMCP 3.1.1++** - modern framework with persistent storage

### Recommended Architecture

```python
# Portmanteau tool pattern (keeps tool count low)
@mcp.tool()
async def onenote(
    operation: str,  # "read", "create", "search", "list", "update", "delete"
    notebook: str | None = None,
    section: str | None = None,
    page: str | None = None,
    content: str | None = None,
    # ... operation-specific params
) -> dict[str, Any]:
    """OneNote operations portmanteau tool.
    
    Operations:
    - read: Read note content in MCP-friendly format (markdown/text)
    - create: Create new page/note
    - search: Search across notebooks
    - list: List notebooks/sections/pages
    - update: Update existing note
    - delete: Delete note/page
    """
```

### Key Requirements

1. **Read Note Content Properly**:
   - Convert OneNote HTML/XML to clean markdown
   - Extract text in readable format
   - Handle images, tables, formatting
   - Return structured content MCP clients can understand

2. **Keep Tool Count Low**:
   - Use portmanteau pattern (1 tool with `operation` parameter)
   - Target: < 10 tools total
   - Follow FastMCP 3.1.1++ best practices

3. **Microsoft Graph API**:
   - Use `msal` for authentication
   - Use `httpx` for API calls
   - Handle OneNote-specific endpoints

### Implementation Guide

1. **Use FastMCP 3.1.1++**:
   ```python
   from fastmcp import FastMCP
   from key_value.aio.stores.disk import DiskStore
   
   mcp = FastMCP("OneNote MCP", storage=DiskStore())
   ```

2. **Microsoft Graph API Client**:
   ```python
   # Use msal for authentication
   # Use httpx for API calls
   # Endpoint: https://graph.microsoft.com/v1.0/me/onenote/...
   ```

3. **Content Formatting**:
   ```python
   # Convert OneNote HTML to markdown
   # Extract clean text
   # Handle images (base64 or URLs)
   # Return structured dict with content, metadata
   ```

## Quick Comparison

| Solution | Tool Count | Read Content | Self-Hosted | Cost |
|----------|------------|--------------|-------------|------|
| **danosb/onenote-mcp** | âœ… Low | âœ… Yes | âœ… Yes | Free |
| **Activepieces** | â“ Unknown | â“ Unknown | âŒ No | Free |
| **CData** | â“ Unknown | âœ… Yes | âŒ No | Paid |
| **viaSocket** | â“ Unknown | âŒ Limited | âŒ No | Free |
| **Build Your Own** | âœ… Full Control | âœ… Full Control | âœ… Yes | Free |

## Recommendation

1. **Try danosb/onenote-mcp first** - It's open source, focused, and addresses the reading issue
2. **If it doesn't meet needs, build your own** - Use FastMCP 3.1.1++ and portmanteau pattern
3. **Reference tailscale-mcp** - Good example of portmanteau pattern and FastMCP 3.1.1++

## Resources

- **FastMCP 3.1.1++ Guide**: `D:\Dev\repos\mcp-central-docs\docs\mcp-technical\FASTMCP_3.1.1+_FEATURES_GUIDE.md`
- **Portmanteau Pattern**: `D:\Dev\repos\mcp-central-docs\patterns\MCP_PORTMANTEAU_BEST_PRACTICES.md`
- **Microsoft Graph API**: https://learn.microsoft.com/en-us/graph/api/resources/onenote-api-overview
- **OneNote API Docs**: https://learn.microsoft.com/en-us/graph/api/resources/onenote

---

**Last Updated**: 2025-11-24


