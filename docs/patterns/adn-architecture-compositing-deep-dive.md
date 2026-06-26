# ADN Architecture & Compositing Deep Dive

**Timestamp**: 2025-12-11 13:45:00  
**Tags**: #architecture #compositing #mcp-orchestration #tool-families #unity3d #robotics #avatar-mcp #fastmcp-3.1.1+  
**Type**: architecture  
**Status**: reference  

---

## Architecture Overview

The MCP Zoo represents a sophisticated compositing architecture where specialized MCP servers work together through well-defined integration patterns, orchestrated by higher-level coordinators.

---

## Core Compositing Patterns

### 1. Tool Family Modularization Pattern

**Problem:** Complex MCP servers with 60+ tools become unmaintainable monoliths.

**Solution:** Tool family modularization with clean separation of concerns.

```
server.py
â”œâ”€â”€ tools/
â”‚   â”œâ”€â”€ __init__.py              # Clean exports
â”‚   â”œâ”€â”€ motor_manager.py         # Motor control family (6 tools)
â”‚   â”œâ”€â”€ path_manager.py          # Path movement family (5 tools)
â”‚   â”œâ”€â”€ import_export_manager.py # Import/export family (11 tools)
â”‚   â””â”€â”€ vrm_avatar_manager.py    # VRM integration family (7 tools)
```

**Implementation Pattern:**
```python
class ToolFamilyManager:
    def __init__(self, mcp_app, config):
        self.app = mcp_app
        self.config = config

    def register_tools(self):
        """Register all tools in this family."""
        # Tool registration logic here
```

**Benefits:**
- **Maintainability:** Each family independently testable
- **Scalability:** New families add zero complexity to core server
- **Discoverability:** 4 families vs 60 individual tools for Claude
- **Parallel Development:** Teams can work on different families

### 2. Unity VRM Integration Pattern

**Problem:** VRM avatars need Unity project integration + advanced compositing.

**Solution:** Unity-focused setup delegates to avatar-mcp for manipulation.

```
Unity Setup (unity3d-mcp) â†’ Avatar Compositing (avatar-mcp)
     â†“                              â†“
Rigging & Materials           Bone Manipulation
Project Integration           Facial Rigging
Build Pipeline               Animation Control
OSC Integration              Physics Simulation
```

**Integration Flow:**
```python
# Phase 1: Unity Integration
import_result = await unity_mcp.import_vrm_to_unity("avatar.vrm", "project/")
import_id = import_result['import_id']

# Phase 2: Avatar Compositing
await avatar_mcp.integrate_with_avatarmcp(import_id, {
    'enable_osc_control': True,
    'setup_animation_sync': True,
    'configure_bone_mapping': True
})
```

**Clean Boundaries:**
- Unity tools: Project setup, rigging, materials, build pipeline
- Avatar-mcp: Bone manipulation, facial rigging, animations, physics

### 3. Robotics Orchestration Pattern

**Problem:** Virtual robotics requires coordination of multiple specialized systems.

**Solution:** Robotics-mcp orchestrates 6+ MCP servers through compositing patterns.

```
Robotics-MCP (Orchestrator)
â”œâ”€â”€ OSC-MCP (Communication)
â”œâ”€â”€ Unity3D-MCP (3D Environment)
â”œâ”€â”€ VRChat-MCP (Social VR)
â”œâ”€â”€ Avatar-MCP (Character Control)
â”œâ”€â”€ Blender-MCP (3D Modeling)
â””â”€â”€ GIMP-MCP (2D Textures)
```

**Orchestration Architecture:**
```python
class RoboticsMCP:
    def __init__(self):
        self.mounted_servers = {
            'osc': osc_mcp,
            'unity': unity_mcp,
            'vrchat': vrchat_mcp,
            'avatar': avatar_mcp,
            'blender': blender_mcp,
            'gimp': gimp_mcp
        }

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

---

## Deep Compositing Patterns

### Cross-MCP State Management

**Challenge:** Maintaining consistent state across multiple MCP servers.

**Pattern:** Import ID tracking with state synchronization.

```python
# State flows through import IDs
unity_import = await unity_mcp.import_vrm_to_unity(vrm_path, project_path)
import_id = unity_import['import_id']  # "unity_vrm_import_avatar.vrm_123456"

# State synchronized across servers
avatar_state = await avatar_mcp.get_import_state(import_id)
robotics_state = await robotics_mcp.get_robot_state(import_id)

# Actions coordinated
await robotics_mcp.control_robot(import_id, "start_motor", {"speed": 3.0})
await avatar_mcp.update_animation(import_id, "walking")
```

**State Synchronization:**
- Import IDs as universal identifiers
- State versioning for conflict resolution
- Event-driven updates between servers
- Rollback capabilities for consistency

### OSC Protocol Integration

**Challenge:** Real-time communication between Unity, VRChat, and robotics systems.

**Pattern:** OSC bridge with avatar-mcp as central hub.

```
Robot Control â†’ OSC Bridge â†’ Avatar-MCP â†’ Unity/VRChat
    â†‘              â†‘              â†“
    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
        Parameter Mapping & Translation
```

**Implementation:**
```python
# OSC message routing
osc_config = {
    'avatar_parameters': {
        '/robot/speed': 'motor_speed',
        '/robot/steer': 'steering_angle',
        '/robot/pose': 'body_pose'
    },
    'unity_parameters': {
        'motor_speed': '/unity/robot/motor',
        'steering_angle': '/unity/robot/steer',
        'body_pose': '/unity/robot/pose'
    }
}

# Avatar-mcp translates OSC to avatar control
await avatar_mcp.setup_osc_mapping(import_id, osc_config)
```

### Path Following & Locomotion

**Challenge:** Complex path following with physics and character animation.

**Pattern:** Multi-layer path execution with Unity physics + avatar animation.

```
High-Level Path â†’ Unity Path Following â†’ Avatar Locomotion â†’ Physics Simulation
     â†“                      â†“                      â†“
  Waypoints            Transform Updates      Bone Animation      Collision Detection
```

**Path Execution Stack:**
```python
# High-level path definition
path_config = {
    'type': 'spline',
    'points': [{'x':0,'y':0,'z':0}, {'x':10,'y':0,'z':10}],
    'loop': False,
    'speed': 3.0  # m/s
}

# Unity path following
unity_path = await unity_mcp.api_move_along_path(
    object_name='robot',
    path_type='spline',
    path_points=path_config['points'],
    duration=10.0
)

# Avatar locomotion sync
await avatar_mcp.sync_locomotion(import_id, path_config)

# Physics integration
await unity_mcp.configure_motor_physics(import_id, {
    'torque_curve': [...],
    'friction_model': 'coulomb'
})
```

---

## Tool Family Architecture Deep Dive

### Manager Class Pattern

**Standard Interface:**
```python
class BaseToolManager:
    def __init__(self, mcp_app, config):
        self.app = mcp_app
        self.config = config
        self.active_operations = {}  # Track async operations

    def register_tools(self):
        """Register all tools in this family."""
        raise NotImplementedError

    async def _validate_operation(self, operation, params):
        """Validate operation parameters."""
        pass

    async def _execute_operation(self, operation, params):
        """Execute validated operation."""
        pass
```

**Motor Manager Example:**
```python
class MotorManager(BaseToolManager):
    def register_tools(self):
        @self.app.tool
        async def api_start_motor(self, object_name: str, target_speed: float, ...):
            """Start motor with speed/acceleration control."""
            # Validation
            await self._validate_motor_exists(object_name)

            # State tracking
            motor_id = f"{object_name}_motor"
            self.active_operations[motor_id] = {
                'status': 'starting',
                'target_speed': target_speed,
                'start_time': time.time()
            }

            # Execution
            result = await self._execute_motor_start(object_name, target_speed, ...)

            # State update
            self.active_operations[motor_id].update({
                'status': 'running',
                'current_speed': 0.0,
                'result': result
            })

            return result
```

### Async Operation Tracking

**Pattern:** Track long-running operations with status monitoring.

```python
class OperationTracker:
    def __init__(self):
        self.operations = {}
        self._cleanup_task = asyncio.create_task(self._periodic_cleanup())

    async def track_operation(self, op_id, operation_type, params):
        """Track async operation."""
        self.operations[op_id] = {
            'type': operation_type,
            'params': params,
            'status': 'running',
            'start_time': time.time(),
            'progress': 0.0
        }
        return op_id

    async def update_progress(self, op_id, progress, message=None):
        """Update operation progress."""
        if op_id in self.operations:
            self.operations[op_id].update({
                'progress': progress,
                'message': message,
                'last_update': time.time()
            })

    async def get_status(self, op_id):
        """Get operation status."""
        return self.operations.get(op_id, {'status': 'not_found'})
```

---

## Cross-MCP Communication Patterns

### Mounted Server Pattern

**Robotics-MCP Implementation:**
```python
class RoboticsMCP:
    def __init__(self):
        self.mounted_servers = {}
        self._load_mounted_servers()

    def _load_mounted_servers(self):
        """Load and mount external MCP servers."""
        try:
            # Load avatar-mcp for internal use
            from avatarmcp.server import AvatarMCPServer
            self.mounted_servers['avatar'] = AvatarMCPServer()
        except ImportError:
            logger.warning("avatar-mcp not available")

    async def call_mounted_server_tool(self, server_name, tool_name, params):
        """Call tool on mounted server."""
        if server_name not in self.mounted_servers:
            raise ValueError(f"Server {server_name} not mounted")

        server = self.mounted_servers[server_name]
        return await server.call_tool(tool_name, params)
```

### Error Propagation Pattern

**Cross-Server Error Handling:**
```python
class CrossMCPEror(Exception):
    def __init__(self, server_name, tool_name, original_error):
        self.server_name = server_name
        self.tool_name = tool_name
        self.original_error = original_error
        super().__init__(f"{server_name}.{tool_name}: {original_error}")

async def safe_cross_call(server_name, tool_name, params):
    """Safe cross-server tool call with error handling."""
    try:
        result = await call_mounted_server_tool(server_name, tool_name, params)
        return result
    except Exception as e:
        # Wrap in cross-server context
        raise CrossMCPEror(server_name, tool_name, e) from e
```

### State Synchronization Pattern

**Distributed State Management:**
```python
class DistributedState:
    def __init__(self):
        self.server_states = {}  # {server_name: {import_id: state}}
        self.state_versions = {}  # Version tracking for conflicts

    async def sync_state(self, import_id, server_name, state_update):
        """Synchronize state across servers."""
        current_version = self.state_versions.get(import_id, 0)
        new_version = current_version + 1

        # Check for conflicts
        if import_id in self.server_states.get(server_name, {}):
            existing = self.server_states[server_name][import_id]
            if existing.get('version', 0) > current_version:
                # Conflict resolution
                await self._resolve_conflict(import_id, server_name, state_update)

        # Apply update
        if server_name not in self.server_states:
            self.server_states[server_name] = {}

        self.server_states[server_name][import_id] = {
            **state_update,
            'version': new_version,
            'timestamp': time.time()
        }

        self.state_versions[import_id] = new_version
```

---

## Performance & Scalability Patterns

### Tool Family Parallelization

**Pattern:** Independent tool families can execute in parallel.

```python
async def execute_parallel_operations(operations):
    """Execute operations across tool families in parallel."""
    # Group by tool family
    family_ops = {}
    for op in operations:
        family = op['family']
        if family not in family_ops:
            family_ops[family] = []
        family_ops[family].append(op)

    # Execute families in parallel
    tasks = []
    for family, ops in family_ops.items():
        task = asyncio.create_task(
            execute_family_operations(family, ops)
        )
        tasks.append(task)

    # Wait for all families to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Resource Pooling Pattern

**Pattern:** Shared resource pools for cross-family operations.

```python
class ResourcePool:
    def __init__(self):
        self.pools = {
            'unity_scenes': asyncio.Queue(maxsize=10),
            'avatar_imports': asyncio.Queue(maxsize=5),
            'osc_connections': asyncio.Queue(maxsize=20)
        }

    async def acquire_resource(self, resource_type, timeout=30):
        """Acquire resource from pool."""
        try:
            resource = await asyncio.wait_for(
                self.pools[resource_type].get(),
                timeout=timeout
            )
            return resource
        except asyncio.TimeoutError:
            raise ResourceTimeout(f"No {resource_type} available")

    async def release_resource(self, resource_type, resource):
        """Release resource back to pool."""
        await self.pools[resource_type].put(resource)
```

---

## Testing & Validation Patterns

### Tool Family Integration Testing

**Pattern:** Test tool families in isolation and integration.

```python
class ToolFamilyTestSuite:
    def test_motor_family_isolation(self):
        """Test motor family independently."""
        motor_manager = MotorManager(mock_mcp_app, test_config)

        # Test individual tools
        result = await motor_manager.api_start_motor("test_robot", 5.0)
        assert result['success'] == True
        assert result['target_speed'] == 5.0

    def test_cross_family_integration(self):
        """Test interaction between families."""
        motor_mgr = MotorManager(mcp_app, config)
        path_mgr = PathManager(mcp_app, config)

        # Create path
        path_result = await path_mgr.api_move_along_path(
            object_name="robot",
            path_type="straight",
            path_points=[{"x":0,"y":0,"z":0}, {"x":10,"y":0,"z":0}]
        )

        # Start motor for path following
        motor_result = await motor_mgr.api_start_motor("robot", 3.0)

        # Verify integration
        assert path_result['object_name'] == motor_result['object_name']
```

### Compositing Validation Pattern

**Pattern:** Validate cross-MCP compositing works correctly.

```python
async def validate_robotics_compositing():
    """Validate full robotics compositing workflow."""
    # Setup test environment
    unity_server = await setup_test_unity_server()
    avatar_server = await setup_test_avatar_server()

    # Execute compositing workflow
    import_result = await unity_server.import_vrm_to_unity("test.vrm", "test_project")
    import_id = import_result['import_id']

    integration_result = await avatar_server.integrate_with_avatarmcp(import_id, {
        'enable_osc_control': True
    })

    # Validate state consistency
    unity_state = await unity_server.get_unity_import_status(import_id)
    avatar_state = await avatar_server.get_avatar_state(import_id)

    assert unity_state['status'] == 'complete'
    assert avatar_state['osc_enabled'] == True
    assert unity_state['import_id'] == avatar_state['import_id']
```

---

## Future Evolution Patterns

### Plugin Architecture Extension

**Pattern:** Tool families as dynamically loadable plugins.

```python
class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = Path("plugins/")

    async def load_plugin(self, plugin_name):
        """Load tool family plugin."""
        plugin_path = self.plugin_dir / f"{plugin_name}_manager.py"

        # Dynamic import
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Instantiate and register
        manager_class = getattr(module, f"{plugin_name.title()}Manager")
        manager = manager_class(self.mcp_app, self.config)
        manager.register_tools()

        self.plugins[plugin_name] = manager

    async def unload_plugin(self, plugin_name):
        """Unload tool family plugin."""
        if plugin_name in self.plugins:
            # Cleanup resources
            await self.plugins[plugin_name].cleanup()
            del self.plugins[plugin_name]
```

### Distributed MCP Orchestration

**Pattern:** Orchestrate MCP servers across network boundaries.

```python
class DistributedMCPOrchestrator:
    def __init__(self):
        self.remote_servers = {}  # {name: connection}
        self.local_servers = {}   # Local mounted servers

    async def call_remote_server(self, server_name, tool_name, params):
        """Call tool on remote MCP server."""
        if server_name not in self.remote_servers:
            connection = await self._establish_connection(server_name)
            self.remote_servers[server_name] = connection

        connection = self.remote_servers[server_name]
        return await connection.call_tool(tool_name, params)

    async def orchestrate_distributed_workflow(self, workflow):
        """Execute workflow across distributed MCP servers."""
        # Parse workflow DAG
        tasks = self._parse_workflow_dag(workflow)

        # Execute with dependency resolution
        results = await self._execute_with_dependencies(tasks)

        return results
```

---

## Conclusion

The MCP Zoo compositing architecture represents a sophisticated approach to distributed AI tool orchestration. Through tool family modularization, clean integration patterns, and cross-MCP state management, we've created a scalable and maintainable ecosystem.

**Key Achievements:**
- Tool family modularization reduces complexity while improving maintainability
- Unity VRM integration cleanly separates project setup from avatar manipulation
- Robotics orchestration successfully coordinates 6+ specialized MCP servers
- Cross-MCP compositing enables complex workflows through simple APIs

**Future Evolution:**
- Plugin architecture for dynamic tool family loading
- Distributed orchestration across network boundaries
- Advanced state synchronization and conflict resolution
- Performance optimization through resource pooling and parallelization

This architecture provides a solid foundation for the growing MCP ecosystem, enabling complex AI workflows through composable, specialized servers.

---

## References

**Related ADN Notes:**
- [[2025-12-11-mcp-zoo-integration-progress]]
- [[MCP Portmanteau Tools]]
- [[Unity3D Integration]]
- [[Avatar Compositing]]
- [[Robotics Orchestration]]

**MCP Central Docs:**
- `STANDARDS.md` - Updated documentation standards
- `docs/fastmcp/migration-guide.md` - FastMCP 3.1.1++ migration
- `docs/tools/zoo-analyzer.md` - MCP Zoo analysis tools

**Code References:**
- `unity3d-mcp/src/unity3d_mcp/tools/` - Tool family implementations
- `robotics-mcp/src/robotics_mcp/server.py` - Orchestration patterns
- `avatar-mcp/src/avatarmcp/` - Compositing server

