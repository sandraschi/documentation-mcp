# Reversing MCP — fleet index (Digitale Bibliothek / Directmedia)

**Central index** for fleet discovery. **Source of truth:** [sandraschi/reversing-mcp](https://github.com/sandraschi/reversing-mcp) · **Local clone:** `D:\Dev\repos\reversing-mcp`

---

## Role

**FastMCP 3.1** server for **static binary analysis** and **heuristic Directmedia `.DKI` helpers**. It does **not** implement **ReVa’s** Ghidra MCP tools — add **[ReVa](https://github.com/cyberkaida/reverse-engineering-assistant)** as a **second** MCP server for interactive decompilation.

**`Digibib5.exe` / DKI** are the **worked example / test case**: a **small-to-medium** Windows app to validate reversing-mcp + webapp (and Ghidra via ReVa). **Out of scope** as a design target: decompiling massive suites (e.g. Word).

---

## Digitale Bibliothek / `text.dki` (2026-03)

- **Mission:** Use this product as a **concrete exercise** to read/decode Directmedia volumes and to prove the toolchain on a real but modest binary; optional preservation/viewer follow-through.
- **Phased Ghidra plan (canonical):** upstream **[docs/DIGIBIB_DECOMPILE_PLAN.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIGIBIB_DECOMPILE_PLAN.md)** — also at `D:\Dev\repos\reversing-mcp\docs\DIGIBIB_DECOMPILE_PLAN.md` locally.
- **Empirical:** `tree.dki` is often **cleartext CP1252 TOC**; **`text.dki`** on large bands is **header + `uint32` offset table + packed stream** — zlib heuristics alone are **insufficient** until the EXE reader is reversed.
- **Index files** (`index.htx`, `.plx`, `.ttx`, `.wlx`, `index.set`): Directmedia-internal search/navigation; **not** the same as unrelated `.htx` uses elsewhere (e.g. legacy Microsoft Index Server templates).
- **Public GitHub:** no widely adopted open decoder for this binary **TEXT.DKI** family; treat **Digibib5.exe** as the specification source.

---

## Read next

| Doc | Contents |
|-----|----------|
| [STATUS.md](./STATUS.md) | Short fleet snapshot (this folder) |
| [DIRECTMEDIA_MISSION.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIRECTMEDIA_MISSION.md) | Mission, workflow, ethics |
| [DIRECTMEDIA_REVERSING_TOOLKIT.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIRECTMEDIA_REVERSING_TOOLKIT.md) | MCP/CLI commands, volume layout table |
| [DIGIBIB_DECOMPILE_PLAN.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/DIGIBIB_DECOMPILE_PLAN.md) | Full decompile plan of attack + notes |
| [GHIDRA.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/GHIDRA.md) | ReVa vs headless |
| [README.md](https://github.com/sandraschi/reversing-mcp/blob/main/README.md) | Install, webapp, tool list |
| [CHANGELOG.md](https://github.com/sandraschi/reversing-mcp/blob/main/CHANGELOG.md) | Release notes |

---

## Fleet

| | |
|--|--|
| **Webapp ports** | **10750** (backend) · **10751** (frontend) — [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) |
| **MCP** | `uv run` / package `reversing-mcp` from clone root |

---

## Changelog (fleet)

See **[CHANGELOG.md](./CHANGELOG.md)** in this folder for documentation sync notes; **canonical** changelog is in the **source repo** `CHANGELOG.md`.
