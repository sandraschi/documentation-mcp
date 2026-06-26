# Mayo CAD Converter API Reference

## Command Line Interface

### Basic Usage

```bash
mayo-conv [options] input_file [output_file]
```

### Global Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `-h, --help` | Display help information | - | `mayo-conv --help` |
| `-v, --version` | Display version information | - | `mayo-conv --version` |
| `-o, --output <file>` | Output file path | Auto-generated | `-o model.obj` |
| `--format <fmt>` | Output format (obj, stl, ply) | obj | `--format stl` |

### Mesh Generation Options

| Option | Description | Default | Range | Example |
|--------|-------------|---------|-------|---------|
| `--meshing-edge-length <float>` | Maximum edge length for mesh triangles | 0.5 | 0.01-10.0 | `--meshing-edge-length 0.1` |
| `--meshing-angle <float>` | Maximum angle for mesh adaptation (degrees) | 30.0 | 1.0-90.0 | `--meshing-angle 15.0` |
| `--meshing-deflection <float>` | Maximum deflection for mesh adaptation | 0.1 | 0.001-1.0 | `--meshing-deflection 0.05` |

### Transformation Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--scale <float>` | Scale factor for geometry | 1.0 | `--scale 0.001` |
| `--translate <x,y,z>` | Translation vector | 0,0,0 | `--translate 10,0,0` |
| `--rotate <x,y,z>` | Rotation angles (degrees) | 0,0,0 | `--rotate 0,90,0` |

### Advanced Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--use-settings <file>` | Use INI settings file | - | `--use-settings config.ini` |
| `--cache-settings` | Cache current settings | false | `--cache-settings` |
| `--force` | Overwrite output files | false | `--force` |
| `--verbose` | Enable verbose output | false | `--verbose` |

## Settings File Format (INI)

```ini
[General]
OutputFormat=obj
ScaleFactor=1.0

[Meshing]
EdgeLength=0.5
Angle=30.0
Deflection=0.1
Algorithm=standard

[Transform]
Scale=1.0,1.0,1.0
Translate=0.0,0.0,0.0
Rotate=0.0,0.0,0.0

[Output]
ForceOverwrite=false
Verbose=false
```

## MCP Tool APIs

### Robotics MCP - CAD Converter

#### convert_cad

Converts a single CAD file to mesh format.

**Parameters:**
- `operation`: `"convert_cad"` (string, required)
- `cad_path`: Path to input CAD file (string, required)
- `output_format`: Output format ("obj", "stl", "ply") (string, optional, default: "obj")
- `mesh_quality`: Quality preset ("low", "medium", "high", "ultra") (string, optional, default: "medium")
- `scale_factor`: Scale factor for unit conversion (float, optional, default: 1.0)
- `output_path`: Custom output path (string, optional)

**Returns:**
```json
{
  "success": true,
  "input_file": "/path/to/input.step",
  "output_file": "/path/to/output.obj",
  "conversion_time": 2.5,
  "triangle_count": 15432,
  "file_size_mb": 1.2
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "ConversionFailed",
  "message": "Failed to process CAD file",
  "details": "Invalid STEP file format"
}
```

#### batch_convert_cad

Converts multiple CAD files in batch.

**Parameters:**
- `operation`: `"batch_convert_cad"` (string, required)
- `input_directory`: Directory containing CAD files (string, required)
- `output_format`: Output format ("obj", "stl", "ply") (string, optional, default: "obj")
- `mesh_quality`: Quality preset (string, optional, default: "medium")
- `file_pattern`: Glob pattern for input files (string, optional, default: "*.step")
- `recursive`: Search subdirectories (boolean, optional, default: false)

**Returns:**
```json
{
  "success": true,
  "total_files": 5,
  "converted_files": 4,
  "failed_files": 1,
  "results": [
    {
      "input_file": "part1.step",
      "output_file": "part1.obj",
      "success": true,
      "triangle_count": 12345
    },
    {
      "input_file": "part2.step",
      "output_file": "part2.obj",
      "success": false,
      "error": "File corrupted"
    }
  ]
}
```

### Blender MCP - Import Tools

#### import_cad

Imports CAD file directly into Blender scene.

**Parameters:**
- `operation`: `"import_cad"` (string, required)
- `filepath`: Path to CAD file (string, required)
- `cad_converter`: Converter to use ("mayo") (string, optional, default: "mayo")
- `mesh_quality`: Quality preset (string, optional, default: "medium")
- `scale_factor`: Scale factor (float, optional, default: 0.001)
- `preserve_materials`: Extract materials from CAD (boolean, optional, default: false)
- `import_textures`: Import embedded textures (boolean, optional, default: false)

**Returns:**
```json
{
  "success": true,
  "imported_objects": ["Part1", "Part2"],
  "materials_created": 3,
  "import_time": 5.2,
  "blender_objects": [
    {
      "name": "Part1",
      "vertices": 5432,
      "faces": 10864
    }
  ]
}
```

### Unity3D MCP - Import Tools

#### import_cad_unity

Imports CAD file optimized for Unity pipeline.

**Parameters:**
- `operation`: `"import_cad_unity"` (string, required)
- `cad_path`: Path to CAD file (string, required)
- `output_format`: Output format ("obj", "fbx") (string, optional, default: "obj")
- `unity_scale_factor`: Scale for Unity units (float, optional, default: 1.0)
- `generate_lod`: Create LOD variants (boolean, optional, default: false)
- `optimize_mesh`: Unity mesh optimization (boolean, optional, default: true)

**Returns:**
```json
{
  "success": true,
  "output_files": ["model.obj", "model_LOD1.obj", "model_LOD2.obj"],
  "unity_import_settings": {
    "scale_factor": 1.0,
    "generate_lightmap_uvs": true,
    "optimize_mesh": true
  },
  "lod_levels": 3
}
```

## Error Codes

### Conversion Errors

| Code | Description | Resolution |
|------|-------------|------------|
| `FileNotFound` | Input file does not exist | Verify file path and permissions |
| `UnsupportedFormat` | File format not supported | Check supported formats (STEP, IGES, BREP) |
| `CorruptedFile` | CAD file is corrupted | Validate file with CAD software |
| `GeometryError` | Invalid geometry in file | Repair CAD model or use different file |
| `MemoryError` | Insufficient memory | Reduce mesh quality or split model |
| `TimeoutError` | Conversion took too long | Increase timeout or reduce complexity |

### System Errors

| Code | Description | Resolution |
|------|-------------|------------|
| `ExecutableNotFound` | mayo-conv not in PATH | Add Mayo to system PATH |
| `PermissionDenied` | No write permissions | Check output directory permissions |
| `DiskFull` | Insufficient disk space | Free up disk space |
| `ProcessFailed` | Mayo process crashed | Check Mayo installation and logs |

## Quality Presets

### Predefined Settings

```python
QUALITY_PRESETS = {
    "low": {
        "edge_length": 1.0,
        "angle": 45.0,
        "deflection": 0.5
    },
    "medium": {
        "edge_length": 0.5,
        "angle": 30.0,
        "deflection": 0.1
    },
    "high": {
        "edge_length": 0.1,
        "angle": 15.0,
        "deflection": 0.05
    },
    "ultra": {
        "edge_length": 0.01,
        "angle": 5.0,
        "deflection": 0.01
    }
}
```

### Custom Quality Profiles

```ini
[Quality.HighDetail]
EdgeLength=0.05
Angle=10.0
Deflection=0.02
Algorithm=adaptive

[Quality.QuickPreview]
EdgeLength=2.0
Angle=60.0
Deflection=1.0
Algorithm=fast
```

## Performance Benchmarks

### File Size Performance

| File Size | Low Quality | Medium Quality | High Quality |
|-----------|-------------|----------------|--------------|
| < 1MB | < 1s | 1-2s | 2-5s |
| 1-10MB | 1-3s | 3-10s | 10-30s |
| 10-100MB | 5-15s | 15-60s | 60-300s |
| > 100MB | 30s+ | 2-5min | 10min+ |

### Memory Usage

| Complexity | RAM Usage | Recommended |
|------------|-----------|-------------|
| Simple parts | 50-100MB | Any system |
| Assemblies | 200-500MB | 8GB+ RAM |
| Complex models | 1-4GB | 16GB+ RAM |
| Large assemblies | 4GB+ | 32GB+ RAM |

## File Format Specifications

### STEP (ISO 10303-21)
- **Extensions**: .step, .stp, .p21
- **Versions**: AP203, AP214, AP242
- **Geometry**: BREP-based solids
- **Metadata**: Product structure, materials

### IGES (Initial Graphics Exchange)
- **Extensions**: .iges, .igs
- **Versions**: 5.3, 6.0
- **Geometry**: Wireframe, surface, solid
- **Limitations**: Older format, less robust

### BREP (Boundary Representation)
- **Extensions**: .brep, .rle
- **Format**: OpenCASCADE native
- **Geometry**: Exact boundary representation
- **Advantages**: No approximation errors

---

*API Version: 0.9.0*
*Last updated: January 2026*
