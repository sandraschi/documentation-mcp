# VRMDance

**Model:** Free app + IAP dance and character packs
**Repo:** [apple-test](https://github.com/sandraschi/apple-test) (Phase 1 — Hub OAuth + stage)
**Comps:** Doll Dancer, DanceDreamMV (iOS dance MV editors)
**Target:** Xcode 27.2, iOS 27 SDK

## Product

Load VRoid Hub avatars, play dances on a stage, export short MP4 clips. Monetize **your** bundled motion packs — not Hub subscription reselling.

## Fleet reuse

| Piece | Source |
|-------|--------|
| Hub OAuth + download flow | avatar-mcp `hub_client.py` → Swift port |
| VRM staging / dev samples | avatar-mcp pipeline |
| Motion v1 | blender-mcp bake VMD → bundled clips |
| Docs | [VRM_DANCE_APP.md](../ios/VRM_DANCE_APP.md), [MMD explainer](../../../docs/avatars/MMD_EXPLAINER.md) |

## Monetization

| SKU type | Example |
|----------|---------|
| Non-consumable | “K-pop pack 01” (10 dances) |
| Non-consumable | “Stage: neon club” |
| Optional sub | “Dance club monthly” (new pack each month) |

**Do not:** charge for Hub access; respect per-avatar VRM license flags.

## AI angle (optional v2)

- On-device: auto camera angles from Foundation Models (scene description → preset)
- Not required for v1 revenue

## Effort / revenue

- **Effort:** High (renderer, StoreKit, export pipeline)
- **Upside:** Highest in portfolio if catalog + ASO land; crowded niche

## Next milestone

Real VRM load in SceneKit/Metal — remove placeholder stage mesh.

## Ship checklist (App Store)

- Privacy manifest + Hub OAuth disclosure in App Privacy labels
- VRM license flags respected per avatar (already a monetization rule above — enforce in code, not just docs)
- Export via share sheet (MP4); test on oldest supported iPhone for draw-call budget

---
*Status: spec + Phase-1 scaffold in apple-test. Last updated: 2026-10-28.*
