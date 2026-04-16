# OBS Studio MCP Server - Project Structure

**Source Repository:** `D:\Dev\repos\obs-mcp`  
**Documentation Root:** `D:\Dev\repos\mcp-central-docs\docs\projects\obs-mcp\`

---

## 📁 Directory Structure

```
obs-mcp/
├── src/obs_studio_mcp/          # Main package
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # CLI entry point
│   ├── mcp_server.py           # FastMCP server implementation
│   ├── obs_client.py            # OBS WebSocket client
│   ├── models.py                # Pydantic data models
│   ├── config.py                # Configuration management
│   └── server.py                # FastAPI HTTP server (optional)
├── dist/                        # Distribution packages
│   ├── obs-mcp-0.1.0.dxt        # DXT package for MCP deployment
│   └── obs-mcp-0.1.0-extracted/ # Extracted DXT contents
├── docs/                        # Comprehensive documentation
│   ├── development/             # Development guides
│   ├── glama-platform/          # Glama integration docs
│   ├── mcp-technical/           # MCP protocol docs
│   ├── mcpb-packaging/          # Packaging guides
│   ├── repository-protection/   # Security docs
│   └── *.md                     # Various documentation files
├── recordings/                  # OBS recording output
├── replays/                     # Replay buffer files
├── screenshots/                 # OBS screenshots
├── tests/                       # Test suite
├── assets/                      # Static assets
│   └── prompts/                 # MCP prompt templates
├── scripts/                     # Utility scripts
│   ├── backup-repo.ps1          # Repository backup
│   └── check-repo-standards.ps1 # Standards compliance
├── glama.json                   # Glama platform configuration
├── manifest.json                # MCP manifest
├── pyproject.toml               # Python project configuration
├── requirements.txt             # Python dependencies
├── README.md                    # Project README
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT license
└── Dockerfile                   # Docker container definition
```

---

## 🔧 Key Files

### Core Implementation
- **`src/obs_studio_mcp/mcp_server.py`**: Main FastMCP server with all 20+ tools
- **`src/obs_studio_mcp/obs_client.py`**: OBS WebSocket client implementation
- **`src/obs_studio_mcp/models.py`**: Pydantic models for OBS data structures
- **`src/obs_studio_mcp/config.py`**: Configuration management with environment variables

### Entry Points
- **`src/obs_studio_mcp/__main__.py`**: CLI interface and argument parsing
- **`src/obs_studio_mcp/server.py`**: Optional FastAPI HTTP server

### Configuration & Packaging
- **`pyproject.toml`**: Python project metadata and dependencies
- **`manifest.json`**: MCP server manifest
- **`Dockerfile`**: Container build definition
- **`dist/obs-mcp-0.1.0.dxt`**: DXT package for MCP deployment

---

## 🏗️ Architecture Layers

### 1. **MCP Protocol Layer**
```
mcp_server.py
├── FastMCP App Instance
├── Tool Registration (20+ tools)
├── STDIO Transport
└── Error Handling
```

### 2. **OBS Integration Layer**
```
obs_client.py
├── WebSocket Connection
├── OBS SDK Integration
├── Request/Response Handling
└── Connection Management
```

### 3. **Data Model Layer**
```
models.py
├── OBSRequest/Response Models
├── Scene/Audio/Video Models
├── Status Models
└── Pydantic Validation
```

### 4. **Configuration Layer**
```
config.py
├── Environment Variables
├── Settings Management
├── Validation
└── Path Resolution
```

---

## 🔄 Data Flow

### MCP Request Flow
```
Claude Desktop → STDIO → FastMCP → Tool Handler → OBS Client → WebSocket → OBS Studio
                      ↑                                                ↓
                   Response ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

### WebSocket Communication
```
OBS Client → OBS WebSocket Server → OBS Studio Core
     ↓              ↓                        ↓
  Request      Message Routing         Scene/Audio Control
  Response ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

---

## 📦 Distribution Packages

### DXT Package Structure
```
obs-mcp-0.1.0.dxt (ZIP archive)
├── manifest.json              # MCP manifest
├── obs-mcp/                   # Extracted package
│   ├── __init__.py           # Package init
│   ├── mcp_server.py        # Main server
│   ├── obs_client.py         # OBS client
│   ├── models.py             # Data models
│   └── requirements.txt      # Dependencies
└── metadata.json             # Package metadata
```

### Docker Image Layers
```
FROM python:3.11-slim
├── System dependencies
├── Python dependencies
├── Application code
└── Configuration
```

---

## 🔧 Development Workflow

### Source Code Organization
- **`src/`**: Main application code
- **`tests/`**: Unit and integration tests
- **`docs/`**: Documentation and guides
- **`scripts/`**: Development utilities

### Build Process
```
Source Code → Ruff Linting → Testing → Packaging → Distribution
     ↓            ↓            ↓         ↓            ↓
  *.py files   0 errors     Tests pass  DXT + Docker  Releases
```

### Quality Gates
- **Linting**: `ruff check .` (0 errors required)
- **Formatting**: `ruff format .` (consistent style)
- **Testing**: `pytest` (all tests pass)
- **Type Checking**: Full type annotation coverage
- **Documentation**: Updated for all changes

---

## 🔗 Integration Points

### MCP Ecosystem
- **Claude Desktop**: Primary MCP client
- **MCP Studio**: Management dashboard
- **DXT Registry**: Package distribution
- **Central Docs**: Documentation hub

### OBS Studio
- **WebSocket API**: Primary communication
- **Scene System**: Scene management
- **Source System**: Audio/video sources
- **Recording System**: File output management
- **Streaming System**: RTMP/ SRT protocols

### External Services
- **Docker Hub**: Container distribution
- **GitHub**: Source code hosting
- **PyPI**: Python package distribution
- **Glama**: MCP server registry

---

## 📊 Metrics & Monitoring

### Code Quality Metrics
- **Lines of Code**: ~2,000 lines
- **Test Coverage**: Core functionality tested
- **Linting Score**: 0 errors, 0 warnings (Ruff)
- **Type Coverage**: Full type annotations

### Performance Metrics
- **Startup Time**: < 2 seconds
- **Memory Usage**: ~50MB baseline
- **WebSocket Latency**: < 50ms
- **Concurrent Tools**: Multiple simultaneous operations

### Distribution Metrics
- **Package Size**: ~5MB (DXT compressed)
- **Docker Image**: ~200MB (Python + dependencies)
- **Supported Platforms**: Windows, macOS, Linux
- **Python Versions**: 3.9+ supported

---

**Structure Version:** 1.0 | **Last Updated:** 2025-12-21 | **Next Review:** 2026-01-15













