# 🎨 Resonite Artifacts: Import, Export & Creation Guide

**Complete guide to creating, importing, exporting, and controlling 3D artifacts in Resonite - from VRM avatars to Gaussian splats and MCP control.**

---

## 📦 Artifact Types

### 🎭 Avatars
- **VRM Format**: Standard avatar specification (.vrm)
- **Resonite Native**: Optimized internal format
- **Custom Parameters**: Blend shapes, IK, physics

### 🏗️ 3D Models
- **OBJ/FBX**: Traditional mesh formats
- **GLTF/GLB**: Modern web formats
- **PLY**: Point cloud and splat data

### 🎯 Gaussian Splats
- **PLY Splats**: 3D Gaussian representations
- **Collider Meshes**: Physics collision geometry
- **World Labs Marble**: AI-powered scene capture

---

## 📥 Import Procedures

### Three Import Methods:

#### 1. File Drop (Simplest)
```bash
# Drag file into Resonite window
# Wait for processing bar
# Position imported object
```

#### 2. Inventory Import
```bash
# Press I → Inventory
# Click "Import" button
# Browse and select file
# Configure import options
```

#### 3. World Import
```bash
# Press B → Create menu
# Select "Import" section
# Import directly into world
```

### ⚙️ Import Settings
- **Scale**: Auto-detect or manual
- **Materials**: Include/exclude
- **Textures**: Embed or separate
- **Animations**: Import with model

---

## 📤 Export Procedures

### Object Export
```bash
# Select object → Right-click → Export
# Choose format (OBJ, FBX, GLTF)
# Configure options
# Save to file
```

### Batch Export
```bash
# Inventory → Select multiple items
# Export Selected → Choose format
# Batch export to folder
```

---

## 🎭 VRM Avatar Import

### Step-by-Step Process:

1. **Prepare VRM File**
   - Create in VRoid Studio, Blender, or Unity
   - Ensure VRM 1.0 specification
   - Test in VRM viewer first

2. **Import to Resonite**
   ```bash
   # Drag .vrm file into Resonite
   # Wait for processing (complex avatars take time)
   ```

3. **Configure Avatar**
   - **Scale**: Adjust size (1.6-2.0 units recommended)
   - **Eye Tracking**: Enable/disable
   - **Viseme**: Lip sync setup
   - **IK**: Inverse kinematics

4. **Parameter Mapping**
   - Open Avatar menu (ESC → Avatar)
   - Map parameters to blend shapes
   - Test animations in mirror

### 🎯 VRM Features
- **Blend Shapes**: Facial expressions and body morphs
- **IK Rigging**: Natural pose control
- **Physics**: Cloth and hair simulation
- **Custom Parameters**: User-defined controls

---

## 🏗️ 3D Mesh Import

### Supported Formats:
- **OBJ**: Simple geometry + materials
- **FBX**: Complex models with animation
- **GLTF/GLB**: Modern PBR format

### Import Pipeline:
1. **Pre-process** in source software (Blender, Maya, etc.)
2. **Clean geometry** and apply transforms
3. **Set up materials** and UVs
4. **Import to Resonite** and test

### ⚡ Optimization:
- **Triangles**: < 10K (mobile), < 100K (PC)
- **Textures**: 512x512 or 1024x1024
- **Materials**: < 8 per object

---

## 🎯 Gaussian Splat Import

### What are Gaussian Splats?
3D representation technique capturing real-world scenes as Gaussian point clouds - photorealistic and efficient.

### Import Process:

#### Using World Labs Marble:
1. **Upload photos/videos** to Marble service
2. **Wait for processing** (10-60 minutes)
3. **Download files**:
   - `splat.ply` - Gaussian data
   - `collision.obj` - Physics mesh
   - `thumbnail.jpg` - Preview

#### Import to Resonite:
```bash
# Drag .ply file into Resonite
# Import collision mesh separately
# Position and scale splat
# Adjust rendering quality
```

### 🎨 Applications:
- **Real Locations**: Capture and recreate places
- **Architecture**: Show designs in context
- **Art**: Experimental representations
- **Performance**: Interactive stages and venues

---

## 🎮 Controlling Artifacts

### 🔗 ProtoFlux Control
```protoflux
[Button Press] → [Set Position] → [Target Object]
[Sensor Data] → [Animation] → [Feedback]
[OSC Input] → [Parameter Control] → [Avatar Response]
```

### 🎛️ OSC Control
```
/avatar/parameters/Custom/[object_name]/[parameter]
/world/objects/[object_id]/[property]
/audio/[source]/[parameter]
```

### 🤖 MCP Server Control

#### Object Manipulation:
```bash
# Move and transform objects
resonite_object_move(object_id, position, rotation, scale)
resonite_object_set_property(object_id, property_name, value)
resonite_object_animate(object_id, animation_data)
```

#### Avatar Control:
```bash
# Load and control avatars
resonite_avatar_load(avatar_path, slot, parameters)
resonite_parameter_set(parameter_name, value, avatar_slot)
resonite_protoflux_execute("avatar_animation", {"intensity": 0.8})
```

#### Import/Export:
```bash
# Import artifacts programmatically
resonite_import_artifact(file_path, import_options)
resonite_export_artifact(object_id, export_format, options)
```

---

## 🏗️ Creating Artifacts

### In-World Tools:
1. **Primitives**: Basic shapes (cube, sphere, etc.)
2. **Transform**: Move, rotate, scale
3. **Materials**: PBR material editor
4. **Mesh Editor**: Direct geometry manipulation

### Advanced Creation:
- **ProtoFlux Logic**: Add interactive behaviors
- **Material Creation**: Custom shaders and effects
- **Particle Systems**: Dynamic effects
- **Audio Integration**: Spatial sound

---

## 📊 Performance Guidelines

### Geometry Budget:
- **Mobile/Quest**: < 10K triangles per object
- **PC**: < 100K triangles per object
- **World Total**: < 1M visible triangles

### Texture Guidelines:
- **Resolution**: 512x512 for most assets
- **Format**: PNG (transparency), JPG (opaque)
- **Compression**: Enable for performance
- **Mipmaps**: Always enable

### Material Limits:
- **Per Object**: 4-8 materials maximum
- **Shader Complexity**: Balance quality vs performance

---

## 🔧 Troubleshooting

### Import Issues:
- **File not recognized**: Check format compatibility
- **Materials missing**: Ensure textures are accessible
- **Scale problems**: Adjust import scale settings
- **VRM issues**: Verify VRM 1.0 compliance

### Runtime Issues:
- **Performance lag**: Reduce polygon count and textures
- **Control not working**: Check ProtoFlux connections
- **OSC failures**: Verify network and address settings

### Export Issues:
- **Format limitations**: Some features don't export
- **File size**: Optimize geometry and textures
- **Animation loss**: Ensure proper export settings

---

## 🚀 Advanced Techniques

### Procedural Generation:
- **Runtime mesh creation** with ProtoFlux
- **Dynamic material variation**
- **Algorithmic content generation**

### External Integration:
- **Unity live sync** for rapid iteration
- **REST API control** for automation
- **WebSocket communication** for real-time updates

### Multi-User Experiences:
- **State synchronization** across users
- **Collaborative editing** tools
- **Permission systems** for access control

---

## 🎯 Quick Reference

| Asset Type | Import Format | Export Format | Control Method | Performance Target |
|------------|---------------|---------------|----------------|-------------------|
| **Avatars** | VRM | VRM | Parameters/OSC | < 32K triangles |
| **Meshes** | OBJ/FBX/GLTF | OBJ/FBX/GLTF | Transform/ProtoFlux | < 100K triangles |
| **Splatts** | PLY | PLY | Quality/LOD | GPU memory dependent |
| **Audio** | WAV/MP3/OGG | N/A | Spatial/OSC | < 50MB total |
| **Textures** | PNG/JPG | PNG/JPG | Materials | < 4K resolution |

---

**Resonite makes 3D artifact creation and control intuitive through visual programming and powerful import/export capabilities. From VRM avatars to photorealistic Gaussian splats, bring your creations to life in VR!** 🎨🚀

---

*See [ProtoFlux Guide](./PROTOFLUX_GUIDE.md) for programming control details, and [Beginner's Guide](./RESONITE_BEGINNERS_GUIDE.md) for getting started.*






