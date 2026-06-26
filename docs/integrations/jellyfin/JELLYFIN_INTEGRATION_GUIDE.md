# Jellyfin Integration Guide

**Last Updated:** 2026-05-21  
**Status:** Pre-Implementation  
**Source Repo:** (to be created) `D:\Dev\repos\jellyfin-mcp`

## Overview

This guide covers the complete Jellyfin-MCP integration: server setup, API key acquisition, MCP configuration, webapp deployment, and troubleshooting. Jellyfin-MCP wraps Jellyfin's full OpenAPI/Swagger REST API and WebSocket event stream, exposing 22+ portmanteau tools and a real-time dashboard webapp.

## Table of Contents

1. [Jellyfin Overview](#jellyfin-overview)
2. [Jellyfin vs Plex: Migration Guide](#jellyfin-vs-plex-migration-guide)
3. [Installation and Setup](#installation-and-setup)
4. [Configuration](#configuration)
5. [MCP Tools Reference](#mcp-tools-reference)
6. [WebSocket Real-Time Events](#websocket-real-time-events)
7. [Plugin Management](#plugin-management)
8. [Media Management](#media-management)
9. [Playback Control](#playback-control)
10. [Live TV & DVR](#live-tv--dvr)
11. [Advanced Features](#advanced-features)
12. [Troubleshooting](#troubleshooting)
13. [Legal & Compliance](#legal--compliance)

---

## Jellyfin Overview

### What is Jellyfin?

Jellyfin is the Free Software Media System — an open-source (GPL-2.0) alternative to proprietary media servers like Plex and Emby. Key properties:

- **Zero cost, zero paywalls**: Hardware transcoding, DVR, offline sync all free
- **Plugin architecture**: 100+ community plugins (metadata scanners, intro skip, subtitle downloaders)
- **Real-time WebSocket API**: Push events for playback, sessions, library changes
- **Full OpenAPI/Swagger docs**: Auto-generated, complete, versioned
- **Air-gappable**: No cloud account required, no telemetry, fully self-hosted
- **Cross-platform**: Windows, Linux, macOS, Docker, NAS (Synology, QNAP)
- **51.8k GitHub stars**, 4.8k forks, active development (latest: 10.11.9)

### Jellyfin Architecture

```
Jellyfin Server (C# .NET, port 8096)
├── REST API (HTTP, port 8096)
│   ├── /Items — Media browsing and search
│   ├── /Users — User authentication and management
│   ├── /Library — Library scanning and management
│   ├── /Sessions — Playback session control
│   ├── /Playlists — Playlist CRUD
│   ├── /LiveTv — EPG, recordings, tuners
│   ├── /Plugins — Plugin lifecycle
│   └── /System — Server status, logs, tasks
├── WebSocket (ws://jellyfin:8096/websocket)
│   ├── PlaybackStart / Stop / Progress
│   ├── SessionStarted / Ended
│   ├── LibraryChanged
│   ├── UserDataChanged
│   └── TranscodeProgress
└── Web Client (static HTML5/JS, served from server)
```

---

## Jellyfin vs Plex: Migration Guide

### Why Switch from Plex to Jellyfin?

| Concern | Plex | Jellyfin |
|---------|------|----------|
| **Cost** | HW transcode: $120 lifetime or $5/mo | $0 |
| **Plugins** | Deprecated (2024), removed from ecosystem | 100+ active plugins |
| **Privacy** | Mandatory telemetry, cloud account required | Zero telemetry, local-only |
| **API access** | Semi-documented, some endpoints undocumented | Full OpenAPI/Swagger, auto-generated |
| **Real-time** | Polling only (expensive, high latency) | WebSocket push events |
| **Offline** | Requires internet for auth | Fully air-gappable |
| **Ads** | Yes (Plex Movies & TV, cannot fully disable) | No |

### Migration Path

1. **Install Jellyfin** alongside Plex (different port, no conflict)
2. **Export Plex data** via plex-mcp `plex_integration(operation="export")` 
3. **Import into Jellyfin** via jellyfin-mcp `jellyfin_integration(operation="import_plex")`
4. **Sync watch states** via `jellyfin_integration(operation="sync_watchstate")`
5. **Verify** all media detected, metadata correct
6. **Decommission Plex** when satisfied

### Migration Checklist

- [ ] Media files accessible from both servers
- [ ] Jellyfin libraries configured (Movies, TV, Music, etc.)
- [ ] Metadata providers configured (TMDB, TVDB, MusicBrainz)
- [ ] Hardware transcoding tested (Intel QSV, NVENC, VAAPI)
- [ ] Client apps installed (Android, iOS, Roku, WebOS, etc.)
- [ ] Plugins configured (intro skip, subtitle downloaders, theme songs)
- [ ] Watch history migrated
- [ ] User accounts recreated
- [ ] External access configured (reverse proxy, Tailscale)

---

## Installation and Setup

### Prerequisites

- **Python 3.12+**: Required for jellyfin-mcp
- **Jellyfin Server**: Installed and running (port 8096)
- **Jellyfin API Key**: Required for API access
- **Network Access**: Server must be reachable from MCP host

### Jellyfin Server Installation

#### Windows
```powershell
# Download from https://jellyfin.org/downloads/windows
# Run installer with default settings
# Jellyfin runs as a Windows service, port 8096
```

#### Linux (Debian/Ubuntu)
```bash
curl https://repo.jellyfin.org/install-debuntu.sh | sudo bash
# Or Docker:
docker run -d \
  --name jellyfin \
  -p 8096:8096 \
  -v /path/to/config:/config \
  -v /path/to/media:/media \
  jellyfin/jellyfin:latest
```

#### macOS
```bash
brew install --cask jellyfin
```

#### Docker Compose
```yaml
version: '3.8'
services:
  jellyfin:
    image: jellyfin/jellyfin:latest
    container_name: jellyfin
    ports:
      - "8096:8096"
    volumes:
      - ./config:/config
      - ./cache:/cache
      - /mnt/media:/media:ro
    restart: unless-stopped
```

### Getting Your Jellyfin API Key

Unlike Plex, Jellyfin provides a straightforward API key management interface:

**Method 1: Web UI**
1. Open Jellyfin: `http://your-server:8096`
2. Navigate to **Dashboard → Users**
3. Click on your user
4. Go to **API Keys** tab
5. Click **Create Key**, give it a name (e.g. "mcp-server")
6. Copy the generated key

**Method 2: API Authentication**
```bash
# Authenticate and get access token
curl -X POST "http://localhost:8096/Users/AuthenticateByName" \
  -H "Content-Type: application/json" \
  -H 'X-Emby-Authorization: MediaBrowser Client="jellyfin-mcp", Device="server", DeviceId="mcp-001", Version="1.0.0"' \
  -d '{"Username": "your-username", "Pw": "your-password"}'

# Response contains:
# {
#   "User": { "Id": "...", "Name": "..." },
#   "AccessToken": "your-api-key-here"
# }

# Create API Key (more permanent than AccessToken)
curl -X POST "http://localhost:8096/Auth/Keys" \
  -H "X-Emby-Token: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"App": "jellyfin-mcp"}'
```

### jellyfin-mcp Installation

```powershell
# Clone repository (URL TBD)
cd D:\Dev\repos
git clone https://github.com/sandraschi/jellyfin-mcp.git
cd jellyfin-mcp

# Install dependencies
uv sync
# Or: pip install -e ".[dev]"
```

---

## Configuration

### Environment Variables

```powershell
# Required
$env:JELLYFIN_URL = "http://localhost:8096"
$env:JELLYFIN_API_KEY = "your-api-key-here"

# Optional
$env:JELLYFIN_MCP_TRANSPORT = "stdio"    # stdio, http, sse, ws
$env:JELLYFIN_MCP_PORT = "10934"         # HTTP/SSE/WS port
$env:JELLYFIN_SAMPLING_BASE_URL = "http://127.0.0.1:11434/v1"
$env:JELLYFIN_SAMPLING_MODEL = "llama3.2"
$env:PYTHONUNBUFFERED = "1"
```

### Claude Desktop Configuration (`mcp.json`)

```json
{
  "jellyfin-mcp": {
    "command": "python",
    "args": ["-m", "jellyfin_mcp", "--stdio"],
    "cwd": "D:/Dev/repos/jellyfin-mcp",
    "env": {
      "JELLYFIN_URL": "http://localhost:8096",
      "JELLYFIN_API_KEY": "YOUR_API_KEY_HERE",
      "PYTHONPATH": "D:/Dev/repos/jellyfin-mcp/src",
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

### `.env` File

```bash
# jellyfin-mcp/.env
JELLYFIN_URL=http://localhost:8096
JELLYFIN_API_KEY=your-api-key-here
JELLYFIN_SAMPLING_BASE_URL=http://127.0.0.1:11434/v1
JELLYFIN_SAMPLING_MODEL=llama3.2
```

---

## MCP Tools Reference

### Core Media Tools

#### `jellyfin_library` (15 operations)
| Operation | Description | Args |
|-----------|-------------|------|
| `list` | List all media libraries | — |
| `get` | Get library details | `library_id` |
| `scan` | Trigger library scan | `library_id` |
| `refresh` | Refresh metadata for library | `library_id`, `force` |
| `create` | Create new library | `name`, `type`, `paths` |
| `update` | Update library settings | `library_id`, `settings` |
| `delete` | Delete library | `library_id` |
| `stats` | Library statistics | `library_id` |
| `cleanup` | Remove missing items | `library_id` |

#### `jellyfin_media` (10 operations)
| Operation | Description | Args |
|-----------|-------------|------|
| `browse` | Browse library contents | `library_id`, `filters`, `sort` |
| `search` | Search media items | `query`, `types` |
| `get` | Get item details | `item_id` |
| `get_recent` | Recently added items | `library_id`, `limit` |
| `get_recommended` | Recommended for user | `user_id` |
| `update` | Update item metadata | `item_id`, `metadata` |
| `delete` | Delete item | `item_id` |
| `stream_info` | Get stream/codec info | `item_id` |
| `similar` | Find similar items | `item_id`, `limit` |
| `refresh` | Refresh single item | `item_id`, `mode` |

#### `jellyfin_search` (6 operations)
| Operation | Description |
|-----------|-------------|
| `search` | Full text search across libraries |
| `advanced` | Advanced filter search (genre, year, rating, resolution) |
| `people` | Search by actor/director/writer |
| `studios` | Search by studio/network |
| `suggest` | Auto-complete suggestions |
| `saved` | View saved search history |

### Playback Control Tools

#### `jellyfin_playback` (12 operations)
| Operation | Description |
|-----------|-------------|
| `list_sessions` | Active playback sessions |
| `play` | Start playback on device |
| `pause` | Pause session |
| `stop` | Stop session |
| `seek` | Seek to position (ticks) |
| `skip_next` | Next track/episode |
| `skip_prev` | Previous track/episode |
| `set_volume` | Set session volume |
| `set_subtitle` | Change subtitle track |
| `set_audio` | Change audio track |
| `set_quality` | Set transcode quality |
| `report` | Report playback progress |

#### `jellyfin_streaming` (8 operations)
| Operation | Description |
|-----------|-------------|
| `sessions` | All active sessions with stream details |
| `clients` | Registered playback clients |
| `transcode` | Current transcode jobs |
| `bandwidth` | Per-session bandwidth |
| `direct_play` | Direct play status (no transcode) |
| `remote` | Remote streaming sessions |
| `lan` | LAN streaming sessions |
| `kill` | Terminate session |

### Plugin Tools (Unique to Jellyfin)

#### `jellyfin_plugin` (8 operations)
| Operation | Description |
|-----------|-------------|
| `catalog` | List available plugins from manifest |
| `list` | List installed plugins |
| `install` | Install plugin by ID |
| `uninstall` | Uninstall plugin |
| `enable` | Enable plugin |
| `disable` | Disable plugin |
| `configure` | Get/set plugin configuration |
| `update` | Update plugin to latest |

### Server Management

#### `jellyfin_server` (10 operations)
| Operation | Description |
|-----------|-------------|
| `status` | Server health + uptime |
| `info` | Version, OS, hardware info |
| `health` | Health check results |
| `logs` | Fetch server logs |
| `restart` | Restart Jellyfin |
| `shutdown` | Shutdown Jellyfin |
| `updates` | Check for Jellyfin updates |
| `tasks` | Scheduled task status |
| `transcode_queue` | Current transcode queue |
| `plugins_list` | Installed plugin list |

### Agentic Tools

#### `jellyfin_agentic` (3 operations)
| Operation | Description |
|-----------|-------------|
| `workflow` | Multi-step workflow via FastMCP `sample_step` |
| `natural_query` | Natural language media query (uses sampling) |
| `batch` | Batch operation across multiple items |

---

## WebSocket Real-Time Events

### Architecture

```
Jellyfin Server ←→ WebSocketService ←→ Internal Event Bus ←→ Webapp WS Proxy
     :8096              (aiohttp)           (asyncio.Queue)        :10934/ws
```

### Event Types

| Event | Payload | Webapp Use |
|-------|---------|------------|
| `PlaybackStart` | Item, user, device, stream info | Live session list |
| `PlaybackStop` | Item, user, position | Remove from session list |
| `PlaybackProgress` | Ticks, position | Progress bars in dashboard |
| `SessionStarted` | Session info | New session notification |
| `SessionEnded` | Session ID | Remove session |
| `LibraryChanged` | Library ID, items added/removed | Update library stats |
| `UserDataChanged` | User, item, played status | Update watch indicators |
| `TranscodeProgress` | Job ID, progress, FPS | Transcode queue display |

### Subscribing from Webapp

```typescript
const ws = new WebSocket('ws://localhost:10934/ws');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  switch (data.event) {
    case 'PlaybackStart':
      // Update active sessions
      break;
    case 'TranscodeProgress':
      // Update transcode progress bar
      break;
  }
};
```

---

## Plugin Management

### Top Jellyfin Plugins (First-Class MCP Support)

| Plugin | ID | Purpose | Category |
|--------|-----|---------|----------|
| Intro Skipper | `intro-skipper` | Auto-detect and skip intros | Media Enhancement |
| Subtitle Extract | `subtitle-extract` | Extract embedded subtitles | Subtitles |
| Open Subtitles | `opensubtitles` | Download subtitles from OpenSubtitles | Subtitles |
| Theme Songs | `theme-songs` | Download and play theme songs | Media Enhancement |
| LDAP Auth | `ldap-auth` | LDAP/Active Directory authentication | Auth |
| Reports | `reports` | Generate media library reports | Reporting |
| Merge Versions | `merge-versions` | Auto-merge multiple versions of same movie | Organization |
| Trakt | `trakt` | Scrobble to Trakt.tv | Integration |
| AniDB | `anidb` | Anime metadata from AniDB | Metadata |
| TMDb Box Sets | `tmdb-box-sets` | Auto-create collections from TMDb | Collections |

### Plugin Lifecycle via MCP

```
Install:  jellyfin_plugin("install", plugin_id="intro-skipper")
           → PluginService downloads .dll → copies to plugins dir
           → Triggers jellyfin_server("restart")
           
Configure: jellyfin_plugin("configure", plugin_id="intro-skipper", config={...})
           → Updates plugin XML config
           
Enable:   jellyfin_plugin("enable", plugin_id="intro-skipper")
Disable:  jellyfin_plugin("disable", plugin_id="intro-skipper")
Uninstall: jellyfin_plugin("uninstall", plugin_id="intro-skipper")
```

---

## Media Management

### Library Organization Best Practices

```
/media/
├── movies/              → Jellyfin Library: "Movies" (type: Movie)
│   ├── Inception (2010)/
│   │   └── Inception.2010.1080p.mkv
│   └── The Matrix (1999)/
│       └── The.Matrix.1999.4K.mkv
├── tv/                  → Jellyfin Library: "TV Shows" (type: Series)
│   ├── Breaking Bad/
│   │   ├── Season 1/
│   │   │   ├── S01E01.mkv
│   │   │   └── S01E02.mkv
│   │   └── Season 2/
│   └── The Office/
├── music/               → Jellyfin Library: "Music" (type: Music)
│   ├── Artist/
│   │   └── Album/
│   │       └── 01 - Track.flac
├── photos/              → Jellyfin Library: "Photos" (type: Photos)
├── home-videos/         → Jellyfin Library: "Home Videos" (type: HomeVideos)
└── recordings/          → Jellyfin Library: "Recordings" (DVR output)
```

### Metadata Providers (Priority Order)

```
Movies:
  1. TMDb (The Movie Database) — preferred
  2. OMDb (Open Movie Database)
  3. TVDb (The TV Database) — fallback

TV Shows:
  1. TMDb — preferred
  2. TVDb — fallback

Music:
  1. MusicBrainz — preferred
  2. TheAudioDB — fallback
  3. Discogs — for album art only
```

---

## Playback Control

### Transcoding Architecture

```
Media File → Jellyfin Server → FFmpeg Transcode → Stream → Client
                │
                ├── Direct Play (no transcode, if compatible)
                ├── Direct Stream (remux container only)
                └── Full Transcode (video + audio)
```

### Hardware Acceleration (Free on Jellyfin!)

| Platform | API | jf Argument |
|----------|-----|-------------|
| Intel | Quick Sync (QSV) | `--hwaccel=qsv` |
| NVIDIA | NVENC/NVDEC | `--hwaccel=cuda` |
| AMD | AMF/VCE | `--hwaccel=vaapi` (Linux) |
| Apple | VideoToolbox | `--hwaccel=videotoolbox` |
| Raspberry Pi | V4L2-M2M | `--hwaccel=rkmpp` |

---

## Live TV & DVR

### Tuner Support

| Tuner Type | Setup | Features |
|------------|-------|----------|
| HDHomeRun | Auto-discovered via UDP | Multi-tuner, EPG built-in |
| IPTV (M3U) | M3U playlist URL | Any IPTV provider |
| XML TV | EPG XML URL | Guide data |
| TVHeadend | TVHeadend server URL | Advanced DVR features |

### MCP Commands

```
# List channels
jellyfin_livetv("channels")

# View guide
jellyfin_livetv("guide", start_time="2026-05-21T18:00:00Z")

# Schedule recording
jellyfin_livetv("schedule", channel_id="...", start="...", end="...")

# List recordings
jellyfin_livetv("recordings", status="completed")
```

---

## Advanced Features

### RAG Semantic Search

```python
# Index Jellyfin metadata
jellyfin_rag("sync")

# Semantic search
jellyfin_rag("search", query="dark sci-fi with strong female lead")

# Check index status
jellyfin_rag("status")
```

### Media Enrichment

```python
# Enrich single item from TMDB/Wikipedia
jellyfin_enrichment("tmdb", item_id="abc123")

# Batch enrich library
jellyfin_enrichment("batch", library_id="movies", sources=["tmdb", "wikipedia"])
```

### Arr Stack Integration

```python
# Check Radarr/Sonarr/Lidarr status
jellyfin_arr_stack("status")

# View download queue
jellyfin_arr_stack("queue")

# Trigger library sync after download
jellyfin_arr_stack("sync", library_id="movies")
```

---

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| **Authentication failed** | Wrong API key or expired | Generate new key in Dashboard → Users → API Keys |
| **Connection refused** | Jellyfin not running or wrong URL | Verify `http://localhost:8096` accessible |
| **Tool returns empty** | API key user lacks permissions | Check user has "Allow media playback" checked |
| **WebSocket disconnect** | Firewall or reverse proxy | WebSocket needs `/websocket` path proxied |
| **Plugin install fails** | Plugin directory not writable | Check permissions on `plugins/` dir |
| **Transcode not using GPU** | HW acceleration not configured | Verify ffmpeg path and GPU drivers |
| **Slow search** | No search index | Wait for initial library scan to complete |

### Debug Mode

```powershell
# Enable verbose logging
$env:JELLYFIN_MCP_LOG_LEVEL = "DEBUG"
$env:PYTHONUNBUFFERED = "1"
python -m jellyfin_mcp --stdio
```

### Health Check

```powershell
# Verify Jellyfin server is accessible
curl http://localhost:8096/System/Info

# Verify MCP server health
curl http://localhost:10934/health

# List all registered tools
curl http://localhost:10934/mcp/tools
```

---

## Legal & Compliance

### SCOTUS Cox Ruling (2025) & Media Server Legality

The Supreme Court's ruling in *Sony Music Entertainment v. Cox Communications* (2025) has significant implications for self-hosted media servers:

**What the ruling says:**
- ISPs can be held liable for contributory copyright infringement when they **knowingly profit** from subscriber piracy and **refuse to terminate** repeat infringers
- The Court explicitly **reaffirmed** the Betamax doctrine (*Sony v. Universal*, 1984): a technology with "substantial non-infringing uses" is not an infringing tool

**What this means for Jellyfin users:**
1. Jellyfin is unequivocally protected under the Betamax doctrine — streaming your own DVDs, home videos, and CC-licensed content is substantial non-infringing use
2. Jellyfin has **no profit motive** around infringement — unlike Plex, it has no commercial streaming arm, no user monetization, no data collection
3. The Cox ruling targets **conduct** (ignoring infringement to keep subscription revenue), not **tools** (media servers)

**Plex's legal position vs Jellyfin's:**
- Plex operates a commercial streaming service (Plex Movies & TV, TIDAL integration, Plex Arcade) alongside the media server — this is a hybrid model where commercial content provides a figleaf of legitimacy
- Jellyfin has **zero commercial content, zero telemetry, zero cloud dependency** — it is the purest expression of the Betamax doctrine
- The Cox ruling makes Plex's "commercial content shield" unnecessary — the tool itself is protected regardless of whether it also hosts commercial content

### Best Practices for Compliance

- **Don't share your server publicly** — Jellyfin's sharing features are for household/family use
- **Use HTTPS** with a valid certificate when accessing remotely
- **Document your legitimate media sources** — keep receipts for DVDs/Blu-rays you've ripped
- **Don't sell access** — charging for Jellyfin access is the kind of "profiting from infringement" the Cox ruling targets
- **Jellyfin collects nothing** — no server-side analytics, no user tracking, no cloud dependency. Your watch history stays on your hardware.

### GPL-2.0 License Considerations

Jellyfin is licensed under GPL-2.0. The jellyfin-mcp server is a **separate process** that communicates via HTTP/WebSocket — it is not a derivative work of Jellyfin. The MCP server's Python source code can use any license without GPL obligations. Only modifications to Jellyfin's C# source code would trigger GPL requirements.

---

## Appendix: Jellyfin API Quick Reference

### Common Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/System/Info` | GET | Server info |
| `/System/Ping` | POST | Health check |
| `/Users/AuthenticateByName` | POST | Username/password auth |
| `/Users/{userId}` | GET/DELETE | User management |
| `/Items` | GET | Browse/search items |
| `/Items/{itemId}` | GET/POST/DELETE | Item CRUD |
| `/Items/{itemId}/PlaybackInfo` | POST | Get stream URLs |
| `/Library/VirtualFolders` | GET/POST | Library management |
| `/Library/Refresh` | POST | Trigger scan |
| `/Sessions` | GET | Active sessions |
| `/Sessions/{sessionId}/Playing` | POST | Playback control |
| `/Sessions/{sessionId}/Command` | POST | Send command to session |
| `/Playlists` | GET/POST | Playlist management |
| `/LiveTv/Channels` | GET | Channel list |
| `/LiveTv/Recordings` | GET | DVR recordings |
| `/Plugins` | GET | Plugin management |
| `/ScheduledTasks` | GET | Task management |
| `/Devices` | GET | Registered devices |

### Authorization Header Format

```
X-Emby-Token: {api_key}
```

Or in the authorization header (Jellyfin custom):
```
MediaBrowser Client="{app_name}", Device="{device}", DeviceId="{device_id}", Version="{version}", Token="{api_key}"
```

---

*Last updated: 2026-05-21 — Pre-implementation phase*
