# open-drone-mcp

Control small DIY drones from an LLM through MCP, with a safety layer the LLM cannot talk its
way past. Crazyflie nano quads first; the simulator works with no hardware at all.

## What this wraps

**[Crazyflie](https://www.bitcraze.io/products/crazyflie-2-1-brushless/)** (Bitcraze), an open-source
nano quadcopter, via its Python library `cflib` and a Crazyradio USB dongle. Not DJI. Full
background in [docs/WRAPPEE.md](docs/WRAPPEE.md).

> **First time?** Read [docs/ONBOARDING.md](docs/ONBOARDING.md) before expecting real flight.
> The default backend is a **declared simulator** (`"simulated": true` in every response).

## Preview

| Dashboard | Flight console | Safety |
|-----------|----------------|--------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Flight](docs/screenshots/flight.png) | ![Safety](docs/screenshots/safety.png) |

*The web console running against the simulator. The red bar and the MOCK samples clear only when a
real vehicle is connected; the STOP button is on every page.*

## What You Can Do

**How it runs**: an MCP server (stdio by default, HTTP optional) plus a local web console. The LLM
sends waypoint-level commands (take off, go to, land). Stabilisation stays on the drone; the LLM never
sits in the control loop.

| Direction | Artifacts | Notes |
|-----------|-----------|-------|
| **Hands-in** | Natural-language flight requests, geofence and limit changes | Every command passes the safety engine first |
| **Hands-out** | Telemetry (position, battery), audit log, alerts | `drone_telemetry`, `drone_safety`, web console |

- Geofence box, speed cap and battery floor enforced server-side, independent of the LLM
- Motion on real hardware is OFF until you set two explicit flags
- `emergency_stop`, `land` and `hover` are never gated
- Append-only audit log of every command and every refusal
- Loosening a limit requires `confirm=true`; hard ceilings cannot be exceeded at all
- The web API refuses foreign browser origins and non-loopback Host headers, so a web page cannot fly your drone

## Quick Install

```powershell
git clone https://github.com/sandraschi/open-drone-mcp
cd open-drone-mcp
uv sync
uv run open-drone-mcp        # MCP over stdio (Claude Desktop)
.\start.bat                  # web console on http://127.0.0.1:11221
```

Real Crazyflie hardware: `uv sync --extra crazyflie`, then see [INSTALL.md](INSTALL.md).
ArduPilot multirotors over MAVLink: `uv sync --extra mavlink` and `OPEN_DRONE_BACKEND=mavlink`; see
[docs/ONBOARDING.md](docs/ONBOARDING.md) section 5d. **Passes a fake autopilot and ArduPilot 4.5.7 SITL; never flown.**
A simulator-only `.mcpb` bundle can be built with `just mcpb-pack`.

## Example Prompts

- "Connect to the drone and tell me the battery level."
- "Take off to 0.5 metres, move 0.3 m forward, then land."
- "Shrink the geofence to a 1 m square around the coffee table."
- "Before you take off, look at the room and tell me if the flight area is clear." (needs the room camera)

## Fleet Crossconnects (Companions)

`open-drone-mcp` works completely standalone.

| Companion Server | Feature Unlocked | Status | Setup |
|---|---|---|---|
| [`robotics-mcp`](https://github.com/sandraschi/robotics-mcp) | Shared robot dashboard and virtual twin | Optional, not yet wired | n/a |
| [`devices-mcp`](https://github.com/sandraschi/devices-mcp) | `drone_camera`: one still from ONE room camera you name, plus a live still on the Flight page | Optional, **off by default** | [Setup](docs/CONFIGURATION.md) (`OPEN_DRONE_ENABLE_CAMERA`, `OPEN_DRONE_CAMERA_NAME`) |

> **Camera privacy**: every frame an assistant asks for goes to the LLM provider your client uses. The tool has no
> camera argument, so the assistant cannot list or pick other cameras, even though `devices-mcp` may serve your
> kitchen or doorbell. Choose a camera that only sees the flight area.

## Documentation

| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Onboarding](docs/ONBOARDING.md) | Cost, hardware, first flight, pitfalls |
| [Wrapped app](docs/WRAPPEE.md) | Crazyflie, official links, community |
| [Camera drone: Holybro X500 v2](docs/hardware/HOLYBRO_X500_V2.md) | Spec, shopping list, usage analysis, first-flight protocol |
| [Onboard camera design](docs/ONBOARD_CAMERA.md) | Stage 2, not built |
| [Architecture](docs/ARCHITECTURE.md) | Safety engine, backends, web layer, data flow |
| [Configuration](docs/CONFIGURATION.md) | Env vars, ports and safety flags |
| [Tool Reference](docs/TOOLS.md) | MCP tools and REST endpoints |
| [Development](docs/DEVELOPMENT.md) | Local setup, tests, declared doubles |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues |

## Requirements

Windows 11 (Linux/macOS untested), `uv` (installs Python 3.12 for you), Node.js for the web console.
Real flight additionally needs a Crazyflie, a Crazyradio 2.0, and the Zadig driver step on Windows.

## Status

Phase 1 plus web console and MCPB bundle. The simulator, safety engine and web layer are tested
(179 pytest tests, 28 Playwright end-to-end tests). The Crazyflie backend is implemented but **not yet
flown on real hardware**. The desktop installer (Tauri/NSIS) is not built yet. See [CHANGELOG.md](CHANGELOG.md).

## License

MIT. The optional `cflib` dependency (Crazyflie hardware) is GPL; see [docs/WRAPPEE.md](docs/WRAPPEE.md)
before redistributing anything that bundles it.
