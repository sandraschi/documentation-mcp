---
title: "MCP Client Config Snippets Pattern"
category: pattern
status: active
audience: mcp-dev
skill_candidate: true
related:
  - standards/AGENT_PROTOCOLS.md
last_updated: 2026-02-10
---

# MCP Client Config Snippets Pattern

**Reusable JSON snippets and standard locations for adding MCP servers to IDE/client configs.**

## Pattern

1. **Snippet**: One JSON object keyed by server name; `command`, `args`, `env` (with `PYTHONPATH` pointing at repo `src/`)
2. **Placement**: Merge into client's `mcpServers` object
3. **Idempotency**: Only insert if server key not already present
4. **Backup**: Timestamped backup before writing

## Generic Snippet Template (clone-based Python)

```json
"<server-key>": {
  "command": "python",
  "args": ["-m", "<MODULE>"],
  "env": {
    "PYTHONPATH": "<REPO_ROOT>/src",
    "PYTHONUNBUFFERED": "1"
  }
}
```

Windows venv: `"command": "<REPO_ROOT>/.venv/Scripts/python.exe"`

## Client Config Locations (Windows)

| Client | Config path | Servers key |
|--------|-------------|-------------|
| **Cursor** | `%APPDATA%\Cursor\User\globalStorage\cursor-storage\mcp_config.json` | `mcpServers` |
| **Claude Desktop** | `%APPDATA%\Claude\claude_desktop_config.json` | `mcpServers` |
| **Windsurf** | `%USERPROFILE%\.codeium\windsurf\mcp_config.json` | `mcpServers` |
| **Zed** | `%APPDATA%\Zed\settings.json` | `mcpServers` |
| **Antigravity** | `%USERPROFILE%\.gemini\antigravity\mcp_config.json` | `mcpServers` |
| **LM Studio** | `%USERPROFILE%\.lmstudio\mcp.json` | `mcpServers` |

## Snippet Files in Repos

Ship under `snippets/` directory:
- `mcp-config-<server-name>.json` — one key: server name; value: config object with `<REPO_ROOT>` placeholder
- `README.md` — replace placeholder, merge into `mcpServers`; link to INSTALL

## Insert Automation Logic

1. Resolve config path per client
2. Read existing JSON; if missing, create with `{ "mcpServers": {} }`
3. Backup: copy to `config.YYYYMMDD-HHMMSS.json` in same directory
4. If server key already under `mcpServers` → skip (idempotent)
5. Add snippet, write back with pretty-print
