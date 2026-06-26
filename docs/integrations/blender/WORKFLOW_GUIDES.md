# Blender MCP Workflow Guides

## Architectural Visualization Pipeline

### Complete Building Creation Workflow

```python
from blender_mcp import BlenderClient
from robotics_mcp import CADConverter
import asyncio

async def create_architectural_visualization(cad_files, output_requirements):
    """Complete architectural visualization pipeline."""

    blender = BlenderClient()
    cad_converter = CADConverter()

    await blender.connect()

    try:
        # Phase 1: CAD Import and Cleanup
        print("Phase 1: Importing CAD files...")
        building_geometry = await import_cad_geometry(cad_files, cad_converter, blender)

        # Phase 2: Material Assignment
        print("Phase 2: Applying materials...")
        materials = await create_architectural_materials(blender)
        await assign_materials_to_building(building_geometry, materials, blender)

        # Phase 3: Environment Setup
        print("Phase 3: Setting up environment...")
        environment = await create_environment(blender, output_requirements["environment"])

        # Phase 4: Lighting Setup
        print("Phase 4: Configuring lighting...")
        lighting_setup = await setup_architectural_lighting(blender, output_requirements["time_of_day"])

        # Phase 5: Camera Setup
        print("Phase 5: Positioning cameras...")
        cameras = await setup_camera_rig(blender, building_geometry, output_requirements["views"])

        # Phase 6: Rendering
        print("Phase 6: Rendering outputs...")
        renders = await render_visualization(blender, cameras, output_requirements["resolution"])

        return {
            "geometry": building_geometry,
            "materials": materials,
            "environment": environment,
            "lighting": lighting_setup,
            "cameras": cameras,
            "renders": renders
        }

    finally:
        await blender.disconnect()

async def import_cad_geometry(cad_files, cad_converter, blender):
    """Import and prepare CAD geometry."""

    imported_objects = []

    for cad_file in cad_files:
        # Convert CAD to mesh
        mesh_file = await cad_converter.convert_cad(
            cad_path=cad_file,
            output_format="obj",
            scale_factor=0.001,  # mm to meters
            mesh_quality="high"
        )

        # Import to Blender
        obj = await blender.import_obj(mesh_file)

        # Initial cleanup
        await blender.apply_transforms(obj)  # Apply any transforms
        await blender.recalculate_normals(obj)  # Fix normals

        imported_objects.append(obj)

    # Group objects
    collection = await blender.create_collection("Building_Geometry")
    for obj in imported_objects:
        await blender.move_to_collection(obj, collection)

    return imported_objects
```

### BIM Data Integration

```python
async def integrate_bim_data(blender_client, bim_data, cad_geometry):
    """Integrate BIM data with CAD geometry."""

    # Create BIM data visualization
    bim_visualization = await create_bim_overlay(blender_client, bim_data)

    # Link BIM data to geometry
    for bim_element in bim_data["elements"]:
        # Find corresponding geometry
        geometry_obj = await find_corresponding_geometry(cad_geometry, bim_element)

        if geometry_obj:
            # Attach BIM metadata
            await attach_bim_metadata(blender_client, geometry_obj, bim_element)

            # Create visual indicators
            await create_bim_visualization(blender_client, geometry_obj, bim_element)

    return bim_visualization

async def create_bim_overlay(blender_client, bim_data):
    """Create visual overlay for BIM data."""

    overlay_objects = []

    # Room/space indicators
    for space in bim_data.get("spaces", []):
        space_indicator = await blender_client.create_object("cube", name=f"Space_{space['id']}")
        await blender_client.set_location(space_indicator, space["centroid"])
        await blender_client.set_scale(space_indicator, space["dimensions"])
        await blender_client.set_material(space_indicator, await create_space_material(blender_client, space))

        overlay_objects.append(space_indicator)

    # Equipment symbols
    for equipment in bim_data.get("equipment", []):
        symbol = await create_equipment_symbol(blender_client, equipment)
        overlay_objects.append(symbol)

    return overlay_objects
```

## Game Development Pipeline

### Character Creation Workflow

```python
async def create_game_character(character_spec, output_requirements):
    """Complete game character creation pipeline."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Base Mesh Creation
        print("Phase 1: Creating base mesh...")
        base_mesh = await create_base_character_mesh(blender, character_spec["body_type"])

        # Phase 2: Topology Optimization
        print("Phase 2: Optimizing topology...")
        await optimize_character_topology(blender, base_mesh)

        # Phase 3: UV Mapping
        print("Phase 3: Creating UV maps...")
        await create_character_uvs(blender, base_mesh)

        # Phase 4: Texturing
        print("Phase 4: Setting up textures...")
        textures = await create_character_textures(blender, character_spec["appearance"])

        # Phase 5: Rigging
        print("Phase 5: Creating rig...")
        rig = await create_character_rig(blender, base_mesh, character_spec["rig_type"])

        # Phase 6: LOD Generation
        print("Phase 6: Creating LOD variants...")
        lods = await generate_character_lods(blender, base_mesh)

        # Phase 7: Export
        print("Phase 7: Exporting character...")
        exported_files = await export_character_package(blender, base_mesh, rig, lods, textures)

        return exported_files

    finally:
        await blender.disconnect()

async def create_base_character_mesh(blender, body_type):
    """Create base character mesh."""

    if body_type == "humanoid":
        # Use makehuman or manual modeling
        base_obj = await create_humanoid_base(blender)
    elif body_type == "creature":
        base_obj = await create_creature_base(blender)
    else:
        base_obj = await blender.create_object("cube", name="Character_Base")

    # Add mirror modifier for symmetry
    await blender.add_modifier(base_obj, "MIRROR")

    # Add subdivision surface
    subdiv_mod = await blender.add_modifier(base_obj, "SUBSURF")
    await blender.set_modifier_property(subdiv_mod, "levels", 2)

    return base_obj
```

### Environment Art Pipeline

```python
async def create_game_environment(environment_spec, asset_library):
    """Create game environment with modular assets."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Terrain Creation
        print("Phase 1: Creating terrain...")
        terrain = await create_terrain_mesh(blender, environment_spec["terrain_size"])

        # Phase 2: Landscape Texturing
        print("Phase 2: Applying terrain materials...")
        await texture_terrain(blender, terrain, environment_spec["biome"])

        # Phase 3: Foliage Placement
        print("Phase 3: Adding vegetation...")
        vegetation = await place_vegetation(blender, terrain, asset_library["foliage"])

        # Phase 4: Structure Placement
        print("Phase 4: Adding structures...")
        structures = await place_structures(blender, terrain, asset_library["buildings"])

        # Phase 5: Lighting Setup
        print("Phase 5: Configuring lighting...")
        lighting = await setup_environment_lighting(blender, environment_spec["time_of_day"])

        # Phase 6: Optimization
        print("Phase 6: Optimizing for performance...")
        await optimize_environment(blender, terrain, vegetation, structures)

        # Phase 7: Export
        print("Phase 7: Exporting environment...")
        exported_files = await export_environment_package(blender, terrain, vegetation, structures)

        return exported_files

    finally:
        await blender.disconnect()

async def create_terrain_mesh(blender, size):
    """Create terrain mesh with displacement."""

    # Create base plane
    terrain = await blender.create_object("plane", size=(size, size))

    # Add displacement modifier
    displace_mod = await blender.add_modifier(terrain, "DISPLACE")
    displacement_texture = await blender.create_texture("terrain_heightmap", "heightmap.png")
    await blender.assign_displacement_texture(displace_mod, displacement_texture)

    # Subdivide for detail
    await blender.add_modifier(terrain, "SUBSURF")

    return terrain
```

### VFX Pipeline Integration

```python
async def create_vfx_shot(vfx_spec, character_rig, environment):
    """Create VFX shot with character and environment."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Scene Setup
        print("Phase 1: Setting up VFX scene...")
        scene = await setup_vfx_scene(blender, character_rig, environment)

        # Phase 2: Animation Setup
        print("Phase 2: Creating animation...")
        animation = await create_character_animation(blender, character_rig, vfx_spec["action"])

        # Phase 3: Effects Creation
        print("Phase 3: Adding visual effects...")
        effects = await add_visual_effects(blender, vfx_spec["effects"])

        # Phase 4: Camera Work
        print("Phase 4: Setting up camera...")
        camera_rig = await create_camera_rig(blender, vfx_spec["camera_movement"])

        # Phase 5: Lighting
        print("Phase 5: Configuring lighting...")
        lighting = await setup_vfx_lighting(blender, vfx_spec["mood"])

        # Phase 6: Rendering
        print("Phase 6: Rendering VFX shot...")
        render_output = await render_vfx_shot(blender, vfx_spec["resolution"], vfx_spec["frames"])

        return render_output

    finally:
        await blender.disconnect()

async def add_visual_effects(blender, effects_spec):
    """Add various visual effects to the scene."""

    effects = []

    for effect in effects_spec:
        if effect["type"] == "particles":
            particle_system = await create_particle_effect(blender, effect)
            effects.append(particle_system)

        elif effect["type"] == "fluid":
            fluid_sim = await create_fluid_effect(blender, effect)
            effects.append(fluid_sim)

        elif effect["type"] == "smoke":
            smoke_sim = await create_smoke_effect(blender, effect)
            effects.append(smoke_sim)

        elif effect["type"] == "force_field":
            force_field = await create_force_field(blender, effect)
            effects.append(force_field)

    return effects
```

## Robotics Simulation Pipeline

### Robot Model Creation

```python
async def create_robot_model(robot_spec, cad_files):
    """Create complete robot model for simulation."""

    blender = BlenderClient()
    cad_converter = CADConverter()

    await blender.connect()

    try:
        # Phase 1: Import Robot Components
        print("Phase 1: Importing robot components...")
        robot_parts = await import_robot_parts(cad_files, cad_converter, blender)

        # Phase 2: Assembly
        print("Phase 2: Assembling robot...")
        robot_assembly = await assemble_robot(blender, robot_parts, robot_spec["assembly"])

        # Phase 3: Rigging
        print("Phase 3: Creating robot rig...")
        robot_rig = await create_robot_rig(blender, robot_assembly, robot_spec["joints"])

        # Phase 4: Physics Setup
        print("Phase 4: Configuring physics...")
        physics_setup = await setup_robot_physics(blender, robot_assembly, robot_spec["physics"])

        # Phase 5: Control System
        print("Phase 5: Adding control system...")
        controls = await add_robot_controls(blender, robot_rig, robot_spec["control"])

        # Phase 6: Export
        print("Phase 6: Exporting robot model...")
        export_files = await export_robot_model(blender, robot_assembly, robot_rig, robot_spec["format"])

        return export_files

    finally:
        await blender.disconnect()

async def import_robot_parts(cad_files, cad_converter, blender):
    """Import and categorize robot parts."""

    parts_by_type = {
        "base": [],
        "links": [],
        "joints": [],
        "end_effectors": [],
        "sensors": []
    }

    for cad_file in cad_files:
        # Convert CAD to mesh
        mesh_file = await cad_converter.convert_cad(
            cad_path=cad_file,
            output_format="obj",
            scale_factor=0.001,
            mesh_quality="high"
        )

        # Import to Blender
        part_obj = await blender.import_obj(mesh_file)

        # Categorize part
        part_type = await categorize_robot_part(part_obj, cad_file)
        parts_by_type[part_type].append(part_obj)

    return parts_by_type
```

### Simulation Environment Setup

```python
async def create_robotics_simulation_environment(environment_spec):
    """Create complete robotics simulation environment."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Workspace Creation
        print("Phase 1: Creating workspace...")
        workspace = await create_simulation_workspace(blender, environment_spec["dimensions"])

        # Phase 2: Obstacles and Fixtures
        print("Phase 2: Adding obstacles...")
        obstacles = await add_simulation_obstacles(blender, environment_spec["obstacles"])

        # Phase 3: Workpieces
        print("Phase 3: Adding workpieces...")
        workpieces = await add_workpieces(blender, environment_spec["workpieces"])

        # Phase 4: Sensors and Cameras
        print("Phase 4: Setting up sensors...")
        sensors = await setup_simulation_sensors(blender, environment_spec["sensors"])

        # Phase 5: Physics World
        print("Phase 5: Configuring physics...")
        physics_world = await configure_physics_world(blender, environment_spec["physics"])

        # Phase 6: Export Simulation
        print("Phase 6: Exporting simulation...")
        simulation_package = await export_simulation_package(blender, workspace, obstacles, workpieces, sensors)

        return simulation_package

    finally:
        await blender.disconnect()

async def setup_simulation_sensors(blender, sensor_spec):
    """Setup various sensors for simulation."""

    sensors = []

    for sensor in sensor_spec:
        if sensor["type"] == "camera":
            camera_sensor = await create_camera_sensor(blender, sensor)
            sensors.append(camera_sensor)

        elif sensor["type"] == "lidar":
            lidar_sensor = await create_lidar_sensor(blender, sensor)
            sensors.append(lidar_sensor)

        elif sensor["type"] == "force_torque":
            force_sensor = await create_force_sensor(blender, sensor)
            sensors.append(force_sensor)

        elif sensor["type"] == "proximity":
            proximity_sensor = await create_proximity_sensor(blender, sensor)
            sensors.append(proximity_sensor)

    return sensors
```

## Motion Graphics Pipeline

### Title Sequence Creation

```python
async def create_title_sequence(title_spec, style_guide):
    """Create animated title sequence."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Typography Setup
        print("Phase 1: Setting up typography...")
        title_text = await create_title_text(blender, title_spec["text"], style_guide["font"])

        # Phase 2: Text Animation
        print("Phase 2: Animating text...")
        text_animation = await animate_title_text(blender, title_text, title_spec["animation"])

        # Phase 3: Background Design
        print("Phase 3: Creating background...")
        background = await create_title_background(blender, style_guide["background"])

        # Phase 4: Effects and Transitions
        print("Phase 4: Adding effects...")
        effects = await add_title_effects(blender, title_text, background, title_spec["effects"])

        # Phase 5: Camera Movement
        print("Phase 5: Setting up camera...")
        camera_work = await create_title_camera(blender, title_spec["camera_movement"])

        # Phase 6: Audio Synchronization
        print("Phase 6: Syncing with audio...")
        audio_sync = await synchronize_with_audio(blender, title_spec["audio_cue"])

        # Phase 7: Rendering
        print("Phase 7: Rendering sequence...")
        final_render = await render_title_sequence(blender, title_spec["duration"], title_spec["resolution"])

        return final_render

    finally:
        await blender.disconnect()

async def animate_title_text(blender, title_text, animation_spec):
    """Create complex text animations."""

    animations = []

    # Letter-by-letter animation
    if animation_spec["type"] == "letter_by_letter":
        letters = await blender.separate_text_into_letters(title_text)

        for i, letter in enumerate(letters):
            # Staggered entrance animation
            delay = i * animation_spec["stagger_delay"]

            # Position animation
            await blender.animate_object_property(
                letter, "location",
                start_frame=delay + 1,
                end_frame=delay + animation_spec["entrance_duration"],
                start_value=(letter.location.x - 10, letter.location.y, letter.location.z),
                end_value=letter.location
            )

            # Scale animation
            await blender.animate_object_property(
                letter, "scale",
                start_frame=delay + 1,
                end_frame=delay + animation_spec["entrance_duration"],
                start_value=(0.1, 0.1, 0.1),
                end_value=(1.0, 1.0, 1.0)
            )

    # Wave animation
    elif animation_spec["type"] == "wave":
        await create_wave_animation(blender, title_text, animation_spec)

    # 3D transformation
    elif animation_spec["type"] == "3d_transform":
        await create_3d_transform_animation(blender, title_text, animation_spec)

    return animations
```

### Logo Animation Pipeline

```python
async def create_logo_animation(logo_spec, brand_guidelines):
    """Create animated logo reveal."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Logo Import
        print("Phase 1: Importing logo...")
        logo_geometry = await import_logo_geometry(blender, logo_spec["source"])

        # Phase 2: Material Setup
        print("Phase 2: Applying brand materials...")
        logo_materials = await apply_brand_materials(blender, logo_geometry, brand_guidelines)

        # Phase 3: Animation Design
        print("Phase 3: Creating logo animation...")
        logo_animation = await design_logo_animation(blender, logo_geometry, logo_spec["style"])

        # Phase 4: Sound Design Sync
        print("Phase 4: Syncing with sound design...")
        audio_reactive = await add_audio_reactivity(blender, logo_animation, logo_spec["audio"])

        # Phase 5: Camera and Lighting
        print("Phase 5: Setting up presentation...")
        presentation = await setup_logo_presentation(blender, logo_geometry, logo_spec["presentation"])

        # Phase 6: Export
        print("Phase 6: Exporting animation...")
        final_output = await export_logo_animation(blender, logo_animation, logo_spec["format"])

        return final_output

    finally:
        await blender.disconnect()

async def design_logo_animation(blender, logo_geometry, animation_style):
    """Design logo animation based on style."""

    if animation_style == "build_up":
        animation = await create_build_up_animation(blender, logo_geometry)
    elif animation_style == "morphing":
        animation = await create_morphing_animation(blender, logo_geometry)
    elif animation_style == "kinetic":
        animation = await create_kinetic_typography_animation(blender, logo_geometry)
    elif animation_style == "minimalist":
        animation = await create_minimalist_animation(blender, logo_geometry)

    return animation
```

## Scientific Visualization Pipeline

### Data Visualization Creation

```python
async def create_scientific_visualization(data_sets, visualization_spec):
    """Create scientific data visualization."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Data Import
        print("Phase 1: Importing scientific data...")
        data_objects = await import_scientific_data(blender, data_sets)

        # Phase 2: Geometry Generation
        print("Phase 2: Generating visualization geometry...")
        viz_geometry = await generate_visualization_geometry(blender, data_objects, visualization_spec["type"])

        # Phase 3: Material Assignment
        print("Phase 3: Applying visualization materials...")
        materials = await create_scientific_materials(blender, visualization_spec["color_scheme"])

        # Phase 4: Animation Setup
        print("Phase 4: Creating data animation...")
        animation = await animate_data_visualization(blender, viz_geometry, data_sets["temporal"])

        # Phase 5: Camera and Lighting
        print("Phase 5: Setting up scientific presentation...")
        presentation = await setup_scientific_presentation(blender, viz_geometry, visualization_spec["view"])

        # Phase 6: Rendering
        print("Phase 6: Rendering scientific visualization...")
        render_output = await render_scientific_visualization(blender, visualization_spec["resolution"])

        return render_output

    finally:
        await blender.disconnect()

async def generate_visualization_geometry(blender, data_objects, viz_type):
    """Generate appropriate geometry for data visualization."""

    if viz_type == "volume_rendering":
        geometry = await create_volume_visualization(blender, data_objects)
    elif viz_type == "surface_plot":
        geometry = await create_surface_plot(blender, data_objects)
    elif viz_type == "particle_system":
        geometry = await create_particle_visualization(blender, data_objects)
    elif viz_type == "vector_field":
        geometry = await create_vector_field_visualization(blender, data_objects)
    elif viz_type == "isosurface":
        geometry = await create_isosurface_visualization(blender, data_objects)

    return geometry
```

### Molecular Visualization

```python
async def create_molecular_visualization(molecular_data, visualization_style):
    """Create molecular structure visualization."""

    blender = BlenderClient()
    await blender.connect()

    try:
        # Phase 1: Atom and Bond Creation
        print("Phase 1: Creating molecular structure...")
        molecular_structure = await create_molecular_geometry(blender, molecular_data)

        # Phase 2: Material Assignment
        print("Phase 2: Applying molecular materials...")
        materials = await assign_atomic_materials(blender, molecular_structure)

        # Phase 3: Animation
        print("Phase 3: Adding molecular motion...")
        motion = await animate_molecular_motion(blender, molecular_structure, molecular_data["dynamics"])

        # Phase 4: Rendering Setup
        print("Phase 4: Configuring scientific rendering...")
        render_setup = await setup_molecular_rendering(blender, visualization_style)

        # Phase 5: Export
        print("Phase 5: Exporting molecular visualization...")
        export_files = await export_molecular_visualization(blender, molecular_structure)

        return export_files

    finally:
        await blender.disconnect()

async def create_molecular_geometry(blender, molecular_data):
    """Create 3D geometry for molecular visualization."""

    atoms = []
    bonds = []

    # Create atoms
    for atom_data in molecular_data["atoms"]:
        atom_obj = await blender.create_object("sphere", name=f"Atom_{atom_data['element']}")
        await blender.set_location(atom_obj, atom_data["position"])
        await blender.set_scale(atom_obj, (atom_data["radius"], atom_data["radius"], atom_data["radius"]))

        atoms.append(atom_obj)

    # Create bonds
    for bond_data in molecular_data["bonds"]:
        bond_obj = await create_bond_geometry(blender, bond_data["atom1"], bond_data["atom2"])
        bonds.append(bond_obj)

    return {"atoms": atoms, "bonds": bonds}
```

## Batch Processing Workflows

### Asset Library Generation

```python
async def generate_asset_library(source_assets, library_spec):
    """Generate complete asset library from source files."""

    blender = BlenderClient()
    await blender.connect()

    try:
        processed_assets = []

        for asset_spec in source_assets:
            print(f"Processing asset: {asset_spec['name']}")

            # Load source asset
            source_obj = await load_asset_source(blender, asset_spec)

            # Process variations
            variations = await generate_asset_variations(blender, source_obj, asset_spec["variations"])

            # Create LODs
            lods = await generate_asset_lods(blender, source_obj, asset_spec["lod_settings"])

            # Generate materials
            materials = await create_asset_materials(blender, asset_spec["material_spec"])

            # Export package
            asset_package = await export_asset_package(blender, source_obj, variations, lods, materials)

            processed_assets.append(asset_package)

        # Create library index
        library_index = await create_asset_library_index(blender, processed_assets, library_spec)

        return processed_assets, library_index

    finally:
        await blender.disconnect()

async def generate_asset_variations(blender, base_asset, variation_spec):
    """Generate asset variations (color, size, style)."""

    variations = []

    for variation in variation_spec:
        # Duplicate base asset
        variation_obj = await blender.duplicate_object(base_asset)

        # Apply variation
        if variation["type"] == "color":
            await apply_color_variation(blender, variation_obj, variation["colors"])
        elif variation["type"] == "size":
            await apply_size_variation(blender, variation_obj, variation["scale"])
        elif variation["type"] == "style":
            await apply_style_variation(blender, variation_obj, variation["parameters"])

        # Rename
        await blender.rename_object(variation_obj, f"{base_asset.name}_{variation['name']}")

        variations.append(variation_obj)

    return variations
```

### Automated Quality Assurance

```python
async def run_asset_quality_checks(asset_library, qa_spec):
    """Run comprehensive quality checks on asset library."""

    blender = BlenderClient()
    await blender.connect()

    try:
        qa_results = []

        for asset in asset_library:
            print(f"Checking asset: {asset['name']}")

            # Load asset
            asset_obj = await blender.load_asset(asset["path"])

            # Run checks
            checks = await perform_quality_checks(blender, asset_obj, qa_spec)

            # Generate report
            report = await generate_asset_report(blender, asset_obj, checks)

            qa_results.append({
                "asset": asset["name"],
                "checks": checks,
                "report": report,
                "passed": all(check["passed"] for check in checks)
            })

        # Generate summary report
        summary = await generate_qa_summary(blender, qa_results)

        return qa_results, summary

    finally:
        await blender.disconnect()

async def perform_quality_checks(blender, asset_obj, qa_spec):
    """Perform detailed quality checks on asset."""

    checks = []

    # Geometry checks
    if qa_spec.get("check_geometry"):
        geometry_checks = await check_geometry_quality(blender, asset_obj)
        checks.extend(geometry_checks)

    # Material checks
    if qa_spec.get("check_materials"):
        material_checks = await check_material_quality(blender, asset_obj)
        checks.extend(material_checks)

    # UV checks
    if qa_spec.get("check_uvs"):
        uv_checks = await check_uv_quality(blender, asset_obj)
        checks.extend(uv_checks)

    # LOD checks
    if qa_spec.get("check_lods"):
        lod_checks = await check_lod_quality(blender, asset_obj)
        checks.extend(lod_checks)

    # Performance checks
    if qa_spec.get("check_performance"):
        performance_checks = await check_performance_metrics(blender, asset_obj)
        checks.extend(performance_checks)

    return checks
```

---

*Workflow Guides Version: 2.0*
*Blender Version: 4.2.x*
*Last updated: January 2026*
