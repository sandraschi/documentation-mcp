# MCP Fleet Marketplace

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**Claude Code as fleet conductor.** 22 live MCP servers across 4 bundles — not static skills, real tools Claude can call.

## Quick Start

```powershell
git clone https://github.com/sandraschi/mcp-fleet-marketplace
cd mcp-fleet-marketplace
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

## The Difference

| Static Skills (pm-claude-skills) | MCP Fleet Plugins (this repo) |
|---|---|
| "Here's how to write a PRD" | "Actually create the repo, open the PR" |
| "Here's how to plan a sprint" | "Query Jira, diff branches, open files for review" |
| Markdown instructions | Live MCP HTTP servers |
| Claude reads text | Claude calls APIs |

Each plugin bundle gives Claude Code real API access to multiple fleet servers, plus skills teaching it *how to orchestrate across them*.

## Quick Install

```
/plugin marketplace add sandr/mcp-fleet-marketplace
```

Then install individual bundles:

```
/plugin install media-deck-fleet@mcp-fleet-marketplace
/plugin install dev-toolchain@mcp-fleet-marketplace
/plugin install design-cad-fleet@mcp-fleet-marketplace
/plugin install windows-automation@mcp-fleet-marketplace
```

## Bundles

### media-deck-fleet (7 servers)
Audio/visual cross-app workflow. **The demo-reel bundle.**

| Server | Port | What it controls |
|---|---|---|
| virtualdj | 10877 | DJ decks, mixer, track loading |
| reaper | 10797 | DAW — multitrack recording/editing |
| obs | 10819 | Streaming scenes, recording, sources |
| resolume | 10920 | VJ visuals, clip triggering, compositing |
| osc | 10767 | Universal OSC protocol bridge |
| songgeneration | 10885 | AI music generation with deck export |
| audiotool-nexus | 10900 | Web modular synth and effects |

**Killer demo**: "Generate a track in SongGeneration, load it into VirtualDJ deck A, switch OBS to the DJ overlay scene, fire the Resolume visual preset on the drop."

### dev-toolchain (5 servers)
Every developer's daily stack with real API access.

| Server | Port | What it controls |
|---|---|---|
| git-github | 10702 | Git ops + GitHub API (PRs, issues, branches) |
| opencode-cli | 10951 | OpenCode CLI agent for sub-tasks |
| beyondcompare | 10841 | File/folder diff and merge comparison |
| notepadpp | 10815 | Editor automation, find/replace, macros |
| filesystem | 10742 | File read/write/search/glob |

### design-cad-fleet (6 servers)
3D, CAD, gamedev, and image pipeline.

| Server | Port | What it controls |
|---|---|---|
| blender | 10849 | 3D modeling, rendering, animation, export |
| freecad | 10944 | Parametric CAD, constraints, TechDraw |
| qcad | 10966 | 2D technical drafting, DXF, dimensions |
| gimp | 10773 | Image editing, layers, filters, batch |
| unity3d | 10831 | Scene management, GameObjects, prefabs |
| godot | 10993 | Scene tree, nodes, resources, TCP bridge |

### windows-automation (4 servers)
Windows power tools — your home turf.

| Server | Port | What it controls |
|---|---|---|
| windows-operations | 10748 | System ops, processes, services, registry |
| autohotkey | 10746 | Scripting, hotkeys, window management |
| pywinauto | 10789 | GUI automation, window control, inspection |
| winrar | 10762 | Archive operations (RAR, ZIP, 7z) |

## Prerequisites

Fleet servers must be running before Claude Code can connect. Each bundle includes a `start-fleet.ps1` script:

```powershell
# Start the media deck fleet
.\plugins\media-deck-fleet\scripts\start-fleet.ps1

# Or start all 22 servers at once:
Get-ChildItem plugins\*\scripts\start-fleet.ps1 | ForEach-Object { & $_ }
```

## Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the full design rationale.

## License

MIT
