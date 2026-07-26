# SOTA 2026 Open-Source ASIC/VLSI CAD Pipeline

**Status**: Active  
**Audience**: chip-design-mcp, future silicon repos  
**Last Updated**: 2026-05-27

## Abstract

The fleet standard for open-source chip design leverages the mature
ecosystem of open-source EDA tools (Yosys, OpenLane, cocotb, Magic, netgen)
and the SkyWater 130nm open PDK. The `chip-design-mcp` repo serves as
the MCP orchestration layer — it does not reimplement any EDA algorithm;
it coordinates subprocess execution and exposes a unified tool interface.

## Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      chip-design-mcp (FastMCP 3.2)               │
│  port 11022  │  REST + MCP HTTP/SSE  │  28 tools / 6 domains    │
└──────────────┬───────────────────────┬───────────────────────────┘
               │                       │
    ┌──────────▼──────┐     ┌──────────▼──────────────┐
    │  Headless CLI    │     │  Docker (OpenLane)       │
    │  yosys, iverilog │     │  openroad, magic, klayout│
    │  magic, netgen   │     │  full RTL-to-GDSII flow  │
    └─────────────────┘     └─────────────────────────┘
```

## Tool Chain (Approved)

| Stage | Tool | License | Role |
|-------|------|---------|------|
| RTL Simulation | **cocotb** + **iverilog** | BSD / GPLv2 | Python testbenches, Verilog simulation |
| Synthesis | **Yosys** | ISC | RTL → gate-level netlist |
| Place & Route | **OpenLane** (wraps OpenROAD) | Apache 2.0 | Automated RTL-to-GDSII |
| STA | **OpenSTA** | GPLv3 | Static timing analysis |
| DRC | **Magic** | MIT-style | Design rule checking |
| LVS | **netgen** | GPLv2 | Layout vs schematic |
| Layout View | **KLayout** | GPLv3 | GDSII viewer (optional) |

## PDKs (Approved)

| PDK | Node | Source | Install |
|-----|------|--------|---------|
| **SkyWater 130nm** | 130nm | Google/SkyWater | `volare enable --pdk sky130 0bbdd5` |
| **GF180MCU** | 180nm | GlobalFoundries | `volare enable --pdk gf180mcu` |
| **IHP SG13G2** | 130nm BiCMOS | IHP | `volare enable --pdk ihp-sg13g2` |

### What a PDK Contains

A Process Design Kit is the bridge between your design and the foundry —
a collection of files modeling the manufacturing process:

- **Standard cell library**: Pre-characterized logic gates (AND, OR, DFF)
  with timing models (.lib), GDSII layout, LEF abstracts, Verilog models.
  SkyWater HD library: ~500 cells in 5 drive strengths.
- **Device models**: SPICE models for transistors (NMOS/PMOS, HV, native),
  resistors, capacitors, diodes, BJTs across PVT corners.
- **Technology files**: Layer definitions, DRC rules, extraction rules,
  mask layer mapping for Magic, KLayout, netgen.
- **Verification decks**: DRC, LVS, antenna rule, ERC check scripts.
- **I/O pad library**: ESD-protected pads with digital and analog variants.

Install with `volare enable --pdk <name> <revision>`. Volare manages
`$PDK_ROOT` automatically. Never install PDKs manually — the tool convention
depends on versioned directory layouts under `$PDK_ROOT`.

## Mini Fab & Production Paths

### What "Mini Fab" Means

"Mini fab" covers two related concepts:

1. **Physical mini fabs**: Smaller fabrication lines (SkyWater Minnesota,
   X-Fab 150mm) running limited wafer volumes (25-100 wafers vs 10,000+).
   These exist but are B2B only — minimum engagement is $10k-50k.

2. **MPW shuttles (accessible mini fab)**: The practical path for individuals.
   Multi-Project Wafer services aggregate designs from many customers onto
   a single mask set, sharing the ~$500k mask cost. At 130nm, this brings
   per-designer cost from $500k to $100-15,000.

Tiny Tapeout further reduces cost by using a carrier chip (packing 100-400
tiny designs into one Sky130 shuttle) and handling the full logistics of
fabrication, assembly, and distribution.

### Production Paths Comparison

| Path | Cost | Area | Lead Time | Chips | Best For |
|------|------|------|-----------|-------|----------|
| **Tiny Tapeout** | ~$100-500 | 0.016mm²/tile | 6-9 mo | 1 chip + dev kit | Hobby, education, proof of concept |
| **ChipFoundry** (formerly Efabless) | ~$14,950 | ~15mm² + RISC-V SoC | 6 mo | 100 QFN or bare die | Startup MVP, real products |
| **Custom MPW** (CMP, Europractice, Muse) | ~$8k-150k | 1mm²+ | 4-6 mo | 1-10 wafers = 1000s of chips | Volume prototyping |
| **Full mask set** | ~$500k-2M | Full reticle | 2-3 mo | Unlimited | High volume (>10k units) |

## Fleet Integration

### KiCad → Chip Design Bridge

```
kicad-mcp (PCB)  →  export netlist (.kicad_net)
                  →  chip-design-mcp: load for verification
                  →  cross-check PCB BOM against ASIC pads
```

### FreeCAD → Package Co-Design

```
freecad-mcp (BIM) →  step export (.step)
                  →  chip-design-mcp: package thermal simulation
                  →  verify die area fits package cavity
```

### Documentation → Silicon Paper Trail

```
documentation-mcp  →  generate datasheets from chip-design-mcp reports
                   →  timing/power/area summaries → PDF datasheet
```

## Repo Standard

Every chip design MCP repo MUST follow the fleet repo conventions.
**Reference implementation:** `chip-design-mcp` — fleet entry
[`projects/chip-design-mcp/README.md`](../../projects/chip-design-mcp/README.md).

Mandatory:

- `pyproject.toml` with `fastmcp==3.2.0`, `prefab-ui>=0.14.0`
- `uv.lock`, root `justfile` (`bootstrap`, `serve`, `dev`, `lint`, `test`, `e2e`, `mcpb-pack`, `install-mcp`)
- `llms.txt` + `llms-full.txt`, `glama.json`, `manifest.json`, MCPB prompts (`assets/prompts/`)
- `start.ps1` + `start.bat` — naked-PC (`Require-Command` uv + Bun + Node fallback)
- `install-mcp.ps1`, `GET /api/capabilities`, `GET /.well-known/mcp/manifest.json`
- `docs/mcp_registration.md`, `docs/docstrings_sota.md` (or pointers to MCD canonical rules)
- `SkillsDirectoryProvider`, `@mcp.prompt`, `@mcp.resource`, agentic sampling tool
- Prefab cards for list/status/stats surfaces
- React 19 + Vite 6 + Tailwind webapp; **Bun** Phase 1 (`bun.lock`, `bun run dev`)
- CI (ruff + pytest); pre-commit; optional `--agentic` CodeMode

## Gotchas

- **Yosys ABC9 vs ABC**: Use `abc9` for SkyWater 130nm — it supports the
  full liberty format. Regular `abc` may fail on complex .lib files.
- **iverilog SystemVerilog**: iverilog has limited SV support. For complex
  SV designs, use Verilator or switch to commercial simulators.
- **OpenLane Docker**: The Docker image is ~3 GB. First pull takes time.
  Use `docker pull` explicitly rather than relying on OpenLane's auto-pull.
- **PDK Volare vs Manual**: Always use volare. Manual PDK installs break
  the `$PDK_ROOT` convention that the tools rely on.
- **Magic DRC**: Magic requires the tech file path to be absolute.
  It auto-resolves from `$PDK_ROOT` but falls back to explicit parameter.
- **KiCad hybrid install (kicad-mcp v0.3.0+)**: Keep **10.x stable** for fab exports;
  add **11 nightly** for headless IPC CRUD. See `kicad-mcp/docs/NIGHTLY_HEADLESS.md`.
  Do not save production boards with nightly without backup (file format may exceed 10.x).
- **Tiny Tapeout wait times**: 6-12 months from submission to chip arrival.
  Plan ahead — you can't get a chip next week.
- **Efabless → ChipFoundry**: As of 2025, Efabless was acquired by
  UmbraLogic/ChipFoundry. The free open-source MPW program ended;
  the commercial chipIgnite service ($14,950/tapeout) continues.
