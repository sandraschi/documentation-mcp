# VRMDance

**Model:** Free app + IAP dance and character packs  
**Repo:** [apple-test](https://github.com/sandraschi/apple-test)  
**Comps:** Doll Dancer, DanceDreamMV (iOS dance MV editors)

## Product

Load VRoid Hub avatars, play dances on a stage, export short MP4 clips. Monetize **your** bundled motion packs — not Hub subscription reselling.

## Fleet reuse

| Piece | Source |
|-------|--------|
| Hub OAuth + download flow | avatar-mcp `hub_client.py` → Swift port |
| VRM staging / dev samples | avatar-mcp pipeline |
| Motion v1 | blender-mcp bake VMD → bundled clips |
| Docs | [VRM_DANCE_APP.md](../ios/VRM_DANCE_APP.md), [MMD explainer](../../docs/avatars/MMD_EXPLAINER.md) |

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
