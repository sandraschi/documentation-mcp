# Robotics MCP - Architecture Deep Dive

**Last Updated:** 2025-12-11
**Status:** REFERENCE
**Source:** `D:\Dev\repos\robotics-mcp`

---

## Overview

The Robotics MCP implements sophisticated compositing patterns where specialized MCP servers work together through well-defined integration protocols. This document outlines the architectural patterns for cross-MCP orchestration and state management in robotics applications.

---

## Core Compositing Patterns

### 1. Tool Family Modularization Pattern

**Problem:** Complex MCP servers with 60+ tools become unmaintainable monoliths.

**Solution:** Tool family modularization with clean separation of concerns.

```
server.py
â”œâ”€â”€ tools/
â”‚   â”œâ”€â”€ motor_manager.py     # Motor control family
â”‚   â”œâ”€â”€ path_manager.py      # Path movement family
â”‚   â”œâ”€â”€ import_export.py     # Import/export family
â”‚   â””â”€â”€ vrm_avatar.py        # VRM integration family
```

**Benefits:**
- **Scalability:** Zero complexity increase for new families
- **Maintainability:** Family-level isolation
- **Discoverability:** 4 families vs 60 individual tools for Claude
- **Parallel Development:** Teams can work on different families

### 2. Robotics Orchestration Pattern

**Problem:** Virtual robotics requires coordination of multiple specialized systems.

**Solution:** Robotics-mcp orchestrates the entire workflow.

```
Robotics-MCP (Coordinator)
â”œâ”€â”€ OSC-MCP (Communication)
â”œâ”€â”€ Unity3D-MCP (Environment)
â”œâ”€â”€ Avatar-MCP (Character)
â”œâ”€â”€ Blender-MCP (Modeling)
â””â”€â”€ GIMP-MCP (Textures)
```

**Orchestration Flow:**
```python
async def spawn_virtual_robot(self, robot_type, config):
    # 1. Create Unity scene
    scene = await self.call_mounted('unity', 'create_scene')

    # 2. Import robot model
    robot = await self.call_mounted('unity', 'import_robot_model', config)

    # 3. Setup avatar integration
    await self.call_mounted('avatar', 'integrate_robot', robot.id)

    # 4. Configure OSC control
    await self.call_mounted('osc', 'setup_robot_control', robot.id)

    return robot
```

### 3. Unity VRM Integration Pattern

**Problem:** VRM avatars need both Unity project setup AND advanced compositing.

**Solution:** Unity-focused tools delegate advanced manipulation to avatar-mcp.

```
Unity Setup (unity3d-mcp) â†’ Avatar Compositing (avatar-mcp)
     â†“                              â†“
Project Integration           Bone Manipulation
Rigging & Materials           Facial Rigging
Build Pipeline               Animation Control
OSC Integration              Physics Simulation
```

**Implementation:**
```python
# Phase 1: Unity Integration
import_result = await unity_mcp.import_vrm_to_unity("avatar.vrm", "project/")
import_id = import_result['import_id']

# Phase 2: Avatar Compositing
await avatar_mcp.integrate_with_avatarmcp(import_id, {
    'enable_osc_control': True,
    'setup_animation_sync': True
})
```

---

## State Management Patterns

### Import ID Tracking

**Problem:** Maintaining state consistency across MCP server boundaries.

**Solution:** Universal import IDs for cross-server coordination.

```python
# Import ID flows through the entire pipeline
unity_import = await unity_mcp.import_vrm_to_unity(vrm_path, project_path)
import_id = unity_import['import_id']  # "unity_vrm_import_avatar.vrm_123456"

# Same ID used across all servers
avatar_state = await avatar_mcp.get_import_state(import_id)
robotics_state = await robotics_mcp.get_robot_state(import_id)
```

### Distributed State Synchronization

**Problem:** Real-time state updates across distributed servers.

**Solution:** Event-driven state propagation with conflict resolution.

```python
class DistributedStateManager:
    def __init__(self):
        self.server_states = {}  # {server_name: {import_id: state}}
        self.state_versions = {}  # Version tracking

    async def sync_state(self, import_id, server_name, state_update):
        current_version = self.state_versions.get(import_id, 0)
        new_version = current_version + 1

        # Apply update with versioning
        self.server_states[server_name][import_id] = {
            **state_update,
            'version': new_version,
            'timestamp': time.time()
        }
        self.state_versions[import_id] = new_version
```

---

## Communication Patterns

### OSC Protocol Bridge

**Problem:** Real-time communication between Unity, VRChat, and robotics systems.

**Solution:** OSC bridge with avatar-mcp as central hub.

```
Robot Control â†’ OSC Bridge â†’ Avatar-MCP â†’ Unity/VRChat
    â†‘              â†‘              â†“
Parameter Mapping    Translation     Real-time Sync
```

**OSC Configuration:**
```python
osc_config = {
    'avatar_parameters': {
        '/robot/speed': 'motor_speed',
        '/robot/steer': 'steering_angle',
        '/robot/pose': 'body_pose'
    },
    'unity_parameters': {
        'motor_speed': '/unity/robot/motor',
        'steering_angle': '/unity/robot/steer'
    }
}
```

### Cross-Server Tool Calls

**Problem:** Calling tools on remote MCP servers.

**Solution:** Mounted server pattern with error propagation.

```python
class RoboticsMCP:
    async def call_mounted_server_tool(self, server_name, tool_name, params):
        if server_name not in self.mounted_servers:
            raise ServerNotMountedError(server_name)

        server = self.mounted_servers[server_name]
        try:
            result = await server.call_tool(tool_name, params)
            return result
        except Exception as e:
            raise CrossMCPEror(server_name, tool_name, e) from e
```

---

## Portmanteau Tools Architecture

### Tool Organization

**Portmanteau Pattern** - Consolidates related operations into unified interfaces:

1. **robot_control** - Movement, status, control operations
2. **robot_behavior** - Animation, camera, navigation, manipulation
3. **robot_virtual** - Virtual robot operations
4. **robot_model_tools** - 3D model lifecycle (create, import, export, convert)
5. **vbot_crud** - Virtual robot CRUD operations
6. **robot_animation** - Animation and pose control
7. **robot_camera** - Camera feed and visual control
8. **robot_navigation** - Path planning and navigation
9. **spz_converter** - SPZ file format handling
10. **robotics_system** - System management
11. **virtual_robotics** - Legacy virtual robotics operations

### Tool Implementation Pattern

```python
class RobotControlTool:
    def __init__(self, mcp, state_manager, mounted_servers):
        self.mcp = mcp
        self.state = state_manager
        self.mounted = mounted_servers

    def register_tools(self):
        @self.mcp.tool
        async def robot_control(
            operation: Literal["move", "stop", "status", "calibrate"],
            robot_id: str,
            **params
        ):
            """Unified robot control operations."""
            if operation == "move":
                return await self._move_robot(robot_id, **params)
            elif operation == "stop":
                return await self._stop_robot(robot_id, **params)
            # ... other operations
```

---

## Integration Patterns

### MCP Server Composition

**6+ Specialized Servers Orchestrated:**

- **osc-mcp** - Communication protocol bridge
- **unity3d-mcp** - 3D environment and physics simulation
- **vrchat-mcp** - Social VR integration
- **avatar-mcp** - Character compositing and manipulation
- **blender-mcp** - 3D modeling and asset creation
- **gimp-mcp** - 2D texture and image processing

### Graceful Degradation

**Pattern:** Continue operation when servers are unavailable.

```python
async def spawn_robot_with_fallbacks(self, config):
    robot = await self._basic_robot_spawn(config)

    # Try advanced features, but don't fail if unavailable
    try:
        await self.call_mounted('avatar', 'enhance_robot', robot.id)
    except ServerUnavailableError:
        logger.warning("Avatar-mcp unavailable, using basic robot")

    try:
        await self.call_mounted('unity', 'add_physics', robot.id)
    except ServerUnavailableError:
        logger.warning("Unity unavailable, using basic physics")

    return robot
```

---

## Performance Patterns

### Async Operation Tracking

**Problem:** Long-running operations need monitoring.

**Solution:** Track async operations with progress updates.

```python
class OperationTracker:
    def __init__(self):
        self.operations = {}
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def track_operation(self, op_id, operation_type, params):
        self.operations[op_id] = {
            'type': operation_type,
            'params': params,
            'status': 'running',
            'start_time': time.time(),
            'progress': 0.0
        }
        return op_id

    async def update_progress(self, op_id, progress, message=None):
        if op_id in self.operations:
            self.operations[op_id].update({
                'progress': progress,
                'message': message,
                'last_update': time.time()
            })
```

### Resource Pooling

**Problem:** Limited resources across distributed servers.

**Solution:** Shared resource pools with queuing.

```python
class ResourcePool:
    def __init__(self):
        self.pools = {
            'unity_scenes': asyncio.Queue(maxsize=10),
            'avatar_imports': asyncio.Queue(maxsize=5),
            'osc_connections': asyncio.Queue(maxsize=20)
        }

    async def acquire_resource(self, resource_type, timeout=30):
        return await asyncio.wait_for(
            self.pools[resource_type].get(),
            timeout=timeout
        )
```

---

## Error Handling Patterns

### Cross-Server Error Propagation

**Problem:** Errors occurring in one MCP server need context from calling server.

**Solution:** Wrap errors with cross-server context.

```python
class CrossMCPEror(Exception):
    def __init__(self, server_name, tool_name, original_error):
        self.server_name = server_name
        self.tool_name = tool_name
        self.original_error = original_error
        super().__init__(f"{server_name}.{tool_name}: {original_error}")

# Usage
try:
    result = await robotics_mcp.call_mounted('unity', 'import_model', params)
except CrossMCPEror as e:
    logger.error(f"Unity import failed: {e}")
    # Error includes both server context and original error
```

---

## Real-World Workflows

### Complete Robotics Pipeline

```python
# 1. VRM Avatar Setup
avatar_import = await unity_mcp.import_vrm_to_unity("scout.vrm", "robotics_project")
avatar_id = avatar_import['import_id']

# 2. Unity Rigging
await unity_mcp.setup_unity_avatar_rigging(avatar_id, {
    'humanoid_avatar': True,
    'inverse_kinematics': True
})

# 3. Avatar-mcp Integration
await avatar_mcp.integrate_with_avatarmcp(avatar_id, {
    'enable_osc_control': True,
    'setup_animation_sync': True
})

# 4. Robotics Spawn
robot = await robotics_mcp.spawn_virtual_robot("scout", {
    'avatar_id': avatar_id,
    'motor_config': {'max_speed': 3.0},
    'path_following': True
})

# 5. Control Operations
await robotics_mcp.control_robot(robot.id, "start_motor", {"speed": 1.34})  # 3 mph
await robotics_mcp.move_robot(robot.id, "follow_path", {
    'path_type': 'spline',
    'waypoints': [[0,0,0], [10,0,10], [20,5,20]]
})
```

### Moorebot Scout Integration

```python
# 1. Physical Robot Setup (Future)
scout_config = {
    'model': 'moorebot-scout',
    'wheels': 'mecanum',  # 45Â° alternating rollers
    'sensors': ['lidar', 'camera', 'imu'],
    'communication': 'ros1-melodic'
}

# 2. Virtual Robot Testing
virtual_scout = await robotics_mcp.spawn_virtual_robot("scout", scout_config)

# 3. Test Behaviors
await robotics_mcp.test_robot_behavior(virtual_scout.id, "obstacle_avoidance")
await robotics_mcp.test_robot_behavior(virtual_scout.id, "path_following")

# 4. Performance Validation
performance = await robotics_mcp.validate_robot_performance(virtual_scout.id, {
    'terrain_types': ['flat', 'rough', 'inclined'],
    'speed_tests': [1.0, 2.0, 3.0],  # mph
    'battery_simulation': True
})
```

---

## Testing Patterns

### Compositing Integration Tests

**Problem:** Testing interactions between multiple MCP servers.

**Solution:** Mock servers with controlled state.

```python
async def test_robotics_compositing():
    # Setup mock servers
    unity_mock = MockUnityServer()
    avatar_mock = MockAvatarServer()

    # Execute compositing workflow
    import_result = await unity_mock.import_vrm_to_unity("test.vrm", "test_project")
    import_id = import_result['import_id']

    integration_result = await avatar_mock.integrate_with_avatarmcp(import_id, {
        'enable_osc_control': True
    })

    # Verify state consistency
    unity_state = await unity_mock.get_unity_import_status(import_id)
    avatar_state = await avatar_mock.get_avatar_state(import_id)

    assert unity_state['status'] == 'complete'
    assert avatar_state['osc_enabled'] == True
    assert unity_state['import_id'] == avatar_state['import_id']
```

---

## Evolution Patterns

### Plugin Architecture

**Problem:** Adding new robot types or MCP servers to the composition.

**Solution:** Plugin system for dynamic extension.

```python
class RoboticsPluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = Path("plugins/")

    async def load_robot_plugin(self, robot_type):
        plugin_path = self.plugin_dir / f"{robot_type}_plugin.py"
        spec = importlib.util.spec_from_file_location(robot_type, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_class = getattr(module, f"{robot_type.title()}Plugin")
        plugin = plugin_class(self.config)
        plugin.register_with_robotics(self)

        self.plugins[robot_type] = plugin
```

---

## Best Practices

### 1. Clean API Boundaries
- Each MCP server has well-defined responsibilities
- APIs are versioned and backward-compatible
- Error handling includes cross-server context

### 2. State Consistency
- Use import IDs for universal identification
- Implement versioning for conflict resolution
- Provide rollback capabilities

### 3. Performance Considerations
- Implement resource pooling for shared resources
- Use async operations with progress tracking
- Monitor cross-server performance

### 4. Error Resilience
- Implement graceful degradation
- Provide fallback mechanisms
- Log cross-server errors with full context

### 5. Testing Strategy
- Unit test individual server functionality
- Integration test cross-server workflows
- Contract test API compatibility

---

## Related Documentation

**Project Documentation:**
- `STATUS.md` - Current implementation status
- `STRUCTURE.md` - Project organization
- `docs/PROGRESS_REPORT.md` - Implementation progress

**Integration Guides:**
- `../patterns/mcp-zoo-compositing-patterns.md` - Cross-MCP patterns
- `../patterns/adn-architecture-compositing-deep-dive.md` - Technical deep dive

**MCP Central Docs:**
- `../fastmcp/migration-guide.md` - FastMCP 3.1.1++ migration
- `../tools/zoo-analyzer.md` - MCP Zoo analysis tools

---

**This architecture enables complex robotics workflows through coordinated specialization while maintaining clean separation of concerns. The compositing patterns allow the Robotics MCP to orchestrate multiple specialized servers for complete robot lifecycle management.**

