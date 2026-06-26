# Fleet lanes — mission flows vs cross-cutting planes

**Status:** Active doctrine  
**Last updated:** 2026-06-05  
**Companion:** [FLEET_PHILOSOPHY.md](FLEET_PHILOSOPHY.md) (ship classes) · [FLEET_NAMING.md](FLEET_NAMING.md) · [FLEET_CONTROL_PLANE.md](../FLEET_CONTROL_PLANE.md)

---

## Lanes vs planes vs ship classes

| Concept | Question it answers | Example |
|---------|---------------------|---------|
| **Ship class** | What *is* this hull? | Carrier, destroyer, submarine, minesweeper |
| **Mission lane** | What *cargo* flows where? | readly → arxiv → aiwatcher → brief |
| **Plane** | What *cross-cuts* all lanes? | Engineering, agent ops, trust, human command |

A destroyer **belongs to** a ship class and **participates in** one or more mission lanes.  
**MetaMCP is not a mission lane** — it sits on the **Engineering plane** (see below).

---

## Mission lanes (vertical flows)

Canonical **A → B → C** paths. Hulls may appear in multiple lanes.

| Lane | One-line mission | Primary flow | Key hulls | Example sortie |
|------|------------------|--------------|-----------|----------------|
| **Intel** | Know what changed in the world | readly → arxiv → aiwatcher → calibre/email → ViLife brief | readly-mcp, arxiv-mcp, aiwatcher-mcp, glance-mcp, calibre-mcp, email-mcp | WF-001 `intel` node; Office Day Prep intel slice |
| **Life** | Run Vienna as a human | ViLife ↔ transit ↔ shopping ↔ `/fleet` meta | vienna-life-assistant, mywienerlinien, gtfs-mcp, vienna-transit | `vienna_life(life_brief)`; meta dashboard |
| **Office** | Ship work artifacts | Fritz → opencode/git → docs → email → MemOps ADN | fleet-agent-mcp, opencode-cli-mcp, git-github-mcp, docs_mcp, email-mcp, advanced-memory-mcp | `day_prep`; PR pipeline; board pack |
| **Comms** | Reach Sandra on a channel | agent decision → comms → human reply loop | email-mcp, discord-mcp; **P4 comms-mcp** (Telegram) | Outbound digest; inbound “reply yes/no” |
| **Media** | Acquire, library, play | arr → plex/jellyfin → virtualdj / immich | arr-mcp, plex-mcp, jellyfin-mcp, immich-mcp, dj-media-hub | “Add season, watch tonight” |
| **Creative** | Make assets & worlds | worldlabs → blender/davinci → godot/unity → export | worldlabs-mcp, blender-mcp, davinci-resolve-mcp, godot-mcp, suno-mcp | Scene + render + publish |
| **Robotics** | Sim + VLA + motion (not ViLife) | vla-mcp → sim/gazebo → yahboom/teleoperator → osc | **vla-mcp**, robotics-mcp, yahboom-mcp, ag-gazebo-bridge, teleoperator-mcp | `vla_pipeline`; fleet ingest → aiwatcher |
| **VR / Social** | Presence & avatars | avatar/vroid → unity/resonite/vrchat → osc | vrchat-mcp, resonite-mcp, avatar-mcp, vroidstudio-mcp, unity3d-mcp | World upload; OSC parameter drive |
| **Home** | Sense & act on physical house | devices → home-assistant → ring/nest → alexa | devices-mcp, home-assistant-mcp, ring-mcp, nest-protect-mcp, alexa-mcp | Alarm, camera, TTS alert |

**Renamed from FLEET_PHILOSOPHY “Physical lane”:** split into **Robotics** (motion/VLA) and **VR/Social** (embodiment/social VR). Overlap at OSC — both lanes may use `osc-mcp`.

---

## Cross-cutting planes (horizontal)

These are **not** cargo lanes. They **serve** every lane.

| Plane | Role (naval) | Flagship / core hulls | When agents call here |
|-------|--------------|----------------------|------------------------|
| **Human command** | Flag bridge (human) | **vienna-life-assistant** (ViLife) | “What’s on today?” “Open fleet grid.” |
| **Agent ops** | Flag bridge (agent) | **robofang**, fleet-agent-mcp (Fritz), fleet_bridge | Install, health, heartbeat, YAML workflows |
| **Engineering** | **Shipyard / naval architect** | **meta_mcp** | Repo surgery, scaffold, Tool Lab, fleet analysis, inspire_repo |
| **Trust** | Minesweepers + drydock security | mcp-test-suite, secrets-mcp, sync-fleet-registry, deepfang | Before creds, before new destroyer, smoke CI |
| **Infra / tender** | Fuel & tugs | mcp-central-docs, docker-mcp, virtualization-mcp, backupops, multi-backup-mcp | Ports, VMs, backups, standards |
| **Memory** | Logbook & charts (submarine) | advanced-memory-mcp (MemOps) | ADN, notes, tiered RAG after any lane completes — see [P6 spec](specs/P6-memops-stabilization.md) |

### Where is MetaMCP?

**Primary home: Engineering plane.**

| MetaMCP does | Lane? |
|--------------|-------|
| Scaffold new `*-mcp`, diagnose broken server, Tool Lab, repo structure cards | **Engineering** ✓ |
| Run / suggest fleet smoke, registry hygiene | **Trust** (secondary) |
| Operate Plex, calendar, or robots directly | **No** — route to lane destroyer |

**Rule:** MetaMCP **builds and repairs hulls**; it does not **sail them on a mission**.  
Analogous to ViLife on **Human command** and RoboFang on **Agent ops** — three carriers, three planes.

```text
  Human command (ViLife)     Agent ops (RoboFang/Fritz)     Engineering (MetaMCP)
           \                           |                            /
            \                          |                           /
             -------- Mission lanes (Intel, Life, Media, …) --------
                                    |
                          Trust + Infra under everything
```

---

## Lane ↔ ship class cheat sheet

| Lane | Typical ship classes |
|------|---------------------|
| Intel | Submarines + knowledge destroyers |
| Life | **Carrier** (ViLife) + frigates |
| Office | Landing craft + submarines (Fritz, MemOps) + code destroyers |
| Comms | Landing craft + comms destroyers |
| Media / Creative | Destroyers + frigates |
| Robotics / VR | Destroyers + frigates |
| Home | Destroyers (devices = gold standard) |
| Engineering | **Carrier** (MetaMCP) only |
| Trust | Minesweepers + tenders |
| **LCS** (satire) | **No lane assignment** — weak hulls; not mission-critical |

**LCS repos do not get a shipping lane.** They are dock ornaments until promoted or scrapped. See [FLEET_PHILOSOPHY.md § LCS](FLEET_PHILOSOPHY.md).

---

## Multi-lane workflows

| Workflow | Lanes touched | Nodes |
|----------|---------------|-------|
| **WF-001 morning_brief** | Intel → Life → Office (MemOps) | glance → aiwatcher → vienna-life → memory |
| **Office Day Prep** | Intel + Office + Life (partial) | aiwatcher pulse, opencode inspect, ViLife context |
| **Code-hunt drop** | Intel (+ Robotics signal) | arxiv code-hunt → aiwatcher ingest → optional ViLife card |
| **Media night** | Media only | arr → plex → virtualdj |
| **Robot sortie** | Robotics (+ Intel if logged) | vla-mcp → yahboom → aiwatcher ingest on completion |

Define new workflows by **listing lanes first**, then picking one hull per step.

---

## Agent routing (quick)

| User intent | Plane first | Then lane |
|-------------|-------------|-----------|
| Fix / scaffold / analyze a repo | **Engineering** → meta_mcp | — |
| Fleet health / install MCP | **Agent ops** → robofang | — |
| Morning digest, papers, magazines | — | **Intel** |
| Calendar, shopping, fleet grid | **Human command** → ViLife | **Life** |
| Send Telegram / email | — | **Comms** |
| Robot / VLA / Yahboom | — | **Robotics** (alias `vla-robotics`, not ViLife) |
| VRChat / Resonite avatar | — | **VR / Social** |
| Credentials / smoke / registry | **Trust** | — |

---

## Honing notes (open)

1. **email-mcp** spans **Intel** (digest delivery) and **Comms** (bidirectional) — tag by *operation*, not hull.
2. **glance-mcp** is Intel-adjacent (RSS/probes) but also **Trust** (fleet probe) — WF-001 uses it as intel preamble.
3. **observability-mcp** — candidate **Trust** or sub-plane of Agent ops; not yet assigned a mission lane.
4. **ednaficator** (revival) — conversational **Agent ops** launcher across lanes (P2 decision).

---

## Related

- [FLEET_PHILOSOPHY.md § Harbors & shipping lanes](FLEET_PHILOSOPHY.md) — original four lanes (subset of this doc)
- [FLEET_GAP_CLOSURE_ROADMAP.md](FLEET_GAP_CLOSURE_ROADMAP.md) — P4 comms lane, P5 trust plane
- [META_DASHBOARD.md](META_DASHBOARD.md) — Life lane L3 surface
