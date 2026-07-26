# Installing {REPO_NAME}

{ONE_SENTENCE_DESCRIPTION}

---

## Prerequisites

Install these if you don't have them already. Windows commands use
[winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
(built into Windows 10 1809+ / Windows 11):

| Tool | Required for | Windows | macOS |
|------|-------------|---------|-------|
| **Claude Desktop** | all options | [claude.ai/download](https://claude.ai/download) | same |
| **uv** | Options C and D | `winget install astral-sh.uv` | `brew install uv` |
| **git** | clone repo (Options C/D) | `winget install Git.Git` | `brew install git` |
| **Node.js** | Option B only | `winget install OpenJS.NodeJS` | `brew install node` |

> **Windows:** After any winget install, **close and reopen PowerShell** so PATH updates apply.  
> **macOS:** use `brew install uv git node` equivalents.

<!-- Add repo-specific prerequisites here (gh CLI, Docker Desktop, Ollama, host app, etc.) -->
<!-- Docker: "Docker Desktop is only needed for X tools. Everything else works without it." -->
<!-- Host app: "Blender/Unity/etc. is never bundled — install separately: [url]" -->
<!-- LLM (if applicable): see section below — Ollama AND cloud API, equal prominence -->

---

## Option A — Drag and Drop (Recommended)

No Python, uv, or git required. Claude Desktop manages the runtime.

1. Go to [Releases](https://github.com/sandraschi/{REPO_NAME}/releases/latest)
2. Download `{REPO_NAME}-*.mcpb`
3. Open Claude Desktop
4. Drag the `.mcpb` file onto the Claude Desktop window and accept the install prompt

**Pass criteria:** server appears in the MCP list with no terminal steps.

---

## Option B — mcpb CLI

`mcpb` is **not** on PyPI — `uvx mcpb` will fail. Requires Node.js:

```powershell
winget install OpenJS.NodeJS --accept-source-agreements --accept-package-agreements
# Close and reopen terminal, then:
npx @anthropic-ai/mcpb install https://github.com/sandraschi/{REPO_NAME}
```

Restart Claude Desktop after install completes.

---

## Option C — Manual Configuration

```powershell
winget install astral-sh.uv --accept-source-agreements --accept-package-agreements
winget install Git.Git --accept-source-agreements --accept-package-agreements
# Close and reopen terminal

git clone https://github.com/sandraschi/{REPO_NAME}
cd {REPO_NAME}
uv sync --all-extras
```

Edit Claude Desktop config:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "{REPO_NAME}": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\{REPO_NAME}",
        "run",
        "{ENTRY_POINT}",
        "--stdio"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

Replace `C:\\path\\to\\{REPO_NAME}` with your actual clone path. Restart Claude Desktop.

<!-- Entry point from [project.scripts] in pyproject.toml — NOT uv run -m module -->

---

## Option D — Developer Mode

For contributing or running from source. Requires all tools in Prerequisites.

```powershell
winget install Casey.Just --accept-source-agreements --accept-package-agreements
git clone https://github.com/sandraschi/{REPO_NAME}
cd {REPO_NAME}
uv sync --all-extras
uv run {ENTRY_POINT} --stdio
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for linting, testing, and mcpb packaging.

---

## Verify Installation

In Claude Desktop, try:

> "{VERIFY_PROMPT}"

You should see: {VERIFY_EXPECTED_OUTPUT}

If you get "tool not found", restart Claude Desktop and check that the server appears
in Settings → MCP Servers.

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MCP_TRANSPORT` | `stdio` | Transport: `stdio` \| `http` \| `sse` |
| `MCP_HOST` | `127.0.0.1` | Bind address for HTTP/SSE |
| `MCP_PORT` | `{DEFAULT_PORT}` | MCP HTTP port |
| `FASTMCP_LOG_LEVEL` | `WARNING` | Log verbosity: `DEBUG` \| `INFO` \| `WARNING` |
| `PYTHONUNBUFFERED` | — | Set to `1` in Claude Desktop config |

<!-- Add repo-specific env vars. See docs/CONFIGURATION.md for full reference. -->

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Server not in Claude Desktop | Run `uv run {ENTRY_POINT} --stdio` directly to see error; check config path |
| `uv` not found | `winget install astral-sh.uv`; reopen terminal |
| `git` not found | `winget install Git.Git`; reopen terminal |
| `uv sync` fails | Ensure Python 3.12+: `uv python install 3.12` |
| `uvx mcpb` fails | Expected — use Option A or `npx @anthropic-ai/mcpb` |

<!-- Add repo-specific troubleshooting rows here -->

Full diagnostics: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) · [open an issue](https://github.com/sandraschi/{REPO_NAME}/issues)

---

*Feature overview: [README.md](README.md)*

---

<!--
TEMPLATE VARIABLES — replace all before committing:
  {REPO_NAME}                  e.g. filesystem-mcp
  {ONE_SENTENCE_DESCRIPTION}   e.g. "File system, Git, and Docker operations for Claude Desktop."
  {ENTRY_POINT}                from [project.scripts] in pyproject.toml (e.g. filesystem-mcp)
  {DEFAULT_PORT}               from WEBAPP_PORTS.md (e.g. 10742)
  {VERIFY_PROMPT}              e.g. "List the files in my home directory"
  {VERIFY_EXPECTED_OUTPUT}     e.g. "a directory listing from file_ops"

REPO CLASS — identify before filling:
  MCP hand (blender-mcp, filesystem-mcp, git-github-mcp, ...): Options A-D; this template
  Control plane (robofang): start.ps1 + hub UI — use CONTROL_PLANE_INSTALL.md instead
  Isolation stack (deepfang): Docker required — see CONTROL_PLANE_INSTALL.md

CHECKLIST (from AGENT_INSTALL_REFERENCE.md §18):
  [ ] Options A-D preserved with correct semantics
  [ ] --stdio in Option C args
  [ ] --accept-source-agreements on winget commands
  [ ] uv sync --all-extras
  [ ] No uvx mcpb anywhere
  [ ] No dev tools (just/ruff/biome) in end-user Prerequisites
  [ ] Host app (if any): documented as separate install, not bundled
  [ ] LLM (if any): Ollama/LM Studio AND cloud API, equal prominence — see blender-mcp reference
  [ ] Docker: optional footnote only (unless deepfang-class)
  [ ] Entry point from pyproject.toml [project.scripts]
  [ ] Ran check-readme-structure.ps1 -Strict

REFERENCE IMPLEMENTATION: sandraschi/blender-mcp INSTALL.md
FULL STANDARD: mcp-central-docs/standards/AGENT_INSTALL_REFERENCE.md
FORBIDDEN PATTERNS: see AGENT_INSTALL_REFERENCE.md §13
-->
