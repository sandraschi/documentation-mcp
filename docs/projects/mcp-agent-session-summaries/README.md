<h1 align="center">MCP Tool to Create Agent Session Summaries in a Specified Folder</h1>

<p align="center">
  Let your OpenCode coding agent document agent sessions in a safe, sandboxed markdown folder.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/MCP%20Server-purple" alt="MCP Server">
  <img src="https://img.shields.io/badge/License-MIT-yellowgreen" alt="MIT License">
  <img src="https://img.shields.io/badge/OpenCode-ready-brightgreen" alt="OpenCode Ready">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="Version 0.1.0">
</p>

---

Let your OpenCode coding agent document agent sessions in a safe, sandboxed markdown folder.

Add to your project's `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "mcp-agent-session-summaries": {
      "type": "local",
      "command": [
        "python3",
        // Where the mcp-agent-session-summaries/server.py is located
        "/User/path/mcp-agent-session-summaries/server.py",
        // Your chosen documentation folder
        "/User/path/Documents/agent-session-documents"
      ],
      "enabled": true
    }
  }
}
```

This lets the agent manage the server lifecycle automatically.

## What this is for

This MCP tool leverages your agent's LLM to document what happened during your current session.

Instead of relying on the agent's internal database or manually creating READMEs for each of your projects, you tell your agent to document a summary and it will save it your chosen markdown folder.

Ideas of what the agent can document:

- Session summaries and conversation histories
- System design decisions
- Task executions and outcomes
- Architecture decisions and tradeoffs
- Engineering logs
- Any context you want to capture from the session

Your chosen documentation folder becomes a living record of what your agents have done. It's goal is to contain human-readable markdown, ready to reference in the future.

Example:

After a long coding session, you tell your agent:

*"Summarize this session and save it to my docs folder."*

The agent uses the MCP tools to create and edit markdown files with all the details: Engineering decisions, system design, prompts that worked, architecture notes.

Over time you build a human-readable folder of every session's knowledge. No digging through OpenCode's internal database. No hunting for README files across your filesystem. Just a docs folder full of markdown, ready to reference at any time.

---

## Why not just README files?

- You'd have to manually create one for every project
- You'd have to search your filesystem to find what you need
- You'd lose context — you can only document what you remember after the fact

This server lets the agent use its current session context (everything you just did) to generate rich documentation *at the moment it's fresh*. Past sessions become reference docs you can point the agent back to later.

---

## How it works

OpenCode starts this server as a background process when your agent session begins. The server exposes 9 tools over the Model Context Protocol. The agent decides when to call them based on what you ask.

```
┌──────────────┐   stdio (JSON-RPC)    ┌──────────────────────────┐
│              │   tools/list          │                          │
│  OpenCode    │ ───────────────────►  │  mcp-agent-session-summaries │
│              │   tools/call          │                          │
│              │ ◄──────────────────── │  9 tools for .md files   │
└──────────────┘                       └──────────────────────────┘
```

---

## Design

These tools are named and described based on how LLMs select and use them:

1. **Tool names are the strongest signal** — the `doc_` prefix groups related tools so the model recognizes them as a documentation system, not generic file operations.

2. **Descriptions say WHEN to use the tool** — vague descriptions make the LLM guess. Each tool's description tells the model exactly when it's the right choice.

3. **Write tools get explicit directives** — `doc_create_file` and `doc_edit_file` tell the model "ALWAYS use this for markdown documentation" and "do NOT write .md files directly." This prevents the model from writing documentation to the wrong folder.

4. **Tool descriptions are the only reliable channel** — research shows agents consistently read tool names and descriptions, while other metadata types are frequently ignored. All usage guidance lives here.

---

## Tools

| Tool | What it does | Input |
|---|---|---|
| `doc_read_file` | Read a session documentation file | `path` |
| `doc_read_multiple_files` | Read several documentation files at once | `paths` (list) |
| `doc_list_directory` | Browse the documentation folder structure | `path` |
| `doc_search_files` | Search for documentation files matching a pattern | `pattern`, `path` |
| `doc_get_file_info` | Get metadata about a documentation file | `path` |
| `doc_create_file` | Create a new session documentation file | `path`, `content` |
| `doc_edit_file` | Overwrite an existing documentation file | `path`, `content` |
| `doc_delete_file` | Delete a documentation file | `path` |
| `doc_create_directory` | Create a subfolder inside the documentation folder | `path` |

---

## Requirements

- **Python 3.10 or newer**
- The `mcp` package: `pip install mcp`

---

## Setup

Add to your project's `opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "mcp-agent-session-summaries": {
      "type": "local",
      "command": [
        "python3",
        // Where the mcp-agent-session-summaries/server.py is located
        "/User/path/mcp-agent-session-summaries/server.py",
        // Your chosen documentation folder
        "/User/path/Documents/agent-session-documents"
      ],
      "enabled": true
    }
  }
}
```

Replace the two paths:
- `/full/path/to/server.py` — where you saved `server.py`
- `/full/path/to/your/documents` — the folder where you want session docs to accumulate

---

## Example prompts

Once configured, just ask your agent naturally:

| What you want | Prompt |
|---|---|
| **Log a session** | *"Summarize everything we did this session and save it to sessions/2025-07-13-api-redesign.md"* |
| **Document design decisions** | *"Create a markdown file documenting the system design decisions we made today in docs/design-decisions.md"* |
| **Engineering log** | *"Update engineering-log.md with what we accomplished this session"* |
| **Architecture docs** | *"Document the architecture of this project in docs/architecture.md"* |
| **Reference past work** | *"Read sessions/2025-07-10-auth-flow.md and remind me what we decided about authentication"* |

---

## Security: what it CAN'T do

- **Can't access files outside the documents folder** — path traversal (`../../etc/passwd`) is rejected
- **Can't create non-markdown files** — only `.md` extension is allowed for writes
- **Can't overwrite files by accident** — `create_markdown` refuses if the file already exists
- **Can't read non-markdown files** — `read_file` and `read_multiple_files` also require `.md`

---

## Project structure

```
mcp-agent-session-summaries/
├── server.py         # The MCP server (all 9 tools)
├── pyproject.toml    # Python dependencies
└── README.md         # This file
```

---

## Non-agent testing

This is for testing this tool outside your agent.


```bash
git clone https://github.com/chrisipanaque/mcp-agent-session-summaries
cd mcp-agent-session-summaries
python3 -m venv .venv
source .venv/bin/activate
pip install mcp
# create your documentation folder
mkdir -p /Documents/agent-coding-sessions
# point the tool to your documentation folder
python server.py /Documents/agent-coding-sessions
```

---
