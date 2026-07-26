# Platform Alternatives — Considered, Not Chosen (Yet)

**Created**: 2026-07-18. Side-quest research, parked here so it doesn't need
re-deriving later. Neither platform below changes the Resonite Living plan;
both are documented so "come back to it later" actually works.

---

## Vircadia — FOSS virtual world, viable later, not now

**What it is**: Apache 2.0, fully open source, a continuation of the old
High Fidelity VR platform. Distributed architecture (domain server +
assignment clients + client). Maintained by DigiSomni LLC, genuinely active
(commits into Jan 2026). Development focus has shifted from the old native
(Qt/C++) desktop client toward **"Vircadia World"** — a web-first stack:
Babylon.js browser client ("Aether") + TypeScript SDK ("Ananke"). So
"Vircadia" today increasingly means a browser/WebXR platform, not a
native-VR-first one the way Resonite is.

**Population** (checked 2026-07-18, not assumed):

| Metric | Resonite | Vircadia |
|---|---|---|
| Discord members | ~11,459 | ~1,111 (~10x smaller) |
| Concurrent players | ~119-235 (Steam, May 2026) | not trackable/visible anywhere |

Resonite is itself a niche VR platform. Vircadia is empty next to a
platform that's already small — most substantive public writeups about it
date to 2020, not 2025/2026, which is itself a signal of low current
mindshare.

**Capability**: real entity-scripting model (JS/TS — Interface/Client
Entity/Avatar/Server Entity/Assignment Client scripts), self-hostable,
fits a FOSS/data-sovereignty ethos well. No confirmed native VRM import —
would need conversion into Vircadia's own avatar packaging format.
(A search result conflated Vircadia with VIVERSE, HTC's *separate*
commercial metaverse platform, which does support VRM — different product,
don't reuse that claim without re-checking.)

**Verdict**: not a Resonite replacement for this project — we already have
ResoniteLink proven end-to-end, and Vircadia's thin ecosystem (avatar
tooling, community troubleshooting, content) makes every phase harder for
no benefit right now. The population gap barely matters for a *private*
home (no neighbors needed), but the ecosystem gap does. Plausible **later**
as a browser-accessible mirror of the home for people without Resonite
installed (Marion, Steve). Candidate future module: `vircadia-mcp`, once
Resonite Living's Phases 1-5 are further along.

Sources: [vircadia.com](https://vircadia.com/) ·
[vircadia-web](https://github.com/vircadia/vircadia-web) ·
[vircadia-web-sdk](https://github.com/vircadia/vircadia-web-sdk) ·
[Vircadia World Babylon.js client](https://vircadia.com/vircadia-world/client/web_babylon_js/) ·
[Entities API docs](https://apidocs.vircadia.dev/Entities.html) ·
[Vircadia Discord](https://discord.com/invite/Pvx2vke) ·
[Resonite Discord](https://discord.com/invite/resonite) ·
[Resonite Steam Charts](https://steamcharts.com/app/2519830)

---

## VRChat — still genuinely hard to build in and automate creation for

**Population** (checked 2026-07-18): ~51,600 concurrent (Steam, 2026),
~44,600 30-day average, all-time peak ~78,600 (mid-Feb 2026) — Steam only,
Quest standalone adds more. Roughly 200-400x Resonite's concurrent count.
Not remotely a ghost town, unlike Vircadia. **The reason we're not building
Resonite Living there isn't population — it's the creation pipeline.**

**World creation**: Unity Editor + VRChat Worlds SDK (installed/managed via
VRChat Creator Companion) + Udon. Everything is authored offline in a Unity
scene, then built and uploaded through VRChat's pipeline — there is no live
external API into a running world's scene graph. A polished original world
realistically takes 20-100+ hours. Udon itself is deliberately sandboxed
(Node Graph visual scripting, or UdonSharp — C#-like but compiles to a
restricted VM with no arbitrary reflection/file access), a defensible
security/moderation trade-off given VRChat's much larger public audience,
but it closes off exactly the kind of external, live, agent-driven content
authoring that ResoniteLink gave us this week (connect → read the live data
model → addSlot/addComponent → done, no Editor, no build step, no upload).
VRChat's SDK does expose a public API hook for automating the *build/
upload* pipeline (validations, custom build steps) — genuinely useful for
CI, but that automates packaging content a human already authored in Unity,
not live scene construction by an agent. This is the concrete substance
behind the master plan's "sleepy" verdict on VRChat: it's specifically the
content-creation side that hasn't moved, not the whole platform.

**Correction, 2026-07-18 (later same session)**: "no live external API"
needed a footnote after actually reading `unity3d-mcp`'s source rather than
its README. Scene assembly (create/transform/delete objects, import
Blender/Marble assets, preflight validation) genuinely IS automatable via
`unity3d-mcp`'s `unity_bridge` (live Editor bridge, MCPBridge.cs, port
10835) — real, verified-against-source capability, not aspirational. What
remains manual and structural: Udon interactivity authoring, and the
VRChat SDK's world Build & Publish step (`unity3d-mcp`'s `vrchat` tool
only wraps avatar upload, not world upload — no `publish_world` operation
exists). Full writeup, with the exact pipeline and honest gap list:
`vrchat-mcp/docs/Building_VRChat_Worlds_With_Unity3D_MCP.md`.

**Where VRChat automation is genuinely good: OSC.** Real-time, well
documented (docs.vrchat.com), two APIs — Avatar Parameters (read/write,
drives expressions/animations/custom behaviors) and Input Control
(simulates movement/look/jump/VR input). Active community ecosystem
(HTTP-to-OSC bridges, MCP integrations already exist in the wild). The
fleet already has this lane covered: `vrchat-mcp` (v3.1.1+.0+) does
real-time OSC control of avatars and assets. So "puppet an avatar's
expressions/behavior in an existing VRChat world" is a solved, live
problem for us already — it's specifically "generate and inject new world
content via automation" that VRChat still can't do, and that's exactly
what Phases 1-4 of Resonite Living need.

**Verdict**: no reason to reconsider VRChat for Resonite Living. The
population advantage is real but irrelevant to a private home. The actual
blocker — no live external content-authoring API, Unity-Editor-only world
building — is unchanged and structural, not a temporary gap. `vrchat-mcp`
stays useful for its narrow OSC lane (cross-platform avatar puppeting, if
that ever comes up) but isn't a substitute for what ResoniteLink now gives
us.

Sources: [VRChat World Creation Guide (2026)](https://creators.vrchat.com/worlds/creating-your-first-world/) ·
[Udon docs](https://creators.vrchat.com/worlds/udon/) ·
[VRChat SDK wiki](https://wiki.vrchat.com/wiki/VRChat_SDK/en) ·
[OSC Overview](https://docs.vrchat.com/docs/osc-overview) ·
[OSC Avatar Parameters](https://docs.vrchat.com/docs/osc-avatar-parameters) ·
[VRChat OSC for Avatars announcement](https://hello.vrchat.com/blog/vrchat-osc-for-avatars) ·
[VRChat Steam Charts](https://steamcharts.com/app/438100)
