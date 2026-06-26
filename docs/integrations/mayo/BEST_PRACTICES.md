# Mayo CAD Converter Best Practices

## File Organization

### Directory Structure

```
project/
├── cad/                    # Original CAD files
│   ├── assemblies/        # Complete assemblies
│   ├── parts/            # Individual components
│   └── vendor/           # Third-party components
├── converted/            # Converted mesh files
│   ├── obj/             # Wavefront OBJ files
│   ├── stl/             # STL files for 3D printing
│   └── ply/             # PLY files for scanning
├── cache/               # Conversion cache
└── config/              # Mayo settings files
    └── mayo.ini
```

### Naming Conventions

- **Input files**: `part_name.step`, `assembly_v2.iges`
- **Output files**: `part_name_high.obj`, `part_name_medium.stl`
- **Cache files**: Use hash-based naming for cache keys
- **Batch processing**: `batch_YYYYMMDD_HHMMSS/`

## Quality Optimization

### Choosing Mesh Quality

#### For Different Use Cases

**Prototyping & Concept Development**
```bash
# Fast iteration, visual reference only
mayo-conv input.step -o output.obj --meshing-edge-length 2.0
```
- **Triangle count**: ~5K-20K
- **Use case**: Quick visualization, design reviews
- **Processing time**: < 5 seconds

**Simulation & Analysis**
```bash
# Balanced quality for physics simulation
mayo-conv input.step -o output.obj --meshing-edge-length 0.5
```
- **Triangle count**: ~20K-100K
- **Use case**: FEA, CFD, motion simulation
- **Processing time**: 10-60 seconds

**Visualization & Rendering**
```bash
# High detail for final renders
mayo-conv input.step -o output.obj --meshing-edge-length 0.1
```
- **Triangle count**: ~100K-1M
- **Use case**: Marketing, documentation, VR
- **Processing time**: 1-10 minutes

**3D Printing & Manufacturing**
```bash
# Optimized for printing
mayo-conv input.step -o output.stl --meshing-edge-length 0.2
```
- **Triangle count**: ~50K-200K
- **Use case**: Prototyping, end-use parts
- **Processing time**: 30 seconds - 5 minutes

### Adaptive Quality Settings

```python
def get_optimal_quality(file_size_mb, use_case):
    """Determine optimal mesh quality based on file size and use case."""

    quality_matrix = {
        "prototyping": {"small": 2.0, "medium": 1.5, "large": 1.0},
        "simulation": {"small": 0.5, "medium": 0.3, "large": 0.2},
        "rendering": {"small": 0.1, "medium": 0.05, "large": 0.03},
        "printing": {"small": 0.2, "medium": 0.15, "large": 0.1}
    }

    if file_size_mb < 10:
        size_category = "small"
    elif file_size_mb < 100:
        size_category = "medium"
    else:
        size_category = "large"

    return quality_matrix[use_case][size_category]
```

## Scale Management

### Unit System Conversion

**Common CAD → Target Application Conversions:**

| Source CAD | Target Application | Scale Factor | Example Use |
|------------|-------------------|--------------|-------------|
| millimeters | Blender (meters) | 0.001 | Most CAD → Blender |
| millimeters | Unity (units) | 0.01 | CAD → Unity (1 unit = 1m) |
| millimeters | Unreal (cm) | 0.1 | CAD → Unreal Engine |
| inches | Blender (meters) | 0.0254 | Imperial CAD → Blender |
| millimeters | Gazebo (meters) | 0.001 | Robotics simulation |

**Scale Factor Calculator:**
```python
def calculate_scale_factor(source_unit, target_unit, target_scale=1.0):
    """Calculate scale factor for unit conversion."""

    unit_conversions = {
        ("mm", "m"): 0.001,
        ("cm", "m"): 0.01,
        ("dm", "m"): 0.1,
        ("km", "m"): 1000,
        ("in", "m"): 0.0254,
        ("ft", "m"): 0.3048,
        ("yd", "m"): 0.9144
    }

    key = (source_unit.lower(), target_unit.lower())
    base_factor = unit_conversions.get(key, 1.0)

    return base_factor * target_scale
```

### Scale Validation

```python
def validate_scale(model_bounds, expected_size_range):
    """Validate converted model is in expected size range."""

    min_bounds, max_bounds = expected_size_range

    # Check if model dimensions are within expected range
    for axis in ['x', 'y', 'z']:
        dimension = model_bounds[f'max_{axis}'] - model_bounds[f'min_{axis}']
        if not (min_bounds <= dimension <= max_bounds):
            return False, f"Dimension {axis}={dimension} outside range {min_bounds}-{max_bounds}"

    return True, "Scale validation passed"
```

## Batch Processing

### Efficient Batch Conversion

**Directory-based Processing:**
```bash
#!/bin/bash
# batch_convert.sh
INPUT_DIR="/cad/models"
OUTPUT_DIR="/converted/obj"
QUALITY="0.5"

find "$INPUT_DIR" -name "*.step" -o -name "*.iges" | while read -r file; do
    filename=$(basename "$file")
    output_file="$OUTPUT_DIR/${filename%.*}.obj"

    echo "Converting $file → $output_file"
    mayo-conv "$file" -o "$output_file" --meshing-edge-length "$QUALITY"

    if [ $? -eq 0 ]; then
        echo "✓ Converted successfully"
    else
        echo "✗ Conversion failed"
    fi
done
```

**Parallel Processing:**
```python
import asyncio
import os
from concurrent.futures import ProcessPoolExecutor

async def convert_batch_parallel(input_files, output_dir, quality=0.5, max_workers=4):
    """Convert multiple CAD files in parallel."""

    async def convert_single(input_file):
        output_file = os.path.join(output_dir,
                                 os.path.splitext(os.path.basename(input_file))[0] + '.obj')

        # Run conversion in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=1) as executor:
            await loop.run_in_executor(executor, run_mayo_conversion,
                                     input_file, output_file, quality)

        return output_file

    # Process files concurrently with semaphore for resource control
    semaphore = asyncio.Semaphore(max_workers)

    async def convert_with_semaphore(input_file):
        async with semaphore:
            return await convert_single(input_file)

    tasks = [convert_with_semaphore(f) for f in input_files]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results
```

### Progress Tracking

```python
import tqdm
import asyncio

async def convert_with_progress(input_files, output_dir):
    """Convert files with progress bar."""

    with tqdm.tqdm(total=len(input_files), desc="Converting CAD files") as pbar:
        results = []

        for input_file in input_files:
            result = await convert_single_file(input_file, output_dir)
            results.append(result)
            pbar.update(1)
            pbar.set_postfix(file=os.path.basename(input_file))

        return results
```

## Caching Strategies

### Conversion Cache Implementation

```python
import hashlib
import json
import os
from pathlib import Path

class MayoCache:
    def __init__(self, cache_dir="/cache/mayo"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_key(self, input_file, settings):
        """Generate cache key from file content and conversion settings."""

        # File hash
        with open(input_file, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        # Settings hash
        settings_str = json.dumps(settings, sort_keys=True)
        settings_hash = hashlib.md5(settings_str.encode()).hexdigest()

        return f"{file_hash}_{settings_hash}"

    def get_cached_file(self, cache_key, output_format):
        """Get cached file path if it exists."""

        cache_file = self.cache_dir / f"{cache_key}.{output_format}"
        return cache_file if cache_file.exists() else None

    def cache_file(self, source_file, cache_key, output_format):
        """Cache converted file."""

        cache_file = self.cache_dir / f"{cache_key}.{output_format}"
        if source_file != cache_file:
            import shutil
            shutil.copy2(source_file, cache_file)

        return cache_file

    def is_cache_valid(self, cache_key, output_format):
        """Check if cached file is still valid."""

        cache_file = self.cache_dir / f"{cache_key}.{output_format}"
        if not cache_file.exists():
            return False

        # Check if cache file is newer than input file
        input_file = self.get_input_file_from_key(cache_key)
        if input_file and os.path.getmtime(cache_file) < os.path.getmtime(input_file):
            return False

        return True
```

### Cache Usage in MCP Tools

```python
async def convert_cad_cached(cad_path, output_format="obj", quality=0.5, use_cache=True):
    """Convert CAD file with caching."""

    cache = MayoCache()
    settings = {"format": output_format, "quality": quality}

    cache_key = cache.get_cache_key(cad_path, settings)

    if use_cache:
        cached_file = cache.get_cached_file(cache_key, output_format)
        if cached_file and cache.is_cache_valid(cache_key, output_format):
            return str(cached_file)

    # Perform conversion
    temp_output = await convert_cad_file(cad_path, output_format, quality)

    # Cache result
    if use_cache:
        cached_file = cache.cache_file(temp_output, cache_key, output_format)
        return str(cached_file)

    return temp_output
```

## Error Handling & Recovery

### Robust Conversion Pipeline

```python
async def convert_cad_robust(cad_path, output_format="obj", quality=0.5, max_retries=3):
    """Convert CAD file with error handling and retries."""

    errors = []

    for attempt in range(max_retries):
        try:
            # Try conversion with current settings
            result = await convert_cad_file(cad_path, output_format, quality)
            return result

        except Exception as e:
            error_msg = f"Attempt {attempt + 1} failed: {str(e)}"
            errors.append(error_msg)

            # Progressive quality reduction on retries
            if attempt < max_retries - 1:
                quality *= 1.5  # Reduce quality (higher edge length)
                logger.warning(f"Reducing quality to {quality} for retry")

    # All attempts failed
    raise RuntimeError(f"Conversion failed after {max_retries} attempts. Errors: {errors}")
```

### Fallback Strategies

```python
async def convert_with_fallback(cad_path, preferred_format="obj"):
    """Convert with fallback to alternative formats."""

    formats_to_try = [preferred_format, "stl", "ply"]

    for fmt in formats_to_try:
        try:
            result = await convert_cad_file(cad_path, fmt)
            if fmt != preferred_format:
                logger.info(f"Fell back to {fmt} format (preferred {preferred_format} failed)")
            return result, fmt
        except Exception as e:
            logger.warning(f"Format {fmt} failed: {e}")
            continue

    raise RuntimeError(f"All conversion formats failed for {cad_path}")
```

## Performance Optimization

### Memory Management

**Large File Handling:**
```python
def should_split_large_file(file_size_mb, available_ram_gb):
    """Determine if large file should be split for processing."""

    # Rough heuristic: need ~3x file size in RAM
    required_ram_gb = file_size_mb * 3 / 1024

    return required_ram_gb > available_ram_gb * 0.8  # Leave 20% headroom
```

**Memory-efficient Batch Processing:**
```python
async def convert_batch_memory_efficient(input_files, output_dir, max_concurrent=2):
    """Convert files in small batches to manage memory."""

    results = []

    for i in range(0, len(input_files), max_concurrent):
        batch = input_files[i:i + max_concurrent]

        # Process batch concurrently
        batch_results = await asyncio.gather(
            *[convert_single_file(f, output_dir) for f in batch],
            return_exceptions=True
        )

        results.extend(batch_results)

        # Brief pause between batches to allow memory cleanup
        await asyncio.sleep(0.1)

    return results
```

### Hardware Acceleration

**GPU-accelerated Conversion (Future):**
```python
# Conceptual GPU acceleration for mesh generation
async def convert_with_gpu_acceleration(cad_path, use_gpu=True):
    """Convert using GPU acceleration if available."""

    if use_gpu and torch.cuda.is_available():
        # Use GPU-accelerated mesh generation
        device = torch.device('cuda')
        mesh_generator = GPUMeshGenerator(device=device)

        result = await mesh_generator.convert(cad_path)
    else:
        # Fallback to CPU conversion
        result = await convert_cad_file(cad_path)

    return result
```

## Integration Patterns

### MCP Server Integration

**Error Handling in MCP Tools:**
```python
from mcp import Tool
from pydantic import BaseModel, Field

class CADConversionRequest(BaseModel):
    cad_path: str = Field(..., description="Path to CAD file")
    output_format: str = Field(default="obj", description="Output format")
    quality: str = Field(default="medium", description="Mesh quality")

@Tool()
async def convert_cad_tool(request: CADConversionRequest) -> dict:
    """Convert CAD file to mesh format using Mayo."""

    try:
        # Validate input
        if not os.path.exists(request.cad_path):
            raise ValueError(f"CAD file not found: {request.cad_path}")

        # Convert quality string to numeric
        quality_map = {"low": 2.0, "medium": 0.5, "high": 0.1, "ultra": 0.01}
        quality_value = quality_map.get(request.quality, 0.5)

        # Perform conversion with error handling
        result = await convert_cad_robust(
            request.cad_path,
            request.output_format,
            quality_value
        )

        return {
            "success": True,
            "output_file": result,
            "input_file": request.cad_path,
            "quality": request.quality
        }

    except Exception as e:
        logger.error(f"CAD conversion failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "input_file": request.cad_path
        }
```

### Pipeline Integration

**Automated CAD Processing Pipeline:**
```python
class CADProcessingPipeline:
    def __init__(self, mayo_cache=None, quality_presets=None):
        self.cache = mayo_cache or MayoCache()
        self.quality_presets = quality_presets or QUALITY_PRESETS

    async def process_cad_files(self, input_dir, output_dir, pipeline_config):
        """Process CAD files through complete pipeline."""

        # 1. Discover CAD files
        cad_files = self.discover_cad_files(input_dir)

        # 2. Analyze files (size, complexity)
        file_analysis = await self.analyze_files(cad_files)

        # 3. Determine optimal conversion settings
        conversion_plan = self.create_conversion_plan(file_analysis, pipeline_config)

        # 4. Execute conversions with progress tracking
        results = await self.execute_conversions(conversion_plan, output_dir)

        # 5. Validate results
        validation_results = await self.validate_conversions(results)

        # 6. Generate report
        report = self.generate_processing_report(results, validation_results)

        return report
```

## Monitoring & Metrics

### Conversion Metrics

```python
class ConversionMetrics:
    def __init__(self):
        self.conversions_total = 0
        self.conversions_success = 0
        self.conversions_failed = 0
        self.average_conversion_time = 0
        self.total_processing_time = 0

    def record_conversion(self, success, duration, file_size):
        self.conversions_total += 1

        if success:
            self.conversions_success += 1
        else:
            self.conversions_failed += 1

        # Update average time
        self.total_processing_time += duration
        self.average_conversion_time = self.total_processing_time / self.conversions_total

    def get_metrics(self):
        return {
            "total_conversions": self.conversions_total,
            "success_rate": self.conversions_success / max(self.conversions_total, 1),
            "average_time": self.average_conversion_time,
            "failure_rate": self.conversions_failed / max(self.conversions_total, 1)
        }
```

### Logging Best Practices

```python
import structlog

def setup_structured_logging():
    """Configure structured logging for CAD conversion operations."""

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.WriteLoggerFactory(),
        wrapper_class=structlog.BoundLogger,
        cache_logger_on_first_use=True,
    )

def log_conversion_event(event_type, **kwargs):
    """Log structured CAD conversion events."""

    logger = structlog.get_logger()

    log_data = {
        "event": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        **kwargs
    }

    if event_type == "conversion_started":
        logger.info("CAD conversion started", **log_data)
    elif event_type == "conversion_completed":
        logger.info("CAD conversion completed", **log_data)
    elif event_type == "conversion_failed":
        logger.error("CAD conversion failed", **log_data)
```

---

*Best Practices Version: 1.0*
*Last updated: January 2026*
