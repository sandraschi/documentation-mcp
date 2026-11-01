# Antigravity IDE MCP Server Configuration

**Last Updated:** 2025-12-11
**Status:** Configured for Sandra's repos
**Official Documentation:** [https://antigravity.google/docs/mcp](https://antigravity.google/docs/mcp)

**Note:** This is Google's official MCP integration documentation. The page is a JavaScript application that loads content dynamically. Based on page structure analysis, it includes sections for MCP overview, core features, connection setup, custom server configuration, and supported servers.

---

# 🚨 CRITICAL SAFETY WARNING

## Data Destruction Risk

**Antigravity IDE has caused complete data loss** by wiping user drives. **BACKUP ALL DATA** before using Antigravity IDE. This tool has proven capable of destroying user data through normal operations.

**Recommendation:** Do not use Antigravity IDE for any work involving important data until comprehensive safety audits are completed.

---

## Overview

Antigravity IDE provides **two complementary approaches** for MCP server integration:

### 1. MCP Store (Recommended for Supported Servers)
Antigravity includes a built-in **MCP Store** for easy installation of pre-configured servers. This is the primary method for most users.

### 2. Custom MCP Server Configuration
For custom or self-hosted MCP servers, configuration can be done through raw config editing.

**⚠️ Important:** Our reverse-engineered `settings.json` approach may be a fallback/alternative method, but the official documentation emphasizes the MCP Store and `mcp_config.json` for custom servers.

## Method 1: MCP Store (Official Recommended Approach)

### Accessing the MCP Store
1. Open the MCP Store panel within the **"..." dropdown** at the top of the editor's side panel
2. Browse the list of supported servers
3. Click **Install** for any server you want to use
4. Follow authentication prompts for services that require it

### Supported Servers (Official List)
The MCP Store includes integrations for:
- **Databases:** AlloyDB PostgreSQL, BigQuery, Cloud SQL (PostgreSQL/MySQL/SQL Server), Dataplex, MongoDB, Neon, Prisma, Redis, Spanner, Supabase
- **Development Tools:** Dart, Figma Dev Mode, GitHub, Heroku, Linear, Locofy, Netlify, SonarQube
- **Business Tools:** Airweave, Atlassian, Harness, Looker, Notion, PayPal, Perplexity Ask, Sequential Thinking, Stripe
- **AI/Data:** MCP Toolbox for Databases, Pinecone

### Features Provided
- **Context Resources:** Real-time data access (database schemas, build logs, etc.)
- **Custom Tools:** Safe execution of server-defined actions ("Create Linear issue", "Search Notion", etc.)

## Method 2: Custom MCP Server Configuration

### Via MCP Store Interface (⚠️ Well Hidden!)
1. Open the MCP Store via the **"..." dropdown** at the top of the editor's agent panel
2. Click **"Manage MCP Servers"** (buried in submenu!)
3. Click **"View raw config"** (even more hidden!)
4. Modify the `mcp_config.json` with your custom MCP server configuration

**UX Criticism:** This custom server integration method is extremely well-hidden. The official docs don't prominently feature it, requiring users to dig through multiple obscure menu options. Poor discoverability for power users who want to integrate their own MCP servers.

### Alternative: Settings.json Approach (Reverse-Engineered)
```
Location: C:\Users\[username]\AppData\Roaming\Antigravity\User\settings.json
```

Antigravity uses the `"mcpServers"` key in `settings.json` with the same structure as Claude Desktop:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "cwd": "working/directory",
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

## Current Configuration (Settings.json Approach)

**Note:** Our current setup uses the alternative `settings.json` approach, which appears to coexist with the official MCP Store. This may be a more flexible method for custom/advanced server configurations.

Antigravity IDE is configured with MCP servers using the `settings.json` approach. **Bright Data MCP** is configured for scraping websites with anti-bot protection that block regular web scraping attempts.

**✅ Fixed:** Advanced Memory MCP startup issue resolved - suppressed logging interference with MCP JSON-RPC protocol in stdio mode.

**✅ Optimized:** Removed unnecessary `cwd` field from Advanced Memory MCP configuration - the server uses absolute paths and doesn't depend on working directory.

**✅ Also configured in Cursor IDE** (`C:\Users\<user>\.cursor\mcp.json`) for cross-IDE availability.

### Local Development Servers
- **advanced-memory**: Zettelkasten knowledge management
- **calibre**: E-book library management
- **database-mcp**: SQLite database operations
- **filesystem-mcp**: File system operations
- **osc-mcp**: OSC protocol for music/production
- **devices-mcp**: Tapo camera control
- **unity3d-mcp**: Unity3D game engine integration
- **fastsearch-mcp**: Fast text search across files
- **virtualdj-mcp**: VirtualDJ integration
- **plex-mcp**: Plex media server control

### External Services
- **mcp-server-docker**: Docker container management
- **fetch**: Web fetching utilities
- **brightdata**: Anti-bot protected web scraping (Bright Data service) - handles recalcitrant pages with Cloudflare/DataDome protection
- **github-mcp-server**: GitHub operations

## Testing MCP Connections

1. **Launch Antigravity IDE**
2. **Open Command Palette** (`Ctrl+Shift+P`)
3. **Search for "MCP"** - you should see MCP-related commands
4. **Check MCP Server Status** - look for server connection indicators
5. **Test a server** - try using tools from configured servers

## Troubleshooting

### Server Won't Start
- Check `cwd` path exists and is accessible
- Verify `PYTHONPATH` and other environment variables
- Ensure required dependencies are installed
- Check server logs in Antigravity's log directory

### Permission Issues
- Some servers may require elevated permissions
- Check if paths use correct Windows format (forward slashes work)

### Environment Variables
- `PYTHONUNBUFFERED=1` prevents output buffering issues
- Custom environment variables are server-specific

## Adding New Servers

To add new MCP servers to Antigravity:

1. Add server configuration to `settings.json` under `"mcpServers"`
2. Use same format as Claude Desktop config
3. Restart Antigravity IDE
4. Test server connection

## Differences from Claude Desktop

- Configuration stored in VS Code-style `settings.json`
- No separate config file (unlike Claude's `claude_desktop_config.json`)
- Settings are user-specific, not application-specific
- Uses VS Code's settings sync if enabled

## Related Documentation

- [Antigravity IDE Overview](../README.md)
- [MCP Protocol](../../protocol/OVERVIEW.md)
- [FastMCP Framework](../../fastmcp/README.md)
