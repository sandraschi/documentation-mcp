# CUA tour for RE (behavioral half of the combo)

**Status: spec, not built.** The canonical doc is the Tier 3 spec in reversing-mcp -
this page is the fleet catalog pointer, not a second source of truth.

**Go to:** [Tier 3 spec: Disassembly + CUA click-through](https://github.com/sandraschi/reversing-mcp/blob/main/docs/CUA_DISASSEMBLY_COMBO.md) -
Tour -> Capture -> Correlate -> Map pipeline, capture bundle v1, runtime-strings-to-code MVP.

## Concept in three lines

White-box RE answers *which code implements feature X*; a scripted CUA feature tour answers
*what the app does when the user does X*. Correlate the two (observed strings/behaviors as
seeds for disassembly queries) and you get **feature-to-code maps** - the product neither
half produces alone. The artmarket/Adobe wave proved the behavioral half is legible to
everyone; this fleet does both halves, with disassembly and no qualms.

## Fleet building blocks (already exist)

- **Tour driver:** pywinauto stack per [CUA smoke standard](../standards/rules/cua_nsis_smoke_testing.md) -
  title-first UIA matching, OCR verification, mouse safety; `scripts/cua-smoke.py` phases as the base.
- **Clicker counterparts:** [Cua Driver](cua-driver.md) (external) / windows-computer-use-mcp (fleet);
  comparison in [CUA_DRIVER_AND_PYWINAUTO](../patterns/CUA_DRIVER_AND_PYWINAUTO.md).
- **Analysis backend:** [Reversing MCP](../projects/reversing-mcp/README.md) (`analyze_binary`,
  `rea_investigate`, ReVa) - the correlation target.
- **Sibling halves:** [Hopper](hopper.md) (which-code engine), [Frida](frida.md) (runtime truth),
  [five-way comparison](re-tools-comparison.md).

## Safety (from the spec, non-negotiable)

Isolated host, no credentials, filtered/no network, entitled targets only; the tour *executes*
its target. Human reviews every map; stated limits travel with it.

---

*Last updated: 2026-10-11*
