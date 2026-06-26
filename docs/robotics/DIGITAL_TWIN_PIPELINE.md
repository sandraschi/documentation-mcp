# Digital Twin Pipeline: ROS 2 → 3D Visualization

**Scope**: Real-time 3D representation of the Yahboom Raspbot v2 (and future fleet robots) driven by live ROS 2 telemetry. The pipeline spans four repositories and a central standard. Each serves a distinct purpose — model authoring, web visualization, physics simulation, social VR, and cross-fleet conventions.

---

## Why this exists

The autonomous mission we built (Ollama → JSON → ROS → obstacle avoidance → vision detection) produces rich real-time data: ultrasonic readings, IMU heading, wheel velocity, servo positions, and mission status. This data currently renders as numbers on the Dashboard and Status pages. A digital twin makes it visible — you see the robot turning, the camera panning, the obstacle alert flashing on the model, all synchronized with what the physical robot is doing.

The same pipeline works for Bumi when it arrives. The ROS topics and TF frames change; the 3D pipeline stays the same.

---

## Component Architecture

The system has four roles, each owned by a different repository. They share data through ROS 2 topics and files on disk (STL mesh artefacts), not through direct dependencies.

**Model Authoring (blender-mcp)** creates the canonical 3D assets. An artist or engineer builds a rigged Boomy model with articulated joints (wheel rotation, servo pan and tilt, ultrasonic sensor orientation). The armature matches ROS 2 joint names so `/joint_states` can drive it directly. Exports happen in two formats: STL for the web (Three.js) and GLTF with armature for Unity3D and Resonite. Blender Python scripts automate the export pipeline so a mesh update doesn't require manually re-exporting four times.

**Web Visualization (yahboom-mcp, existing Viz.tsx)** is the quickest path to seeing the robot move. It already has Three.js, STL loading, and telemetry polling. The gaps are: proxy meshes need replacing with real Raspbot v2 STLs, joint animations need wiring to servo topics, and wheel rotation needs to respond to `/cmd_vel` history. This is the cheapest way to validate that the pipeline works before investing in Unity3D.

**Physics Simulation (unity3d-mcp)** provides the richest environment. Unity's physics engine simulates the mecanum wheel interactions with floor surfaces, collision detection against furniture, and realistic lighting for demo visibility. A ROS 2 subscriber inside Unity reads `/joint_states`, `/tf`, and `/odom` via rosbridge WebSocket (same pattern as the MCP server — rosbridge on the Pi, Unity client on the PC). The robot model uses the GLTF exported from Blender. Additional value: you can run "what-if" missions in Unity first, then deploy them to the real robot.

**Social VR (resonite-mcp)** places Boomy in a Resonite world. The Resonite session loads the same GLTF model and subscribes to ROS 2 telemetry through a lightweight WebSocket bridge. This is the demo layer — imagine attending a coffee shop demo remotely via VR, seeing Boomy's digital twin move in real time while punters watch the physical robot. Resonite's multiplayer means multiple people can observe simultaneously.

**Cross-Fleet Standard (robotics-mcp)** documents the conventions that make all of this work: the ROS 2 topic names and message types each component should publish and subscribe to, the TF frame hierarchy (base_footprint, base_link, camera_servo_pan, camera_servo_tilt, wheel_fl, etc.), the coordinate system convention (ROS 2 standard: X forward, Y left, Z up), and the recommended export settings for Blender GLTF. This document is the contract between hardware, software, and 3D teams. Adding a new robot to the fleet means publishing joint states in the standard format and the digital twin pipeline absorbs it without changes.

---

## Implementation Order

**Phase 1 — Fix the web visualizer (yahboom-mcp, Viz.tsx)**

The existing Viz.tsx is functional but uses placeholder meshes (X3 proxy) and doesn't animate joint motions. The first step is to replace the STL files with accurate Raspbot v2 meshes — the chassis, mecanum wheels, camera bracket, PTZ servos, and ultrasonic sensor. Yahboom's GitHub has STL files in the Raspbot-V2 repository under a models directory, or they can be extracted from the `Raspbot_V2_Yahboom.jpg` hero shot by modelling approximate dimensions.

Once the meshes load, wire the wheel objects to rotate in response to linear velocity from telemetry. The telemetry data already includes `velocity.linear` and `velocity.angular`, so wheel angular velocity = linear velocity / wheel radius. Servo objects need to rotate around their hinge axis in response to the last known servo position (stored in the camera PTZ state). The ultrasonic sensor mesh should tilt based on the sonar reading — closer objects could flash the mesh red.

This phase does not require changes outside yahboom-mcp. It depends on accurate meshes and a few hours of Three.js work.

**Phase 2 — Unity3D twin (unity3d-mcp)**

Unity3D-mcp is a new repository with a Unity project that imports the Blender-exported GLTF and subscribes to ROS 2 via rosbridge. The Unity scene has a floor plane, basic lighting, and the robot model. A C# script connects to `ws://192.168.1.11:9090` (or the Pi's Tailscale IP) and subscribes to `/joint_states`, `/tf`, and `/odom`.

The core class is a `RosBridgeSubscriber` that deserializes the JSON messages and applies transforms to the Unity GameObjects. Each joint in the armature maps to a named Transform in Unity's hierarchy. The mecanum wheel physics can be approximated by applying forces at the wheel contact points — Unity's WheelCollider handles this natively, though for a demo the simpler approach is to just rotate the wheel meshes and translate the root object according to `/odom` pose.

A separate script subscribes to `/ultrasonic` and shows a proximity ring or color flash on the front of the robot when an obstacle is near. This is the same data the mission executor uses for obstacle avoidance — visualizing it in Unity helps debug mission behavior.

The Unity build target is Windows standalone (the PC runs Unity and receives data from the Pi over the local network or Tailscale). No Unity build runs on the Pi — it's too heavy.

**Phase 3 — Resonite world (resonite-mcp)**

Resonite-mcp is a Resonite world package. The world spawns the Boomy GLTF model and runs a background `Coroutine` that opens a WebSocket to the Pi's rosbridge. The Resonite `WebSocketClient` component sends JSON subscribe messages for `/joint_states` and `/tf`, then applies received transforms to the model's slot hierarchy.

Resonite's advantage is zero-install for viewers. A Resonite session URL can be shared, and anyone with Resonite (free on Steam) joins the world and sees the robot moving in real time. For the coffee shop demo, the physical robot roams the shop while remote viewers in Resonite watch its digital twin from any angle.

The WebSocket bridge library for Resonite already exists in the community (Nioku's WebSocket client). The work is wiring it to ROS 2 topic names and mapping joint names to slot paths.

**Phase 4 — Standardize and document (robotics-mcp)**

The final phase is documentation. A `docs/robotics/DIGITAL_TWIN_PIPELINE.md` in robotics-mcp captures:
- ROS 2 topics and message types used by the pipeline
- TF frame naming convention (with examples for Boomy and Bumi)
- Blender armature structure requirements (bone names must match joint names)
- Export settings (GLTF 2.0, Y-up, embedded textures)
- Build and run instructions for each consumer (Viz.tsx, Unity, Resonite)
- Coordinate system alignment: ROS 2 (REP 103: X forward, Y left, Z up) maps directly to Unity (left-handed Z forward) via a -90° rotation around X on the root transform. Three.js (right-handed Y-up) only needs the standard ROS→Three.js quaternion conversion already used in Viz.tsx.

---

## ROS 2 Topics Consumed by All Consumers

| Topic | Type | Frequency | Purpose |
|-------|------|-----------|---------|
| `/tf` | tf2_msgs/TFMessage | ~50 Hz | Root pose, sensor frame transforms |
| `/joint_states` | sensor_msgs/JointState | ~10 Hz | Servo angles, wheel rotation |
| `/ultrasonic` | std_msgs/Float32 | ~10 Hz | Obstacle proximity visualization |
| `/odom` | nav_msgs/Odometry | ~50 Hz | Ground truth pose for Unity physics |
| `/cmd_vel` | geometry_msgs/Twist | on change | Wheel rotation speed cue |
| `/boomy/mission_status` | std_msgs/String | on change | Mission phase indicator overlay |

---

## File Formats and Dependencies

```
blender-mcp/                              # Authoring
  models/boomy/
    boomy_chassis.blend                   # Master Blender scene with armature
    export_stl.py                         # Script: exports rigid parts as STL
    export_gltf.py                        # Script: exports full rig as GLTF
    meshes/
      chassis.stl                         # For Viz.tsx (Three.js)
      wheel_fl.stl, wheel_fr.stl, ...     # 4 mecanum wheels
      camera_bracket.stl
      ultrasonic_holder.stl
    boomy_rigged.gltf                     # For Unity + Resonite (armature + meshes)
```

No Unity or Resonite project runs on the Pi. The Pi (or Bumi's Jetson) runs ROS 2 and rosbridge. 3D applications run on the PC, reading ROS data over the network via WebSocket. This keeps the compute load off the robot.

---

## Why Not Just One Repo

Each consumer has different dependencies and deployment targets. Unity3D-mcp needs a Unity Editor license and builds a Windows executable (500 MB+). Resonite-mcp is a Resonite world package that only loads inside Resonite. Viz.tsx lives inside yahboom-mcp's webapp and has no external dependencies beyond the browser. Blender-mcp requires Blender to be installed. Robotics-mcp is documentation shared across all fleet projects. Combining them would create a monorepo with conflicting dependency chains and build tools. Separate repos with a shared standard (robotics-mcp) is the cleaner architecture.

The ROS 2 topics and TF frames are the interface. As long as every consumer reads from the same topics, the pipeline works regardless of which repo the 3D code lives in.

---

## Effort Estimate

| Phase | Repo | Effort | Dependencies |
|-------|------|--------|-------------|
| 1. Web viz | yahboom-mcp | 4-6 hours | Raspbot STL meshes |
| 2. Unity twin | unity3d-mcp | 8-12 hours | Blender GLTF export, rosbridge on Pi |
| 3. Resonite world | resonite-mcp | 4-6 hours | GLTF import in Resonite, WebSocket client |
| 4. Standards | robotics-mcp | 2 hours | Phases 1-3 done, conventions extracted |

Total: approximately 20-26 hours over multiple sessions. Phase 1 is the highest-leverage starting point — it improves the existing Viz page with accurate meshes and joint animations, giving immediate visual feedback without installing any new software.
