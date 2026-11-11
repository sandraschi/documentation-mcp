# Craft Anything: Deep Dive, Architecture Analysis, and Parity with REA (rea.tools)

**Status:** Research & Architectural Teardown | **Date:** 2026-11-01  
**Subject:** `storytold/craft-anything` — the newly published clean-room reverse-engineering and autonomous software reconstruction app, adapted from `morluto/rea` (the 400k-star `rea.tools` repository).  
**Evidence Base:** Source tree at `_upstream/craft-anything` (13 crates, 284 tools), comparative analysis against `_upstream/rea` (`morluto/rea` v6.8.0), our fleet's reversing playbook (`mcp-central-docs/projects/reversing-mcp/REVERSE_TO_CRAFT_PLAYBOOK.md`), and live tool registration checks.

**Related Documents:**
- `mcp-central-docs/projects/reversing-mcp/REVERSE_TO_CRAFT_PLAYBOOK.md` — Reverse-to-Craft doctrine
- `mcp-central-docs/research/2026-10-28-ios-reverse-engineering.md` — Mobile reversing in REA
- `mcp-central-docs/reference/COOL_REPOS.md` — Upstream repo index
- `_upstream/craft-anything/README.md` & `_upstream/craft-anything/AGENTS.md`

---

## 1. Executive Summary

On November 1, 2026, the ArtCraft team (`storytold`) released **Craft Anything**, a landmark tool with the tagline:  
> *"See how any website, app or game works, then have AI build your own version; an open-source, clean-room engine in pure Rust."*

Craft Anything is an architectural reimagining and adaptation of **REA** (`morluto/rea`, rea.tools), the acclaimed 400,000+ star repository that defined modern agentic reverse engineering. While REA established the standard for reverse-engineering MCP tools across binaries, web, and runtime behavior, **Craft Anything transforms REA's observational tools into an end-to-end autonomous software recreation engine.**

---

## 2. Core Differences: REA (`morluto/rea`) vs. Craft Anything (`storytold/craft-anything`)

| Dimension | REA (`morluto/rea`) | Craft Anything (`storytold/craft-anything`) |
|---|---|---|
| **Primary Thesis** | **Reverse-engineer anything.** Diagnostic & observational oracle across runtimes and binaries. | **Understand anything, then craft your own.** Four-step autonomous reconstruction pipeline (**Study → Build → Check → Ready**). |
| **Language & Stack** | TypeScript / Node.js orchestration (`package.json`, Turborepo), native C/C++ bridges, Python helper bridges. | **100% Pure Rust** multi-crate workspace (13 crates), native `egui` GUI, zero non-test unwrap/panics. |
| **Tool Count** | ~350+ modular MCP tools across native, mobile, web, and binary analyzers. | **284 unified tools** (271 engine tools, rest setup/AI). Each tool is simultaneously a CLI subcommand, an egui UI action, and an MCP tool. |
| **AI Agent Integration** | MCP server exposes endpoints for external clients (Claude Desktop, Cursor, Cline). | **Direct agent orchestration:** embeds a coding agent driver (Claude Code CLI `claude` supported natively; Codex adapter experimental) with iterative self-healing loops. |
| **Legal / IP Posture** | Universal analysis (investigator responsible for operational boundaries). | **Strict Dual-Mode Architecture:** Enforces **Clean Room Mode** by default (only visible UI, external APIs, measured layout; refuses internal binary inspection). **Deep Mode** available for authorized private work. |
| **Decompiler / Lifter** | Heavy reliance on external tools (Ghidra, IDA Pro via MCP, radare2/rizin, Hopper). | Built-in native disassembler and decompiler (`crates/disasm`, `crates/formats`) working without any external dependencies; optional Ghidra bridge for Deep mode. |

---

## 3. The Four-Stage Reconstruction Pipeline ("Crafting")

Where classical reverse engineering ends with a disassembler report or IDA/Ghidra database, Craft Anything treats reverse engineering as step 1 of an automated production loop:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   1. STUDY   │ ──> │   2. BUILD   │ ──> │   3. CHECK   │ ──> │   4. READY   │
│              │     │              │     │              │     │              │
│ Clean Room:  │     │ Coding agent │     │ Visual diff  │     │ Launch, run, │
│  viewports,  │     │ (Claude Code)│     │ (CDP at 3    │     │ or play game;│
│  DOM, CSS,   │     │ crafts fresh │     │  widths),    │     │ refine via   │
│  window cap. │     │ project in   │     │ runtime test,│     │ chat box.    │
│ Deep Mode:   │     │ chosen tech  │     │ AST & route  │     │              │
│  AST, pseudo-│     │ stack.       │     │ comparison.  │     │              │
│  C, Ghidra.  │     │              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

1. **Study:** The engine observes the target. In Clean Room mode, it analyzes visual structure, DOM hierarchies, API endpoints, typography, and color tokens without reading proprietary source code. In Deep mode, it analyzes functions, CFGs, strings, and decompiled code.
2. **Build:** Craft Anything invokes a local, unmodified `claude` CLI session (Claude Code), instructing it to build the project from scratch in a target directory using a clean-room specification.
3. **Check:** The engine runs automated verification (`compare_tools`, `check_tools`). For web applications, it captures both the target and the reconstructed site at 3 viewports via loopback CDP, computes perceptual pixel and layout diffs, and lists remaining discrepancies.
4. **Ready:** Presents the running clone, offers a mock backend (`standin_tools`) if the target relied on private APIs, and allows the user to converse with the agent to polish remaining details.

---

## 4. The Ghidra vs. IDA Pro Strategy

A critical design choice in Craft Anything is its deliberate treatment of external decompilers:

### 4.1 Automated Ghidra Lifecycle
Craft Anything provides fully automated, hands-off setup for Ghidra:
- Located in `crates/engines/src/ghidra/get.rs`.
- Downloads **Ghidra 12.1.4** (~543 MB) and **Eclipse Temurin OpenJDK 21** (~196 MB).
- Validates the publisher's cryptographic SHA-256 checksum *before* extracting to disk.
- Operates Ghidra completely headless via `CraftAnythingBridge.java` and `analyzeHeadless.bat`.
- No user configuration or Java installation required.

### 4.2 Complete Omission of IDA / IDA Pro
While REA (`morluto/rea`) provided an IDA provider (`docs/ida-provider.md`) bridging to `mrexodia/ida-pro-mcp`, **Craft Anything contains zero support for IDA or IDA Pro.** The codebase confirms no IDA references, binaries, or bridge scripts exist.

**Why did ArtCraft omit IDA Pro?**
1. **Commercial Licensing & Redistribution:** IDA Pro (Hex-Rays) is proprietary commercial software costing thousands of dollars per license. It cannot be automated, distributed, or pinned in a public installer.
2. **Piracy & Legal Liability:** A significant portion of hobbyist reverse engineers use cracked or illicit copies of IDA Pro ("legally or lees legally"). ArtCraft is an open-source, corporate-backed initiative (Apache 2.0 / MIT) that must avoid legal exposure, license compliance issues, or implicit endorsement of warez.
3. **Headless Clean-Room Philosophy:** Craft Anything prioritizes reproducible, automated CI and CLI workflows. Ghidra provides a sanctioned, open-source, headless Java API that can be checked and run autonomously.
4. **Pure-Rust Native Engine:** Craft Anything ships its own disassembler and decompiler (`crates/disasm`), meaning basic static analysis functions out-of-the-box without needing any external disassembly suite at all.

---

## 5. Scope Boundaries: Software vs. Hardware

The user noted: *"it clones / reverses / 'crafts' apps, websites but no hardware (so far)"*.

### 5.1 What Craft Anything Supports
- **Desktop & Native Binaries:** ELF (Linux), PE (Windows), Mach-O (macOS), .NET (ECMA-335 bytecode), Java (.class, JAR, WAR), Go, Rust (symbol table, `cargo-auditable`).
- **Web & Electron Applications:** JavaScript bundles, source map resolution, AST parsing, module graph recovery, Electron ASAR unpacking and fuse wire analysis, Chromium loopback CDP instrumentation, network capture mocking (`standin_tools`).
- **Mobile Applications:** Android (APK, DEX, resources, JADX decompiler bridge, ADB phone/emulator bridge), Apple (Swift metadata, Interface Builder, dyld shared cache, iOS simulator).
- **Game Archives:** Unity FS / IL2CPP metadata parsing, Unreal PAK archives, Godot PCK packages.
- **Embedded Software & Firmware Images:** `firmware_regions_list` and `firmware_image_extract` provide signature scanning, entropy mapping, and carving for SquashFS, cramfs, romfs, JFFS2, UBI, ext2/3/4, FAT, device trees/FIT, and bootloaders.
- **Radio Signal Captures:** `radio_recording_decode` interfaces with `rtl_433` to decode recorded I/Q SDR samples.
- **Packet Captures:** PCAP / PCAPNG parsing.

### 5.2 What Craft Anything Deliberately Does NOT Support (Hardware Boundaries)
1. **No Physical Hardware Debugging:** No JTAG, SWD, UART, or SPI physical bus debugging adapters.
2. **No Hardware Logic Capture:** No oscilloscope, logic analyzer (e.g. Saleae), or glitching interfaces.
3. **No PCB / Silicon Reversing:** No PCB trace routing recovery, Gerber/drill file netlist reconstruction, or silicon die optical decapping analysis.
4. **No Hardware "Crafting":** Craft Anything's build stage only outputs software (React, Vue, HTML, Rust, Python, Go). It does not craft schematics, KiCad PCB layouts, or Verilog/VHDL FPGA bitstreams (for CAD solids, the ecosystem relies separately on SolidCraft).

---

## 6. Workspace Layout of `craft-anything`

The codebase is organized into a clean 13-crate hierarchy governed by strict layering tests (`cargo xtask layers`):

```
crates/
  evidence     L0  Canonical evidence models, confidence ratings, limitation ledgers
  formats      L0  Standalone zero-IO parsers (ELF, PE, Mach-O, WASM, DEX, APK, ASAR, .NET)
  disasm       L1  Native Clean-Room engine: instruction decode, CFG, xrefs, pseudo-C
  js           L1  JavaScript/Electron analysis: module graphs, AST unbundling, source maps
  analysis     L2  Evidence synthesis: triage dossiers, runtime trace, rebuild ledger
  platform     L2  Native OS primitives: sandbox, PTY process capture, atomic storage
  engines      L3  External engine adapters: Ghidra headless bridge, ADB, CDP, Frida, JADX
  engine       L4  Session state, .cany project format, 284 ToolSpecs, settings & consent
  ai           L5  Coding agent backends (Claude Code CLI driver, OpenAI/Anthropic APIs)
  mcp          L5  High-performance MCP server with progressive toolsets & paging
  setup        L5  Coding-agent connector, system doctor, external tool installer
  ui-egui      L6  Desktop GUI with beginner "Make" view and expert "Workbench"
  testkit          Synthetic target generation and testing harness
```

---

## 7. Strategic Impact on the Fleet

Craft Anything directly completes the vision articulated in our fleet's `mcp-central-docs/projects/reversing-mcp/REVERSE_TO_CRAFT_PLAYBOOK.md`:
1. It validates the **Reverse-to-Craft doctrine** on a global scale.
2. It provides our agents with a pre-packaged, zero-configuration reverse-engineering and recreation toolset that runs natively on Windows without Node.js runtime overhead.
3. It complements `solidcraft` (CAD), `texturecraft` (3D texturing), and `figcraft`/`designcraft` (UI/graphic design), positioning the ArtCraft suite as the premier open-source autonomous creation stack.
