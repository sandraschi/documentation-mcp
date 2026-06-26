# 🌍 World Labs Marble in Resonite: Complete Integration Guide

**Master World Labs Marble workflows with Resonite - from photogrammetry capture to interactive VR experiences using Gaussian splats and collider meshes.**

---

## 📸 What is World Labs Marble?

World Labs Marble is an **AI-powered photogrammetry platform** that transforms photos/videos into high-fidelity 3D representations using **Gaussian Splats**.

### Key Features:
- **Input**: Photos/videos from any camera/smartphone
- **Processing**: AI-powered 3D reconstruction
- **Output**: Photorealistic VR-ready scenes
- **Efficiency**: Optimized for real-time VR performance

### Workflow Overview:
1. **Capture** 50-200 overlapping photos of scene
2. **Upload** to Marble for AI processing (10-60 min)
3. **Download** PLY splat + OBJ collision mesh
4. **Import** to Resonite for VR experience
5. **Enhance** with ProtoFlux interactions

---

## 📁 Marble File Formats

### Download Contents:
```
marble_export.zip/
├── splat.ply           # Gaussian Splat data (visual)
├── collision.obj       # Physics collision mesh
├── collision.mtl       # Collision materials
├── thumbnail.jpg       # Preview image
└── metadata.json       # Processing info
```

### Key Formats:

#### PLY (Gaussian Splats)
- **Contains**: Position, color, opacity, scale, rotation per Gaussian
- **Size**: 100MB-2GB typical
- **Purpose**: Photorealistic visual representation

#### OBJ (Collision Mesh)
- **Purpose**: Physics collisions and interactions
- **Optimization**: Simplified geometry for performance
- **Materials**: Basic physics properties

---

## 🛠️ Import to Resonite

### Method 1: Direct Drag & Drop
```bash
1. Extract Marble ZIP download
2. Drag splat.ply into Resonite world
3. Wait for import progress
4. Drag collision.obj for physics
5. Align collision mesh with splat
```

### Method 2: Inventory Import
```bash
1. Press I → Inventory → Import
2. Select splat.ply
3. Configure: quality, distance, LOD
4. Import collision mesh separately
5. Set collision as physics-only (hidden)
```

### Configuration Options:
- **Quality**: High/Medium/Low (performance vs detail)
- **View Distance**: Maximum render distance
- **LOD**: Level of detail reduction
- **Lighting**: Dynamic lighting integration

---

## 🔄 Unity3D Bridging

Unity serves as a powerful **preprocessing and enhancement** bridge:

### Why Use Unity?
- **Preprocessing**: Optimize splats before Resonite
- **Enhancement**: Add interactive elements
- **Prototyping**: Test interactions
- **Conversion**: Transform formats if needed

### Basic Unity Workflow:
```csharp
// 1. Import Marble assets to Unity
// 2. Optimize splats (reduce Gaussians, add LOD)
// 3. Add interactive components
// 4. Export enhanced assets for Resonite
```

### Essential Unity Packages:
- **Gaussian Splatting for Unity**: Core splat rendering
- **PLY Importer**: File format support
- **Resonite Bridge Tools**: Export utilities

---

## ⚡ Performance Optimization

### Resonite Settings:
- **VRAM Budget**: 2-4GB for complex scenes
- **Quality Scaling**: Reduce with distance
- **Culling**: Aggressive frustum culling
- **LOD Levels**: Automatic detail reduction

### File Size Guidelines:
- **Target**: < 500MB for smooth loading
- **Gaussians**: 1-5 million optimal
- **Collision Mesh**: < 10K triangles

---

## 🎨 Creative Applications

### Architectural Visualization:
- **Real Estate**: Walk through captured properties
- **Historical Sites**: Preserve locations virtually
- **Urban Planning**: Preview developments

### Performance Spaces:
- **Concert Venues**: Virtual performances in real spaces
- **Theaters**: Authentic lighting and acoustics
- **Event Spaces**: Plan gatherings realistically

### Artistic Installations:
- **Photorealistic Art**: Gallery-like VR experiences
- **Mixed Reality**: Blend physical and virtual
- **Interactive Narratives**: Story-driven environments

---

## 🤖 MCP Integration

### Import Control:
```bash
# Import Marble splat with options
resonite_import_artifact("splat.ply", {
    "type": "gaussian_splat",
    "quality": "high",
    "collision_mesh": "collision.obj"
})
```

### Runtime Control:
```bash
# Adjust rendering settings
resonite_object_set_property(splat_id, "render_quality", "medium")
resonite_object_set_property(splat_id, "view_distance", 50.0)
```

### ProtoFlux Enhancement:
```bash
# Add interactivity
resonite_protoflux_execute("splat_interaction", {
    "splat_id": splat_id,
    "interaction_type": "proximity_fade",
    "fade_distance": 5.0
})
```

---

## 📋 Best Practices

### Capture Tips:
- **360° Coverage**: Complete scene coverage
- **60-80% Overlap**: Between photos
- **Reference Objects**: Include known-size items for scale
- **Consistent Lighting**: Avoid harsh shadows

### Performance:
- **File Size**: Keep under 500MB
- **Gaussian Count**: 1-5M optimal balance
- **View Distance**: Limit based on scene size
- **Quality Scaling**: Reduce for distant objects

### Integration:
- **Physics First**: Set up collision before visuals
- **Scale Check**: Verify proper sizing
- **Lighting Match**: Blend with world lighting
- **Interaction Zones**: Add ProtoFlux logic

---

## 🔧 Troubleshooting

### Import Issues:
- **Not Loading**: Check PLY file integrity
- **Performance Lag**: Reduce quality/view distance
- **Visual Glitches**: Verify Resonite version compatibility

### Physics Problems:
- **No Collision**: Ensure OBJ mesh is aligned with splat
- **Complex Mesh**: Simplify collision geometry
- **Wrong Materials**: Check physics material settings

### Quality Issues:
- **Blurry**: Increase quality setting or check source
- **Flat Looking**: Enable dynamic lighting
- **Color Wrong**: Check lighting/environment settings

---

## 🚀 Advanced Workflows

### Production Pipeline:
1. **Plan Capture**: Scene requirements, access, equipment
2. **Systematic Capture**: 360° coverage with overlap
3. **Marble Processing**: Upload and wait for AI reconstruction
4. **Unity Enhancement**: Add interactions and optimizations
5. **Resonite Import**: Final integration with ProtoFlux
6. **Performance Testing**: Verify smooth VR experience

### Custom Tools:
- **Marble Preprocessor**: Optimize assets for Resonite
- **Unity Bridge Components**: ProtoFlux translation
- **MCP Automation**: Batch import and configuration

---

**Marble + Resonite = Photorealistic VR experiences made interactive.** 🌍🎮

For technical details, see the full guide in the `resonite-mcp` repository. For ProtoFlux integration, check the [ProtoFlux Guide](./PROTOFLUX_GUIDE.md). For general artifact handling, see the [Artifacts Guide](./ARTIFACTS_GUIDE.md).






