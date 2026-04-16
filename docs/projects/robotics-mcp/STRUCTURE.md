# Robotics MCP - Project Structure

**Last Updated:** 2025-12-04  
**Source Repo:** `D:\Dev\repos\robotics-mcp`

---

## ðŸ“ Directory Structure

```
robotics-mcp/
â”œâ”€â”€ src/robotics_mcp/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ server.py              # Main FastMCP server (dual transport)
â”‚   â”œâ”€â”€ clients/               # Robot client implementations
â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”œâ”€â”€ integrations/          # MCP server integration wrappers
â”‚   â”‚   â””â”€â”€ __init__.py
â”‚   â”œâ”€â”€ tools/                 # Portmanteau tool implementations
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ robot_control.py
â”‚   â”‚   â”œâ”€â”€ robot_behavior.py
â”‚   â”‚   â”œâ”€â”€ robot_virtual.py
â”‚   â”‚   â”œâ”€â”€ robot_model_tools.py
â”‚   â”‚   â”œâ”€â”€ vbot_crud.py
â”‚   â”‚   â”œâ”€â”€ robot_animation.py
â”‚   â”‚   â”œâ”€â”€ robot_camera.py
â”‚   â”‚   â”œâ”€â”€ robot_navigation.py
â”‚   â”‚   â”œâ”€â”€ spz_converter.py
â”‚   â”‚   â”œâ”€â”€ robotics_system.py
â”‚   â”‚   â””â”€â”€ virtual_robotics.py
â”‚   â””â”€â”€ utils/                 # Utilities
â”‚       â”œâ”€â”€ __init__.py
â”‚       â”œâ”€â”€ config_loader.py
â”‚       â”œâ”€â”€ error_handler.py
â”‚       â”œâ”€â”€ mcp_client_helper.py
â”‚       â”œâ”€â”€ mock_data.py
â”‚       â””â”€â”€ state_manager.py
â”‚
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ conftest.py            # Test fixtures
â”‚   â”œâ”€â”€ unit/                  # Unit tests
â”‚   â”‚   â”œâ”€â”€ test_config_loader.py
â”‚   â”‚   â”œâ”€â”€ test_error_handler.py
â”‚   â”‚   â”œâ”€â”€ test_robot_animation.py
â”‚   â”‚   â”œâ”€â”€ test_robot_behavior.py
â”‚   â”‚   â”œâ”€â”€ test_robot_camera.py
â”‚   â”‚   â”œâ”€â”€ test_robot_control.py
â”‚   â”‚   â”œâ”€â”€ test_robot_model_tools.py
â”‚   â”‚   â”œâ”€â”€ test_robot_navigation.py
â”‚   â”‚   â”œâ”€â”€ test_robot_virtual.py
â”‚   â”‚   â”œâ”€â”€ test_robotics_system.py
â”‚   â”‚   â”œâ”€â”€ test_spz_converter.py
â”‚   â”‚   â”œâ”€â”€ test_state_manager.py
â”‚   â”‚   â””â”€â”€ test_vbot_crud.py
â”‚   â””â”€â”€ integration/           # Integration tests
â”‚       â”œâ”€â”€ test_robot_control_integration.py
â”‚       â”œâ”€â”€ test_server_tools.py
â”‚       â”œâ”€â”€ test_server.py
â”‚       â””â”€â”€ test_virtual_robotics.py
â”‚
â”œâ”€â”€ docs/                      # Project documentation
â”‚   â”œâ”€â”€ PROGRESS_REPORT.md
â”‚   â”œâ”€â”€ IMPLEMENTATION_SUMMARY.md
â”‚   â”œâ”€â”€ UNITY_VBOT_INSTANTIATION.md
â”‚   â”œâ”€â”€ VRM_VS_ROBOT_MODELS.md
â”‚   â”œâ”€â”€ QUICK_START_VRCHAT.md
â”‚   â”œâ”€â”€ ROS1_LOCAL_SETUP.md
â”‚   â”œâ”€â”€ VRChat_INTEGRATION.md
â”‚   â”œâ”€â”€ VRCHAT_SCOUT_SETUP.md
â”‚   â”œâ”€â”€ CREATE_SCOUT_MODEL.md
â”‚   â”œâ”€â”€ IMPORT_SCOUT_TO_UNITY.md
â”‚   â”œâ”€â”€ UNITY_SETUP_GUIDE.md
â”‚   â”œâ”€â”€ UNITY_FBX_IMPORT_FIX.md
â”‚   â”œâ”€â”€ UNITY_VBOT_INSTANTIATION.md
â”‚   â”œâ”€â”€ ADD_WORLDLABS_TO_SCENE.md
â”‚   â”œâ”€â”€ RENDER_PLY_SPLATS.md
â”‚   â”œâ”€â”€ INSTALL_SPZ_PLUGIN.md
â”‚   â”œâ”€â”€ MARBLE_SPZ_SUPPORT.md
â”‚   â”œâ”€â”€ COMPREHENSIVE_NOTES.md
â”‚   â”œâ”€â”€ NEXT_STEPS_AFTER_IMPORT.md
â”‚   â”œâ”€â”€ PRIORITY_1_IMPLEMENTATION.md
â”‚   â”œâ”€â”€ TOOL_GAPS_ANALYSIS.md
â”‚   â””â”€â”€ MCP_SERVERS_STATUS.md
â”‚
â”œâ”€â”€ scripts/                   # Utility scripts
â”‚   â”œâ”€â”€ run-tests.ps1
â”‚   â”œâ”€â”€ check-standards.ps1
â”‚   â”œâ”€â”€ create_scout.py
â”‚   â”œâ”€â”€ create_scout_model.py
â”‚   â”œâ”€â”€ import_scout_to_unity.py
â”‚   â”œâ”€â”€ import_living_room.py
â”‚   â”œâ”€â”€ test_spawn_scout.py
â”‚   â”œâ”€â”€ test_wheel_rotation.py
â”‚   â”œâ”€â”€ check_blend_file.py
â”‚   â”œâ”€â”€ check_spz_and_install.py
â”‚   â”œâ”€â”€ verify_fbx_contents.py
â”‚   â”œâ”€â”€ list_tools.py
â”‚   â””â”€â”€ install_gaussian_splatting.ps1
â”‚
â”œâ”€â”€ config/
â”‚   â””â”€â”€ config.yaml.example    # Example configuration
â”‚
â”œâ”€â”€ docker/
â”‚   â”œâ”€â”€ README.md
â”‚   â”œâ”€â”€ Dockerfile.ros1-melodic
â”‚   â”œâ”€â”€ docker-compose.ros1.yml
â”‚   â””â”€â”€ scripts/
â”‚       â”œâ”€â”€ setup-ros1-workspace.ps1
â”‚       â””â”€â”€ setup-ros1-workspace.sh
â”‚
â”œâ”€â”€ mcpb/                      # MCPB packaging
â”‚   â”œâ”€â”€ manifest.json
â”‚   â””â”€â”€ assets/
â”‚       â””â”€â”€ prompts/
â”‚           â”œâ”€â”€ system.md
â”‚           â”œâ”€â”€ user.md
â”‚           â””â”€â”€ examples.json
â”‚
â”œâ”€â”€ Assets/                    # Unity assets (if applicable)
â”‚   â””â”€â”€ Scripts/
â”‚       â”œâ”€â”€ EnvironmentLoader.cs
â”‚       â”œâ”€â”€ GaussianSplatRenderer.cs
â”‚       â”œâ”€â”€ RobotAnimator.cs
â”‚       â”œâ”€â”€ RobotCamera.cs
â”‚       â”œâ”€â”€ RobotExporter.cs
â”‚       â”œâ”€â”€ RobotNavigator.cs
â”‚       â””â”€â”€ VbotSpawner.cs
â”‚
â”œâ”€â”€ README.md                  # Main project README
â”œâ”€â”€ IMPLEMENTATION_SUMMARY.md  # Implementation status
â”œâ”€â”€ PLAN.md                    # Implementation plan
â”œâ”€â”€ CHANGELOG.md               # Version history
â”œâ”€â”€ CONTRIBUTING.md            # Contribution guidelines
â”œâ”€â”€ LICENSE                    # MIT License
â”œâ”€â”€ pyproject.toml             # Python project config
â”œâ”€â”€ requirements.txt           # Python dependencies
â””â”€â”€ mcpb.json                  # MCPB packaging config
```

---

## ðŸ—ï¸ Architecture

### Server Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         FastMCP 3.1.1++ Server            â”‚
â”‚                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚   Dual Transport                  â”‚ â”‚
â”‚  â”‚   - stdio (MCP Protocol)          â”‚ â”‚
â”‚  â”‚   - HTTP (FastAPI)                â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚   11 Portmanteau Tools            â”‚ â”‚
â”‚  â”‚   - robot_control                 â”‚ â”‚
â”‚  â”‚   - robot_behavior                â”‚ â”‚
â”‚  â”‚   - robot_virtual                 â”‚ â”‚
â”‚  â”‚   - robot_model_tools             â”‚ â”‚
â”‚  â”‚   - vbot_crud                     â”‚ â”‚
â”‚  â”‚   - robot_animation               â”‚ â”‚
â”‚  â”‚   - robot_camera                  â”‚ â”‚
â”‚  â”‚   - robot_navigation              â”‚ â”‚
â”‚  â”‚   - spz_converter                 â”‚ â”‚
â”‚  â”‚   - robotics_system               â”‚ â”‚
â”‚  â”‚   - virtual_robotics              â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚   MCP Server Composition          â”‚ â”‚
â”‚  â”‚   - osc-mcp                       â”‚ â”‚
â”‚  â”‚   - unity3d-mcp                   â”‚ â”‚
â”‚  â”‚   - vrchat-mcp                    â”‚ â”‚
â”‚  â”‚   - avatar-mcp                    â”‚ â”‚
â”‚  â”‚   - blender-mcp                   â”‚ â”‚
â”‚  â”‚   - gimp-mcp                      â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚                                         â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚   State Management                â”‚ â”‚
â”‚  â”‚   - RobotStateManager             â”‚ â”‚
â”‚  â”‚   - RobotState                    â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Tool Organization

**Portmanteau Pattern** - Consolidates related operations:

- **robot_control** - Unified bot + vbot control (move, stop, status)
- **robot_behavior** - Complex behaviors (animation, camera, navigation)
- **robot_virtual** - Virtual robot operations
- **robot_model_tools** - 3D model lifecycle (create, import, export, convert)
- **vbot_crud** - Virtual robot CRUD operations
- **robot_animation** - Animation and pose control
- **robot_camera** - Camera feed and visual control
- **robot_navigation** - Path planning and navigation
- **spz_converter** - SPZ file format handling
- **robotics_system** - System management
- **virtual_robotics** - Legacy virtual robotics operations

---

## ðŸ”— Integration Points

### MCP Server Composition

The server mounts external MCP servers with prefixes:

- `osc` â†’ osc-mcp
- `unity` â†’ unity3d-mcp
- `vrchat` â†’ vrchat-mcp
- `avatar` â†’ avatar-mcp
- `blender` â†’ blender-mcp
- `gimp` â†’ gimp-mcp

**Graceful fallback** - If a server is unavailable, tools degrade gracefully.

### External Dependencies

- **ROS 1.4 (Melodic)** - For physical robot control (planned)
- **Unity3D** - Virtual robotics platform
- **VRChat** - Social VR testing
- **World Labs Marble/Chisel** - Environment generation
- **Blender** - 3D model creation
- **GIMP** - Texture creation

---

## ðŸ“¦ Key Files

### Core Server

- **`src/robotics_mcp/server.py`** - Main FastMCP server with dual transport
- **`src/robotics_mcp/utils/state_manager.py`** - Robot state management
- **`src/robotics_mcp/utils/config_loader.py`** - Configuration loading

### Tools

- **`src/robotics_mcp/tools/robot_control.py`** - Unified robot control
- **`src/robotics_mcp/tools/robot_model_tools.py`** - 3D model operations
- **`src/robotics_mcp/tools/vbot_crud.py`** - Virtual robot CRUD

### Testing

- **`tests/conftest.py`** - Test fixtures
- **`tests/unit/`** - Unit tests for all tools
- **`tests/integration/`** - End-to-end integration tests

### Configuration

- **`config/config.yaml.example`** - Example configuration
- **`pyproject.toml`** - Python project configuration
- **`mcpb.json`** - MCPB packaging configuration

---

## ðŸ§ª Testing Structure

### Unit Tests

Each tool has dedicated unit tests:
- `test_robot_control.py`
- `test_robot_model_tools.py`
- `test_vbot_crud.py`
- etc.

### Integration Tests

End-to-end workflows:
- `test_server.py` - Server initialization
- `test_server_tools.py` - Tool execution
- `test_virtual_robotics.py` - Virtual robotics workflows

### Test Fixtures

- Mock robot clients
- Mock MCP servers
- Test configuration
- Sample data

---

## ðŸ“š Documentation Structure

### Project Docs (`docs/`)

- **Progress Report** - Comprehensive status
- **Implementation Summary** - What's implemented
- **Unity Guides** - Unity integration
- **VRChat Guides** - VRChat integration
- **ROS Guides** - ROS setup
- **Model Creation** - 3D model guides

### Central Docs (`mcp-central-docs/docs/robotics/`)

- **Robotics Integration** - Complete robotics documentation
- **Moorebot Scout** - Scout integration guide
- **Virtual Robotics** - Test before buying approach
- **ROS Fundamentals** - ROS basics
- **ROS MCP Integration** - Integration patterns

---

## ðŸ”§ Development Workflow

### Adding a New Tool

1. Create tool file in `src/robotics_mcp/tools/`
2. Implement portmanteau pattern
3. Add unit tests in `tests/unit/`
4. Add integration tests in `tests/integration/`
5. Update documentation

### Adding MCP Server Integration

1. Add to `mcp_integration` config section
2. Create integration wrapper in `src/robotics_mcp/integrations/`
3. Update tools to use integration
4. Add tests

### Testing

```powershell
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_robot_control.py

# Run with coverage
pytest --cov=robotics_mcp --cov-report=html
```

---

## ðŸ“¦ Packaging

### MCPB Package

- **`mcpb.json`** - Package configuration
- **`mcpb/manifest.json`** - MCP manifest
- **`mcpb/assets/prompts/`** - System and user prompts

### Build

```powershell
.\scripts\build-mcpb.ps1
```

---

**This structure follows SOTA standards for MCP server development!**


