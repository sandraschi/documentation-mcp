# Blender MCP - Status

**Repository**: [blender-mcp](https://github.com/sandraschi/blender-mcp)
**FastMCP Version**: 3.1.1+.1  
**Status**: âœ… SOTA (State of the Art)

## Overview

Comprehensive MCP server for Blender 3D automation. Provides programmatic control over modeling, animation, materials, rendering, and export workflows. Fully supports VRM avatar workflows. Includes batch workflow tool for macro execution.

## Tool Summary

| Tools | Operations | Pattern |
|-------|------------|---------|
| 33 | 100+ | Portmanteau |

## Portmanteau Tools

| Tool | Operations | Description |
|------|------------|-------------|
| `blender_mesh` | 9 | Create/manipulate 3D primitives |
| `blender_animation` | **21** | Keyframes, shape keys, actions, baking |
| `blender_rigging` | **8** | Armatures, bone posing, VRM support |
| `blender_materials` | 7 | PBR materials (fabric, metal, wood, glass) |
| `blender_scene` | 12 | Scene, collection, lighting, camera |
| `blender_lighting` | 7 | Sun, point, spot, area, HDRI |
| `blender_camera` | 3 | Camera creation and lens settings |
| `blender_physics` | 8 | Rigid body, cloth, soft body, fluid |
| `blender_particles` | 7 | Particle systems and effects |
| `blender_modifiers` | 12 | Subsurf, bevel, mirror, array, boolean |
| `blender_transform` | 8 | Location, rotation, scale operations |
| `blender_selection` | 6 | Select by name, type, material |
| `blender_textures` | 7 | Procedural textures |
| `blender_uv` | 5 | UV mapping operations |
| `blender_render` | 4 | Preview, turntable, animation render |
| `blender_export` | 2 | Unity/VRChat export |
| `blender_import` | 2 | FBX, OBJ, glTF import |
| `blender_furniture` | 9 | Chairs, tables, beds, sofas |
| `blender_addons` | 3 | Addon management |
| `blender_help` | 5 | Help system |
| `blender_status` | 4 | System status |
| `blender_download` | 2 | Asset downloads |
| `blender_log` | 2 | Log viewing |
| `blender_workflow` | 3 | Batch execution, templates, macros |

## VRM Workflow Support â­

Complete workflow for VRM avatar animation:

```python
# 1. Import VRM model
blender_import(operation="import_gltf", filepath="avatar.vrm")

# 2. Discover bone structure
blender_rigging(operation="list_bones", armature_name="Armature")

# 3. Find facial expressions
blender_animation(operation="list_shape_keys", object_name="Face")

# 4. Pose bones
blender_rigging(operation="pose_bone", armature_name="Armature", 
                bone_name="leftUpperArm", rotation=[0, 0, 90])

# 5. Set facial expression
blender_animation(operation="set_shape_key", object_name="Face", 
                  shape_key_name="happy", value=1.0)

# 6. Keyframe poses
blender_rigging(operation="set_bone_keyframe", armature_name="Armature", 
                bone_name="leftUpperArm", frame=1)
blender_animation(operation="keyframe_shape_key", object_name="Face", 
                  shape_key_name="happy", frame=1)

# 7. Bake for export
blender_animation(operation="bake_action", object_name="Armature", 
                  start_frame=1, end_frame=120)
```

## Animation Features

### Shape Keys (VRM Expressions)
- `list_shape_keys` - Discover morphs/expressions
- `set_shape_key` - Set expression value (0-1)
- `keyframe_shape_key` - Animate expressions
- `create_shape_key` - Add new morph targets

### Action Management
- `list_actions` - List animation clips
- `create_action` - Create new clip
- `set_active_action` - Assign to object
- `push_to_nla` - Layer animations

### Bone Animation
- `list_bones` - Discover VRM bone names
- `pose_bone` - Rotate/position bones
- `set_bone_keyframe` - Keyframe bone poses
- `reset_pose` - Return to rest position

### Interpolation & Constraints
- `set_interpolation` - LINEAR, BEZIER, BOUNCE, ELASTIC
- `set_easing` - EASE_IN, EASE_OUT, EASE_IN_OUT
- `add_constraint` - Object constraints
- `add_bone_constraint` - Bone constraints

### Baking
- `bake_action` - Constraints â†’ keyframes
- `bake_all_actions` - NLA â†’ single action

## CI/CD

- âœ… GitHub Actions (lint, test, release)
- âœ… Ruff linting
- âœ… Dependabot (monthly, grouped)

## Recent Changes

### 2025-11-29
- **Portmanteau refactor**: 49 â†’ 33 tools
- **VRM workflow**: Complete bone + shape key animation
- **Animation expansion**: 7 â†’ 21 operations
- **Rigging expansion**: 4 â†’ 8 operations
- **Fixed import paths**: All subdirectory tools now load correctly
- **NEW: blender_workflow**: Batch/macro execution tool
  - Execute multiple operations in single call
  - Predefined templates (product_shot, simple_scene, turntable_setup)
  - Variable passing between steps
  - Conditional execution

## Installation

```json
{
  "mcpServers": {
    "blender": {
      "command": "uv",
      "args": ["run", "--directory", "D:/Dev/repos/blender-mcp", "blender-mcp"]
    }
  }
}
```

## Requirements

- Blender 4.0+ installed
- Python 3.10+
- FastMCP 3.1.1++


