# Blender MCP API Reference

## Core Classes

### BlenderClient

Main client class for interacting with Blender MCP server.

```python
from blender_mcp import BlenderClient

client = BlenderClient(host="localhost", port=8765)
await client.connect()
```

#### Connection Methods

**connect()** → `bool`
- Establishes connection to Blender MCP server
- Returns: True if successful

**disconnect()** → `None`
- Closes connection to server

**is_connected()** → `bool`
- Returns: True if connected

#### Scene Management

**create_scene(name: str)** → `Scene`
- Creates new scene
- Parameters: `name` - Scene name
- Returns: Scene object

**load_scene(filepath: str)** → `Scene`
- Loads .blend file
- Parameters: `filepath` - Path to .blend file
- Returns: Active scene

**save_scene(filepath: str)** → `bool`
- Saves current scene
- Parameters: `filepath` - Save path
- Returns: True if successful

**get_active_scene()** → `Scene`
- Returns: Currently active scene

#### Object Management

**create_object(type: str, name: str = None, **kwargs)** → `Object`
- Creates new object
- Parameters:
  - `type`: "cube", "sphere", "plane", "cylinder", etc.
  - `name`: Optional object name
  - `location`: (x, y, z) tuple
  - `rotation`: (x, y, z) degrees tuple
  - `scale`: (x, y, z) tuple
- Returns: Created object

**delete_object(obj: Object)** → `bool`
- Deletes object from scene
- Parameters: `obj` - Object to delete
- Returns: True if successful

**duplicate_object(obj: Object, linked: bool = False)** → `Object`
- Duplicates object
- Parameters:
  - `obj` - Object to duplicate
  - `linked` - Create linked duplicate
- Returns: New object

**get_object(name: str)** → `Object`
- Gets object by name
- Parameters: `name` - Object name
- Returns: Object or None

**get_all_objects()** → `List[Object]`
- Returns: List of all objects in scene

#### Transformations

**set_location(obj: Object, location: tuple)** → `bool`
- Sets object location
- Parameters:
  - `obj` - Target object
  - `location` - (x, y, z) coordinates

**set_rotation(obj: Object, rotation: tuple)** → `bool`
- Sets object rotation (degrees)
- Parameters:
  - `obj` - Target object
  - `rotation` - (x, y, z) rotation

**set_scale(obj: Object, scale: tuple)** → `bool`
- Sets object scale
- Parameters:
  - `obj` - Target object
  - `scale` - (x, y, z) scale factors

**translate(obj: Object, vector: tuple)** → `bool`
- Translates object relatively
- Parameters:
  - `obj` - Target object
  - `vector` - (dx, dy, dz) translation

**rotate(obj: Object, angles: tuple)** → `bool`
- Rotates object relatively (degrees)
- Parameters:
  - `obj` - Target object
  - `angles` - (rx, ry, rz) rotation

#### Materials and Textures

**create_material(name: str, material_type: str = "principled")** → `Material`
- Creates new material
- Parameters:
  - `name` - Material name
  - `material_type` - "principled", "emission", "glass", etc.
- Returns: Material object

**assign_material(obj: Object, material: Material)** → `bool`
- Assigns material to object

**create_texture(name: str, filepath: str)** → `Texture`
- Creates texture from image file
- Parameters:
  - `name` - Texture name
  - `filepath` - Image file path
- Returns: Texture object

**assign_texture(material: Material, texture: Texture, target: str)** → `bool`
- Assigns texture to material property
- Parameters:
  - `material` - Target material
  - `texture` - Texture to assign
  - `target` - Property name ("base_color", "normal", "roughness", etc.)

#### Mesh Operations

**create_mesh_object(name: str, vertices: list, faces: list)** → `Object`
- Creates object from vertex/face data
- Parameters:
  - `name` - Object name
  - `vertices` - List of (x,y,z) tuples
  - `faces` - List of vertex index tuples
- Returns: Mesh object

**apply_modifier(obj: Object, modifier_type: str, **params)** → `bool`
- Applies modifier to object
- Parameters:
  - `obj` - Target object
  - `modifier_type` - "SUBSURF", "MIRROR", "ARRAY", etc.
  - `**params` - Modifier-specific parameters

**remove_modifier(obj: Object, modifier_name: str)** → `bool`
- Removes modifier from object

**subdivide_mesh(obj: Object, cuts: int = 1)** → `bool`
- Subdivides mesh
- Parameters: `cuts` - Number of cuts per edge

**merge_vertices(obj: Object, distance: float)** → `bool`
- Merges nearby vertices
- Parameters: `distance` - Merge threshold

#### Animation

**set_frame_current(frame: int)** → `bool`
- Sets current frame
- Parameters: `frame` - Frame number

**insert_keyframe(obj: Object, property: str, frame: int = None)** → `bool`
- Inserts keyframe for object property
- Parameters:
  - `obj` - Target object
  - `property` - Property name ("location", "rotation", "scale")
  - `frame` - Frame number (current frame if None)

**set_fcurve_interpolation(obj: Object, property: str, interpolation: str)** → `bool`
- Sets keyframe interpolation type
- Parameters:
  - `interpolation` - "CONSTANT", "LINEAR", "BEZIER", "SINE", etc.

**create_action(name: str)** → `Action`
- Creates new animation action
- Parameters: `name` - Action name
- Returns: Action object

#### Rendering

**set_render_engine(engine: str)** → `bool`
- Sets render engine
- Parameters: `engine` - "BLENDER_EEVEE", "CYCLES", "WORKBENCH"

**set_render_resolution(width: int, height: int)** → `bool`
- Sets render resolution

**set_render_samples(samples: int)** → `bool`
- Sets render samples (for Cycles)

**render_frame(filepath: str, frame: int = None)** → `bool`
- Renders single frame
- Parameters:
  - `filepath` - Output file path
  - `frame` - Frame to render (current if None)

**render_animation(filepath: str, start_frame: int, end_frame: int)** → `bool`
- Renders animation sequence

#### Camera Operations

**create_camera(name: str, **kwargs)** → `Object`
- Creates camera object
- Parameters:
  - `name` - Camera name
  - `location` - Camera position
  - `rotation` - Camera rotation
  - `lens` - Focal length (mm)
  - `sensor_width` - Sensor width (mm)

**set_active_camera(camera: Object)** → `bool`
- Sets active camera

**point_camera_at(camera: Object, target: Object)** → `bool`
- Points camera at target object

**set_camera_lens(camera: Object, focal_length: float)** → `bool`
- Sets camera focal length

#### Lighting

**create_light(name: str, type: str, **kwargs)** → `Object`
- Creates light object
- Parameters:
  - `name` - Light name
  - `type` - "POINT", "SUN", "SPOT", "AREA"
  - `location` - Light position
  - `rotation` - Light rotation
  - `energy` - Light intensity
  - `color` - Light color (r,g,b)

**set_light_energy(light: Object, energy: float)** → `bool`
- Sets light energy/intensity

**set_light_color(light: Object, color: tuple)** → `bool`
- Sets light color (r,g,b)

#### Collections

**create_collection(name: str)** → `Collection`
- Creates new collection
- Parameters: `name` - Collection name
- Returns: Collection object

**move_to_collection(obj: Object, collection: Collection)** → `bool`
- Moves object to collection

**set_collection_visible(collection: Collection, visible: bool)** → `bool`
- Sets collection visibility

#### Import/Export

**import_obj(filepath: str)** → `Object`
- Imports OBJ file
- Returns: Imported object

**import_fbx(filepath: str)** → `Object`
- Imports FBX file
- Returns: Imported object

**import_stl(filepath: str)** → `Object`
- Imports STL file
- Returns: Imported object

**export_obj(objects: list, filepath: str)** → `bool`
- Exports objects as OBJ

**export_fbx(objects: list, filepath: str)** → `bool`
- Exports objects as FBX

**export_stl(objects: list, filepath: str)** → `bool`
- Exports objects as STL

#### Geometry Nodes

**create_geometry_nodes_modifier(obj: Object, name: str)** → `NodeGroup`
- Creates geometry nodes modifier
- Returns: Node group

**add_geo_node(group: NodeGroup, node_type: str)** → `Node`
- Adds node to geometry node group
- Parameters: `node_type` - Blender node type name
- Returns: Node object

**connect_geo_nodes(from_node: Node, from_socket: str, to_node: Node, to_socket: str)** → `bool`
- Connects geometry node sockets

**set_node_property(node: Node, property: str, value)** → `bool`
- Sets node property value

#### UV Mapping

**add_uv_unwrap(obj: Object, method: str = "SMART")** → `bool`
- Adds UV unwrapping to object
- Parameters: `method` - "SMART", "ANGLE_BASED", "CONFORMAL"

**generate_lightmap_uv(obj: Object)** → `bool`
- Generates lightmap UV layout

**pack_uv_islands(obj: Object, margin: float = 0.02)** → `bool`
- Packs UV islands with margin

#### Physics Simulation

**add_rigid_body(obj: Object, **params)** → `bool`
- Adds rigid body physics
- Parameters:
  - `mass` - Object mass
  - `friction` - Friction coefficient
  - `restitution` - Bounciness

**add_soft_body(obj: Object, **params)** → `bool`
- Adds soft body physics
- Parameters:
  - `goal_strength` - Shape preservation
  - `damping` - Motion damping

**add_cloth_simulation(obj: Object, **params)** → `bool`
- Adds cloth physics
- Parameters:
  - `stiffness` - Cloth stiffness
  - `damping` - Motion damping

#### Particle Systems

**create_particle_system(obj: Object, name: str)** → `ParticleSystem`
- Creates particle system on object
- Returns: Particle system object

**set_particle_settings(system: ParticleSystem, **params)** → `bool`
- Configures particle system
- Parameters:
  - `count` - Number of particles
  - `lifetime` - Particle lifetime
  - `emit_from` - Emission source ("VERT", "FACE", "VOLUME")
  - `physics_type` - Physics mode ("NO", "NEWTON", "FLUID")

## Advanced Classes

### Scene

Scene management class.

**get_objects()** → `List[Object]`
- Returns: All objects in scene

**get_collections()** → `List[Collection]`
- Returns: All collections in scene

**set_active_collection(collection: Collection)** → `bool`
- Sets active collection

**get_render_settings()** → `dict`
- Returns: Current render settings

**set_render_settings(settings: dict)** → `bool`
- Updates render settings

### Object

3D object representation.

**get_location()** → `tuple`
- Returns: (x, y, z) location

**get_rotation()** → `tuple`
- Returns: (rx, ry, rz) rotation in degrees

**get_scale()** → `tuple`
- Returns: (sx, sy, sz) scale

**get_mesh()** → `Mesh`
- Returns: Object's mesh data

**get_materials()** → `List[Material]`
- Returns: Assigned materials

**get_modifiers()** → `List[Modifier]`
- Returns: Applied modifiers

### Material

Material representation.

**get_type()** → `str`
- Returns: Material type ("principled", "emission", etc.)

**get_node_tree()** → `NodeTree`
- Returns: Material node tree

**set_base_color(color: tuple)** → `bool`
- Sets base color (r, g, b, a)

**set_metallic(value: float)** → `bool`
- Sets metallic value (0.0-1.0)

**set_roughness(value: float)** → `bool`
- Sets roughness value (0.0-1.0)

**set_emission_color(color: tuple)** → `bool`
- Sets emission color

**set_emission_strength(strength: float)** → `bool`
- Sets emission strength

### Mesh

Mesh data structure.

**get_vertices()** → `List[tuple]`
- Returns: List of (x,y,z) vertex coordinates

**get_edges()** → `List[tuple]`
- Returns: List of (v1,v2) edge vertex indices

**get_faces()** → `List[tuple]`
- Returns: List of face vertex indices

**get_uv_layers()** → `List[UVLayer]`
- Returns: UV layer data

**get_vertex_groups()** → `List[VertexGroup]`
- Returns: Vertex group data

**calculate_normals()** → `bool`
- Recalculates mesh normals

**validate_mesh()** → `dict`
- Returns: Mesh validation results (manifold, holes, etc.)

## Error Classes

### BlenderConnectionError
Raised when connection to Blender fails.

```python
try:
    await client.connect()
except BlenderConnectionError as e:
    print(f"Connection failed: {e}")
```

### BlenderOperationError
Raised when Blender operation fails.

```python
try:
    await client.create_object("invalid_type")
except BlenderOperationError as e:
    print(f"Operation failed: {e}")
```

### BlenderTimeoutError
Raised when operation times out.

```python
try:
    await client.render_animation("long_scene.mp4", 1, 1000)
except BlenderTimeoutError as e:
    print(f"Operation timed out: {e}")
```

## Constants

### Object Types

```python
OBJECT_TYPES = [
    "MESH", "CURVE", "SURFACE", "META", "FONT", "ARMATURE",
    "LATTICE", "EMPTY", "GPENCIL", "CAMERA", "LIGHT", "SPEAKER",
    "LIGHT_PROBE", "VOLUME"
]
```

### Primitive Types

```python
PRIMITIVE_TYPES = [
    "cube", "sphere", "cylinder", "cone", "torus", "plane",
    "circle", "grid", "monkey", "uv_sphere", "ico_sphere"
]
```

### Render Engines

```python
RENDER_ENGINES = [
    "BLENDER_EEVEE", "CYCLES", "BLENDER_WORKBENCH"
]
```

### Interpolation Types

```python
INTERPOLATION_TYPES = [
    "CONSTANT", "LINEAR", "BEZIER", "SINE", "QUAD", "CUBIC",
    "QUART", "QUINT", "EXPO", "CIRC", "BACK", "BOUNCE", "ELASTIC"
]
```

### Material Types

```python
MATERIAL_TYPES = [
    "principled", "emission", "glass", "transparent",
    "diffuse", "glossy", "refraction", "subsurface"
]
```

## Performance Metrics

### get_memory_usage() → `int`
- Returns: Current memory usage in MB

### get_peak_memory() → `int`
- Returns: Peak memory usage in MB

### get_render_time() → `float`
- Returns: Last render time in seconds

### get_frame_rate() → `float`
- Returns: Current viewport frame rate

## Utility Functions

### get_blender_info() → `dict`
Returns Blender version and system information.

```python
info = await client.get_blender_info()
# {
#   "version": "4.2.0",
#   "build_date": "2024-12-01",
#   "platform": "Linux",
#   "python_version": "3.11.5",
#   "gpu_devices": ["NVIDIA RTX 4070"]
# }
```

### validate_scene() → `dict`
Validates scene for common issues.

```python
issues = await client.validate_scene()
# {
#   "orphaned_objects": 2,
#   "missing_materials": 1,
#   "invalid_meshes": 0,
#   "performance_warnings": ["High poly count on object 'terrain'"]
# }
```

### cleanup_temp_data() → `bool`
Cleans up temporary Blender data.

### export_scene_data(format: str) → `dict`
Exports scene data in various formats.

---

*API Version: 2.0*
*Blender Version: 4.2.x*
*Last updated: January 2026*
