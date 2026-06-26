# Plex Integration Guide

**Last Updated:** 2025-12-02  
**Status:** Active Development / Beta  
**Source Repo:** `D:\Dev\repos\plex-mcp`

## Overview

PlexMCP provides comprehensive integration with Plex Media Server. This guide covers all aspects of Plex integration, from basic setup to advanced features and troubleshooting.

## Table of Contents

1. [Plex Overview](#plex-overview)
2. [Installation and Setup](#installation-and-setup)
3. [Configuration](#configuration)
4. [MCP Tools](#mcp-tools)
5. [Media Management](#media-management)
6. [Playback Control](#playback-control)
7. [Client Integration](#client-integration)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

## Plex Overview

### What is Plex?

Plex Media Server is a powerful media management platform that provides:

- **Media Organization**: Organize movies, TV shows, music, photos, and more
- **Streaming**: Stream media to any device
- **Metadata Management**: Automatic metadata fetching and organization
- **Multi-user Support**: User management and sharing
- **Remote Access**: Access your media library from anywhere

### Key Features

- **Multi-format Support**: Movies, TV shows, music, photos, podcasts
- **Automatic Metadata**: Fetches artwork, descriptions, and metadata
- **Transcoding**: On-the-fly media conversion
- **Client Apps**: Available on all major platforms
- **Web Interface**: Browser-based access

## Installation and Setup

### Prerequisites

- **Python 3.11+**: Required for PlexMCP
- **Plex Media Server**: Installed and running
- **Plex Authentication Token**: Required for API access
- **Network Access**: Server must be accessible

### Plex Media Server Installation

#### Windows
```powershell
# Download from https://www.plex.tv/media-server-downloads/
# Run installer with default settings
```

#### macOS
```bash
# Download from https://www.plex.tv/media-server-downloads/
# Or use Homebrew
brew install --cask plex-media-server
```

#### Linux
```bash
# Ubuntu/Debian
wget -O plex.deb https://downloads.plex.tv/plex-media-server-new/1.32.8.7639-fb6452ebf/debian/plexmediaserver_1.32.8.7639-fb6452ebf_amd64.deb
sudo dpkg -i plex.deb

# Or use official repository
```

### Getting Your Plex Token

1. **Via Web Interface**:
   - Open Plex Web: `http://your-server:32400/web`
   - Open browser developer tools (F12)
   - Go to Network tab
   - Look for requests to `plex.tv` or your server
   - Find `X-Plex-Token` in request headers

2. **Via Plex.tv**:
   - Visit: https://plex.tv/pms/servers
   - View page source
   - Search for `token`
   - Copy the token value

### PlexMCP Installation

```powershell
# Clone repository
cd D:\Dev\repos
git clone https://github.com/sandraschi/plex-mcp.git
cd plex-mcp

# Install dependencies
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

```powershell
# Required
$env:PLEX_URL = "http://192.168.0.81:32400"
$env:PLEX_TOKEN = "your-plex-token-here"

# Optional
$env:PYTHONUNBUFFERED = "1"
```

### MCP Configuration (`mcp.json`)

```json
{
  "plex-mcp": {
    "command": "python",
    "args": ["-m", "plex_mcp", "--stdio"],
    "cwd": "D:/Dev/repos/plex-mcp",
    "env": {
      "PLEX_URL": "http://192.168.0.81:32400",
      "PLEX_TOKEN": "YOUR_TOKEN_HERE",
      "PYTHONPATH": "D:/Dev/repos/plex-mcp/src",
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

## MCP Tools

PlexMCP uses the **portmanteau pattern** with 15 comprehensive tools:

### Core Tools

| Tool | Operations | Description |
|------|------------|-------------|
| `plex_library` | 12 | Library management (list, scan, refresh, optimize) |
| `plex_media` | 5 | Browse, search, get details, recent items |
| `plex_search` | 5 | Basic search, advanced search, suggestions, history |
| `plex_streaming` | 10 | Sessions, clients, play, pause, stop, seek, skip |
| `plex_user` | 6 | User management and permissions |
| `plex_playlist` | 8 | Playlist CRUD and analytics |
| `plex_collections` | 7 | Collection management |
| `plex_metadata` | 7 | Metadata refresh, fix match, analyze |
| `plex_organization` | 5 | Library organization and cleanup |
| `plex_performance` | 12 | Transcoding, bandwidth, quality profiles |
| `plex_reporting` | 6 | Library stats, usage reports |
| `plex_quality` | 6 | Quality profile management |
| `plex_server` | 6 | Server status, health, maintenance |
| `plex_integration` | 6 | Third-party integrations |
| `plex_help` | 4 | Help and discovery |

**Total: 15 portmanteau tools, 100+ operations**

## Media Management

### Library Operations

```python
# List all libraries
plex_library(operation="list")

# Scan library for new content
plex_library(operation="scan", library_name="Movies")

# Refresh library metadata
plex_library(operation="refresh", library_name="TV Shows")
```

### Search Operations

```python
# Basic search
plex_search(operation="basic", query="The Matrix")

# Advanced search with filters
plex_search(
    operation="advanced",
    query="sci-fi",
    year="1999",
    library="Movies"
)

# Search plot summaries
plex_search(
    operation="advanced",
    summary_contains="time travel"
)
```

## Playback Control

### Session Management

```python
# List active sessions
plex_streaming(operation="get_sessions")

# List available clients
plex_streaming(operation="get_clients")
```

### Playback Commands

```python
# Play media on client
plex_streaming(
    operation="play",
    client_name="Plexamp",
    media_key="/library/metadata/12345"
)

# Pause playback
plex_streaming(operation="pause", session_key="abc123")

# Stop playback
plex_streaming(operation="stop", session_key="abc123")
```

## Client Integration

### Supported Clients

| Client | Status | Notes |
|--------|--------|-------|
| Plexamp | âœ… Full | Play, pause, stop via server:// URI |
| Plex Web | âš ï¸ Read-only | Sessions visible, no remote control |
| VLC | âœ… Full | Via HTTP streaming URL |
| Native Apps | ðŸ”„ Untested | Should work with remote control enabled |

### Plexamp Integration

Plexamp requires the `server://` URI format for playback:

```
server://{serverMachineId}/com.plexapp.plugins.library/library/metadata/{trackKey}
```

### VLC Integration

VLC can play media via HTTP streaming URLs:

```python
# Get streaming URL
plex_streaming(operation="get_stream_url", media_key="/library/metadata/12345")

# Open in VLC
# Use the returned HTTP URL
```

## Advanced Features

### Metadata Management

```python
# Refresh metadata for item
plex_metadata(operation="refresh", media_key="/library/metadata/12345")

# Fix match
plex_metadata(operation="fix_match", media_key="/library/metadata/12345")

# Analyze media
plex_metadata(operation="analyze", media_key="/library/metadata/12345")
```

### Performance Monitoring

```python
# Get transcoding sessions
plex_performance(operation="get_transcoding_sessions")

# Get bandwidth usage
plex_performance(operation="get_bandwidth_usage")
```

### Media Enrichment & RAG Augmentation (v2.4.1)

PlexMCP supports high-value media enrichment by fetching deep contextual summaries from external sources like Wikipedia.

#### 1. Standalone Enrichment
Fetch on-demand narrative context for any movie or show:
```python
plex_media_enrichment(
    operation="enrich_item",
    title="Inception",
    year=2010
)
```

#### 2. RAG Augmentation
Deepen your local semantic search index by enabling enrichment during sync:
```python
plex_rag(operation="sync_metadata", enrich=True)
```
This appends Wikipedia narrative data to the vector index, significantly improving accuracy for thematic and historical discovery.

For more details, see the [Enrichment Guide](https://github.com/sandraschi/plex-mcp/blob/main/docs/ENRICHMENT.md).

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Verify Plex server is running
   - Check firewall settings
   - Verify URL and port (default: 32400)

2. **Authentication Failed**
   - Verify PLEX_TOKEN is correct
   - Token may have expired (regenerate if needed)
   - Check token has proper permissions

3. **Client Not Found**
   - Ensure client is connected to server
   - Check client name matches exactly
   - Verify remote control is enabled

4. **Playback Not Working**
   - Check client supports remote control
   - Verify media is accessible
   - Check network connectivity

## Best Practices

1. **Token Security**
   - Store tokens in environment variables
   - Never commit tokens to version control
   - Rotate tokens periodically

2. **Performance**
   - Use specific library names when possible
   - Limit search results with appropriate limits
   - Cache frequently accessed data

3. **Error Handling**
   - Always check operation results
   - Handle network timeouts gracefully
   - Log errors for debugging

4. **Client Management**
   - Verify client is available before playback
   - Handle client disconnections gracefully
   - Use session keys for reliable control

## Plex Plus (MyAI Platform)

### Overview

**Plex Plus** is an AI-enhanced Plex companion application that runs as part of the MyAI platform. It provides a web-based interface with advanced AI features for Plex media management.

**Location:** `D:\Dev\repos\myai\projects\plex_plus`

### Key Features

- **Semantic Media Search**: ChromaDB-powered vector embeddings for natural language queries
- **Advanced Search & Filtering**: 20+ filter types (genre, year, actor, director, rating, etc.)
- **Video Streaming**: HLS support for remote devices (iPad, mobile)
- **AI Metadata Enrichment**: AI-generated summaries, genres, tags, and content warnings
- **Metadata Editing**: Update titles, summaries, genres, match fixes
- **Playlist Management**: Full CRUD operations for playlists
- **Collection Management**: Organize media into collections
- **Watch Status & Ratings**: Track viewing progress and ratings
- **Subtitle Support**: List and enable subtitles during playback

### Architecture

```
projects/plex_plus/
â”œâ”€â”€ backend/          # FastAPI REST API (port 6221)
â”œâ”€â”€ frontend/         # React SPA (port 6220)
â””â”€â”€ chromadb/         # Vector store for semantic search (port 8002)
```

### Service Configuration

| Component | Port | Description |
|-----------|------|-------------|
| Frontend | 6220 | React SPA served by Vite/NGINX |
| Backend | 6221 | FastAPI REST API, WebSockets |
| ChromaDB | 8002 | Vector store for embeddings |

### Quick Start

```powershell
# From D:\Dev\repos\myai
docker compose up -d plex-plus-frontend plex-plus-backend plex-plus-chromadb
```

### Comparison: PlexMCP vs Plex Plus

| Feature | PlexMCP | Plex Plus |
|---------|---------|-----------|
| **Purpose** | MCP server for AI assistants | Web application with AI features |
| **Interface** | MCP protocol (stdio) | Web UI (React) + REST API |
| **AI Features** | None (pure Plex API) | Semantic search, metadata enrichment |
| **Playback Control** | Full (Plexamp, VLC) | Limited |
| **Deployment** | Python package | Docker Compose |
| **Use Case** | Claude Desktop integration | Standalone web app |

**Choose PlexMCP if:**
- You want Claude Desktop integration
- You need comprehensive playback control
- You prefer MCP protocol

**Choose Plex Plus if:**
- You want a web-based interface
- You need semantic search with embeddings
- You want AI-powered metadata enrichment

### Related Documentation

- **Plex Plus README**: `D:\Dev\repos\myai\projects\plex_plus\README.md`
- **Comparison Guide**: `D:\Dev\repos\myai\projects\plex_plus\PLEX_COMPARISON.md`
- **Implementation Summary**: `D:\Dev\repos\myai\projects\plex_plus\docs\COMPLETE_IMPLEMENTATION_SUMMARY.md`
- **MyAI Platform**: `D:\Dev\repos\myai\README.md`

## Ecosystem Integration (*Arr Stack)

> "Arr! Prepare to be boarded!" ðŸ´â€â˜ ï¸

Plex is just one part of the complete media supply chain. To fully automate your library, we integrate with the **Arr Ecosystem** (Sonarr, Radarr, Lidarr, etc.).

These services run alongside Plex in the `media-stack` and handle:
- **Acquisition**: Finding and downloading media (Prowlarr -> Sonarr/Radarr -> qBittorrent)
- **Logistics**: Renaming, moving, and organizing files
- **Plex Notification**: Telling Plex when new loot arrives

For a complete guide on the Arr stack, including our Vienna-compatible "Scattered Media" architecture, see the dedicated documentation:

ðŸ‘‰ **[The Arr Ecosystem Guide](../arr/ARR_ECOSYSTEM.md)**

## Related Documentation

- **Status Report**: `docs/projects/plexmcp/STATUS.md`
- **Portmanteau Pattern**: `docs/patterns/PORTMANTEAU_CONCEPT.md`
- **FastMCP Migration**: `FASTMCP_3.1.1+_MIGRATION.md`
- **Source Repository**: `D:\Dev\repos\plex-mcp`
- **Plex Plus**: `D:\Dev\repos\myai\projects\plex_plus`

---

*Last updated: 2025-12-02*


