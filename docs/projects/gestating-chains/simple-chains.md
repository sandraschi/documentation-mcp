# Simple Chains (1–2 hops, mostly already wired)

Per [`README.md`](./README.md) template — compressed form for this tier.

---

### Photo → styled image/video → Immich

**Pitch:** point phone at something, apply a comfyops treatment, result lands in the photo library.
**Steps:** Ekphrasis (phone) → comfyops-mcp REST upload → job → Immich ingest op.
**Feasibility:** comfyops MVP exists; Immich auto-ingest is a named-but-not-yet-built comfyops remediation item (deep analysis §11 status). Everything else exists.
**Effort:** ~1 d for the missing Immich op once touched.
**Revenue:** none — personal-use tool.
**Notes:** fully speced as Ekphrasis in `IOS_APP_PLANS.md` §4.

---

### Benny FM — morning briefing

**Pitch:** fleet status + overnight papers + weather, narrated, on the walk.
**Steps:** Fritz composer (gitops + arxiv-mcp + netatmo + local LLM script) → speech-mcp TTS → admiral `notify` → phone player.
**Feasibility:** every source exists; composer logic is the only new code.
**Effort:** ~3.5 d, mostly server-side, per `IOS_APP_PLANS.md` §3.
**Revenue:** none.
**Notes:** first thing that should get built once FleetKit + admiral `notify` exist — proves the whole delivery chassis cheaply.

---

### VCV patch generate → OSC play-test

**Pitch:** generate a patch, verify it actually makes sound and its OSC map is real, without leaving the terminal.
**Steps:** vcv-rack-mcp patch generation → depot save → osc-mcp sends a test message against the address map → confirm audible/measurable response.
**Feasibility:** vcv-rack-mcp is Phase 5 complete per FLEET_INDEX; gated entirely on Sandra saving 3–4 reference patches (BLOCKER-0, still unresolved as of 2026-07-12 evening per FLEET_INDEX row).
**Effort:** near-zero once BLOCKER-0 clears — this is closer to a smoke test than a build.
**Revenue:** none directly, but it's the gate that unblocks Pocket Patch (medium tier) and the whole artistic-audio chain's credibility.
**Notes:** the cheapest possible next step in the whole audio chain — do this before anything fancier.

---

### Record fingerprint → "do I already own this?"

**Pitch:** at a record stand, ten seconds of mic audio tells you if it's already in your collection.
**Steps:** phone mic capture → server-side audio fingerprint (Chromaprint/AcoustID, not yet built) → plex-mcp ownership check → wantlist entry if new.
**Feasibility:** the fingerprinting lane is genuinely new server work; everything downstream (Plex query, wantlist) exists.
**Effort:** ~2.5 d, per `IOS_APP_PLANS.md` §5.7 (Flohmarkt).
**Revenue:** none — pure anti-double-purchase utility. (Arguably negative revenue, i.e. money saved, which is its own kind of return.)

---

### Book query → deep research (ALREADY BUILT)

**Pitch:** ask about a book, get Wikipedia + SFE + TVTropes + Anime News Network + OpenLibrary synthesized into one answer.
**Steps:** calibre-mcp `media_research_book` — this already IS the chain, in one tool.
**Feasibility:** done. Listed here as the reference example of what a "simple chain" looks like once it's fully baked into a single portmanteau tool rather than staying as an orchestrated sequence across servers.
**Effort:** zero — already shipped.
**Revenue:** none.
**Notes:** worth remembering as the end state simple chains graduate toward — the best simple chains eventually stop being chains and become one tool.
