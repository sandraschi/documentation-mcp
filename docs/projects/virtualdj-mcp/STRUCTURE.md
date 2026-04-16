# VirtualDJ MCP - Project Structure

**Last Updated:** 2025-11-28  
**Source Repo:** `D:\Dev\repos\virtualdj-mcp`

---

## Directory Layout

```
virtualdj-mcp/
â”œâ”€â”€ src/
â”‚   â””â”€â”€ virtualdj_mcp/
â”‚       â”œâ”€â”€ __init__.py           # Package init, exports mcp
â”‚       â”œâ”€â”€ __main__.py           # Entry point (python -m virtualdj_mcp)
â”‚       â”œâ”€â”€ server.py             # FastMCP server setup, tool registration
â”‚       â”œâ”€â”€ app.py                # Application logic
â”‚       â”œâ”€â”€ config.py             # Configuration management
â”‚       â”œâ”€â”€ mixer_controller.py   # Mixer state management
â”‚       â”‚
â”‚       â”œâ”€â”€ api/                  # FastAPI REST API
â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚       â”‚   â””â”€â”€ app.py            # FastAPI routes
â”‚       â”‚
â”‚       â”œâ”€â”€ core/                 # Core functionality
â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚       â”‚   â””â”€â”€ vdj_client.py     # VirtualDJ HTTP client, VDJError
â”‚       â”‚
â”‚       â”œâ”€â”€ services/             # Business logic services
â”‚       â”‚   â”œâ”€â”€ __init__.py
â”‚       â”‚   â”œâ”€â”€ audio_analysis.py # AudioAnalyzer (aubio + librosa)
â”‚       â”‚   â”œâ”€â”€ auto_dj.py        # Auto-DJ service
â”‚       â”‚   â”œâ”€â”€ library_scanner.py# LibraryScanner (mutagen)
â”‚       â”‚   â”œâ”€â”€ performance.py    # Performance metrics
â”‚       â”‚   â”œâ”€â”€ preferences.py    # User preferences
â”‚       â”‚   â”œâ”€â”€ recording.py      # Recording management
â”‚       â”‚   â””â”€â”€ suggestions.py    # Track suggestions
â”‚       â”‚
â”‚       â””â”€â”€ tools/                # MCP tools (organized by category)
â”‚           â”œâ”€â”€ __init__.py
â”‚           â”œâ”€â”€ shared/           # Shared utilities
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â”œâ”€â”€ dependencies.py
â”‚           â”‚   â””â”€â”€ exceptions.py # VDJError re-export
â”‚           â”‚
â”‚           â”œâ”€â”€ deck_control/     # Deck tools
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â””â”€â”€ tools.py      # play_pause, load_track, seek, volume, status
â”‚           â”‚
â”‚           â”œâ”€â”€ mixing/           # Mixer tools
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â””â”€â”€ tools.py      # crossfader, auto_sync
â”‚           â”‚
â”‚           â”œâ”€â”€ library/          # Library tools
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â”œâ”€â”€ models.py     # TrackInfo model
â”‚           â”‚   â””â”€â”€ tools.py      # search_tracks, analyze_track_audio
â”‚           â”‚
â”‚           â”œâ”€â”€ automation/       # Automation tools
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â””â”€â”€ tools.py      # auto_dj_mode, suggestions
â”‚           â”‚
â”‚           â”œâ”€â”€ recording/        # Recording tools
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â””â”€â”€ tools.py      # start/stop, list, export
â”‚           â”‚
â”‚           â”œâ”€â”€ performance/      # Performance tools
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â””â”€â”€ tools.py      # metrics, stats, trends
â”‚           â”‚
â”‚           â”œâ”€â”€ skin/             # Skin control tools
â”‚           â”‚   â”œâ”€â”€ __init__.py
â”‚           â”‚   â””â”€â”€ tools.py      # load_skin, set_panel
â”‚           â”‚
â”‚           â””â”€â”€ system/           # System tools
â”‚               â”œâ”€â”€ __init__.py
â”‚               â””â”€â”€ tools.py      # system_status, help
â”‚
â”œâ”€â”€ tests/                        # Test suite
â”‚   â”œâ”€â”€ local/                    # Local testing scripts
â”‚   â”‚   â”œâ”€â”€ test_fastapi_interface.py
â”‚   â”‚   â”œâ”€â”€ test_http_api.py
â”‚   â”‚   â”œâ”€â”€ test_mcp_interface.py
â”‚   â”‚   â””â”€â”€ VirtualDJ-MCP_API.postman_collection.json
â”‚   â”œâ”€â”€ test_mixer_controller.py
â”‚   â””â”€â”€ test_mixer_controls.py
â”‚
â”œâ”€â”€ docs/                         # Documentation
â”‚   â”œâ”€â”€ development/              # Development guides
â”‚   â”œâ”€â”€ glama-platform/           # Glama registry guides
â”‚   â”œâ”€â”€ mcpb-packaging/           # MCPB packaging guides
â”‚   â”œâ”€â”€ mcp-technical/            # MCP technical docs
â”‚   â”œâ”€â”€ serena/                   # Serena integration
â”‚   â”œâ”€â”€ NETWORK_CONTROL_SETUP.md  # VirtualDJ plugin setup
â”‚   â””â”€â”€ VIRTUALDJ_REFERENCE.md    # VDJScript reference
â”‚
â”œâ”€â”€ assets/                       # Static assets
â”‚   â””â”€â”€ prompts/                  # Prompt templates
â”‚       â”œâ”€â”€ automation.md
â”‚       â”œâ”€â”€ dj_performance.md
â”‚       â”œâ”€â”€ library_management.md
â”‚       â”œâ”€â”€ mixing_guide.md
â”‚       â”œâ”€â”€ system.md
â”‚       â””â”€â”€ troubleshooting.md
â”‚
â”œâ”€â”€ mcpb/                         # MCPB package contents
â”‚   â”œâ”€â”€ manifest.json
â”‚   â”œâ”€â”€ assets/prompts/
â”‚   â””â”€â”€ server/server.py
â”‚
â”œâ”€â”€ dist/                         # Built packages
â”‚   â””â”€â”€ virtualdj-mcp.mcpb
â”‚
â”œâ”€â”€ scripts/                      # Utility scripts
â”‚   â”œâ”€â”€ backup-repo.ps1
â”‚   â”œâ”€â”€ check-repo-standards.ps1
â”‚   â””â”€â”€ fix-standards.ps1
â”‚
â”œâ”€â”€ examples/                     # Usage examples
â”‚   â”œâ”€â”€ auto_dj_example.py
â”‚   â”œâ”€â”€ basic_playback.py
â”‚   â”œâ”€â”€ performance_monitor.py
â”‚   â””â”€â”€ recording_example.py
â”‚
â”œâ”€â”€ pyproject.toml                # Python project config
â”œâ”€â”€ requirements.txt              # Dependencies
â”œâ”€â”€ manifest.json                 # Tool manifest
â”œâ”€â”€ README.md                     # Main readme
â”œâ”€â”€ CHANGELOG.md                  # Version history
â”œâ”€â”€ CONTRIBUTING.md               # Contribution guide
â”œâ”€â”€ SECURITY.md                   # Security policy
â””â”€â”€ LICENSE                       # MIT License
```

---

## Key Files

### Entry Points

| File | Purpose |
|------|---------|
| `src/virtualdj_mcp/__main__.py` | `python -m virtualdj_mcp` |
| `src/virtualdj_mcp/server.py` | FastMCP server setup |

### Core Services

| File | Purpose |
|------|---------|
| `core/vdj_client.py` | VirtualDJ HTTP client, `VDJError` exception |
| `services/audio_analysis.py` | `AudioAnalyzer` (aubio + librosa) |
| `services/library_scanner.py` | `LibraryScanner` (mutagen) |
| `services/auto_dj.py` | Auto-DJ logic |

### Tool Categories (8 categories)

| Category | File | Tools |
|----------|------|-------|
| Deck Control | `tools/deck_control/tools.py` | play_pause, load_track, seek, volume, status |
| Mixing | `tools/mixing/tools.py` | crossfader, auto_sync |
| Library | `tools/library/tools.py` | search_tracks, analyze_track_audio |
| Automation | `tools/automation/tools.py` | auto_dj_mode, stop, status, suggest |
| Recording | `tools/recording/tools.py` | start, stop, status, list, delete, export |
| Performance | `tools/performance/tools.py` | metrics, stats, trends, recommendations |
| Skin | `tools/skin/tools.py` | get_info, load, switch, set_panel, toggle_window |
| System | `tools/system/tools.py` | system_status, show_help |

---

## Dependencies

### Core Dependencies (pyproject.toml)

```toml
dependencies = [
    # MCP Framework
    "fastmcp>=3.1.1+.1,<3.0.0",
    "fastapi>=0.95.0",
    "uvicorn[standard]>=0.22.0",
    
    # HTTP client
    "aiohttp>=3.8.0",
    "httpx>=0.24.0",
    
    # Audio processing (aubio for DJ-grade analysis)
    "librosa>=0.10.0",
    "soundfile>=0.12.0",
    "numpy>=1.24.0",
    "mutagen>=1.47.0",
    "aubio>=0.4.9",
    
    # Utilities
    "pydantic>=2.0.0,<3.0.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
    "psutil>=5.9.0",
]
```

### Python Version Constraint

```toml
requires-python = ">=3.10,<3.12"
```

**Why?** aubio lacks pre-built wheels for Python 3.12+. Python 3.11 is recommended.

---

## Audio Analysis Stack

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                     AudioAnalyzer                            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                              â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚     aubio       â”‚      â”‚         librosa             â”‚   â”‚
â”‚  â”‚  (if available) â”‚      â”‚       (fallback)            â”‚   â”‚
â”‚  â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤      â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤   â”‚
â”‚  â”‚ â€¢ BPM detection â”‚      â”‚ â€¢ Chroma-based key detectionâ”‚   â”‚
â”‚  â”‚ â€¢ Pitch/key     â”‚      â”‚ â€¢ Beat tracking             â”‚   â”‚
â”‚  â”‚ â€¢ Beat tracking â”‚      â”‚ â€¢ Spectral analysis         â”‚   â”‚
â”‚  â”‚ â€¢ Real-time     â”‚      â”‚ â€¢ Energy/onset              â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚                                                              â”‚
â”‚  Priority: aubio first (DJ-grade) â†’ librosa fallback        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Configuration Flow

```
Environment Variables (.env or system)
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ config.py                     â”‚
â”‚ - VDJ_HTTP_HOST/PORT         â”‚
â”‚ - VDJ_PATH                   â”‚
â”‚ - VDJ_LIBRARY_PATH           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ core/vdj_client.py           â”‚
â”‚ - VirtualDJClient            â”‚
â”‚ - HTTP connection to VDJ     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
        â”‚
        â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Tools (tools/*/tools.py)     â”‚
â”‚ - Use VirtualDJClient        â”‚
â”‚ - Exposed via FastMCP        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## Testing

### Local Tests

```powershell
# Test MCP interface
uv run python tests/local/test_mcp_interface.py

# Test HTTP API
uv run python tests/local/test_http_api.py

# Test FastAPI interface
uv run python tests/local/test_fastapi_interface.py
```

### Postman Collection

Import `tests/local/VirtualDJ-MCP_API.postman_collection.json` for API testing.

---

## Build & Packaging

### MCPB Package

```powershell
# Build MCPB package
# (manual process - copy to mcpb/, update manifest.json)

# Package location
dist/virtualdj-mcp.mcpb
```

### Run Server

```powershell
# With uv (recommended)
uv run --python 3.11 python -m virtualdj_mcp

# With pip
python -m virtualdj_mcp
```

---

## Related Files in Central Docs

- `docs/projects/virtualdj-mcp/STATUS.md` - This status report
- `docs/mcp-technical/` - MCP technical documentation
- `docs/patterns/` - MCP patterns and best practices


