# Frida Integration (Dynamic Analysis)

## Overview

**Frida** is a dynamic instrumentation toolkit. It lets you inject scripts (JavaScript or Python) into a running process to hook functions, read/write memory, and trace execution **without** source code and without patching the binary. It is used for reverse engineering, debugging, and security research. In the MCP fleet, Frida is used **alongside** Reversing MCP (Ghidra, binary analysis) for **runtime behavior**: capturing file reads, API calls, and buffers when a target application (e.g. Digibib5.exe) opens or processes specific files (e.g. .dki).

**Frida**: [frida.re](https://frida.re)  
**No dedicated Frida MCP server** in this fleet. Frida is used via **scripts** and automation in the [reversing-mcp](https://github.com/sandraschi/reversing-mcp) repo and documented in the **Directmedia reversing toolkit**.

---

## What Frida does

- **Attach** to a running process or **spawn** a process under Frida.
- **Hook** exported APIs (e.g. `kernel32!ReadFile`, `CreateFileW`) or **module + offset** (e.g. `Module.findBaseAddress("Digibib5.exe") + 0x12345`).
- **Inspect** arguments and return values; **dump** memory (e.g. `Memory.readByteArray(buffer, size)`); **trace** call order.
- **No C DLL or binary patch** required: instrumentation is script-driven (JS or Python bindings).

Typical use in reversing: hook file I/O or a decompress function identified in Ghidra; log or dump buffers to disk for later analysis.

---

## Role in the fleet

### Reversing MCP and Directmedia

- **Target**: Digibib5.exe (Digitale Bibliothek 5), which reads Directmedia .dki files.
- **Goal**: Capture the raw bytes read from .dki files (and optionally trace into a decompress routine) to reverse the format.
- **Flow**: Use **Ghidra** (via Reversing MCP) to find ReadFile/CreateFile and decompress logic; use **Frida** to hook those at runtime and dump buffers when the user opens a .dki in the reader.

Scripts and docs live in **reversing-mcp**:

- **Toolkit**: [docs/DIRECTMEDIA_REVERSING_TOOLKIT.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIRECTMEDIA_REVERSING_TOOLKIT.md) — Section "2.4 Frida" and automation.
- **Scripts**: `scripts/directmedia/` — e.g. Frida script that hooks CreateFileW + ReadFile and dumps .dki reads to `tools/directmedia/captures/` (via `send()` to a Python host that writes files).
- **Mission**: [docs/DIRECTMEDIA_MISSION.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIRECTMEDIA_MISSION.md) — Target binary and workflow.

There is **no Frida MCP server** in mcp-central-docs; Frida is run as a **standalone tool** (CLI or Python) with scripts maintained in reversing-mcp.

---

## When to use Frida vs Ghidra

| Use case | Prefer |
|----------|--------|
| Static structure, strings, xrefs, decompilation | **Ghidra** (via Reversing MCP `ghidra_*` tools) |
| Runtime behavior: what bytes are read, in what order, with what handles | **Frida** (scripts; no MCP tools) |
| Finding where ReadFile/decompress is called | **Ghidra** (xrefs, decompile) |
| Capturing actual read buffers when user opens a file | **Frida** (hook ReadFile, dump buffer) |
| Batch analysis of many binaries, no GUI | **Ghidra headless** or PyGhidra; Frida is per-process at runtime |

Use **Ghidra first** to identify addresses and call flow; use **Frida** when you need live data from a running instance of the target.

---

## Setup and usage (outline)

1. **Install Frida**: `pip install frida frida-tools` (or see [frida.re](https://frida.re/docs/installation/)).
2. **Target**: Run the target app (e.g. Digibib5.exe) or use Frida spawn.
3. **Script**: Use a script from reversing-mcp (e.g. hook CreateFileW + ReadFile; on .dki path, tag handle; on ReadFile for that handle, dump buffer via `send()` to Python and write to `tools/directmedia/captures/`).
4. **Run**: `frida -l script.js -f "C:\...\Digibib5.exe" --no-pause` or attach to running process.
5. **Trigger**: In the app, open a .dki file; inspect dumps in the captures folder.

No MCP tool invokes Frida; automation is via shell or Python runner in reversing-mcp.

---

## References

- [Frida](https://frida.re) — official site and docs
- [Reversing MCP](../projects/reversing-mcp/README.md) — MCP server (project): Ghidra bridge, binary tools, webapp
- [Reversing MCP – Directmedia reversing toolkit](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIRECTMEDIA_REVERSING_TOOLKIT.md) — Frida section and automation
- [Reversing MCP – Directmedia mission](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIRECTMEDIA_MISSION.md) — target binary and workflow

---

*Last updated: 2026-03*
