# Configuration

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPEN_DRONE_BACKEND` | `dryrun` | `dryrun` (simulator) or `crazyflie` (real hardware). Unknown values give a structured `configuration` error |
| `OPEN_DRONE_URI` | unset | Crazyflie radio URI used by `connect` when no `uri` is passed, e.g. `radio://0/80/2M/E7E7E7E7E7` |
| `OPEN_DRONE_ENABLE_ACTUATION` | `0` | Gate 1 for motion on a **real** backend. Truthy: `1`, `true`, `yes`, `on` |
| `OPEN_DRONE_ALLOW_REAL_VEHICLE` | `0` | Gate 2 for motion on a **real** backend. Both gates are required |
| `OPEN_DRONE_ENABLE_CAMERA` | `0` | Privacy gate for `drone_camera` and the console's camera panel. Off means no request to the companion is ever made |
| `OPEN_DRONE_CAMERA_NAME` | unset | The ONE camera name (in devices-mcp) the assistant may see. Letters, digits, `_`, `-`, max 100. No default, deliberately |
| `OPEN_DRONE_CAMERA_URL` | unset | Companion base URL, plain `http` on loopback only. Default: the `devices-mcp` port from the fleet registry, else none |
| `FLEET_REGISTRY_PATH` | `D:/Dev/repos/mcp-central-docs/operations/fleet-registry.json` | Where peers' ports are looked up (Apps page, camera default). Missing is fine |
| `OPEN_DRONE_AUDIT_LOG` | `~/.open-drone-mcp/audit.jsonl` | Append-only JSONL audit log path |
| `OPEN_DRONE_PORT` | `11222` | Backend port (REST + `/mcp`). Fleet-claimed; see `operations/WEBAPP_PORTS.md` |
| `OPEN_DRONE_WEBAPP_PORT` | `11221` | Console port; used for the CORS/Origin allow-list |
| `OPEN_DRONE_HOST` | `127.0.0.1` | Bind address. Keep loopback unless you know why not |
| `MCP_PORT` | unset | Fleet convention: if set, the server starts in HTTP mode on this port instead of stdio |
| `OPEN_DRONE_ALLOWED_HOSTS` | unset | Extra comma-separated Host names the API will serve (default: loopback + Tauri) |
| `OPEN_DRONE_ALLOWED_ORIGINS` | unset | Extra comma-separated browser origins allowed to POST |
| `OPEN_DRONE_DATA_DIR` | `~/.open-drone-mcp` | LLM keystore (`llm_keys.json`, 0600) and `llm_settings.json` |
| `VITE_PORT` / `VITE_API_TARGET` | 11221 / `http://127.0.0.1:11222` | Console dev server port and API proxy target (set by the fleet launcher) |
| `SCREENSHOTS` | unset | Set to `1` to let `e2e/screenshots.spec.ts` regenerate the README screenshots |

Gates are read once at start-up. Change them in the client config and restart the server.

## Runtime limits (not env vars)

Defaults, changed live with `drone_safety(operation="set_limits")`:

| Limit | Default | Hard ceiling (cannot be exceeded) |
|-------|---------|-----------------------------------|
| Geofence x, y | -1.0 to +1.0 m | -3.0 to +3.0 m |
| Geofence z | 0.0 to 1.5 m | 0.0 to 2.5 m |
| Max speed | 0.5 m/s | 1.0 m/s |
| Takeoff battery minimum | 3.7 V | (policy only) |
| In-flight battery minimum | 3.3 V | (policy only) |

Tightening is immediate. Loosening needs `confirm=true`. Limits reset to defaults on restart. Hard
ceilings live in `src/open_drone_mcp/safety.py` (`HARD_LIMITS`, `HARD_MAX_SPEED_MPS`); changing them is
a code change with tests.

## Setting variables

In `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "open-drone": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\open-drone-mcp", "run", "open-drone-mcp"],
      "env": {
        "OPEN_DRONE_BACKEND": "crazyflie",
        "OPEN_DRONE_URI": "radio://0/80/2M/E7E7E7E7E7",
        "OPEN_DRONE_ENABLE_ACTUATION": "0",
        "OPEN_DRONE_ALLOW_REAL_VEHICLE": "0"
      }
    }
  }
}
```

For local development copy `.env.example` to `.env` (never commit it).
