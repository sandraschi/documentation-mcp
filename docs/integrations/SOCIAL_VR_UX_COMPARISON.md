# Social VR: How the Actual Experience Differs (VRChat / Resonite / Overte)

Practical, in-headset differences — not MCP integration, not architecture.
For "what does it feel like to actually be in this thing," see below. Cross-
links from each platform's own integration folder (`../resonite/`,
`../overte/`); VRChat has no MCP server in this fleet yet, so this is the
only home for VRChat UX notes so far.

Grounded in official docs/wikis where cited; anything without a citation is
lower-confidence or platform-generic and flagged as such — don't take it as
gospel without checking in-headset.

---

## Locomotion (walking, running, flying)

| | VRChat | Resonite | Overte |
|---|---|---|---|
| Default movement | Walk (analog stick / WASD), no native flight | Walk, with <cite index="66-1">flying implemented as a movement method by default</cite> | Configurable — Settings → Controls exposes <cite index="81-1">jumping, flying, and leaning behavior</cite> |
| Flight | Not native — <cite index="82-1">"Openflight" is a client-side mod, applies movement client-side, no avatar edits required"</cite> (against VRChat's rules to use); some worlds grant flight via world-specific scripts | On by default, no mod needed | Built-in toggle, on by the sound of the docs page but not stated as default |
| Hand-tracking gesture movement | Yes on Quest — <cite index="86-1">pinch your middle finger to thumb, move hand away from the sphere that appears to move in that direction</cite> | Not confirmed | Not confirmed |
| Teleport | Some worlds/admin tools implement it; not the platform default | Not the primary paradigm (flying is) | Configurable per the same Controls menu |

**Takeaway**: Resonite is the only one of the three where unrestricted flight
is a baked-in, always-available movement mode — in VRChat you're normally
walking unless a specific world or an against-the-rules client mod grants
flight; Overte exposes it as a setting but the docs don't frame it as "on by
default" the way Resonite's community explicitly does.

## Grabbing / picking up objects

**VRChat**: first-party `VRC_Pickup` component. <cite index="73-1">Adding it to an object automatically adds a Rigidbody if there wasn't one, and combined with Object Sync, position syncs for all players and ownership transfers to whoever picks it up.</cite> Two grab detection modes: <cite index="76-1">raycast (laser from your hand in VR, or head in desktop mode) for far objects, and proximity for close ones.</cite> World creators explicitly opt objects into being grabbable; nothing is grabbable by default.

**Resonite**: grabbing is a platform-wide default behavior, not something a world creator has to individually enable per-object the way VRChat requires — <cite index="120-1">any object can interact with (and to some extent modify) any other object,</cite> and the same live in-world editing philosophy extends to what you can pick up and manipulate directly, including modifying other users' worlds/avatars if permissions allow. There's also a genuinely unique trick: <cite index="116-1">"Grab Smuggling," a way to transfer items across worlds</cite> by holding something while you switch sessions — this doesn't exist as a concept in VRChat, where inventory/asset transfer between worlds isn't a "hold it and walk through" mechanic.

**Overte**: entity grab/interaction exists via the Interface JS API (`Entities` grabbable properties), same general idea as VRChat's opt-in pickups, but not independently verified here — less documented than the other two, flagging honestly rather than guessing specifics.

## Mirrors

**VRChat**: first-party `VRCMirror` prefab, real-time reflection, <cite index="78-1">drag it into your scene, position/rotate/scale, and reflection layers (e.g. Pickup, Walkthrough) are configurable</cite> — a very common, expected fixture in social worlds (checking your avatar is a core VRChat ritual).

**Resonite / Overte**: mirrors exist in both (real-time reflective surfaces are a standard feature of both engines), but the specifics of how they're placed/configured weren't independently verified for this doc — don't take VRChat's level of detail here as implying the other two lack mirrors, just that this doc hasn't confirmed the exact mechanism for either yet.

## Portals / traveling between worlds

This is the most structurally different area across the three platforms.

**VRChat**: a genuine first-party in-world object. <cite index="99-1">Portals can be present statically in worlds or 'dropped' by users — walking forward into one transfers you to the associated world/instance, and dropped portals carry a 30-second countdown timer that resets when someone enters.</cite> World creators add the `VRCPortalMarker` prefab and set a target world/room ID directly in Unity.

**Resonite**: no single first-party "portal object" — the equivalent is **built by the community using ProtoFlux**, via nodes like `WorldSessionID`/`WorldSessionURL` — <cite index="110-1">useful for making world switchers, or keeping a reference to a session for a keycard-like system where each room is actually a portal to a different currently open world.</cite> Complementary concept: **World Orbs** — <cite index="116-1">saving a world spawns a World Orb, which is a link to the world (the world itself lives in your Worlds tab), not the world's content directly</cite> — these can be carried, placed, and grabbed like any other object. So "portal" in Resonite is a ProtoFlux-built pattern layered on top of session/world-link primitives, not a single built-in component — another concrete example of why "ProtoFlux is real and important" matters: this is exactly the kind of platform feature Resonite implements by giving users the tool to build it themselves rather than shipping it pre-made.

**Overte**: no in-world portal object either — the platform-level mechanism is the **Explore app**, which <cite index="91-1">lets you explore other domains created in Overte and visit friends' virtual worlds</cite> — closer to a world browser/directory you open from a menu than something you walk through in-world. Same general shape as Resonite's World Browser, structurally different from VRChat's walk-through object.

## Sessions / instances — same idea, different vocabulary

- VRChat: a world can have multiple **instances** running simultaneously, each with a capacity and access type (public/friends/private/group).
- Resonite: a **session** is an instance of a world; <cite index="111-1">a session has exactly one host — if the host quits, the session closes</cite> — and per <cite index="122-1">Wikipedia's summary, you can be present in multiple worlds/sessions at the same time,</cite> switching focus between them (confirmed independently by the FAQ's session-switching description).
- Overte: a **domain** is closer to "a server you connect to" than "an instance of a shared published thing" — domains are self-hosted, so there's no central "instance list" the way VRChat/Resonite have; discovery happens through the Explore app rather than a unified public world directory.

## Lootboxes / gacha — reality check

**None of the three platforms have a first-party lootbox or gacha mechanic.**
Don't take "lootboxes" as a real platform feature anywhere here — the actual
analogs are:
- VRChat: an avatar **marketplace** (paid avatars/assets from creators,
  browsed and purchased directly — not randomized)
- Resonite: **public inventory folders** other users favorite/link to (not
  owned, not randomized, can be deleted by the owner)
- Any gacha/lootbox-style content that exists is a **community-built
  minigame** inside a specific world (a ProtoFlux or Udon script someone
  wrote), not a platform mechanic — treat any specific claim about "the
  lootbox system" in any of these three as almost certainly about one
  particular custom world, not the platform itself.

---

## What's confirmed vs. what needs a live check

Confirmed against official wikis/docs (cited above): VRChat pickups,
mirrors, portals, controls; Resonite flying-by-default, sessions, World
Orbs, ProtoFlux world-switching pattern, Grab Smuggling; Overte's Explore
app and configurable movement settings.

**Not yet independently verified** — worth an actual in-headset session
before writing anything more specific: Overte's grab/interaction UX details,
Overte's mirror implementation, Resonite's exact mirror placement workflow,
and any VR-hand-tracking-gesture equivalents in Resonite/Overte beyond
VRChat's confirmed pinch-to-move gesture.

---

## Godot: same primitives, no platform

`godot-mcp` doesn't belong in the table above as a fourth competitor —
Godot is a general-purpose game engine, not a social-VR platform. There's
no built-in avatar system, no multiplayer social layer, no world directory,
no account system. Everything VRChat/Resonite/Overte give you out of the
box, Godot makes you build yourself — which is exactly the point. A portal
that drops you into a Gaussian-splat scene is a *world someone builds*,
not a *feature the platform ships*.

Concretely, the fleet owner's own project is the working example: a
primitive game with a portal leading into a splat world, built in Godot —
functionally the same idea as a VRChat `VRCPortalMarker` or a
Resonite ProtoFlux world-switcher, except every piece of it (the portal
trigger, the transition, the splat rendering) is bespoke code rather than a
platform-provided component.

### Where the primitives actually overlap

| Primitive | VRChat | Resonite | Overte | Godot |
|---|---|---|---|---|
| Portal | First-party `VRCPortalMarker` component | Community-built via ProtoFlux (`WorldSessionID`/`WorldSessionURL`) + World Orbs | Explore app (menu-based, not in-world object) | Bespoke — you write the trigger/transition yourself |
| Gaussian splats | No first-party support found | No first-party support found | Just getting real import support (`nianticlabs/spz`, via `overte-mcp`'s fix) | **Native** — `godot_import_splat` ships a custom billboarded Gaussian shader for `.ply`/`.spz` |
| World-building | In-world (own tools) or Unity SDK upload | Fully in-world, live, collaborative | Model entities via Interface | Full editor, offline, not collaborative-live the way Resonite is |

The splat row is the interesting one: `godot-mcp` is actually the most
mature of the four fleet repos at Gaussian-splat handling right now — it
has a real import pipeline with a custom Gaussian shader. Its `.spz` decode
path had the same class of bug found in `overte-mcp` (worse, in fact — it
was treating real Niantic SPZ as gzip-compressed PLY, which was never
correct even for legacy files, not just incompatible with v4) — fixed
2026-07-30 using the same official `nianticlabs/spz` library.

### Why Godot is worth keeping in the comparison at all

Not because it's a competitor, but because it's the "no training wheels"
version of the same underlying problems every one of these platforms
solves for you: how do you get a player from one space into another
(portal), how do you render a captured real-world scene as an explorable
space (splats), how do you let non-programmers build interactive behavior
(scripting — see below). Seeing how Godot handles these with zero platform
scaffolding clarifies what VRChat/Resonite/Overte are actually giving you
for free.

---

## Scripting compared

| | VRChat (Udon) | Resonite (ProtoFlux) | Overte | Godot |
|---|---|---|---|---|
| Paradigm | Visual graph **or** text (your choice) | Visual graph **only** | Text only | Text only (visual scripting removed) |
| Text language | UdonSharp — <cite index="127-1">limited C# syntax, similar to Unity's built-in C# scripting</cite> | None | JavaScript — <cite index="135-1">runs on the V8 scripting engine, with support for both JavaScript and WebAssembly</cite> | GDScript (Python-like), or C#/C++ via GDExtension |
| Visual language | Udon Node Graph — <cite index="126-1">"noodles" connecting nodes, compiles to Udon Assembly bytecode</cite> | ProtoFlux — live, collaborative, edited directly in-world | None | None (removed in 4.0, see below) |
| Execution model | <cite index="126-1">Sandboxed VM interpreting Udon Assembly bytecode — a select set of approved operations, since untrusted worlds run on other users' machines</cite> | Runs directly in FrooxEngine; sandboxing model not independently confirmed here | Runs directly in V8 per script type (Interface/Client Entity/Avatar/Server Entity/Assignment Client — <cite index="137-1">five distinct script types with different entity visibility scopes</cite>) | Compiled/interpreted directly, no untrusted-multiplayer sandboxing concern (single-author or trusted-team context) |
| Live editing | No — compile step, then upload/reload world | **Yes** — edited live, in-headset, collaboratively, no compile step | Load/reload a script file; no live in-world node editing | No — standard edit/save/run cycle in the editor |
| Debugging | ClientSim or Build & Test in Unity Editor | Watch data flow through wires directly in-world | <cite index="139-1">Interface script errors visible via debug output; server entity scripts use the Server Entity Script Log</cite> | Standard IDE debugger, breakpoints, full toolchain |

### The interesting pattern: visual scripting correlates with live multiplayer, not with target audience

Godot deliberately **removed** its visual scripting language in version 4.0
— <cite index="145-1">despite continuous effort it never gained traction, and a poll of over 5000 respondents found only 0.5% of the user base used VisualScript as their main engine language.</cite> Meanwhile VRChat and Resonite both lean on visual scripting as a first-class (Resonite: the *only*) authoring path, and it works well for them.

The difference isn't "programmers vs non-programmers" — Godot's audience
includes plenty of non-programmers too, and GDScript wasn't the barrier for
most of them, per Godot's own postmortem. The actual difference is **live,
in-world, collaborative editing**. ProtoFlux and Udon Graph both exist
inside a persistent multiplayer space where a compile-upload-reload cycle
would break the "explore and tinker together" experience the platform is
selling. Godot has no equivalent constraint — you're editing a project
offline, alone or with your team, then shipping a build — so the value
visual scripting offers (see the logic spatially, no compile/test cycle,
edit while others watch) doesn't offset its costs (harder to search, diff,
version-control, or scale to large codebases) the way it does for
Resonite/VRChat.

This also explains why Overte, despite being the most similar platform to
Resonite (shared HiFi lineage), never adopted a ProtoFlux/Udon-Graph
equivalent — it grew out of a High Fidelity codebase built around a
straightforward embedded JS engine, not around a live-collaborative-editing
philosophy the way FrooxEngine and Udon were designed for from the start.

