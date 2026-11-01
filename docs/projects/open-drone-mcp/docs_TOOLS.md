# Tool Reference

All tools return `{"success": bool, "message": str, "data": ...}`. Failures also carry `error`,
`error_type` (`safety`, `backend`, `configuration`, `audit`, `internal`) and `suggestions`.
Every flight/telemetry response includes `simulated`.

## drone_system

Vehicle link and system status.

| Operation | Parameters | Description |
|-----------|------------|-------------|
| `status` | none | Version, backend, connected, both gate flags |
| `backend_info` | none | Active backend, available backends |
| `connect` | `uri` (optional) | Open the link. Uses `OPEN_DRONE_URI` if `uri` omitted. Dry-run needs no URI |
| `disconnect` | none | Close the link. Refused while flying |

Registered with `app=True` (MCP Apps surface). Plain-text `message` is always returned. Card
rendering in a host has not been verified.

## drone_flight

Motion. Checked against geofence, speed cap and battery floor.

| Operation | Parameters | Description |
|-----------|------------|-------------|
| `takeoff` | `height_m` (0-2.5, default 0.5), `speed_mps` | Refused if battery below takeoff minimum or height outside the fence |
| `go_to` | `x`, `y`, `z` (all required), `speed_mps` | Absolute position in the estimator frame; must be flying |
| `move` | `dx`, `dy`, `dz` (each within +-3 m), `speed_mps` | Relative to current position; must be flying |
| `land` | `speed_mps` | Never gated |
| `hover` | none | Hold current estimate. Never gated |
| `emergency_stop` | none | Cut motors immediately. Never gated |

`takeoff`, `go_to`, `move` on a real backend need both actuation gates. Speeds are clamped to the policy
maximum. A straight line between two in-fence points stays in-fence, so only endpoints are checked.

## drone_telemetry

Read-only. Bounded output.

| Operation | Description |
|-----------|-------------|
| `status` (default) | Position, battery, flying, backend, simulated |
| `position` | x, y, z in metres |
| `battery` | Voltage and `ready_for_takeoff` |

Registered with `app=True`, same caveat as `drone_system`.

## drone_safety

| Operation | Parameters | Description |
|-----------|------------|-------------|
| `get_policy` | none | Limits, gates, hard ceilings |
| `set_limits` | any of `x_min`, `x_max`, `y_min`, `y_max`, `z_min`, `z_max`, `max_speed_mps`; `confirm` | Tighten freely; loosen only with `confirm=true`; hard ceilings never move |
| `audit_tail` | `limit` (1-200, default 20) | Last entries of the audit log, oldest first. Bounded tail, no cursor |

## drone_camera

One JPEG from **one fixed room camera** brought in from the `devices-mcp` companion. It is a camera watching the
drone, not the drone's own view. The frame is returned as real MCP image content plus the usual text summary.

| Operation | Description |
|-----------|-------------|
| `status` | Enabled? Companion reachable? Does the configured camera exist? Never lists any other camera. No network call at all while the gate is off |
| `snapshot` | One frame. `data`: `camera`, `bytes`, `mime`, `captured_at`, `drone_position_m` (estimator metres, or null if not connected), `drone_simulated`, `note` |

Privacy and safety properties (each has a test):

- **Off by default.** Needs `OPEN_DRONE_ENABLE_CAMERA=1` and `OPEN_DRONE_CAMERA_NAME`. Disabled means `error_type: "safety"`.
- **No camera argument.** The model cannot choose, list or ask about another camera; `devices-mcp` may also serve a
  kitchen or doorbell camera, which this tool never requests, names or returns.
- **Loopback only.** `OPEN_DRONE_CAMERA_URL` must be plain `http://127.0.0.1|localhost|[::1]`; redirects are not followed.
- **Validated frames.** Must be `image/jpeg`, start with the JPEG magic bytes, and be at most 2 MB. At most one per second.
- **Audited without pixels.** The audit log records that a frame was taken from which camera, never the image.
- Every frame reaches the LLM provider your client uses. That is inherent to giving an assistant a picture.

Errors: `error_type: "camera"` (not configured, companion missing with its install link, unknown camera, rate
limited, bad image) or `"safety"` (gate closed).

## drone_help

`topic`: `overview`, `flight`, `safety`, `camera`, `troubleshooting`.

## drone_shutdown

Land if flying, disconnect, and with `terminate=true` exit the server process.

## REST API (web layer, port 11222)

The console and any script can use the same operations over HTTP. Flight routes call the MCP tools in-process,
so they get the same safety checks and audit trail. Only endpoints that exist are listed.

| Method and path | Purpose |
|-----------------|---------|
| `GET /api/health` | Liveness; `instance_configured` is true only for a connected REAL vehicle |
| `GET /api/dashboard` | Backend, link, telemetry, policy, audit count |
| `GET /api/telemetry?operation=` | `drone_telemetry` |
| `POST /api/system/connect?uri=`, `POST /api/system/disconnect`, `GET /api/system` | `drone_system` |
| `POST /api/flight` `{arguments}` | `drone_flight` |
| `POST /api/emergency-stop` | `drone_flight emergency_stop` |
| `GET /api/safety`, `POST /api/safety/limits` `{arguments}` | `drone_safety get_policy` / `set_limits` |
| `GET /api/audit?limit=`, `GET /api/inbox?limit=` | Audit tail; refusals and failures only |
| `GET /api/tools`, `GET /api/tools/{name}`, `POST /api/tools/{name}` `{arguments, confirm}` | Tools harness contract; motion needs `confirm: true` |
| `POST /api/tools/{name}/call` | Raw form, returns the dialogic dict directly |
| `GET /api/skills`, `GET /api/skills/{name}` | Skill list and `SKILL.md` |
| `GET /api/logs`, `POST /api/logs` | Log ring buffer |
| `GET /api/camera/status`, `GET /api/camera/snapshot` | Room camera state; one JPEG (`Cache-Control: no-store`). 403 while the gate is off or for `Sec-Fetch-Site: cross-site`, 409 when unconfigured, 429 when too fast, 502 for a companion problem |
| `GET /api/apps` | EXPERIMENTAL: direct fleet companions (`robotics-mcp`, `devices-mcp`) and whether they answer; `unknown` when no fleet registry is on the machine |
| `GET /docs`, `/redoc`, `/openapi.json` | Swagger UI, ReDoc, OpenAPI document (also shown on the console's API Docs page) |
| `/api/llm/*`, `/api/settings/llm*` | Provider registry, models, chat proxy (SSE), write-only keys |
| `/mcp` | MCP streamable HTTP endpoint |

Guards: loopback Host headers only; POST/DELETE with a foreign `Origin` or `Sec-Fetch-Site: cross-site` get 403.

## Resources and prompts

- `resource://drone/quickstart`, `resource://drone/safety`
- Prompt `drone_first_flight`
- Skill `open-drone` (from `skills/`)

## Webhooks

None. The product has no inbound events.
