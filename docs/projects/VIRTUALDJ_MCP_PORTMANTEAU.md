# VirtualDJ-MCP Portmanteau Reference

> **Status**: Production Ready  
> **Tool Count**: 12 portmanteau tools (consolidated from 62+)  
> **New Feature**: Plex Media Server integration

## Overview

VirtualDJ-MCP provides professional DJ automation through 12 consolidated portmanteau tools, following the [Portmanteau Pattern](../patterns/PORTMANTEAU_CONCEPT.md) for cleaner AI interfaces.

## Tool Summary

| Tool | Operations | Use Case |
|------|------------|----------|
| `vdj_deck` | play, pause, toggle, stop, load, seek, volume, status, load_security | Basic deck control |
| `vdj_mixer` | crossfader, sync, eq_high, eq_mid, eq_low, gain, filter | Mixing and EQ |
| `vdj_library` | search, analyze | Library management |
| `vdj_automation` | start, stop, status, suggest, preferences | Auto-DJ |
| `vdj_recording` | start, stop, status, list, export, delete | Recording mixes |
| `vdj_performance` | metrics, stats, trends, recommendations, export | Analytics |
| `vdj_stems` | kill, unkill, volume, acapella, instrumental, isolate_drums, swap, reset | Stem separation |
| `vdj_beatgrid` | set_bpm, tap, adjust, anchor, pitch_bend, pitch_reset, beat_jump, loop, loop_roll, loop_exit | BPM/loops |
| `vdj_skin` | info, load, variation, panel, panel_group, window | UI control |
| `vdj_video` | crossfader, transition, fx, text, output, master, karaoke, scratch, loop, tempo_sync, load | Video mixing |
| `vdj_plex` | search, get_path, load_from_plex, list_libraries | Plex integration |
| `vdj_system` | status, help, connection_test | System status |

## Plex Integration

The new `vdj_plex` tool enables loading tracks directly from Plex Media Server:

```python
# Search Plex
vdj_plex("search", query="ABBA", limit=10)
vdj_plex("search", artist="Pink Floyd")

# Load to deck
vdj_plex("load_from_plex", query="Dancing Queen", deck_id=1)
vdj_plex("load_from_plex", artist="Pink Floyd", deck_id=2)
```

### Configuration

```json
{
  "virtualdj-mcp": {
    "env": {
      "PLEX_SERVER_URL": "http://localhost:32400",
      "PLEX_TOKEN": "your_token"
    }
  }
}
```

## Stem Separation

Real-time vocal/instrumental isolation:

| Stem | Description |
|------|-------------|
| `vocal` | Vocals |
| `instru` | Instrumental |
| `bass` | Bass |
| `drums` | Drums |
| `melody` | Melody/synths |

### Mashup Example

```python
# Load tracks from Plex
vdj_plex("load_from_plex", query="Dancing Queen", deck_id=1)
vdj_plex("load_from_plex", artist="Pink Floyd", deck_id=2)

# Sync BPM
vdj_mixer("sync", deck_a=1, deck_b=2)

# Create mashup: ABBA vocals over Pink Floyd instrumental
vdj_stems("swap", deck_a=1, deck_b=2, stem="vocal")
```

## Tool Mode

Set `VDJ_TOOL_MODE` environment variable:

| Mode | Description | Tool Count |
|------|-------------|------------|
| `portmanteau` | Consolidated tools (default) | 12 |
| `individual` | Original individual tools | 62+ |

## Quick Reference

### Deck Control

```python
vdj_deck("play", deck_id=1)
vdj_deck("load", deck_id=1, track_path="C:/Music/track.mp3")
vdj_deck("volume", deck_id=1, volume=80)
vdj_deck("status", deck_id=1)
```

### Mixing

```python
vdj_mixer("crossfader", position=0)     # Center
vdj_mixer("crossfader", position=-100)  # Full deck A
vdj_mixer("sync", deck_a=1, deck_b=2)
vdj_mixer("eq_low", deck_id=1, value=75)
```

### Stems

```python
vdj_stems("acapella", deck_id=1)        # Vocals only
vdj_stems("instrumental", deck_id=1)    # No vocals
vdj_stems("kill", deck_id=1, stem="bass")
vdj_stems("reset", deck_id=1)           # Restore all
```

### Recording

```python
vdj_recording("start", name="Mix 2024", format="mp3")
vdj_recording("stop")
vdj_recording("list")
```

## Natural Language Examples

With Claude, you can say:

- "Load Dancing Queen to deck 1 and play it"
- "Search Plex for Pink Floyd and load to deck 2"
- "Sync the decks and fade to the center"
- "Put deck 1 in acapella mode"
- "Create a mashup with ABBA vocals over Pink Floyd"
- "Start recording this mix"

## Related Documentation

- [Portmanteau Pattern](../patterns/PORTMANTEAU_CONCEPT.md)
- [Tool Explosion Fix](../patterns/TOOL_EXPLOSION_FIX.md)
- [MCP Portmanteau Best Practices](../patterns/MCP_PORTMANTEAU_BEST_PRACTICES.md)

