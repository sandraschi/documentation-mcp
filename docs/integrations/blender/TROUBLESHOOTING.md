# Blender MCP Troubleshooting Guide

## Connection Issues

### "Failed to connect to Blender"

**Symptoms:**
- Connection timeout errors
- Blender process not starting
- "Connection refused" messages

**Diagnosis:**
```bash
# Check if Blender is running
ps aux | grep blender

# Test MCP server
curl -X GET http://localhost:8765/health

# Check firewall settings
netstat -tlnp | grep 8765

# Verify Blender installation
which blender
blender --version
```

**Solutions:**

1. **Start Blender MCP Server Manually:**
   ```bash
   # Start Blender in background mode
   blender --background --python /path/to/mcp_server.py

   # Or use the MCP CLI
   blender-mcp start --host localhost --port 8765
   ```

2. **Check Firewall Settings:**
   ```bash
   # Linux
   sudo ufw allow 8765

   # Windows Firewall
   # Add inbound rule for port 8765 in Windows Defender Firewall
   ```

3. **Verify Python Path:**
   ```python
   import sys
   print(sys.path)
   import bpy  # Should work in Blender context
   ```

### "Blender not responding"

**Symptoms:**
- Operations hang indefinitely
- Timeout errors
- UI becomes unresponsive

**Diagnosis:**
```bash
# Check system resources
top -p $(pgrep blender)  # Linux
Get-Process blender     # Windows

# Monitor memory usage
free -h                 # Linux
Get-Counter '\Memory\Available MBytes'  # Windows

# Check Blender console for errors
# In Blender: Window → Toggle System Console
```

**Solutions:**

1. **Increase Timeout Values:**
   ```python
   # In MCP client configuration
   client = BlenderClient(timeout=300)  # 5 minutes
   ```

2. **Reduce Scene Complexity:**
   ```python
   # Simplify before processing
   await blender.apply_decimate(ratio=0.5)  # Reduce polygons by half
   await blender.remove_unused_materials()
   ```

3. **Use Background Mode:**
   ```bash
   blender --background --python script.py
   ```

## Import/Export Issues

### "OBJ import fails"

**Symptoms:**
- Import returns empty objects
- Materials not applied
- Geometry appears corrupted

**Diagnosis:**
```bash
# Check OBJ file format
head -20 file.obj
grep -c "^v " file.obj      # Count vertices
grep -c "^f " file.obj      # Count faces
file file.obj              # Check file type

# Validate in text editor
# Check for proper vertex/face format
```

**Common OBJ Issues:**
- Missing vertex normals (`vn`)
- Invalid face indices (referencing non-existent vertices)
- Material file not found (`mtllib`)
- Mixed line endings

**Solutions:**

1. **Validate and Repair OBJ:**
   ```bash
   # Use Blender to re-export
   blender --background --python -c "
   import bpy
   bpy.ops.import_scene.obj(filepath='input.obj')
   bpy.ops.export_scene.obj(filepath='repaired.obj')
   "
   ```

2. **Fix Material Paths:**
   ```python
   # Update material library path
   await blender.set_obj_import_settings(
       use_custom_normals=True,
       import_materials=True,
       material_path_mode='RELATIVE'
   )
   ```

3. **Use Alternative Import:**
   ```python
   # Try FBX format instead
   await blender.import_fbx("file.fbx")
   ```

### "FBX export corrupted"

**Symptoms:**
- Exported files unreadable by other applications
- Missing geometry or materials
- Scale issues

**Diagnosis:**
```bash
# Check Blender version compatibility
blender --version

# Validate export settings
# In Blender: File → Export → FBX (.fbx)
# Check applied transforms, scale, etc.
```

**Solutions:**

1. **Use Correct Export Settings:**
   ```python
   await blender.export_fbx(
       filepath="output.fbx",
       use_selection=False,
       apply_transforms=True,
       apply_scale_options='FBX_SCALE_ALL',
       axis_forward='-Z',
       axis_up='Y'
   )
   ```

2. **Apply Transforms Before Export:**
   ```python
   # Apply all transforms
   await blender.select_all_objects()
   await blender.apply_transforms(rotation=True, scale=True, location=False)
   ```

3. **Check Object Hierarchy:**
   ```python
   # Ensure proper parent-child relationships
   await blender.clear_parent_transforms()
   ```

### "CAD import scale issues"

**Symptoms:**
- Imported CAD models appear tiny or huge
- Measurements don't match expected values

**Diagnosis:**
```python
# Check current unit system
scene_units = await blender.get_scene_units()

# Verify import scale
import_scale = await blender.get_cad_import_scale()
```

**Solutions:**

1. **Set Correct Units:**
   ```python
   # For architectural models (meters)
   await blender.set_scene_unit("meters")

   # For product design (millimeters)
   await blender.set_scene_unit("millimeters")
   ```

2. **Apply Scale During Import:**
   ```python
   # CAD units to Blender units conversion
   scale_factors = {
       "mm_to_m": 0.001,      # millimeters to meters
       "in_to_m": 0.0254,     # inches to meters
       "mm_to_cm": 0.1        # millimeters to centimeters
   }

   await blender.import_cad(
       filepath="model.step",
       scale_factor=scale_factors["mm_to_m"]
   )
   ```

3. **Post-Import Scaling:**
   ```python
   # Scale all imported objects
   imported_objects = await blender.get_recently_imported()
   for obj in imported_objects:
       await blender.scale_object(obj, factor=0.001)
   ```

## Rendering Issues

### "Render fails with GPU errors"

**Symptoms:**
- GPU out of memory errors
- CUDA/OpenCL initialization failures
- Render crashes

**Diagnosis:**
```bash
# Check GPU status
nvidia-smi                    # NVIDIA
clinfo                        # OpenCL

# Verify Blender GPU settings
blender --background --python -c "
import bpy
print('GPU devices:', bpy.context.preferences.addons['cycles'].preferences.devices)
"
```

**Solutions:**

1. **Switch to CPU Rendering:**
   ```python
   await blender.set_render_engine("CYCLES")
   await blender.set_cycles_device("CPU")
   ```

2. **Reduce GPU Memory Usage:**
   ```python
   # Use smaller tile sizes
   await blender.set_render_setting("tile_x", 64)
   await blender.set_render_setting("tile_y", 64)

   # Enable memory optimization
   await blender.set_render_setting("use_persistent_data", False)
   ```

3. **Update GPU Drivers:**
   ```bash
   # NVIDIA (Ubuntu)
   sudo apt update && sudo apt install nvidia-driver-latest

   # AMD GPU drivers depend on hardware
   ```

### "Cycles render too slow"

**Symptoms:**
- Renders take excessively long
- High CPU/GPU usage but slow progress

**Diagnosis:**
```bash
# Check render settings
blender --background --python -c "
import bpy
render = bpy.context.scene.render
print('Samples:', render.cycles.samples)
print('Resolution:', render.resolution_x, 'x', render.resolution_y)
print('Device:', bpy.context.scene.cycles.device)
"
```

**Solutions:**

1. **Optimize Sampling:**
   ```python
   # Enable adaptive sampling
   await blender.set_render_setting("use_adaptive_sampling", True)
   await blender.set_render_setting("adaptive_threshold", 0.01)
   await blender.set_render_setting("samples", 1024)  # Lower max samples
   ```

2. **Use Denoising:**
   ```python
   await blender.set_render_setting("use_denoising", True)
   await blender.set_render_setting("denoiser", "OPENIMAGEDENOISE")
   ```

3. **Optimize Scene:**
   ```python
   # Reduce complexity
   await blender.hide_complex_objects()  # Hide objects not in frame
   await blender.bake_indirect_lighting()  # Bake lightmaps
   ```

### "EEVEE render quality issues"

**Symptoms:**
- Artifacts in renders
- Lighting inconsistencies
- Material appearance problems

**Diagnosis:**
```bash
# Check EEVEE settings
blender --background --python -c "
import bpy
eevee = bpy.context.scene.eevee
print('Samples:', eevee.taa_samples)
print('Shadows:', eevee.shadow_cube_size, eevee.shadow_cascade_size)
"
```

**Solutions:**

1. **Increase Sampling:**
   ```python
   await blender.set_eevee_setting("taa_samples", 128)
   await blender.set_eevee_setting("taa_render_samples", 64)
   ```

2. **Fix Shadow Settings:**
   ```python
   await blender.set_eevee_setting("shadow_cube_size", "1024")
   await blender.set_eevee_setting("shadow_cascade_size", "2048")
   ```

3. **Enable Advanced Features:**
   ```python
   await blender.set_eevee_setting("use_ssr", True)     # Screen space reflections
   await blender.set_eevee_setting("use_sss", True)     # Subsurface scattering
   await blender.set_eevee_setting("use_volumetric", True)  # Volumetric lighting
   ```

## Material and Texture Issues

### "Materials not appearing correctly"

**Symptoms:**
- Materials look flat or wrong color
- Textures not showing
- PBR properties not working

**Diagnosis:**
```python
# Check material setup
materials = await blender.get_all_materials()
for mat in materials:
    nodes = await blender.get_material_nodes(mat)
    print(f"Material {mat.name}: {len(nodes)} nodes")

# Check texture paths
textures = await blender.get_material_textures(mat)
for tex in textures:
    path = await blender.get_texture_filepath(tex)
    print(f"Texture {tex.name}: {path}")
```

**Solutions:**

1. **Fix Node Setup:**
   ```python
   # Ensure Principled BSDF is connected
   await blender.connect_material_nodes(
       material=mat,
       from_node="Principled BSDF",
       from_socket="BSDF",
       to_node="Material Output",
       to_socket="Surface"
   )
   ```

2. **Repair Texture Paths:**
   ```python
   # Update missing texture paths
   await blender.relink_textures(material, old_path="/old/path", new_path="/new/path")
   ```

3. **Convert Legacy Materials:**
   ```python
   # Convert Blender Internal to Cycles
   await blender.convert_legacy_materials()
   ```

### "Texture resolution issues"

**Symptoms:**
- Textures appear blurry or pixelated
- Memory usage high with large textures

**Diagnosis:**
```bash
# Check texture sizes
identify texture.png  # ImageMagick

# Check Blender texture settings
blender --background --python -c "
import bpy
for img in bpy.data.images:
    print(f'{img.name}: {img.size[0]}x{img.size[1]}')
"
```

**Solutions:**

1. **Resize Large Textures:**
   ```python
   await blender.resize_texture(texture, max_size=4096)
   ```

2. **Enable Mipmaps:**
   ```python
   await blender.set_texture_filtering(texture, "LINEAR_MIPMAP_LINEAR")
   await blender.generate_mipmaps(texture)
   ```

3. **Use Texture Compression:**
   ```python
   await blender.set_texture_compression(texture, format="BC7")
   ```

## Animation Issues

### "Animation playback lag"

**Symptoms:**
- Timeline scrubbing is slow
- Playback stutters
- High CPU usage during playback

**Diagnosis:**
```bash
# Check animation complexity
blender --background --python -c "
import bpy
print('Objects:', len(bpy.data.objects))
print('Keyframes:', sum(len(fcurves) for action in bpy.data.actions for fcurves in action.fcurves))
print('Scene FPS:', bpy.context.scene.render.fps)
"
```

**Solutions:**

1. **Simplify Animation:**
   ```python
   # Reduce keyframe density
   await blender.simplify_fcurves(tolerance=0.001)

   # Bake complex animations
   await blender.bake_animation(step=2)  # Every 2nd frame
   ```

2. **Optimize Scene for Playback:**
   ```python
   await blender.set_viewport_quality("LOW")  # Faster viewport
   await blender.disable_complex_modifiers()  # For playback
   ```

3. **Use Proxies:**
   ```python
   # Create proxy objects for complex meshes during animation
   await blender.create_animation_proxies()
   ```

### "Rigging problems"

**Symptoms:**
- Bones not deforming mesh properly
- Weight painting issues
- IK solver failures

**Diagnosis:**
```bash
# Check armature setup
blender --background --python -c "
import bpy
for arm in bpy.data.armatures:
    print(f'Armature {arm.name}: {len(arm.bones)} bones')
    for bone in arm.bones:
        print(f'  {bone.name}: {len(bone.vertex_groups) if hasattr(bone, \"vertex_groups\") else 0} groups')
"
```

**Solutions:**

1. **Fix Weight Painting:**
   ```python
   # Recalculate weights
   await blender.recalculate_vertex_weights(armature, mesh)

   # Normalize weights
   await blender.normalize_vertex_weights(mesh)
   ```

2. **Repair IK Setup:**
   ```python
   # Fix common IK issues
   await blender.validate_ik_chains(armature)
   await blender.repair_broken_ik(armature)
   ```

3. **Optimize Rig:**
   ```python
   # Reduce bone count
   await blender.optimize_bone_hierarchy(armature, max_bones=50)
   ```

## Performance Issues

### "Blender using too much memory"

**Symptoms:**
- System slowdown
- Out of memory crashes
- Blender becomes unresponsive

**Diagnosis:**
```bash
# Monitor memory usage
while true; do
    ps aux | grep blender | grep -v grep | awk '{print $6/1024 " MB"}'
    sleep 5
done
```

**Solutions:**

1. **Limit Undo History:**
   ```python
   await blender.set_preferences({
       "system": {
           "undo_memory_limit": 128,  # MB
           "undo_steps": 16
       }
   })
   ```

2. **Clear Unused Data:**
   ```python
   await blender.purge_orphaned_data()
   await blender.remove_unused_materials()
   await blender.remove_unused_textures()
   ```

3. **Use Memory-Efficient Settings:**
   ```python
   await blender.set_render_setting("use_persistent_data", False)
   await blender.disable_texture_caching()
   ```

### "Large scene loading slow"

**Symptoms:**
- Scene files take long to load
- Blender hangs during load

**Diagnosis:**
```bash
# Check file size
ls -lh scene.blend

# Analyze file contents
blender --background --python -c "
import bpy
bpy.ops.wm.open_mainfile(filepath='scene.blend')
print('Objects:', len(bpy.data.objects))
print('Meshes:', len(bpy.data.meshes))
print('Materials:', len(bpy.data.materials))
print('Textures:', len(bpy.data.textures))
"
```

**Solutions:**

1. **Optimize Before Saving:**
   ```python
   # Clean scene before saving
   await blender.remove_unused_data()
   await blender.pack_external_files()  # Embed textures
   ```

2. **Use Scene Linking:**
   ```python
   # Link rather than append for large scenes
   await blender.link_scene_elements(library_path="library.blend")
   ```

3. **Compress File:**
   ```python
   # Enable file compression
   await blender.set_save_compression(enabled=True, level=6)
   ```

## Python Scripting Issues

### "Script execution fails"

**Symptoms:**
- Python errors in console
- Scripts not running
- Import errors

**Diagnosis:**
```bash
# Check Python path
blender --background --python -c "import sys; print(sys.path)"

# Test script execution
blender --background --python test_script.py

# Check for syntax errors
python -m py_compile script.py
```

**Solutions:**

1. **Fix Import Issues:**
   ```python
   # Add custom paths to Blender Python
   import sys
   sys.path.append("/path/to/custom/modules")
   ```

2. **Handle Blender API Changes:**
   ```python
   # Check Blender version
   import bpy
   if bpy.app.version < (4, 0, 0):
       # Legacy API
       bpy.ops.object.select_all(action='SELECT')
   else:
       # New API
       bpy.ops.object.select_all()
   ```

3. **Debug Script Execution:**
   ```python
   try:
       # Your script here
       pass
   except Exception as e:
       print(f"Error: {e}")
       import traceback
       traceback.print_exc()
   ```

### "Addon installation problems"

**Symptoms:**
- Addons not loading
- Missing dependencies
- Compatibility issues

**Diagnosis:**
```bash
# Check addon directory
ls ~/.config/blender/4.2/scripts/addons/

# Test addon loading
blender --background --python -c "
import bpy
bpy.ops.preferences.addon_enable(module='your_addon')
print('Addon enabled successfully')
"
```

**Solutions:**

1. **Install Dependencies:**
   ```bash
   pip install addon_dependency
   ```

2. **Fix Compatibility:**
   ```python
   # Check version compatibility
   import bpy
   addon_info = {
       "name": "Your Addon",
       "version": (1, 0, 0),
       "blender": (4, 0, 0),
       "category": "Interface"
   }
   ```

3. **Manual Installation:**
   ```bash
   # Copy to addon directory
   cp -r addon ~/.config/blender/4.2/scripts/addons/

   # Enable in Blender
   blender --background --python -c "import bpy; bpy.ops.preferences.addon_enable(module='addon')"
   ```

## System Integration Issues

### "Blender not starting"

**Symptoms:**
- Blender executable not found
- Missing DLLs on Windows
- Library errors on Linux

**Diagnosis:**
```bash
# Windows dependency check
where blender
dumpbin /dependents blender.exe

# Linux library check
ldd /usr/bin/blender

# macOS framework check
otool -L /Applications/Blender.app/Contents/MacOS/Blender
```

**Solutions:**

1. **Install Missing Dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt install libgl1-mesa-glx libxi6 libxrender1 libxext6 libxxf86vm1

   # Windows - Install Visual C++ Redistributables
   # Download from Microsoft website
   ```

2. **Update Graphics Drivers:**
   ```bash
   # NVIDIA
   sudo apt install nvidia-driver-latest

   # AMD
   sudo apt install mesa-vulkan-drivers
   ```

3. **Use Portable Version:**
   ```bash
   # Download portable Blender
   # Extract and run from folder
   ./blender-portable/blender
   ```

### "MCP integration not working"

**Symptoms:**
- MCP server can't control Blender
- Commands not executing
- Connection lost

**Diagnosis:**
```bash
# Test MCP server
curl http://localhost:8765/health

# Check Blender Python console
blender --background --python -c "
import bpy
print('Blender Python working')
"

# Verify MCP addon
blender --background --python -c "
import bpy
addon = bpy.context.preferences.addons.get('mcp_blender')
if addon:
    print('MCP addon found')
else:
    print('MCP addon not found')
"
```

**Solutions:**

1. **Install MCP Addon:**
   ```python
   # Install MCP integration addon
   await blender.install_mcp_addon()
   ```

2. **Configure Network Settings:**
   ```python
   # Set correct host/port
   await blender.configure_mcp_server(host="localhost", port=8765)
   ```

3. **Check Permissions:**
   ```bash
   # Ensure Blender can access network
   sudo setcap cap_net_bind_service+ep blender
   ```

## Recovery Procedures

### Emergency Scene Recovery

```bash
# Recover corrupted .blend file
blender corrupted.blend --recovery

# Extract data from corrupted file
blender --background --python -c "
import bpy
bpy.ops.wm.recover_auto_save(filepath='corrupted.blend')
bpy.ops.wm.save_as_mainfile(filepath='recovered.blend')
"
```

### System Cleanup

```bash
# Clear Blender cache
rm -rf ~/.cache/blender/*
rm -rf ~/.config/blender/4.2/datafiles/*

# Reset preferences
blender --factory-startup

# Clear temporary files
find /tmp -name "*blender*" -type f -delete
```

### Complete Reinstallation

```bash
# Backup custom settings
cp ~/.config/blender/4.2/config ~/.config/blender/4.2/config.backup

# Remove Blender
sudo apt remove blender  # Linux
# Uninstall via Control Panel  # Windows

# Clean remaining files
rm -rf ~/.config/blender
rm -rf ~/.cache/blender

# Reinstall fresh
# Follow installation guide
```

---

*Troubleshooting Version: 2.0*
*Blender Version: 4.2.x*
*MCP Protocol: 2025-11-25*
*Last updated: January 2026*
