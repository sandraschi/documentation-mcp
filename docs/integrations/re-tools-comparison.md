# RE tooling compared: Hopper vs IDA Free vs IDA Pro vs Ghidra vs Frida

Fleet-wide answer to "which engine behind REA / reversing-mcp?" Verified 2026-10-11 against
REA docs and vendor sites. Prices and free-tier scopes move - re-check before spending or
building workflows on them.

## The one-paragraph version

- **Static disassembly (pick ONE to start):** Hopper if ~$100 is spendable (best REA support),
  Ghidra if the budget is $0 (best free decompiler, heavier), IDA Pro if someone else pays
  (best decompiler, most wiring).
- **IDA Free** is try-before-you-buy for learning, not a fleet workhorse (x86/x64 targets,
  non-commercial, feature-limited; REA+IDA assumes Pro).
- **Frida is not in the same race:** it instruments RUNNING processes (dynamic). It complements
  whichever static tool you pick - Hopper/Ghidra/IDA find the address, Frida dumps the live bytes.

## Comparison

| | Hopper | IDA Free | IDA Pro | Ghidra | Frida |
|---|---|---|---|---|---|
| Cost | Commercial, ~$100 range | Free, non-commercial only | $$$$ per seat + Hex-Rays | Free (Apache-2.0) | Free (wxWindows Library Licence) |
| Hosts | macOS, Linux (no Windows build) | Win/Lin/mac | Win/Lin/mac | Win/Lin/mac (Java) | Win/Lin/mac/mobile |
| Targets | macOS/Linux binaries (Intel + ARM) | x86/x64 only | All CPUs | 90+ architectures | Any running process |
| Kind | Static | Static | Static | Static | Dynamic |
| Decompiler | Serviceable pseudo-C | None/limited (v9 scope TO-VERIFY) | Hex-Rays, best in class | Good, slower first import | N/A - reads live memory instead |
| REA provider | First-class, auto-installed by setup | Treat as unsupported (adapter assumes Pro) | BYO adapter (`mrexodia/ida-pro-mcp`), narrow coverage | Good, Windows glue experimental | Not a provider; output feeds REA process-capture inputs |
| Fleet path | `rea_investigate(provider="hopper")` | Practice only, no fleet workflows | `rea_investigate(provider="ida")` + `REA_IDA_MCP_CONFIG` | `rea_investigate(provider="ghidra")`, ReVa, `analyze_binary` headless | Scripts + `docs/DIRECTMEDIA_REVERSING_TOOLKIT.md` |
| Goliath fit | WSL/2nd host (TO-VERIFY) | Native Windows OK | Native Windows OK | Native, experimental REA glue | Native Windows OK |

## Decision matrix

- $0, Windows, want answers today -> **Ghidra** for static depth, **Frida** scripts for runtime questions.
- ~$100 spendable, macOS/Linux (or WSL once verified) -> **Hopper**: least friction behind an agent.
- Employer-owned IDA seat -> **IDA Pro** for the hard functions (Hex-Rays), Hopper/Ghidra for bulk triage.
- "What does it DO when I click X?" -> **Frida** (+ CUA tour per the Tier 3 spec), regardless of static choice.
- Weekend learning on x86 crackmes -> **IDA Free** is fine; do not build fleet workflows on it.

## Coverage honesty (REA adapter limits matter here)

- **IDA adapter:** function dossiers, search, pseudocode/asm. NO whole-binary overview, symbol
  inventory, mutation, debugging, Python forwarding, GUI nav. Empty facets mean *unknown*.
- **Hopper/Ghidra via REA:** full native workflows (analyze/search/function/decompile/xrefs/trace)
  plus snapshots for repeat queries.
- **Frida:** no disassembly at all. Proves runtime facts: bytes read, call order, handles, buffers.

## Honorable mentions (not compared)

- **radare2/rizin:** already probed by reversing-mcp `check_tools`; free and scriptable, no REA
  provider, no fleet docs yet. Candidate if Ghidra feels heavy and Hopper is unavailable.
- **Binary Ninja:** excellent commercial middle ground with a real API; no REA provider, no fleet
  integration. Revisit if Hopper hits decompiler limits before an IDA seat appears.

## References

- [Hopper](hopper.md) - recommended provider page, license hygiene, Windows TO-VERIFY
- [Frida](frida.md) - dynamic half, Directmedia capture scripts
- [Reversing MCP](../projects/reversing-mcp/README.md) - Tier 2 bridge (`rea_investigate`), Tier 3 spec
- [REA](https://rea.tools) - [installation](https://github.com/morluto/rea/blob/main/docs/installation.md),
  [IDA provider](https://github.com/morluto/rea/blob/main/docs/ida-provider.md),
  [CLI](https://github.com/morluto/rea/blob/main/docs/cli.md)

---

*Last updated: 2026-10-11*
