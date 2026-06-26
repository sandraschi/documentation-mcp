# Mayo CAD Converter Integration

## Overview

Mayo is an open-source CAD file converter that enables MCP servers to convert CAD files (STEP, IGES, BREP) to mesh formats compatible with 3D modeling applications like Blender.

**Homepage**: https://github.com/fougue/mayo
**Latest Version**: 0.9.0 (January 2025)
**License**: BSD 2-Clause

## Integration with MCP Ecosystem

Mayo is integrated into the robotics-mcp and blender-mcp servers to provide seamless CAD conversion capabilities:

- **robotics-mcp**: `cad_converter` tool provides Mayo integration
- **blender-mcp**: Enhanced `blender_import` tool supports direct CAD import via Mayo

## Supported Formats

### Input Formats
- **STEP** (.step, .stp) - ISO 10303-21 standard
- **IGES** (.iges, .igs) - Initial Graphics Exchange Specification
- **BREP** (.brep) - Boundary Representation

### Output Formats
- **OBJ** (.obj) - Wavefront OBJ (recommended for Blender)
- **STL** (.stl) - Stereolithography (good for 3D printing)
- **PLY** (.ply) - Polygon File Format

## Installation

### Windows
1. Download `Mayo-0.9.0-win64-binaries.zip` or `Mayo-0.9.0-win64-installer.exe`
2. Extract/install to a directory (e.g., `C:\Program Files\Mayo\`)
3. Ensure `mayo-conv.exe` is in PATH or note its location

### Linux/macOS
1. Download appropriate AppImage (`.AppImage`) or compile from source
2. Make executable: `chmod +x MayoConv-*-x86_64.AppImage`
3. Place in PATH or note location

## Usage in MCP Tools

### Basic Conversion

```python
# Using robotics-mcp cad_converter tool
result = await cad_converter(
    operation="convert_cad",
    cad_path="C:/models/robot_part.step",
    output_format="obj",
    mesh_quality="high"
)
```

### Blender Direct Import

```python
# Using blender-mcp import tool
result = await blender_import(
    operation="import_cad",
    filepath="C:/models/robot_part.step",
    cad_conversion_tool="mayo",
    mesh_quality="high"
)
```

## Command Line Usage

Mayo can be used directly from command line:

```bash
# Basic conversion
mayo-conv input.step -o output.obj

# High quality mesh
mayo-conv input.step -o output.obj --meshing-edge-length 0.1

# Scale adjustment
mayo-conv input.step -o output.obj --scale 0.001

# Multiple options
mayo-conv input.step -o output.obj --meshing-edge-length 0.5 --scale 1000
```

## Mesh Quality Settings

Control mesh quality with `--meshing-edge-length` parameter:

- **Low quality**: `--meshing-edge-length 1.0` (faster, fewer polygons)
- **Medium quality**: `--meshing-edge-length 0.5` (balanced)
- **High quality**: `--meshing-edge-length 0.1` (slower, more polygons)

## Scale Considerations

CAD files often use millimeters while Blender uses meters:

- **From CAD to Blender**: Use `--scale 0.001` (mm to meters)
- **From Blender to CAD**: Use `--scale 1000` (meters to mm)

## Integration Examples

### Robotics Workflow

```python
# 1. Convert STEP to OBJ
await cad_converter(
    operation="convert_cad",
    cad_path="scout_wheel.step",
    output_format="obj",
    mesh_quality="high",
    scale_factor=0.001  # mm to meters
)

# 2. Import to Blender
await blender_import(
    operation="import_obj",
    filepath="scout_wheel.obj"
)

# 3. Create robot model
await robot_model_tools(
    operation="create_robot",
    robot_type="scout",
    model_files=["scout_body.obj", "scout_wheel_left.obj", "scout_wheel_right.obj"]
)
```

### Batch Conversion

```python
# Convert multiple CAD files
await cad_converter(
    operation="batch_convert_cad",
    input_path="C:/cad_models/",
    output_format="obj",
    mesh_quality="medium"
)
```

## Troubleshooting

### Common Issues

1. **"mayo-conv not found"**
   - Ensure Mayo is installed and in PATH
   - Or specify full path to mayo-conv.exe

2. **Poor mesh quality**
   - Try lower `--meshing-edge-length` value
   - Or use different output format

3. **Scale issues**
   - Check unit system (CAD often uses mm, Blender uses meters)
   - Apply appropriate scale factor

4. **Timeout errors**
   - Complex models may take time to convert
   - Increase timeout in MCP tool calls

### Performance Tips

- **Use appropriate mesh quality**: High quality only when needed
- **Batch convert**: Process multiple files together
- **Cache conversions**: Reuse converted files when possible
- **Parallel processing**: Convert independent parts simultaneously

## Technical Details

### Architecture

Mayo uses OpenCASCADE technology for robust CAD geometry processing:

- **OpenCASCADE**: Industry-standard CAD kernel
- **Mesh generation**: Adaptive triangulation algorithms
- **Format support**: Comprehensive CAD format coverage
- **Cross-platform**: Windows, Linux, macOS support

### File Size Handling

- **Small files**: < 10MB - instant conversion
- **Medium files**: 10-100MB - seconds to minutes
- **Large files**: > 100MB - may require optimization

### Memory Usage

- **Base memory**: ~50MB for simple conversions
- **Complex models**: 200-500MB depending on geometry
- **Batch processing**: Memory scales with concurrent conversions

## Related MCP Servers

- **robotics-mcp**: Primary CAD conversion interface
- **blender-mcp**: Direct CAD import capabilities
- **advanced-memory-mcp**: Knowledge graph integration for CAD models

## Version Compatibility

- **MCP Protocol**: 2024-11-05 and later
- **FastMCP**: 3.1.1++ recommended
- **Blender**: 4.0+ for enhanced import tools
- **Python**: 3.8+ required

## Development Notes

Mayo integration follows these design principles:

1. **Non-intrusive**: Works as external tool, no compilation required
2. **Reliable**: Industry-standard OpenCASCADE backend
3. **Flexible**: Multiple output formats and quality settings
4. **Scalable**: Handles files from KB to GB in size

## Future Enhancements

Planned improvements:

- **Direct API integration**: Eliminate subprocess calls
- **Material preservation**: Maintain colors/textures from CAD
- **Assembly support**: Preserve hierarchical structure
- **Cloud processing**: Handle very large files remotely

---

*Last updated: January 2026*
*Mayo version: 0.9.0*

