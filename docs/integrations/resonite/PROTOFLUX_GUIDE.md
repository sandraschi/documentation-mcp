# ProtoFlux: Resonite's Visual Programming System

ProtoFlux is Resonite's node-based visual programming system — the genuine
standout feature of the platform. This is real and important, not fleet
fantasy: it's live, collaborative, in-world visual scripting that lets
non-programmers build interactive behavior by connecting nodes with wires,
edited by multiple users simultaneously in real time.

## Core concepts (accurate, general ProtoFlux knowledge)

**Nodes** — visual building blocks:
- Value nodes: store data (numbers, text, colors, vectors)
- Operation nodes: math and logic
- Flow control: sequencing, conditionals, loops
- I/O nodes: interface with the world (buttons, triggers, sensors)

**Wires** — connections carrying data or execution flow between nodes.

**Components** — reusable ProtoFlux programs you can save and share.

### Common patterns

- Door that opens when approached: distance check → conditional → rotation
- Color-changing object: time source → wave function → material color
- Teleport pad: trigger enter → get target position → set player position

## Where to learn more (official, not duplicated here)

- Official wiki: https://wiki.resonite.com/ProtoFlux
- Node reference: https://wiki.resonite.com/Category:ProtoFlux_Nodes

## MCP integration — honest status (2026-07-30)

This is the part worth being careful about. `resonite-mcp`'s tool surface
touching ProtoFlux is a **mix of real and not-yet-working**:

- `resonite_protoflux_execute` (in `avatar.py`) sends OSC to
  `/protoflux/execute` — **not a real Resonite-native address**. It would
  only work if a matching ProtoFlux "OSC In" graph were hand-built in-world
  to listen there, and nothing in this repo ships that graph yet.
- The `protoflux_helpers.py` plugin's `analyze_script` and `debug_session`
  tools have the same problem (`/protoflux/analyze`, `/protoflux/debug`
  aren't real endpoints either). Its `generate_template` and
  `optimize_script` tools are static canned text, not real script
  inspection.
- What genuinely works: `resonite_link.py`'s WebSocket client for the
  official **ResoniteLink** protocol — real reflection, sync method calls,
  verified against the upstream C# reference. The fix path for ProtoFlux
  tooling is to route through this real client instead of the fictional OSC
  addresses above — see `resonite-mcp/ASSESSMENT.md` for the concrete plan.

Don't take the function names above as proof the feature works — check
`ASSESSMENT.md` for current status before relying on any of them.

---

*Revision note (2026-07-30): this file previously included a fabricated
"OSC Integration" section with an invented address format
(`/avatar/parameters/ProtoFlux/...`) and an unverified Discord link. Removed
both. The general ProtoFlux conceptual content above was accurate and kept.*
