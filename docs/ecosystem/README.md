# MCP Ecosystem

**Last Updated:** 2026-06-06

The Model Context Protocol ecosystem - tools, platforms, and services that support MCP.

---

## 📚 In This Section

| Directory | Purpose |
|-----------|---------|
| **[claude-desktop/](claude-desktop/)** | Claude Desktop configuration and setup |
| **[cursor/](cursor/)** | Cursor IDE — [Jun 2026 digest](cursor/CHANGELOG_DIGEST_JUN_2026.md), [no local provider](cursor/NO_LOCAL_PROVIDER.md), Cloud Agents, [cursor-mcp](cursor/CURSOR_MCP_PROPOSAL.md) |
| **[zed/](zed/)** | Zed IDE — [May–Jun 2026 digest](zed/CHANGELOG_DIGEST_MAY_JUN_2026.md), FOSS, Ollama/LM Studio $0 path |
| **[IDE_LOCAL_INFERENCE.md](IDE_LOCAL_INFERENCE.md)** | Cross-IDE matrix: Cursor / Antigravity 2.0 / Zed / OpenCode — who has Ollama, DeepSeek, $0 |
| **[glama/](glama/)** | Glama MCP server registry |
| **[mcpb/](mcpb/)** | MCPB packaging standards |
| **[FREE_AI_CODING_RESOURCES.md](FREE_AI_CODING_RESOURCES.md)** | Free AI coding options: Bonsai, Antigravity, Xcode 26.3 (2026) |
| **[skills/](../skills/)** | Agent Skills - ecosystem, assessments, content notes |

---

## 🎯 Overview

The MCP ecosystem consists of clients, servers, tools, and registries. In 2026, the selection of an **Agentic IDE** is the most critical decision for a SOTA-compliant workflow.

### ⚠️ 2026 Agentic IDE Risk Registry

| IDE | Stability | Autonomy | Data Safety | Persona Alignment | Primary Risk |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Antigravity** | High | Extreme | Medium | High | Free tier gutted (2026); no Ollama; drive-nuking risk. |
| **Cursor 3.0** | High | High | High | Medium | Unicode Emoji Regression (breaks logic). |
| **Zed** | Exceptional | Emerging | Supreme | High | Hardware backend (Vulkan) stability. |
| **Xcode 26.3** | Medium | Extreme | High | Variable | "Vibecoding" terminology drift. |
| **Windsurf** | Low | Low | Low | Low | **LEGACY**: Acquired/Frozen ecosystem. |

---

## 🖥️ Active Agentic IDEs

- **[Antigravity](antigravity/)** - Google agent IDE; **deprioritized** post–I/O pricing ([matrix](IDE_LOCAL_INFERENCE.md)).
- **[Cursor](cursor/)** - The industry standard for task delegation.
- **[Zed](zed/)** - FOSS native editor; Ollama/LM Studio for $0 inference ([digest](zed/CHANGELOG_DIGEST_MAY_JUN_2026.md)).
- **[Xcode 26.3](../apple/)** - Apple's deeply integrated agentic build pipeline.
- **[Windsurf](windsurf/)** - **[ARCHIVAL]** Legacy orchestration patterns.

---

## 🏗️ Core Components

---

## 🖥️ Claude Desktop

Official Anthropic client for MCP servers.

### Configuration

Location: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["D:/path/to/server.py"]
    }
  }
}
```

→ Complete guide: [claude-desktop/](claude-desktop/)

---

## 🎛️ MCP Studio

**Mission Control for the MCP Zoo** - Management dashboard for MCP servers.

### Features
- **Working Sets**: Purpose-built server configurations for specific workflows
  - Media Consumption (Calibre, Plex, Immich)
  - Robotics & 3D Development (Robotics MCP, Unity3D, Blender, VRChat)
  - Development, Automation, Communication sets
- **Tool Enablement**: Individual tool activation/deactivation per client
- **Runt Analyzer**: Scan repos for SOTA compliance
- **Multi-Client Support**: Manage Claude Desktop, Cursor, Windsurf configs

### Working Sets
One-click switching between focused MCP server configurations:

```bash
# Activate Media Consumption set
# Includes: Calibre (ebooks) + Plex (streaming) + Immich (photos)

# Activate Robotics set  
# Includes: Robotics MCP + Avatar MCP + Unity3D MCP + OSC MCP + Blender MCP + VRChat MCP
```

→ **Repository:** [mcp-studio](https://github.com/sandraschi/mcp-studio)

---

## 🌐 Glama Registry

Community MCP server registry at https://glama.ai/mcp/servers

### Publishing to Glama

1. Build your MCP server
2. Create GitHub repository
3. Add proper README and documentation
4. Submit to Glama registry

→ Publishing guide: [glama/REGISTRY_GUIDE.md](glama/REGISTRY_GUIDE.md)

---

## 📦 MCPB Packaging

MCPB (Model Context Protocol Bundle) - Standard packaging format for MCP servers.

### Benefits

- ✅ Easy distribution
- ✅ Dependency management
- ✅ Version control
- ✅ Cross-platform support

→ Complete guide: [../../MCPB_PACKAGING_STANDARDS.md](../../MCPB_PACKAGING_STANDARDS.md)

---

## 🔗 Official Resources

- **MCP Website**: https://modelcontextprotocol.io/
- **Specification**: https://spec.modelcontextprotocol.io/
- **Glama Registry**: https://glama.ai/mcp/servers
- **GitHub**: https://github.com/modelcontextprotocol

---

## 📚 Related Documentation

| Section | Purpose |
|---------|---------|
| [../getting-started/](../getting-started/) | Quick start guide |
| [../protocol/](../protocol/) | MCP protocol fundamentals |
| [../fastmcp/](../fastmcp/) | FastMCP framework |
| [../deployment/](../deployment/) | Production deployment |

---

**The MCP ecosystem is growing rapidly. Join the community!** 🚀
