# raspberrypi-mcp

FastMCP 3.4 — **Raspberry Pi MCP**. The Pi as a lab instrument: GPIO, I2C, SPI,
system health, CSI camera, and Pico/Pico 2 MCU management (UF2 flashing +
MicroPython REPL). Simulator by default — no hardware needed.

## Quick start

```powershell
Set-Location D:\Dev\repos\raspberrypi-mcp
uv sync --extra dev
uv run python run_server.py --stdio
```

## Tools (all return `{success, message, data}`)

- `pi_device` — list, connect, disconnect, status
- `pi_gpio` — read, write, pwm, status (BCM, lgpio on Pi 5)
- `pi_i2c` — scan, read, write
- `pi_spi` — full-duplex transfer
- `pi_sys` — info, temp (model, throttling)
- `pi_cam` — info, snapshot (CSI via rpicam)
- `pi_pico` — list, info, flash_uf2, repl_exec
- `pi_help` — quickstart, discover, status
- `pi_shutdown` — graceful self-termination

Plus prompt `pi_bringup_guide`, resources `resource://pi/*`.
REST: `/health`, `/api/status`, `/api/capabilities`, `/api/v1/diagnostics`,
peer-call contract `/api/tools` + `/api/tools/{name}/call`.

## Ports

Backend: **11218** · Frontend: **11217** (web_sota dashboard)

## Fleet

Bench family: peered by `bench-orchestrator-mcp`, sibling to `jtag-swd-mcp`
(SWD debug), `oscilloscope-mcp`, `logic-analyzer-mcp`, `multimeter-mcp`,
`power-supply-mcp`, `function-generator-mcp`, `bench-camera-mcp`.
New in 0.1.0 (assfix-zero scaffold, 2026-09-29).
