# Blender MCP Integration Guide

## Overview

This guide provides comprehensive instructions for integrating Blender with MCP (Model Context Protocol) servers, enabling automated 3D content creation, processing, and pipeline management.

## Architecture Overview

### Blender MCP Server Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   MCP Client    â”‚â”€â”€â”€â–¶â”‚  Blender MCP     â”‚â”€â”€â”€â–¶â”‚   Blender App   â”‚
â”‚   (Python/Node) â”‚    â”‚   Server         â”‚    â”‚   (GUI/Headless)â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚                       â”‚                       â”‚
         â–¼                       â–¼                       â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Robotics MCP    â”‚    â”‚ CAD Converter    â”‚    â”‚ Unity3D MCP     â”‚
â”‚ (Simulation)    â”‚    â”‚ (Mayo)          â”‚    â”‚ (Game Dev)      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Communication Patterns

- **Synchronous**: Direct Python API calls for immediate operations
- **Asynchronous**: Background processing for rendering and simulation
- **Streaming**: Real-time updates for interactive operations
- **Batch Processing**: Queue-based processing for large operations

## Installation & Setup

### Prerequisites

**System Requirements:**
- **OS**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- **RAM**: 8GB minimum, 32GB recommended
- **GPU**: OpenGL 3.3+ compatible (NVIDIA/AMD/Intel)
- **Storage**: 10GB for Blender + workspace

**Software Dependencies:**
- Python 3.10+ (included with Blender)
- Blender 4.0+ (recommended 4.2.x)
- MCP server libraries

### Blender Installation

#### Windows Installation

1. **Download**: Get Blender from [official website](https://www.blender.org/download/)
2. **Install**: Run installer with default options
3. **Verify**: Open Blender and check version in Help â†’ About Blender

```powershell
# Command line verification
& "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --version
```

#### Linux Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install blender

# Or download AppImage
wget https://www.blender.org/download/release/Blender4.2/blender-4.2.0-linux-x64.tar.xz
tar -xf blender-4.2.0-linux-x64.tar.xz
sudo mv blender-4.2.0-linux-x64 /opt/blender
sudo ln -s /opt/blender/blender /usr/local/bin/blender
```

#### macOS Installation

```bash
# Homebrew
brew install blender

# Or download DMG from website
# Mount DMG and drag to Applications
```

### MCP Server Setup

#### blender-mcp Installation

```bash
# Clone and install
git clone https://github.com/your-org/blender-mcp.git
cd blender-mcp
pip install -e .

# Configure Blender path
export BLENDER_EXECUTABLE="/path/to/blender"
```

#### Configuration File

```json
{
  "blender": {
    "executable": "/usr/bin/blender",
    "version": "4.2",
    "python_path": "/usr/lib/python3.10",
    "default_scene": "default.blend",
    "render_engine": "CYCLES",
    "device": "GPU"
  },
  "workspace": {
    "temp_dir": "/tmp/blender_mcp",
    "cache_dir": "/var/cache/blender_mcp",
    "output_dir": "/home/user/blender_output"
  },
  "performance": {
    "max_concurrent_jobs": 4,
    "timeout": 3600,
    "memory_limit": "8GB"
  }
}
```

## Basic Usage

### Connecting to Blender

```python
from blender_mcp import BlenderClient

# Initialize client
client = BlenderClient()

# Connect to running Blender instance or start new one
await client.connect()

# Verify connection
info = await client.get_blender_info()
print(f"Connected to Blender {info['version']}")
```

### Basic Operations

#### Creating Objects

```python
# Create primitive objects
cube = await client.create_object("cube", location=(0, 0, 0), size=2.0)
sphere = await client.create_object("sphere", location=(3, 0, 0), radius=1.0)
plane = await client.create_object("plane", location=(0, 0, -1), size=10.0)

# Create custom mesh
vertices = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
faces = [(0,1,2,3)]
mesh = await client.create_mesh_object("quad", vertices, faces)
```

#### Material and Texturing

```python
# Create PBR material
material = await client.create_material("metal_material", material_type="pbr")

# Set material properties
await client.set_material_property(material, "base_color", (0.8, 0.2, 0.1, 1.0))
await client.set_material_property(material, "metallic", 0.9)
await client.set_material_property(material, "roughness", 0.1)

# Apply material to object
await client.assign_material(cube, material)

# Add texture
texture = await client.create_texture("diffuse_tex", "/path/to/diffuse.png")
await client.assign_texture(material, texture, "base_color")
```

#### Transformations

```python
# Position, rotation, scale
await client.set_location(cube, (2, 3, 1))
await client.set_rotation(cube, (0, 0, 45))  # degrees
await client.set_scale(cube, (2, 1, 0.5))

# Relative transformations
await client.translate(cube, (1, 0, 0))
await client.rotate(cube, (0, 90, 0))
await client.scale(cube, (1.5, 1.5, 1.5))
```

## Advanced Features

### Geometry Nodes

```python
# Create geometry nodes setup
geo_nodes = await client.create_geometry_nodes_modifier(cube, "ProceduralCube")

# Add nodes
input_node = await client.add_geo_node(geo_nodes, "GeometryNodeGroupInput")
output_node = await client.add_geo_node(geo_nodes, "GeometryNodeGroupOutput")

# Create subdivision surface
subdiv_node = await client.add_geo_node(geo_nodes, "GeometryNodeSubdivisionSurface")
await client.set_node_property(subdiv_node, "level", 2)

# Connect nodes
await client.connect_geo_nodes(input_node, "geometry", subdiv_node, "mesh")
await client.connect_geo_nodes(subdiv_node, "mesh", output_node, "geometry")
```

### Animation

```python
# Create animation
await client.set_frame_current(1)
await client.set_location(cube, (0, 0, 0))

await client.set_frame_current(60)  # 2 seconds at 30fps
await client.set_location(cube, (5, 0, 0))

# Insert keyframes
await client.insert_keyframe(cube, "location", frame=1)
await client.insert_keyframe(cube, "location", frame=60)

# Set interpolation
await client.set_fcurve_interpolation(cube, "location", "BEZIER")
```

### Rendering

```python
# Configure render settings
await client.set_render_engine("CYCLES")
await client.set_render_resolution(1920, 1080)
await client.set_render_samples(128)

# Set up camera
camera = await client.create_camera("render_camera", location=(10, -10, 5))
await client.point_camera_at(camera, cube)

# Add lighting
light = await client.create_light("key_light", type="SUN", location=(5, -5, 10))
await client.set_light_energy(light, 5.0)

# Render frame
await client.render_frame("/output/frame_001.png")

# Render animation
await client.render_animation("/output/animation.mp4", start_frame=1, end_frame=120)
```

## Integration Workflows

### CAD to Blender Pipeline

```python
from blender_mcp import BlenderClient
from mayo_mcp import MayoConverter

async def cad_to_blender_pipeline(cad_files, output_dir):
    """Complete CAD to Blender conversion pipeline."""

    # Initialize clients
    blender = BlenderClient()
    mayo = MayoConverter()

    await blender.connect()

    imported_objects = []

    for cad_file in cad_files:
        # Convert CAD to OBJ using Mayo
        mesh_file = await mayo.convert_cad(
            cad_path=cad_file,
            output_format="obj",
            scale_factor=0.001,  # mm to meters
            mesh_quality="high"
        )

        # Import to Blender
        obj = await blender.import_obj(mesh_file)
        imported_objects.append(obj)

        # Apply materials
        material = await blender.create_material(f"{obj.name}_mat")
        await blender.assign_material(obj, material)

    # Create collection for imported objects
    collection = await blender.create_collection("CAD_Imports")
    for obj in imported_objects:
        await blender.move_to_collection(obj, collection)

    # Save scene
    await blender.save_scene(f"{output_dir}/cad_import.blend")

    return imported_objects
```

### Game Asset Pipeline

```python
async def create_game_asset_pipeline(source_mesh, texture_dir, output_dir):
    """Create game-ready asset with LOD variants."""

    blender = BlenderClient()
    await blender.connect()

    # Import base mesh
    base_obj = await blender.import_fbx(source_mesh)

    # Setup PBR materials
    materials = await setup_pbr_materials(blender, texture_dir)
    for material in materials:
        await blender.assign_material(base_obj, material)

    # Create LOD variants
    lod0 = base_obj
    lod1 = await blender.create_lod_variant(base_obj, reduction=0.5, name="LOD1")
    lod2 = await blender.create_lod_variant(base_obj, reduction=0.25, name="LOD2")

    # Optimize for game engines
    for obj in [lod0, lod1, lod2]:
        await blender.optimize_mesh(obj, target_tris=1000)
        await blender.add_uv_unwrap(obj)
        await blender.generate_lightmap_uv(obj)

    # Export for Unity
    await blender.export_unity_package(
        objects=[lod0, lod1, lod2],
        filepath=f"{output_dir}/asset.unitypackage",
        include_materials=True,
        include_textures=True
    )

    # Export for Unreal
    await blender.export_unreal_assets(
        objects=[lod0, lod1, lod2],
        filepath=f"{output_dir}/asset_unreal",
        format="fbx"
    )
```

### Architectural Visualization

```python
async def create_architectural_scene(building_data, output_dir):
    """Create architectural visualization scene."""

    blender = BlenderClient()
    await blender.connect()

    # Setup scene
    await blender.set_scene_unit("meters")
    await blender.set_render_engine("CYCLES")

    # Create ground plane
    ground = await blender.create_object("plane", size=100.0)
    ground_mat = await blender.create_material("ground_mat", color=(0.2, 0.4, 0.1))
    await blender.assign_material(ground, ground_mat)

    # Import building geometry
    building = await blender.import_obj(building_data["mesh_file"])

    # Apply architectural materials
    materials = await create_architectural_materials(blender, building_data["materials"])
    for material_data in materials:
        await blender.assign_material(building, material_data["material"])

    # Setup lighting
    sun_light = await blender.create_light("sun", type="SUN", energy=5.0)
    await blender.set_light_rotation(sun_light, (-45, 0, 45))

    # Add HDRI environment
    await blender.set_hdri_environment("/path/to/studio_hdri.hdr")

    # Setup cameras
    cameras = await setup_cameras(blender, building_data["camera_positions"])

    # Render views
    for i, camera in enumerate(cameras):
        await blender.set_active_camera(camera)
        await blender.render_frame(f"{output_dir}/view_{i:02d}.png")
```

## Scripting and Automation

### Custom Addon Development

```python
# blender_addon_template.py
bl_info = {
    "name": "MCP Integration Addon",
    "author": "MCP Team",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > MCP",
    "description": "MCP server integration for Blender",
    "category": "Interface",
}

import bpy
from .mcp_client import MCPClient

class MCP_OT_Connect(bpy.types.Operator):
    """Connect to MCP server"""
    bl_idname = "mcp.connect"
    bl_label = "Connect to MCP"

    def execute(self, context):
        client = MCPClient()
        bpy.context.scene.mcp_client = client
        return {'FINISHED'}

class MCP_PT_Panel(bpy.types.Panel):
    """MCP Integration Panel"""
    bl_label = "MCP Server"
    bl_idname = "MCP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MCP'

    def draw(self, context):
        layout = self.layout

        if hasattr(bpy.context.scene, 'mcp_client'):
            layout.label(text="Connected to MCP Server")
            layout.operator("mcp.execute_tool")
        else:
            layout.operator("mcp.connect")

def register():
    bpy.utils.register_class(MCP_OT_Connect)
    bpy.utils.register_class(MCP_PT_Panel)

def unregister():
    bpy.utils.unregister_class(MCP_OT_Connect)
    bpy.utils.unregister_class(MCP_PT_Panel)

if __name__ == "__main__":
    register()
```

### Batch Processing

```python
import asyncio
from pathlib import Path

async def batch_process_blend_files(input_dir, output_dir, operations):
    """Process multiple .blend files with MCP operations."""

    blender = BlenderClient()
    await blender.connect()

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    blend_files = list(input_path.glob("*.blend"))

    for blend_file in blend_files:
        print(f"Processing {blend_file.name}")

        # Load scene
        await blender.load_scene(str(blend_file))

        # Apply operations
        for operation in operations:
            if operation["type"] == "optimize":
                await optimize_scene(blender, operation["settings"])
            elif operation["type"] == "render":
                await render_scene(blender, operation["settings"])
            elif operation["type"] == "export":
                await export_scene(blender, operation["settings"])

        # Save processed scene
        output_file = output_path / f"processed_{blend_file.name}"
        await blender.save_scene(str(output_file))

    await blender.disconnect()
```

## Performance Optimization

### Memory Management

```python
# Configure Blender for headless operation
blender_args = [
    "--background",  # Run without UI
    "--python-use-system-env",  # Use system Python
    "--enable-autoexec",  # Allow script execution
    "--factory-startup",  # Don't load user preferences
]

# Memory optimization
await blender.set_preferences({
    "system": {
        "memory_cache_limit": 4096,  # MB
        "undo_memory_limit": 128,    # MB
        "undo_steps": 1
    }
})
```

### GPU Acceleration

```python
# Configure Cycles for GPU rendering
await blender.set_render_engine("CYCLES")

# Detect and configure GPU
gpu_devices = await blender.get_gpu_devices()
if gpu_devices:
    # Use first available GPU
    await blender.set_compute_device_preference("CUDA", gpu_devices[0])
    await blender.set_cycles_device("GPU")
else:
    print("No GPU detected, using CPU")
    await blender.set_cycles_device("CPU")
```

### Scene Optimization

```python
async def optimize_scene(blender_client, scene_settings):
    """Optimize scene for performance."""

    # Reduce subdivision levels
    modifiers = await blender_client.get_modifiers_by_type("SUBSURF")
    for modifier in modifiers:
        await blender_client.set_modifier_property(modifier, "levels", 1)

    # Merge by distance to reduce vertices
    await blender_client.apply_merge_by_distance(merge_distance=0.001)

    # Remove unused materials and textures
    await blender_client.remove_unused_materials()
    await blender_client.remove_unused_textures()

    # Optimize mesh topology
    await blender_client.apply_triangulate()
    await blender_client.apply_limited_dissolve(angle_limit=5.0)
```

## Error Handling

### Connection Issues

```python
async def connect_with_retry(max_retries=3, delay=2.0):
    """Connect to Blender with retry logic."""

    blender = BlenderClient()

    for attempt in range(max_retries):
        try:
            await blender.connect()
            print(f"Connected on attempt {attempt + 1}")
            return blender
        except ConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Connection failed (attempt {attempt + 1}), retrying in {delay}s")
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise RuntimeError(f"Failed to connect after {max_retries} attempts") from e
```

### Operation Timeouts

```python
async def execute_with_timeout(operation, timeout=300):
    """Execute operation with timeout protection."""

    try:
        result = await asyncio.wait_for(operation, timeout=timeout)
        return result
    except asyncio.TimeoutError:
        # Cancel operation if possible
        if hasattr(operation, 'cancel'):
            operation.cancel()

        # Clean up Blender state
        await blender.cleanup_temp_data()

        raise RuntimeError(f"Operation timed out after {timeout} seconds")
```

## Monitoring and Logging

### Performance Monitoring

```python
class BlenderPerformanceMonitor:
    def __init__(self, blender_client):
        self.client = blender_client
        self.metrics = {}

    async def start_monitoring(self):
        """Start performance monitoring."""
        self.start_time = time.time()
        self.initial_memory = await self.client.get_memory_usage()

    async def stop_monitoring(self, operation_name):
        """Stop monitoring and log metrics."""

        end_time = time.time()
        final_memory = await self.client.get_memory_usage()

        metrics = {
            "operation": operation_name,
            "duration": end_time - self.start_time,
            "memory_used": final_memory - self.initial_memory,
            "peak_memory": await self.client.get_peak_memory(),
            "timestamp": datetime.utcnow().isoformat()
        }

        # Log metrics
        logger.info("Blender operation completed", **metrics)

        return metrics
```

### Debug Logging

```python
# Enable verbose Blender logging
await blender.set_debug_mode(True)

# Log Blender console output
blender.set_console_callback(lambda msg: logger.debug(f"Blender: {msg}"))

# Capture render progress
await blender.render_with_progress_callback(
    output_path="/output/render.png",
    progress_callback=lambda frame, total: logger.info(f"Rendering {frame}/{total}")
)
```

## Security Considerations

### Script Execution

```python
# Validate scripts before execution
def validate_blender_script(script_path):
    """Validate Blender script for security."""

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for dangerous operations
    dangerous_patterns = [
        r'import\s+os\b',
        r'import\s+subprocess\b',
        r'import\s+sys\b',
        r'exec\s*\(',
        r'eval\s*\(',
        r'__import__\s*\('
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, content):
            raise SecurityError(f"Dangerous pattern found in script: {pattern}")

    return True
```

### File Access Control

```python
# Restrict file access to allowed directories
ALLOWED_DIRECTORIES = ["/allowed/input", "/allowed/output", "/tmp"]

def validate_file_path(file_path):
    """Validate file path for security."""

    resolved_path = Path(file_path).resolve()

    # Check if path is within allowed directories
    allowed = any(str(resolved_path).startswith(allowed_dir)
                 for allowed_dir in ALLOWED_DIRECTORIES)

    if not allowed:
        raise SecurityError(f"Access denied to path: {file_path}")

    return resolved_path
```

## Version Compatibility

### Blender Version Matrix

| Feature | 3.6 LTS | 4.0 | 4.1 | 4.2 |
|---------|---------|-----|-----|-----|
| Geometry Nodes | Basic | Enhanced | Advanced | Latest |
| Cycles X | No | Yes | Yes | Optimized |
| Python API | 3.10 | 3.11 | 3.11 | 3.11 |
| USD Support | Basic | Enhanced | Full | Latest |
| Extensions | No | Yes | Yes | Platform |

### MCP Compatibility

- **MCP Protocol**: 2025-11-25 and later
- **FastMCP**: 3.1.1++ recommended
- **Python**: 3.10+ required
- **Async Support**: Required for real-time operations

## Migration Guide

### Upgrading from Blender 3.x to 4.x

```python
# Update material system
async def migrate_materials(blender_client):
    """Migrate materials from Blender 3.x to 4.x."""

    materials = await blender_client.get_all_materials()

    for material in materials:
        # Convert legacy nodes to new system
        if await blender_client.is_legacy_material(material):
            await blender_client.convert_to_bsdf(material)

        # Update Principled BSDF inputs
        await blender_client.update_bsdf_inputs(material)
```

### API Changes

```python
# Blender 3.x â†’ 4.x API changes
API_CHANGES = {
    # Object creation
    "bpy.ops.mesh.primitive_cube_add": "blender.create_object('cube')",

    # Material system
    "material.node_tree": "material.get_node_tree()",

    # Render settings
    "bpy.context.scene.render.engine": "blender.get_render_engine()",

    # Modifier access
    "obj.modifiers['Subsurf']": "blender.get_modifier(obj, 'SUBSURF')"
}
```

## Best Practices Summary

### Performance
- Use GPU acceleration when available
- Optimize scenes before complex operations
- Batch similar operations together
- Monitor memory usage

### Reliability
- Implement proper error handling
- Use timeouts for long operations
- Validate inputs and outputs
- Log operations for debugging

### Security
- Validate all file paths
- Sanitize script inputs
- Use isolated Blender instances
- Monitor resource usage

### Maintainability
- Use descriptive names for objects/materials
- Organize scenes with collections
- Document custom scripts and addons
- Version control blend files

---

*Integration Guide Version: 2.0*
*Blender Version: 4.2.x*
*MCP Protocol: 2024-11-05*
*Last updated: January 2026*

