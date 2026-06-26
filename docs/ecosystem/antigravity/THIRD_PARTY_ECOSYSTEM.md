# Antigravity Third-Party Ecosystem

Antigravity (Google's AI IDE) doesn't have a public GitHub repo or open-source core, but a surprisingly active third-party ecosystem has grown around it — tools for account management, MCP servers, mobile companions, and cross-IDE config sync.

## Index

| Category | Project | Stars | Description |
|----------|---------|-------|-------------|
| Account mgmt | [jlcodes99/cockpit-tools](https://github.com/jlcodes99/cockpit-tools) | 7.9k | Multi-IDE account manager for Antigravity, Codex, Copilot, Windsurf, Cursor, Gemini CLI. Quota monitoring, auto-wake, multi-instance. |
| Account mgmt | [lingxiao69/lingxiao-ai-manager](https://github.com/lingxiao69/lingxiao-ai-manager) | — | Cursor + Antigravity dual-IDE account manager — quota queries, multi-account switching, machine ID reset. |
| UI customization | [Star016/Antigravity-Better](https://github.com/Star016/Antigravity-Better) | 252 | Customize the Antigravity AI chat panel — your IDE, your rules. |
| MCP ecosystem | [ali-kamali/Axon.MCP.Server](https://github.com/ali-kamali/Axon.MCP.Server) | 165 | Turn your codebase into an intelligent knowledge base for Cursor, Antigravity, and MCP-enabled tools. Semantic search, Roslyn analysis. |
| MCP integration | [mezallastudio/antigravity-blender-mcp](https://github.com/mezallastudio/antigravity-blender-mcp) | 31 | AI-powered Blender MCP for Antigravity IDE. |
| Mobile companion | [cafeTechne/antigravity-link-extension](https://github.com/cafeTechne/antigravity-link-extension) | 163 | Mobile companion for Antigravity — mirror AI sessions on your phone, send messages, stop generation, 9 MCP tools. |
| Mobile remote | [AvenalJ/AntigravityMobile](https://github.com/AvenalJ/AntigravityMobile) | 122 | Feature-rich mobile dashboard — live AI chat streaming, model quota monitoring, file browsing, Git, screen mirroring, terminal. |
| Mobile remote | [mrkungfudn/antigravity-ide-mobile](https://github.com/mrkungfudn/antigravity-ide-mobile) | 49 | Remote control panel for Antigravity — live AI chat streaming, file browser, Git, screen mirroring, terminal & admin panel. |
| Config sync | [Bronc-X/Lotus](https://github.com/Bronc-X/Lotus) | 114 | Write AI agent rules once, deploy to every IDE. Global protocol for Claude Code, Cursor, Windsurf, Antigravity, Codex & more. |
| Backend proxy | [funny-vibes/agent-vibes](https://github.com/funny-vibes/agent-vibes) | 307 | Unified Agent Gateway — lets Claude Code CLI and Cursor IDE use free AI backends (Antigravity, Codex) through protocol translation. |

## Key Observations

| Insight | Detail |
|---------|--------|
| **Account management dominates** | The most popular tools (cockpit-tools: 7.9k stars) solve quota management and multi-account switching — suggesting Antigravity has tight rate limits that power users bump into. |
| **Mobile companions are a theme** | Three separate projects (cafeTechne, AvenalJ, mrkungfudn) built mobile remotes — unusual for an IDE ecosystem. Suggests Antigravity sessions run unattended and users want remote monitoring. |
| **No official GitHub presence** | The supposed `github.com/google/antigravity-ide` doesn't exist. Google hasn't open-sourced any part of Antigravity. |
| **Config portability is underserved** | Only one project (Lotus) tackles cross-IDE config sync. Most users configure MCP servers per-IDE manually. |
| **The MCP layer is thin** | Only two MCP-specific projects (Axon, Blender MCP). The MCP config path (`%USERPROFILE%\.gemini\antigravity\mcp_config.json`) and key (`mcpServers`) match the standard pattern. |

## Fleet Implications

Antigravity is treated as a standard MCP client in our fleet. The `install-mcp.ps1` script supports it out of the box (see `arxiv-mcp/install-mcp.ps1`):

```powershell
.\install-mcp.ps1 antigravity
```

This writes to `%USERPROFILE%\.gemini\antigravity\mcp_config.json` with the standard `mcpServers` key — same format as Claude Desktop.
