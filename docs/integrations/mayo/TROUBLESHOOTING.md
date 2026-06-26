# Mayo CAD Converter Troubleshooting Guide

## Quick Diagnosis

### Installation Issues

#### Symptom: "mayo-conv command not found"

**Diagnosis:**
```bash
# Check if Mayo is installed
mayo-conv --version

# Check PATH environment
echo $PATH | tr ':' '\n' | grep -i mayo

# Find Mayo installation
find /usr -name "mayo-conv" 2>/dev/null
find "C:\Program Files" -name "*mayo*" -type d
```

**Solutions:**

1. **Add to PATH (Linux/macOS):**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$PATH:/path/to/mayo"
   source ~/.bashrc
   ```

2. **Add to PATH (Windows):**
   ```powershell
   # PowerShell (run as Administrator)
   $mayoPath = "C:\Program Files\Fougue\Mayo"
   [Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$mayoPath", "Machine")
   ```

3. **Use absolute path:**
   ```python
   # In MCP tool configuration
   MAYO_EXECUTABLE = "/full/path/to/mayo-conv.exe"
   ```

#### Symptom: "Permission denied" on Linux/macOS

**Diagnosis:**
```bash
ls -la /path/to/mayo-conv
```

**Solutions:**
```bash
# Make executable
chmod +x /path/to/mayo-conv

# Or reinstall with proper permissions
sudo chmod 755 /path/to/mayo-conv
```

### File Format Issues

#### Symptom: "Unsupported file format"

**Diagnosis:**
```bash
# Check file extension
file input.step
head -c 100 input.step | hexdump -C

# Validate STEP file
grep -i "ISO-10303-21" input.step
```

**Supported Formats:**
- **STEP**: `.step`, `.stp`, `.p21` (ISO 10303-21)
- **IGES**: `.iges`, `.igs` (versions 5.3, 6.0)
- **BREP**: `.brep`, `.rle` (OpenCASCADE native)

**Solutions:**
1. **Convert file format** using CAD software
2. **Repair corrupted files** in original CAD application
3. **Export clean STEP** from CAD software

#### Symptom: "Empty or invalid geometry"

**Diagnosis:**
```bash
# Check file size
ls -lh input.step

# Basic validation
mayo-conv input.step --help 2>&1 | grep -i error
```

**Causes:**
- Empty parts/assemblies in CAD
- Construction geometry exported
- Hidden/suppressed features

**Solutions:**
1. **Check CAD model** for empty bodies
2. **Export visible geometry only**
3. **Use "Export as STEP"** instead of "Save As"

### Conversion Quality Issues

#### Symptom: "Mesh too coarse/blocky"

**Diagnosis:**
```bash
# Check current quality settings
mayo-conv input.step -o output.obj --meshing-edge-length 0.1
```

**Solutions:**

1. **Reduce edge length:**
   ```bash
   mayo-conv input.step -o output.obj --meshing-edge-length 0.05
   ```

2. **Adjust angle tolerance:**
   ```bash
   mayo-conv input.step -o output.obj --meshing-angle 10.0
   ```

3. **Use quality presets:**
   ```python
   quality_settings = {
       "high": "--meshing-edge-length 0.1 --meshing-angle 15.0",
       "ultra": "--meshing-edge-length 0.01 --meshing-angle 5.0"
   }
   ```

#### Symptom: "Mesh too dense/slow"

**Diagnosis:**
```bash
# Check triangle count
# (Use mesh analysis tool or import into Blender)
```

**Solutions:**

1. **Increase edge length:**
   ```bash
   mayo-conv input.step -o output.obj --meshing-edge-length 1.0
   ```

2. **Use fast algorithm:**
   ```bash
   mayo-conv input.step -o output.obj --algorithm fast
   ```

3. **Simplify geometry first** in CAD software

### Scale and Units Issues

#### Symptom: "Model too small/large in target application"

**Diagnosis:**
```python
# Expected size ranges
blender_ranges = {"min": 0.1, "max": 100}  # meters
unity_ranges = {"min": 0.01, "max": 1000}  # units

# Check current scale
current_bounds = get_model_bounds(output_file)
print(f"Model size: {current_bounds}")
```

**Common Scale Factors:**

| CAD Units | Target App | Scale Factor | Example |
|-----------|------------|--------------|---------|
| mm | Blender | 0.001 | `--scale 0.001` |
| mm | Unity | 0.01 | `--scale 0.01` |
| inches | Blender | 0.0254 | `--scale 0.0254` |

**Solutions:**

1. **Apply correct scale factor:**
   ```bash
   # CAD mm → Blender meters
   mayo-conv input.step -o output.obj --scale 0.001
   ```

2. **Check CAD export units** in original software

3. **Post-process scaling:**
   ```python
   import trimesh

   mesh = trimesh.load('output.obj')
   mesh.apply_scale(0.001)  # Scale down by factor
   mesh.export('scaled_output.obj')
   ```

### Performance Issues

#### Symptom: "Conversion takes too long"

**Diagnosis:**
```bash
# Time the conversion
time mayo-conv input.step -o output.obj

# Check file size
ls -lh input.step

# Monitor system resources
top -p $(pgrep mayo-conv)
```

**Performance Factors:**
- **File size**: >100MB files are slow
- **Model complexity**: High face counts
- **Mesh quality**: Lower quality = faster
- **System RAM**: Insufficient memory causes swapping

**Solutions:**

1. **Use lower quality for testing:**
   ```bash
   mayo-conv input.step -o output.obj --meshing-edge-length 2.0
   ```

2. **Split large assemblies:**
   ```bash
   # Export individual parts separately
   mayo-conv part1.step -o part1.obj
   mayo-conv part2.step -o part2.obj
   ```

3. **Increase system resources** or use cloud processing

#### Symptom: "Out of memory errors"

**Diagnosis:**
```bash
# Check available RAM
free -h
# Windows: Get-WmiObject Win32_OperatingSystem | Select FreePhysicalMemory

# Check ulimits (Linux)
ulimit -a
```

**Solutions:**

1. **Reduce mesh quality:**
   ```bash
   mayo-conv input.step -o output.obj --meshing-edge-length 1.0
   ```

2. **Process in parts:**
   ```bash
   # Split large assemblies
   mayo-conv --split-assembly input.step -o output_dir/
   ```

3. **Increase system memory** or use swap file

4. **Use streaming processing** for very large files

### Integration Issues

#### Symptom: "MCP server can't find mayo-conv"

**Diagnosis:**
```python
import subprocess
import os

# Test direct execution
try:
    result = subprocess.run(['mayo-conv', '--version'],
                          capture_output=True, text=True, timeout=10)
    print("Success:", result.stdout)
except Exception as e:
    print("Error:", e)

# Check PATH in Python
print("Python PATH:", os.environ.get('PATH', '').split(os.pathsep))
```

**Solutions:**

1. **Set MAYO_PATH environment variable:**
   ```bash
   export MAYO_PATH="/full/path/to/mayo-conv"
   ```

2. **Configure in MCP server:**
   ```python
   # In MCP server configuration
   MAYO_EXECUTABLE = os.environ.get('MAYO_PATH', 'mayo-conv')
   ```

3. **Use absolute path in tools:**
   ```python
   command = ['/full/path/to/mayo-conv', input_file, '-o', output_file]
   ```

#### Symptom: "Timeout errors in MCP tools"

**Diagnosis:**
```python
# Check current timeout settings
timeout_config = get_mcp_timeout_config()
print("Current timeout:", timeout_config)

# Test conversion time
import time
start = time.time()
result = subprocess.run(['mayo-conv', 'input.step', '-o', 'output.obj'])
duration = time.time() - start
print(f"Conversion took: {duration} seconds")
```

**Solutions:**

1. **Increase timeout in MCP calls:**
   ```python
   result = await asyncio.wait_for(
       convert_cad_tool(request),
       timeout=300  # 5 minutes
   )
   ```

2. **Use progress callbacks:**
   ```python
   async def convert_with_progress(cad_path, progress_callback):
       process = await asyncio.create_subprocess_exec(
           'mayo-conv', cad_path, '-o', output_path,
           stdout=asyncio.subprocess.PIPE,
           stderr=asyncio.subprocess.PIPE
       )

       # Monitor progress and call callback
       while not process.stdout.at_eof():
           line = await process.stdout.readline()
           progress_callback(line.decode())

       return await process.wait()
   ```

3. **Implement resumable conversions** for large files

### Output Format Issues

#### Symptom: "OBJ file won't import into application"

**Diagnosis:**
```bash
# Check file format
head -20 output.obj
file output.obj

# Validate OBJ structure
grep -c "^v " output.obj  # vertices
grep -c "^f " output.obj  # faces
```

**OBJ Requirements:**
- Must have vertices (`v x y z`)
- Must have faces (`f v1 v2 v3`)
- May have normals (`vn x y z`)
- May have texture coordinates (`vt u v`)

**Solutions:**

1. **Use STL format instead:**
   ```bash
   mayo-conv input.step -o output.stl
   ```

2. **Check for empty geometry:**
   ```bash
   if [ $(grep -c "^f " output.obj) -eq 0 ]; then
       echo "No faces found - empty geometry"
   fi
   ```

3. **Repair in mesh processing software** (Blender, Meshlab)

#### Symptom: "STL file has holes/gaps"

**Diagnosis:**
```bash
# Check for manifold issues
# (Use mesh analysis tools or import into Blender)
python -c "
import trimesh
mesh = trimesh.load('output.stl')
print('Is watertight:', mesh.is_watertight)
print('Is manifold:', mesh.is_manifold)
print('Holes:', len(mesh.faces) - len(mesh.faces_unique))
"
```

**Solutions:**

1. **Use different mesh algorithm:**
   ```bash
   mayo-conv input.step -o output.stl --algorithm robust
   ```

2. **Increase mesh quality:**
   ```bash
   mayo-conv input.step -o output.stl --meshing-edge-length 0.05
   ```

3. **Repair mesh in post-processing:**
   ```bash
   # Use Blender or Meshlab to fix holes
   blender --background --python fix_mesh.py output.stl
   ```

### Network/Remote Issues

#### Symptom: "Conversion fails on remote files"

**Diagnosis:**
```bash
# Test local file access
ls -la /remote/path/input.step

# Test network connectivity
ping remote.host
```

**Solutions:**

1. **Copy files locally first:**
   ```python
   import shutil
   import tempfile

   with tempfile.TemporaryDirectory() as temp_dir:
       local_file = os.path.join(temp_dir, os.path.basename(remote_file))
       shutil.copy2(remote_file, local_file)

       # Convert local file
       result = await convert_cad_file(local_file, output_path)
   ```

2. **Use streaming for large files:**
   ```python
   async def convert_remote_file(remote_url, output_path):
       async with aiohttp.ClientSession() as session:
           async with session.get(remote_url) as response:
               with tempfile.NamedTemporaryFile() as temp_file:
                   async for chunk in response.content.iter_chunked(8192):
                       temp_file.write(chunk)
                   temp_file.flush()

                   # Convert temp file
                   result = await convert_cad_file(temp_file.name, output_path)
                   return result
   ```

## Advanced Debugging

### Verbose Logging

Enable detailed logging for troubleshooting:

```bash
# Command line verbose output
mayo-conv input.step -o output.obj --verbose

# Environment variable for extra debug info
export MAYO_DEBUG=1
mayo-conv input.step -o output.obj
```

### Core Dump Analysis (Linux)

```bash
# Enable core dumps
ulimit -c unlimited

# Run conversion
mayo-conv input.step -o output.obj

# Analyze core dump if crash occurs
gdb mayo-conv core.mayo-conv
```

### Memory Profiling

```python
import memory_profiler
import psutil

@memory_profiler.profile
def convert_with_memory_monitoring(input_file, output_file):
    """Convert with memory usage tracking."""

    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Perform conversion
    result = subprocess.run(['mayo-conv', input_file, '-o', output_file])

    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = final_memory - initial_memory

    print(f"Memory used: {memory_used:.1f} MB")
    print(f"Peak memory: {process.memory_info().peak_rss / 1024 / 1024:.1f} MB")

    return result
```

### CAD File Analysis

```python
def analyze_cad_file(cad_path):
    """Analyze CAD file for potential conversion issues."""

    analysis = {
        'file_size': os.path.getsize(cad_path),
        'file_extension': os.path.splitext(cad_path)[1].lower(),
        'estimated_complexity': 'unknown',
        'potential_issues': []
    }

    # Check file size
    if analysis['file_size'] > 100 * 1024 * 1024:  # 100MB
        analysis['potential_issues'].append('Large file - may be slow')

    # Basic content analysis for STEP files
    if analysis['file_extension'] in ['.step', '.stp']:
        with open(cad_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(10000)  # First 10KB

            # Count entities
            entity_count = content.count('=')
            analysis['estimated_complexity'] = f"~{entity_count} entities"

            # Check for binary STEP (uncommon but possible)
            if '\x00' in content[:100]:
                analysis['potential_issues'].append('May be binary STEP format')

    return analysis
```

## Common Error Patterns

### Error Code Reference

| Error Code | Description | Likely Cause | Solution |
|------------|-------------|--------------|----------|
| `1` | General error | Various | Check logs |
| `2` | File not found | Invalid path | Verify file exists |
| `3` | Permission denied | Access issues | Check permissions |
| `4` | Invalid format | Unsupported file | Convert file format |
| `5` | Memory error | Insufficient RAM | Reduce quality/split file |
| `6` | Timeout | Long conversion | Increase timeout |
| `7` | Geometry error | Invalid CAD data | Repair in CAD software |

### Log Message Patterns

**Memory Issues:**
```
ERROR: std::bad_alloc
ERROR: Out of memory
WARNING: Memory allocation failed
```

**File Issues:**
```
ERROR: Cannot open file
ERROR: File format not recognized
WARNING: Invalid STEP structure
```

**Geometry Issues:**
```
ERROR: Empty geometry
WARNING: Degenerate faces detected
ERROR: Invalid topology
```

## Recovery Procedures

### Automatic Recovery

```python
async def convert_with_recovery(cad_path, output_path, max_attempts=3):
    """Convert with automatic error recovery."""

    strategies = [
        {},  # Default settings
        {'quality': 'low'},  # Reduce quality
        {'format': 'stl'},  # Try different format
        {'scale': 1.0},  # Reset scale
    ]

    for attempt, strategy in enumerate(strategies[:max_attempts]):
        try:
            result = await convert_cad_with_strategy(cad_path, output_path, strategy)
            if attempt > 0:
                logger.info(f"Recovery successful on attempt {attempt + 1}")
            return result

        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            continue

    raise RuntimeError(f"All {max_attempts} recovery attempts failed")
```

### Manual Recovery Steps

1. **Identify the issue** using diagnostic commands
2. **Simplify the CAD model** in original software
3. **Try alternative export settings** from CAD
4. **Use different file formats** if available
5. **Split complex assemblies** into components
6. **Contact support** with diagnostic information

## Support Resources

### Getting Help

1. **Check existing issues:** [Mayo GitHub Issues](https://github.com/fougue/mayo/issues)
2. **MCP server logs:** Check `logs/mcp_server.log`
3. **System information:**
   ```bash
   # Linux/macOS
   uname -a
   mayo-conv --version

   # Windows
   systeminfo | findstr /B /C:"OS"
   mayo-conv --version
   ```

### Diagnostic Information

When reporting issues, include:

- Mayo version: `mayo-conv --version`
- Operating system and version
- CAD software and version used to create files
- Sample problematic CAD file (if possible)
- Complete error messages and logs
- System specifications (RAM, CPU)

---

*Troubleshooting Version: 1.0*
*Last updated: January 2026*
