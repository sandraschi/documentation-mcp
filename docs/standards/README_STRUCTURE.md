# Fleet README Structure Standard

**Status**: ACTIVE — applies to all sandraschi MCP server repos  
**Adopted**: 2026-05-28

---

## The Problem with Monolithic READMEs

A single README that covers installation, configuration, development setup,
tool reference, and troubleshooting satisfies no reader. End users drown in
dev setup details. Developers can't find the API reference. Install
instructions get buried under feature descriptions.

The rule: **one README, one audience, one job**.

---

## Required Structure

```
repo-root/
├── README.md                  ← PRIMARY: users, short, friendly, TOC
├── INSTALL.md                 ← All install paths (required)
├── AGENTS.md                  ← OpenAI Codex context
├── CLAUDE.md                  ← Claude Code context
└── docs/
    ├── CONFIGURATION.md       ← All env vars and config options
    ├── DEVELOPMENT.md         ← Dev setup, tools, contributing
    ├── TOOLS.md               ← Full MCP tool reference (MCP repos only)
    └── TROUBLESHOOTING.md     ← FAQ, common errors, diagnostics
```

---

## Primary README.md

**Audience**: First-time user, evaluating whether to install  
**Length**: 100–200 lines maximum  
**Tone**: Friendly, benefit-focused, no jargon  

### Required Sections (in order)

```markdown
# repo-name

One sentence: what it does and why you'd want it.

## Preview (webapp repos — required)

If the repo ships a React/Vite dashboard, include a **Preview** section with 1–2 screenshots
showing the AI-oriented webapp (not the native host app UI). See
[README_WEBAPP_SCREENSHOTS.md](../standards/README_WEBAPP_SCREENSHOTS.md).

```markdown
## Preview
| Dashboard | Feature |
|-----------|---------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Feature](docs/screenshots/feature-demo.png) |
*Caption: how this simplifies the wrapped host app (Blender, GIMP, KiCad, …).*
```

stdio-only repos may skip Preview or use an architecture diagram instead.

## How it runs (wrapper MCPs — required)

If the repo wraps a host application (Blender, KiCad, GIMP, Resolve, …), document
**headless vs GUI** execution honestly — do not bury this in INSTALL.md only.
See [README_WRAPPER_MCP.md](../standards/README_WRAPPER_MCP.md).

```markdown
## How it runs
| Mode | Host app | When |
| **Headless (default)** | … | … |
| **Live GUI (optional)** | … | … |

> **Headless by default** — one-sentence plain-language callout when true.
```

## Hands-in / Hands-out (wrapper MCPs — required)

What artifacts flow **into** and **out of** the wrappee (for agents and fleet pipelines).
Reference: blender-mcp → tahoma2d-mcp / godot-mcp chains.

```markdown
## Hands-in / Hands-out
| Direction | Artifacts | Notes |
| **Hands-in** | … | … |
| **Hands-out** | … | … |
```

## Features
- Bullet list of 4–8 capabilities (user benefits, not implementation details)

## Quick Install
The single fastest path (drag-and-drop .mcpb). One code block, done.
Link to INSTALL.md for other methods.

## What You Can Do
2–3 example prompts showing real usage. Shows value immediately.

## Documentation
| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Configuration](docs/CONFIGURATION.md) | Env vars, config options |
| [Tool Reference](docs/TOOLS.md) | All available tools |
| [Development](docs/DEVELOPMENT.md) | Contributing, local setup |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues |

## Requirements
Minimal: OS, Claude Desktop version, any hard dependencies

## License
```

### What Does NOT Belong in README.md

- Detailed install steps beyond the quick path
- Configuration tables with env vars
- Full tool reference
- Dev setup (uv, ruff, biome, just installation)
- Changelog
- Architecture diagrams

---

## INSTALL.md

**Audience**: Any user trying to install, across all experience levels  
**Length**: 150–300 lines  
**Critical requirement**: Must work on a naked Windows box with zero dev tools

**Normative bundling and LLM tiers:** [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md) — host apps and models are never in the installer; document Ollama/LM Studio **and** cloud API paths when the repo uses inference; Docker is not an Option A prerequisite.

### Required Sections

```markdown
# Installing {repo-name}

## Prerequisites

Install these if you don't have them already:

| Tool | Purpose | Install |
|------|---------|---------|
| Claude Desktop | Required host | [download](https://claude.ai/download) |
| Git | Clone repo (Option C/D only) | `winget install Git.Git` |
| Python + uv | Run server (Option C/D only) | `winget install astral-sh.uv` |
| Node.js | mcpb CLI (Option B only) | `winget install OpenJS.NodeJS` |

> Windows: all installs via [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/)  
> macOS: use `brew install` equivalents  
> Linux: use your distro package manager

## Option A — Drag and Drop (Recommended)
1. Go to [Releases](https://github.com/sandraschi/{repo}/releases/latest)
2. Download `{repo}-{version}.mcpb`
3. Open Claude Desktop → drag the file onto the window  
   *Or*: Settings → MCP Servers → Install from file

## Option B — mcpb CLI
```bash
# Requires Node.js (see Prerequisites)
npx @anthropic-ai/mcpb install https://github.com/sandraschi/{repo}
```

## Option C — Manual Configuration
1. Clone: `git clone https://github.com/sandraschi/{repo}`
2. Install deps: `cd {repo} && uv sync`
3. Add to Claude Desktop config:

```json
{
  "mcpServers": {
    "{repo}": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\{repo}", "run", "{entry-point}"],
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

Config file location:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

4. Restart Claude Desktop

## Option D — Developer Mode
For contributing or running from source with live reload.
See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Verify Installation
After installing, open Claude Desktop and type:
> "{a natural language prompt that exercises a basic tool}"

You should see: {expected output description}

## Troubleshooting
See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for common issues.
```

### INSTALL.md Anti-Patterns

- Do not assume `uv`, `git`, or `node` are installed without a winget step
- Do not use `uvx mcpb` — mcpb is npm, not PyPI
- Do not omit the config file path — users don't know where it is
- Do not omit the JSON snippet — users shouldn't have to look it up
- Do not link to "see the README" for install steps — the README links here

---

## docs/CONFIGURATION.md

**Audience**: User who has installed and wants to customize  
**Format**: Table of all environment variables, then any config file format

```markdown
# Configuration

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENV_VAR` | `value` | What it does |

## Setting Variables

In `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "{repo}": {
      "env": {
        "ENV_VAR": "your-value"
      }
    }
  }
}
```
```

---

## docs/DEVELOPMENT.md

**Audience**: Developer who wants to contribute or run from source  
**Must include**: Every tool needed, with install commands — do not assume anything

```markdown
# Development Setup

## Tools Required

Install all of these before continuing:

```bash
# Windows (winget)
winget install astral-sh.uv
winget install Git.Git
winget install OpenJS.NodeJS
winget install Casey.Just

# Verify
uv --version
git --version
node --version
just --version
```

## Setup

```bash
git clone https://github.com/sandraschi/{repo}
cd {repo}
uv sync
```

## Common Tasks

```bash
just lint      # ruff + biome
just test      # pytest
just format    # ruff format
just build     # build wheel + mcpb
```

## Code Standards
Link to mcp-central-docs standards.
```

---

## docs/TOOLS.md (MCP repos only)

**Audience**: Developer/power user who wants to understand all tools  
**Format**: One section per tool, with operation enum and examples

---

## docs/TROUBLESHOOTING.md

**Format**: Problem → Cause → Fix, as a flat list, no nesting

```markdown
# Troubleshooting

## Server doesn't appear in Claude Desktop
**Cause**: Config JSON is malformed  
**Fix**: Validate at jsonlint.com, check for trailing commas

## "command not found: uv"
**Cause**: uv not installed or not in PATH  
**Fix**: `winget install astral-sh.uv` then restart terminal

## Tool returns empty results
...
```

---

## Enforcement

### New Repos

Use `mcp-central-docs/templates/` as scaffold — it contains the correct
structure. The `new-mcp-server-intelligent.ps1` script should be updated to
emit this structure.

A repo isn't done being created until it's also registered in
`fleet-registry.json`, has a synced `projects/<repo-name>/` page, and has
a `FLEET_INDEX.md` row — see
[PROJECT_PAGE_STANDARD.md](./PROJECT_PAGE_STANDARD.md). This is a separate
checklist from the file-structure one above and is commonly skipped
(learnbot-mcp existed for three weeks, fully committed and running, before
anyone noticed it was invisible to the fleet's own catalog).

### Existing Repos

Priority order for retrofitting:
1. **INSTALL.md** — highest user impact, missing from most repos
2. **Primary README** restructure (shorten + add TOC)
3. **docs/CONFIGURATION.md** — extract env vars from README
4. **docs/TROUBLESHOOTING.md** — extract existing troubleshooting sections
5. **docs/DEVELOPMENT.md** — extract dev setup, add winget steps
6. **docs/TOOLS.md** — extract tool tables

### Validation

Run `scripts/check-readme-structure.ps1 -RepoPath <repo> -Strict` from mcp-central-docs
(or copy the script into the repo). It checks:

**Agents:** read `standards/AGENT_INSTALL_REFERENCE.md` before editing INSTALL.md.

The broader `scripts/check-repo-standards.ps1` can also be extended to check:
- [ ] README.md under 250 lines
- [ ] INSTALL.md exists
- [ ] INSTALL.md contains `winget` (prerequisite install steps)
- [ ] INSTALL.md contains `claude_desktop_config.json` JSON snippet
- [ ] INSTALL.md does NOT recommend `uvx mcpb install` (warnings that uvx fails are OK)
- [ ] LLM-enabled repos: INSTALL documents local **and** cloud inference ([LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md))
- [ ] Host-app repos: INSTALL documents external app install, not bundled ([LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md))
- [ ] docs/CONFIGURATION.md exists (for MCP repos)
- [ ] docs/TROUBLESHOOTING.md exists
