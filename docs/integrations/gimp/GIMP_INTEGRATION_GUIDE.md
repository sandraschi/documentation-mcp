# GIMP MCP Integration Guide

## Overview

This comprehensive guide covers the integration of GIMP (GNU Image Manipulation Program) with MCP (Model Context Protocol) servers, enabling automated image processing, batch operations, and creative workflows through programmatic control.

## Architecture Overview

### GIMP MCP Server Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   MCP Client    â”‚â”€â”€â”€â–¶â”‚   GIMP MCP       â”‚â”€â”€â”€â–¶â”‚   GIMP App      â”‚
â”‚   (Python/Node) â”‚    â”‚   Server         â”‚    â”‚   (GUI/Headless)â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚                       â”‚                       â”‚
         â–¼                       â–¼                       â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Blender MCP     â”‚    â”‚ Unity3D MCP      â”‚    â”‚ Advanced Memory â”‚
â”‚ (Textures)      â”‚    â”‚ (Game Assets)    â”‚    â”‚ MCP (Assets)    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Communication Patterns

- **Synchronous**: Direct API calls for immediate image operations
- **Asynchronous**: Background processing for complex filters and batch operations
- **Streaming**: Real-time updates for interactive editing sessions
- **Batch Processing**: Queue-based processing for large image collections

## Installation & Setup

### Prerequisites

**System Requirements:**
- **OS**: Windows 7+, macOS 10.9+, Linux (Ubuntu 16.04+)
- **RAM**: 2GB minimum, 8GB recommended for complex operations
- **Storage**: 2GB for GIMP installation + workspace
- **Display**: 1280x720 minimum resolution

**Software Dependencies:**
- Python 3.6+ (included with GIMP)
- GIMP 3.1.1++ (recommended 3.1.1+.34+)
- GEGL library for advanced filters
- BABL library for color management

### GIMP Installation

#### Windows Installation

1. **Download**: Get GIMP installer from [official website](https://www.gimp.org/downloads/)
2. **Install**: Run installer with default options
   - Include Python support
   - Include GEGL operations
   - Include debug symbols (for troubleshooting)

3. **Verify Installation**:
```powershell
& "C:\Program Files\GIMP 2\bin\gimp-3.1.1+.exe" --version
# Should output: GNU Image Manipulation Program version 3.1.1+.x
```

4. **Test Python Support**:
```powershell
& "C:\Program Files\GIMP 2\bin\gimp-3.1.1+.exe" --batch - < python_test.py
```

#### Linux Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install gimp gimp-python gimp-data-extras

# Or compile from source
sudo apt install build-essential libgtk-3-dev libgegl-dev libbabl-dev
wget https://download.gimp.org/pub/gimp/v3.1.1+/gimp-3.1.1+.34.tar.bz2
tar -xf gimp-3.1.1+.34.tar.bz2
cd gimp-3.1.1+.34
./configure --enable-python
make
sudo make install
```

#### macOS Installation

```bash
# Homebrew
brew install gimp

# Or download DMG from website
# Drag GIMP.app to Applications folder
```

### MCP Server Setup

#### gimp-mcp Installation

```bash
# Clone and install
git clone https://github.com/your-org/gimp-mcp.git
cd gimp-mcp
pip install -e .

# Configure GIMP path
export GIMP_EXECUTABLE="/usr/bin/gimp"
export GIMP_CONSOLE_PATH="/usr/bin/gimp-console"
```

#### Configuration File

```json
{
  "gimp": {
    "executable": "/usr/bin/gimp",
    "console_executable": "/usr/bin/gimp-console",
    "version": "3.1.1+",
    "python_path": "/usr/lib/python3/dist-packages",
    "plugin_path": "~/.config/GIMP/3.1.1+/plug-ins",
    "temp_dir": "/tmp/gimp_mcp"
  },
  "workspace": {
    "cache_dir": "/var/cache/gimp_mcp",
    "output_dir": "/home/user/gimp_output",
    "max_open_images": 10
  },
  "performance": {
    "max_concurrent_jobs": 4,
    "timeout": 300,
    "memory_limit": "2GB"
  },
  "quality": {
    "default_jpeg_quality": 90,
    "default_png_compression": 6,
    "enable_color_management": true
  }
}
```

## Basic Usage

### Connecting to GIMP

```python
from gimp_mcp import GIMPClient

# Initialize client
client = GIMPClient()

# Connect to running GIMP instance or start new one
await client.connect()

# Verify connection
version = await client.get_version()
print(f"Connected to GIMP {version}")
```

### Basic Image Operations

#### Opening and Saving Images

```python
# Open image
image = await client.open_image("/path/to/image.jpg")

# Get image properties
width, height = await client.get_image_size(image)
mode = await client.get_image_mode(image)  # RGB, GRAY, INDEXED

# Save with different formats
await client.save_image(image, "/output/result.png")
await client.save_image(image, "/output/result.jpg", quality=95)
await client.save_image(image, "/output/result.tiff", compression="lzw")
```

#### Layer Management

```python
# Create new layer
layer = await client.create_layer(image, "New Layer", width=1920, height=1080)

# Duplicate layer
duplicate_layer = await client.duplicate_layer(layer)

# Move layer in stack
await client.move_layer(layer, position=0)  # Move to bottom

# Set layer properties
await client.set_layer_opacity(layer, 0.8)
await client.set_layer_mode(layer, "MULTIPLY")
await client.set_layer_visible(layer, True)
```

#### Selections and Masks

```python
# Create rectangular selection
await client.select_rectangle(image, x=100, y=100, width=500, height=300)

# Create elliptical selection
await client.select_ellipse(image, x=200, y=200, radius_x=150, radius_y=100)

# Feather selection
await client.feather_selection(image, radius=5.0)

# Create layer mask from selection
mask = await client.create_layer_mask_from_selection(layer)

# Apply mask
await client.apply_layer_mask(layer)
```

### Color and Tone Adjustments

#### Basic Adjustments

```python
# Brightness/Contrast
await client.adjust_brightness_contrast(image, brightness=10, contrast=15)

# Levels
await client.adjust_levels(image, shadows=20, midtones=1.1, highlights=240)

# Curves
curve_points = [(0, 0), (64, 50), (128, 128), (192, 180), (255, 255)]
await client.adjust_curves(image, curve_points)

# Hue/Saturation
await client.adjust_hue_saturation(image, hue=10, saturation=20, lightness=5)
```

#### Color Correction

```python
# Auto color correction
await client.auto_color_correct(image)

# Color balance
await client.adjust_color_balance(image, cyan_red=5, magenta_green=-3, yellow_blue=2)

# White balance
await client.adjust_white_balance(image, temperature=5500, tint=10)

# Remove color cast
await client.remove_color_cast(image, neutral_color=(128, 128, 128))
```

## Advanced Features

### Filters and Effects

#### Built-in Filters

```python
# Blur filters
await client.apply_gaussian_blur(image, radius=5.0)
await client.apply_motion_blur(image, angle=45, distance=20)
await client.apply_lens_blur(image, radius=10)

# Sharpen filters
await client.apply_unsharp_mask(image, radius=1.0, amount=1.5, threshold=0)
await client.apply_smart_sharpen(image, amount=50, radius=1.0, threshold=0)

# Noise filters
await client.apply_noise_reduction(image, strength=25)
await client.add_rgb_noise(image, red=5, green=5, blue=5, alpha=0)
```

#### Artistic Filters

```python
# Oil paint effect
await client.apply_oil_paint(image, mask_size=5, exponent=8)

# Cartoon effect
await client.apply_cartoon(image, mask_radius=7, pct_black=0.2)

# Photocopy effect
await client.apply_photocopy(image, mask_radius=5, sharpness=0.8, pct_black=0.2)

# Weave effect
await client.apply_weave(image, width=10, height=10, shadow_darkness=1.0, shadow_depth=3)
```

#### Distortions

```python
# Lens distortion
await client.apply_lens_distortion(image, main=20, edge=0, zoom=0, x_shift=0, y_shift=0)

# Perspective correction
await client.correct_perspective(image, corners=[(0,0), (100,0), (100,100), (0,100)])

# Barrel distortion
await client.apply_barrel_distortion(image, strength=0.5)
```

### Scripting and Automation

#### Script-Fu Scripts

```python
# Execute Script-Fu script
await client.execute_script_fu('script-fu-drop-shadow image layer 5 5 15 \'(0 0 0) 80 TRUE')

# Create custom Script-Fu
script = '''
(define (my-custom-effect img drawable)
  (gimp-image-undo-group-start img)
  (gimp-desaturate drawable)
  (plug-in-gauss 1 img drawable 5.0 5.0 1)
  (gimp-image-undo-group-end img)
)
'''
await client.define_script_fu("my-custom-effect", script)
```

#### Python Scripting

```python
# Execute Python script in GIMP context
python_script = '''
import gimp
from gimpfu import *

def my_python_filter(img, layer):
    gimp.progress_init("Processing...")
    # Custom processing logic
    pdb.gimp_desaturate(layer)
    pdb.plug_in_gauss_rle(img, layer, 5, True, True)
    gimp.progress_update(1.0)
    return layer

register(
    "my_python_filter",
    "My Custom Python Filter",
    "Description",
    "Author",
    "Copyright",
    "2024",
    "<Image>/Filters/Custom/My Filter",
    "*",
    [],
    [],
    my_python_filter
)

main()
'''

await client.execute_python_script(python_script)
```

### Plugin Integration

#### Using Existing Plugins

```python
# Resynthesizer (heal tool)
await client.apply_resynthesizer_heal(image, source_selection, target_selection)

# Liquid Rescale
await client.apply_liquid_rescale(image, new_width=800, new_height=600, rigidity=0)

# Wavelet Decompose
await client.apply_wavelet_decompose(image, scales=5)

# G'MIC filters
await client.apply_gmic_filter(image, "blur", "gaussian", radius=3)
```

#### Custom Plugin Development

```python
# Register custom plugin
plugin_code = '''
#!/usr/bin/env python3

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import GObject

class MyCustomPlugin(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["my-custom-operation"]

    def do_create_procedure(self, name):
        procedure = Gimp.Procedure.new(self, name,
                                     Gimp.PDBProcType.PLUGIN,
                                     self.run, None)
        procedure.add_menu_path('<Image>/Filters/Custom/')
        return procedure

    def run(self, procedure, run_mode, image, n_drawables, drawables, args, run_data):
        # Plugin implementation
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())
'''

await client.install_custom_plugin("my_custom_plugin.py", plugin_code)
```

## Integration Workflows

### Photo Editing Pipeline

```python
async def professional_photo_pipeline(input_path, output_path, corrections):
    """Complete professional photo editing pipeline."""

    gimp = GIMPClient()
    await gimp.connect()

    try:
        # Load image
        image = await gimp.open_image(input_path)

        # Initial assessment
        histogram = await gimp.analyze_histogram(image)
        exposure_issues = await gimp.detect_exposure_problems(image)

        # Color space conversion if needed
        if await gimp.get_image_color_space(image) != "RGB":
            await gimp.convert_color_space(image, "RGB")

        # Lens correction
        if corrections.get("lens_correction"):
            await gimp.correct_lens_distortion(image, corrections["lens_profile"])

        # Noise reduction
        if corrections.get("noise_reduction"):
            await gimp.apply_noise_reduction(image, strength=corrections["noise_strength"])

        # Color correction
        await gimp.apply_color_correction_profile(image, corrections["color_profile"])

        # Detail enhancement
        await gimp.enhance_details(image, radius=1.0, amount=0.3)

        # Final sharpening
        await gimp.apply_selective_sharpening(image, radius=1.0, amount=0.8, threshold=10)

        # Output with color management
        await gimp.save_with_color_management(image, output_path,
                                            color_space="sRGB",
                                            quality=95)

    finally:
        await gimp.disconnect()
```

### Texture Creation Pipeline

```python
async def create_texture_atlas(source_images, atlas_spec):
    """Create texture atlas from multiple source images."""

    gimp = GIMPClient()
    await gimp.connect()

    try:
        # Create new atlas image
        atlas_width, atlas_height = atlas_spec["dimensions"]
        atlas = await gimp.create_new_image(atlas_width, atlas_height, "RGBA")

        # Layout images in atlas
        layout = await gimp.calculate_atlas_layout(source_images, atlas_spec["packing"])

        for i, (image_path, position) in enumerate(layout.items()):
            # Load source image
            source_img = await gimp.open_image(image_path)

            # Process for atlas
            await gimp.resize_image(source_img, position["width"], position["height"])
            await gimp.apply_texture_compression(source_img, atlas_spec["compression"])

            # Copy to atlas
            await gimp.copy_to_atlas(atlas, source_img, position["x"], position["y"])

            # Close source
            await gimp.close_image(source_img)

        # Generate mipmaps if specified
        if atlas_spec.get("generate_mipmaps"):
            await gimp.generate_mipmap_chain(atlas, atlas_spec["mipmap_levels"])

        # Save atlas variants
        await gimp.save_texture_atlas(atlas, atlas_spec["output_formats"])

        return atlas_spec["output_files"]

    finally:
        await gimp.disconnect()
```

### Batch Processing Workflows

```python
async def batch_image_processing(input_dir, output_dir, processing_spec):
    """Process large collections of images."""

    gimp = GIMPClient()
    await gimp.connect()

    try:
        # Discover images
        image_files = await gimp.find_images_recursive(input_dir, processing_spec["file_types"])

        # Process in batches
        batch_size = processing_spec.get("batch_size", 10)
        results = []

        for i in range(0, len(image_files), batch_size):
            batch = image_files[i:i + batch_size]

            # Process batch concurrently
            batch_results = await asyncio.gather(*[
                process_single_image(gimp, img_path, output_dir, processing_spec)
                for img_path in batch
            ], return_exceptions=True)

            results.extend(batch_results)

            # Progress reporting
            progress = (i + len(batch)) / len(image_files) * 100
            print(f"Processed {i + len(batch)}/{len(image_files)} images ({progress:.1f}%)")

        return results

    finally:
        await gimp.disconnect()

async def process_single_image(gimp, input_path, output_dir, spec):
    """Process a single image according to specifications."""

    try:
        # Load image
        image = await gimp.open_image(input_path)

        # Apply processing pipeline
        for operation in spec["operations"]:
            if operation["type"] == "resize":
                await gimp.resize_image(image, operation["width"], operation["height"])
            elif operation["type"] == "filter":
                await gimp.apply_filter(image, operation["filter_name"], **operation["params"])
            elif operation["type"] == "adjustment":
                await gimp.apply_adjustment(image, operation["adjustment_type"], **operation["params"])

        # Save result
        output_path = await gimp.generate_output_path(input_path, output_dir, spec["output_format"])
        await gimp.save_image(image, output_path, **spec["save_options"])

        # Close image
        await gimp.close_image(image)

        return {"status": "success", "input": input_path, "output": output_path}

    except Exception as e:
        return {"status": "error", "input": input_path, "error": str(e)}
```

## Performance Optimization

### Memory Management

**Large Image Handling:**
```python
# Configure memory limits
await gimp.set_memory_limits(
    tile_cache_size="1GB",
    max_new_image_size="512MB",
    undo_levels=5
)

# Process large images in tiles
async def process_large_image_tiled(gimp, image_path, tile_size=2048):
    """Process large images by dividing into tiles."""

    # Get image dimensions
    full_image = await gimp.open_image(image_path)
    width, height = await gimp.get_image_size(full_image)

    # Calculate tile grid
    tiles_x = (width + tile_size - 1) // tile_size
    tiles_y = (height + tile_size - 1) // tile_size

    processed_tiles = []

    for tile_y in range(tiles_y):
        for tile_x in range(tiles_x):
            # Calculate tile boundaries
            x1 = tile_x * tile_size
            y1 = tile_y * tile_size
            x2 = min(x1 + tile_size, width)
            y2 = min(y1 + tile_size, height)

            # Extract tile
            tile = await gimp.extract_tile(full_image, x1, y1, x2, y2)

            # Process tile
            processed_tile = await gimp.process_tile(tile)

            processed_tiles.append({
                "position": (x1, y1),
                "image": processed_tile
            })

    # Reassemble tiles
    result = await gimp.assemble_tiles(processed_tiles, width, height)

    return result
```

### GPU Acceleration

**Configure GEGL for GPU:**
```python
# Enable GPU acceleration for GEGL operations
await gimp.configure_gegl_backend(
    use_gpu=True,
    gpu_device="auto",  # auto, cuda, opencl
    tile_size=1024,
    threads=8
)

# Use GPU-accelerated filters
await gimp.set_filter_acceleration("gaussian-blur", "GPU")
await gimp.set_filter_acceleration("unsharp-mask", "GPU")
await gimp.set_filter_acceleration("color-balance", "GPU")
```

### Caching Strategies

**Implement Smart Caching:**
```python
class GIMPCache:
    def __init__(self, cache_dir="/cache/gimp"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    async def get_cached_result(self, operation_hash, output_format):
        """Get cached operation result."""
        cache_file = self.cache_dir / f"{operation_hash}.{output_format}"
        if cache_file.exists():
            return str(cache_file)
        return None

    async def cache_result(self, operation_hash, result_path, output_format):
        """Cache operation result."""
        cache_file = self.cache_dir / f"{operation_hash}.{output_format}"
        await gimp.copy_file(result_path, str(cache_file))
        return str(cache_file)

    def generate_operation_hash(self, image_path, operations):
        """Generate hash for operation cache key."""
        image_hash = hashlib.md5(open(image_path, 'rb').read()).hexdigest()
        ops_str = json.dumps(operations, sort_keys=True)
        ops_hash = hashlib.md5(ops_str.encode()).hexdigest()
        return f"{image_hash}_{ops_hash}"
```

## Error Handling

### Connection Issues

```python
async def connect_with_retry(max_retries=3, delay=2.0):
    """Connect to GIMP with retry logic."""

    gimp = GIMPClient()

    for attempt in range(max_retries):
        try:
            await gimp.connect()
            print(f"Connected to GIMP on attempt {attempt + 1}")
            return gimp
        except GIMPConnectionError as e:
            if attempt < max_retries - 1:
                print(f"Connection failed (attempt {attempt + 1}), retrying in {delay}s")
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                raise RuntimeError(f"Failed to connect to GIMP after {max_retries} attempts") from e
```

### Operation Timeouts

```python
async def execute_with_timeout(operation, timeout=120):
    """Execute GIMP operation with timeout protection."""

    try:
        result = await asyncio.wait_for(operation, timeout=timeout)
        return result
    except asyncio.TimeoutError:
        # Cancel operation if possible
        await gimp.cancel_current_operation()
        # Clean up temporary files
        await gimp.cleanup_temp_files()
        raise RuntimeError(f"Operation timed out after {timeout} seconds")
```

### Resource Cleanup

```python
class GIMPResourceManager:
    def __init__(self, gimp_client):
        self.client = gimp_client
        self.open_images = []
        self.temp_files = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Close all open images
        for image in self.open_images:
            try:
                await self.client.close_image(image)
            except:
                pass  # Ignore errors during cleanup

        # Clean up temp files
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except:
                pass

    async def open_tracked_image(self, path):
        """Open image and track for cleanup."""
        image = await self.client.open_image(path)
        self.open_images.append(image)
        return image

    async def create_temp_file(self, suffix=".png"):
        """Create temporary file tracked for cleanup."""
        temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        temp_file.close()
        self.temp_files.append(temp_file.name)
        return temp_file.name
```

## Scripting and Automation

### Batch Script Development

**Template for Batch Processing:**
```python
#!/usr/bin/env python3

import asyncio
import sys
from pathlib import Path
from gimp_mcp import GIMPClient

async def main():
    if len(sys.argv) < 3:
        print("Usage: batch_process.py <input_dir> <output_dir>")
        sys.exit(1)

    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(exist_ok=True)

    # Initialize GIMP
    gimp = GIMPClient()
    await gimp.connect()

    try:
        # Find all images
        image_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
        image_files = [
            f for f in input_dir.rglob('*')
            if f.suffix.lower() in image_extensions
        ]

        print(f"Found {len(image_files)} images to process")

        for image_file in image_files:
            try:
                # Process image
                result_path = await process_image(gimp, image_file, output_dir)
                print(f"Processed: {image_file.name} â†’ {result_path}")

            except Exception as e:
                print(f"Failed to process {image_file.name}: {e}")

    finally:
        await gimp.disconnect()

async def process_image(gimp, input_path, output_dir):
    """Process a single image."""

    # Open image
    image = await gimp.open_image(str(input_path))

    # Apply processing
    await gimp.adjust_levels(image, shadows=10, highlights=245)
    await gimp.apply_unsharp_mask(image, radius=1.0, amount=1.2, threshold=5)

    # Generate output path
    output_path = output_dir / f"{input_path.stem}_processed{input_path.suffix}"

    # Save
    await gimp.save_image(image, str(output_path), quality=95)

    # Close
    await gimp.close_image(image)

    return output_path

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Filter Development

**GEGL-based Custom Filter:**
```python
async def create_custom_gegl_filter(gimp, filter_spec):
    """Create custom filter using GEGL operations."""

    # Define filter pipeline
    filter_ops = [
        {"op": "gegl:gaussian-blur", "params": {"std-dev-x": 3.0, "std-dev-y": 3.0}},
        {"op": "gegl:unsharp-mask", "params": {"std-dev": 1.0, "scale": 1.5}},
        {"op": "gegl:contrast-curve", "params": {"curve": [0,0, 255,255]}}
    ]

    # Register filter
    filter_id = await gimp.register_gegl_filter(
        name=filter_spec["name"],
        description=filter_spec["description"],
        operations=filter_ops
    )

    return filter_id

# Usage
filter_spec = {
    "name": "my_enhancement_filter",
    "description": "Custom image enhancement filter"
}

filter_id = await create_custom_gegl_filter(gimp, filter_spec)

# Apply filter
await gimp.apply_custom_filter(image, filter_id)
```

## Version Compatibility

### GIMP Version Matrix

| Feature | 2.8 | 3.1.1+.0-3.1.1+.18 | 3.1.1+.20+ | 2.99 (Dev) |
|---------|-----|----------------|----------|------------|
| Python 3 | No | Yes | Yes | Yes |
| GEGL | Partial | Full | Full | Enhanced |
| GPU Accel | Basic | Full | Full | Advanced |
| Color Mgmt | Basic | Full | Full | Enhanced |
| Plugins | Python 2 | Python 3 | Python 3 | Python 3 |

### MCP Compatibility

- **MCP Protocol**: 2025-11-25 and later
- **GIMP Python**: 3.1.1++ required
- **GEGL**: 0.4+ recommended
- **BABL**: 0.1+ required

---

*Integration Guide Version: 1.0*
*GIMP Version: 3.1.1+.x*
*MCP Protocol: 2024-11-05*
*Last updated: January 2026*

