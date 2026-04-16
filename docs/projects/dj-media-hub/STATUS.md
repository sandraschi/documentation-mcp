# DJ Media Hub - Status

## Overview

**DJ Media Hub** is a composite MCP server mounting VirtualDJ and Plex for cross-server DJ workflows.

## Health: âœ… Active

| Metric | Status |
|--------|--------|
| Last Updated | November 2025 |
| Python | 3.10-3.11 |
| FastMCP | 3.1.1++ |
| Server Type | Composite |

## Mounted Servers

| Mount | Server | Tools |
|-------|--------|-------|
| `/dj/*` | VirtualDJ-MCP | 61 |
| `/plex/*` | Plex-MCP | 15 |

## Cross-Server Tools

| Tool | Description |
|------|-------------|
| `plex_to_deck` | Search Plex â†’ Load to VirtualDJ deck |
| `plex_playlist_to_automix` | Plex playlist â†’ VDJ automix queue |
| `record_mix_to_plex` | Save VDJ recording â†’ Plex library |
| `multi_deck_plex_load` | Load 8 tracks from Plex â†’ 8 decks |
| `hub_status` | Status of mounted servers |
| `hub_help` | Help for workflows |

## Key Feature: Multi-Deck Plex Load

```python
multi_deck_plex_load([
    "Daft Punk Around the World",
    "Chemical Brothers Block Rockin",
    "Fatboy Slim Praise You",
    # ... up to 8 tracks
])
# All 8 decks loaded in one call!
```

## Installation

```powershell
cd D:\Dev\repos\dj-media-hub
uv venv --python 3.11
.venv\Scripts\Activate.ps1
uv pip install -e .
uv pip install -e D:\Dev\repos\virtualdj-mcp
uv pip install -e D:\Dev\repos\plexmcp
```

## Repository

- Path: `D:\Dev\repos\dj-media-hub`
- GitHub: `sandraschi/dj-media-hub`

## Relation to AI Producer Hub

DJ Media Hub is the simpler version focused only on VirtualDJ + Plex.

AI Producer Hub extends this with Suno, Reaper, OBS, and MIDI tools.


