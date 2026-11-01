# Hopper Integration (Native RE Provider)

## Overview

**Hopper Disassembler** ([hopperapp.com](https://www.hopperapp.com), Cryptic Apps) is a commercial
disassembler/decompiler for macOS and Linux binaries - the "cheap little brother of IDA Pro":
a commercial license in the ~$100 range (perpetual historically; check the site for current v5
pricing), versus IDA Pro's four-figure seat. In the MCP fleet, Hopper is the **recommended happy
path** for REA native analysis: it is REA's best-supported provider, and `npx rea-agents setup`
installs it with one approval.

**Hopper**: [hopperapp.com](https://www.hopperapp.com)  
**No dedicated Hopper MCP server** in this fleet. Hopper is consumed **through REA**
(`rea-agents` provider `hopper`) and through
**reversing-mcp** (`rea_investigate(..., provider="hopper")` - see Tier 2 bridge).

---

## What Hopper does

- **Disassemble** macOS/Linux binaries (Intel + ARM) with control-flow graphs.
- **Decompile** procedures to pseudo-C (weaker than Hex-Rays, stronger than nothing).
- **Scriptable** analysis sessions that REA drives per query (function dossiers, search, xrefs,
  traces) with evidence + stated limits, same contract as the other providers.

Typical use in reversing: the provider behind `rea_investigate(path, kind="native_overview")`
and follow-up `native_search` / `native_function` / `decompile` calls - no Hopper GUI needed,
the agent never leaves the chat.

---

## Role in the fleet

### reversing-mcp Tier 2 + REA sidecar

- **Target**: any native binary triaged by `analyze_binary` first.
- **Goal**: agent-driven pseudocode/search/xrefs without learning a disassembler UI.
- **Flow**: `check_tools()` confirms REA + Hopper -> `rea_investigate(path)` (auto-selects
  Hopper when it is the only provider) -> follow-up kinds for specifics -> ReVa/Ghidra when
  Hopper's decompiler is not enough.

Docs live in **reversing-mcp**:

- **Provider ranking**: [docs/REA.md §5b](https://github.com/sandraschi/reversing-mcp/blob/main/docs/REA.md) -
  Hopper first, Ghidra second, IDA bring-your-own-license.
- **Bridge**: `src/reversing_mcp/rea_bridge.py` + `rea_investigate` tool.
- **Tier 3 spec**: [docs/CUA_DISASSEMBLY_COMBO.md](https://github.com/sandraschi/reversing-mcp/blob/main/docs/CUA_DISASSEMBLY_COMBO.md) -
  Hopper answers "which code" for behaviors a CUA tour observes.

There is **no Hopper MCP server** in mcp-central-docs; Hopper runs as an **analysis engine**
under REA, driven from reversing-mcp or any REA-registered agent.

---

## Hopper vs Ghidra vs IDA Pro

| | Hopper (recommended) | Ghidra | IDA Pro |
|---|---|---|---|
| Cost | Commercial, ~$100 range | Free (NSA, Apache-2.0) | $$$$ per seat + Hex-Rays |
| License friction | Buy once, REA setup installs | None, but heavy install | Bring-your-own everything (`REA_IDA_MCP_CONFIG` + supervisor wiring) |
| Decompiler quality | Serviceable pseudo-C | Good, slow first import | Best in class (Hex-Rays) |
| REA support | First-class, auto-installed | Good, most knobs | Narrow adapter (function dossiers; no whole-binary overview, no mutation/debugging) |
| Catch | macOS/Linux-native (see below) | Windows support experimental upstream | Most setup; REA never touches activation - keep the license clean |

Full five-way comparison (adds IDA Free + Frida with decision matrix):
[RE tooling compared](re-tools-comparison.md).

Omit `provider` everywhere and let REA auto-select; pass one explicitly only when several
engines are installed and you want a specific one.

---

## Setup and usage (outline)

1. **Install REA sidecar**: `npx rea-agents setup` (approves Hopper install) - or
   `just setup-rea` from reversing-mcp.
2. **Restart the agent**, verify: `rea_investigate(None, kind="providers")` should list hopper.
3. **Query**: `rea_investigate("prog.exe")` for auto-routed overview, then `native_search` /
   `native_function` / `native_decompile` follow-ups.
4. **Escalate**: when Hopper's pseudo-C is insufficient, re-run with `provider="ghidra"` or
   go interactive via ReVa (see [Reversing MCP](../projects/reversing-mcp/README.md)).

No MCP tool invokes Hopper directly; all traffic goes through the `rea` CLI / REA MCP server.

---

## Host caveat (Goliath / Windows) - VERIFIED 2026-10-11: unsupported

`rea providers` on win32/x64 reports: **"Hopper integration is not supported on win32."**
No Hopper path exists on a Windows REA host — not native, not via WSL (the provider
runs in REA's own host context). Hopper is a macOS/Linux-host option only. On Goliath
the working REA engines are Ghidra (needs 12.1.x + `GHIDRA_INSTALL_DIR`; 12.0 present
at `C:\Program Files\ghidra_12.0_PUBLIC`, env var set 2026-10-11, upgrade pending) and
IDA Pro (bring-your-own license + `REA_IDA_MCP_CONFIG`). Engine-free REA kinds
(JS/Electron/.NET/APK/browser) are unaffected.

---

## License hygiene

REA's IDA adapter talks to a shim and never touches activation - which means it cannot
distinguish a legitimate IDA seat from a cracked one either. That is between the user and
Hex-Rays enforcement. Fleet stance: the documented path is **Hopper (cheap, legit)** or
**Ghidra (free)**; IDA appears in docs strictly as bring-your-own-license for seats the
operator already pays for. Analyze only targets you are entitled to analyze.

---

## References

- [Hopper](https://www.hopperapp.com) - official site, pricing, downloads
- [REA](https://rea.tools) - sidecar home; [installation](https://github.com/morluto/rea/blob/main/docs/installation.md) (Hopper section), [IDA provider](https://github.com/morluto/rea/blob/main/docs/ida-provider.md)
- [Reversing MCP](../projects/reversing-mcp/README.md) - MCP server (project): Tier 2 bridge, binary tools, webapp
- [Frida](frida.md) - dynamic half of the same workflow (hook at runtime what Hopper found statically)

---

*Last updated: 2026-10-11*
