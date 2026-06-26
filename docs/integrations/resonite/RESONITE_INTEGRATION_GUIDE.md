# Resonite Integration Guide

**Last Updated:** 2025-12-22
**Status:** Beta (v0.1.1)
**Source Repo:** `D:\Dev\repos\resonite-mcp`

## Overview

This guide covers Resonite integration through the **Resonite MCP Server**, a FastMCP 3.1.1++ server that provides natural language control over the Resonite social VR platform.

The Resonite MCP Server enables Claude Desktop and Cursor IDE to interact with Resonite through:
- Avatar control and parameter manipulation
- World loading and session management
- ProtoFlux script execution
- OSC communication with Resonite
- Inventory management and asset handling
- Plugin system for extensibility

## Table of Contents

1. [Resonite Overview](#resonite-overview)
2. [How Resonite Compares](#how-resonite-compares)
3. [Resonite MCP Server](#resonite-mcp-server)
4. [Installation and Setup](#installation-and-setup)
5. [Configuration](#configuration)
6. [Tool Reference](#tool-reference)
7. [OSC Communication](#osc-communication)
8. [Session Management](#session-management)
9. [Avatar Control](#avatar-control)
10. [ProtoFlux Scripting](#protoflux-scripting)
11. [Inventory Management](#inventory-management)
12. [Plugin System](#plugin-system)
13. [HTTP API](#http-api)
14. [Troubleshooting](#troubleshooting)
15. [Best Practices](#best-practices)

## Resonite Overview

### What is Resonite?

Resonite is a social VR platform that provides:
- **Social VR Experience**: Multi-user virtual reality environments
- **Avatar System**: Customizable avatars with parameters and animations
- **World Creation**: User-generated content and worlds
- **ProtoFlux Scripting**: Visual programming system for interactive content
- **Asset Management**: Inventory system for user assets
- **OSC Integration**: Open Sound Control protocol for external control

### Key Features

- **Multi-platform Support**: PC, Quest, mobile devices
- **Real-time Collaboration**: Multi-user sessions and interactions
- **Visual Scripting**: ProtoFlux for creating interactive experiences
- **Asset Marketplace**: User-generated content sharing
- **OSC Protocol**: Bidirectional communication with external applications

For a deep dive into ProtoFlux visual programming, see the **[ProtoFlux Guide](./PROTOFLUX_GUIDE.md)**.

For practical ProtoFlux script examples and implementations, see the **[Useful ProtoFlux Scripts Guide](./USEFUL_PROTOFLUX_SCRIPTS.md)**.

For hands-on step-by-step tutorials perfect for beginners, see the **[ProtoFlux Hands-On Guide](./PROTOFLUX_HANDS_ON_GUIDE.md)**.

For information about running Resonite on different platforms (Quest, Pico, PC, mobile), see the **[Access Guide](./RESONITE_ACCESS_GUIDE.md)**.

For detailed information about importing and controlling 3D artifacts (VRM avatars, meshes, Gaussian splats), see the **[Artifacts Guide](./ARTIFACTS_GUIDE.md)**.

For World Labs Marble photogrammetry workflows and Unity bridging, see the **[Marble Integration Guide](./MARBLE_RESONITE_GUIDE.md)**.

### How Resonite Compares to Other VR Platforms

Resonite stands out from other social VR platforms through its focus on **creation, experimentation, and technical excellence**.

#### Quick Platform Comparison:

| Feature | Resonite | VRChat | AltspaceVR | Rec Room |
|---------|----------|--------|------------|----------|
| **Primary Focus** | Creation & Social | Social & UGC | Events & Social | Games & Social |
| **Programming** | ProtoFlux (Visual) | Udon (C#) | Limited | Game Maker |
| **User Creation** | Full 3D World Building | Avatars & Worlds | Avatars Only | Mini-games |
| **OSC Support** | Native | Limited | None | Limited |
| **Content Freedom** | Unlimited | Moderate | Moderate | Family-friendly |

#### Why Choose Resonite?

**Choose Resonite if you want:**
- **Advanced Creation Tools** - ProtoFlux, in-world building, professional 3D tools
- **Technical Experimentation** - OSC integration, custom scripting, open APIs
- **Creative Freedom** - No corporate restrictions, experimental content encouraged
- **Collaborative Building** - Real-time world editing with teams
- **Live Performances** - External control for concerts, installations, events

**Resonite excels at being a "professional VR creation platform" while maintaining social features.**

For a detailed comparison with other VR platforms, see the **[Platform Comparison Guide](./RESONITE_VS_OTHERS.md)**.

## Resonite MCP Server

### Architecture

The Resonite MCP Server follows FastMCP 3.1.1++ standards with:

- **Portmanteau Tool Organization**: Complex operations organized into logical tool groups
- **Pydantic Input Validation**: Type-safe parameter validation for all tools
- **Dual Interface Support**: MCP stdio protocol + HTTP REST API
- **Plugin System**: Extensible architecture for additional functionality
- **OSC Communication**: Real-time bidirectional communication with Resonite

### Implementation Status

- **âœ… Core OSC Communication**: 8 tools fully implemented
- **âœ… Avatar Control**: 3 tools fully implemented
- **âœ… Session Management**: 4 tools (3 fully implemented, 1 mock)
- **âš ï¸ Inventory Management**: 7 tools (structure complete, mock responses)
- **âš ï¸ Plugin Management**: 5 tools (structure complete, mock responses)
- **âœ… System Tools**: 3 tools fully implemented
- **âœ… Health Monitoring**: 1 tool fully implemented

**Total: 31 tools (13 fully functional, 15 with mock responses, 3 documentation)**

## Installation and Setup

### Prerequisites

- **Python**: 3.8+
- **Resonite**: Latest version installed and running
- **OSC Enabled**: Resonite OSC settings configured (port 9000)

### Installation

```bash
# Clone the repository
git clone https://github.com/sandraschi/resonite-mcp.git
cd resonite-mcp

# Install with development dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import resonite_mcp; print('âœ… Installation successful')"
```

### Resonite Setup

1. **Install Resonite** from [Steam](https://store.steampowered.com/app/2519830/Resonite/)
2. **Enable OSC** in Resonite settings:
   - Open Resonite Settings (Menu â†’ Settings)
   - Navigate to "Network" tab
   - Enable "OSC" option
   - Set OSC Port to `9000`
   - Optionally enable "Receive OSC" for bidirectional communication

## Configuration

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "resonite": {
      "command": "python",
      "args": ["-m", "resonite_mcp"],
      "env": {
        "RESONITE_OSC_HOST": "127.0.0.1",
        "RESONITE_OSC_PORT": "9000"
      }
    }
  }
}
```

### Cursor IDE Configuration

Add to Cursor `settings.json`:

```json
{
  "mcp": {
    "resonite": {
      "command": "python",
      "args": ["-m", "resonite_mcp", "--stdio"],
      "cwd": "D:\\Dev\\repos\\resonite-mcp",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

### Environment Variables

- `RESONITE_OSC_HOST`: OSC server hostname (default: 127.0.0.1)
- `RESONITE_OSC_PORT`: OSC server port (default: 9000)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Tool Reference

### Session Management (4 tools)

- `resonite_session_start(session_name?, world_path?, avatar_slot?)` - Start new session
- `resonite_session_status()` - Get current session status
- `resonite_session_end()` - End current session
- `resonite_world_load(world_path)` - Load a world

### Avatar Control (3 tools)

- `resonite_avatar_load(avatar_path, slot?, parameters?)` - Load avatar with parameters
- `resonite_parameter_set(parameter_name, value, avatar_slot?)` - Set parameter value
- `resonite_protoflux_execute(script_name, parameters?)` - Execute ProtoFlux script

### Inventory Management (7 tools)

- `resonite_inventory_list(item_type?, search_query?, limit?, offset?)` - List items
- `resonite_inventory_search(query, item_type?)` - Search inventory
- `resonite_inventory_spawn(item_data)` - Spawn item in world
- `resonite_inventory_upload(file_data)` - Upload to inventory
- `resonite_inventory_delete(item_data)` - Delete from inventory
- `resonite_inventory_share(item_data)` - Share with users
- `resonite_inventory_info(item_id)` - Get item details

### OSC Communication (8 tools)

- `send_osc(host, port, address, values?)` - Send OSC message
- `start_osc_server(port, address?)` - Start OSC server
- `stop_osc_server(port)` - Stop OSC server
- `get_received_messages(port, address_pattern?, max_age_seconds?, limit?)` - Get messages
- `get_latest_message(port, address_pattern?)` - Get latest message
- `get_osc_server_stats(port)` - Get server stats
- `clear_osc_message_buffer(port)` - Clear buffer
- `test_osc_echo(port?)` - Test connectivity

### Plugin Management (5 tools)

- `plugin_list()` - List plugins
- `plugin_load(plugin_name)` - Load plugin
- `plugin_unload(plugin_name)` - Unload plugin
- `plugin_reload(plugin_name)` - Reload plugin
- `plugin_discover()` - Discover plugins
- `plugin_info(plugin_name?)` - Get plugin info

### System Tools (3 tools)

- `help(level?, topic?)` - Get help documentation
- `status(level?, focus?)` - Get server status
- `health_check()` - Health check

## OSC Communication

### OSC Protocol Basics

OSC (Open Sound Control) is a protocol for communication between multimedia applications. In Resonite:

- **Default Port**: 9000
- **Message Format**: Address pattern + values
- **Bidirectional**: Send and receive messages
- **Real-time**: Low-latency communication

### Common OSC Addresses

- `/avatar/parameters/Happy` - Avatar happiness parameter
- `/avatar/parameters/Angry` - Avatar anger parameter
- `/world/load` - Load a world
- `/session/start` - Start session
- `/inventory/list` - List inventory items

### OSC Server Management

The MCP server can start OSC servers to receive messages from Resonite:

```python
# Start OSC server on port 9001
await start_osc_server(port=9001)

# Get received messages
messages = await get_received_messages(port=9001)
```

## Session Management

### Session Lifecycle

1. **Start Session**: `resonite_session_start()` initializes a new session
2. **Load World**: `resonite_world_load()` loads a world into the session
3. **Load Avatar**: `resonite_avatar_load()` loads an avatar
4. **Interact**: Use avatar controls and ProtoFlux scripts
5. **End Session**: `resonite_session_end()` closes the session

### Session States

- **Not Started**: No active session
- **Starting**: Session initialization in progress
- **Active**: Session running, world and avatar loaded
- **Ending**: Session cleanup in progress

## Avatar Control

### Avatar Parameters

Resonite avatars support various parameters:

- **Facial Expressions**: Happy, Angry, Sad, Surprised
- **Body Language**: Relaxed, Tense, Excited
- **Movement**: Walking, Running, Jumping
- **Custom Parameters**: User-defined parameters

### Parameter Control

```python
# Set happiness to 80%
await resonite_parameter_set("Happy", 0.8)

# Set custom parameter
await resonite_parameter_set("MyCustomParam", 0.5)
```

### Avatar Loading

```python
# Load avatar with initial parameters
await resonite_avatar_load(
    avatar_path="resonite://DefaultAvatar",
    slot=0,
    parameters={"Happy": 0.7, "Relaxed": 0.8}
)
```

## ProtoFlux Scripting

### ProtoFlux Overview

ProtoFlux is Resonite's visual programming system:

- **Visual Programming**: Node-based scripting interface
- **Real-time Execution**: Scripts run in real-time
- **Component Integration**: Integrates with Resonite components
- **Performance Optimized**: Compiled execution

### Script Execution

```python
# Execute a color changer script
await resonite_protoflux_execute("ColorChanger", {
    "target_color": [1.0, 0.5, 0.0],
    "transition_time": 2.0
})
```

## Inventory Management

### Inventory Structure

Resonite inventory contains:

- **Avatars**: Custom avatar assets
- **Worlds**: User-created worlds
- **Objects**: 3D models and assets
- **Scripts**: ProtoFlux scripts
- **Textures**: Image assets
- **Audio**: Sound files

### Inventory Operations

```python
# List inventory items
items = await resonite_inventory_list(limit=20)

# Search for specific items
results = await resonite_inventory_search("avatar")

# Spawn item in world
await resonite_inventory_spawn({"item_id": "item123"})
```

## Plugin System

### Built-in Plugins

- **OSC Extensions**: Enhanced OSC communication
- **ProtoFlux Helpers**: ProtoFlux scripting assistance

### Plugin Architecture

Plugins extend the MCP server with additional functionality:

- **Tool Registration**: Add new MCP tools
- **OSC Extensions**: Custom OSC message handling
- **Integration Features**: Third-party service integration

## HTTP API

### Server Modes

The MCP server supports two modes:

1. **MCP Stdio Mode**: For Claude Desktop/Cursor integration
2. **HTTP API Mode**: REST API for web applications

### HTTP Endpoints

- `GET /` - Server information
- `GET /health` - Health check
- `POST /osc/send` - Send OSC messages
- `POST /resonite/session/start` - Start session
- `POST /resonite/avatar/load` - Load avatar
- `GET /resonite/inventory/list` - List inventory
- `POST /plugins/load` - Load plugin

### Starting HTTP Server

```bash
resonite-mcp --host 127.0.0.1 --port 8000
```

## Troubleshooting

### Common Issues

#### "MCP server not starting"

**Symptoms:**
- Server fails to start in Cursor/Claude
- AttributeError or ImportError

**Solutions:**
1. Check Python path and installation
2. Verify Cursor configuration uses "mcp" key
3. Ensure `--stdio` flag is included

#### "OSC connection failed"

**Symptoms:**
- Tools return connection errors
- No response from Resonite commands

**Solutions:**
1. Verify Resonite is running
2. Check OSC settings in Resonite
3. Confirm port 9000 is available
4. Test network connectivity

#### "Tools not appearing"

**Symptoms:**
- MCP tools not visible in IDE
- Server starts but no tools listed

**Solutions:**
1. Restart Cursor/Claude Desktop
2. Check MCP configuration syntax
3. Verify server logs for errors

### Debug Mode

Enable detailed logging:

```bash
LOG_LEVEL=DEBUG resonite-mcp --stdio
```

### OSC Testing

Test OSC connectivity:

```bash
# Send test message
curl -X POST http://127.0.0.1:8000/osc/send \
  -H "Content-Type: application/json" \
  -d '{"host": "127.0.0.1", "port": 9000, "address": "/test"}'
```

## Best Practices

### Session Management

1. **Clean Session Lifecycle**: Always start and end sessions properly
2. **Resource Management**: Close OSC servers when not needed
3. **Error Handling**: Check return values for error conditions

### Performance Optimization

1. **OSC Connection Reuse**: Reuse OSC connections when possible
2. **Batch Operations**: Group related parameter changes
3. **Resource Cleanup**: Properly close connections and servers

### Development Workflow

1. **Test Environment**: Use separate Resonite instance for testing
2. **Version Control**: Keep MCP server and Resonite versions in sync
3. **Documentation**: Document custom OSC addresses and parameters

### Security Considerations

1. **OSC Access Control**: Limit OSC access to trusted networks
2. **Parameter Validation**: Validate parameter values before sending
3. **Session Isolation**: Use separate sessions for different activities

---

**Integration Status:** Beta (v0.1.1) - Core functionality complete, inventory management pending full implementation

**Last Updated:** 2025-12-22

