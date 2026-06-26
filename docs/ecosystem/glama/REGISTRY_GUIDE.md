# Glama - MCP Server Registry Guide

**Last Updated:** 2025-11-25  
**Status:** Active  
**URL:** https://glama.ai/mcp/servers

---

## What is Glama?

**Glama** is the primary **MCP server registry and discovery platform**. It allows:
- Browsing available MCP servers
- Discovering new tools for Claude
- Publishing your own MCP servers
- Community ratings and reviews

---

## Finding MCP Servers

### Web Interface
1. Visit https://glama.ai/mcp/servers
2. Browse by category or search
3. View server details, tools, and installation instructions

### Categories
- **Developer Tools** - Code, git, databases
- **Productivity** - Files, notes, automation
- **Media** - Images, video, audio
- **Smart Home** - IoT, cameras, devices
- **Communication** - Email, messaging

---

## Installing from Glama

### Method 1: Claude Desktop Config
Most servers provide a JSON snippet for `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "uvx",
      "args": ["package-name"]
    }
  }
}
```

### Method 2: MCPB Package
Some servers offer `.mcpb` packages:
1. Download the `.mcpb` file
2. Open Claude Desktop
3. Drag and drop the package

---

## Publishing to Glama

### Prerequisites
1. Working MCP server (FastMCP 3.1.1++ recommended)
2. Published to PyPI (for Python servers)
3. README with installation instructions
4. Tool documentation

### Submission Process
1. Go to https://glama.ai/mcp/submit
2. Provide:
   - Package name (PyPI)
   - GitHub repository URL
   - Description
   - Category
3. Wait for review (usually 1-3 days)

### Best Practices for Acceptance
- **Clear README** with installation steps
- **Comprehensive tool docstrings** (50+ lines)
- **Working examples**
- **No hardcoded secrets**
- **Proper error handling**

---

## Glama vs Other Registries

| Registry | Focus | Status |
|----------|-------|--------|
| **Glama** | Primary MCP registry | âœ… Active |
| **Smithery** | Alternative registry | âœ… Active |
| **MCP Hub** | Community collection | âš ï¸ Limited |

---

## Glama Integration Tips

### SEO for Discovery
- Use descriptive package names
- Include keywords in description
- List all tool names clearly

### Ratings & Reviews
- Respond to user feedback
- Keep server updated
- Fix reported issues promptly

### Version Updates
- Glama auto-pulls from PyPI
- Major updates may need re-review
- Announce breaking changes in README

---

## Troubleshooting

### Server Not Appearing
- Verify PyPI package is public
- Check submission status
- Ensure README has installation instructions

### Installation Issues
- Test with fresh Claude Desktop install
- Verify `uvx` or `npx` command works standalone
- Check for dependency conflicts

---

## Resources

- **Glama Website:** https://glama.ai
- **MCP Servers List:** https://glama.ai/mcp/servers
- **Submit Server:** https://glama.ai/mcp/submit
- **FastMCP Docs:** See `../fastmcp/`
- **MCPB Packaging:** See `../mcpb/`


