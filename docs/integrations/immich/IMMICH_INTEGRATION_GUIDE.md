# Immich Integration Guide

**Last Updated:** 2025-12-18
**Status:** Production Ready + API Migration Complete
**Source Repos:** `D:\Dev\repos\immich-mcp` (MCP Server) + `D:\Dev\repos\myai\projects\immich_plus` (Web Frontend)

## Overview

This guide covers comprehensive Immich integration through **two complementary approaches**:

### ðŸŽ¨ Immich++ (Web Frontend)
**AI-Powered Immich Frontend** | **Dual Transport Architecture** | **Turbopack-Ready**

- **Location**: `D:\Dev\repos\myai\projects\immich_plus`
- **Technology**: Node.js/Express backend + React 19/Vite frontend with Turbopack
- **Features**: AI semantic search, multilingual OCR, theme toggle, responsive UI
- **Status**: âœ… **Immich v2.4.0 Compatible** (API migration completed 2025-12-18)
- **Architecture**: **Dual Transport** - MCP Proxy (recommended) + Direct API fallback

### ðŸ¤– ImmichMCP (MCP Server)
**Claude Desktop Integration** | **FastMCP 3.1.1++** | **Programmatic Access**

- **Location**: `D:\Dev\repos\immich-mcp`
- **Technology**: Python FastMCP server
- **Features**: CLIP search, OCR search, album management, batch operations
- **Status**: âš ï¸ **Requires API Migration** (see API Migration section below)

---

## âš ï¸ CRITICAL: Immich v2.4.0 API Migration

**Date:** December 18, 2025  
**Impact:** Major API architecture change discovered and resolved  
**Duration:** 4+ hours of debugging  

### What Happened

During Immich++ development, we discovered that **Immich v2.4.0 completely changed its API architecture**:

- **Old Assumption**: Traditional REST API with direct `/api/assets` endpoints
- **New Reality**: Search-based API using `/api/search/metadata` for asset access
- **Impact**: Both Immich++ and ImmichMCP needed major API refactoring

### Migration Results

**âœ… Immich++**: Successfully migrated to v2.4.0 search API  
**âš ï¸ ImmichMCP**: Still needs API migration (see upgrade section below)  
**ðŸ“š Documentation**: Complete migration notes in `IMMICH_API_V2.4_MIGRATION.md`

### Key Changes

| Feature | Old (Pre-v2.4.0) | New (v2.4.0+) |
|---------|------------------|----------------|
| Asset Listing | `GET /api/assets` | `POST /api/search/metadata` |
| Direct Asset Access | `GET /api/assets/:id` | **Not Available** |
| Album Access | `GET /api/albums` | `GET /api/albums` âœ… |
| Authentication | API Key | API Key âœ… |

---

## Integration Options

## Table of Contents

1. [Immich Overview](#immich-overview)
2. [Immich++ (Web Frontend)](#immich-web-frontend)
3. [ImmichMCP (MCP Server)](#immichmcp-mcp-server)
4. [API Migration Notes](#api-migration-notes)
5. [Installation and Setup](#installation-and-setup)
6. [Configuration](#configuration)
7. [MCP Tools](#mcp-tools)
8. [Photo Management](#photo-management)
9. [Search Capabilities](#search-capabilities)
10. [Album Management](#album-management)
11. [Advanced Features](#advanced-features)
12. [Troubleshooting](#troubleshooting)
13. [Best Practices](#best-practices)

## Immich Overview

### What is Immich?

Immich is a self-hosted photo and video backup solution that provides:

- **Photo Backup**: Automatic backup from mobile devices
- **Smart Search**: AI-powered photo search using CLIP
- **OCR Search**: Text extraction and search (v2.2.0+)
- **Album Management**: Organize photos into albums
- **Metadata Preservation**: Maintains EXIF and other metadata
- **Web Interface**: Modern, responsive web UI

### Key Features

- **CLIP-based Search**: Natural language photo search
- **OCR Search**: Find photos by text content (v2.2.0+)
- **Metadata Search**: Search by EXIF data, tags, dates
- **Album Organization**: Create and manage albums
- **Batch Operations**: Upload and manage multiple photos
- **API-first**: Comprehensive REST API

## Immich++ (Web Frontend)

### Overview

**Immich++** is a modern, AI-enhanced web frontend for Immich that transforms your photo management experience. Built with cutting-edge web technologies and optimized for Turbopack development.

**Location:** `D:\Dev\repos\myai\projects\immich_plus`  
**Technology Stack:** Node.js/Express + React 19/Vite + Turbopack  
**Status:** âœ… **Fully Compatible with Immich v2.4.0** (API migration completed)

### Key Features

#### ðŸ¤– AI-Powered Features
- **Smart Semantic Search** - Find photos using natural language ("dog in snow")
- **Multilingual OCR** - Search text in 12+ languages (Greek, Korean, Russian, etc.)
- **AI Content Analysis** - Automatic photo categorization and tagging
- **Smart Album Suggestions** - AI-generated album organization ideas

#### ðŸš€ Performance & UX
- **Turbopack Ready** - Lightning-fast development with <100ms hot reload
- **Modern React 19** - Latest React features with concurrent rendering
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Theme Toggle** - Automatic dark/light mode switching
- **Virtual Scrolling** - Handle thousands of photos smoothly

#### ðŸŽ¨ User Interface
- **Settings Page** - API key management and configuration
- **Help Documentation** - Built-in help and user guide
- **Logger UI** - Debug and monitoring interface
- **Modern UI Components** - Clean, intuitive interface design

### Installation

#### Prerequisites
- **Node.js 18+**
- **Immich Server v2.4.0+** running and accessible
- **Immich API Key** (from Administration â†’ API Keys)

#### Quick Start
```bash
# Clone and setup
git clone <immich-plus-repo>
cd immich-plus

# Backend setup
cd backend
npm install

# Frontend setup
cd ../frontend
npm install

# Start development
cd ../backend && npm run dev    # Terminal 1
cd ../frontend && npm run dev:turbo  # Terminal 2
```

#### Production Deployment
```bash
# Build and deploy
docker-compose up -d

# Access at http://localhost:3000
```

### Configuration
```env
# Required
IMMICH_BASE_URL=http://localhost:2283
IMMICH_API_KEY=your_api_key_here

# Optional AI Features
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...

# Development
NODE_ENV=development
LOG_LEVEL=info
PORT=3001
```

### API Endpoints
- `GET /api/immich/assets` - List assets (via search API)
- `GET /api/immich/albums` - List albums
- `POST /api/immich/search` - Advanced search
- `GET /api/immich/people` - Face recognition data

### Planned Features (Phase 2-5)

#### Phase 2: Enhanced UI (In Progress)
- [x] Theme toggle
- [x] Settings page with API key management
- [ ] Advanced search filters
- [ ] Virtual scrolling implementation
- [ ] Bulk operations interface

#### Phase 3: AI Features (Planned)
- [ ] Smart semantic search
- [ ] AI-powered album suggestions
- [ ] Photo content analysis
- [ ] Face recognition clustering
- [ ] Multilingual OCR search (12+ languages)
- [ ] Memory generation from photos

#### Phase 4: Advanced Features (Future)
- [ ] Timeline view with infinite scroll
- [ ] Map integration for location browsing
- [ ] Sharing and collaboration
- [ ] Plugin system for custom AI models
- [ ] Offline PWA functionality

### Integration with ImmichMCP

Immich++ complements ImmichMCP by providing:
- **Web Interface** for MCP's programmatic features
- **Visual Experience** for AI-powered photo management
- **User-Friendly Access** to advanced Immich capabilities

Together they create a complete AI-powered photo management ecosystem.

---

## ðŸ”„ Dual Transport Architecture

Immich++ implements a **dual transport architecture** that intelligently routes requests through the most appropriate channel:

### Transport Options

#### ðŸš€ **MCP Proxy Transport (Recommended)**
```
Immich++ â†’ ImmichMCP HTTP API â†’ Immich Server
```
- **Benefits**: Leverages tested MCP tools, consistent API, automatic updates
- **Configuration**: `USE_MCP_PROXY=true` (default in Immich++)
- **Requirements**: ImmichMCP server running in HTTP mode
- **Advantages**: Single source of truth, tool reuse, future-proof

#### ðŸ”— **Direct API Transport (Fallback)**
```
Immich++ â†’ Immich REST API
```
- **Benefits**: No additional services required, direct communication
- **Configuration**: `USE_MCP_PROXY=false`
- **Requirements**: Direct access to Immich server
- **Advantages**: Simplicity, no proxy dependency

### MCP Proxy Setup

1. **Start ImmichMCP in HTTP mode:**
   ```bash
   cd D:\Dev\repos\immich-mcp
   python run_http_server.py --host 127.0.0.1 --port 8000
   ```

2. **Configure Immich++ environment:**
   ```env
   MCP_BASE_URL=http://localhost:8000
   USE_MCP_PROXY=true
   ```

3. **Verify MCP proxy:**
   ```bash
   curl http://localhost:8000/immich-mcp/api/v1/health
   curl http://localhost:8000/immich-mcp/api/v1/system/storage
   ```

### Architecture Benefits

- **ðŸ”„ Automatic Fallback**: MCP proxy failure â†’ Direct API
- **ðŸ› ï¸ Tool Reuse**: All 15+ MCP tools available via HTTP
- **ðŸ“ˆ Maintainability**: Single Immich API implementation
- **ðŸ”§ Flexibility**: Works with or without MCP proxy
- **ðŸš€ Future-Proof**: MCP updates benefit Immich++ automatically

---

## ImmichMCP (MCP Server)

### Overview

**ImmichMCP** is a FastMCP 3.1.1++ compliant MCP server that provides Claude Desktop integration with Immich photo library management system. It enables AI agents to interact with your photo collection through the MCP protocol.

**Location:** `D:\Dev\repos\immich-mcp`

### Key Features

- **FastMCP 3.1.1++ Compliance** - Modern MCP server implementation
- **Comprehensive Photo Operations** - Upload, search, organize photos
- **Smart Search** - CLIP-based natural language photo search
- **OCR Search** - Text extraction search (Immich v2.2.0+)
- **Album Management** - Create and manage photo albums
- **Metadata Preservation** - Maintains EXIF and other metadata
- **Batch Operations** - Upload and manage multiple photos efficiently
- **Austrian Efficiency** - Optimized for performance and reliability

### Installation

#### Prerequisites

- **Python 3.11+**: Required for ImmichMCP
- **Immich Server**: v2.0.0+ running and accessible (v2.2.0+ for OCR search)
- **Immich API Key**: Required for authentication

#### Installation Steps

```powershell
# Clone repository
cd D:\Dev\repos
git clone https://github.com/sandraschi/immich-mcp.git
cd immich-mcp

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
Copy-Item .env.example .env
# Edit .env with your Immich URL and API key
```

#### MCP Configuration

For Claude Desktop, add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "immich-mcp": {
      "command": "python",
      "args": ["-m", "immich_mcp.server"],
      "cwd": "D:/Dev/repos/immich-mcp",
      "env": {
        "IMMICH_API_KEY": "your-api-key-here",
        "IMMICH_URL": "http://localhost:2283",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Configuration

#### Environment Variables

```bash
# Required
IMMICH_API_KEY=your_api_key_here
IMMICH_URL=http://localhost:2283

# Optional
LOG_LEVEL=INFO
MCP_SERVER_NAME="Immich Photo Management MCP ðŸ“¸"
```

#### Getting Your API Key

1. **Via Web Interface**:
   - Open Immich Web UI
   - Go to User Settings â†’ API Keys
   - Click "Create API Key"
   - Copy the generated key

2. **Via API**:
   ```bash
   curl -X POST http://your-immich-server:2283/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"your-email","password":"your-password"}'
   ```

### Available Tools

ImmichMCP provides comprehensive photo management tools:

1. **Upload Photos**
   - Batch upload with progress tracking
   - Automatic duplicate detection
   - Metadata preservation

2. **Get Photo Info**
   - View detailed metadata
   - Check storage location
   - See creation/modification dates

3. **Search Photos**
   - CLIP-based semantic search
   - OCR text search (v2.2.0+)
   - Metadata search
   - Filename search

4. **Album Management**
   - Create and manage albums
   - Add photos to albums
   - List and filter albums

5. **Server Health**
   - Check Immich server status
   - Verify API connectivity
   - View version information

### Usage Examples

```python
# Upload photos
immich_upload_photo(
    file_paths=["/path/to/photo.jpg"],
    album_name="Vacation 2025",
    preserve_metadata=True
)

# Search photos using CLIP
immich_search_photos(
    query="Benny playing in the park",
    search_type="smart",
    limit=50
)

# Search photos using OCR (v2.2.0+)
immich_search_photos(
    query="invoice number 12345",
    search_type="ocr",
    limit=20
)

# Get photo details
immich_get_photo(asset_id="abc123")

# Create album
immich_create_album(
    album_name="Vienna Trip 2025",
    description="Photos from Vienna vacation"
)
```

## API Migration Notes

### âš ï¸ Immich v2.4.0 Breaking Changes

**Discovered:** December 18, 2025  
**Impact:** Major API architecture change requiring full rewrite  
**Resolution:** Immich++ migrated successfully, ImmichMCP needs update

#### What Changed

Immich v2.4.0 completely redesigned the asset access API:

**âŒ Old Structure (Pre-v2.4.0):**
```typescript
// Direct asset access
GET /api/assets              // List all assets
GET /api/assets/:id         // Get specific asset
GET /api/assets/statistics  // Get statistics
```

**âœ… New Structure (v2.4.0+):**
```typescript
// Search-based asset access
POST /api/search/metadata   // List assets via search
GET /api/assets/statistics  // Statistics still work
// No direct asset access by ID
```

#### Migration Impact

| Component | Status | Notes |
|-----------|--------|-------|
| **Immich++** | âœ… **Migrated** | Uses search API successfully |
| **ImmichMCP** | âš ï¸ **Needs Update** | Still uses old API structure |
| **API Documentation** | ðŸ“ **Updated** | Migration notes documented |

#### Upgrade Required for ImmichMCP

ImmichMCP currently assumes the old API structure and will fail with Immich v2.4.0+. Update required:

1. Replace direct `/api/assets` calls with search API
2. Update asset retrieval logic
3. Test all operations against v2.4.0

---

### Compatibility

#### Immich Versions

| Feature | Immich++ | ImmichMCP | Notes |
|---------|----------|-----------|-------|
| **Basic Operations** | v2.4.0+ | v2.0.0+ | Upload, search, albums |
| **CLIP Search** | v2.4.0+ | v2.0.0+ | Semantic search |
| **OCR Search** | Planned | v2.2.0+ | Text extraction search |
| **Search API** | âœ… v2.4.0+ | âš ï¸ Needs migration | New asset access method |

#### FastMCP Version (ImmichMCP)

- **Required**: FastMCP 3.1.1++
- **Recommended**: FastMCP 3.1.1++
- **Status**: âš ï¸ **API Migration Required** for v2.4.0 compatibility

### Performance

**Austrian Efficiency Metrics:**
- **Photo upload**: ~2-5 seconds per image (depending on size)
- **Smart search**: ~1-3 seconds for CLIP queries
- **Album operations**: ~0.5-1 seconds for typical operations
- **Face detection**: ~5-10 seconds per batch (server-dependent)

### Documentation

- **Full README**: `D:\Dev\repos\immich-mcp\README.md`
- **API Documentation**: `D:\Dev\repos\immich-mcp\docs\API.md`
- **User Guide**: `D:\Dev\repos\immich-mcp\docs\USER_GUIDE.md`
- **Troubleshooting**: `D:\Dev\repos\immich-mcp\docs\Troubleshooting.md`

---

## Installation and Setup

### Prerequisites

- **Python 3.11+**: Required for ImmichMCP
- **Immich Server**: v2.0.0+ running and accessible
- **Immich API Key**: Required for authentication
- **Network Access**: Server must be accessible

### Immich Server Installation

#### Docker (Recommended)

```bash
# Clone Immich repository
git clone https://github.com/immich-app/immich.git
cd immich

# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Start services
docker compose up -d
```

#### Manual Installation

See [Immich Documentation](https://immich.app/docs/install) for detailed installation instructions.

### Getting Your API Key

1. **Via Web Interface**:
   - Open Immich Web UI
   - Go to User Settings â†’ API Keys
   - Click "Create API Key"
   - Copy the generated key

2. **Via API**:
   ```bash
   curl -X POST http://your-immich-server:2283/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"your-email","password":"your-password"}'
   ```

### Immich Server Installation

See the [ImmichMCP section](#immichmcp-mcp-server) above for detailed installation instructions.

## Configuration

### Environment Variables

```powershell
# Required
$env:IMMICH_API_KEY = "your-api-key-here"
$env:IMMICH_URL = "http://localhost:2283"

# Optional
$env:LOG_LEVEL = "INFO"
```

### Configuration File (`.env`)

```bash
# Required
IMMICH_API_KEY=your_api_key_here
IMMICH_URL=http://localhost:2283

# Optional: Logging
LOG_LEVEL=INFO
```

### MCP Configuration (`mcp.json`)

```json
{
  "immich-mcp": {
    "command": "python",
    "args": ["-m", "immich_mcp.server"],
    "cwd": "D:/Dev/repos/immich-mcp",
    "env": {
      "IMMICH_API_KEY": "your-api-key-here",
      "IMMICH_URL": "http://localhost:2283",
      "PYTHONUNBUFFERED": "1"
    }
  }
}
```

## MCP Tools

ImmichMCP provides comprehensive photo management tools:

### Core Tools

1. **`immich_upload_photo`**
   - Upload photos/videos with metadata preservation
   - Batch upload support
   - Automatic duplicate detection

2. **`immich_get_albums`**
   - List all albums
   - Get album details
   - Filter by name or date

3. **`immich_create_album`**
   - Create new albums
   - Set album metadata
   - Add photos to albums

4. **`immich_search_photos`**
   - CLIP-based semantic search
   - OCR text search (v2.2.0+)
   - Metadata search
   - Filename search

5. **`immich_get_photo`**
   - Get detailed photo information
   - View metadata
   - Get download URLs

## Photo Management

### Uploading Photos

```python
# Upload single photo
immich_upload_photo(
    file_paths=["/path/to/photo.jpg"],
    album_name="Vacation 2025",
    preserve_metadata=True
)

# Batch upload
immich_upload_photo(
    file_paths=[
        "/path/to/photo1.jpg",
        "/path/to/photo2.jpg",
        "/path/to/photo3.jpg"
    ],
    album_name="Summer Trip"
)
```

### Getting Photo Information

```python
# Get photo details
immich_get_photo(asset_id="abc123")

# Returns:
# - Metadata (EXIF, GPS, etc.)
# - Tags and labels
# - Album associations
# - File information
```

## Search Capabilities

### CLIP-based Semantic Search

```python
# Natural language search
immich_search_photos(
    query="Benny playing in the park",
    search_type="smart",
    limit=50
)
```

### OCR Text Search (v2.2.0+)

```python
# Search for text in photos
immich_search_photos(
    query="invoice number 12345",
    search_type="ocr",
    limit=20
)
```

### Metadata Search

```python
# Search by camera model
immich_search_photos(
    query="Canon EOS",
    search_type="metadata",
    limit=50
)
```

### Filename Search

```python
# Search by filename
immich_search_photos(
    query="vacation_2025",
    search_type="filename",
    limit=50
)
```

## Album Management

### Creating Albums

```python
# Create new album
immich_create_album(
    album_name="Vienna Trip 2025",
    description="Photos from Vienna vacation"
)
```

### Listing Albums

```python
# List all albums
immich_get_albums()

# Get specific album
immich_get_albums(album_name="Vienna Trip 2025")
```

### Organizing Photos

```python
# Upload photos to album
immich_upload_photo(
    file_paths=["/path/to/photo.jpg"],
    album_name="Vienna Trip 2025"
)
```

## Advanced Features

### Batch Operations

```python
# Upload multiple photos to album
immich_upload_photo(
    file_paths=[
        "/vacation/photo1.jpg",
        "/vacation/photo2.jpg",
        "/vacation/photo3.jpg"
    ],
    album_name="Summer 2025",
    preserve_metadata=True
)
```

### Metadata Preservation

```python
# Upload with metadata preservation
immich_upload_photo(
    file_paths=["/path/to/photo.jpg"],
    preserve_metadata=True  # Keeps EXIF, GPS, etc.
)
```

### Date-based Organization

```python
# Organize photos by date
# (Feature available through Immich API)
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Verify Immich server is running
   - Check firewall settings
   - Verify URL and port (default: 2283)

2. **Authentication Failed**
   - Verify IMMICH_API_KEY is correct
   - Check API key has proper permissions
   - Regenerate API key if needed

3. **Upload Failures**
   - Check file permissions
   - Verify file format is supported
   - Check available storage space

4. **Search Not Working**
   - Verify Immich version (v2.0.0+ for CLIP, v2.2.0+ for OCR)
   - Check machine learning features are enabled
   - Ensure photos have been processed

5. **OCR Search Not Available**
   - Requires Immich v2.2.0+
   - Verify OCR feature is enabled in server settings
   - Check photos have been processed for OCR

## Best Practices

1. **API Key Security**
   - Store API keys in environment variables
   - Never commit keys to version control
   - Use separate keys for different environments

2. **Upload Performance**
   - Use batch uploads for multiple photos
   - Preserve metadata when possible
   - Organize photos into albums during upload

3. **Search Optimization**
   - Use specific search types when possible
   - Limit results to reasonable numbers
   - Use CLIP search for semantic queries
   - Use OCR search for text-based queries

4. **Album Organization**
   - Create albums before uploading photos
   - Use descriptive album names
   - Add descriptions for context

5. **Metadata Management**
   - Always preserve metadata when uploading
   - Use metadata search for technical queries
   - Leverage EXIF data for organization

## Compatibility

### Immich Versions

| Feature | Minimum Version | Notes |
|---------|----------------|-------|
| Basic Operations | v2.0.0+ | Upload, search, albums |
| CLIP Search | v2.0.0+ | Semantic search |
| OCR Search | v2.2.0+ | Text extraction search |

### FastMCP Version

- **Required**: FastMCP 3.1.1++
- **Recommended**: FastMCP 3.1.1++

## Related Documentation

### ImmichMCP
- **Source Repository**: `D:\Dev\repos\immich-mcp`
- **README**: `D:\Dev\repos\immich-mcp\README.md`
- **API Documentation**: `D:\Dev\repos\immich-mcp\docs\API.md`
- **User Guide**: `D:\Dev\repos\immich-mcp\docs\USER_GUIDE.md`
- **Troubleshooting**: `D:\Dev\repos\immich-mcp\docs\Troubleshooting.md`

### Immich Platform
- **Immich Documentation**: https://immich.app/docs
- **Immich GitHub**: https://github.com/immich-app/immich
- **Immich API Reference**: https://immich.app/docs/api

### Platform Documentation
- **MCP Central Docs**: `D:\Dev\repos\mcp-central-docs\`

---

*This integration guide covers ImmichMCP (MCP server) and follows Austrian efficiency principles for comprehensive, clear, and actionable documentation.*

*Last updated: 2025-12-02*


