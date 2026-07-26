# PoL & Recombinant Capabilities — Ongoing Brainstorm

**Date started:** 2026-07-13
**Status:** LIVING BRAINSTORM — not a build brief. Promote sections to `architecture/` briefs when ready to build.
**Tags:** [pattern, brainstorm, pol, fritz, privacy, running-plan]

---

## 0. The pattern this doc is really about

Proof-of-Life started this doc, but PoL is a *case study*, not the point. The point is a pattern worth naming: **recombinant capability** — a new function that emerges from re-reading signals that already exist, produced by servers built for unrelated reasons, interpreted by an agent that already exists, delivered through a channel that already exists. No new sensor, no new device, no new subscription. The capability was latent in infrastructure the fleet already has; it just hadn't been *asked the right question* yet.

This is worth naming because it's a different mode of fleet growth than everything in FLEET_INDEX and the gap-analysis briefs. Those are "build server X to do Y." Recombinant capabilities are "servers A, B, C already produce signals that, read together with a small state machine and a decision about who gets told what, do Y — and Y was never in anyone's spec."

**Ingredients, generalized from PoL:**
1. **Existing sensors/signals** — usually built for something else (home automation, security, general vision work).
2. **A small interpretive layer** — a state machine or rule set, cheap and legible, NOT a new ML model trained for the purpose. The crudeness is a feature: it's auditable, and it fails in predictable ways.
3. **An agent with standing access to those signals** — Fritz, here, because it already has the fleet bridge and the health/log-polling habit.
4. **A delivery/escalation channel that already exists** — admiral-mcp's notify + approval infrastructure, a phone call, whatever's already wired.
5. **A privacy fence stated up front** — recombinant capabilities are exactly where scope creep toward surveillance happens by accident, because every ingredient already existing makes the *next* increment feel free. It isn't. Write the fence before writing the state machine.

---

## 1. Case study: Proof-of-Life (PoL)

*(Consolidated from FLEET_DEEP_ANALYSIS_2026-07-13.md §1.6–1.6.1 — this is now the canonical PoL doc; the analysis doc's §1.6 should eventually be trimmed to a pointer here once this stabilizes.)*

### 1.1 The recombination

| Ingredient | Existing thing being reused |
|---|---|
| Signal: motion/stillness | devices-mcp camera feeds (built for home automation / general vision) |
| Signal: mail accumulation | devices-mcp mailbox sensor (if wired — verify inventory) |
| Signal: liveness check | speech-mcp TTS prompt + FunASR STT listen (built for dictation/briefings elsewhere in the fleet) |
| Interpretation | Fritz's new `fritz_surveil` engine (built for log-triage, §1 of the analysis doc) |
| Self-check delivery | admiral-mcp `notify` (built for agent-approval pings) |
| Emergency escalation | a literal phone call to [[brother]] — the existing backup-contact relationship, not a new "emergency contact" concept |

Nothing here is a health device. Nothing here was bought for this. That's the whole point.

### 1.2 State machine (draft — promote to a diagram in the eventual build brief)

```
present-normal
   │  (no motion detected in a covered zone, timer starts)
   ▼
present-no-signal ──────────────► [known-absence toggle ON?] ──yes──► suppressed (no further action)
   │ no
   │ (zone + duration classifier, §1.3)
   ▼
pol-check-low  ────────────────────────────────────────────────────┐
   │ (self-check notify: "tap if you're up/OK")                     │
   │ responded ──► present-normal                                   │
   │ no response within fuse ──► escalate                           │
   ▼                                                                │
pol-check-high  (floor-zone, short fuse — SKIPS self-check step) ◄──┘
   │
   ▼
escalated ──► phone call to [[brother]] ──► he confirms/denies/calls further (ambulance etc. is HIS call, not the system's)
   │
   ▼
resolved (manually cleared — by Sandra confirming OK, or by [[brother]] confirming resolution)
```

Two entry points into `pol-check`, not one — this is the load-bearing design decision from the 2026-07-13 session: **low-severity path always self-checks first; high-severity path (floor-zone) skips straight past the self-check to escalation**, because a floor-zone stillness event is close enough to the signal itself that waiting for a tap-to-confirm is the wrong trade.

### 1.3 Zone/duration classifier (the "interpretive layer" ingredient, concretely)

Per-zone config, not a global timer:

```yaml
zones:
  bedroom:
    surface: furniture   # on-bed vs on-floor distinguished by coarse bounding-box heuristic
    fuse_hours: 10        # only alarms past normal wake time
    severity: low
    active_hours: "22:00-09:00"   # outside this window, floor-of-bedroom logic applies instead
  living_room_floor:
    surface: floor
    fuse_minutes: 20
    severity: high
    active_hours: "always"
  bathroom_floor:
    surface: floor
    fuse_minutes: 15
    severity: high
    active_hours: "always"
  hallway:
    surface: floor
    fuse_minutes: 20
    severity: high
    active_hours: "always"
```

Deliberately NOT pose-estimation. "On furniture" vs "not on furniture" is a bounding-box-vs-known-furniture-region check, not a body-pose model. Crude, legible, auditable — the classifier can be wrong in ways a human can understand by reading the config, which matters enormously for something that can end in a phone call to your brother.

### 1.4 Known-absence gate

v1 is manual only — a toggle ("heading out" / "back") from admiral-pager or piggybacked on the Benny FM push channel. Explicitly NOT auto-inferred from calendar/GPS in v1: the failure mode of auto-inference is a false negative in exactly the scenario PoL exists to catch (system decides "she's probably out" when something's actually wrong). Auto-inference is a v2 idea, gated on the manual version having a track record of not being annoying.

### 1.5 Privacy fence (restated, because this is the section most likely to erode)

- No stored video analysis — motion/zone *events*, not footage, consumed by the classifier.
- No pose-estimation ML, no "this looks like a fall" model.
- No vitals, no wearables, no health-cloud integration.
- No automatic absence-inference from location/calendar in v1.
- Escalation to a person (Steve), not to a service — the system's job ends at "get a human with judgment involved," not "diagnose" or "dispatch emergency services" itself.

### 1.6 Effort

~1–1.5 d once `fritz_surveil`'s core engine exists (it's a state-machine mode on top of that, not a parallel system) + zone-config authoring time (walking the flat once to define zones, similar in spirit to the ArUco marker survey in Boomy's Leash — worth doing both surveys in one pass if Boomy's Leash Lane B ships first).

---

## 2. Other things already in flight that fit the same pattern

Worth cross-referencing so the pattern is recognized rather than reinvented per-idea:

- **Boomy's Leash Lane B** (iOS app plans §2) — ARKit/LiDAR, built for AR apps generally, repurposed as a surveying instrument for robot navigation. Same shape: existing phone hardware, novel reading.
- **Fritz's `report_logs` polling itself** (analysis doc §0/§1) — NSSM restart events plus per-server log tools, built for ops visibility, repurposed as a near-real-time triage trigger instead of waiting for scheduled digests.
- **Ekphrasis dataset mode** (iOS app plans §4, v0.2) — camera app built for image treatments, repurposed as a LoRA dataset-capture front end once comfyops Phase 2 lands.
- **worldlabs → Resonite handoff** (analysis doc §2.2) — a photo-to-3D-world pipeline built for one purpose (Marble worlds), repurposed as a way to generate visitable social-VR locations.
- **openbci-mcp, dormant** (analysis doc §2.3.2) — already has an OSC trigger path built for EEG research use; the day the hardware justifies revisiting it, the recombination is free: it slots straight into the artistic chain as a control-signal source (mind-controlled VCV patch) with zero new integration work, because osc-mcp already exists as the connective tissue.
- **Pinokio inventory** (`architecture/PINOKIO_INVENTORY.md`, 2026-07-14) - a year of unrelated, one-off Pinokio app installs (~550GB, 20 apps) re-read through the lens of current fleet needs, surfaced real usable local backends for four separate open threads (splatmaker-mcp's `from_prompt`, songgeneration-mcp's missing generation backend, ittybitty's TTS gap) without building anything new - the interpretive layer here was a filesystem size/extension scan plus cross-referencing against known gaps, and `pinokio-mcp` (already built, verified working the same session) was the delivery channel that made it actionable rather than just theoretical.

## 3. Open brainstorm — candidate recombinations, unfiled

Loose ideas, not sized, not committed. Add freely; promote to §1-style write-ups when one gets serious.

- **Cross-referencing PoL's zone/motion data with Benny's activity** (existing dog-related device signals, if any exist in devices-mcp's inventory) — a dog behaving oddly near a still owner is itself a signal humans use; probably not worth the complexity, but worth a line so it's been considered and explicitly deferred rather than never thought of.
- **aiwatcher's urgency-scoring model repurposed for household admin** — junk mail vs. something that actually needs action, if mail-sensor OCR ever gets added to devices-mcp, is the same 0–10 relevance-scoring approach aiwatcher already does for news, applied to a completely different signal.
- **osc-mcp as the universal actuator for "controller-shaped" ideas** — Pocket Patch (VCV) and a hypothetical openbci revival both terminate in the same OSC transport; worth remembering osc-mcp is already the shared final hop for "some input device controls some real-time process," so new controller ideas should default to asking "can this just emit OSC?" before building a bespoke transport.
- **Fritz's triage engine applied to leanforge's proof-search stalls** — already flagged as Beweisstück in the iOS app plans backlog (§5.5); note here that it's the *same* triage-engine reuse as PoL and log-surveillance, not a separate idea — one engine, four+ consumers now (news, environment, PoL, proof-search).

---

## 4. Hygiene

This is a brainstorm doc: keep adding to §3 as ideas surface, promote to a numbered §1-style case study (state machine, ingredient table, privacy fence, effort estimate) when an idea is ready to be briefed, and cross-link back to whichever build brief eventually implements it rather than duplicating the spec here once it's built.
