# norirobotics-mcp — Status

**Version**: 0.1.0
**Status**: Core MCP server + REST API + webapp built and verified. Pre-hardware (Nori A3 ships Fall 2026).

## What's real and verified

- FastMCP 3.4 server wrapping `nori-sdk` (real PyPI package, v1.1.0, Apache-2.0) — verified to
  exist and install cleanly (`uv sync`).
- 6 tools (`nori_info`, `nori_session`, `nori_control`, `nori_recording`, `nori_help`,
  `nori_shutdown`), all mapped 1:1 onto real `nori_sdk.RemoteTeleop` / `nori_sdk.mock.MockRobot`
  methods — verified by introspecting the installed package, not guessed.
- 33 pytest cases, all passing against the real installed `nori_sdk` mock backend (no fakes of
  our own). Two real API-mismatch bugs (sync-vs-async methods; `RecordVerb` semantics) were
  caught during **live browser verification**, not just unit tests, and fixed with regression
  tests added.
- REST API (`/api/health`, `/api/hero`, `/api/session/*`, `/api/control/*`, `/api/recording/*`,
  `/api/logs`, `/api/llm/*`) + webapp (React/Vite/Tailwind/Zustand, 8 pages: Dashboard, Info,
  Session, Control, Recording, Settings, Help, Logging) — built, `tsc` clean, `biome check` clean,
  `npm run build` succeeds, and manually click-tested end to end in a real browser: connect
  (mock), e-stop, episode start/stop all confirmed working with real SDK responses.
- ruff check + ruff format clean on the Python side.
- Full docs stack (README, INSTALL, AGENTS, CLAUDE, docs/{ONBOARDING,ARCHITECTURE,CONFIGURATION,
  TOOLS,DEVELOPMENT,TROUBLESHOOTING,WRAPPEE}.md), .gitignore/.mcpbignore, start scripts, CI
  workflow, glama.json, llms.txt/llms-full.txt.
- Fleet registration: `FLEET_INDEX.md` row, `fleet-registry.json` entry, ports 11970/11971 in
  `WEBAPP_PORTS.md`.

## Deliberately deferred (not yet built)

- **MCPB packaging** (manifest + assets/prompts 3-4-100) — not yet built this pass.
- **Tauri/NSIS native installer** — not scaffolded; per fleet convention this is a separate
  downstream step (`nsis-build` skill) after the MCP server itself is stable, and building it
  now would mean maintaining a native config against a tool surface still likely to shift once
  real hardware exists.
- **Playwright e2e** — no automated browser test suite yet; verification this pass was manual
  (see above), not scripted.
- No real robot has ever been connected — cannot be, until Fall 2026 shipment. Every "real
  credentials" code path (`session_state.connect` when `NORI_MCP_SUPABASE_*` is set) is written
  against the SDK's documented API but has zero hardware-in-the-loop verification.

## Research

Full sourced research pass: [RESEARCH.md](RESEARCH.md) — specs, HN launch thread, XLeRobot/HF
LeRobot lineage, actuator-upgrade note (Feetech vs. CubeMars/MyActuator QDD).
