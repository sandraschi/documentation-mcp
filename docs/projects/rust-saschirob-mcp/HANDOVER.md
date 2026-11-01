# HANDOVER: Saschirob Fleet Mesh & TU Wien Club Demo

**Last Updated:** 2026-10-28 13:20 CET  
**Repo:** `rust-saschirob-mcp` (Mirrored from root)  
**Current State:** Fully Operational & Rehearsed  
**Next Milestone:** TU Wien Student Robotics Club Presentation (Karlsplatz, Vienna)

---

## 1. What Was Just Completed

1. **Dashboard & Multi-Environ Hero Overhaul (`crates/saschirob-app/src/app.rs`):**
   - Redesigned the primary Dashboard with the Vienna Open Humanoid concept hero.
   - Added the explicit multi-environ banner: `"Spawns in: MuJoCo, Isaac Lab, NVIDIA Cosmos, DeepMind Genie 4, Godot 4, Unity3D, Overte, Resonite, VRChat, Blender, FreeCAD, WebXR"`.
   - Added a 5-row One-Click Dojo Action Launcher with explicit starter texts (*"What is this demonstrating?"*) for MuJoCo, Overte, Godot, Cosmos/Genie, and Blender/FreeCAD.
2. **MuJoCo Active Inference Dance (`simulation/mujoco/dance.py`):**
   - Created and verified an 18-actuator sinusoidal active inference compliance dance script.
   - Synchronizes 3-stage column elevation ($0.69\text{m} \leftrightarrow 1.40\text{m}$) and bimanual greeting wave.
3. **Overte Diegetic Teach Pendant Integration (`overte-mcp`):**
   - Added zero-CDN responsive dark HTML Teach Pendant at `/embed/saschirob-pendant` on port 11110.
   - Created in-world script [`overte-mcp/scripts/saschirob-overte-twin.js`](file:///D:/Dev/repos/overte-mcp/scripts/saschirob-overte-twin.js) to spawn the robot model and parent the interactive Web entity pendant.
4. **Physical Boomy Robocar Presentation Controller (`scripts/boomy_presenter.py`):**
   - Enforced hardware table-edge anti-drop guard (motor speed locked to $0.0\text{ m/s}$).
   - Locked lightstrip to warm amber profile, strictly disarming flashing police car sirens.
   - Implemented PTZ micro-projector alignment onto the A3 tabletop screen.
5. **Master Rehearsal Suite (`scripts/rehearse_club_demo.py`):**
   - Complete 6-act automated rehearsal walk with Vincent Price voiceover cues, tested and passing with exit code 0.
6. **Fleet Meshing & Club Documentation:**
   - Authored PRD ([`docs/PRD_CLUB_DEMO_FLEET_MESH.md`](file:///D:/Dev/repos/rust-saschirob-mcp/docs/PRD_CLUB_DEMO_FLEET_MESH.md)).
   - Authored Plan ([`docs/PLAN_CLUB_DEMO_FLEET_MESH.md`](file:///D:/Dev/repos/rust-saschirob-mcp/docs/PLAN_CLUB_DEMO_FLEET_MESH.md)).
   - Authored Technical Assessment ([`docs/ASSESSMENT_CLUB_DEMO_FLEET_MESH.md`](file:///D:/Dev/repos/rust-saschirob-mcp/docs/ASSESSMENT_CLUB_DEMO_FLEET_MESH.md)).
   - Authored Demo Video Storyboard ([`docs/DEMO_VIDEO_SPEC.md`](file:///D:/Dev/repos/rust-saschirob-mcp/docs/DEMO_VIDEO_SPEC.md)) and validated YAML in `demo-vid-mcp`.

---

## 2. Verification Gate Evidence

- `cargo clippy --workspace --all-targets --all-features -- -D warnings`: **0 warnings**.
- `cargo test --workspace`: **43 passed; 0 failed**.
- `cargo run -p saschirob-app -- --smoke`: **13/13 dispatches ok, 14/14 pages inventoried**.
- `overte-mcp` pytest: **9/9 passed**.
- Rehearsal execution: `py scripts/rehearse_club_demo.py`: **Pass (Exit code 0)**.

---

## 3. Deliberately NOT Done (Known Scope Boundaries)

- **Physical Actuator Driving on Saschirob:** Physical aluminum parts and SO-101 arm prints are in production at Happylab 1020 / TMW techLAB; actuator operations on Saschirob remain in software/demo emulation until hardware assembly is complete.
- **Boomy Autonomous Driving:** Boomy is intentionally restricted to stationary tabletop projection with active motor lock to prevent accidental falls.
- **Overte Public Server Deployment:** The Overte domain runs locally (`127.0.0.1:40100` / `11110`) for the demo; no external cloud dependency is required.

---

## 4. Next Immediate Steps

1. Run live interactive rehearsal with Steve on his GPD Duo dual-screen laptop (`py scripts/rehearse_club_demo.py --interactive`).
2. Test Pico 4 VR headset connection into local Overte domain to verify in-headset laser pointer clicking on `/embed/saschirob-pendant`.
3. Print A3 tabletop projection screen test pattern.
