# Fleet philosophy — naval metaphor & ship classes

**Status:** Active doctrine  
**Last updated:** 2026-06-05  
**Companion:** [FLEET_GAP_CLOSURE_ROADMAP.md](FLEET_GAP_CLOSURE_ROADMAP.md) · [FLEET_CONTROL_PLANE.md](../FLEET_CONTROL_PLANE.md)

---

## Why naval?

The fleet is not a monolith. It is a **task force**: heterogeneous hulls with different ranges, crews, and missions. Agents need a **doctrine** — which ship to call, which harbor to return to, which carrier launches the landing craft.

Naval metaphor maps cleanly onto the Sandra-class MCP stack:

| Naval concept | Fleet equivalent |
|---------------|------------------|
| **Home port** | Vienna (Alsergrund) — data residency, daily life, transit |
| **Task force** | Cursor + RoboFang + enabled MCP servers |
| **Flag bridge** | Meta dashboard (VLA) + RoboFang hub (ops) |
| **Charts & logs** | mcp-central-docs, MemOps, fleet-registry |
| **Rules of engagement** | DeepFang, secrets-mcp, AGENT_PROTOCOLS |

---

## Ship classes

### Aircraft carriers — command & launch

**Role:** Carry many capabilities; launch sorties; never do every job themselves.

| Ship | Repo | Mission |
|------|------|---------|
| **CVN — Vienna Life** | `vienna-life-assistant` | **Flagship for human life** — calendar, todos, expenses, shopping, meta dashboard above all webapps |
| **CVN — RoboFang** | `robofang` | **Flagship for agent ops** — install, launch, health, Council, Hands heartbeat |
| **CVN — MetaMCP** | `meta_mcp` | **Flagship for fleet engineering** — diagnostics, Tool Lab, scaffolding, fleet analysis |

**Doctrine:** Carriers **aggregate and route**. They do not replace destroyers. VLA opens Plex dashboard; it does not transcode video.

### Destroyers — domain superiority

**Role:** Heavy, self-contained MCP servers for one battlespace. SOTA webapp + portmanteau tools.

Examples:

| Destroyer | Domain |
|-----------|--------|
| `devices-mcp` | Home security (Gold Standard) |
| `blender-mcp` | 3D / VFX |
| `plex-mcp` / `jellyfin-mcp` | Media library |
| `calibre-mcp` | Knowledge library |
| `robotics-mcp` / `yahboom-mcp` | Physical motion |
| `chip-design-mcp` | Silicon |

**Doctrine:** One destroyer per sea. Do not build a second Plex MCP — extend the destroyer.

### Frigates — composite & federation

**Role:** Escort groups; mount multiple destroyer capabilities behind one gateway.

| Frigate | Mounts |
|---------|--------|
| `dj-media-hub` | VirtualDJ + Plex |
| `ai-producer-hub` | Music production stack |
| `mcp-federation-hub` | 80+ server orchestration |
| `universal-actuator-mcp` | Plex + Calibre + Immich discovery |

**Doctrine:** Frigates reduce **agent tool count** for common missions.

### Landing craft — sorties from carriers

**Role:** Small, fast, mission-specific; launched from carrier workflows; return to port.

| Craft | Example |
|-------|---------|
| Fritz workflows | WF-001 morning brief |
| `email-mcp` send | One message sortie |
| `comms-mcp` (planned) | Telegram reply |
| `fastsearch-mcp` | NTFS needle query |

**Doctrine:** Landing craft are **chained steps**, not permanent infrastructure. Fritz YAML defines beachheads.

### Submarines — silent & deep

**Role:** Background, always-on, low UI; intelligence and memory.

| Submarine | Role |
|-----------|------|
| `advanced-memory-mcp` (MemOps) | Long-term memory, ADN, RAG |
| `aiwatcher-mcp` | News distillation, urgency |
| `glance-mcp` | RSS, probes, weather |
| `fleet-agent-mcp` (Fritz) | Heartbeat, cron, PR pipeline |
| `observability-mcp` | Fleet telemetry |

**Doctrine:** Submarines **surface findings** to carriers (digest → VLA dashboard, alert → comms).

### Minesweepers — trust & safety

**Role:** Clear phantom capabilities before the fleet sails.

| Minesweeper | Role |
|-------------|------|
| `mcp-test-suite` | Contract smoke |
| `sync-fleet-registry.ps1` | Catalog truth |
| `secrets-mcp` (planned) | Credential hygiene |
| `deepfang` | Execution isolation |

**Doctrine:** **Minesweepers lead the convoy.** No new destroyer without registry entry and smoke pass.

### Tenders & supply — infrastructure

**Role:** Keep the fleet fueled; no glamour.

| Tender | Role |
|--------|------|
| `mcp-central-docs` | Standards, ports, planning |
| `mcp-server-template` | New hull fabrication |
| `multi-backup-mcp` | Archive & nuclear backup |
| `docker-mcp` / `virtualization-mcp` | Compute substrate |

### Hospital ship — quarantine

**Role:** Ships too damaged to sail with the fleet; repair or decommission.

Current quarantine: `sdr-mcp`, `vbox-mcp`, `mcp-links-service`. Reviving: `ednaficator`.

### LCS — littoral combat ship (satire class)

**Role:** The joke hull class for repos that **cost a lot of ambition, deliver littoral combat with no combat**, and make taxpayers (Sandra) wonder why we bought them.

Named after the US Navy [Littoral Combat Ship](https://en.wikipedia.org/wiki/Littoral_Combat_Ship) program — modular, expensive, mission package swaps, chronic reliability jokes, eventual early retirement. **Not an insult to contributors; an insult to scope creep.**

| Signal in registry | Meaning |
|--------------------|---------|
| `priority: weak` | LCS candidate — sails, barely; do not task-force it |
| Duplicate of a carrier | Promoted to **hospital ship** (e.g. `vienna-live-mcp`) |
| `status: quarantined` | Drydock — worse than LCS; do not invoke |

**Doctrine:**

1. **Do not chain LCS hulls in Fritz workflows** — use the destroyer that actually works.
2. **No new features** until promoted to frigate or decommissioned.
3. Agents may **mention** LCS in banter; MemOps tags: `lcs`, `weak`, `scope-creep`.

**Current fleet LCS (registry `priority: weak`):** `vroidstudio-mcp`, `suno-mcp`, `virtualdj-mcp`, `vienna-live-mcp` (also quarantined — double failure: duplicate *and* LCS).

**Promote out of LCS when:** smoke passes, one documented lane mission, no duplicate carrier.

---

## Harbors & shipping lanes

```text
                    ┌─────────────────────────────────────┐
                    │  VIENNA (home port)                 │
                    │  vienna-life-assistant — human UI   │
                    │  Meta dashboard → all webapps       │
                    └──────────────┬──────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
   RoboFang (agent CVN)      MetaMCP (eng CVN)         MemOps (submarine)
         │                         │
         └────────────┬────────────┘
                      ▼
              Destroyers / Frigates
              (individual *-mcp webapps)
```

**Shipping lanes (data flows):** — full taxonomy in [FLEET_LANES.md](FLEET_LANES.md)

- **Intel lane:** readly → arxiv → aiwatcher → email/calibre → ViLife brief
- **Life lane:** ViLife ↔ transit ↔ shopping ↔ meta dashboard
- **Office / Comms lanes:** Fritz workflows, opencode, email; P4 comms-mcp
- **Media lane:** arr → plex/jellyfin → virtualdj
- **Creative lane:** worldlabs → godot → steam
- **Robotics lane:** vla-mcp → sim → yahboom → osc (not ViLife — see [FLEET_NAMING.md](FLEET_NAMING.md))
- **VR / Social lane:** avatar → vrchat/resonite → osc
- **Cross-cutting planes:** Human command (ViLife), Agent ops (RoboFang/Fritz), **Engineering (MetaMCP)**, Trust, Infra

---

## Rules of engagement (agent-facing)

1. **Ask the carrier first** — life → ViLife; fleet ops → RoboFang; repo surgery → MetaMCP (**Engineering plane**, not a mission lane).
2. **Do not invoke quarantined hulls** — check `fleet-registry.json` `status`.
3. **Chain landing craft via Fritz** — multi-step missions use workflows, not improvisation.
4. **Log to MemOps** — every significant mission leaves an ADN or note.
5. **Depth over breadth** — new destroyer requires minesweeper clearance (P5 + P1).

---

## Centering Vienna

Vienna is not just a locale — it is the **why** of the fleet:

- Transit (`mywienerlinien`, `gtfs-mcp`) — move through the city
- Life admin (`vienna-life-assistant`) — time, money, shopping
- Residency (`ednaficator` vision) — data stays local/Austria where possible
- Culture pages in VLA — coffee, museums, Musikverein

**The meta dashboard lives on the Vienna carrier** because the human commander lives there. RoboFang remains the agent-facing bridge.

---

## Related docs

- [META_DASHBOARD.md](META_DASHBOARD.md) — architecture above repo webapps
- [robofang AGENTIC_OS_PHILOSOPHY](file:///D:/Dev/repos/robofang/docs/AGENTIC_OS_PHILOSOPHY.md)
- [FLEET_CONTROL_PLANE.md](../FLEET_CONTROL_PLANE.md)
