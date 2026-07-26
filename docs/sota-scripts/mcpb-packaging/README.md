# MCPB Packaging Tools

State-of-the-art automation for MCPB (Model Context Protocol Bundle) packaging across all MCP server repositories.

## Overview

This directory contains comprehensive automation tools for setting up, building, and verifying MCPB packages for all MCP server repositories in the workspace.

## Tools

### setup_all_mcpb.ps1

**Comprehensive MCPB automation script for all MCP repos.**

#### Features
- **Setup Mode**: Automatically creates MCPB directory structure, assets, and manifests for new repos
- **Build Mode**: Builds MCPB packages using official MCPB CLI
- **Verify Mode**: Validates built packages and checks contents
- **Batch Processing**: Process multiple repos with filtering

#### Usage Examples

```powershell
# Setup MCPB structure for specific repos
.\setup_all_mcpb.ps1 -Action setup -RepoFilter "blender-mcp,calibre-mcp"

# Build MCPB packages for all repos
.\setup_all_mcpb.ps1 -Action build

# Verify all built packages
.\setup_all_mcpb.ps1 -Action verify

# Setup and build specific repo
.\setup_all_mcpb.ps1 -Action setup -RepoFilter "my-mcp-repo"
.\setup_all_mcpb.ps1 -Action build -RepoFilter "my-mcp-repo"
```

#### What It Creates

For each MCP repo, the script sets up:

```
repo/
├── dist/                    # ✅ MCPB packages (repo root)
│   └── repo-name.mcpb
├── mcpb/                    # Build configuration
│   ├── manifest.json        # MCPB manifest (v0.2 format)
│   ├── assets/
│   │   ├── icon.png        # 256x256 PNG icon
│   │   └── prompts/        # Claude Desktop prompts
│   │       ├── system.md
│   │       ├── user.md
│   │       └── examples.json
│   └── src/                 # Copied source code
└── README.md
```

#### MCPB Standards Compliance

- ✅ **Manifest v0.2** format
- ✅ **No dependencies** in packages (runtime handles them)
- ✅ **Full source code** inclusion
- ✅ **Comprehensive prompts** for Claude Desktop
- ✅ **Proper assets** (icons, screenshots)
- ✅ **Unicode-clean** (no encoding errors)
- ✅ **Repo root `/dist`** placement

#### Requirements

- PowerShell 7+
- MCPB CLI (`npm install -g @anthropic-ai/mcpb`)
- Source code in `src/` directory
- Python MCP server implementation

## Integration

This script integrates with:
- **MCP Central Docs** standards
- **MCPB CLI** for official packaging
- **Workspace automation** for batch processing
- **Quality assurance** for package validation

## Changelog

### v1.0.0
- Initial release
- Full MCPB automation for all MCP repos
- Unicode-clean implementation
- Proper error handling and validation

## See Also

- [MCPB Packaging Standards](../../docs/mcpb-packaging/MCPB_PACKAGING_STANDARDS.md)
- [MCP Server Builder](../mcp-server-builder/)
- [Repo Standards](../repo-standards/)



