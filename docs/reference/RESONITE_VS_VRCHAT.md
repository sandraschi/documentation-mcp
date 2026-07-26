---
title: "Resonite vs VRChat — Fleet Platform Decision"
category: reference
status: active
audience: mcp-dev, fleet
last_updated: 2026-07-15
---

# Resonite vs VRChat — Why the Fleet Chose Resonite

## The 2024 Analysis

A year ago, the fleet evaluated both platforms for avatar hosting, NPC companions, and automation. The conclusion was that Resonite was more developer-friendly. In 2026 that gap has widened, not narrowed.

## Feature Comparison

| Feature | Resonite | VRChat |
|---------|----------|--------|
| **Web panels** (display web content in-world) | Native — place a web panel, set a URL | Does not exist. |
| **Headless server** (24/7 automation) | Native — run without GPU | Requires a full GPU client logged in. No native headless mode. |
| **OSC API** | Full — blendshapes, audio, parameters | Frozen since 2022. No blendshape streaming, no audio input. |
| **Visual scripting** | ProtoFlux (node-based, in-editor) | Does not exist. Requires C# Udon or community tools. |
| **C# SDK** | Full — create worlds and avatars programmatically | UdonSharp (community fork). Official C# support never shipped. |
| **NPC / companion spawning** | `POST /rl/world/import-vrm` — spawn persistent NPCs | Impossible. You wear avatars, you don't spawn them. |
| **Avatar format** | VRM (open standard) + custom | Custom binary format. No VRM import path. |
| **Asset import** | Drag-and-drop glTF, VRM, PNG, audio | Requires Unity project, build, upload. |
| **Anti-cheat** | None (not needed — open creation) | EAC (Easy Anti-Cheat) — blocks mods, automation, research. |
| **Modding** | Not needed — the platform IS the SDK | Banned via EAC. Community MelonLoader forks exist but are fragile. |
| **Monetization priority** | Creator tools, performance, stability | Moderation, anti-cheat, VRChat+ subscriptions. |
| **Social graph** | Smaller, focused community | Massive network effect. Hard to leave. |

## Development Priority Divergence

By 2026, the two platforms have taken fundamentally different paths:

**Resonite** allocates dev resources to:
- Web panels (in-world browser rendering)
- ProtoFlux visual scripting improvements
- Resonite Link (headless automation API)
- VRM/glTF import pipeline
- Performance optimization for complex worlds

**VRChat** allocates dev resources to:
- EAC anti-cheat hardening
- Moderation tooling and trust/safety
- VRChat+ subscription features
- Avatar/shader security sandboxing
- Account verification and age gating

Both are rational business decisions. Resonite chose to be a creation platform. VRChat chose to be a social network with creation as a secondary feature. The consequence is that Resonite is the only viable choice for anyone who wants to **build on top of** the platform rather than just **exist inside** it.

## The Hosting Difference

This is the single most important distinction and the one that seals the decision:

| | Resonite | VRChat |
|--|----------|--------|
| **Server** | Self-hosted (Goliath, or any machine) | VRChat's cloud (locked) |
| **Control** | Full — stop, modify, backup at will | None — you accept their uptime and rules |
| **Privacy** | All data stays on your network | Everything passes through VRChat's servers |
| **Offline** | Works on LAN without internet | Requires VRChat login and cloud connectivity |
| **Cost** | Electricity + hardware | VRChat+ subscription + potential future platform fees |
| **Persistence** | Your machine decides when the world is up | VRChat's servers decide. They can and do shut down instances. |
| **Modification** | Edit ProtoFlux at runtime, reload scripts | Rebuild and re-upload entire Unity project |

Resonite's headless server runs as a process on Goliath alongside Ollama, speech-mcp, and learnbot-mcp. They share the same LAN, the same Tailscale network, and the same filesystem (VRM models in `~/.avatarmcp/models/`). Miko-chan's world is always up, always reachable, and answers to no API rate limit or TOS.

VRChat cannot do this. Your avatar in VRChat only exists when a user wearing it logs into VRChat's servers. There is no "companion" concept. There is no headless mode. There is no local API. It is a social app, not a platform.

## Fleet Decision

The fleet uses **Resonite** for all avatar hosting, NPC companions, and automation:

| Use Case | Resonite | VRChat |
|----------|----------|--------|
| Miko-chan as persistent home companion | **Yes** — spawned NPC with VRM, conversation via web panel | No — NPCs cannot exist without a user wearing the avatar |
| Miko-chan as social avatar | Possible but not primary | Possible — VRM could be converted, but not worth the pipeline overhead |
| 24/7 headless presence | **Yes** — Resonite Link on Goliath | No — requires full GPU client |
| Web UI in-world | **Yes** — web panel with mascot.html | No |
| Automation via MCP | **Yes** — resonite-mcp has full REST API | **Partial** — vrchat-mcp exists but works through OSC with no NPC support |

## The VRChat Trap

VRChat's social network effect is real. If the goal is to meet strangers in a virtual nightclub, VRChat has no competitor. But that's not what the fleet builds. The fleet builds persistent AI companions that live in a world and interact with their owner over time. That requires:

- A world that stays running when nobody is logged in (headless)
- An NPC that persists across sessions (spawned entity)
- A web surface for conversation, TTS, and emotion display (web panel)
- An open API for automation and tool calling (REST/MCP)

VRChat offers none of these. Resonite offers all of them. The choice is clear.

## Document History

- 2026-07-15: Initial analysis. Based on fleet experience with resonite-mcp (v2.1) and vrchat-mcp (v14.1).
