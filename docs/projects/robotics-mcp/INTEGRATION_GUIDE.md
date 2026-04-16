# Robotics MCP - Integration Guide

**Last Updated:** 2025-12-11
**Status:** REFERENCE
**Source:** `D:\Dev\repos\robotics-mcp`

---

## Overview

The Robotics MCP orchestrates 6+ specialized MCP servers to provide comprehensive robotics capabilities. This guide covers integration patterns, setup procedures, and cross-server workflows.

---

## MCP Server Composition

### Required MCP Servers

The Robotics MCP requires these specialized servers for full functionality:

| Server | Purpose | Status |
|--------|---------|--------|
| **osc-mcp** | Communication protocol bridge | Required |
| **unity3d-mcp** | 3D environment and physics simulation | Required |
| **avatar-mcp** | Character compositing and manipulation | Required |
| **blender-mcp** | 3D modeling and asset creation | Required |
| **gimp-mcp** | 2D texture and image processing | Required |
| **vrchat-mcp** | Social VR integration | Optional |

### Graceful Degradation

The system continues to function with reduced capabilities when servers are unavailable:

- **Without avatar-mcp:** Basic robot control, no character animation
- **Without unity3d-mcp:** No 3D environment, simulation-only
- **Without blender-mcp:** No custom model creation
- **Without gimp-mcp:** No texture generation

---

## Setup Procedures

### 1. Environment Preparation

```bash
# Ensure all MCP servers are available
mcp-studio discover-mcp-servers

# Verify server health
mcp-studio test-server-connection robotics-mcp
mcp-studio test-server-connection unity3d-mcp
mcp-studio test-server-connection avatar-mcp
mcp-studio test-server-connection osc-mcp
```

### 2. Configuration

```yaml
# config/config.yaml
mcp_integration:
  enabled: true
  servers:
    osc:
      enabled: true
      prefix: "osc"
    unity:
      enabled: true
      prefix: "unity"
    avatar:
      enabled: true
      prefix: "avatar"
    blender:
      enabled: true
      prefix: "blender"
    gimp:
      enabled: true
      prefix: "gimp"
    vrchat:
      enabled: false  # Optional
      prefix: "vrchat"

robotics:
  default_environment: "unity"
  physics_engine: "unity_physics"
  communication_protocol: "osc"
```

### 3. Unity Environment Setup

```python
# Initialize Unity project for robotics
await unity_mcp.create_unity_project_with_univrm(
    project_name="RoboticsLab",
    template="3D (URP)",
    vrm_version="vrm1"
)

# Setup Gaussian Splatting for environments
await unity_mcp.install_gaussian_splatting("RoboticsLab")
```

---

## Integration Workflows

### Complete Robot Lifecycle

```python
# 1. Create Robot Model
robot_model = await blender_mcp.create_robot_model({
    'type': 'scout',
    'wheels': 'mecanum',
    'dimensions': {'length': 0.3, 'width': 0.25, 'height': 0.15}
})

# 2. Setup Unity Environment
environment = await unity_mcp.create_robotics_environment({
    'size': 'large',
    'terrain': 'mixed',
    'lighting': 'realistic'
})

# 3. Import Robot to Unity
robot_import = await unity_mcp.import_robot_model(robot_model, environment)

# 4. Configure Physics
await unity_mcp.configure_robot_physics(robot_import.id, {
    'mass': 5.0,
    'friction': 0.8,
    'restitution': 0.2
})

# 5. Setup OSC Communication
await osc_mcp.setup_robot_communication(robot_import.id, {
    'protocol': 'osc',
    'port': 9000,
    'parameters': ['speed', 'steer', 'pose']
})

# 6. Integrate with Avatar System
await avatar_mcp.integrate_robot(robot_import.id, {
    'avatar_type': 'robot',
    'control_mapping': {
        'speed': 'motor_speed',
        'steer': 'steering_angle'
    }
})

# 7. Spawn Virtual Robot
robot = await robotics_mcp.spawn_virtual_robot("scout", {
    'unity_id': robot_import.id,
    'avatar_id': avatar_integration.id,
    'osc_config': osc_setup
})
```

### Moorebot Scout Integration

```python
# Physical Robot Configuration (Future)
scout_config = {
    'model': 'moorebot-scout',
    'hardware': {
        'wheels': 'mecanum_4x',
        'sensors': ['ydlidar_x4', 'camera_1080p', 'imu_bmi088'],
        'battery': '3000mah_liion',
        'motor_controllers': '4x_outrunner'
    },
    'software': {
        'ros_version': '1.4_melodic',
        'navigation': 'move_base',
        'localization': 'amcl'
    }
}

# Virtual Testing Environment
virtual_scout = await robotics_mcp.create_virtual_scout(scout_config)

# Test Behaviors in Unity
test_results = await robotics_mcp.test_scout_behaviors(virtual_scout.id, [
    'obstacle_avoidance',
    'path_following',
    'object_manipulation',
    'terrain_adaptation'
])

# Performance Validation
performance_metrics = await robotics_mcp.validate_scout_performance(
    virtual_scout.id,
    {
        'speed_tests': [0.5, 1.0, 2.0, 3.0],  # mph
        'terrain_types': ['flat', 'gravel', 'grass', 'mud'],
        'battery_simulation': True,
        'sensor_accuracy_tests': True
    }
)
```

---

## Cross-Server Communication

### OSC Protocol Integration

The Robotics MCP uses OSC (Open Sound Control) for real-time communication, with clean separation between protocol and application layers:

#### OSC Tool Organization Pattern

**Protocol Layer (`osc-mcp`):**
- Generic OSC message sending/receiving
- Connection management
- Protocol-level operations

**Application Layer (`vrchat-mcp`):**
- VRChat-specific OSC conventions
- Avatar parameter control
- VRChat address space management

**Orchestration Layer (`robotics-mcp`):**
- High-level robot commands
- Cross-server coordination
- Domain-specific mappings

```python
# OSC Address Spaces by Layer

# osc-mcp: Generic protocol operations
generic_addresses = {
    '/system/status': 'Status messages',
    '/debug/log': 'Debug logging',
    '/ping': 'Connection testing'
}

# vrchat-mcp: VRChat-specific operations
vrchat_addresses = {
    '/avatar/parameters/VelocityZ': 'Forward/backward movement',
    '/avatar/parameters/VelocityX': 'Left/right movement',
    '/avatar/parameters/AngularY': 'Rotation',
    '/avatar/parameters/Jump': 'Jump trigger'
}

# robotics-mcp: Domain-specific operations
robotics_addresses = {
    '/robot/{id}/motor/speed': 'Motor speed control',
    '/robot/{id}/steer/angle': 'Steering angle',
    '/robot/{id}/sensor/lidar': 'LIDAR data',
    '/robot/{id}/sensor/imu': 'IMU data'
}
```

#### Integration Example

```python
# Robotics-mcp orchestrates both servers
async def control_robot_via_vrchat(self, robot_id: str, command: dict):
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

### State Synchronization

Import IDs ensure state consistency across servers:

```python
# Import ID tracks state across all servers
unity_import = await unity_mcp.import_vrm_to_unity("robot.vrm", "project/")
import_id = unity_import['import_id']

# Same ID used everywhere
avatar_state = await avatar_mcp.get_import_state(import_id)
robotics_state = await robotics_mcp.get_robot_state(import_id)
osc_state = await osc_mcp.get_connection_state(import_id)

# State remains consistent
assert avatar_state['import_id'] == robotics_state['import_id']
assert osc_state['import_id'] == import_id
```

---

## Tool Usage Patterns

### Robot Control Operations

```python
# Basic Movement
await robotics_mcp.robot_control("move", robot_id, {
    'linear_velocity': 1.5,  # m/s
    'angular_velocity': 0.0,  # rad/s
    'duration': 10.0  # seconds
})

# Path Following
await robotics_mcp.robot_navigation("follow_path", robot_id, {
    'path_type': 'spline',
    'waypoints': [
        {'x': 0, 'y': 0, 'z': 0},
        {'x': 5, 'y': 0, 'z': 5},
        {'x': 10, 'y': 2, 'z': 10}
    ],
    'speed': 2.0,  # m/s
    'loop': False
})

# Behavior Execution
await robotics_mcp.robot_behavior("execute", robot_id, {
    'behavior': 'patrol',
    'parameters': {
        'area': {'width': 20, 'height': 20},
        'pattern': 'lawnmower',
        'speed': 1.0
    }
})
```

### Model Management

```python
# Create Custom Robot Model
model = await robotics_mcp.robot_model_tools("create", None, {
    'type': 'wheeled_robot',
    'base_dimensions': {'length': 0.4, 'width': 0.3, 'height': 0.2},
    'wheels': {
        'count': 4,
        'type': 'mecanum',
        'diameter': 0.1,
        'width': 0.02
    }
})

# Import Existing Model
imported = await robotics_mcp.robot_model_tools("import", None, {
    'source_path': 'D:/Models/CustomRobot.fbx',
    'format': 'fbx',
    'optimize_for_unity': True,
    'generate_colliders': True
})

# Convert Model Format
converted = await robotics_mcp.robot_model_tools("convert", imported.id, {
    'target_format': 'obj',
    'optimize_geometry': True,
    'reduce_polygons': 0.8  # 80% reduction
})
```

---

## Testing and Validation

### Virtual Testing Environment

```python
# Setup Test Environment
test_env = await robotics_mcp.create_test_environment({
    'size': 'medium',
    'terrain': 'mixed',
    'obstacles': 'moderate',
    'lighting': 'indoor'
})

# Spawn Test Robot
test_robot = await robotics_mcp.spawn_test_robot("scout", test_env.id)

# Run Automated Tests
test_suite = [
    'basic_movement',
    'obstacle_avoidance',
    'path_following',
    'sensor_integration',
    'physics_simulation',
    'avatar_sync'
]

test_results = {}
for test_name in test_suite:
    result = await robotics_mcp.run_robot_test(test_robot.id, test_name, {
        'duration': 60,  # seconds
        'record_video': True,
        'collect_telemetry': True
    })
    test_results[test_name] = result

# Generate Test Report
report = await robotics_mcp.generate_test_report(test_results, {
    'format': 'html',
    'include_videos': True,
    'performance_metrics': True
})
```

### Performance Validation

```python
# Performance Testing
performance_test = await robotics_mcp.run_performance_test(robot_id, {
    'test_types': [
        'speed_vs_battery',
        'terrain_adaptation',
        'sensor_accuracy',
        'communication_latency'
    ],
    'duration': 300,  # 5 minutes
    'conditions': {
        'temperature': [0, 25, 40],  # Celsius
        'humidity': [30, 60, 90],    # %
        'terrain': ['flat', 'rough', 'wet']
    }
})

# Generate Performance Report
performance_report = await robotics_mcp.analyze_performance_results(
    performance_test.id, {
        'metrics': ['speed', 'efficiency', 'reliability', 'accuracy'],
        'comparison_targets': ['moorebot_specs', 'industry_standards'],
        'recommendations': True
    }
)
```

---

## Troubleshooting

### Common Issues

#### Server Connection Problems
```python
# Check server status
status = await robotics_mcp.get_system_status()
for server_name, server_status in status['servers'].items():
    if not server_status['connected']:
        print(f"Server {server_name} disconnected: {server_status['error']}")

# Restart failed servers
await robotics_mcp.restart_server("unity3d-mcp")
await robotics_mcp.restart_server("avatar-mcp")
```

#### State Synchronization Issues
```python
# Check state consistency
state_check = await robotics_mcp.validate_state_consistency(robot_id)
if not state_check['consistent']:
    print("State inconsistency detected:")
    for issue in state_check['issues']:
        print(f"  - {issue}")

# Force state resync
await robotics_mcp.resync_robot_state(robot_id)
```

#### Performance Problems
```python
# Monitor system performance
performance = await robotics_mcp.get_performance_metrics({
    'time_range': 'last_hour',
    'metrics': ['cpu', 'memory', 'network', 'disk']
})

# Identify bottlenecks
bottlenecks = await robotics_mcp.analyze_performance_bottlenecks(performance)
for bottleneck in bottlenecks:
    print(f"Bottleneck: {bottleneck['component']} - {bottleneck['issue']}")

# Apply optimizations
await robotics_mcp.apply_performance_optimizations(bottlenecks)
```

---

## Future Extensions

### Physical Robot Integration

```python
# ROS 1 Integration (Q1 2026)
ros_config = {
    'ros_version': 'melodic',
    'packages': ['navigation', 'slam', 'control'],
    'hardware_interfaces': ['ydlidar', 'outrunner_motors', 'raspi_camera']
}

physical_scout = await robotics_mcp.integrate_physical_robot("scout", ros_config)

# Twin Reality Testing
await robotics_mcp.enable_twin_reality_testing(physical_scout.id, virtual_scout.id)
```

### Advanced AI Integration

```python
# LLM-Powered Behavior Generation
ai_behavior = await robotics_mcp.generate_behavior_with_ai({
    'description': 'Navigate warehouse and pick items from shelves',
    'constraints': ['avoid_humans', 'optimize_path', 'battery_efficient'],
    'environment': 'industrial_warehouse'
})

# Deploy Generated Behavior
await robotics_mcp.deploy_ai_behavior(robot_id, ai_behavior)
```

---

## Related Documentation

**Project Documentation:**
- `STATUS.md` - Current implementation status
- `STRUCTURE.md` - Project organization
- `ARCHITECTURE.md` - Technical architecture deep dive

**Integration Guides:**
- `../patterns/mcp-zoo-compositing-patterns.md` - Cross-MCP patterns
- `../patterns/osc-tool-organization-pattern.md` - OSC tool organization
- `../patterns/adn-architecture-compositing-deep-dive.md` - Technical deep dive

**MCP Central Docs:**
- `../fastmcp/migration-guide.md` - FastMCP 3.1.1++ migration
- `../tools/zoo-analyzer.md` - MCP Zoo analysis tools

---

**This guide provides comprehensive integration procedures for the Robotics MCP ecosystem. Follow these patterns to achieve seamless orchestration of multiple specialized MCP servers for complete robotics workflows.**

