# RSICraft — Handover Document

**Last Updated**: 2026-11-10
**Current State**: v0.1.0 Hardened Pass
**Primary Artifact**: [sandraschi/rsicraft](https://github.com/sandraschi/rsicraft)

---

## 1. What Was Done
- Transactional SQLite mutations in `rsicraft-core`.
- Hardened Docker sandbox with `cap-drop`, `no-new-privileges`, and host-side process reaper.
- egui 0.37 desktop studio interface.
- 29 tests passing with clean clippy lints.

---

## 2. Immediate Next Steps
1. Move dispatch off the UI thread to eliminate window freezing during long inference steps.
2. Connect to `AICraft` telemetry bus for token and latency logging.
