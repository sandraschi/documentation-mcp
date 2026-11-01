# OBS Studio MCP Server

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**Industrialized FastMCP 3.2.0 server for OBS Studio automation with multi-target OSC support.**

###  **Current Status: INDUSTRIALIZED - SOTA v1.5.0**
- **FastMCP 3.2.0 Compliance** - Latest protocol version with conversational logic
- **OSC Orchestration** - Multi-target OSC sending and listening (stage automation)
- **Biome Toolchain** - Next-gen frontend linting and formatting for `web_sota`
- **Visual Prefab UI** - Premium dashboard with multi-node connection management
- **MCPB 1.5.0 Packaging** - Industrialized packaging format for Claude Desktop
- **Ruff 0.15.2 Hardened** - Enterprise-grade Python code quality
- **Pydantic V2.10 Native** - High-performance data validation
- **SOTA Prompts** - Extensive MCPB prompt suite for agentic reasoning
- **Root FastAPI Server** - Production-grade web interface orchestration

###  **Code Quality Standards**
-  **Zero Ruff Issues**: All code passes enterprise linting standards
-  **Type Safety**: 100% type coverage with mypy strict mode
-  **Modern Python**: 3.10+ with contemporary patterns and async/await
-  **Security**: Input validation, secure defaults, comprehensive error handling
-  **Performance**: Optimized async operations, connection pooling, resource management

## Quick Start

```powershell
git clone https://github.com/sandraschi/obs-mcp
cd obs-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

## Features

- **Stream Control**: Start/stop streams, monitor status, timecode, bitrate
- **Recording**: Start/stop recordings, track file output and status
- **Scene Management**: List scenes, switch between scenes
- **Audio Control**: List audio sources, mute/unmute specific sources
- **Replay Buffer**: Start/stop replay buffer, save highlights
- **Virtual Camera**: Start/stop virtual camera output
- **OSC Orchestration**: Send/Receive OSC messages to multi-node targets
- **Connection Targets**: Manage multiple OBS and OSC nodes in the web dashboard
- **Transition Control**: Set scene transition types and duration
- **System Status**: Get comprehensive OBS system status
- **Help System**: Built-in help and documentation

###  **Available Tools (18)**

####  **Streaming Tools**
- `stream_start()` - Start live streaming
- `stream_stop()` - Stop live streaming
- `stream_status()` - Get streaming status, timecode, bitrate

####  **Recording Tools**
- `recording_start()` - Start recording
- `recording_stop()` - Stop recording
- `recording_status()` - Get recording status and file info

####  **Scene Management**
- `scenes_list()` - List all available scenes
- `scene_switch(scene_name)` - Switch to specific scene

####  **Audio Control**
- `audio_sources()` - List all audio sources
- `audio_mute(source_name, muted)` - Mute/unmute audio sources

####  **Stage Automation (New v1.5.0)**
- `obs_send_osc(target, address, value)` - Send OSC to external gear
- `obs_list_targets()` - Enumerate connection targets
- `obs_status()` - Get comprehensive OBS status
- `help()` - Built-in help system

## Prerequisites

- **Python 3.10+** (3.9 no longer supported for new features)
- **OBS Studio 28.0+** with WebSocket server enabled
  - OBS  Tools  WebSocket Server Settings  Enable server
- **MCPB CLI** (for building packages): `npm install -g @anthropic-ai/mcpb`

##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx obs-studio-mcp
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "obs-studio-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/obs-mcp", "run", "obs-studio-mcp"]
  }
}
```
###  **PyPI Package Install (RECOMMENDED)**

**Fastest Installation - Production Ready:**

```bash
pip install obs-studio-mcp
```

**Claude Desktop Integration:**
- Open Claude Desktop
- Settings  MCP Servers
- Add new MCP server:
  ```json
  {
    "mcpServers": {
      "obs-studio-mcp": {
        "command": "obs-studio-mcp"
      }
    }
  }
  ```

###  **Claude Desktop (MCPB Package)**

**State-of-the-Art Installation:**

1. **Download MCPB Package:**
   ```bash
   # Build from source (recommended)
   git clone https://github.com/sandraschi/obs-studio-mcp.git
   cd obs-studio-mcp
   ./build-mcpb.sh 0.1.0  # Linux/macOS
   # OR
   .\build-mcpb.ps1 -Version 0.1.0  # Windows PowerShell
   ```

2. **Claude Desktop Integration:**
   - Open Claude Desktop
   - Settings  MCP Servers
   - **Drag and drop** the `.mcpb` file
   - Configure OBS WebSocket settings in Claude Desktop

3. **Verify Installation:**
   ```
   Claude: "Check my OBS streaming status"
   # Claude will automatically use the MCP server
   ```

###  **Other MCP Clients (Cursor, Windsurf, etc.)**

```bash
# Install from PyPI (recommended)
pip install obs-studio-mcp

# OR install from source
git clone https://github.com/sandraschi/obs-studio-mcp.git
cd obs-studio-mcp
uv pip install -e .
```

Add to your MCP config:

```json
{
  "mcpServers": {
    "obs-studio-mcp": {
      "command": "python",
      "args": ["-m", "obs_studio_mcp.server"],
      "env": {
        "PYTHONPATH": "D:/Dev/repos/obs-studio-mcp/src",
        "OBS_WS_HOST": "localhost",
        "OBS_WS_PORT": "4455",
        "OBS_WS_PASSWORD": ""
      }
    }
  }
}
```

## Configuration

Set environment variables or create `.env`:

```ini
OBS_WS_HOST=localhost
OBS_WS_PORT=4455
OBS_WS_PASSWORD=your_password
LOG_LEVEL=INFO
```

##  **Documentation**

### **ADN Content Notes**
Comprehensive Advanced Memory Network documentation:
- **[OBS MCP Server](docs/adn-notes/OBS-MCP-Server.md)** - Complete technical overview, use cases, and enhancement roadmap
- **[OBS Studio](docs/adn-notes/OBS-Studio.md)** - In-depth analysis of OBS Studio and its underrated capabilities

### **Technical Documentation**
- **[Complete Documentation Structure](docs/COMPLETE_DOCUMENTATION_STRUCTURE.md)** - Full project documentation index
- **[Development Standards](docs/standards/)** - Code quality and development guidelines
- **[MCP Technical Guide](docs/mcp-technical/)** - MCP protocol implementation details

##  **Building & Packaging**

### **MCPB Package Build (SOTA)**

```bash
# Validate package structure
.\build-mcpb.ps1 -Validate  # Windows
./build-mcpb.sh --validate  # Linux/macOS

# Build MCPB package
.\build-mcpb.ps1 -Version 0.2.0  # Windows
./build-mcpb.sh 0.2.0            # Linux/macOS

# Clean and rebuild
.\build-mcpb.ps1 -Clean -Version 0.2.0
```

### **Package Structure**
```
obs-studio-mcp-v0.1.0.mcpb/
 manifest.json          # MCPB manifest with full tool registry
 assets/
    icon.png          # 256x256 package icon
    screenshots/      # Feature screenshots
    prompts/          # Extensive Claude Desktop prompts
        system.md     # System-level instructions
        user.md       # User interaction templates
        examples.json # Structured usage examples
        quick-start.md
        configuration.md
        troubleshooting.md
 src/
     obs_studio_mcp/   # Source code only (no dependencies)
```

### **Development Setup**

```bash
# Clone repository
git clone https://github.com/sandraschi/obs-studio-mcp.git
cd obs-studio-mcp

# Install development dependencies
uv pip install -r requirements.txt
uv pip install -e .[dev]

# Run tests
pytest

# Lint code
ruff check .
ruff format .

# Type check
mypy src/
```

##  **Usage Examples**

```
"Start streaming"
"Stop the stream"
"Switch to the Gameplay scene"
"List my scenes"
"Mute the microphone"
"Start recording"
"Save that replay!"
```

## Tools

| Tool | Description |
|------|-------------|
| `start_stream` | Start streaming |
| `stop_stream` | Stop streaming |
| `get_stream_status` | Get stream status |
| `start_recording` | Start recording |
| `stop_recording` | Stop recording |
| `list_scenes` | List all scenes |
| `switch_scene` | Switch to a scene |
| `start_replay_buffer` | Start replay buffer |
| `save_replay_buffer` | Save replay clip |
| `start_virtual_cam` | Start virtual camera |
| `stop_virtual_cam` | Stop virtual camera |
| `list_audio_sources` | List audio sources |
| `toggle_mute` | Mute/unmute audio |
| `set_transition` | Set scene transition |

## Building MCPB Package

```bash
npm install -g @anthropic-ai/mcpb
mcpb pack . dist/obs-studio-mcp-v0.1.0.mcpb --validate
```


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

## License

MIT License


##  Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10818**.
*(Assigned ports: **10818** (Web dashboard frontend), **10819** (Web dashboard backend (API)))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10818` in your browser.
