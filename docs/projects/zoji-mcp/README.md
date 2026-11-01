# zoji-mcp

Tracks the water level of a Zojirushi electric water boiler by weight, and
exposes level, events and refill alerts as MCP tools.

Two independent hardware paths (USB Dymo postal scale, ESP32 + HX711 load
cell over MQTT) feed one shared logic layer that turns a raw weight stream
into classified events: refills, dispenses, drift, pot removal, and lever
presses. The evening check answers the real question: is there enough water
for tomorrow morning's coffee?

## What You Can Do

- **Know the level**: `get_level()` returns ml remaining, percent, confidence
  and source. `get_status()` adds drift estimate, pot presence and time since
  refill.
- **Never miss a refill**: REFILL / DISPENSE / LOW_WATER / POT_REMOVED events
  are classified, persisted to SQLite and pushed to a webhook or stdout.
- **Track consumption**: `consumption_report(days)` shows cups per day and
  refills per week. Every dispense-lever press is detected as a temporary
  weight gain and logged as a consumption signal.
- **Plan the morning**: `evening_check()` says yes/no - enough for tomorrow?
- **Calibrate in 2 steps**: empty pot, then full pot. No absolute thresholds;
  the engine re-baselines on every refill and tracks drift separately so a
  creeping load cell stays visible.
- **Two hardware paths, zero averaging**: Dymo HID and HX711/MQTT run in
  parallel; disagreements are logged, the primary source wins.

## Quick Install

```bash
git clone https://github.com/sandraschi/zoji-mcp
cd zoji-mcp
uv sync --all-extras
uv run python -m zoji_mcp.server        # stdio MCP server (replay MOCK source by default)
```

For hardware, copy `.env.example` to `.env` and set `ZOJI_SOURCES=dymo` (or
`hx711`) plus calibration. See [INSTALL.md](INSTALL.md) for all paths.

## Example Prompts

- "How much water is in the Zojirushi right now?"
- "Is there enough hot water for tomorrow morning?"
- "Show me my coffee consumption for the last week"
- "The pot was refilled - is the level reading correct?"

## Documentation

| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Architecture](docs/ARCHITECTURE.md) | WeightSource protocol, logic layer, data flow |
| [Configuration](docs/CONFIGURATION.md) | Env vars, thresholds, calibration |
| [Tool Reference](docs/TOOLS.md) | All MCP tools |
| [Hardware](docs/HARDWARE.md) | Dymo HID, ESPHome/HX711, Zadig fallback |
| [Development](docs/DEVELOPMENT.md) | Local setup, tests, traces |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues |

## Requirements

- Python 3.11+ and [uv](https://docs.astral.sh/uv/) (Option C/D)
- A Zojirushi electric water boiler on a scale: **Dymo M10/M25 USB HID scale**
  (VID 0x0922) or **ESP32 + HX711 + 20 kg load cell** with ESPHome/MQTT
- No hardware? The **replay source** (recorded CSV traces) works out of the
  box - clearly labeled MOCK data everywhere.

## License

MIT
