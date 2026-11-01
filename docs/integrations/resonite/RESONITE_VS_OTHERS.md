# Resonite vs Other VR Platforms

**A comparison of Resonite with the other social VR platforms still actually
standing as of mid-2026, plus Overte for context (different niche — see
below).**

*This comparison complements the [resonite-mcp repo](file:///D:/Dev/repos/resonite-mcp) documentation.*

---

## What's actually still standing (2026)

Most of the mid-2010s social VR field is dead or dying: AltspaceVR shut down
(Microsoft, 2023) — though SideQuest acquired the name in 2026 with a
fall-2026 relaunch planned, see [SOCIAL_VR_WATCH.md](../SOCIAL_VR_WATCH.md) —
NeosVR's cloud services shut down and the platform was delisted from Steam
(2025) — Resonite is its community-built successor.
Horizon Worlds is dropping VR support for a mobile-first pivot (Feb 2026),
alongside Meta cutting Reality Labs' budget 30% and closing three game studios.
Practically speaking, the field that matters now is **VRChat, Resonite, and
Overte** — three platforms with real, different audiences, not three
competitors chasing the same one.

## Quick comparison

| | VRChat | Resonite | Overte |
|---|---|---|---|
| Core engine | Closed source (Unity-based) | Closed source (FrooxEngine) | Open source (HiFi fork) |
| Scripting | Udon (C#), external Unity build | ProtoFlux (in-world visual, live collaborative) | JS (Interface client scripts) |
| Self-hosting | No | No | Yes — you run the domain-server |
| Community | Largest of the three | Smaller, technical/creator-heavy | Smallest, infra/self-host minded |
| Openness | Proprietary | Mod ecosystem (ResoniteModLoader) around a closed core | Fully open, forkable |

## Resonite vs VRChat

### Similarities
- Social VR focus, user-generated avatars and worlds, cross-platform (PC/Quest/mobile), spatial voice.

### Differences
- **Scripting**: VRChat's Udon (C#) needs an external Unity build step; Resonite's ProtoFlux is a node-based visual language edited live, in-world, collaboratively — no external engine needed at all.
- **World building**: VRChat worlds are separate Unity projects uploaded as packages; Resonite worlds are edited directly in-session.
- **Avatars**: VRChat has a much bigger avatar marketplace and rigging ecosystem; Resonite's avatar system is simpler but has stronger live parameter control.
- **Community size**: VRChat's is much larger — Resonite's is smaller and skews toward creators/programmers over general social users.

## Resonite vs Overte

These serve different purposes more than they compete:

- **Overte** is what you reach for when you want to *own the whole stack* — self-hosted domain-server, open C++/JS codebase, full control, no dependency on anyone else's infrastructure. Weaker community, thinner creation tools, but nothing stops you from forking or patching the engine itself.
- **Resonite** is what you reach for when you want *depth of in-world creation and an existing population* — ProtoFlux is a genuinely powerful live visual programming system, and there's an actual community building things in it right now (see the Metaverse Maker Contest). The tradeoff: FrooxEngine itself is closed, so extending Resonite means working through mods (ResoniteModLoader/MonkeyLoader, Harmony patches) that can break on any upstream update, and there's no way to self-host.
- For `overte-mcp` (infrastructure you control) and `resonite-mcp` (rich existing creative space), the platform choice matches the actual use case for each project rather than one being objectively better.

## Who should use which

- **Want full control, self-hosting, or to build your own thing on an open codebase** — Overte.
- **Want the biggest existing social audience, avatar variety** — VRChat.
- **Want the deepest live in-world creation tools and a smaller, technical community** — Resonite.

---

*For MCP integration setup and getting started, see the docs in the [resonite-mcp repo](file:///D:/Dev/repos/resonite-mcp) directly — not duplicated here to avoid drift.*







