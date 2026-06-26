# Mayo CAD Converter Integration Guide

## Overview

Mayo is an open-source CAD file converter that enables MCP servers to convert CAD files (STEP, IGES, BREP) to mesh formats compatible with 3D modeling applications like Blender, Unity, and robotics simulation environments.

**Homepage**: https://github.com/fougue/mayo
**Latest Version**: 0.9.0 (January 2025)
**License**: BSD 2-Clause
**Architecture**: OpenCASCADE-based geometry processing

## MCP Ecosystem Integration

Mayo is integrated into multiple MCP servers to provide seamless CAD conversion capabilities:

- **robotics-mcp**: `cad_converter` and `robot_model_tools` provide Mayo integration for robotics workflows
- **blender-mcp**: Enhanced `blender_import` tool supports direct CAD import via Mayo
- **unity3d-mcp**: CAD conversion support for Unity game development pipelines
- **advanced-memory-mcp**: Knowledge graph integration for CAD model metadata and relationships

## Supported File Formats

### Input Formats (CAD)
- **STEP** (.step, .stp) - ISO 10303-21 standard, most common CAD exchange format
- **IGES** (.iges, .igs) - Initial Graphics Exchange Specification
- **BREP** (.brep) - OpenCASCADE Boundary Representation format

### Output Formats (Mesh)
- **OBJ** (.obj) - Wavefront OBJ (recommended for Blender and Unity)
- **STL** (.stl) - Stereolithography (optimal for 3D printing and robotics simulation)
- **PLY** (.ply) - Polygon File Format (good for point cloud data)

## Installation & Setup

### Windows Installation

1. **Download**: Get `Mayo-0.9.0-win64-binaries.zip` from [GitHub Releases](https://github.com/fougue/mayo/releases)
2. **Extract**: Extract to `C:\Program Files\Fougue\Mayo\` (or preferred location)
3. **PATH Setup**: Add the installation directory to system PATH:
   ```powershell
   # Add to system PATH (run as Administrator)
   $mayoPath = "C:\Program Files\Fougue\Mayo"
   [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$mayoPath", "Machine")
   ```
4. **Verify**: Test installation with `mayo-conv --version`

### Linux/macOS Installation

1. **Download**: Get appropriate AppImage (`.AppImage`) from GitHub releases
2. **Make Executable**: `chmod +x MayoConv-*-x86_64.AppImage`
3. **PATH Setup**: Move to `/usr/local/bin/` or add to PATH
4. **Verify**: Test with `./MayoConv-*-x86_64.AppImage --version`

### Docker Integration

For containerized MCP deployments:

```dockerfile
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Download and extract Mayo
ADD https://github.com/fougue/mayo/releases/download/v0.9.0/Mayo-0.9.0-win64-binaries.zip /temp/
RUN Expand-Archive /temp/Mayo-0.9.0-win64-binaries.zip -DestinationPath C:\Mayo

# Add to PATH
ENV PATH="C:\Mayo;%PATH%"
```

## Configuration

### Environment Variables

```bash
# Mayo installation path (if not in PATH)
MAYO_PATH=/usr/local/bin/mayo-conv

# Default mesh quality settings
MAYO_DEFAULT_EDGE_LENGTH=0.1

# Scale factor for unit conversion
MAYO_SCALE_FACTOR=0.001  # mm to meters
```

### Quality Settings

Control mesh quality with `--meshing-edge-length` parameter:

- **Low Quality** (`--meshing-edge-length 1.0`): Faster conversion, fewer polygons (~10k triangles)
- **Medium Quality** (`--meshing-edge-length 0.5`): Balanced performance (~50k triangles)
- **High Quality** (`--meshing-edge-length 0.1`): Slower but detailed (~500k triangles)
- **Ultra Quality** (`--meshing-edge-length 0.01`): Maximum detail (~5M triangles)

## MCP Tool Integration

### Robotics MCP Integration

#### CAD Converter Tool

```python
from robotics_mcp.tools.cad_converter import convert_cad

# Basic conversion
result = await convert_cad(
    operation="convert_cad",
    cad_path="/models/robot_arm.step",
    output_format="obj",
    mesh_quality="high",
    scale_factor=0.001  # mm to meters
)

# Batch conversion
results = await convert_cad(
    operation="batch_convert_cad",
    input_directory="/cad_models/",
    output_format="stl",
    mesh_quality="medium"
)
```

#### Robot Model Tools Integration

```python
from robotics_mcp.tools.robot_model_tools import create_robot_model

# Create robot from CAD assembly
robot_model = await create_robot_model(
    operation="create_from_cad",
    cad_files=[
        "base.step",
        "arm.step",
        "gripper.step"
    ],
    output_format="urdf",
    cad_converter="mayo"
)
```

### Blender MCP Integration

#### Direct CAD Import

```python
from blender_mcp.tools.import_tools import import_cad

# Import CAD file directly
result = await import_cad(
    filepath="/models/assembly.step",
    cad_converter="mayo",
    mesh_quality="high",
    scale_factor=0.001
)

# Import with material preservation
result = await import_cad(
    filepath="/models/part.step",
    cad_converter="mayo",
    preserve_materials=True,
    import_textures=True
)
```

### Unity3D MCP Integration

```python
from unity3d_mcp.tools.import_tools import import_cad_unity

# Import for Unity pipeline
result = await import_cad_unity(
    cad_path="/models/asset.step",
    output_format="obj",
    unity_scale_factor=1.0,  # Unity units
    generate_lod=True
)
```

## Command Line Usage

### Basic Conversion

```bash
# Convert single file
mayo-conv input.step -o output.obj

# High quality mesh
mayo-conv input.step -o output.obj --meshing-edge-length 0.1

# Scale adjustment (CAD mm to Blender meters)
mayo-conv input.step -o output.obj --scale 0.001

# Multiple options
mayo-conv input.step -o output.obj --meshing-edge-length 0.5 --scale 1000
```

### Batch Processing

```bash
# Convert all STEP files in directory
for file in *.step; do
    mayo-conv "$file" -o "${file%.step}.obj"
done

# Using find for recursive conversion
find . -name "*.step" -exec mayo-conv {} -o {}.obj \;
```

## Workflow Examples

### Robotics Development Pipeline

1. **CAD Design**: Create robot parts in CAD software (SolidWorks, Fusion 360, etc.)
2. **Export**: Export assembly as STEP files
3. **Convert**: Use Mayo to convert to mesh formats
4. **Import**: Load into simulation environment (Gazebo, Webots, etc.)
5. **Configure**: Set up joint constraints and physics properties

```python
# Complete robotics workflow
async def setup_robot_from_cad(cad_files, robot_config):
    # Convert CAD files
    converted_files = await convert_cad_batch(cad_files, format="stl")

    # Create URDF robot description
    urdf = await generate_urdf(converted_files, robot_config)

    # Import to simulation
    robot_model = await import_to_simulation(urdf)

    return robot_model
```

### Game Development Pipeline

1. **CAD Design**: Model game assets in CAD
2. **Convert**: Use Mayo for LOD generation
3. **Import**: Load into Unity/Unreal Engine
4. **Optimize**: Apply LOD settings and materials
5. **Integrate**: Add to game scene with physics

```python
# Unity asset pipeline
async def prepare_asset_for_unity(cad_path, lod_levels):
    results = []

    for i, quality in enumerate(lod_levels):
        output_path = f"{cad_path.stem}_LOD{i}.obj"
        result = await convert_cad_unity(
            cad_path=cad_path,
            output_path=output_path,
            mesh_quality=quality
        )
        results.append(result)

    return results
```

## Performance Optimization

### Memory Management

- **Large Files**: Files >100MB may require chunked processing
- **Batch Processing**: Process multiple small files together
- **Temporary Files**: Clean up intermediate conversions
- **Memory Limits**: Monitor RAM usage for complex geometries

### Quality vs Performance Trade-offs

| Quality Setting | Triangles | Conversion Time | Use Case |
|----------------|-----------|----------------|----------|
| Low (1.0) | ~10K | < 1 second | Prototyping, rough models |
| Medium (0.5) | ~50K | 2-5 seconds | General use, simulation |
| High (0.1) | ~500K | 10-30 seconds | Detailed visualization |
| Ultra (0.01) | ~5M | 1-5 minutes | Maximum detail |

### Caching Strategies

```python
# Implement conversion caching
import hashlib
import os

def get_cache_key(file_path, settings):
    file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    settings_hash = hashlib.md5(str(settings).encode()).hexdigest()
    return f"{file_hash}_{settings_hash}"

def convert_with_cache(cad_path, output_path, settings):
    cache_key = get_cache_key(cad_path, settings)
    cache_path = f"/cache/{cache_key}.obj"

    if os.path.exists(cache_path):
        return cache_path

    # Perform conversion
    result = mayo_convert(cad_path, cache_path, settings)
    return result
```

## Troubleshooting

### Common Issues

#### "mayo-conv not found"
- **Solution**: Verify Mayo is installed and in PATH
- **Check**: `which mayo-conv` (Linux/macOS) or `where mayo-conv` (Windows)
- **Fix**: Add installation directory to PATH

#### Poor Mesh Quality
- **Solution**: Adjust `--meshing-edge-length` parameter
- **Try**: Lower values (0.1, 0.05) for better quality
- **Alternative**: Use different output format

#### Scale Issues
- **Problem**: CAD models appear wrong size in target application
- **Solution**: Apply appropriate scale factor
- **CAD â†’ Blender**: `--scale 0.001` (mm to meters)
- **CAD â†’ Unity**: `--scale 0.01` or adjust in Unity

#### Timeout Errors
- **Cause**: Complex models take time to process
- **Solution**: Increase timeout in MCP tool calls
- **Optimization**: Use lower mesh quality for initial tests

#### Memory Errors
- **Cause**: Large assemblies exceed RAM limits
- **Solution**: Process components separately
- **Alternative**: Split large assemblies into smaller parts

### Debug Commands

```bash
# Check installation
mayo-conv --version

# Test basic conversion
mayo-conv test.step -o test.obj --meshing-edge-length 1.0

# Verbose output (if available)
mayo-conv input.step -o output.obj -v

# Check file format support
mayo-conv --help | grep -A 20 "Supported formats"
```

### Log Analysis

Enable detailed logging in MCP servers:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable Mayo subprocess logging
os.environ['MAYO_DEBUG'] = '1'
```

## API Reference

### Command Line Options

```
Usage: mayo-conv [options] [files...]

Options:
  -?, -h, --help                         Display help
  -v, --version                          Display version
  -u, --use-settings <filepath>          Use settings file (INI format)
  -c, --cache-settings                   Cache settings file
  -o, --output <filepath>                Output file path
  --meshing-edge-length <float>          Mesh quality (default: 0.5)
  --scale <float>                        Scale factor (default: 1.0)
  --format <format>                      Output format (obj, stl, ply)
```

### Python Integration

```python
import subprocess
import os

def convert_cad_file(input_path, output_path, quality=0.5, scale=1.0):
    """Convert CAD file using Mayo CLI."""
    cmd = [
        'mayo-conv',
        input_path,
        '-o', output_path,
        '--meshing-edge-length', str(quality),
        '--scale', str(scale)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Mayo conversion failed: {result.stderr}")

    return output_path
```

## Security Considerations

### Input Validation
- **File Type Checking**: Validate input files are legitimate CAD formats
- **Path Traversal**: Prevent directory traversal attacks in file paths
- **Size Limits**: Implement file size limits to prevent DoS attacks

### Sandboxing
- **Container Execution**: Run Mayo in isolated containers
- **Resource Limits**: Set CPU and memory limits for conversions
- **Temporary Files**: Use secure temporary directories

## Monitoring & Observability

### Metrics to Track
- Conversion success/failure rates
- Average conversion time by file size
- Memory usage during conversions
- Quality setting distribution

### Logging Integration

```python
import structlog

def log_conversion_metrics(input_file, output_file, duration, quality):
    structlog.get_logger().info(
        "cad_conversion_completed",
        input_file=input_file,
        output_file=output_file,
        duration_seconds=duration,
        mesh_quality=quality,
        file_size_mb=os.path.getsize(input_file) / (1024*1024)
    )
```

## Future Enhancements

### Planned Features
- **Direct API Integration**: Eliminate subprocess calls for better performance
- **Material Preservation**: Maintain colors and textures from CAD files
- **Assembly Support**: Preserve hierarchical structure and relationships
- **Cloud Processing**: Handle very large files remotely
- **Real-time Conversion**: Streaming conversion for large datasets

### Integration Roadmap
- **WebAssembly Support**: Browser-based CAD conversion
- **Plugin Architecture**: Extensible conversion pipeline
- **AI-Powered Optimization**: Automatic quality setting recommendations
- **Multi-format Batch**: Convert entire project directories

## Related MCP Servers

### Primary Integrations
- **robotics-mcp**: Core CAD conversion and robot modeling
- **blender-mcp**: 3D modeling and visualization
- **unity3d-mcp**: Game development pipeline integration

### Supporting Servers
- **advanced-memory-mcp**: CAD model knowledge graph
- **filesystem-mcp**: File management and organization
- **database-operations-mcp**: CAD metadata storage

## Version Compatibility

- **MCP Protocol**: 2025-11-25 and later
- **FastMCP**: 3.1.1++ recommended
- **Blender**: 4.0+ for enhanced import tools
- **Unity**: 2020+ for CAD pipeline support
- **Python**: 3.8+ required for MCP integration

## Contributing

### Development Setup
1. Clone Mayo repository: `git clone https://github.com/fougue/mayo`
2. Follow build instructions for your platform
3. Test with sample CAD files
4. Submit pull requests for enhancements

### Testing
- Use provided test CAD files for regression testing
- Validate conversions across all supported formats
- Performance benchmark with various file sizes
- Cross-platform compatibility testing

## License & Attribution

Mayo CAD Converter is licensed under BSD 2-Clause License.
OpenCASCADE technology provides the underlying CAD geometry processing.

---

*Last updated: January 2026*
*Mayo version: 0.9.0*
*MCP integration status: Active*

