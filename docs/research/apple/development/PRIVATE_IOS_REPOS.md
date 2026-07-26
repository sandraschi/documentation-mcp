# Private iOS repos — Mac setup (May 2026)

Apple app source lives in **private** GitHub repos. Fleet docs stay public in `mcp-central-docs`.

| Repo | Visibility | App |
|------|------------|-----|
| [apple-test](https://github.com/sandraschi/apple-test) | **Private** | VRMDance — Hub OAuth + VRM stage |
| [boomy-commander](https://github.com/sandraschi/boomy-commander) | **Private** | Raspbot agentic remote |

## One-time Mac prep

1. Xcode 26+ with iOS 26 simulator runtime  
2. `brew install xcodegen`  
3. Apple Developer team ID in each repo’s `Config/*Secrets.xcconfig`  
4. Optional: `xcrun mcpbridge` for Cursor / Claude Code  

See [AGENTIC_XCODE_26.md](AGENTIC_XCODE_26.md).

## VRMDance (apple-test)

```bash
git clone https://github.com/sandraschi/apple-test.git
cd apple-test
cp Config/HubSecrets.example.xcconfig Config/HubSecrets.xcconfig
./scripts/create_xcode_project.sh
open VRMDanceApp/VRMDanceApp.xcodeproj
```

- Hub app: [hub.vroid.com/oauth/applications](https://hub.vroid.com/oauth/applications) → redirect `vrmdance://hub/callback`  
- SPM: **VRMKit 0.7.1** (VRMRealityKit) via XcodeGen  
- Drop test `.vrm` in `VRMDanceApp/Resources/DevSamples/`  

Full checklist: repo `docs/SETUP_MAC.md`

## Boomy Commander

```bash
git clone https://github.com/sandraschi/boomy-commander.git
cd boomy-commander
cp Config/BoomySecrets.example.xcconfig Config/BoomySecrets.xcconfig
./scripts/create_xcode_project.sh
open BoomyCommander/BoomyCommander.xcodeproj
```

- Gateway URL → yahboom-mcp `:10892` (Tailscale or LAN)  
- StoreKit testing: scheme → Options → `Config/BoomyCommander.storekit`  

Full checklist: repo `docs/SETUP_MAC.md`

## Windows dev box role

- **avatar-mcp** — stage VRM for manual copy to Mac DevSamples  
- **yahboom-mcp** — backend for Boomy Commander (`webapp/start.ps1`)  
- **No iOS signing on Windows** — build/archive on Mac only  

---
*Last updated: 2026-05-28*
