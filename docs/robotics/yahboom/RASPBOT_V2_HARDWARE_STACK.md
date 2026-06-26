# Yahboom Raspbot v2 — Hardware stack (fleet index)

**Canonical document:** [`yahboom-mcp/docs/hardware/RASPBOT_V2_HARDWARE_STACK.md`](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/hardware/RASPBOT_V2_HARDWARE_STACK.md)

That file is the **single source of truth** for: **§1** — **MCU**, **Micro-ROS**, **rosbridge (software on Pi)**, **Debian / Docker / ROS 2 Humble**; chassis through battery; **§15** — **assembly placeholder** (detailed build guide to replace thin Yahboom box leaflet).

Update hardware narrative in fleet docs here only by **linking** or summarizing — avoid drifting copies.

**Software bringup (full text in this folder for RAG):** **[STARTUP_AND_BRINGUP.md](STARTUP_AND_BRINGUP.md)** (Goliath ↔ Pi, Docker, webapp, endpoints) and **[STACK_HEALTH_PROBE.md](STACK_HEALTH_PROBE.md)** (`GET /api/v1/health` → **`stack`**, env vars, restart loop, docker log preview). Use those for semantic search instead of duplicating hardware chapters here.
