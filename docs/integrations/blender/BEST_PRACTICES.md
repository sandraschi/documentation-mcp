# Blender MCP Best Practices

## Performance Optimization

### Scene Setup

#### Startup Configuration

**Optimal Blender Launch Settings:**
```bash
# For headless/server operation
blender --background \
        --python-use-system-env \
        --enable-autoexec \
        --factory-startup \
        --disable-autoexec \
        --disable-crash-handler
```

**Memory Configuration:**
```python
# Set optimal memory limits
await blender.set_preferences({
    "system": {
        "memory_cache_limit": 4096,    # MB for texture cache
        "undo_memory_limit": 256,      # MB for undo history
        "undo_steps": 16,              # Limit undo steps
        "sequencer_disk_cache_limit": 1024  # MB for video cache
    }
})
```

#### Scene Units and Scale

**Consistent Unit System:**
```python
# Always use metric system for consistency
await blender.set_scene_unit("meters")

# Set appropriate scale for your use case
scale_settings = {
    "architectural": 1.0,      # 1 unit = 1 meter
    "product_design": 0.001,   # 1 unit = 1 mm
    "games": 0.01             # 1 unit = 1 cm (Unity compatible)
}
```

### Object Management

#### Naming Conventions

**Standard Naming Scheme:**
```
[Type]_[Name]_[Variant]_[Suffix]

Examples:
GEO_Building_A_High
MAT_Concrete_Gray_Base
TEX_Bricks_Diffuse_4K
COL_Architecture_Exterior
```

**Automated Naming:**
```python
def generate_object_name(obj_type, base_name, variant=None, suffix=None):
    """Generate consistent object names."""
    parts = [obj_type, base_name]
    if variant:
        parts.append(variant)
    if suffix:
        parts.append(suffix)
    return "_".join(parts)

# Usage
building_name = generate_object_name("GEO", "Warehouse", "A", "High")
material_name = generate_object_name("MAT", "Metal", "Brushed")
```

#### Object Organization

**Collection Hierarchy:**
```
Scene Root
├── GEO_Geometry
│   ├── GEO_Buildings
│   ├── GEO_Terrain
│   └── GEO_Props
├── MAT_Materials
├── LIGHT_Lighting
├── CAM_Cameras
└── HIDDEN_Utility
```

**Automated Organization:**
```python
async def organize_scene_objects(blender_client):
    """Automatically organize scene objects into collections."""

    # Create main collections
    collections = {}
    for category in ["GEO", "MAT", "LIGHT", "CAM", "HIDDEN"]:
        collections[category] = await blender_client.create_collection(f"{category}_Root")

    # Move objects to appropriate collections
    objects = await blender_client.get_all_objects()
    for obj in objects:
        category = obj.name.split("_")[0] if "_" in obj.name else "GEO"
        if category in collections:
            await blender_client.move_to_collection(obj, collections[category])
```

### Mesh Optimization

#### Topology Optimization

**Automatic Mesh Cleanup:**
```python
async def optimize_mesh_topology(blender_client, obj, target_tris=None):
    """Optimize mesh topology for performance."""

    # Remove duplicate vertices
    await blender_client.apply_merge_by_distance(merge_distance=0.001)

    # Fill holes
    await blender_client.fill_mesh_holes(max_edges=4)

    # Limited dissolve for cleaner topology
    await blender_client.apply_limited_dissolve(angle_limit=5.0)

    # Reduce triangles if target specified
    if target_tris:
        current_tris = await blender_client.get_triangle_count(obj)
        if current_tris > target_tris:
            reduction_ratio = target_tris / current_tris
            await blender_client.apply_decimate(ratio=reduction_ratio)

    # Recalculate normals
    await blender_client.recalculate_normals(outside=True)
```

#### LOD Generation

**Automated LOD Creation:**
```python
async def create_lod_chain(blender_client, high_poly_obj, lod_levels=3):
    """Create LOD chain from high-poly object."""

    lod_objects = [high_poly_obj]  # LOD0 is original

    base_tris = await blender_client.get_triangle_count(high_poly_obj)

    for level in range(1, lod_levels + 1):
        # Calculate target triangle count (exponential reduction)
        target_tris = int(base_tris * (0.5 ** level))

        # Duplicate and decimate
        lod_obj = await blender_client.duplicate_object(high_poly_obj, linked=False)
        await blender_client.apply_decimate(lod_obj, target_tris=target_tris)

        # Rename
        await blender_client.rename_object(lod_obj, f"{high_poly_obj.name}_LOD{level}")

        lod_objects.append(lod_obj)

    return lod_objects
```

#### UV Optimization

**Automatic UV Unwrapping:**
```python
async def optimize_uv_layout(blender_client, obj):
    """Create optimized UV layout."""

    # Smart UV unwrap
    await blender_client.add_uv_unwrap(method="SMART", margin=0.02)

    # Pack islands efficiently
    await blender_client.pack_uv_islands(margin=0.01, rotate=True)

    # Generate lightmap UV if needed
    if await blender_client.needs_lightmap_uv(obj):
        await blender_client.add_lightmap_uv(obj, resolution=512)
```

### Material Optimization

#### PBR Material Setup

**Standardized PBR Materials:**
```python
async def create_standard_pbr_material(blender_client, name, **properties):
    """Create standardized PBR material."""

    material = await blender_client.create_material(name, material_type="principled")

    # Default PBR values
    defaults = {
        "base_color": (0.8, 0.8, 0.8, 1.0),
        "metallic": 0.0,
        "roughness": 0.5,
        "specular": 0.5,
        "emission_color": (0.0, 0.0, 0.0),
        "emission_strength": 0.0
    }

    # Override with provided properties
    defaults.update(properties)

    # Apply properties
    for prop, value in defaults.items():
        await blender_client.set_material_property(material, prop, value)

    return material
```

#### Texture Optimization

**Texture Compression and Mipmaps:**
```python
async def optimize_textures(blender_client, material):
    """Optimize textures for performance."""

    textures = await blender_client.get_material_textures(material)

    for texture in textures:
        # Enable compression
        await blender_client.set_texture_compression(texture, format="BC7")

        # Generate mipmaps
        await blender_client.generate_mipmaps(texture)

        # Set filtering
        await blender_client.set_texture_filtering(texture, "LINEAR_MIPMAP_LINEAR")
```

### Rendering Optimization

#### Cycles Optimization

**GPU Acceleration Setup:**
```python
async def setup_cycles_gpu(blender_client):
    """Configure Cycles for optimal GPU rendering."""

    # Set Cycles as render engine
    await blender_client.set_render_engine("CYCLES")

    # Detect and configure GPU
    gpu_devices = await blender_client.get_available_compute_devices()

    if gpu_devices:
        # Prefer CUDA over OpenCL
        cuda_devices = [d for d in gpu_devices if "CUDA" in d["type"]]
        if cuda_devices:
            await blender_client.set_compute_device("CUDA", cuda_devices[0])
        else:
            # Fallback to OpenCL
            await blender_client.set_compute_device("OPENCL", gpu_devices[0])

        await blender_client.set_cycles_device("GPU")
    else:
        print("No GPU detected, using CPU")
        await blender_client.set_cycles_device("CPU")
```

#### Render Settings Optimization

**Adaptive Sampling:**
```python
async def configure_adaptive_sampling(blender_client, target_noise=0.01):
    """Configure adaptive sampling for optimal quality/performance."""

    # Enable adaptive sampling
    await blender_client.set_render_setting("use_adaptive_sampling", True)

    # Set quality thresholds
    await blender_client.set_render_setting("adaptive_threshold", target_noise)
    await blender_client.set_render_setting("samples", 4096)  # Max samples
    await blender_client.set_render_setting("adaptive_min_samples", 64)

    # Denoising
    await blender_client.set_render_setting("use_denoising", True)
    await blender_client.set_render_setting("denoiser", "OPENIMAGEDENOISE")
```

#### Scene Lighting Optimization

**Efficient Lighting Setup:**
```python
async def setup_efficient_lighting(blender_client, scene_type="interior"):
    """Setup lighting optimized for performance."""

    lighting_configs = {
        "interior": {
            "hdri_rotation": 0,
            "hdri_strength": 0.8,
            "rim_light": True,
            "fill_light": True
        },
        "exterior": {
            "sun_energy": 5.0,
            "sky_texture": True,
            "rim_light": False,
            "fill_light": False
        }
    }

    config = lighting_configs.get(scene_type, lighting_configs["interior"])

    # HDRI environment
    if "hdri_strength" in config:
        await blender_client.set_hdri_environment("/path/to/hdri.hdr")
        await blender_client.set_hdri_strength(config["hdri_strength"])

    # Sun light for exteriors
    if "sun_energy" in config:
        sun = await blender_client.create_light("sun", type="SUN",
                                               energy=config["sun_energy"])
        await blender_client.set_light_rotation(sun, (-45, 0, 45))

    # Additional lights
    if config.get("rim_light"):
        rim = await blender_client.create_light("rim", type="AREA",
                                              energy=2.0, color=(0.9, 0.8, 0.7))
        await blender_client.set_light_location(rim, (5, -5, 2))

    if config.get("fill_light"):
        fill = await blender_client.create_light("fill", type="AREA",
                                               energy=1.0, color=(0.7, 0.8, 0.9))
        await blender_client.set_light_location(fill, (-3, 3, 1))
```

### Animation Optimization

#### Keyframe Reduction

**Automatic Keyframe Optimization:**
```python
async def optimize_animation_keyframes(blender_client, obj, tolerance=0.001):
    """Remove redundant keyframes from animation."""

    # Get animation curves
    fcurves = await blender_client.get_animation_curves(obj)

    for fcurve in fcurves:
        # Simplify curve by removing points within tolerance
        await blender_client.simplify_fcurve(fcurve, tolerance=tolerance)

        # Bake animation to reduce complexity
        await blender_client.bake_animation(obj, start_frame=1, end_frame=250,
                                          step=1, bake_types={'OBJECT'})
```

#### Rig Optimization

**Efficient Rig Setup:**
```python
async def create_optimized_rig(blender_client, character_mesh):
    """Create optimized character rig."""

    # Create armature
    armature = await blender_client.create_armature("character_rig")

    # Add bones with proper hierarchy
    bones = [
        ("root", None, (0, 0, 0)),
        ("spine", "root", (0, 0, 0.8)),
        ("chest", "spine", (0, 0, 0.3)),
        ("head", "chest", (0, 0, 0.2)),
        ("arm.L", "chest", (-0.2, 0, 0.1)),
        ("forearm.L", "arm.L", (-0.3, 0, 0)),
        ("hand.L", "forearm.L", (-0.2, 0, 0)),
    ]

    for bone_name, parent_name, location in bones:
        await blender_client.add_bone_to_armature(armature, bone_name,
                                                parent_name, location)

    # Setup IK constraints for better performance
    await blender_client.add_ik_constraint(armature, "hand.L", "arm.L", chain_length=2)

    # Parent mesh to armature
    await blender_client.parent_object_to_armature(character_mesh, armature)

    return armature
```

### Pipeline Integration

#### Automated Import Pipeline

**CAD to Blender Pipeline:**
```python
async def cad_to_blender_pipeline(cad_files, blender_client, mayo_client):
    """Complete CAD to Blender pipeline with optimization."""

    imported_objects = []

    for cad_file in cad_files:
        # Convert CAD using Mayo
        mesh_file = await mayo_client.convert_cad(
            cad_path=cad_file,
            output_format="obj",
            scale_factor=0.001,  # mm to meters
            mesh_quality="high"
        )

        # Import to Blender
        obj = await blender_client.import_obj(mesh_file)

        # Optimize imported geometry
        await optimize_mesh_topology(blender_client, obj, target_tris=50000)

        # Setup materials
        material = await create_standard_pbr_material(blender_client,
                                                    f"{obj.name}_mat")
        await blender_client.assign_material(obj, material)

        imported_objects.append(obj)

    # Create organized collection
    collection = await blender_client.create_collection("CAD_Imports")
    for obj in imported_objects:
        await blender_client.move_to_collection(obj, collection)

    return imported_objects
```

#### Batch Processing

**Efficient Batch Operations:**
```python
async def batch_process_scenes(scene_files, operations, max_concurrent=4):
    """Process multiple scene files efficiently."""

    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def process_scene(scene_file):
        async with semaphore:
            blender = BlenderClient()
            await blender.connect()

            try:
                await blender.load_scene(scene_file)

                for operation in operations:
                    if operation["type"] == "optimize":
                        await optimize_scene(blender, operation["params"])
                    elif operation["type"] == "render":
                        await render_scene(blender, operation["params"])

                # Save processed scene
                output_file = scene_file.replace(".blend", "_processed.blend")
                await blender.save_scene(output_file)

                results.append({"file": scene_file, "status": "success"})

            except Exception as e:
                results.append({"file": scene_file, "status": "error", "error": str(e)})

            finally:
                await blender.disconnect()

    # Process all scenes concurrently (with semaphore limit)
    tasks = [process_scene(scene) for scene in scene_files]
    await asyncio.gather(*tasks, return_exceptions=True)

    return results
```

### Memory Management

#### Large Scene Handling

**Memory-Efficient Operations:**
```python
async def process_large_scene(blender_client, scene_file, memory_limit_gb=8):
    """Process large scenes with memory constraints."""

    # Monitor memory usage
    initial_memory = await blender_client.get_memory_usage()

    # Load scene in background mode
    await blender_client.load_scene_background(scene_file)

    # Process in chunks to manage memory
    objects = await blender_client.get_all_objects()
    chunk_size = 50

    for i in range(0, len(objects), chunk_size):
        chunk = objects[i:i + chunk_size]

        # Process chunk
        for obj in chunk:
            await optimize_mesh_topology(blender_client, obj)

        # Check memory usage
        current_memory = await blender_client.get_memory_usage()
        memory_used_gb = (current_memory - initial_memory) / 1024 / 1024 / 1024

        if memory_used_gb > memory_limit_gb * 0.8:
            # Save progress and clear memory
            await blender_client.save_scene(scene_file.replace(".blend", "_temp.blend"))
            await blender_client.purge_orphaned_data()

            # Reset memory baseline
            initial_memory = await blender_client.get_memory_usage()

    # Final save
    await blender_client.save_scene(scene_file.replace(".blend", "_optimized.blend"))
```

#### Out-of-Core Processing

**Processing Scenes Larger Than RAM:**
```python
async def process_scene_out_of_core(scene_file, temp_dir, max_memory_gb=4):
    """Process scenes larger than available RAM."""

    # Create processing plan
    plan = await analyze_scene_complexity(scene_file)

    # Split scene into manageable chunks
    chunks = await split_scene_by_collections(scene_file, temp_dir)

    processed_chunks = []

    for chunk_file in chunks:
        # Process each chunk separately
        blender = BlenderClient(memory_limit=max_memory_gb)
        await blender.connect()

        await blender.load_scene(chunk_file)
        await optimize_scene(blender, {})
        processed_file = chunk_file.replace(".blend", "_processed.blend")
        await blender.save_scene(processed_file)

        await blender.disconnect()
        processed_chunks.append(processed_file)

    # Merge processed chunks
    final_scene = await merge_scene_chunks(processed_chunks, temp_dir)

    return final_scene
```

### Quality Assurance

#### Automated Scene Validation

**Comprehensive Scene Checks:**
```python
async def validate_scene_quality(blender_client, quality_checks):
    """Run comprehensive quality checks on scene."""

    issues = []

    # Check for common problems
    if quality_checks.get("check_orphaned_objects"):
        orphaned = await blender_client.find_orphaned_objects()
        if orphaned:
            issues.append(f"Found {len(orphaned)} orphaned objects")

    if quality_checks.get("check_missing_materials"):
        missing_mat = await blender_client.find_objects_without_materials()
        if missing_mat:
            issues.append(f"Found {len(missing_mat)} objects without materials")

    if quality_checks.get("check_mesh_problems"):
        mesh_issues = await blender_client.validate_all_meshes()
        for obj_name, problems in mesh_issues.items():
            if problems:
                issues.append(f"{obj_name}: {', '.join(problems)}")

    if quality_checks.get("check_texture_resolution"):
        oversized_textures = await blender_client.find_oversized_textures(max_size_mb=100)
        if oversized_textures:
            issues.append(f"Found {len(oversized_textures)} oversized textures")

    if quality_checks.get("check_performance"):
        perf_issues = await blender_client.analyze_performance_bottlenecks()
        issues.extend(perf_issues)

    return issues
```

#### Automated Testing

**Scene Testing Framework:**
```python
async def run_scene_tests(blender_client, test_suite):
    """Run automated tests on scene."""

    test_results = []

    for test in test_suite:
        try:
            if test["type"] == "render_test":
                # Test rendering at specified resolution
                await blender_client.set_render_resolution(
                    test["width"], test["height"]
                )
                start_time = time.time()
                await blender_client.render_frame("/tmp/test_render.png")
                render_time = time.time() - start_time

                if render_time > test.get("max_time", 60):
                    test_results.append({
                        "test": test["name"],
                        "status": "failed",
                        "reason": f"Render took {render_time:.1f}s (max {test['max_time']}s)"
                    })
                else:
                    test_results.append({
                        "test": test["name"],
                        "status": "passed",
                        "render_time": render_time
                    })

            elif test["type"] == "physics_test":
                # Test physics simulation
                await blender_client.setup_physics_simulation(test["params"])
                await blender_client.run_physics_simulation(test["duration"])

                # Check for errors
                errors = await blender_client.get_physics_errors()
                if errors:
                    test_results.append({
                        "test": test["name"],
                        "status": "failed",
                        "reason": f"Physics errors: {errors}"
                    })
                else:
                    test_results.append({
                        "test": test["name"],
                        "status": "passed"
                    })

        except Exception as e:
            test_results.append({
                "test": test["name"],
                "status": "error",
                "reason": str(e)
            })

    return test_results
```

### Workflow Automation

#### Template-Based Scene Creation

**Scene Templates:**
```python
async def create_scene_from_template(blender_client, template_name, parameters):
    """Create scene from predefined template."""

    templates = {
        "architectural_interior": {
            "camera": {"type": "perspective", "lens": 35},
            "lighting": "studio_hdri",
            "ground": True,
            "units": "meters"
        },
        "product_showcase": {
            "camera": {"type": "orthographic", "scale": 1.0},
            "lighting": "product_studio",
            "turntable": True,
            "units": "millimeters"
        },
        "game_level": {
            "camera": {"type": "game", "fov": 90},
            "lighting": "realtime",
            "collision": True,
            "units": "centimeters"
        }
    }

    if template_name not in templates:
        raise ValueError(f"Unknown template: {template_name}")

    template = templates[template_name]

    # Apply template settings
    await blender_client.set_scene_unit(template["units"])

    # Setup camera
    camera_config = template["camera"]
    camera = await blender_client.create_camera("main_camera")
    if camera_config["type"] == "perspective":
        await blender_client.set_camera_lens(camera, camera_config["lens"])
    elif camera_config["type"] == "orthographic":
        await blender_client.set_camera_orthographic_scale(camera, camera_config["scale"])

    # Setup lighting
    await setup_lighting_from_template(blender_client, template["lighting"])

    # Add optional elements
    if template.get("ground"):
        ground = await blender_client.create_object("plane", size=20.0)
        await blender_client.set_location(ground, (0, 0, 0))

    if template.get("turntable"):
        await create_turntable_animation(blender_client)

    return template
```

#### Custom Pipeline Integration

**CI/CD Integration:**
```python
async def setup_blender_ci_pipeline(project_config):
    """Setup automated Blender processing in CI/CD."""

    # Configure headless Blender
    blender_config = {
        "executable": "/opt/blender/blender",
        "background": True,
        "python_path": "/usr/bin/python3",
        "memory_limit": "8GB",
        "timeout": 3600
    }

    # Define processing pipeline
    pipeline_steps = [
        {"name": "load_scene", "params": {"file": project_config["scene_file"]}},
        {"name": "validate_scene", "params": project_config["validation_rules"]},
        {"name": "optimize_assets", "params": project_config["optimization_settings"]},
        {"name": "run_tests", "params": project_config["test_suite"]},
        {"name": "render_outputs", "params": project_config["render_settings"]},
        {"name": "export_assets", "params": project_config["export_formats"]}
    ]

    # Generate CI configuration
    ci_config = generate_ci_workflow(blender_config, pipeline_steps)

    return ci_config
```

---

*Best Practices Version: 2.0*
*Blender Version: 4.2.x*
*Last updated: January 2026*
