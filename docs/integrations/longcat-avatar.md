# Meituan LongCat-Video-Avatar 1.5 Integration

**Last updated:** 2026-08-21 · **Model:** `meituan-longcat/LongCat-Video-Avatar-1.5` · **Fleet Target:** [`avatar-mcp`](../projects/avatar-mcp/README.md)

LongCat-Video-Avatar 1.5 is an audio-driven digital human video generation framework developed by Meituan's LongCat team. It synthesizes photorealistic, audio-synced digital human video MP4 outputs from a single audio narration track and portrait image/video reference.

---

## Capabilities & Architecture

| Feature | Specification |
|---|---|
| **Architecture** | Dense Diffusion Transformer (DiT) Audio-Conditioned Engine |
| **Output** | 720p @ 30 FPS photorealistic digital human video MP4 |
| **Primary Tasks** | Audio-Driven Lip-Sync, Facial Expression Synthesis, Multi-Person Interaction |
| **Licensing** | Open-source MIT License |

---

## AvatarMCP Integration

In `avatar-mcp`, LongCat-Video-Avatar 1.5 is integrated via:
1. **Digital Human Service Module:** `avatarmcp.digital_human.LongCatAvatarService`
2. **Portmanteau Tool:** `digital_human_avatar` (`longcat_status`, `longcat_generate`, `lipsync_drive`)
3. **Creative Pipeline Operations:** `avatar_pipeline(operation="longcat_avatar_generate")`
4. **Web Interface (`web_sota`):** `DigitalHumanStudio` page (`/digital-human`)

---

*Maintained by: Antigravity AI Fleet Orchestrator · 2026*
