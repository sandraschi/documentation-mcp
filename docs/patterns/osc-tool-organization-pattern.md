# OSC Tool Organization Pattern

**Last Updated:** 2025-12-11
**Status:** STANDARD
**Applies To:** osc-mcp, vrchat-mcp, robotics-mcp

---

## The Question

**Where should OSC tools live when multiple MCP servers handle OSC protocols?**

- Should OSC protocol tools be in `vrchat-mcp` (VRChat-specific)?
- Should VRChat tools be in `osc-mcp` (protocol-specific)?
- How to organize when both must be composited in `robotics-mcp`?

---

## The Answer: Clean Layer Separation

**OSC tools should be organized by responsibility layer, not by platform.**

### 1. Protocol Layer: `osc-mcp`

**Generic OSC protocol operations:**
- Message sending/receiving (any destination)
- Connection management (servers, clients)
- Protocol-level configuration
- Transport reliability

**Tools:**
```python
# osc-mcp tools
async def send_osc_message(address: str, args: list, host: str = "127.0.0.1", port: int = 9000)
async def receive_osc_messages(callback: Callable, port: int = 9001)
async def setup_osc_server(port: int, handlers: dict)
async def test_osc_connection(host: str, port: int)
async def get_osc_server_status()
```

### 2. Application Layer: `vrchat-mcp`

**VRChat-specific OSC operations:**
- Avatar parameter control
- VRChat address space management
- Platform-specific conventions
- VRChat authentication integration

**Tools:**
```python
# vrchat-mcp tools
async def control_avatar_parameter(parameter: str, value: float)
async def set_vrchat_avatar_pose(pose_data: dict)
async def trigger_vrchat_emote(emote_id: str)
async def get_vrchat_parameter_list()
async def setup_vrchat_osc_routing()
```

### 3. Orchestration Layer: `robotics-mcp`

**High-level domain operations:**
- Robot-to-OSC command translation
- Cross-server coordination
- Domain-specific workflows
- State management

**Tools:**
```python
# robotics-mcp tools
async def control_robot_via_vrchat(robot_id: str, command: dict)
async def spawn_robot_with_osc_control(robot_config: dict)
async def monitor_robot_osc_feedback(robot_id: str)
async def calibrate_robot_osc_mapping(robot_id: str, calibration_data: dict)
```

---

## Why This Organization Works

### Clean Separation of Concerns

**Protocol Layer (`osc-mcp`):**
- Knows nothing about VRChat, Unity, or robotics
- Pure OSC protocol implementation
- Reusable by any application needing OSC

**Application Layer (`vrchat-mcp`):**
- Knows VRChat conventions and limitations
- Handles platform-specific requirements
- Translates between generic OSC and VRChat specifics

**Orchestration Layer (`robotics-mcp`):**
- Knows robot control semantics
- Coordinates multiple servers for complex workflows
- Provides high-level robot control API

### Compositing Benefits

**No Tool Duplication:**
- OSC protocol tools only in `osc-mcp`
- VRChat tools only in `vrchat-mcp`
- Robotics orchestration in `robotics-mcp`

**Clean Dependencies:**
```python
# robotics-mcp orchestrates both
class RoboticsMCP:
    async def control_robot_via_vrchat(self, robot_id: str, command: dict):
        # 1. Convert robot command to VRChat OSC
        osc_command = await self.convert_robot_to_vrchat_osc(command)

        # 2. Send via osc-mcp (protocol layer)
        await self.mounted_servers['osc'].send_osc_message(
            osc_command['address'],
            osc_command['args']
        )

        # 3. Verify via vrchat-mcp (application layer)
        await self.mounted_servers['vrchat'].verify_parameter_set(
            osc_command['parameter'],
            osc_command['expected_value']
        )
```

**Flexible Architecture:**
- Can replace `vrchat-mcp` with `unity-mcp` for Unity OSC control
- Can add new application layers (e.g., `resonite-mcp`)
- Protocol layer remains stable and reusable

---

## Real-World Examples

### Robot Control via VRChat Avatar

```python
# High-level robotics command
await robotics_mcp.robot_control("move", robot_id, {
    'linear_velocity': 1.5,  # m/s forward
    'angular_velocity': 0.0  # no rotation
})

# Gets translated to:
# 1. Robotics layer: Convert to VRChat avatar movement
# 2. OSC layer: Send "/avatar/parameters/VelocityZ 1.5"
# 3. VRChat layer: Verify avatar is moving forward
```

### Avatar Animation Control

```python
# VRChat-specific command
await vrchat_mcp.control_avatar_parameter("VelocityZ", 2.0)

# Uses:
# 1. VRChat layer: Knows VelocityZ controls forward/backward
# 2. OSC layer: Sends message to VRChat OSC port
# 3. Protocol layer: Handles reliable message delivery
```

### Generic OSC Communication

```python
# Protocol-level command
await osc_mcp.send_osc_message("/custom/parameter", [42], "192.168.1.100", 9000)

# Uses:
# 1. OSC layer: Pure protocol implementation
# 2. No application-specific knowledge required
```

---

## Implementation Guidelines

### Tool Naming Conventions

**Protocol Layer (`osc-mcp`):**
- `send_osc_message()` - Generic sending
- `receive_osc_messages()` - Generic receiving
- `setup_osc_server()` - Server management
- `test_osc_connection()` - Connectivity testing

**Application Layer (`vrchat-mcp`):**
- `control_avatar_parameter()` - VRChat avatar control
- `set_vrchat_avatar_pose()` - VRChat pose setting
- `get_vrchat_parameter_list()` - VRChat parameter discovery
- `setup_vrchat_osc_routing()` - VRChat-specific routing

**Orchestration Layer (`robotics-mcp`):**
- `control_robot_via_vrchat()` - Domain-specific control
- `spawn_robot_with_osc_control()` - Setup orchestration
- `monitor_robot_osc_feedback()` - Monitoring orchestration

### Address Space Management

**Protocol Layer:** Generic address validation
```python
# osc-mcp validates OSC address format
def validate_osc_address(address: str) -> bool:
    return address.startswith('/') and len(address.split('/')) >= 2
```

**Application Layer:** Platform-specific address knowledge
```python
# vrchat-mcp knows VRChat OSC addresses
VRCHAT_ADDRESSES = {
    '/avatar/parameters/VelocityZ': 'Forward/backward movement',
    '/avatar/parameters/VelocityX': 'Left/right movement',
    '/avatar/parameters/AngularY': 'Rotation'
}
```

**Orchestration Layer:** Domain-specific address mapping
```python
# robotics-mcp maps robot commands to OSC addresses
ROBOT_TO_OSC_MAPPING = {
    'forward': '/avatar/parameters/VelocityZ',
    'turn': '/avatar/parameters/AngularY',
    'jump': '/avatar/parameters/Jump'
}
```

---

## Migration Guide

### If You Have Mixed OSC Tools

**Step 1: Identify Tool Types**
```python
# Analyze existing tools
mixed_tools = [
    'send_osc_message',           # → osc-mcp (protocol)
    'control_vrchat_avatar',      # → vrchat-mcp (application)
    'robot_osc_control',          # → robotics-mcp (orchestration)
    'setup_osc_server',          # → osc-mcp (protocol)
    'vrchat_parameter_list',      # → vrchat-mcp (application)
]
```

**Step 2: Move Tools to Correct Servers**
```python
# Move protocol tools to osc-mcp
# Move VRChat tools to vrchat-mcp
# Keep orchestration tools in robotics-mcp
# Update import statements and cross-server calls
```

**Step 3: Update Compositing**
```python
# Before: Direct tool calls
await vrchat_mcp.send_osc_message(address, args)  # Wrong!

# After: Clean layer separation
await osc_mcp.send_osc_message(address, args)     # Protocol layer
await vrchat_mcp.control_avatar_parameter(param, value)  # Application layer
```

---

## Benefits Summary

### For Developers
- **Clear ownership:** Each tool belongs to one server
- **Reduced complexity:** Protocol vs application separation
- **Better testing:** Each layer can be tested independently
- **Easier maintenance:** Changes isolated to appropriate layer

### For Compositing
- **No conflicts:** Tools don't duplicate across servers
- **Clean APIs:** Each server has well-defined responsibilities
- **Flexible orchestration:** Easy to mix and match layers
- **Future-proof:** New applications can reuse protocol layer

### For Users
- **Consistent experience:** Same OSC tools work across platforms
- **Clear documentation:** Tools organized by purpose
- **Predictable behavior:** Protocol layer provides reliability

---

## Related Patterns

- **Tool Family Modularization** - Organizing tools within servers
- **MCP Server Compositing** - Orchestrating multiple MCP servers
- **Cross-Server State Management** - Managing state across boundaries
- **Protocol vs Application Separation** - Clean abstraction layers

---

**This pattern ensures OSC tools are organized by responsibility rather than platform, enabling clean compositing while preventing duplication and confusion.**
