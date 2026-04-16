# AI Producer Hub - Status

## Overview

**AI Producer Hub** is a composite MCP server for AI-powered music production.

Generate, Mix, Master, Stream - all in one server.

## Health: âœ… Active Development

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
| `/suno/*` | Suno-MCP | Pending |
| `/reaper/*` | Reaper-MCP | Pending |
| `/obs/*` | OBS-MCP | Pending |

## Local Tools

### MIDI Tools (8)

| Tool | Description |
|------|-------------|
| `list_midi_devices` | Scan connected hardware |
| `record_midi_performance` | Capture playing to MIDI file |
| `send_midi_note` | Trigger synths/modules |
| `play_midi_file` | Playback through hardware |
| `midi_monitor` | Debug MIDI connections |
| `midi_to_reaper` | Import to DAW |
| `midi_to_ai_seed` | Your melody â†’ AI prompt |

### Cross-Server Workflows

| Tool | Description |
|------|-------------|
| `suno_to_deck` | Generate AI track â†’ Load to VirtualDJ |
| `ai_dj_set` | Theme â†’ Full DJ set |
| `remix_plex_track` | Existing track â†’ AI remix |
| `live_stream_producer` | Generate + Mix + Stream |
| `album_factory` | Theme â†’ Full album â†’ Plex |
| `karaoke_generator` | Lyrics â†’ Song â†’ Karaoke mode |
| `bpm_bridge_generator` | Transition between tempos |
| `ai_mashup` | Combine two tracks with AI |

## Dependencies

```toml
dependencies = [
    "fastmcp>=3.1.1+.0",
    "python-rtmidi>=1.5.0",  # MIDI I/O
    "mido>=1.3.0",           # MIDI files
    "aiohttp>=3.9.0",
    "rich>=13.0.0"
]
```

## Installation

```powershell
cd D:\Dev\repos\ai-producer-hub
uv venv --python 3.11
.venv\Scripts\Activate.ps1
uv pip install -e .

# Install component servers
uv pip install -e D:\Dev\repos\virtualdj-mcp
uv pip install -e D:\Dev\repos\plexmcp
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "ai-producer-hub": {
      "command": "python",
      "args": ["-m", "ai_producer_hub"],
      "cwd": "D:\\Dev\\repos\\ai-producer-hub"
    }
  }
}
```

## Key Feature: MIDI â†’ AI

```
Your fingers on keys â†’ MIDI bytes â†’ AI understanding â†’ Full production
     (1983 tech)      (serial data)   (2025 magic)    (instant result)
```

Play 4 bars. Get a track. That's the future.

## Repository

- Path: `D:\Dev\repos\ai-producer-hub`
- GitHub: `sandraschi/ai-producer-hub`


