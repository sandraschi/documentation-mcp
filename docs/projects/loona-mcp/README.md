# Loona MCP

FastMCP 3.2+ server for the KEYi Loona Petbot — hardware reverse engineering, motor/sensor control, and AI companion stack.

**Status: Pre-Alpha (Phase 1 — ADB Probe)**

## Dual-Track Architecture

| Track | Approach | Goal |
|-------|----------|------|
| **Software** | ADB shell → dump firmware → WiFi API reverse-engineering | Access existing hardware without physical modification |
| **Hardware** | UART → eMMC dump → motor protocol sniff → RPi gut+replace | Full control with modern AI stack on known hardware |

## Attack Vectors (Priority Order)

1. **USB-C ADB** — plug into Goliath, run `adb devices` (free, try first)
2. **UART test pads** — scan PCB for TX/RX/GND near SoC + CP2102 adapter
3. **eMMC ISP clip** — in-circuit read via BGA153 clip (non-destructive)
4. **eMMC chip-off** — desolder and read externally (destructive last resort)

## Fleet Tooling

| Tool | Port | Use |
|------|------|-----|
| `logic-analyzer-mcp` | 10985 | Motor protocol sniffing via sigrok |
| `oscilloscope-mcp` | 10936 | Analog probing of motor/sensor rails |
| `reversing-mcp` | 10750 | Firmware binary static analysis |
| `yahboom-mcp` | 10892 | Motion/sensor patterns to clone |

## Hardware

- **SoC**: 5 TOPS BPU, likely Rockchip RV1126
- **RAM**: LPDDR4 2GB
- **Storage**: eMMC 8GB
- **Sensors**: 720p RGB cam, 3D ToF, 4-mic array, accel/gyro/mag
- **Actuators**: 2x BLDC (wheels), 2x brushed DC (body), 2x brushed DC (ears)
- **Ports**: USB-C (data lines unconfirmed)

## Quick Start

```powershell
# Install
uv sync

# Run MCP server (stdio for Claude Desktop/Cursor)
just serve

# Run HTTP server
just serve-http

# Run tests
just test
```

## Documentation

- [SPEC.md](docs/SPEC.md) — architecture, tool surface, open questions
- [ATTACK_PLAN.md](docs/ATTACK_PLAN.md) — Phase 1-3 attack vectors with tooling lists
- [HARDWARE_RE.md](docs/HARDWARE_RE.md) — known hardware, PCB photos, community RE status
- [MOTOR_PROTOCOL.md](docs/MOTOR_PROTOCOL.md) — motor inventory, protocol hypotheses, RPi driver candidates

## Ports

- Backend: 11069 (FastAPI + FastMCP HTTP)
- Frontend: 11070 (Vite React, future)

## References

- Teardown blog: https://vector.thedroidyouarelookingfor.info/category/loona/
- Ear motor replacement (PCB photos): https://vector.thedroidyouarelookingfor.info/2023/03/12/changing-loonas-ear-motors-with-lots-of-pictures/
- Loona Discord: https://discord.gg/loona
- loona-api (deleted from GitHub, need mirror)
