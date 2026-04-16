# 🔥 OBS Studio MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP 3.1.1+.3](https://img.shields.io/badge/FastMCP-3.1.1+.3-blue)](https://github.com/modelcontextprotocol/fastmcp)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![MCPB](https://img.shields.io/badge/MCPB-0.2-blue)](https://docs.anthropic.com/claude/docs/desktop-mcp)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green)](https://github.com/sandraschi/obs-studio-mcp)

**State-of-the-Art MCP server for automating OBS Studio with AI-powered scene management and streaming control.**

### ✅ **Current Status: PRODUCTION READY - FastMCP 3.1.1+.3**
- **FastMCP 3.1.1+.3 Compliance** - Latest MCP specification with conversational and sampling capabilities
- **SEP-1577 Sampling Support** - Agentic workflows with autonomous tool orchestration
- **Conversational Tool Returns** - Natural language responses with structured metadata
- **MCPB Packaging** - Official Claude Desktop integration format
- **Ruff Linted** - Enterprise-grade code quality (0 issues)
- **Pydantic V2 Native** - Modern data validation with full V2 compatibility
- **Comprehensive Prompts** - Extensive MCPB prompt templates for Claude Desktop
- **REST API Server** - Full FastAPI REST interface for direct integration

### 🔧 **Code Quality Standards**
- ✅ **Zero Ruff Issues**: All code passes enterprise linting standards
- ✅ **Type Safety**: 100% type coverage with mypy strict mode
- ✅ **Modern Python**: 3.10+ with contemporary patterns and async/await
- ✅ **Security**: Input validation, secure defaults, comprehensive error handling
- ✅ **Performance**: Optimized async operations, connection pooling, resource management

## Features

- **Stream Control**: Start/stop streams, monitor status, timecode, bitrate
- **Recording**: Start/stop recordings, track file output and status
- **Scene Management**: List scenes, switch between scenes
- **Audio Control**: List audio sources, mute/unmute specific sources
- **Replay Buffer**: Start/stop replay buffer, save highlights
- **Virtual Camera**: Start/stop virtual camera output
- **Transition Control**: Set scene transition types and duration
- **System Status**: Get comprehensive OBS system status
- **Help System**: Built-in help and documentation

### 📋 **Available Tools (18)**

#### 🎥 **Streaming Tools**
- `stream_start()` - Start live streaming
- `stream_stop()` - Stop live streaming
- `stream_status()` - Get streaming status, timecode, bitrate

#### 🎬 **Recording Tools**
- `recording_start()` - Start recording
- `recording_stop()` - Stop recording
- `recording_status()` - Get recording status and file info

#### 🎭 **Scene Management**
- `scenes_list()` - List all available scenes
- `scene_switch(scene_name)` - Switch to specific scene

#### 🔊 **Audio Control**
- `audio_sources()` - List all audio sources
- `audio_mute(source_name, muted)` - Mute/unmute audio sources

#### 🎮 **Advanced Features**
- `replay_start()` - Start replay buffer
- `replay_stop()` - Stop replay buffer
- `replay_save()` - Save replay highlight
- `virtualcam_start()` - Start virtual camera
- `virtualcam_stop()` - Stop virtual camera
- `transition_set()` - Configure scene transitions
- `obs_status()` - Get comprehensive OBS status
- `help()` - Built-in help system

## Prerequisites

- **Python 3.10+** (3.9 no longer supported for new features)
- **OBS Studio 28.0+** with WebSocket server enabled
  - OBS → Tools → WebSocket Server Settings → Enable server
- **MCPB CLI** (for building packages): `npm install -g @anthropic-ai/mcpb`

## 🚀 Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### 📦 Quick Start
Run immediately via `uvx`:
```bash
uvx obs-studio-mcp
```

### 🎯 Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "obs-studio-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/obs-mcp", "run", "obs-studio-mcp"]
  }
}
```
### 📦 **PyPI Package Install (RECOMMENDED)**

**Fastest Installation - Production Ready:**

```bash
pip install obs-studio-mcp
```

**Claude Desktop Integration:**
- Open Claude Desktop
- Settings → MCP Servers
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

### 🎯 **Claude Desktop (MCPB Package)**

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
   - Settings → MCP Servers
   - **Drag and drop** the `.mcpb` file
   - Configure OBS WebSocket settings in Claude Desktop

3. **Verify Installation:**
   ```
   Claude: "Check my OBS streaming status"
   # Claude will automatically use the MCP server
   ```

### 🛠️ **Other MCP Clients (Cursor, Windsurf, etc.)**

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

## 📚 **Documentation**

### **ADN Content Notes**
Comprehensive Advanced Memory Network documentation:
- **[OBS MCP Server](docs/adn-notes/OBS-MCP-Server.md)** - Complete technical overview, use cases, and enhancement roadmap
- **[OBS Studio](docs/adn-notes/OBS-Studio.md)** - In-depth analysis of OBS Studio and its underrated capabilities

### **Technical Documentation**
- **[Complete Documentation Structure](docs/COMPLETE_DOCUMENTATION_STRUCTURE.md)** - Full project documentation index
- **[Development Standards](docs/standards/)** - Code quality and development guidelines
- **[MCP Technical Guide](docs/mcp-technical/)** - MCP protocol implementation details

## 📦 **Building & Packaging**

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
├── manifest.json          # MCPB manifest with full tool registry
├── assets/
│   ├── icon.png          # 256x256 package icon
│   ├── screenshots/      # Feature screenshots
│   └── prompts/          # Extensive Claude Desktop prompts
│       ├── system.md     # System-level instructions
│       ├── user.md       # User interaction templates
│       ├── examples.json # Structured usage examples
│       ├── quick-start.md
│       ├── configuration.md
│       └── troubleshooting.md
└── src/
    └── obs_studio_mcp/   # Source code only (no dependencies)
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

## 🎬 **Usage Examples**

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

## License

MIT License


## 🌐 Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10818**.
*(Assigned ports: **10818** (Web dashboard frontend), **10819** (Web dashboard backend (API)))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10818` in your browser.
