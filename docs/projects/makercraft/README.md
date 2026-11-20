# MakerCraft

**Version**: v0.2.0 — Pure-Rust ArtCraft Digital Fabrication Bench & Instrument Studio.
**Repository**: [`d:\Dev\repos\makercraft`](file:///d:/Dev/repos/makercraft) | [GitHub: sandraschi/makercraft](https://github.com/sandraschi/makercraft)
**Parent Suite**: Storytold ArtCraft / Hardware

---

## Features & Architecture

```
makercraft-hal  (Moonraker HTTP, GRBL serial, Bus Pirate, SCPI/USBTMC, sigrok)
      │
      ▼
makercraft-core (G-code Parser, Safety Linter, Profiles, Command::dispatch, 8 Skills)
      │
      ├──► makercraft-mcp (L2: CLI + MCP 2024-11-05 stdio, 18 tools + skill:// resources)
      └──► makercraft-app (L3: egui 0.37 Workstation + makercraft-cli)
```

- **Consolidates 7 Bench Instrument Repos**: `oscilloscope-mcp`, `logic-analyzer-mcp`, `multimeter-mcp`, `function-generator-mcp`, `spectrum-analyzer-mcp`, `jtag-swd-mcp`, and `bus-pirate-mcp`.
- **G-Code Parser & Safety Linter**: Modal `G0/G1`, `G90/G91`, `G20/G21`, `G2/G3` arc notices, envelope gates, rapid-plunge hard errors, and `gcode_check` CI gate (exit 2 when unsafe).
- **Interactive Workshop & Pictorial Studio**: 2-bay Maker's Workshop & ESD Workbench panorama (`Workshop` tab) plus individual vector hardware cards (`Machines` & `Instruments` tabs).
- **8 Bundled Skills & Local-First AI Chat (`Ctrl+J`)**: Embedded `SKILL.md` guides served over MCP `resources/list` + `makercraft_skill_read`, CLI `skills`, and used as the preprompt for the Ollama/LM Studio/OpenAI-compatible Chat Dock.
- **Vienna Makerspaces & Buying Guide**: Dedicated `Vienna & Buying` tab covering Metalab, Happylab, Maker Austria, and hardware buying advice.
