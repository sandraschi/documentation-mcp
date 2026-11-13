# GameCraft

**Version**: v0.1.0 — Natural-Language to Godot 4 Game Development Studio.
**Repository**: [`d:\Dev\repos\gamecraft`](file:///d:/Dev/repos/gamecraft) | [GitHub: sandraschi/gamecraft](https://github.com/sandraschi/gamecraft)
**Parent Suite**: Sovereign Craft Suite / Gaming

---

## Features & Architecture

```
gamecraft-core (Scene Graph Generator / GDScript Synthesizer / Asset Assembler)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
 gamecraft-mcp (L1/L2)                         gamecraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 Game Inspector & Launcher)
```

- **One-Sentence Generation**: `gamecraft-cli new --prompt "a snowy mountain pass at dusk"`.
- **Godot 4 Native Export**: Produces valid `.godot` project files, `.tscn` node trees, and GDScript scripts.
- **MCP Scene Tools**: `scene_lint`, `spatial_query`, `scene_inspect`, `export_scene`.
