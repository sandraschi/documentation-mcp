# Troubleshooting

## Server does not appear in Claude Desktop

**Cause**: Config JSON is malformed or the path is wrong.
**Fix**: Validate the JSON (no trailing commas), check the `--directory` path, restart Claude Desktop.

## "command not found: uv"

**Cause**: uv is not installed or not on PATH.
**Fix**: `winget install astral-sh.uv`, then restart the terminal.

## takeoff returns error_type "safety": "Actuation is disabled"

**Cause**: The backend is real and `OPEN_DRONE_ENABLE_ACTUATION` is not set.
**Fix**: Intended default. After the bench test, set it to `1` in the client config `env` and restart.

## takeoff returns "real-vehicle flight is not allowed"

**Cause**: Second gate closed.
**Fix**: Set `OPEN_DRONE_ALLOW_REAL_VEHICLE=1` and restart.

## "outside the geofence"

**Cause**: The target, or the takeoff height, is outside the current box.
**Fix**: Pick an in-fence target. Widening the fence needs `drone_safety(set_limits, confirm=true)` and a human operator's consent. Hard ceilings cannot be widened.

## "This change loosens a safety limit and needs confirm=True"

**Cause**: Working as designed.
**Fix**: Only the human operator should re-issue the call with `confirm=true`.

## "Battery ... is below the takeoff minimum"

**Cause**: Voltage under 3.7 V (or the reading is missing, which is treated as 0 V).
**Fix**: Charge the battery. The thresholds are conservative placeholders; adjust in code after calibrating on your pack.

## "Audit log is not writable; refusing to move"

**Cause**: Motion fails closed when the audit log cannot be written.
**Fix**: Check `OPEN_DRONE_AUDIT_LOG` and permissions on `~/.open-drone-mcp/`.

## "No radio URI"

**Cause**: `connect` on the crazyflie backend without `uri` or `OPEN_DRONE_URI`.
**Fix**: Pass `uri="radio://0/80/2M/E7E7E7E7E7"` (use your drone's channel/address) or set the env var.

## "Could not open Crazyflie link"

**Cause**: Crazyradio not plugged in, driver not installed, drone off, or wrong URI.
**Fix**: On Windows install the Crazyradio driver with Zadig/WinUSB per the Bitcraze docs. Power the drone. Confirm the URI.

## "Connected but no telemetry arrived"

**Cause**: The link opened but the log stream did not start within 3 s.
**Fix**: Reset the drone, move closer, check radio interference on the channel, retry.

## cflib fails to install on Windows

**Cause**: Python 3.13 without the Visual Studio C++ workload (Bitcraze install doc).
**Fix**: Use Python 3.12. This repo's `.python-version` selects it via uv.

## "Not flying" on go_to or move

**Cause**: Nothing has taken off yet.
**Fix**: `drone_flight(operation="takeoff")` first.

## Web console: POST fails with 403 "Origin not allowed"

**Cause**: The request carried a browser Origin that is not the console. This is the CSRF guard that stops another
website from sending flight commands to localhost.
**Fix**: Open the console at `http://127.0.0.1:11221` or `http://localhost:11221`. For another origin set
`OPEN_DRONE_ALLOWED_ORIGINS` and restart.

## Web console: 400 "Invalid host header"

**Cause**: The Host header was not loopback (DNS-rebinding guard).
**Fix**: Browse via `127.0.0.1` or `localhost`, or add the name to `OPEN_DRONE_ALLOWED_HOSTS` and restart.

## Port 11222 stays busy after stopping the server

**Cause**: `uv run` starts Python as a child of the uv wrapper on Windows, so killing the wrapper leaves the server.
**Fix**: Stop the `python.exe` that owns the port. For scripted runs launch `.venv\Scripts\python.exe -m open_drone_mcp --http`.

## drone_camera: "The room camera is disabled"

**Cause**: Working as designed. The camera is a privacy gate and is off by default.
**Fix**: Set `OPEN_DRONE_ENABLE_CAMERA=1` and `OPEN_DRONE_CAMERA_NAME`, restart. Read the privacy note first.

## drone_camera: "No room camera is configured"

**Cause**: The gate is on but no camera name is set. There is deliberately no default and no way for the assistant to pick one.
**Fix**: Set `OPEN_DRONE_CAMERA_NAME` to the camera's name in devices-mcp (letters, digits, `_`, `-`), restart.

## drone_camera: "The devices-mcp companion was not detected"

**Cause**: Nothing answered at the companion URL. The port comes from `OPEN_DRONE_CAMERA_URL`, else from the fleet
registry; with neither, none is known.
**Fix**: Start devices-mcp (https://github.com/sandraschi/devices-mcp) or set `OPEN_DRONE_CAMERA_URL=http://127.0.0.1:<port>`.

## drone_camera: "OPEN_DRONE_CAMERA_URL must be plain http on a loopback host"

**Cause**: SSRF guard. Only `http://127.0.0.1`, `localhost` or `[::1]` are accepted; credentials and other hosts are refused.
**Fix**: Run the companion on this machine, or tunnel it to a loopback port.

## drone_camera: "The companion does not know a camera named ..."

**Cause**: The configured name is not a camera in devices-mcp.
**Fix**: Compare `OPEN_DRONE_CAMERA_NAME` with the camera names in devices-mcp; names are case-sensitive.

## drone_camera: "At most one snapshot per 1 s"

**Cause**: Rate limit. The Flight page's live panel refreshes every 2 s, so an assistant asking at the same moment can collide.
**Fix**: Wait a second and retry.

## Chat page says "Choose a local LLM first"

**Cause**: No model is selected. The app never auto-picks one (a large model once loaded itself silently).
**Fix**: Settings, pick a provider and a model, save.

## Chat page takes several seconds to appear

**Cause**: The gate probes Ollama, LM Studio and vLLM first; Windows needs about 2.5 s to refuse a closed port.
**Fix**: Nothing to fix; it is a one-off delay per page load.

## `just mcpb-pack` fails at "bunx not found"

**Cause**: Bun is not installed.
**Fix**: `winget install Oven-sh.Bun`, then reopen the terminal.

## Server output corrupts the MCP connection

**Cause**: Something printed to stdout on the stdio transport.
**Fix**: Log to stderr only. Never `print()` in `src/`.
