# Overte

[Overte](https://overte.org) is the actively-maintained open-source
continuation of the original Vircadia/High Fidelity architecture: a C++
desktop client ("Interface"), a domain-server, an entity-server, avatars,
spatial audio, and in-world JavaScript scripting. Maintained by the
nonprofit Overte e.V.

**Not to be confused with**: current "Vircadia," which pivoted to an
unrelated stack ("Vircadia World" — PostgreSQL, Bun/TypeScript, Docker,
OAuth2) that shares no wire protocol, admin API, or client with Overte. If
you see "Vircadia" in older fleet docs, check which one is actually meant —
`overte-mcp` targets Overte specifically, not Vircadia World.

## Fleet MCP server: `overte-mcp`

Repo: `D:\Dev\repos\overte-mcp` — full docs live there, not duplicated here.
Start with [overte-mcp/STATUS.md](file:///D:/Dev/repos/overte-mcp/STATUS.md)
for current verification status and
[overte-mcp/ASSESSMENT.md](file:///D:/Dev/repos/overte-mcp/ASSESSMENT.md)
for the fleet audit history.

### Architecture (real, as implemented)

```
MCP client (stdio) ──┐
React dashboard ──────┼──► FastAPI backend (port 11110)
Interface bridge JS ──┘         │
                                 ├── HTTP → Overte domain-server admin API (port 40100)
                                 │     GET /nodes.json, /settings.json
                                 └── WebSocket bridge (/api/overte/ws)
                                       ↕
                              scripts/overte-mcp-bridge.js
                              (runs inside Overte Interface)
                                       │
                                       ▼
                              Entities.addEntity() / editEntity()
                              → Overte entity-server (octree protocol)
```

Overte's entity-server has no plain "POST an entity" HTTP endpoint — only
Interface's JavaScript API can create/modify in-world entities. That's why
entity spawn and script injection require a bridge script loaded inside a
running Interface client, not just the domain-server.

### Tools

| Tool | What it does | Status (as of 2026-07-30) |
|------|--------------|---------------------------|
| `overte_domain_status` | Queries domain-server `/nodes.json` + `/settings.json` | Verified live |
| `overte_entity_spawn` | Spawns Box/Sphere/Web/Model entities via the Interface bridge | Verified live |
| `overte_script_inject` | Attaches a JS behavior script to an existing entity | Verified live |
| `overte_sampling_assist` | Multi-step planning via `ctx.sample()` | Static plan, not independently tracked |

Every tool response includes a `source: "live"` or `source: "simulated"`
field — simulated responses always carry a `warning` explaining what's
needed to go live. No silent fake success.

### Model formats

Overte supports **FBX, glTF, and OBJ** for Model entities. It does **not**
support VRM as a Model entity format — VRM is an avatar-only format loaded
via `.fst` files, and its skeletal data lives in glTF extensions the entity
pipeline doesn't parse (so `getJointNames()` returns 0 on a VRM loaded as a
Model entity). Convert VRM → GLB first if you need a VRM-sourced model as an
in-world entity with working joints.

### Local dev setup

1. Domain-server + Interface from https://overte.org/downloads.html.
2. Domain-server admin at `http://localhost:40100/settings` — local sandbox
   convention is `admin`/`admin`.
3. Load `scripts/overte-mcp-bridge.js` into Interface (Developer → Script
   Manager → Load Script → From Disk) for live entity/script tools.

Full onboarding: `overte-mcp/docs/ONBOARDING.md`.

## In-headset UX vs. VRChat and Resonite

For the practical differences — locomotion/flying, grabbing objects,
portals (Overte uses the Explore app to jump between domains rather than an
in-world portal object), mirrors, and a reality check on lootboxes (not a
real feature on any of the three platforms) — see
[../SOCIAL_VR_UX_COMPARISON.md](../SOCIAL_VR_UX_COMPARISON.md).

---

*A note on this integrations folder*: the sibling `resonite/README.md` in
this same directory currently describes fictional tooling (an "Antigravity
cognitive core," tools like `inject_protoflux`/`trigger_impulse` that don't
exist in `resonite-mcp`'s actual codebase, a nonexistent "RTX 4099," and a
"SOTA v13.0 compliance" framing with no basis in reality). This overte doc
was written by reading the actual `overte-mcp` source and `STATUS.md`
instead, specifically to avoid repeating that failure mode. The resonite
doc is worth a rewrite on the same basis.
