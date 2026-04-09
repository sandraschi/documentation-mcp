# MCPB Format Status & Limitations

**Last Updated**: November 2025  
**MCPB Version**: 1.1.1  
**Status**: Claude Desktop Only - Limited Adoption  
**Applicable To**: All MCP Servers

---

## Why MCPB Failed to Gain Widespread Adoption

### 1. **Claude Desktop Exclusivity**

MCPB (Model Context Protocol Bundle) was designed specifically for Claude Desktop's extension system. While Anthropic intended it to become a universal standard, it never gained traction outside Claude Desktop:

- **No other major MCP clients adopted it**: Cursor IDE, Windsurf, Zed, and other MCP-compatible tools use standard JSON-RPC configuration
- **Vendor lock-in**: The format is tightly coupled to Claude Desktop's UI and extension system
- **Limited ecosystem**: Without broad client support, MCPB remains a niche format

### 2. **Weird Installation UX**

The "drag-and-drop into Claude Desktop settings UI" approach is unconventional:

- **Not intuitive**: Users expect traditional installers or package managers
- **No version management**: Difficult to update or uninstall cleanly
- **Manual process**: Requires users to navigate to settings, find the extensions panel, and drag files
- **No dependency resolution**: Users must manually ensure prerequisites are met

### 3. **Lack of Standard Tooling**

Unlike established formats (npm, pip, cargo), MCPB lacks:

- **Package registry**: No central repository for discovery
- **Version management**: No semantic versioning enforcement
- **Dependency resolution**: No automatic dependency handling
- **Update mechanisms**: No built-in update system
- **Uninstall process**: Removal requires manual cleanup

### 4. **Competing Standards**

The MCP ecosystem already has better alternatives:

- **Standard MCP config**: Works across all clients (Cursor, Windsurf, Zed, Claude Desktop)
- **NPX**: Universal Node.js package execution
- **Local installation**: Direct git clone + pip install (most flexible)

### 5. **Maintenance Overhead**

For developers, MCPB adds complexity:

- **Extra build step**: Requires MCPB CLI and build process
- **Manifest complexity**: Separate manifest.json with strict format requirements
- **Testing overhead**: Must test both standard MCP and MCPB packaging
- **Documentation burden**: Need to document MCPB-specific quirks

---

## What MCPB Does Well: Prompt Templates

The **one genuinely useful feature** of MCPB is its prompt template system:

### How It Works

MCPB packages can include prompt templates that Claude Desktop automatically loads:

```json
{
  "prompts": [
    {
      "name": "system",
      "description": "System prompt defining capabilities",
      "text": "prompts/system.md"
    },
    {
      "name": "user",
      "description": "User guide and examples",
      "text": "prompts/user.md"
    },
    {
      "name": "examples",
      "description": "Example interactions",
      "text": "prompts/examples.json"
    }
  ]
}
```

### Why Prompts Are Useful

1. **System context**: Provides Claude with detailed information about your MCP server's capabilities
2. **User guidance**: Helps users understand how to interact with your tools
3. **Example interactions**: Shows Claude expected usage patterns
4. **Consistent behavior**: Ensures Claude understands your server's purpose and limitations

### Typical Prompt Template Structure

Most MCP servers include:

- **`prompts/system.md`**: Architecture, tools, capabilities, constraints
- **`prompts/user.md`**: User guide with examples and common use cases
- **`prompts/examples.json`**: Example interactions demonstrating tool usage

---

## Replicating Prompt Templates with Other Install Methods

**Important distinction**: While docstrings can replicate *some* prompt template functionality, prompt templates provide **structured usage scenarios** that are genuinely useful for helping Claude understand how to use your tools effectively.

### What Prompt Templates Provide That Docstrings Don't

1. **Structured Usage Scenarios**: `prompts/user.md` provides complete usage patterns, not just parameter examples
2. **Example Interactions**: `prompts/examples.json` shows real conversation flows with expected responses
3. **System Context**: `prompts/system.md` provides architectural context and constraints that help Claude understand *why* tools work the way they do
4. **Cross-Tool Relationships**: Prompt templates can explain how tools work together, not just individual tool behavior

### Option 1: Include in Documentation (Partial Replication)

The prompt templates can be included in your repository at `prompts/`. Users can:

1. Read `prompts/system.md` to understand capabilities and architecture
2. Reference `prompts/user.md` for complete usage scenarios
3. Use `prompts/examples.json` as a reference for interaction patterns

**Location**: `prompts/` directory in repository root

**Limitation**: Claude won't automatically load these - they're just documentation.

### Option 2: Manual Claude Desktop Configuration

For Claude Desktop users using standard MCP config (not MCPB), you can manually reference prompts:

```json
{
  "mcpServers": {
    "your-mcp-server": {
      "command": "python",
      "args": ["-m", "your_mcp_server"],
      "env": {
        "PYTHONPATH": "${PWD}/src"
      },
      "prompts": {
        "system": "file:///path/to/prompts/system.md",
        "user": "file:///path/to/prompts/user.md"
      }
    }
  }
}
```

**Note**: Claude Desktop's support for prompts in standard MCP config is limited compared to MCPB, but this is better than nothing.

### Option 3: Embed in Tool Docstrings (Partial Replication)

Include key prompt content in tool docstrings. FastMCP automatically exposes these to all MCP clients:

```python
@mcp.tool()
async def your_tool(
    param1: str,
    param2: int = 100
) -> Dict[str, Any]:
    """
    Tool description with detailed examples.
    
    This tool provides functionality by doing X, Y, and Z.
    
    Examples:
        - Basic usage: param1="value1", param2=50
        - Advanced usage: param1="value2", param2=200
    
    Architecture:
        Uses underlying service/API for core functionality.
        Requires service to be running (check with status tool).
    """
```

**Advantage**: Works with ALL MCP clients, not just Claude Desktop.  
**Limitation**: Docstrings provide parameter-level examples, not complete usage scenarios or interaction patterns.

### Option 4: Hybrid Approach (Best Practice)

**For maximum compatibility**:

1. **Rich docstrings**: Include detailed examples and architecture info in tool docstrings (works everywhere)
2. **Prompt templates**: Keep `prompts/` directory for MCPB users and as documentation reference
3. **Manual configuration**: Document how to reference prompt templates in standard MCP config
4. **Examples in README**: Include usage scenarios in project documentation

This way:
- âœ… MCPB users get full prompt template benefits
- âœ… Standard MCP users can reference prompts manually
- âœ… All users benefit from rich docstrings
- âœ… Documentation provides usage scenarios for reference

---

## Recommendation

### Keep MCPB For:
- âœ… Claude Desktop users who want one-click installation
- âœ… Users who specifically request MCPB format
- âœ… Maintaining prompt template structure (useful reference)

### Prefer Other Methods For:
- â­ **NPX Installation** - Universal, works with all MCP clients
- â­ **Local Installation** - Most flexible, best for development
- â­ **Standard MCP Config** - Works everywhere, no vendor lock-in

### Best Practice:
1. **Primary**: Document NPX and local installation methods prominently
2. **Secondary**: Keep MCPB as optional convenience for Claude Desktop users
3. **Prompts**: Use prompt templates as documentation reference for all users
4. **Tool Docs**: Embed key prompt content in tool docstrings (universal compatibility)

---

## Current Status

- **MCPB Version**: 1.1.1 (latest)
- **Client Support**: Claude Desktop only
- **Maintenance**: Low priority (kept for Claude Desktop users)
- **Recommendation**: Use NPX or local installation for broader compatibility

---

## Bottom Line

- **MCPB format**: Failed standard attempt - Claude Desktop only, limited adoption
- **Prompt templates**: Genuinely useful for providing structured usage scenarios and example interactions
- **Replication**: Docstrings can replicate *some* functionality (parameter examples, basic usage), but prompt templates provide better structured scenarios and interaction patterns
- **Recommendation**: Keep prompt templates as they provide value beyond what docstrings can offer, especially for usage scenarios and example interactions. MCPB remains optional, but the prompt templates themselves are worth maintaining.

---

## Related Documentation

- [MCPB Packaging Standards](MCPB_PACKAGING_STANDARDS.md) - How to build MCPB packages
- [FastMCP 3.1.1++ Migration Guide](FASTMCP_3.1.1+_MIGRATION.md) - FastMCP compliance
- [MCP Server Standards](STANDARDS.md) - General MCP server development standards

---

**This document applies to all MCP servers in the ecosystem.**  
**Consider this when deciding whether to support MCPB packaging.**


