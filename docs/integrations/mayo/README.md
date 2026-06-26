# Mayo CAD Converter MCP Integration

This directory contains comprehensive documentation for integrating the Mayo open-source CAD converter with MCP (Model Context Protocol) servers.

## Overview

Mayo is an open-source CAD file converter built on OpenCASCADE technology that enables MCP servers to convert CAD files (STEP, IGES, BREP) to mesh formats compatible with 3D modeling applications like Blender, Unity, and robotics simulation environments.

## Documentation Index

### Core Documentation

- **[MAYO_INTEGRATION_GUIDE.md](MAYO_INTEGRATION_GUIDE.md)** - Complete integration guide covering installation, configuration, usage, and workflows
- **[API_REFERENCE.md](API_REFERENCE.md)** - Detailed API reference for command-line options and MCP tool interfaces
- **[BEST_PRACTICES.md](BEST_PRACTICES.md)** - Best practices for file organization, quality optimization, batch processing, and performance
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Comprehensive troubleshooting guide for common issues and error recovery

## Quick Start

### 1. Installation

**Windows:**
```powershell
# Download from GitHub releases
# Extract to C:\Program Files\Fougue\Mayo
# Add to PATH
$env:PATH += ";C:\Program Files\Fougue\Mayo"
```

**Linux/macOS:**
```bash
# Download AppImage and make executable
chmod +x MayoConv-*-x86_64.AppImage
# Move to PATH location
sudo mv MayoConv-*-x86_64.AppImage /usr/local/bin/mayo-conv
```

### 2. Basic Usage

```bash
# Convert STEP to OBJ
mayo-conv input.step -o output.obj

# High quality conversion
mayo-conv input.step -o output.obj --meshing-edge-length 0.1

# Scale for Blender (mm to meters)
mayo-conv input.step -o output.obj --scale 0.001
```

### 3. MCP Integration

The Mayo converter integrates with these MCP servers:

- **robotics-mcp**: CAD conversion for robot modeling and simulation
- **blender-mcp**: Direct CAD import into Blender scenes
- **unity3d-mcp**: CAD pipeline support for Unity development

## Supported Formats

### Input Formats
- **STEP** (.step, .stp) - ISO 10303-21 standard
- **IGES** (.iges, .igs) - Initial Graphics Exchange Specification
- **BREP** (.brep) - OpenCASCADE Boundary Representation

### Output Formats
- **OBJ** (.obj) - Wavefront OBJ (recommended for Blender/Unity)
- **STL** (.stl) - Stereolithography (optimal for 3D printing)
- **PLY** (.ply) - Polygon File Format (point cloud data)

## Quality Settings

| Preset | Edge Length | Triangles | Use Case | Conversion Time |
|--------|-------------|-----------|----------|-----------------|
| Low | 2.0 | ~5K-20K | Prototyping | < 5 seconds |
| Medium | 0.5 | ~20K-100K | Simulation | 10-60 seconds |
| High | 0.1 | ~100K-1M | Visualization | 1-10 minutes |
| Ultra | 0.01 | ~5M+ | Maximum detail | 10+ minutes |

## Key Features

### High Performance
- OpenCASCADE-based geometry processing
- Multi-threaded mesh generation
- Memory-efficient algorithms
- Batch processing support

### Flexible Configuration
- Command-line and configuration file support
- Quality presets and custom settings
- Scale factor adjustments
- Multiple output formats

### Robust Error Handling
- Comprehensive error reporting
- Automatic recovery strategies
- Timeout and memory management
- Detailed logging and diagnostics

### MCP Integration
- Native tool integration
- Structured error responses
- Progress tracking
- Caching support

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CAD Files     │───▶│   Mayo Converter │───▶│   Mesh Files    │
│ (STEP, IGES,    │    │   (OpenCASCADE)  │    │ (OBJ, STL, PLY) │
│  BREP)         │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Robotics MCP    │    │ Blender MCP      │    │ Unity MCP       │
│ (Simulation)    │    │ (3D Modeling)    │    │ (Game Dev)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Use Cases

### Robotics Development
- Convert CAD robot parts for simulation
- Generate collision meshes for physics engines
- Prepare models for URDF generation

### Game Development
- Convert CAD assets for game engines
- Generate LOD variants automatically
- Optimize meshes for real-time rendering

### 3D Printing & Manufacturing
- Convert CAD designs to STL for printing
- Generate support structures
- Optimize mesh for printing parameters

### Research & Education
- Convert complex assemblies for analysis
- Generate meshes for computational studies
- Prepare data for visualization tools

## Configuration Examples

### Settings File (INI Format)

```ini
[General]
OutputFormat=obj
ScaleFactor=0.001

[Meshing]
EdgeLength=0.5
Angle=30.0
Deflection=0.1
Algorithm=standard

[Transform]
Scale=1.0,1.0,1.0
Translate=0.0,0.0,0.0
Rotate=0.0,0.0,0.0
```

### MCP Tool Configuration

```python
# Robotics MCP CAD converter
cad_converter_config = {
    "executable": "mayo-conv",
    "default_quality": "medium",
    "scale_factors": {
        "blender": 0.001,  # mm to meters
        "unity": 0.01,     # mm to units
        "gazebo": 0.001    # mm to meters
    },
    "cache_enabled": True,
    "timeout": 300  # 5 minutes
}
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

| Complexity | RAM Required | Recommended System |
|------------|--------------|-------------------|
| Simple parts | 50-100MB | Any modern system |
| Assemblies | 200-500MB | 8GB+ RAM |
| Complex models | 1-4GB | 16GB+ RAM |
| Large assemblies | 4GB+ | 32GB+ RAM |

## Getting Help

### Documentation
- [Integration Guide](MAYO_INTEGRATION_GUIDE.md) - Complete setup and usage
- [API Reference](API_REFERENCE.md) - Detailed command and tool reference
- [Best Practices](BEST_PRACTICES.md) - Optimization and workflow tips
- [Troubleshooting](TROUBLESHOOTING.md) - Problem diagnosis and solutions

### Support Resources
- **GitHub Issues**: [fougue/mayo](https://github.com/fougue/mayo/issues)
- **MCP Documentation**: [mcp-central-docs](https://github.com/your-org/mcp-central-docs)
- **Community**: MCP server-specific Discord/GitHub communities

### Diagnostic Information

When reporting issues, include:
- Mayo version: `mayo-conv --version`
- Operating system and version
- CAD software and version
- Sample problematic file (if possible)
- Complete error messages
- System specifications (RAM, CPU)

## Version Information

- **Mayo Version**: 0.9.0 (January 2025)
- **OpenCASCADE**: 7.7.x
- **MCP Protocol**: 2025-11-25
- **Documentation Version**: 1.0

## License

Mayo CAD Converter is licensed under BSD 2-Clause License.
OpenCASCADE technology provides the underlying CAD geometry processing.

---

*Last updated: January 2026*
