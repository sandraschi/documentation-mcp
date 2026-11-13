# RobotCraft — Handover Document

**Last Updated**: 2026-11-10
**Current State**: Active Architecture
**Primary Artifact**: [sandraschi/robotcraft](https://github.com/sandraschi/robotcraft)

---

## 1. What Was Done
- Scaffolding of universal robotics cockpit consolidating 9 fleet repos.
- Kinematic solver abstractions and URDF model parsing.
- Control port `14116` allocated in `WEBAPP_PORTS.md`.

---

## 2. Immediate Next Steps
1. Connect LeRobot dataset replay pipeline for physical arm actuation.
2. Link `teleoperator-mcp` WebXR poses into `robotcraft-app` 3D viewport.
