# virtualization-mcp - Professional VirtualBox & Hyper-V Management for Claude Desktop

**v1.2.0 - FastMCP 3.1 with prompts, skills, and SOTA web dashboard**

> **âœ… Production Ready**: Full-featured VirtualBox and Hyper-V management through Claude Desktop with 60+ operations, FastMCP 3.1 prompts/skills, and optional LLM sampling in tools.

[![FastMCP](https://img.shields.io/badge/FastMCP-3.1+-blue)](https://github.com/jlowin/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![VirtualBox](https://img.shields.io/badge/VirtualBox-7.0+-orange)](https://virtualbox.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-499%20passing-brightgreen)](./tests)
[![Coverage](https://img.shields.io/badge/coverage-39%25-yellow)](./coverage.xml)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-black)](https://github.com/astral-sh/ruff)

---

## ðŸš€ What is virtualization-mcp?

virtualization-mcp is a professional Model Context Protocol (MCP) server that brings comprehensive VirtualBox and Hyper-V management to Claude Desktop and other MCP clients. Manage VMs with natural language; use the web dashboard for live console view and a dedicated **Prompts & Skills** page for FastMCP 3.1 prompts and bundled skills.

### âœ¨ Key Highlights

- **ðŸŽ¯ 5 Portmanteau Tools** - Clean, organized interface with 60+ operations
- **âš¡ FastMCP 3.1** - Prompts (`virtualization_expert`), skills (virtualization-expert), Context, progress reporting, optional `suggest_config` sampling
- **ðŸŒ Web dashboard** - Frontend 10700, Backend 10701; **Prompts & Skills** page lists and displays prompt/skill content
- **ðŸ”„ Switchable Modes** - Production (5 tools) or Testing (60+ tools)
- **ðŸ“– 100% Documented** - Comprehensive docstrings for every operation
- **ðŸ§ª 499 Passing Tests** - Robust test suite
- **ðŸŒ Cross-Platform** - Windows, macOS, Linux support
- **Ports** - Webapp: 10700 (frontend), 10701 (backend). MCP HTTP/SSE: 10702 (set `VIRTUALIZATION_MCP_PORT` to override).

---

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx virtualization-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "virtualization-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/virtualization-mcp", "run", "virtualization-mcp"]
  }
}
```
### For Claude Desktop (Recommended)

1. **Download MCPB Package:**
   - Go to [Releases](https://github.com/sandraschi/virtualization-mcp/releases/latest)
   - Download `virtualization-mcp-{version}.mcpb`

2. **Install in Claude Desktop:**
   - Open Claude Desktop
   - Go to Settings â†’ Extensions
   - Drag and drop the `.mcpb` file
   - Restart Claude Desktop

3. **Start Managing VMs:**
   ```
   "List all my virtual machines"
   "Create a new Ubuntu VM with 4GB RAM"
   "Take a snapshot of my-vm"
   ```

### For Python / Development

```bash
# From GitHub release
pip install https://github.com/sandraschi/virtualization-mcp/releases/download/v1.0.1b2/virtualization_mcp-1.0.1b2-py3-none-any.whl

# Or from git
pip install git+https://github.com/sandraschi/virtualization-mcp.git

# Or for development
git clone https://github.com/sandraschi/virtualization-mcp.git
cd virtualization-mcp
uv sync --dev
```

### Prerequisites

- **VirtualBox 7.0+** installed and in PATH
- **Python 3.10+** (for manual installation)
- **Claude Desktop** (for MCPB installation)

---

## ðŸŽ¯ Features

### VM Lifecycle Management
- Create VMs from templates or custom configurations
- Start, stop, pause, resume, reset VMs
- Clone VMs (full or linked clones)
- Delete VMs with optional disk cleanup
- Get detailed VM information and metrics

### Storage Management
- Create virtual disks (VDI, VMDK, VHD formats)
- Attach/detach storage devices
- Manage storage controllers (IDE, SATA, SCSI, NVMe)
- Configure disk properties and settings
- Shared folder management

### Network Configuration
- Configure network adapters (NAT, Bridged, Host-only, Internal)
- Set up port forwarding rules
- Manage host-only networks
- Advanced network adapter configuration

### Snapshot Management
- Create snapshots with descriptions
- List all snapshots for a VM
- Restore VMs to previous snapshots
- Delete individual snapshots
- Snapshot-based cloning

### System Information
- Host system information
- VirtualBox version details
- Available OS types
- VM performance metrics
- Screenshot capture

---

## ðŸ› ï¸ Tool Modes

### Production Mode (Default) - 6-7 Tools

Clean, organized interface perfect for daily use:

1. **vm_management** - Complete VM lifecycle (10 operations)
2. **network_management** - Network configuration (5 operations)
3. **snapshot_management** - Snapshot operations (4 operations)
4. **storage_management** - Storage & disk management (6 operations)
5. **system_management** - System info & diagnostics (5 operations)
6. **discovery_management** - Help & tool info (4 operations)
7. **hyperv_management** - Hyper-V VMs (4 operations, Windows only)

**Total:** 33 operations in 6 tools (7 on Windows)

**Note:** discovery_management is app-specific help (NOT the same as MCP protocol's native tools/list)

### Testing Mode - 60+ Tools

All individual functions plus portmanteau tools for development and debugging.

**Switch modes in `mcp_config.json`:**
```json
{
  "env": {
    "TOOL_MODE": "production"  // or "testing"
  }
}
```

See [Tool Mode Configuration](docs/mcp-technical/TOOL_MODE_CONFIGURATION.md) for details.

---

## ðŸ’¡ Usage Examples

### Basic VM Management

```
User: "List all my VMs"
Claude: Uses vm_management(action="list")

User: "Create a Ubuntu development VM"
Claude: Uses vm_management(action="create", vm_name="ubuntu-dev", 
        os_type="Ubuntu_64", memory_mb=4096, disk_size_gb=50)

User: "Start the VM ubuntu-dev"
Claude: Uses vm_management(action="start", vm_name="ubuntu-dev")
```

### Snapshot Workflow

```
User: "Create a snapshot of ubuntu-dev called 'clean-state'"
Claude: Uses snapshot_management(action="create", vm_name="ubuntu-dev",
        snapshot_name="clean-state")

User: "List all snapshots for ubuntu-dev"
Claude: Uses snapshot_management(action="list", vm_name="ubuntu-dev")

User: "Restore ubuntu-dev to the clean-state snapshot"
Claude: Uses snapshot_management(action="restore", vm_name="ubuntu-dev",
        snapshot_name="clean-state")
```

### Network Configuration

```
User: "Set up NAT networking on my VM"
Claude: Uses network_management(action="configure_adapter", 
        vm_name="my-vm", adapter_slot=0, network_type="nat")

User: "Create a host-only network called dev-network"
Claude: Uses network_management(action="create_network",
        network_name="dev-network")
```

---

## ðŸ“– Documentation

### Quick Start
- [Quick Start Guide](docs/QUICK_START.md) - Get started in 5 minutes
- [Claude Desktop Setup](CLAUDE_DESKTOP_SETUP.md) - Integration guide

### Technical Documentation
- [Tool Mode Configuration](docs/mcp-technical/TOOL_MODE_CONFIGURATION.md) - Switch between modes
- [FastMCP 3.1.1+ Compliance](docs/mcp-technical/FASTMCP_3.1.1+_COMPLIANCE.md) - Integration details
- [Docstring Coverage](docs/mcp-technical/DOCSTRING_COVERAGE.md) - 100% coverage report
- [Project Status](docs/mcp-technical/PROJECT_STATUS_FINAL.md) - Complete status

### MCPB Packaging
- [MCPB Building Guide](docs/mcpb-packaging/MCPB_BUILDING_GUIDE.md) - Package creation
- [Implementation Summary](docs/mcpb-packaging/MCPB_IMPLEMENTATION_SUMMARY.md) - Technical details

### User Guides
- [VM Management](docs/concepts/vm_management.md) - VM operations
- [Network Configuration](docs/concepts/network_configuration.md) - Networking
- [Snapshot Management](docs/concepts/snapshot_management.md) - Snapshots
- [Storage Management](docs/concepts/storage_management.md) - Disks & storage

---

## ðŸŽ¨ AI Prompt Templates

8 comprehensive templates included (25+ KB total):

- **backup-strategies.md** - Backup and disaster recovery patterns
- **complete-scenarios.md** - Full deployment scenarios
- **network-configuration.md** - Network setup guides
- **security-best-practices.md** - Security hardening
- **snapshot-management.md** - Snapshot strategies
- **storage-optimization.md** - Storage configuration
- **vm-deployment-strategies.md** - Deployment patterns (345 lines!)
- **vm-templates.md** - Template usage and customization

---

## ðŸ—ï¸ Architecture

### Built With:
- **FastMCP 3.1.1+.4** - Latest MCP framework
- **UV** - Modern Python package manager
- **Ruff** - Fast Python linter & formatter
- **pytest** - Comprehensive test suite
- **VirtualBox 7.0+** - Virtualization platform

### Tool Organization:
- **Portmanteau Tools** - Action-based consolidated operations
- **Individual Tools** - Direct function access (testing mode)
- **Service Layer** - Business logic and validation
- **VBox Adapter** - VirtualBox integration
- **Plugin System** - Extensible architecture

---

## ðŸ§ª Testing

### Run Tests:
```bash
# Install development dependencies
uv sync --dev

# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=virtualization_mcp --cov-report=term-missing
```

### Test Statistics:
- **Total Tests:** 605
- **Passing:** 499 (82.5%)
- **Coverage:** 39% â†’ Target: 80% (GLAMA Gold Standard)
- **Integration Tests:** VBox-aware (mocked when unavailable)

---

## ðŸ”§ Configuration

### Basic Setup (Claude Desktop):

```json
{
  "mcpServers": {
    "virtualization-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/virtualization-mcp",
        "run",
        "virtualization-mcp"
      ],
      "env": {
        "TOOL_MODE": "production",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Advanced Configuration:

See `.env.example` for all available settings:
- Tool mode selection
- VirtualBox path configuration
- Logging levels
- Timeouts and limits
- Default VM settings
- Feature flags

---

## ðŸ¤ Contributing

We welcome contributions! Please see:
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute
- [Security Policy](SECURITY.md) - Security considerations
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues

### Development Setup:

```bash
# Clone repository
git clone https://github.com/sandraschi/virtualization-mcp.git
cd virtualization-mcp

# Install with UV
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check .
```

---

## ðŸ“Š Project Status

- âœ… **Production Ready** - v1.0.1b2 released
- âœ… **Quality** - 0 linting errors, 499 tests passing
- âœ… **Documentation** - 100% docstring coverage
- âœ… **MCPB Packaged** - Optimized for Claude Desktop
- âœ… **FastMCP Compliant** - Version 3.1.1+.4
- âœ… **Clean Repository** - Professional organization

See [Project Status](docs/mcp-technical/PROJECT_STATUS_FINAL.md) for complete details.

---

## ðŸš€ Roadmap & Extensions

### **Coming Soon**
- **VM Templates**: Pre-built configurations for Ubuntu, Windows, macOS
- **Advanced Monitoring**: Real-time performance metrics and health checks
- **Security Features**: Vulnerability scanning and access control
- **Enhanced Networking**: Visual topology mapping and advanced port management

### **Planned Features**
- **Plugin System**: Extensible architecture for custom functionality
- **Cloud Integration**: AWS/Azure VM synchronization
- **CI/CD Support**: Jenkins/GitHub Actions integration
- **Interactive CLI**: Direct command-line interface

### **Quick Wins**
- âœ… Progress tracking for long operations
- âœ… Health check endpoints
- âœ… Configuration validation tools
- âœ… Operation history and audit logging

*See [Extensions & Improvements Guide](docs/planning/EXTENSIONS_AND_IMPROVEMENTS.md) for detailed roadmap.*

---

## ðŸ”— Links

- **Repository:** https://github.com/sandraschi/virtualization-mcp
- **Releases:** https://github.com/sandraschi/virtualization-mcp/releases
- **Issues:** https://github.com/sandraschi/virtualization-mcp/issues
- **Latest Release:** [v1.0.1b2](https://github.com/sandraschi/virtualization-mcp/releases/tag/v1.0.1b2)

---

## ðŸ“§ Contact

**Author:** Sandra Schi  
**Email:** sandraschipal@protonmail.com  
**GitHub:** [@sandraschi](https://github.com/sandraschi)

---

## ðŸ“„ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ðŸŽ‰ Quick Start

1. Download `.mcpb` from releases
2. Drop into Claude Desktop
3. Ask: **"What can you do with VirtualBox?"**
4. Start managing VMs with natural language!

**Manage VirtualBox VMs effortlessly through Claude Desktop!** ðŸš€


## ðŸŒ Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10700**.
*(Assigned ports: **10700** (Web dashboard))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10700` in your browser.

