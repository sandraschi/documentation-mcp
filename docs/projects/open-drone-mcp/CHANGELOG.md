# Changelog

## 0.1.0 - unreleased

Phase 1 scaffold.

### Changed

- Licence is MIT (initially scaffolded as GPL-3.0-or-later because of the optional `cflib` dependency).
  `cflib` stays an optional, unbundled extra. See docs/WRAPPEE.md for the redistribution caveat.

### Added

- Safety engine: geofence box, speed cap, battery floors, tiers, confirm-to-loosen, hard ceilings.
- Actuation gates: real-vehicle motion needs `OPEN_DRONE_ENABLE_ACTUATION` and
  `OPEN_DRONE_ALLOW_REAL_VEHICLE`; `land`, `hover` and `emergency_stop` are never gated.
- Append-only JSONL audit log; motion fails closed when the log is unwritable.
- Declared dry-run simulator backend.
- Crazyflie backend on `cflib` (high-level commander). **Not yet flown on hardware.**
- MAVLink backend (`OPEN_DRONE_BACKEND=mavlink`, extra `mavlink`, pymavlink): ArduPilot Copter in GUIDED. Real
  COMMAND_ACKs, no force-arm, refuses to command a vehicle that is not in GUIDED, never writes a parameter, GCS
  heartbeats at 1 Hz, positions re-based to the takeoff spot, simulator proved (loopback plus a `SIM_` parameter),
  never assumed. PX4 is refused by name. Tested against a declared fake autopilot AND real ArduPilot 4.5.7 SITL (opt-in
  tests, `docker/ardupilot-sitl`). **Never flown.** `OPEN_DRONE_BATTERY_CELLS` is required.
- Camera-drone hardware decision (Holybro X500 v2, Pixhawk 6C): sub-README `docs/hardware/HOLYBRO_X500_V2.md`
  (vendor spec, shopping list, mass budget, usage analysis against the current safety envelope, first-flight
  protocol, risks) and a matching section in the console Help page (Wrappee tab, FAQ, Troubleshooting).
- Room camera (`drone_camera`, seventh tool): one JPEG from ONE operator-named camera served by the `devices-mcp`
  companion, delivered as real MCP image content. Default deny (`OPEN_DRONE_ENABLE_CAMERA`), no camera argument
  (the model cannot choose or list cameras), loopback-only URL, redirects not followed, JPEG magic + 2 MB cap,
  1 frame/s, audited without pixels, REST snapshot refuses cross-site fetches. Flight page gets a live still panel.
  Tested against a declared fake companion that also serves a "kitchen" camera and fails if it is ever requested.
- Portmanteau tools: `drone_system`, `drone_flight`, `drone_telemetry`, `drone_safety`, `drone_camera`,
  `drone_help`, `drone_shutdown` (seven). Resources, a prompt, and a skill.
- stdio transport (default) and streamable HTTP (`--http`, port supplied by the operator).

- Web layer (FastAPI, port 11222): REST for every tool through `mcp.call_tool`, the MCP endpoint at `/mcp`,
  Host allow-list (DNS rebinding), Origin and Sec-Fetch-Site check on unsafe methods (CSRF), no wildcard CORS,
  server-side Confirm for takeoff/go_to/move on the tools-harness route.
- Web console (React/Vite, port 11221): Dashboard (red onboarding cue, declared MOCK samples that clear only
  for a connected real vehicle), Flight (fence map), Safety (limits, gates, searchable audit log), Inbox, Tools,
  Skills, Chat, Logs (Ctrl+L), Settings, Onboarding, Help (5 tabs). STOP button on every page (Ctrl+Shift+E).
- LLM provider registry, write-only keystore and chat proxy (fleet-canonical module from arxiv-mcp).
- MCPB bundle (simulator only, `cflib` never bundled): manifest, 110 schema-validated examples, prompts of
  3368 / 4140 words, fleet pack script with import-isolation, AST, pollution and launch checks.
- Fleet start layer on claimed ports 11221/11222; `MCP_PORT` selects HTTP (fleet convention).

- Apps page (EXPERIMENTAL, labelled as such): direct fleet companions and whether they answer; degrades to
  "unknown" without a fleet registry and never requires a peer. API Docs page (Swagger UI / ReDoc iframe with a
  quick-reference strip built from the live OpenAPI document).

### Fixed (found by the tests while building)

- Console: the Safety form was overwritten by the server policy if the policy arrived after the operator had
  started typing; edits are now never clobbered (deterministic regression test, verified to fail on the old code).
- Console: Help search text leaked across tabs and left Troubleshooting empty.
- Dev proxy: the plain `/api` prefix also captured the SPA route `/api-docs`; now a regex key.
- Log ring entries now use the `timestamp` / `source` / `level` names the Logs page reads.
- Tools harness: annotations serialised by alias (camelCase MCP wire format).
- Apps probe: an HTML `200` (a dev server's SPA fallback, e.g. devices-mcp `/health`) counted as a running peer; JSON is now required.
- E2E suite moved to test-only ports so it can never collide with, or reach a real-vehicle backend on, the claimed pair.

### Not included (deliberately, tracked in the project plan)

- MAVLink (ArduPilot/PX4) backend: phase 4. Not advertised, not stubbed.
- Tauri/NSIS desktop installer.
- Companion mode (compact/pop-out layout); the standard targets creative-app wrappers.
- On-drone camera (AI deck) support and video.
- Webhooks: the product has no inbound events.

### Verification

115 pytest tests and 22 Playwright end-to-end tests pass; ruff, pyright, biome and tsc are clean. The stdio
and HTTP servers were exercised end to end with real MCP clients, and the `.mcpb` was packed, checked and
started from a clean unpacked copy. The Crazyflie backend is tested against a declared fake of `cflib`, which
proves call shapes only. Nothing has been flown on hardware or installed in Claude Desktop.
