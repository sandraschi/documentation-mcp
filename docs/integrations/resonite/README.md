# Resonite

[Resonite](https://resonite.com) is a social VR/desktop platform, the
community-built successor to NeosVR (whose cloud services shut down and was
delisted from Steam in 2025). Deep node-based visual programming (ProtoFlux),
live in-world collaborative building, no external engine required. Core
engine (FrooxEngine) is closed source; the mod ecosystem
(ResoniteModLoader/MonkeyLoader) is open.

## Fleet MCP server: `resonite-mcp`

Repo: `D:\Dev\repos\resonite-mcp` — full docs and audit history live there.
Start with
[resonite-mcp/ASSESSMENT.md](file:///D:/Dev/repos/resonite-mcp/ASSESSMENT.md)
for current verification status.

### What's actually verified real

`resonite_link.py` — a genuine, upstream-verified WebSocket client for the
official **ResoniteLink** protocol (target 0.13.1, confirmed against the
upstream C# reference). Typed `$type` discriminators, reflection, sync
method calls, LAN session discovery (UDP 12512). This is real engineering:
an earlier version of this client spoke a wire format that never existed
upstream at all, and got rewritten to match reality in July 2026.

### What needs a caveat: the OSC-based tool surface

Most of the higher-level Resonite-domain tools —
`resonite_avatar_load`, `resonite_parameter_set`, `resonite_protoflux_execute`
(`avatar.py`), `resonite_session_start`/`world_load` (`session.py`), and the
whole inventory tool set (`inventory.py`) — work by sending OSC messages to
addresses like `/resonite/session/start`, `/protoflux/execute`,
`/inventory/list`, `/inventory/spawn`. **These are not addresses Resonite
listens on out of the box.** Resonite has no built-in OSC-driven session,
inventory, or ProtoFlux-execution API — a matching ProtoFlux graph would
need to be hand-built in-world with "OSC In" nodes wired to exactly these
addresses, and nothing in this repo ships that graph. The underlying OSC
transport itself (`osc.py` — send/receive over real UDP via `python-osc`) is
genuinely functional; it's the assumption that Resonite (or an in-world
listener) responds meaningfully to these specific addresses that's
unverified.

Same class of gap as `overte-mcp`'s WebSocket bridge (which does ship the
matching in-world script) — the difference is `overte-mcp` shipped its half
of the contract, and this OSC-based tooling in `resonite-mcp` hasn't yet.

### Model formats & avatars

VRM avatars work natively via Resonite's own avatar pipeline — unlike Overte,
which needs VRM converted to GLB/FBX for entity use. `protoflux_avatar_presets.py`
and the various avatar tools target this pipeline.

### ProtoFlux

Genuinely Resonite's standout feature — live, collaborative, node-based
visual programming, editable in-world in real time. This repo's
`protoflux_helpers.py` plugin has the same address-assumption problem as
above (`/protoflux/analyze`, `/protoflux/debug` aren't real Resonite
endpoints either); see `resonite-mcp/ASSESSMENT.md` for the fix plan
(route through `resonite_link.py`'s real reflection support instead).

### Local dev setup

See `resonite-mcp/docs/` (or root-level install docs) for current setup —
not duplicated here to avoid drift.

## In-headset UX vs. VRChat and Overte

For the practical "what's it actually like to be in this" differences —
locomotion, grabbing, portals, mirrors, and a reality check on whether
lootboxes are a real platform feature (they aren't, in any of the three) —
see [../SOCIAL_VR_UX_COMPARISON.md](../SOCIAL_VR_UX_COMPARISON.md).

---

*Revision note (2026-07-30): this file previously described fictional
tooling — an "Antigravity cognitive core," tools like
`inject_protoflux`/`trigger_impulse`/`spawn_object_vrm` that don't exist
anywhere in the real `resonite-mcp` codebase, a nonexistent "RTX 4099," and
a "SOTA v13.0 compliance" framing with no basis in reality. Rewritten by
reading the actual source instead. If anyone finds this doc drifting from
the real codebase again, check the source before trusting the doc — that's
what went wrong the first time.*
