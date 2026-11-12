# MakerCraft

**Version**: v0.1.0 — Hardware Workshop, 3D Printing & CNC G-Code Studio.
**Repository**: [`d:\Dev\repos\makercraft`](file:///d:/Dev/repos/makercraft) | [GitHub: sandraschi/makercraft](https://github.com/sandraschi/makercraft)
**Control Port**: `14130` (`makercraft --control 14130`)
**Parent Suite**: Sovereign Craft Suite / Hardware

---

## Features & Architecture

```
makercraft-core (G-Code Parser / Slicer Interface / Serial Controller)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
 makercraft-mcp (L1/L2)                        makercraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 3D Print & Toolhead Canvas)
```

- **Consolidates Fleet Repos**: `bus-pirate-mcp`, `jtag-swd-mcp`, `logic-analyzer-mcp`.
- Real-time 3D printer serial stream monitoring, OctoPrint/Klipper API bridge.
- G-code previewer and automated toolpath optimization.
