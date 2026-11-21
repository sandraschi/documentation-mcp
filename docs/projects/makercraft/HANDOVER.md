---
updated: 2026-11-18T23:08:00+01:00
status: current
tags: [makercraft, handover, artcraft, bench, instruments, workshop]
---

# MakerCraft — Handover Document

**Last Updated**: 2026-11-18
**Current State**: Tiers 4–7 + Workshop Panorama Complete (40 tests green, clippy clean, `--smoke` OK)
**Primary Artifact**: [`d:\Dev\repos\makercraft`](file:///d:/Dev/repos/makercraft) | [sandraschi/makercraft](https://github.com/sandraschi/makercraft)

---

## 1. What Was Done
- **Tier 4 (Menu Bar & Help Suite):** Universal 8-menu bar (`File`, `Edit`, `View`, `Insert`, `Modify`, `Commands`, `Window`, `Help`) with `switch_on_hover`, wired hotkeys, and 5-item Help suite + `HELP.md`.
- **Tier 5 (Pictorial Studio & Workshop Panorama):** Interactive 2-bay Maker's Workshop & ESD Workbench panorama (`Workshop` tab) plus vector technical diagrams (`hardware_viz.rs`) for all 9 machines & instruments wired to `Command::dispatch` probes and `instrument_capture`.
- **Tier 6 (Bundled Skills & AI Chat):** 8 embedded `SKILL.md` files in `makercraft-core::skills`, MCP `resources/list` + `resources/read` (`skill://`), `makercraft_skill_read` (18 MCP tools), CLI `makercraft-mcp skills`, and `Ctrl+J` local-first AI Chat Dock (`chat_dock.rs`).
- **Tier 7 (Vienna & Buying Guide):** `Vienna & Buying` tab (`reference_views.rs`) with Metalab, Happylab, Maker Austria, prep checklists, and machine/instrument buying advice.

---

## 2. Immediate Next Steps
1. Re-cut the Windows release binary and NSIS installer (`scripts/release.ps1`) if distributing updated `dist/` artifacts.
2. Wire live hardware readings into `instrument_capture` for multimeter, function-generator, spectrum-analyzer, and jtag-swd when physical hardware is attached.
