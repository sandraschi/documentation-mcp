# Fleet Exchange Depot (`_exchange/`)

Cross-MCP file exchange directory. Every fleet server writes exports here and reads imports from here.

## Directory Layout

```
D:\Dev\repos\_exchange\
├── cad/        # DXF, STEP, STL — qcad-mcp → freecad-mcp
├── models/     # GLB, FBX, OBJ — blender-mcp → godot-mcp / resonite-mcp
├── cfd/        # CSV velocity fields — freecad-mcp (FluidX3D) → godot-mcp
├── avatars/    # VRM, FBX — blender-mcp / avatar-mcp → resonite-mcp / vrchat-mcp
└── robots/     # URDF, STL, STEP — freecad-mcp → robotics-mcp / yahboom-mcp / godot-mcp
```

## Convention

1. **Producers** write to the appropriate subdirectory with a timestamped filename:
   `D:\Dev\repos\_exchange\models\robot_20260519_172500.glb`

2. **Consumers** read from the exchange depot. Use the latest file matching the expected extension.

3. **Cleanup** is the consumer's responsibility. After successful import, delete the source file.

4. **Fallback** — when no explicit output path is given, default to `_exchange/{category}/`.

## Pipeline Examples

### CAD → 3D → Game
```powershell
# qcad-mcp exports DXF to cad/
# freecad-mcp reads cad/, exports STL to models/
# godot-mcp reads models/, imports STL/GLB
```

### CFD Visualization
```powershell
# freecad-mcp runs FluidX3D, writes CSV to cfd/
# godot-mcp reads cfd/, loads as velocity field
```

### Avatar → VR
```powershell
# blender-mcp exports VRM/GLB to avatars/
# resonite-mcp reads avatars/, injects into world
```

## Server Integration Status

| Server | Produces | Consumes | Adopted |
|--------|---------|----------|---------|
| qcad-mcp | DXF, STL | — | pending |
| freecad-mcp | STL, STEP, OBJ, IFC | DXF, STL | pending |
| blender-mcp | GLB, FBX, VRM | STL, OBJ, DXF | pending |
| godot-mcp | HTML5 | STL, GLB, OBJ, CSV | pending |
| resonite-mcp | — | GLB, VRM, PLY | pending |
| avatar-mcp | VRM | — | pending |
| yahboom-mcp | — | STL, URDF | pending |
| robotics-mcp | — | STL, STEP | pending |
