# Medium Chains (3–6 hops, cross-domain, some new wiring needed)

Per [`README.md`](./README.md) template.

---

### Settee → Marble room → Resonite

**Tier:** medium
**One-line pitch:** design a Louis XIV settee, generate a room for it, walk into it in social VR.

#### 1. Step chain
1. worldlabs-mcp — generate the room as a Marble Gaussian-splat world.
2. blender-mcp `blender_splatting` — import splat, generate **collision mesh** (the load-bearing step — see §2 below).
3. blender-mcp `blender_ai_generate` (Tripo/Rodin/Hunyuan) — the settee mesh, period-styled prompt.
4. comfyops-mcp — optional: generate gilt-wood / brocade reference textures, feed into Blender's shader graph.
5. blender-mcp `blender_vision_refine` — screenshot-review the settee before proceeding.
6. Compose — place settee on the collision-mesh floor.
7. blender-mcp `blender_export` → Resonite target (combined or separate — open design choice, see below).
8. resonite-mcp — world injection (ResoniteLink, OSC), settee placement if exported separately.
9. Hop in (human step, outside the pipeline).

#### 2. Feasibility / gap analysis
- Already works: every individual tool call above exists in blender-mcp and worldlabs-mcp today. worldlabs' generation response already includes `assets.mesh.collider_mesh_url` (a GLB collision mesh) alongside the splat — the pipeline does NOT need Blender to compute one from scratch; `blender_splatting`'s collision-mesh tool is a fallback, not the default path.
- New wiring needed: nobody's walked this exact sequence end to end; the outbox/inbox/ack contract (deep analysis §3.2) doesn't exist yet for either handoff (worldlabs→Blender, Blender→Resonite).
- Hardest single point of failure: **making sure the collider mesh is actually requested, downloaded, and handed off** — it exists on worldlabs' server whether or not the pipeline code remembers to ask for it, so the realistic failure mode is a plumbing bug (only `spz_urls` fetched, `collider_mesh_url` silently dropped), not a missing capability. Textbook case for the §3.2 manifest tracking it as its own artifact.
- Real bug surfaced while tracing this: worldlabs-mcp's README cites its Blender bridge as port 10740; blender-mcp's own README says 10848/10849. Check before building.

#### 3. Effort estimate
2–3 d once the port discrepancy is resolved and someone actually runs the sequence once by hand to find what breaks. Most of the "effort" is verification and the export-strategy decision (combined vs. separate — see full writeup), not new code.

#### 4. Revenue potential
None directly — this is a personal creative/living-space chain. Tangential: if the resulting settee mesh or the room-generation workflow itself turns out reusable, there's a faint case for a Resonite-marketplace asset, but that's speculative and not the point of building this.

#### 5. Notes
Full worked example with all design tradeoffs (combined vs. separate export, the collision-mesh reasoning) lives in `architecture/FLEET_DEEP_ANALYSIS_2026-07-13.md` §2.2.1. This entry is the compressed pointer; don't duplicate updates, edit the source.

---

### Self-hosted FOSS Gaussian-splat generation (worldlabs alternative) — candidate name `splatmaker-mcp`

**Tier:** medium
**Pitch:** worldlabs isn't cheap; a self-hosted FOSS splat generator (Postshot/gsplat/Nerfstudio-class tooling) would produce comparable rooms/worlds at zero marginal API cost, run on the 4090 like everything else in the artistic chain. **Sideline (2026-07-13, Sandra):** this is plausibly bigger than an internal cost-saver — Resonite and VRChat both have active world-building/asset-maker communities who currently either pay for splat-generation SaaS or fight with research-grade Nerfstudio/gsplat CLI tooling directly. A clean MCP wrapper around "phone/camera capture → zero-cost living-room-scale splat, ready for a VR world" is a real gap in that community's toolchain, not just a Sandra-specific need.
**Steps (draft):** photo/video capture → FOSS splat-mcp (not yet built, no repo exists as of 2026-07-13) generation → hand off to Blender for finishing — same downstream steps as the settee chain from here.
**Feasibility:** the FOSS tooling itself exists in the wild and is mature enough to wrap; the MCP wrapper doesn't exist yet, flagged by Sandra as "will get an MCP repo rsn." **DECIDED 2026-07-13: Nerfstudio.** Postshot scratched entirely — free download, but its CLI (the only tier with real automation value) turned out to be a paid Studio-tier feature (~£40pcm), a free-download/paid-CLI split Sandra rightly called out as bait-and-switch shaped. gsplat ruled out as bare-library/no-CLI/too-much-glue. Full comparison and citations in `splatmaker-mcp`'s README "Engine status" section, kept as the record even though the decision is made. **Load-bearing finding: none of the three produce a collider mesh as a clean sidecar** — unlike worldlabs' `collider_mesh_url`, Nerfstudio's `ns-export tsdf`/`poisson` is a separate, untested-against-Splatfacto command. This means `blender_splatting`'s collision-mesh generation isn't a fallback for the FOSS path, it's the primary path — budget for it as a mandatory pipeline stage, not optional cleanup.
**Key implementation difference from worldlabs:** FOSS splat pipelines generally do NOT return an API-side collision mesh the way worldlabs' Marble does (`assets.mesh.collider_mesh_url`). For this source, `blender_splatting`'s collision-mesh generation is the **primary** path, not a fallback — the opposite of the worldlabs case. Whoever writes this MCP's README should say so explicitly, since the settee-chain writeup got this backwards once already for worldlabs and it's an easy mistake to repeat in the other direction.
**Effort:** unscoped — depends entirely on which FOSS tool gets chosen and how mature its CLI/API surface already is.
**Revenue:** no direct revenue modeled, but a genuinely different case than most of this catalog: if this ships as a clean, well-documented fleet-standard MCP server (per the existing `FLEET_PROMOTION.md` discovery standard — MCPB packaging, Glama listing, GitHub visibility, all already fleet-standard practice), it's a real candidate for external adoption by the Resonite/VRChat maker community. That's reputation/portfolio value, not revenue in the strict sense, and possibly a donations/sponsorship trickle if it's genuinely useful — worth being honest that "community adoption" and "revenue" aren't the same thing, but this entry is closer to the former than most gestating-chains ideas get.
**Notes:** if pursued, worth explicitly designing for a wider install base from day one (naked-PC install standard already covers this) rather than Sandra-specific hardcoding — the difference between an internal tool and a genuinely shareable one is usually a documentation/config-flexibility cost paid early, not a rewrite later.

---

### Boomy ARKit survey → nav map update

**Tier:** medium
**Pitch:** walk the flat once with the phone, Boomy gets a real marker map instead of a hand-measured one.
**Steps:** Boomy's Leash (iOS, ARKit/LiDAR) → marker pose capture → YAML export → yahboom-mcp `nav/save_map_markers`.
**Feasibility:** gated on yahboom nav Phase N1 landing (defines the YAML schema) — build together, per `IOS_APP_PLANS.md` §2.
**Effort:** ~2 d app-side once N1's schema exists.
**Revenue:** none.
**Notes:** the phone's LiDAR replacing a tape measure is the whole idiosyncrasy of this one — see `POL_AND_RECOMBINANT_CAPABILITIES.md` §2 where it's cited as a recombinant-capability example.

---

### PoL escalation state machine

**Tier:** medium
**Pitch:** absence-gated liveness monitoring — see the dedicated doc, this is a pointer entry.
**Steps / feasibility / effort / notes:** all live in `POL_AND_RECOMBINANT_CAPABILITIES.md` §1 in full. Not duplicated here.
**Revenue:** none — explicitly out of scope per that doc's privacy fence (§1.5 of the deep-analysis addendum).

---

### Ekphrasis capture → LoRA dataset → trained style

**Tier:** medium
**Pitch:** shoot a burst of photos, tag as a dataset, comfyops trains a custom style/subject LoRA, available fleet-wide afterward.
**Steps:** Ekphrasis burst-capture mode → dataset tagging → comfyops `dataset_prep` → LoRA training job (ai-toolkit, Phase 2) → new workflow entry in comfyops depot.
**Feasibility:** gated entirely on comfyops Phase 2 (not started, per FLEET_INDEX). Everything upstream (capture) is speced but not built either.
**Effort:** ~1 d app-side (already counted in Ekphrasis v0.2) + comfyops Phase 2's own unscoped effort.
**Revenue:** faint but real — a genuinely good custom LoRA (a consistent original-character style, say) is the kind of thing that has a small secondary market (civitai-adjacent) if it turns out well. Not a plan, just noting the door isn't closed.

---

### Generated song + generated visual → short music video

**Tier:** medium
**Pitch:** songgeneration-mcp writes a track, comfyops or blender-mcp generates matching visuals, tahoma2d or Blender's VSE assembles a short video.
**Steps (draft, not verified against real tool names yet):** songgeneration-mcp → audio file → comfyops i2v or blender-mcp `blender_vse` for edit/assembly → export.
**Feasibility:** unverified — this entry hasn't been traced against actual tool signatures the way the settee chain was. Flagging that explicitly: don't trust this step list until someone checks it the way §2.2.1 checked the settee chain.
**Effort:** unknown until traced.
**Revenue:** the most plausible revenue-bearing chain in this tier — a short AI-assisted music video is a sellable/postable artifact in a way most fleet output isn't. Worth tracing properly if the idea has legs.

---

### Leanforge proof stall → filed research note

**Tier:** medium
**Pitch:** when a leanforge proof search stalls or completes, the result (or the stuck state and candidate branches) gets filed as a structured advanced-memory note automatically, not just pushed and forgotten.
**Steps:** leanforge job queue → Beweisstück's admiral-approval branch-selection (iOS backlog §5.5) → resolution → Denkzettel-style structuring (iOS backlog §5.2) into an advanced-memory zettel.
**Feasibility:** both halves (Beweisstück, Denkzettel) are individually speced as separate iOS app ideas; this entry is just naming that they'd compose into one chain if both existed. Nobody's built either yet.
**Effort:** N/A — depends on both parent ideas being built first.
**Revenue:** none.
**Notes:** good example of a chain that only becomes visible once two unrelated backlog ideas are looked at side by side — worth re-scanning `IOS_APP_PLANS.md`'s backlog periodically for more of these composite opportunities.
