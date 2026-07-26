# Gestating Chains — Multi-Step Pipeline Catalog

**Purpose:** catalog possible multi-server chains across the fleet, from trivial to fantastical, with an honest feasibility read on each. This folder is where an idea lives *before* it's real enough for a `projects/` build brief or an `architecture/` gap-analysis entry — the gestation period.

**Status:** open-ended, living catalog. Add entries freely. Promote an entry to a real build brief (`architecture/`) when it's ready; leave a pointer here when you do, don't delete the entry.

---

## Tiering

| Tier | Definition | File |
|---|---|---|
| **Simple** | 1–2 hops, tools already exist and are already wired for roughly this purpose, mostly a matter of calling them in sequence | [`simple-chains.md`](./simple-chains.md) |
| **Medium** | 3–6 hops, cross-domain, some genuine new wiring needed, but every individual capability already exists somewhere in the fleet | [`medium-chains.md`](./medium-chains.md) |
| **Fantasy** | Requires capabilities, hardware, or reliability the fleet does not have and mostly can't afford yet — dated with an honest "not before ~Year" estimate, kept for the fun of tracing what it would actually take | [`fantasy-chains.md`](./fantasy-chains.md) |

A chain moves tiers as the fleet grows. Something in `fantasy-chains.md` today (comfyops didn't exist a week ago) can be `medium-chains.md` material next month. Re-file when that happens, with a one-line note of what changed.

---

## Entry template

Every chain entry, regardless of tier, uses this shape (fantasy-tier entries get the fullest version; simple-tier entries can compress §3–§5 to a line each):

```markdown
### <Chain name>

**Tier:** simple / medium / fantasy
**One-line pitch:** <what it does, in plain language>

#### 1. Step chain (TODO list)
1. <server/tool> — <what happens>
2. ...

#### 2. Feasibility / gap analysis
- What already exists and works: ...
- What needs new wiring: ...
- What doesn't exist at all (hardware, capability, API): ...
- Hardest single point of failure: ...

#### 3. Effort estimate
<rough, honest, "days" not "weeks" per the fleet's AI-assisted dev pace — or, for fantasy tier, "not before ~Year, contingent on X">

#### 4. Revenue potential (if any)
<only if the chain plausibly produces something sellable — a physical object, a service, a dataset, a design. Most chains have none; say so rather than stretching for one.>

#### 5. Notes
<anything else — safety gates needed, approval-flow requirements, cross-references to other docs>
```

---

## Index (all entries, all tiers, at a glance)

| Chain | Tier | Status |
|---|---|---|
| Photo → comfyops restyle → Immich | Simple | Speced (Ekphrasis, iOS app plans) |
| Benny FM briefing composition | Simple | Speced |
| VCV patch generate → OSC play test | Simple | Gated on vcv BLOCKER-0 |
| Record fingerprint → Plex ownership check | Simple | Speced (Flohmarkt, iOS backlog) |
| Book query → Calibre RAG → TVTropes cross-ref | Simple | **Already built** (`media_research_book`) |
| Settee → Marble room → Resonite | Medium | Traced in detail, see analysis doc §2.2.1 |
| Boomy ARKit survey → nav map update | Medium | Speced (Boomy's Leash Lane B) |
| PoL escalation state machine | Medium | Speced (own doc: `POL_AND_RECOMBINANT_CAPABILITIES.md`) |
| Ekphrasis capture → LoRA training | Medium | Gated on comfyops Phase 2 |
| Generated song + generated visual → short music video | Medium | Idea only, not speced |
| **FOSS self-hosted Gaussian-splat MCP** (`splatmaker-mcp`, cost alternative to worldlabs, possible community tool) | Medium | Not yet a repo, flagged as coming soon; see medium-chains.md for the blender_splatting collision-mesh implication + Resonite/VRChat community angle |
| Leanforge proof stall → Denkzettel-style filed note | Medium | Idea only, cross-references two iOS backlog items |
| Bumi-with-gripper beer run → custom sensor PCB → fab → assemble → patent | Fantasy | See `fantasy-chains.md`, full breakdown |
| G1 + real BCI direct motor control | Fantasy | See `fantasy-chains.md` |
| Fleet reads a paper and ships its own PR unsupervised | Fantasy | See `fantasy-chains.md` |

---

## Why this folder exists (design note)

The fleet has enough servers now (149+) that most *interesting* new capability isn't "build server N+1," it's "chain three existing servers in a sequence nobody's tried." That's a different kind of idea-generation than a gap-analysis brief, and it wants a lower-ceremony home: no port reservations, no phase gates, no honesty-standard evidence requirements — just "here's a chain, here's how far from real it is." When an entry is ready to actually be built, THAT'S when it graduates to the full standards machinery (`AGENT_PROTOCOLS.md`, port reservation, build brief). This folder is upstream of all of that, on purpose.
