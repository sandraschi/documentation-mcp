---
project: mcp-agent-session-summaries
title: session-docs — Agent Session Documentation Server
status: active
priority: low
tags: [session-docs, infrastructure, tooling, session-persistence, agent-tooling]
created: 2026-06-??  (forked from upstream)
updated: 2026-07-25
repo: D:\Dev\repos\mcp-agent-session-summaries
github: https://github.com/chrisipanaque/mcp-agent-session-summaries (upstream)
---

# session-docs (mcp-agent-session-summaries)

Lightweight MCP server that stores and retrieves markdown documentation
files in a flat directory. Used by agent sessions to maintain a running
log of work across context resets and model swaps.

## Origin Story

This server was forked from `chrisipanaque/mcp-agent-session-summaries`
on GitHub during a session where the need for persistent cross-session
documentation became critical. A DeepSeek V4 agent session built the
fleet version, configuring it in `opencode.json` as `"session-docs"`.

The server lives at `D:\Dev\repos\mcp-agent-session-summaries\` and stores
its files in `data/sessions/` within that repo. It uses the legacy
`mcp.server.fastmcp` SDK (pre-fleet-standard `fastmcp>=3.x` package),
is a single-file 258-line server with 11 tools.

It was discovered by the user during a subsequent session when the
agent referenced docs saved in a previous session. This triggered
the "Agent-Spawned MCP Servers" transparency rule
(`mcp-central-docs/standards/rules/agent_spawned_mcp_servers.md`).

## Why It Exists

Agent sessions have finite context and are frequently reset (`/clear`,
`/compact`, model switches). Without a persistent storage layer:
- Session logs are lost
- Design decisions are forgotten
- The agent re-discovers the same codebase structure every session

session-docs fills this gap. It is Tier 1 per the agent-spawned rule:
append-only local file storage with a shutdown tool, bound to 127.0.0.1.

## Tools

| Tool | Access | Purpose |
|------|--------|---------|
| doc_read_file | read | Read a markdown file |
| doc_read_multiple_files | read | Read several files at once |
| doc_list_directory | read | Browse docs folder |
| doc_search_files | read | Glob-based file search |
| doc_get_file_info | read | File metadata |
| doc_help | read | Tool listing |
| doc_create_file | write | Create new markdown file |
| doc_edit_file | write | Overwrite existing file |
| doc_create_directory | write | Create subfolder |
| doc_delete_file | write | Permanently delete |
| doc_shutdown | lifecycle | Stop the server |

## Architecture

- **Transport**: stdio (no HTTP, no webapp)
- **SDK**: legacy `mcp.server.fastmcp` (not fleet `fastmcp>=3.4.4`)
- **Pattern**: single-file server, no package structure
- **Storage**: flat `.md` files in `data/sessions/`
- **Config**: `opencode.json` global MCP config

## Future

- Migrate to fleet-standard `fastmcp>=3.4.4` SDK
- Add `doc_rename` and `doc_duplicate` tools
- Optional HTTP transport for web access
- Search across all docs (full-text grep)
