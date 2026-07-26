# apple-test / VRMDanceApp

Native iOS **VRM dance app** (VRoid Hub + Metal VRM stage). **Private repo.**

**Remote:** https://github.com/sandraschi/apple-test (private)

## Status

Phase 3 — Baked motion JSON on humanoid bones.

Phase 4 — **VRMMetalKit** Metal stage, VRMA + builtin clips, StoreKit motion packs.

Create Xcode project on Mac: **`docs/SETUP_MAC.md`**

## Quick links

| Doc | Purpose |
|-----|---------|
| [docs/SETUP_MAC.md](docs/SETUP_MAC.md) | Mac + Xcode 26 + VRMMetalKit |
| [docs/VRMA_AND_IAP.md](docs/VRMA_AND_IAP.md) | VRMA bundle + StoreKit testing |
| [AGENTS.md](AGENTS.md) | Agent context |
| MCD | [PRIVATE_IOS_REPOS.md](https://github.com/sandraschi/mcp-central-docs/blob/master/apple/development/PRIVATE_IOS_REPOS.md) |

## Fleet

| Service | Role |
|---------|------|
| avatar-mcp | Dev-time VRM staging (copy to Mac DevSamples) |
| blender-mcp | VMD → baked JSON or VRMA export |
| godot-mcp | Games only — not this app |

## Layout

```text
VRMDanceApp/Sources/VRMDanceApp/
VRMDanceApp/Resources/DevSamples/       optional bundled .vrm
VRMDanceApp/Resources/Animations/       .json and .vrma clips
VRMDanceApp/Resources/motion_catalog.json
Config/HubSecrets.example.xcconfig
Config/VRMDance.storekit
scripts/create_xcode_project.sh         VRMMetalKit 0.16.0 SPM
```
