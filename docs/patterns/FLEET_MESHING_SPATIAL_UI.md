---
title: "Fleet Meshing Spatial UI — The Three-Surface Contract"
category: pattern
status: active
audience: mcp-dev
related:
  - patterns/FLEET_MESHING_PHILOSOPHY.md
  - patterns/CROSSCONNECT_PATTERN.md
  - patterns/WORLD_MODEL_ROBOTICS_DOJO.md
last_updated: 2026-10-28
---

# Fleet Meshing Spatial UI: The Three-Surface Contract

## 1. Problem Statement

Across the fleet's 287 repositories, an increasingly common architectural challenge arises:
**When an actor repo (a robot, synthesizer, agent, or game controller) meshes into an environment repo (a 3D virtual world, social VR platform, or media compositor), where does the UI/UX live?**

Ad-hoc integrations suffer from two failure modes:
1. **The Alt-Tab Silo:** The user is immersed in the environment (e.g. Overte VR, Resonite, Blender, Godot), but must take off the headset or Alt-Tab to a separate 2D desktop application to trigger controls.
2. **The Copy-Paste Drift Trap:** The environment repo writes a bespoke mini-control panel in its own React/Vue webapp. Because it does not own the actor's domain model, this UI silently breaks whenever registers, kinematics, or capabilities change.

---

## 2. Core Architectural Principle

> **"Source Owns the Logic, Destination Owns the Projection."**

The actor repository MUST remain the single source of truth for kinematics, state machines, and hardware bus protocols. The destination environment provides a spatial canvas and input routing, projecting the actor's UI into 3D space without reimplementing it.

---

## 3. The Three-Surface Contract

Every complex meshed workflow implements three complementary UI surfaces:

| Surface | Target Medium | Implementation Pattern | User Experience |
|---|---|---|---|
| **Surface 1: Diegetic In-World UI** | Virtual World Canvas (`overte-mcp`, `resonite-mcp`) | 3D `Web` Entity parented to the subject model; serves compact responsive HTML | A physical-looking floating touchscreen or kiosk inside the virtual world; clicked via VR laser pointers or desktop mouse |
| **Surface 2: In-Headset HUD / Tablet** | VR Client Wrist Menu (`Overte.Tablet`, `VRCSDK`) | In-engine web overlay script | Operator controls the actor remotely from their virtual wrist without walking up to the physical model |
| **Surface 3: Out-of-World Ground Station** | Secondary Desktop Display / Presenter Laptop | Native Egui app (`saschirob-app`) or React dashboard | Displays raw register maps, high-frequency oscilloscope waveforms, and safety overrides |

---

## 4. The `/embed/` Endpoint Standard

To enable diegetic projection across the fleet without CDN fragility:

1. **Self-Contained HTML:** The actor or bridge server must expose a dedicated embed route (e.g., `http://127.0.0.1:<port>/embed/<name>-pendant`).
2. **Zero CDN Dependencies:** All styling and scripting must be embedded in the response. QtWebEngine and in-world browsers frequently run on local air-gapped or loopback domains where external CDNs fail to resolve.
3. **Responsive Dimension Target:** Tailored for a $400 \times 520\text{ px}$ aspect ratio, with high-contrast tactile buttons ($> 44\text{ px}$ target area) optimized for VR laser-pointer interaction.
4. **Decoupled Event Streaming:** State updates flow outward over WebSocket or postMessage; control commands dispatch back over local HTTP REST or WebSocket.

---

## 5. Reference Implementation: Saschirob & Overte

- **Actor Repo:** [`rust-saschirob-mcp`](file:///D:/Dev/repos/rust-saschirob-mcp) (Owns 14-servo Feetech STS bus, cascaded mast kinematics, and MuJoCo active inference physics).
- **Environment Repo:** [`overte-mcp`](file:///D:/Dev/repos/overte-mcp) (Owns 3D OpenXR domain, entity server, and avatar presence).
- **In-World Teach Pendant:** Served at `http://127.0.0.1:11110/embed/saschirob-pendant` by `overte-mcp`'s FastAPI backend; spawned and parented beside the robot model by [`scripts/saschirob-overte-twin.js`](file:///D:/Dev/repos/overte-mcp/scripts/saschirob-overte-twin.js).
- **Physical Co-Presenter:** [`rust-yahboom-mcp`](file:///D:/Dev/repos/rust-yahboom-mcp) running on the physical Boomy robocar, projecting slides onto an A3 tabletop screen with active motor locks and Vincent Price voice cadence.
