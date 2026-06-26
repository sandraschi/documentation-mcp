# OpenCode — Ecosystem & Fleet Integration

OpenCode is an open source AI coding agent (160K stars, 900+ contributors). Available as CLI, TUI, desktop app, or IDE extension. Supports 75+ LLM providers including local models via Ollama/LM Studio.

## MCP Server Config

Add MCP servers in `opencode.json` (project) or `~/.config/opencode/opencode.json` (global):

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "arxiv-mcp": {
      "type": "stdio",
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/arxiv-mcp", "python", "-m", "arxiv_mcp", "--stdio"]
    }
  }
}
```

Or use the fleet-standard `install-mcp.ps1` from any repo:
```powershell
.\install-mcp.ps1 print    # just output the JSON
```

OpenCode auto-discovers MCP tools at connect time — no restart required.

## Plugin API Overview

Plugins are JavaScript/TypeScript modules in `~/.config/opencode/plugins/` (global) or `.opencode/plugins/` (project). Each exports an async function that receives a context object and returns hooks.

### Plugin Function Signature

```js
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  return {
    // Hook implementations go here
  }
}
```

| Arg | Type | Purpose |
|-----|------|---------|
| `project` | `{ name, root, language }` | Current project info |
| `client` | SDK client | `.app.log()`, `.session.status()` |
| `$` | Bun shell API | Execute shell commands |
| `directory` | string | Working directory |
| `worktree` | string | Git worktree root |

### Available Hooks

**Session lifecycle:**
| Hook | When | Signature |
|------|------|-----------|
| `session.created` | New session starts | `(input, output) => {}` |
| `session.idle` | Agent becomes idle | via `event:` hook |
| `session.deleted` | Session removed | via `event:` hook |
| `session.compacted` | Context compacted | via `event:` hook |
| `experimental.session.compacting` | Before compaction | `(input, output) => {}` — can inject context |

**Tool interception:**
| Hook | When | Signature |
|------|------|-----------|
| `tool.execute.before` | Before any tool runs | `(input, output) => {}` — throw to block |
| `tool.execute.after` | After tool completes | `(input, output) => {}` |

**Messaging:**
| Hook | When | Signature |
|------|------|-----------|
| `message.updated` | Message content changes | `(input, output) => {}` |
| `message.part.updated` | Message part (tool call/reply) updates | `(input, output) => {}` |
| `message.removed` | Message deleted | `(input, output) => {}` |

**Shell:**
| Hook | When | Signature |
|------|------|-----------|
| `shell.env` | Before any shell executes | `(input, output) => {}` — set `output.env` |

**UI:**
| Hook | When | Signature |
|------|------|-----------|
| `tui.toast.show` | Toast notification appears | `(input, output) => {}` — set `output.message` |
| `tui.prompt.append` | User submits a prompt | `(input, output) => {}` |
| `tui.command.execute` | Slash command invoked | `(input, output) => {}` |

**Events (generic):**
| Hook | When | Signature |
|------|------|-----------|
| `event` | Any system event fires | `({ event }) => {}` where `event.type` is the event name |

Event types: `session.idle`, `session.deleted`, `session.compacted`, `session.error`, `session.status`, `session.diff`, `session.updated`, `permission.asked`, `permission.replied`, `file.edited`, `file.watcher.updated`, `todo.updated`, `lsp.client.diagnostics`, `lsp.updated`, `server.connected`, `command.executed`, `installation.updated`.

### Custom Tools

Plugins can register new tools alongside built-in ones:

```ts
import { type Plugin, tool } from "@opencode-ai/plugin"

export const MyTools: Plugin = async () => ({
  tool: {
    mytool: tool({
      description: "Does something useful",
      args: {
        query: tool.schema.string(),
        limit: tool.schema.number().min(1).max(100).default(10),
      },
      async execute(args, ctx) {
        return `Result for ${args.query}`
      },
    }),
  },
})
```

## Fleet Plugins

The following plugins are maintained in the fleet under `opencode-plugins/` in the `arxiv-mcp` repo. Copy to `~/.config/opencode/plugins/` to install.

### 1. DeepSeek Cost Limiter (`deepseek-limiter.js`)

Tracks token usage per session against a daily budget. Blocks tool execution at budget limit (read-only tools still work). 

```bash
export OPENCODE_DEEPSEEK_DAILY_BUDGET_USD=1.00
```

**Key hooks:** `message.updated` (track tokens), `tool.execute.before` (block), `event` (persist), `tui.toast.show` (warn at 80%)

### 2. Fleet Context Injector (`fleet-context.js`)

Injects live fleet state (which MCP servers are up, their tools, ports) into session context and preserves it across compactions. Polls the federation hub's health API every 30s with local caching.

**Data source:** Federation hub (`GET /api/v1/servers`) — live health from the Fleet Supervisor. Falls back to `fleet-manifest.json` if hub is unreachable.

**Key hooks:** `session.created` (inject on start), `experimental.session.compacting` (preserve across resets), `tool.execute.before` (context hint on heavy ops)

### 3. Fleet Env Injector (`fleet-env.js`)

Injects fleet-standard environment variables (`ARXIV_MCP_*`, service ports, `PYTHONUNBUFFERED`) into every shell.

**Data source:** `~/.config/opencode/plugins/fleet-env.json`

**Key hooks:** `shell.env`

### Plugin Load Order

1. Global config JSON (`~/.config/opencode/opencode.json`)
2. Project config JSON (`opencode.json`)  
3. Global plugin directory (`~/.config/opencode/plugins/`)
4. Project plugin directory (`.opencode/plugins/`)

For fleet plugins, the global directory is recommended — they apply to all projects.

## Agent System

OpenCode supports custom AI agents defined as markdown files:

```
~/.config/opencode/agents/code-reviewer.md
---
description: Reviews code for best practices
mode: subagent
model: deepseek/deepseek-v4-pro
permission:
  edit: deny
  bash: deny
---
You are a code reviewer focused on security and maintainability.
```

Built-in agents: **Build** (full access), **Plan** (read-only, planning), **General** (multi-step), **Explore** (fast codebase search), **Scout** (external docs/deps).

## Skills

Markdown skill files in `~/.config/opencode/skills/` or bundled via MCP servers (like arxiv-mcp's `skill://arxiv-researcher`). These get injected on demand when the agent needs domain expertise.

## Fleet MCP Config Pattern

All fleet repos ship an `install-mcp.ps1` that reads `manifest.json` and writes the correct OpenCode config block. OpenCode uses the same `mcpServers` key as Claude Desktop — the JSON block is identical.

```
just install-mcp print  # see config before installing
```

## Links

- [OpenCode docs](https://opencode.ai/docs)
- [Plugin API reference](https://opencode.ai/docs/plugins)
- [Agent docs](https://opencode.ai/docs/agents)
- [MCP server config](https://opencode.ai/docs/mcp-servers)
- [GitHub repo](https://github.com/anomalyco/opencode)
