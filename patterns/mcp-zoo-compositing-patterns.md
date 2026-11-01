# MCP Zoo Compositing Patterns

**Last Updated:** 2025-12-11
**Status:** REFERENCE

---

## Overview

The MCP Zoo implements sophisticated compositing patterns where specialized MCP servers work together through well-defined integration protocols. This document outlines the architectural patterns for cross-MCP orchestration and state management.

---

## Core Compositing Patterns

### 1. Unity VRM Integration Pattern

**Problem:** VRM avatars need both Unity project setup AND advanced compositing.

**Solution:** Unity-focused tools delegate advanced manipulation to avatar-mcp.

```
Unity Setup (unity3d-mcp) → Avatar Compositing (avatar-mcp)
     ↓                              ↓
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

### 2. Robotics Orchestration Pattern

**Problem:** Virtual robotics requires coordination of multiple specialized systems.

**Solution:** Robotics-mcp orchestrates the entire workflow.

```
Robotics-MCP (Coordinator)
├── OSC-MCP (Communication)
├── Unity3D-MCP (Environment)
├── Avatar-MCP (Character)
├── Blender-MCP (Modeling)
└── GIMP-MCP (Textures)
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

### 3. Tool Family Modularization Pattern

**Problem:** Complex servers become monolithic with 60+ tools.

**Solution:** Organize tools into families with clean separation.

```
server/
├── tools/
│   ├── motor_manager.py     # Motor control family
│   ├── path_manager.py      # Path movement family
│   ├── import_export.py     # Import/export family
│   └── vrm_avatar.py        # VRM integration family
```

**Pattern Benefits:**
- **Scalability:** Zero complexity increase for new families
- **Maintainability:** Family-level isolation
- **Testing:** Independent family testing
- **Discoverability:** 4 families vs 60 individual tools

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

### OSC Protocol Organization Pattern

**Problem:** OSC tools organization between `osc-mcp` (protocol) and `vrchat-mcp` (application).

**Solution:** Clean separation by responsibility - protocol vs application conventions.

```
Robot Control → Robotics-MCP → OSC-MCP → VRChat-MCP → VRChat
    ↑              ↑              ↓              ↓
High-Level      Orchestration   Protocol       Application
Commands        & State         Transport       Specific
                                   Layer         Conventions
```

**Tool Organization Principle:**
- **`osc-mcp`**: Generic OSC protocol tools (send/receive messages, manage connections)
- **`vrchat-mcp`**: VRChat-specific OSC tools (avatar parameters, VRChat conventions)
- **`robotics-mcp`**: Orchestrates both for domain-specific use cases

**Example Implementation:**
```python
# osc-mcp: Protocol-level operations
class OSCMCP:
    async def send_osc_message(self, address: str, args: list, host: str = "127.0.0.1", port: int = 9000):
        """Send OSC message to any destination."""

    async def setup_osc_server(self, port: int, callback):
        """Setup OSC server with message handler."""

# vrchat-mcp: VRChat-specific operations
class VRChatMCP:
    async def control_avatar_parameter(self, parameter: str, value: float):
        """Control VRChat avatar using OSC (handles VRChat conventions)."""

    async def get_vrchat_osc_addresses(self):
        """Return VRChat-specific OSC address mappings."""

# robotics-mcp: High-level orchestration
class RoboticsMCP:
    async def control_robot_via_vrchat(self, robot_id: str, command: dict):
        """Orchestrate robot control through VRChat avatar."""
        # Convert robot command to VRChat OSC
        osc_command = await self.convert_robot_to_vrchat_osc(command)

        # Send via osc-mcp (protocol layer)
        await self.mounted_servers['osc'].send_osc_message(
            osc_command['address'],
            osc_command['args']
        )

        # Verify via vrchat-mcp (application layer)
        await self.mounted_servers['vrchat'].verify_parameter_set(
            osc_command['parameter'],
            osc_command['expected_value']
        )
```

**OSC Address Space Organization:**
```python
# osc-mcp: Generic OSC protocol addresses
generic_addresses = {
    '/system/status': 'Status messages',
    '/debug/log': 'Debug logging',
    '/ping': 'Connection testing'
}

# vrchat-mcp: VRChat-specific OSC addresses
vrchat_addresses = {
    '/avatar/parameters/VelocityZ': 'Forward/backward movement',
    '/avatar/parameters/VelocityX': 'Left/right movement',
    '/avatar/parameters/AngularY': 'Rotation',
    '/avatar/parameters/Jump': 'Jump trigger'
}

# robotics-mcp: Domain-specific OSC mappings
robotics_addresses = {
    '/robot/{id}/motor/speed': 'Motor speed control',
    '/robot/{id}/steer/angle': 'Steering angle',
    '/robot/{id}/sensor/lidar': 'LIDAR data'
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

### Graceful Degradation

**Problem:** Some MCP servers may be unavailable.

**Solution:** Continue operation with reduced functionality.

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

### Cross-Server Contract Testing

**Problem:** Ensuring API compatibility between servers.

**Solution:** Contract tests that verify API expectations.

```python
def test_unity_avatar_contract():
    """Test that unity3d-mcp meets avatar-mcp expectations."""

    # Unity must return import_id
    import_result = await unity_mcp.import_vrm_to_unity("avatar.vrm", "project")
    assert 'import_id' in import_result

    # Import ID must be usable by avatar-mcp
    import_id = import_result['import_id']
    avatar_result = await avatar_mcp.integrate_with_avatarmcp(import_id, {})
    assert avatar_result['success'] == True
```

---

## Evolution Patterns

### Plugin Architecture

**Problem:** Adding new MCP servers to the composition.

**Solution:** Plugin system for dynamic server loading.

```python
class MCPPluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = Path("plugins/")

    async def load_plugin(self, plugin_name):
        plugin_path = self.plugin_dir / f"{plugin_name}_plugin.py"
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_class = getattr(module, f"{plugin_name.title()}Plugin")
        plugin = plugin_class(self.config)
        plugin.register_with_orchestrator(self)

        self.plugins[plugin_name] = plugin
```

### Distributed Orchestration

**Problem:** Orchestrating MCP servers across network boundaries.

**Solution:** Distributed orchestration with remote procedure calls.

```python
class DistributedOrchestrator:
    def __init__(self):
        self.remote_servers = {}  # Network-connected MCP servers
        self.local_servers = {}   # Locally mounted servers

    async def orchestrate_distributed_workflow(self, workflow_dag):
        # Parse workflow dependencies
        tasks = self._parse_workflow_dag(workflow_dag)

        # Execute with dependency resolution
        results = await self._execute_with_dependencies(tasks)

        return results
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

## Real-World Examples

### Complete Robotics Workflow

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

### World Building Pipeline

```python
# 1. Generate World (World Labs)
world_data = await worldlabs_mcp.generate_world("urban street", {
    'style': 'cyberpunk',
    'size': 'medium'
})

# 2. Import to Unity
unity_import = await unity_mcp.import_marble_world(world_data, "world_project")

# 3. Optimize for VRChat
await unity_mcp.optimize_worldlabs_for_vrchat(unity_import.id, {
    'target_platform': 'vrchat',
    'polygon_budget': 50000
})

# 4. Add Robotics Elements
await robotics_mcp.add_robot_to_world("scout", unity_import.id, [10, 0, 10])
```

---

## Related Patterns

- **Tool Family Modularization** - Organizing tools within servers
- **Portmanteau Tools** - Reducing tool explosion
- **State Synchronization** - Managing distributed state
- **Error Propagation** - Cross-boundary error handling

---

**This document defines the architectural patterns for MCP Zoo compositing. These patterns enable complex workflows through coordinated specialization while maintaining clean separation of concerns.**
