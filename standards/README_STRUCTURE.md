---
title: "Fleet README Structure Standard"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
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
    ├── ONBOARDING.md          ← First-timer wrappee/account (DEFAULT — see ONBOARDING_STANDARD.md)
    ├── CONFIGURATION.md       ← All env vars and config options
    ├── DEVELOPMENT.md         ← Dev setup, tools, contributing
    ├── ARCHITECTURE.md        ← System architecture, data flow, ports, protocols
    ├── TOOLS.md               ← Full MCP tool reference (MCP repos only)
    ├── WRAPPEE.md             ← Wrapped host-app overview + community links (wrapper repos — see below)
    └── TROUBLESHOOTING.md     ← FAQ, common errors, diagnostics
```

**Update (2026-07-30)**: `ARCHITECTURE.md` moves from repo root into `docs/`,
alongside the other reference docs - it was never actually specified before
and repos put it wherever felt natural, which was mostly root. New repos and
retrofits should use `docs/ARCHITECTURE.md`.

**Update (2026-10-22)**: contributor-facing rules (issues, PRs, conduct) live
in root `CONTRIBUTING.md` (GitHub-native discovery) - see
`GITHUB_HYGIENE_STANDARDS.md`. `docs/DEVELOPMENT.md` keeps dev setup and
tooling detail.

**`docs/WRAPPEE.md` (wrapper repos — required)**: a dedicated page for the
host application this repo wraps — what it is, and where to find its
homepage, community (Discord/Matrix/Reddit/Mastodon, whatever exists),
official docs, and GitHub. This matters most for **obscure or easily-confused
wrappees** — e.g. a person landing on `overte-mcp` reasonably asks "isn't
this called Vircadia?" (it split from Vircadia's original codebase; current
"Vircadia" is now an unrelated product). A well-known wrappee like Blender
needs this less; an obscure or ambiguously-named one needs it a lot. See the
[Wrapper MCP README Standard](./README_WRAPPER_MCP.md) for the full contract
(this file plus the README's own "What You Can Do" section).

When the product wraps a host app or needs a vendor account (**default for fleet MCPs** — even Notepad++), **`docs/ONBOARDING.md` is mandatory**, plus webapp big-red CTA and MOCK-until-onboarded. See [ONBOARDING_STANDARD.md](./ONBOARDING_STANDARD.md).
---

## Primary README.md

**Audience**: First-time user, evaluating whether to install  
**Length**: 100–200 lines maximum  
**Tone**: Friendly, benefit-focused, no jargon  

### Required Sections (in order)

```markdown
# repo-name

One sentence: what it does and why you'd want it.

## What this wraps (wrapper repos — required, first thing after the title)

Name the wrapped host app immediately — don't make the reader hunt for it.
One or two sentences: what the app is, and a link to
[docs/WRAPPEE.md](docs/WRAPPEE.md) for the full picture (official links,
community, disambiguation from similarly-named projects). This matters most
for obscure or confusable wrappees — e.g. "wraps **Overte**, the open-source
continuation of the original Vircadia/High Fidelity codebase (not to be
confused with current 'Vircadia,' an unrelated product)."

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

## Demo video (optional, when available)

If [demo-vid-mcp](https://github.com/sandraschi/demo-vid-mcp) has produced a
walkthrough for this repo, embed it here (early in the README, near Preview).
Not yet mandatory fleet-wide — demo-vid-mcp is new (2026-07) and still
maturing — but worth adding as videos become available; automating this
across 150+ repos is expected to meaningfully improve first impressions.

## What You Can Do

For **wrapper repos**, this section replaces the old separate "How it runs"
+ "Hands-in / Hands-out" split — fold both into one section so a reader gets
execution honesty and the artifact pipeline in one place, right after they
know what's being wrapped:

```markdown
## What You Can Do

**How it runs**: headless Blender subprocess by default; optional live
session + bridge addon to watch in the GUI. Blender itself is never bundled
— install separately.

| Direction | Artifacts | Notes |
|-----------|-----------|-------|
| **Hands-in** | `.blend`, image refs, natural-language scene prompts | Upload via webapp or tool params |
| **Hands-out** | `.glb`, `.vrm`, `.blend`, viewport PNG | `blender_export`, `blender_render` |

- 4–8 more capability bullets (user benefits, not implementation details)
```

Non-wrapper repos can use a plain features list here instead — the
headless/hands-in-out structure is specifically for repos that drive another
program. Full rules for headless-vs-GUI honesty and artifact tables:
[README_WRAPPER_MCP.md](../standards/README_WRAPPER_MCP.md).

## Install (single-click, installer first)

Lead with the **NSIS installer** for repos with a webapp: it is the only artifact that installs the
whole product (webapp + embedded backend), so it is the default for end users. No `git clone`, no
`just`, no Python or Node. Direct them to GitHub Releases ([RELEASE_TIERS.md](./RELEASE_TIERS.md)).

```markdown
## Install

1. Download **`{repo}-{version}-setup.exe`** from the [latest release](https://github.com/sandraschi/{repo}/releases/latest).
2. Run it. Windows may show a SmartScreen warning because the installer is unsigned:
   choose **More info > Run anyway**.
3. Open **{Product}** from the Start menu.

**Only want the tools inside Claude?** The `.mcpb` bundle registers the MCP server in Claude Desktop
but does **not** install the webapp. Paste this to Claude:

> Install the {repo} MCP extension: download `{repo}-{version}.mcpb` from
> https://github.com/sandraschi/{repo}/releases/latest and open it with Claude Desktop.

**Developers:** build from source, justfile recipes, tests and packaging are in
[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).
```

Rules:
- The installer is step one. The `.mcpb` is the second path and always says what it does not install.
- The "paste this to Claude" wording is a template; validate it against the Claude client you document
  and adjust the sentence, not the structure.
- Repos with **no webapp** (Class B) lead with the `.mcpb` and the same paste-to-Claude prompt.
- **No `just ...` command, no `git clone`, no `uv sync` anywhere in the README install section.** Those
  live in `docs/DEVELOPMENT.md`, together with the justfile recipes (`build-native`, `mcpb-pack`,
  `cua-nsis-test`, ...) and their prerequisites. Ordinary users never need them.
- Link `INSTALL.md` for everything else (manual config, other clients, troubleshooting).

## Example Prompts
2–3 example prompts showing real usage. Shows value immediately.

## Fleet Crossconnects (Companions) (when applicable)
If the server connects to or enhances peer fleet repositories (e.g. email-mcp, speech-mcp),
include the standard crossconnect table. See [FLEET_CROSSCONNECT_STANDARD.md](./FLEET_CROSSCONNECT_STANDARD.md).
Companions must be optional and self-contained; never require mandatory transitive installs.

## Documentation
| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Onboarding](docs/ONBOARDING.md) | First-timer account/host setup, money/CC, pitfalls (when applicable) |
| [Wrapped app](docs/WRAPPEE.md) | What it is, official links, community, disambiguation (wrapper repos) |
| [Architecture](docs/ARCHITECTURE.md) | System architecture, data flow, ports |
| [Configuration](docs/CONFIGURATION.md) | Env vars, config options |
| [Tool Reference](docs/TOOLS.md) | All available tools |
| [Development](docs/DEVELOPMENT.md) | Contributing, local setup |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues |

## Requirements
Minimal: OS, Claude Desktop version, any hard dependencies

## License
```

### What Does NOT Belong in README.md

- `git clone`, `uv sync`, `just ...` or any build step in the install section (developer docs only)
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

## Option A — Windows installer (Recommended, repos with a webapp)
1. Go to [Releases](https://github.com/sandraschi/{repo}/releases/latest)
2. Download `{repo}-{version}-setup.exe` and run it (unsigned: SmartScreen "More info > Run anyway")
3. Open **{Product}** from the Start menu

Installs the webapp and the backend; no other prerequisites. Per-user install, no admin prompt.

## Option A2 — Claude Desktop bundle (.mcpb; Recommended for repos with no webapp)
1. Download `{repo}-{version}.mcpb` from the same release
2. Open Claude Desktop → drag the file onto the window  
   *Or*: Settings → MCP Servers → Install from file

Registers the MCP server in Claude Desktop only. It does **not** install the webapp.

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
- **NEVER require private central infrastructure (`mcp-central-docs` or `D:\Dev\repos` paths)** — the repo must install and run standalone on any clean PC
- Do not reference internal tooling scripts in user install steps (users cannot clone private repositories)
- Document the ConPTY pipe teardown error (`0x800700e8`) in troubleshooting sections with the fix (use `cmd.exe /k` or run frontend build manually)


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
- [ ] README install section links GitHub Releases and contains no `just ...`, `git clone` or `uv sync`
- [ ] Class A repos: README and INSTALL.md lead with the NSIS installer; the `.mcpb` says it does not install the webapp
- [ ] docs/DEVELOPMENT.md documents every justfile recipe a developer needs (`build-native`, `mcpb-pack`, `cua-nsis-test`, ...)
- [ ] Release gate passes: `scripts/check-release-gate.ps1` ([RELEASE_TIERS.md](./RELEASE_TIERS.md))
