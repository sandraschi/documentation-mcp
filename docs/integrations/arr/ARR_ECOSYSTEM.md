# The *Arr Ecosystem Integration

**Status:** Active Deployment  
**Stack Location:** `D:\Dev\repos\media-stack`  

> "Arr, matey! Welcome to the high seas of media automation!" 🏴‍☠️

## Overview

The *Arr ecosystem is a collection of "Personal Video Recorder" (PVR) applications that automate the monitoring, downloading, and organization of media files. They serve as the supply chain for your Plex Media Server, ensuring your libraries remain stocked with the finest booty (content).

While Plex acts as the **Display/Playback** layer (the "Treasure Chest"), the *Arrs act as the **Logistics** layer (the "Crew").

## Key Components (The Crew)

### 📺 Sonarr (TV Shows)
The quartermaster for television.
- **Port**: `8989`
- **Role**: Monitors RSS feeds for new episodes, grabs releases, and renames/moves them to your library.
- **Key Feature**: Automatic quality upgrading (e.g., replace HDTV with WebDL).

### 🎬 Radarr (Movies)
The quartermaster for moving pictures.
- **Port**: `7878`
- **Role**: Same as Sonarr, but for movies. Handles complex release windows (Theatrical -> Digital -> BluRay).

### 🎵 Lidarr (Music)
The bandmaster.
- **Port**: `8686`
- **Role**: Automates music downloads. Supports album/artist monitoring and metadata tagging.

### 🔎 Prowlarr (Indexers)
The navigator.
- **Port**: `9696`
- **Role**: Manages your indexers (trackers). You configure your trackers *once* here, and Prowlarr syncs them to Sonarr, Radarr, and Lidarr automatically.
- **Benefit**: No more copy-pasting API keys to 5 different apps!

### 💬 Bazarr (Subtitles)
The translator.
- **Port**: `6767`
- **Role**: Scans your library for missing subtitles and grabs them from providers (OpenSubtitles, etc.).

### 📥 qBittorrent (Download Client)
The ship.
- **Port**: `8181` (WebUI)
- **Role**: The workhorse that actually pulls the bits from the ether.
- **Integration**: Controlled entirely by the *Arrs. You rarely need to touch this directly.

## Infrastructure & Deployment

### "Scattered Media" Architecture
Unlike a standard "monolithic" volume, this stack is configured to respect the Sandra-standard multi-drive layout across Vienna:

- **Drive D:** `D:\Multimedia Files` -> Mounted as `/data/d/Multimedia Files`
- **Drive E:** `E:\Video` -> Mounted as `/data/e/Video`
- **Drive F:** `F:\Comedy` -> Mounted as `/data/f/Comedy`

This allows the *Arrs to "see" all potential storage locations without requiring a massive data migration (reorganization is strictly forbidden by the Captain).

### Docker Stack
The stack runs in `media-stack` independently of Homarr or Plex, but feeds into the same file systems they read.

```yaml
# Service Ports Quick Reference
Sonarr: 8989
Radarr: 7878
Lidarr: 8686
Prowlarr: 9696
Bazarr: 6767
qBittorrent: 8181
```

## Integration with Plex
The workflow is unidirectional:
1. **Prowlarr** finds the map (indexer).
2. **Sonarr/Radarr** orders the raid (sends download to qBit).
3. **qBittorrent** captures the prize (downloads file).
4. **Sonarr/Radarr** brings it aboard (imports to `D:\Multimedia Files\...`).
5. **Plex** sees the change (via file monitor) and displays the treasure!

## Future: MCP Integration
Currently, the *Arrs are treated as "dumb" services by our AI layer—we configure them via web UI.
**Vision**: Create `radarr-mcp`, `sonarr-mcp`, etc., to allow AI agents to:
- "Find and add this movie"
- "Audit my quality profiles"
- "Check why this download is stalled"

*Arr! Let the automation begin!* 🦜
