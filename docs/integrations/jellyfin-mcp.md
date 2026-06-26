# Jellyfin MCP Integration

## Overview

jellyfin-mcp is a FastMCP 3.2+ server for Jellyfin Media Server — the open-source alternative to Plex. It provides stdio (Claude Desktop) tools, a **React webapp** (Next.js 15 + FastAPI) for browsing libraries, media with Jellyfin artwork, live playback/transcode monitoring (WebSocket), plugin management, Live TV EPG, semantic (RAG) search, and chat with local LLM.

**Status:** Pre-Implementation | **Framework:** FastMCP 3.2+ | **Webapp ports:** Backend 10934, frontend 10935

## Why Jellyfin Over Plex

| Feature | Plex | Jellyfin |
|---------|------|----------|
| License | Proprietary (freemium) | **GPL-2.0 (fully free)** |
| Hardware transcoding | Plex Pass ($120/lifetime) | **Free** |
| DVR / Live TV | Plex Pass | **Free** |
| Intro/credit skip | Plex Pass | **Free (plugin)** |
| Plugins | Deprecated | **100+ plugins** |
| Real-time API | Polling only | **WebSocket events** |
| API documentation | Partial | **Full OpenAPI/Swagger** |
| Cloud dependency | plex.tv required | **Fully air-gappable** |
| Telemetry | Mandatory | **None** |

## Capabilities

- **MCP tools**: 22 portmanteau tools covering libraries, media (browse/search), playback control, users, playlists, collections, metadata, server management, **plugin management**, **Live TV/DVR**, **subtitle management**, FFmpeg transcoding, media enrichment (TMDB/Wikipedia), RAG semantic search, arr-stack integration
- **WebSocket live dashboard**: Real-time playback sessions, transcode queue, bandwidth monitor — no polling
- **Plugin management UI**: Install, configure, enable/disable Jellyfin plugins from the webapp
- **Webapp**:
  - **Media browser**: Poster grid with Jellyfin artwork, detail modal (metadata, cast, similar, Play button)
  - **Playback dashboard**: Live sessions, transcode status, bandwidth usage (WebSocket, real-time)
  - **EPG grid**: Live TV guide with recording management (unique to Jellyfin)
  - **Plugin catalog**: Browse, install, configure plugins
  - **Semantic search**: RAG over Jellyfin metadata (movies/shows/music)
  - Overiew, Libraries, Search, Users, Settings, Chat, RAG, Help
- **Plex migration**: Import/export tools for switching from Plex to Jellyfin

## Getting Your Jellyfin API Key

Unlike Plex's obscure token extraction:

1. Open Jellyfin Web: `http://your-server:8096`
2. Navigate to: **Dashboard → Users → (your user) → API Keys**
3. Click **Create Key**, copy the token

Or via API:
```bash
curl -X POST "http://localhost:8096/Users/AuthenticateByName" \
  -H "Content-Type: application/json" \
  -H 'X-Emby-Authorization: MediaBrowser Client="mcp", Device="server", DeviceId="mcp-001", Version="1.0"' \
  -d '{"Username": "your-user", "Pw": "your-password"}'
# Returns User ID + AccessToken
```

## Claude Desktop Configuration

```json
{
  "jellyfin-mcp": {
    "command": "python",
    "args": ["-m", "jellyfin_mcp", "--stdio"],
    "cwd": "D:/Dev/repos/jellyfin-mcp",
    "env": {
      "JELLYFIN_URL": "http://localhost:8096",
      "JELLYFIN_API_KEY": "your-api-key-here",
      "PYTHONPATH": "D:/Dev/repos/jellyfin-mcp/src",
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `JELLYFIN_URL` | Yes | `http://localhost:8096` | Jellyfin server URL |
| `JELLYFIN_API_KEY` | Yes | — | Jellyfin API key |
| `JELLYFIN_MCP_TRANSPORT` | No | `stdio` | `stdio`, `http`, `sse`, or `ws` |
| `JELLYFIN_MCP_PORT` | No | `10934` | HTTP/SSE/WS port |
| `JELLYFIN_SAMPLING_BASE_URL` | No | `http://127.0.0.1:11434/v1` | LLM endpoint for agentic tools |
| `JELLYFIN_SAMPLING_MODEL` | No | `llama3.2` | Model for sampling |

## Webapp Quickstart

```powershell
# From jellyfin-mcp repo root
cd webapp
.\start.ps1
# Opens browser at http://localhost:10935
# Backend at http://localhost:10934
```

## References

- [Jellyfin API Documentation](https://api.jellyfin.org)
- [Jellyfin GitHub](https://github.com/jellyfin/jellyfin) (51.8k stars)
- [Jellyfin Plugin Catalog](https://github.com/jellyfin/jellyfin-plugin-manifest)
- [MCP Central — WEBAPP_PORTS](../operations/WEBAPP_PORTS.md)
- [jellyfin-mcp PRD](../projects/jellyfin-mcp/PRD.md)
- [jellyfin-mcp Architecture](../projects/jellyfin-mcp/ARCHITECTURE.md)

---

*Last updated: 2026-05-21 — Pre-implementation phase*
