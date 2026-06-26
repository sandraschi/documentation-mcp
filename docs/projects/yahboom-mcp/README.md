# yahboom-mcp — Yahboom Raspbot v2 ROS 2 MCP + dashboard

**FastMCP 3.2** — Unified Gateway: MCP (stdio/SSE) + REST + Vite dashboard.
**v2.4.2** — Container hygiene overhaul, camera pipeline, GPIO, PTZ demo.

> Industrial-grade agentic control for Yahboom Raspbot v2 (Raspberry Pi 5 / ROS 2 Humble).

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\yahboom-mcp` (or clone `sandraschi/yahboom-mcp`) |
| **Ports** | Backend **10892**, Dashboard **10893** (Vite proxies `/api` → 10892) |
| **Pi IPs** | WiFi: `192.168.1.11` · Ethernet: `192.168.0.250` · Ollama: `192.168.1.11:11434` |
| **ROS container** | `yahboom_ros2_final` (image `yahboomtechnology/ros-humble:0.1.0`, 6.3GB) |
| **Start** | `webapp\start.ps1`, or `uv run python -m yahboom_mcp.server --mode dual --host 127.0.0.1 --port 10892` |

---

## Container Architecture (v2.4.2)

The `yahboom_ros2_final` container runs **everything** in one container with `--network host`:

```
yahboom_ros2_final (host networking, privileged)
├── rosbridge_websocket (port 9090)  ← installed via apt ros-humble-rosbridge-server
├── Mcnamu_driver (driver_node)
├── robot_state_publisher, joint_state_publisher
├── camera_publisher (/camera_publisher.py → /image_raw/compressed)
├── mission_executor (/boomy/mission → /cmd_vel)
├── detection_bridge (SSD MobileNet v2 → /boomy/detections_json)
├── usb_cam → /image_raw (raw) + image_transport republish → compressed
└── rosapi (/rosapi/*)
```

### Why one container

Rosbridge DDS subscriptions **cannot receive data** when rosbridge and driver nodes are in separate containers (even with `--network host`). The earlier "sidecar" pattern (`yahboom_rosbridge_sidecar` + `yahboom_ros2_final`) caused a **Telemetry Blackout** — the MCP server could publish `cmd_vel` (outbound) but never received sensor data (inbound). Installing rosbridge-server in the driver container fixed this.

### Systemd survive-reboot

- `/etc/systemd/system/yahboom-robot.service` — enabled
- `/usr/local/bin/yahboom-launch.sh` — wrapper targeting `yahboom_ros2_final`
- Container has `--restart unless-stopped`

---

## Autonomous Missions (v2.4.0+)

Natural-language goals → Ollama planning (Gemma3:1b on Pi) → structured JSON → ROS execution → status feedback.

| Component | Topic |
|-----------|-------|
| **Ollama planner** | Goal → `MissionPlanV1` JSON (intent, behavior, target_description) |
| **Mission executor** | Sub: `/boomy/mission`, `/ultrasonic`, `/boomy/detections_json` · Pub: `/cmd_vel`, `/boomy/mission_status` |
| **Detection bridge** | SSD MobileNet v2 COCO (90 classes) · Pub: `/boomy/detections_json` |
| **Obstacle avoidance** | Ultrasonic < 25 cm → reverse + turn |

**Example**: "find our dog" → Ollama: `{"intent":"search","target_description":"a dog","behavior":"room_search"}` → executor drives sinusoidal pattern, detection bridge spots "dog" (87% confidence), executor stops and reports `{"status":"target_found"}`.

See: **[AUTONOMOUS_MISSIONS.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/AUTONOMOUS_MISSIONS.md)**

### AI Roadmap (in the works)

| Item | Status |
|------|--------|
| **Gemma 3 1B** | Running — 778MB, text-only, handles mission planning |
| **Gemma 4 E2B / E4B** | **Multimodal on Pi 5 16 GB** — vision + audio + tools via `gemma4:e2b` / `gemma4:e4b` (Ollama or LiteRT-LM). E2B &lt;1.5 GB, E4B ~5 GB at 4-bit. See [GEMMA4_EDGE_ON_RASPBOT.md](../../robotics/research/GEMMA4_EDGE_ON_RASPBOT.md). |
| **Gemma 4 12B** | Desktop counterpart (`gemma4:12b` on 4090) — same multimodal story, encoder-free images. |
| **Pi storage** | SD card 95% full (2.2GB free on 46GB). Prune before pulling new Ollama weights. |
| **Pi RAM** | **16 GB** — sized for Gemma 4 edge variants alongside ROS (not 7B text-only legacy planning). |

---

## Camera Pipeline (v2.4.2)

Two-tier capture:

1. **VideoBridge** (primary): Subscribes to `/image_raw/compressed` via rosbridge. Falls back to direct `/dev/video0` capture on the host PC (disabled for remote — set `YAHBOOM_CAMERA_DIRECT=1` to force).
2. **SSH snapshot fallback**: `/api/v1/snapshot` runs `docker exec yahboom_ros2_final python3 -c "import cv2; ..."` to capture a single JPEG frame over SSH when VideoBridge has no frames. Returns 200 OK with JPEG.

Camera device (`/dev/video0`) is shared — only one process can open it at a time. The host `raspbot` server (port 6001) and the container `usb_cam` / `camera_publisher` compete for it. Kill whichever holds the device before starting a different capture.

---

## PTZ Camera + GPIO (v2.4.2)

- **PTZ Demo**: Sweeps camera through a 16-point geometric pattern covering the full 0–180° range in both pan and tilt axes. Button in Dashboard next to "Center".
- **GPIO**: `POST /api/v1/gpio` with `{"pin":"headlight","value":true}` controls GPIO 17 via sysfs. LEDs on GPIO 23/24 also available. Headlight toggle in Dashboard.

---

## Operator starter (read first)

**[Startup & bringup](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/STARTUP_AND_BRINGUP.md)** — Boot order; **ROS 2** vs **rosbridge_suite** (WebSocket software on the Pi) vs **USB-linked controller hardware under the Pi** (often confused with "rosbridge"); Docker + systemd scripts on the Pi; what **Reconnect** vs **Hard Reset** do; **Dashboard** (basic link) vs **Diagnostic Hub** (ROS topics / nodes). **MCP Central RAG (full text):** [STARTUP_AND_BRINGUP.md](../../docs/robotics/yahboom/STARTUP_AND_BRINGUP.md), [STACK_HEALTH_PROBE.md](../../docs/robotics/yahboom/STACK_HEALTH_PROBE.md). Repo copies: [STACK_HEALTH_PROBE.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/STACK_HEALTH_PROBE.md).

---

## Tools

- **yahboom(operation, …)** — Single portmanteau tool: motion, sensors, diagnostics, etc.
- **yahboom_help(category, topic)** — Structured help.
- **yahboom_agentic_workflow(goal)** — High-level goals with sampling.
- **yahboom_agent_mission(goal)** — Autonomous mission: LLM planning → ROS execution.

---

## Webapp Pages

| Page | Path | Purpose |
|------|------|---------|
| Dashboard | `/dashboard` | Camera, WASD drive, PTZ (with demo), GPIO headlight, lightstrip, voice |
| Status | `/status` | Connection health, telemetry, stack diagnostics |
| Missions | `/missions` | Natural-language goals, sample missions, report-back |
| Diagnostic Hub | `/diagnostics` | ROS topics, nodes, SSH shell, stack table |
| Server logs | `/logs` | Live SSE log stream with filter, export, sort |

---

## Cursor / Claude Desktop (stdio MCP)

```json
"yahboom-mcp": {
  "command": "D:/Dev/repos/uv-install/uv.exe",
  "args": ["--directory", "D:/Dev/repos/yahboom-mcp", "run", "python", "-m", "yahboom_mcp.server", "--mode", "stdio"],
  "env": { "PYTHONUNBUFFERED": "1", "PYTHONPATH": "src" }
}
```

**HTTP/SSE MCP** (same process as dashboard): point clients at `http://127.0.0.1:10892/sse` when the gateway runs with `--mode dual`.

Env: **`YAHBOOM_IP`**, **`YAHBOOM_BRIDGE_PORT`** (rosbridge, default 9090), **`OLLAMA_BASE_URL`** (default `http://192.168.1.11:11434`).

---

## Documentation (in repo)

| Doc | Topic |
|-----|--------|
| [AUTONOMOUS_MISSIONS.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/AUTONOMOUS_MISSIONS.md) | Ollama planning → ROS execution → vision detection → obstacle avoidance |
| [RASPBOT_V2_HARDWARE_STACK.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/hardware/RASPBOT_V2_HARDWARE_STACK.md) | Chassis, sensors, expansion board, Pi, battery, switch |
| [ROSMASTER_ARCHITECTURE.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/hardware/ROSMASTER_ARCHITECTURE.md) | Dual-bus (I2C + UART), register map, container architecture |
| [STARTUP_AND_BRINGUP.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/STARTUP_AND_BRINGUP.md) | Power, network, Docker, bringup, webapp surfaces |
| [STACK_HEALTH_PROBE.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/STACK_HEALTH_PROBE.md) | **`health.stack`**, container lifecycle, restart loop, redacted log preview |
| [ROSBRIDGE.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/hardware/ROSBRIDGE.md) | `ROS2Bridge`, topics, env |
| [PI_LESS_SETUP.md](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/ops/PI_LESS_SETUP.md) | ESP32 / PC-as-brain |

---

## Fleet

- **Starts**: `mcp-central-docs/starts/yahboom-start.bat` → `yahboom-mcp/webapp/start.bat`
- **Registry**: `mcp-central-docs/operations/fleet-registry.json` → `yahboom-mcp`

---

## Container Hygiene — Lessons Learned (2026-05-11)

A multi-hour debugging session that culminated in a single root cause:

1. **Host rosbridge disabled** — `yahboom-robot.service` renamed to `.disabled`. Later re-enabled after fixing the wrapper to use the correct container name (`yahboom_ros2_final`, not `yahboom_ros2`).
2. **Sidecar pattern failure** — Running rosbridge in `yahboom_rosbridge_sidecar` and driver nodes in `yahboom_ros2_final` worked for outbound publishing but broke inbound DDS subscriptions. The MCP saw all topics, published successfully, but never received sensor data (Telemetry Blackout).
3. **Unified container fix** — `apt-get install ros-humble-rosbridge-server` inside the driver container (required ROS apt repository setup and working DNS). Both rosbridge and driver now share one DDS participant.
4. **Camera contention** — Host `raspbot.pyc` (port 6001) holds `/dev/video0`. Container can't open it simultaneously. Kill host process or use SSH-based capture fallback.
5. **Pi disk full** — 95% used. `docker system prune` freed ~1.5GB. Can't install larger AI models without storage expansion.

**Backup exists**: 2.05GB container export + docker commit + systemd configs. The Pi state is NOT in GitHub — a full SD card image backup is recommended.
