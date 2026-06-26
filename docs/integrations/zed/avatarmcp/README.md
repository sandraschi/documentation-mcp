# AvatarMCP Zed Extension

FastMCP 3.1.1+.3 compatible VRM avatar management and animation server with VRChat OSC integration and agentic sampling workflows, packaged as a Zed IDE extension.

## Features

- VRM 2.0 Support: Load and manage VRM 2.0 avatar models with real-time manipulation
- Agentic Sampling Workflows: LLM-driven orchestration of complex avatar behaviors (SEP-1577)
- VRChat OSC Integration: Seamless communication with VRChat for avatar control
- 16 Portmanteau Tools: Consolidated functionality for avatar management
- Conversational Error Handling: Friendly, helpful error messages instead of technical jargon

## Installation

### Prerequisites

1. Rust Toolchain: Install via rustup
2. Wasm Target: rustup target add wasm32-wasip1
3. Zed IDE: Download from zed.dev
4. AvatarMCP Server: Install from GitHub

### Build Extension

```bash
# Unix/Mac
./build.sh

# Windows
.\build.ps1
```

### Install in Zed

1. Open Zed IDE
2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Linux/Windows)
3. Type "zed: extensions"
4. Select "Install Dev Extension"
5. Choose this directory (avatarmcp/)

## Configuration

The extension expects AvatarMCP to be available via uv run --project path/to/avatar-mcp --mcp. Update the path in src/lib.rs to match your AvatarMCP installation location.

## Usage

Once installed, AvatarMCP will appear in Zed
'
s Assistant panel as "AvatarMCP". You can then:

- Load VRM avatars
- Control animations and expressions
- Use sampling workflows for complex behaviors
- Integrate with VRChat via OSC
- Manage Unity desktop avatars

## Sampling Workflows

Leverage FastMCP 3.1.1+.3 sampling capabilities for agentic avatar orchestration.

## Architecture

This Zed extension acts as a bridge between Zed
'
s AI assistant and the AvatarMCP Python server.

## Troubleshooting

- Build fails: Ensure wasm32-wasip1 target is installed
- Server not found: Update the path to AvatarMCP in src/lib.rs
- Extension not loading: Check Zed logs for Wasm compilation errors

## License

MIT License - see AvatarMCP repository for full license details.

## Author

Sandra Schipal (sandraschipal@gmail.com)

