# yahboom-mcp - Yahboom Raspbot v2 ROS 2 MCP Server

**FastMCP 3.1 — Portmanteau, sampling (SEP-1577), prompts, skills, scripts**

> Industrial-grade agentic control for Yahboom Raspbot v2 (Raspberry Pi 5 / ROS 2 Humble). Unified Gateway: MCP (stdio/SSE) + REST API + Vite dashboard.

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\yahboom-mcp` |
| **Ports** | Backend 10792, Dashboard 10793 |
| **Protocol** | FastMCP 3.1 |
| **Start** | `starts/yahboom-start.bat` or `uv run python -m yahboom_mcp.server --mode stdio` (Cursor) / `--mode dual --port 10792` (dashboard) |

---

## Tools

- **yahboom(operation, param1, param2, payload)** — Single operation: health_check, forward, backward, turn_left, turn_right, strafe_left, strafe_right, stop, read_imu, read_battery, read_encoders, start_recording, stop_recording, list_trajectories, config_show.
- **yahboom_help(category, topic)** — Multi-level help (motion, sensors, connection, api, mcp_tools, startup, troubleshooting).
- **yahboom_agentic_workflow(goal)** — High-level natural-language goal; uses `ctx.sample()` with sub-tools (get_robot_health, move_robot, read_sensors) for SEP-1577 agentic execution.

---

## Prompts

- **yahboom_quick_start(robot_ip)** — Setup and connect instructions.
- **yahboom_patrol(duration_seconds)** — Patrol plan (e.g. square).
- **yahboom_diagnostics()** — Diagnostic checklist.

---

## Skills & Scripts

- **skills/yahboom-operator.md** — Operator skill: when to use which tool, prompts, workflow rules.
- **scripts/check_health.py** — REST health/telemetry without MCP: `python scripts/check_health.py [--base http://localhost:10792]`.
- **scripts/run_patrol_square.ps1** — Check server and print agentic workflow usage.

---

## Cursor / Claude Desktop

```json
"yahboom-mcp": {
  "command": "D:/Dev/repos/uv-install/uv.exe",
  "args": ["--directory", "D:/Dev/repos/yahboom-mcp", "run", "python", "-m", "yahboom_mcp.server", "--mode", "stdio"],
  "env": { "PYTHONUNBUFFERED": "1" }
}
```

Connection: `YAHBOOM_IP`, `YAHBOOM_BRIDGE_PORT` (rosbridge). For **Pi-less**: `YAHBOOM_CONNECTION=esp32`, `YAHBOOM_IP` (ESP32), `YAHBOOM_ESP32_PORT` (default 2323); or `.\webapp\start.ps1 -RobotIP <ip> -Connection esp32`.

---

## Documentation (in repo)

- **[Pi-less Setup](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/PI_LESS_SETUP.md)** — PC-as-brain, ESP32 bridge, ~$100 bot, protocol.
- **[Hardware & ROS 2](https://github.com/sandraschi/yahboom-mcp/blob/main/docs/HARDWARE_AND_ROS2.md)** — ROSMASTER/STM32 (no OS), Pi tiers (minimal cam/PTZ vs Pi 5 for ROS 2 + LLM), ROS 2 interaction (SSH vs rosbridge), optional terminal tools, LIDAR integration.

---

## Fleet

- **Manifest**: `scripts/fleet-webapp-manifest.json` — yahboom-mcp, webapp/start.ps1, port 10792.
- **Starts symlink**: `starts/yahboom-start.bat` → `yahboom-mcp/webapp/start.bat`.
