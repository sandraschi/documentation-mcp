# Cool Repos

Interesting external projects worth knowing about, even if not directly in our stack.

---

## colibri

https://github.com/JustVugg/colibri

Pure C runtime for GLM-5.2 (744B MoE) on consumer hardware (25 GB RAM). Experts streamed from disk via LRU cache, MLA attention, MTP speculative decoding. Not for us (4090), but the engineering is gorgeous.

---

## TextureCraft (`storytold/texturecraft`)

https://github.com/storytold/texturecraft

Pure Rust open-source 3D texture painting workflow and modern clone of Adobe Substance 3D Painter. Features multi-channel PBR painting across 3D surfaces and UV seams, GPU ray-traced mesh map baking (AO, curvature, thickness), smart materials driven by geometry generators, an interactive GPU path-traced rendering mode (F10), channel-packed engine exports, and native MCP server integration. Paired directly with SolidCraft for the fleet's 3D asset pipeline.

---

## MaterialCraft (`storytold/materialcraft`)

https://github.com/storytold/materialcraft

Pure Rust open-source node-based procedural material authoring tool and modern clone of Adobe Substance 3D Designer and Autodesk Material Editor / Revit physical materials. Features procedural graph compilation (cooks complex graphs in <100ms), parameterized noise and pattern generators (bricks, marble, grunge, edge wear), real-time 3D preview across customizable scene meshes, headless `--hq` beauty rendering with true displacement and AO without requiring a GPU, multi-depth format exports (EXR, HDR, TIFF, PNG up to 32-bit), and native stdio MCP server support for autonomous agent material design. Part of the SolidCraft + MaterialCraft + TextureCraft 3D CAD/asset pipeline.

---

## Craft Anything (`storytold/craft-anything`)

https://github.com/storytold/craft-anything

Clean-room reverse-engineering and software reconstruction suite in 100% pure Rust, adapting the 400k-star `morluto/rea` (rea.tools) into an automated "Reverse-to-Craft" workflow (**Study → Build → Check → Ready**). Contains 284 tools for native binaries, .NET, Java, Android, Web/Electron, game archives, firmware dumps, and radio captures. Enforces legal clean-room boundaries by default, automatically installs and manages headless Ghidra 12.1.4 (omitting proprietary/pirated IDA Pro), and orchestrates Claude Code to autonomously reconstruct and verify functional clones of target apps and websites.



