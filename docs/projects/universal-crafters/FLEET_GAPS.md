# Universal Crafters — Fleet Gaps (what WE should build)

**Date:** 2026-11-07 · **Read after:** COMPARISON + PHYSICAL_LOOP. Honest build
list, smallest verifiable steps. No stubs, no seat-talk.

## Gap 1 — No photo→print verb anywhere (biggest, physical)

- **Missing:** `photo_lift` (photo → GLB), `mesh_repair` (watertight + walls),
  `mesh_split` (matrioska halves + clearance), `slice_preview` (layer check).
- **Own it:** `splatcraft` (B-, Python, already cloud/train/engines) + `makercraft`
  (C+, Rust hal/core) + `modcraft` (C+, geometry). Don't invent a new craft.
- **Step 1 (verifiable):** `splatcraft` gains `lift` op: local TripoSR (seconds,
  free) → GLB; fal Trellis-2 path behind `--paid` flag with budget log.
  Verify: one matrioska photo → GLB in `app/` + cost line in ledger.
- **Step 2:** `trimesh` gate inside `makercraft`: `is_watertight`, wall probe,
  base-flatten. Verify: draft GLB → repaired STL + `checks/mesh.md`.
- **Step 3:** Orca headless slice preview (PNG layers) into `checks/`.
  Verify without owning a printer: PNG stack + grams estimate.

## Gap 2 — Craft Anything has checks for pixels, not for bodies

- Upstream `checks/` compares 3 viewport widths. Bodies need calipers:
  bounding mm, wall mm, clearance mm, scale-from-ruler.
- **Fleet fix (no fork):** `craft-anything-cli` plugin/MCP wrapper in
  `revecraft` or `makercraft` that reads upstream `craft.json` + `checks/`
  and appends `checks/body.md` (mm table + test-fit photo slot). Upstream
  stays untouched (`storytold-ref` rule); we extend beside it.

## Gap 3 — REA ↔ Craft Anything handoff is manual

- REA finds the feature (evidence), Craft Anything rebuilds (project). Today
  Sandra copy-pastes between them.
- **Fix:** `revecraft` recipe `rea_to_craft`: REA session export → Craft
  Anything `--existing edit` folder with `capture/` prefilled. Verify: Notion
  clipboard trace (REA showcase) → rebuild folder in one command.
- Do NOT merge the repos. Different licenses, stacks, legal postures.
  A recipe is a bridge; a merge is a lawsuit.

## Gap 4 — fal key handling is `string`, should be `budget`

- Craft Anything tracks asset spend vs budget per project (good). Fleet crafts
  should copy the pattern: every `--paid` path logs `$ + model + GLB hash`.
- Add to `makercraft`/`splatcraft` TOOLS.md now: which ops are free/local,
  which burn fal cents, what the fallback is when budget = 0.

## Gap 5 — Deploy missing on both FOSS cloners

- Makers win on one-click live. Neither REA nor Craft Anything deploys.
- Cheapest fleet win: `appcraft` (C+, templates) + existing `start.ps1`
  localhost preview → Tailscale/`cloudflared` share link in `Ready` view.
  No Vercel dependency, no seat. Verify: clone → URL on phone in <60s.

## Gap 6 — Einfamilienhaus planning (architect → legal-only, Baumeister → execution)

Sandra's call, logged 2026-11-07: makers progress to complete Einfamilienhaus
planning; architect + Baumeister survive only where the law mandates signature/
liability, because building rules go fully local-and-legal (parcel FLÄWI/
Bebauungsplan, OIB-Richtlinien, Bundesland-Bauordnung — Wien/NÖ/etc.,
Einreichplan, Energieausweis, Statik). Austrian stock is boring cookie-cutter;
an advanced maker should reach Foster/FLW tier instead: site section first,
light + orientation, honest material, plan that earns the view.

- **Own it:** `cadcraft` (plan/BIM verbs) + `qgiscraft` (parcel, FLÄWI,
  Bebauungsplan, solar/orientation context) + `modcraft` (geometry) — one
  `house_plan` recipe across three crafts, IFC as truth, Revit/DWG as export.
- **Step 1 (verifiable):** local rule pack per Gemeinde (setbacks, GFZ/GRZ,
  height, roof, parking, fire): machine-readable YAML + source links, versioned.
  Verify: address in → rule sheet out with citations, no hallucinated paragraphs.
- **Step 2:** clone-then-improve: as-built from BUILDINGS_MACHINES.md pipeline
  → variant plans (cookie-cutter baseline vs Foster/FLW move: section, atrium,
  deep eaves, masonry + timber). Verify: 3 variants + cost/m² + Energiekennzahl
  delta side by side in `checks/`.
- **Anti-cookie-cutter gate:** every generated plan must name its move (light
  section? courtyard? split level on slope? Wrightian hearth core? Foster
  diagrid/skin?) — "Satteldach 38° + WDVS beige" without a move is rejected as
  baseline, not proposal.
- **Legal line (hard):** maker drafts, licensed architect/Baumeister signs +
  submits. Fleet never forges Einreichung, Statik, or Energieausweis. The gain is *fewer billable drafting hours*, not zero liability.

## Non-goals (say no loudly)

- No IDA support in anything fleet-owned (upstream Craft Anything is right:
  licensing + piracy liability). Ghidra + built-in disasm only.
- No hosted seat product. BYOK is the moat; seats are the trap.
- No museum-piece piracy tooling. Clean-room for porcelain like for code.

## Next 3 commits (if Sandra greenlights)

1. `splatcraft`: `lift` op (TripoSR local + fal Trellis-2 `--paid`) + test GLB.
2. `makercraft`: `repair` op (`trimesh` watertight + base + walls) + `checks/mesh.md`.
3. This section: link from `projects/craft-fleet/README.md` (one line, no matrix dup)
   + `research/` index line pointing here.
