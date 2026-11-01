# Reversing MCP

**Source of truth:** [sandraschi/reversing-mcp](https://github.com/sandraschi/reversing-mcp) · local `D:\Dev\repos\reversing-mcp`

FastMCP 3.4 server. Product: **the Reversing Gym** — hand in a Windows app, get a
staged cloning pipeline (intake → triage → gate → oracle capture → clicker tour →
recovery → UI build → round trip → compare) with the original app as oracle.
Vision: [PRD.md](https://github.com/sandraschi/reversing-mcp/blob/main/PRD.md).

## What it is now (2026-10-15)

20 tools across eight domains: static triage (5), file/PE (2), Directmedia/DKI (4),
system (`check_tools`, `shutdown`, `help`, `show_tools_card` Prefab), REA sidecar
(`rea_investigate`), Gym (`gym` portmanteau), Engines (`engine`), Toolbox (`toolbox`),
and ReVa lifecycle (`reva`).

- **Gym G1 (shipped):** job runner + stages 0/1/4 (intake, DiE/capa triage,
  assessment gate), 6 REST endpoints, `/gym` webapp page. Proven on Digibib5 (amber).
  Spec: `docs/GYM_SPEC.md`; playbook: `docs/ELICITATION_AND_CLICKER.md`.
- **Tier 3 ClickerLab (shipped):** automated UI elicitation, tour runs, and static/runtime correlation
  (`correlate_session`) generating Ghidra plate comments and IDA scripts.
- **Engines:** DiE/capa/Frida wrappers (`engines.py`), Java 17 LTS JVM environment with PyGhidra.

Pair with **[ReVa](https://github.com/cyberkaida/reverse-engineering-assistant)** for interactive
Ghidra decompilation over MCP (`docs/REVA.md`).

## The Twin Methods: Disassembly + CUA Clickthrough Synthesis

The architecture of `reversing-mcp` bridges two historically divided paradigms in reverse engineering:

1. **Classical Disassembly (White-Box)**: Ghidra (headless & ReVa bridge), radare2, IDA, Hopper, capa, and Frida provide granular code inspection (instructions, control flow graphs, cross-references, API hooks).
   - *Limitation*: "Static Blindness" — in large stripped or packed binaries (5–50 MB), analysts and LLMs face hundreds of thousands of unlabelled subroutines (`FUN_004012A0`) with no inherent cue as to which function corresponds to a specific user action.
2. **CUA Clickthrough & Gym Oracle Loops (Black-Box)**: Computer Use Agents drive the target binary via Windows Accessibility (pywinauto), capturing OCR text, window transitions, clipboard state, and file/registry diffs.
   - *Limitation*: "Dynamic Blindness" — observing the UI reveals what happened externally, but cannot inspect how the underlying algorithm or decompression routine works internally.

### The Correlation Bridge (Feature-to-Code Maps)

By feeding the output of automated CUA tours through `correlate_session` (ClickerLab / Gym Stage 3), runtime UI strings and event tokens are correlated against the binary's static strings, data references, and call sites. 

The resulting output:
- Generates **Ghidra plate comments** and **IDA import scripts** (`map_import_ida.py`).
- Transforms opaque function addresses into semantic, verified feature implementations (e.g. `Click Export -> ExportDialog::write -> Offset 0x400 -> DecryptStream`).
- Gives autonomous agents both eyes (CUA/OCR) to drive and inspect, and hands (Ghidra/Frida) to dissect and verify.


## Fleet wiring

| Piece | Where |
|-------|-------|
| Gym spec + playbook | `docs/GYM_SPEC.md` + `docs/ELICITATION_AND_CLICKER.md` |
| Provider ranking (Ghidra > IDA-BYO; Hopper non-Windows) | `docs/REA.md` §5b + `integrations/hopper.md` |
| Five-way engine comparison | `integrations/re-tools-comparison.md` |
| CUA tour pointer | `integrations/cua-re-tour.md` |
| Dynamic half (Frida) | `integrations/frida.md` |
| Mission target (Digibib5/DKI) | `DIGIBIB_STATUS.md` in this folder |
| Ports | 10750 / 10751 ([WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)) |

## Docs in this folder

| File | Role |
|------|------|
| [README.md](./README.md) | This hub |
| [REVERSE_TO_CRAFT_PLAYBOOK.md](./REVERSE_TO_CRAFT_PLAYBOOK.md) | Blueprint: rebuilding reversed apps into Rust Crafts |
| [STATUS.md](./STATUS.md) | Fleet snapshot (updated 2026-10-15) |
| [NEXT_STEPS.md](./NEXT_STEPS.md) | Current next steps (G1 done, G2 next) |
| [DIGIBIB_STATUS.md](./DIGIBIB_STATUS.md) | Mirror of upstream Digibib5 / `Text.dki` notes |
| [GHIDRA_SOTA_2026.md](./GHIDRA_SOTA_2026.md) | Ghidra/ReVa background (2026-03, historical) |
| [CHANGELOG.md](./CHANGELOG.md) | Doc-sync log for central-docs only |
