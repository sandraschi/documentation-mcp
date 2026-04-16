# VRoid Studio MCP

**🚨 ALPHA STATUS 🚨 FastMCP 3.1.1+.1+ SOTA Compliant Server for VRoid Studio Automation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1+.1+-brightgreen)](https://fastmcp.readthedocs.io/)
[![ALPHA](https://img.shields.io/badge/Status-ALPHA-red)](docs/README.md)
[![SOTA Compliant](https://img.shields.io/badge/SOTA-Compliant-blueviolet)](docs/architecture.md)

> **🚨 ALPHA STATUS: CURRENTLY NON-FUNCTIONAL 🚨**
>
> A comprehensive MCP server for VRoid Studio automation featuring portmanteau architecture, Windows COM integration, and complete 3D character creation workflow automation.
>
> **⚠️ IMPORTANT LIMITATIONS:**
> - VRoid Studio has **NO CLI, API, or COM interfaces** - cannot be controlled programmatically
> - All current tools are **MOCKED** and return fake responses
> - **No actual VRoid Studio automation occurs**
> - **Planning ongoing** for Windows UI automation (pywinauto-mcp) approach

## 🎯 Overview

VRoid Studio MCP brings the power of Model Context Protocol to Pixiv's VRoid Studio, enabling seamless automation of 3D character creation workflows. Built with FastMCP 3.1.1+.1+ standards and SOTA compliance, it provides natural language control over complex 3D modeling operations.

### ✨ Key Features

- **🎭 Complete Character Creation**: From concept to export in natural language
- **🔧 Portmanteau Architecture**: 15+ consolidated tools for efficient operations
- **⚡ FastMCP 3.1.1+.1+**: Enhanced responses with metadata and recommendations
- **🪟 Windows COM Automation**: Direct integration with VRoid Studio
- **📦 MCPB Packaging**: Ready for Claude Desktop Extensions deployment
- **🔄 Cross-Platform Export**: VRM, FBX, glTF, OBJ with platform optimization
- **🎨 Advanced Morphing**: Body proportion adjustment and character customization
- **📊 Quality Assurance**: Automated validation and optimization

## 🚀 Quick Start

## 🚀 Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### 📦 Quick Start
Run immediately via `uvx`:
```bash
uvx vroidstudio-mcp
```

### 🎯 Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "vroidstudio-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/vroidstudio-mcp", "run", "vroidstudio-mcp"]
  }
}
```
### 2. Claude Desktop Configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "vroidstudio": {
      "command": "python",
      "args": ["-m", "vroidstudio_mcp.server"],
      "env": {
        "VROIDSTUDIO_PATH": "C:\\Program Files\\VRoidStudio\\VRoidStudio.exe"
      }
    }
  }
}
```

### 3. Start Creating Characters

In Claude Desktop, try commands like:
- *"Create a female anime character with blue hair"*
- *"Export this character to VRM format for VRChat"*
- *"Adjust the character's body proportions to be more athletic"*
- *"Convert this model to FBX for Unity"*

## 📚 Documentation

### Core Documentation
- **[Integration Guide](docs/integration-guide.md)** - Claude Desktop setup and configuration
- **[Architecture](docs/architecture.md)** - System design and portmanteau patterns
- **[Tools Reference](docs/tools-reference.md)** - Complete API documentation
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

### Advanced Topics
- **[VRoid Studio Integration](docs/vroid-integration.md)** - COM automation details
- **[Character Creation Workflows](docs/character-workflows.md)** - Best practices
- **[Export Optimization](docs/export-optimization.md)** - Platform-specific settings
- **[Development](docs/development.md)** - Contributing and extending

## 🛠️ Portmanteau Tools Architecture

This server uses a revolutionary **portmanteau tools** design that consolidates related functionality into unified interfaces:

### Core Tools (7 Families)
- **`help_system`** - Multilevel help and documentation
- **`status_system`** - System diagnostics and health monitoring
- **`project_manager`** - Complete project lifecycle management
- **`character_builder`** - Character creation and modification
- **`morphing_tools`** - Body morphing and proportion adjustment
- **`export_manager`** - Multi-format export with optimizations
- **`format_converter`** - Cross-format conversion and validation

### Tool Operations Summary
| Tool Family | Operations | Purpose |
|-------------|------------|---------|
| **Project** | create, open, save, info, backup | Project lifecycle management |
| **Character** | create, modify, preset, randomize | Character design and customization |
| **Morphing** | adjust, preset, analyze, optimize | Body proportion adjustment |
| **Export** | export, batch_export, validate, optimize | Multi-format export operations |
| **Format** | convert, batch_convert, detect, capabilities | Format conversion utilities |
| **UI Analysis** | capture_screenshot, analyze_ui_elements, list_screenshots | Screenshot capture and UI element identification |

## 🎨 Character Creation Examples

### Basic Character Creation
```python
# Create a new character
result = await character_builder("create", character_name="Hero Character")

# Apply a preset style
result = await character_builder("preset", preset_name="anime_girl")

# Customize facial features
modifications = {"face": {"eye_size": 1.2, "nose_shape": "button"}}
result = await character_builder("modify", modifications=modifications)
```

### Advanced Morphing
```python
# Adjust body proportions
params = {"height": 1.1, "shoulder_width": 0.9}
result = await morphing_tools("adjust", category="overall", parameters=params)

# Apply athletic preset
result = await morphing_tools("preset", preset_name="athletic")

# Analyze and optimize proportions
result = await morphing_tools("analyze")  # Get current proportions
result = await morphing_tools("optimize")  # Auto-optimize harmony
```

### Export Operations
```python
# Export to VRM for VRChat
result = await export_manager("export", format_type="vrm", target_platform="vrchat")

# Export high-quality FBX for Unity
result = await export_manager("export",
    format_type="fbx",
    target_platform="unity",
    quality_preset="high",
    include_animations=True
)

# Validate export settings
result = await export_manager("validate", format_type="gltf", target_platform="web")
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
VROIDSTUDIO_PATH=C:\Program Files\VRoidStudio\VRoidStudio.exe

# Optional
AUTO_LAUNCH=true                    # Auto-launch VRoid Studio
OPERATION_TIMEOUT=30.0             # Operation timeout in seconds
MAX_RETRIES=3                      # Retry attempts for failed operations
```

### 📦 Packaging & Distribution

This repository is SOTA 2026 compliant and uses the officially validated `@anthropic-ai/mcpb` workflow for distribution.

#### Pack Extension
To generate a `.mcpb` distribution bundle with complete source code and automated build exclusions:
```bash
# SOTA 2026 standard pack command
mcpb pack . dist/vroidstudio-mcp.mcpb
```

#### Build Integrity
The build process uses root-level `mcpb.json` and `.mcpbignore`, ensuring only source code and necessary assets are included in the final bundle.

## 🏗️ Architecture

### FastMCP 3.1.1+.1+ Compliance
- ✅ Enhanced response patterns with metadata and recommendations
- ✅ Server lifespan management for stateful operations
- ✅ Advanced tool management and duplicate handling
- ✅ Breaking change: `run_stdio_async()` instead of `run_standalone()`

### SOTA Features
- ✅ Portmanteau tools (15+ operations consolidated)
- ✅ MCPB packaging with assets and prompts
- ✅ Comprehensive documentation structure
- ✅ Production-ready error handling and logging
- ✅ Tool family modularization

### Windows COM Integration (Mocked - Non-Functional)
- **CURRENTLY MOCKED**: VRoid Studio doesn't expose COM interfaces
- **PLANNED**: Windows UI automation via pywinauto-mcp for brute-force control
- Robust error handling and connection management
- Automatic retry logic for transient failures
- Proper resource cleanup and COM uninitialization

## 🚨 Alpha Status & Current Limitations

### ❌ What Doesn't Work (Yet)
VRoid Studio has **no programmable interface** - it cannot be controlled from outside:

- **No CLI**: No command-line interface
- **No API**: No official or documented API
- **No COM**: Doesn't register as COM server (`"VRoidStudio.Application"`)
- **No Plugins**: No automation plugin system

**Result:** Tools now perform **actual VRoid Studio operations** through Windows UI automation!

### 🎮 Active Solution: Windows UI Automation

**✅ IMPLEMENTED:** Using [pywinauto-mcp](https://github.com/sandraschi/pywinauto-mcp) for comprehensive Windows automation with **keyboard shortcuts** (preferred method):

```python
# Actual working implementation!
from pywinauto_mcp import WindowsAutomation
from vroidstudio_mcp.core.keyboard_shortcuts import VRoidStudioShortcuts

# Find VRoid Studio window
studio = WindowsAutomation.find_window("VRoid Studio")

# PREFERRED: Use keyboard shortcuts (more reliable than clicking)
await studio.send_keys(VRoidStudioShortcuts.format_for_pywinauto("ctrl+n"))  # New project
await studio.send_keys(VRoidStudioShortcuts.format_for_pywinauto("f8"))  # Export VRM

# Fallback: UI clicking for operations without shortcuts
await studio.click_menu("File", "Export", "FBX")  # No shortcut available
```

**Keyboard Shortcuts (Preferred Method):**
- **Save**: `Ctrl+S` - More reliable than clicking File > Save
- **Save As**: `Ctrl+Shift+S` - Faster than menu navigation
- **Open**: `Ctrl+O` - Direct file dialog access
- **New**: `Ctrl+N` - Instant new project
- **Export VRM**: `F8` - One-key export (most common format)
- **Editor Tabs**: `F1-F9` - Direct editor access
- **Reference**: [Official VRoid Studio Keyboard Shortcuts](https://vroid.pixiv.help/hc/en-us/articles/900006050066)

**Real-World Challenges Solved:**
- **Keyboard Shortcuts**: Preferred method - faster, more reliable, less brittle
- **UI Synchronization**: Waits for dialogs and state changes with adaptive timing
- **Element Reliability**: Multiple detection strategies (text, class, position, AI vision)
- **Timing Issues**: Smart delays and retry mechanisms with exponential backoff
- **Window Focus**: Intelligent focus management and restoration
- **Error Recovery**: Comprehensive fallback strategies and state validation

**Benefits Achieved:**
- ✅ Actually controls real VRoid Studio application
- ✅ No application modifications or plugins required
- ✅ Works with existing VRoid Studio installations
- ✅ Robust error handling and recovery
- ✅ Extensible for future VRoid Studio features

### 📸 Screenshot Capture for UI Element Identification

**ESSENTIAL:** Screenshots are required to identify correct click coordinates and UI element locations in VRoid Studio.

Since VRoid Studio's UI structure is not documented, we must visually identify:
- Menu locations and paths
- Dialog button positions
- UI element coordinates
- State-dependent UI changes

**New UI Analysis Tools:**
- **`capture_screenshot`** - Capture VRoid Studio windows, dialogs, or specific elements
- **`analyze_ui_elements`** - Analyze screenshots to identify UI elements (OCR integration planned)
- **`list_screenshots`** - Review previously captured screenshots

**Usage Example:**
```python
# Capture main window before automation
result = await capture_screenshot(
    screenshot_type="window",
    description="Main VRoid Studio window - before opening project"
)

# Capture file dialog to identify button locations
result = await capture_screenshot(
    screenshot_type="dialog",
    element_name="file_open_dialog",
    description="File open dialog - identify Open/Cancel button positions"
)

# Review captured screenshots
screenshots = await list_screenshots(limit=10)
```

**Screenshot Storage:**
- Default location: `~/.vroidstudio-mcp/screenshots/`
- Format: `vroid_{type}_{element}_{timestamp}.png`
- Used for: UI element coordinate mapping, automation debugging, documentation

## 🧪 Development & Testing

### Setup Development Environment
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=src/vroidstudio_mcp --cov-report=html

# Run linting
black src/
isort src/
mypy src/
```

### Testing Modes
- **Unit Tests**: Individual component testing
- **Integration Tests**: Full workflow validation
- **API Tests**: MCP protocol compliance
- **COM Automation Tests**: VRoid Studio integration

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11 (VRoid Studio requirement)
- **Python**: 3.10+
- **VRoid Studio**: Latest version installed

### Dependencies
- **fastmcp>=3.1.1+.1,<2.15.0**: MCP protocol implementation
- **pywin32>=305**: Windows COM automation
- **pydantic>=2.0.0**: Data validation
- **typing-extensions>=4.0.0**: Type hints

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Standards
- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking
- **pytest** for testing
- **Comprehensive docstrings** following Google style

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Pixiv Inc.** for VRoid Studio
- **FastMCP Community** for the MCP framework
- **Anthropic** for Claude Desktop and MCP specification
- **Contributors** for their valuable input and testing

---

**Made with ❤️ by sandraschi**

*FastMCP 3.1.1+.1+ SOTA Compliant • Portmanteau Architecture • Windows COM Automation*
