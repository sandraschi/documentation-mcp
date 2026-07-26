# iOS VRM / Dance MV App Development (May 2026)

Build **Doll Dancer–class** apps: VRoid Hub characters + MMD-style dances + stage + video export.

## Why native iOS (not godot-mcp)

| Approach | Verdict |
|----------|---------|
| **Swift + Metal/SceneKit + VRM lib** | Correct for App Store dance MV apps |
| **godot-mcp + Godot iOS export** | Possible for **games**, wrong tool for Hub OAuth + VMD cottage-industry UX |
| **Web/HTML5 on itch** | Fine for toys; not Hub-linked native experience |

**Fleet scaffold:** `D:/Dev/repos/apple-test` — follow **`docs/SETUP_MAC.md`** on your M4 Mac after installing Xcode 26.

See [GODOT_VRM_MMD_DECISION.md](../../docs/avatars/GODOT_VRM_MMD_DECISION.md).

## May 2026 dev experience

**Xcode 26.3 agentic coding** makes iOS development comparable to Cursor on Windows:

1. Open Xcode project on Mac  
2. Enable Intelligence → Claude Agent or Codex (or connect Cursor via `xcrun mcpbridge`)  
3. Prompt: *"Add VRoid Hub OAuth, load VRM into SceneKit view, list cached avatars"*  
4. Agent edits Swift, resolves SPM deps, builds, fixes errors, checks Previews  

Detailed setup: [development/AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md)

## Architecture (recommended v1)

```text
SwiftUI shell
  ├── HubAuthService (OAuth PKCE — mirror avatar-mcp hub_client)
  ├── VRMCache (Application Support)
  ├── VRMSceneView (renderer)
  ├── MotionPlayer (VMD retarget OR baked glTF clips)
  ├── StageComposer (lights, sky, particles)
  └── VideoExporter (AVFoundation)
```

## Fleet integration

| Fleet piece | iOS app use |
|-------------|-------------|
| avatar-mcp `hub_download` | Dev-time staging; prototype Swift against same VRM files |
| avatar-mcp Hub OAuth | Copy flow from `hub_client.py` or call backend API |
| blender-mcp | Bake VMD → animation clip before shipping in app bundle |
| mcp-central-docs | [MMD_EXPLAINER.md](../../docs/avatars/MMD_EXPLAINER.md), [FLEET_VRM_PIPELINE.md](../../docs/avatars/FLEET_VRM_PIPELINE.md) |

Optional: avatar-mcp HTTP API as **dev catalog** (`/api/v1/pipeline/status`) while building; production app talks to Hub directly.

## Motion: VMD in v1

**Option A (faster):** Ship 10–20 **pre-baked** dances (glTF/USDZ) converted in blender-mcp — no runtime VMD parser.

**Option B (Doll Dancer parity):** Embed VMD parser + humanoid retarget — 2–4 weeks engineering even with agents.

Start with **Option A**; add VMD import in v2 if IAP dance store is the monetization core.

## Monetization (market reference)

- Free app + **IAP** dance/character packs  
- Hub models: respect per-creator license (commercial flags in VRM metadata)  
- Not a Hub subscription — creators set download rules per model  

## Distribution

| Path | Requirements |
|------|----------------|
| **TestFlight** | Apple Developer Program, Xcode archive |
| **App Store** | Privacy manifest, AI disclosure if using cloud models |
| **Side-load / dev** | Free Apple ID, 7-day cert |

Cannot sign iOS builds on Windows alone — use Mac or Mac cloud CI.

## Agent prompt seed

```text
Create a SwiftUI iOS 26 app target:
- VRoid Hub OAuth PKCE (redirect: myapp://hub/callback)
- Download VRM via Hub download_licenses API (X-Api-Version: 11)
- Display VRM using SceneKit or imported VRM Swift package
- Play bundled glTF animation clip on humanoid skeleton
- Export 30s MP4 of the scene
Follow Apple privacy manifest requirements.
Reference: mcp-central-docs/docs/avatars/MMD_EXPLAINER.md
```

## Related

- [DISTRIBUTION_AND_MONETIZATION.md](./DISTRIBUTION_AND_MONETIZATION.md) — installs, App Store vs itch, IAP  
- [AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md)  
- [publishing/README.md](../publishing/README.md)  
- [MCP_AND_APPLE.md](../MCP_AND_APPLE.md) — Xcode MCP + fleet MCP together  

---
*Last updated: 2026-05-28*
