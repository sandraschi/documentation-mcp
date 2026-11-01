# Installing open-drone-mcp

> **First time?** Complete [docs/ONBOARDING.md](docs/ONBOARDING.md) before expecting real flight.
> The simulator needs no hardware and works right after Option A or B below.

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Claude Desktop | MCP host | [download](https://claude.ai/download) |
| Git | Clone the repo | `winget install Git.Git` |
| Python + uv | Run the server (uv installs Python 3.12 for you) | `winget install astral-sh.uv` |

> Windows: all installs via [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/).
> macOS and Linux are untested.

Real Crazyflie hardware additionally needs a Crazyflie, a Crazyradio 2.0 dongle, and the Bitcraze
Zadig driver step. See ONBOARDING.

## Option A - Manual configuration (recommended today)

1. Clone and install:

```powershell
git clone https://github.com/sandraschi/open-drone-mcp
cd open-drone-mcp
uv sync
```

2. Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "open-drone": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\open-drone-mcp", "run", "open-drone-mcp"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "OPEN_DRONE_BACKEND": "dryrun"
      }
    }
  }
}
```

Config file location:

- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

3. Restart Claude Desktop.

## Option B - Real Crazyflie

```powershell
uv sync --extra crazyflie
```

Then set, in the `env` block above:

```json
"OPEN_DRONE_BACKEND": "crazyflie",
"OPEN_DRONE_URI": "radio://0/80/2M/E7E7E7E7E7",
"OPEN_DRONE_ENABLE_ACTUATION": "1",
"OPEN_DRONE_ALLOW_REAL_VEHICLE": "1"
```

Leave the last two at `"0"` (or unset) until the bench test in ONBOARDING passes. With them off the
server can connect and read telemetry but will refuse to take off.

Use **Python 3.12** (the repo pins it via `.python-version`). `cflib` installs cleanly on 3.12 with no
compiler; Bitcraze documents that Python 3.13 on Windows needs the Visual Studio C++ workload.

## Option C - `.mcpb` bundle (simulator only)

```powershell
just mcpb-pack        # needs Bun: winget install Oven-sh.Bun
```

This builds `dist/open-drone-mcp-v0.1.0.mcpb`; drag it onto Claude Desktop. The bundle starts the server
with `uv run --with <deps>`, so the machine only needs `uv`. **It contains the simulator and the safety
engine, not the Crazyflie library**: `cflib` is GPL and is never bundled. For real hardware use Option A
plus `uv sync --extra crazyflie`. The bundle is unsigned and has not yet been installed in Claude Desktop
itself; it passes the fleet's pack checks and starts from a clean unpacked copy.

## Web console

```powershell
.\start.bat          # or: just serve (MCP only)
```

Starts the API on <http://127.0.0.1:11222> and the console on <http://127.0.0.1:11221> (ports claimed in
`mcp-central-docs/operations/WEBAPP_PORTS.md`) and opens the browser. Needs Node.js
(`winget install OpenJS.NodeJS`); `start.bat` runs `npm install` when needed. The MCP endpoint is also served
at <http://127.0.0.1:11222/mcp>. The server only accepts loopback Host headers and refuses foreign browser
origins; see docs/TROUBLESHOOTING.md if you put it behind another name.

## Optional Companions (Fleet Crossconnects)

`open-drone-mcp` runs standalone. One companion is wired:

**`devices-mcp` (room camera)** - off by default. To let an assistant, and the Flight page, see the flight area:

1. Run [`devices-mcp`](https://github.com/sandraschi/devices-mcp) and note the NAME of one camera that only sees
   the flight area.
2. In the `env` block of the MCP client config (or `.env`), set `OPEN_DRONE_ENABLE_CAMERA=1` and
   `OPEN_DRONE_CAMERA_NAME=<that name>`. Optionally `OPEN_DRONE_CAMERA_URL=http://127.0.0.1:<port>`; otherwise the
   port is read from the fleet registry if it is on the machine.
3. Restart the server. `drone_camera(operation="status")` should report the camera as found.

Read the privacy note in the README first: every frame an assistant requests is sent to your LLM provider, and the
assistant is deliberately unable to choose or list any other camera.

## Verify Installation

In Claude Desktop, ask:

> "Connect to the drone and tell me the battery level."

You should see a connection to the `dryrun` backend and a battery reading with `"simulated": true`.
Command-line check:

```powershell
uv run pytest -q
```

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).
