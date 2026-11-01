# open-drone-mcp - Status

**Phase**: repo built through the web console and a simulator-only MCPB. **Never flown on real hardware.**
**Last updated**: 2026-09-29
**Source repo**: `D:\Dev\repos\open-drone-mcp`, pushed 2026-09-29 to https://github.com/sandraschi/open-drone-mcp (**private**)
**Ports**: backend **11222**, frontend **11221** (claimed and registered 2026-09-29)
**Licence**: MIT (`cflib`, optional and never bundled, is GPL v2 or later; see PLAN decision 1)
**Hardware**: none purchased (tiers in PLAN.md section 5)

## What exists

| Item | State |
|------|-------|
| Safety engine, audit log, dry-run + Crazyflie backends | Done. 151 pytest tests, ruff + pyright clean. Crazyflie backend tested against a declared fake of cflib only |
| MCP server (7 portmanteau tools, incl. drone_camera) | Done. stdio and HTTP exercised with real MCP clients |
| Web layer (FastAPI) | Done. Host allow-list, Origin/Sec-Fetch-Site guard, no wildcard CORS, server-side Confirm |
| Web console (React/Vite) | Done. Dashboard (red cue, declared MOCK), Flight, Safety, Inbox, Tools, Skills, Apps (experimental), Chat, API Docs, Logs, Settings, Onboarding, Help; STOP on every page. 28 Playwright tests, biome + tsc clean |
| MAVLink backend | Built, 179 pytest tests total. ArduPilot Copter only, PX4 refused. Fake autopilot speaks real MAVLink over UDP. Passes real ArduPilot 4.5.7 SITL (official binary in docker/ardupilot-sitl; takeoff, go_to, hover, land, RTL override refused, force-disarm; opt-in tests). **Never flown** |
| Room camera (stage 1) | Done, off by default. `drone_camera` via devices-mcp: one operator-named camera, loopback-only, JPEG-validated, 1 frame/s, no pixels in audit. Console panel + Safety gate row. Verified with a real stdio client against a fake companion; never against real home cameras. Frames go to the LLM provider |
| Fleet start layer | `start.bat` -> fleet engine verified end to end (backend, Vite, proxy, UI, 6 tools) |
| MCPB | Simulator-only bundle packs and starts from a clean unpacked copy (74.6 kB, 24 files). Prompts 3368 / 4140 words, 110 schema-validated examples. **Unsigned, not installed in Claude Desktop** |
| Fleet registration | `fleet-registry.json` entry, `FLEET_INDEX.md` row, `projects/open-drone-mcp/` synced, `starts/open-drone-start.bat` |
| Docs | README with screenshots, INSTALL, ONBOARDING, WRAPPEE, ARCHITECTURE, CONFIGURATION, TOOLS, DEVELOPMENT, TROUBLESHOOTING, CHANGELOG, AGENTS, CLAUDE, llms.txt |

## Assfix-zero: NOT claimed

Known gaps against `NEW_REPO_BUILD_COMPLETE.md`:

- **No Tauri/NSIS desktop installer** (`native/`). Also undecided: an installer with the Crazyflie backend would bundle GPL `cflib`.
- `assfix` and `fakefind` have not been run. I checked mock/fake/planned mentions by hand (only the declared ones remain).
- The Chat page comes from the fleet template and the LLM module is a canonical copy; I did **not** read `chat_skills_prefab_standard.md`, so it is unaudited against it.
- Prefab cards: `drone_system` and `drone_telemetry` are registered with `app=True` and their renderers exist, but nothing verified they render in a host.
- Companion mode skipped (the standard targets creative-app wrappers).
- Standards not read: `BUN_STANDARDS` (I used npm plus a bun lockfile like the reference repo), `PACKAGING_STANDARDS` in full, `tauri_nsis_building`, `TAURI_PRODUCTION_PITFALLS`, `chat_skills_prefab_standard`, `RAG_OPERATIONS_STANDARD`, `GITHUB_ACTIONS_NO_PRIVATE_CI`, `TESTING_GUIDE` beyond the declared-doubles section.
- Repo is private; no release tag or GitHub release has been cut, and the `.mcpb` is not attached anywhere.
- Apps page is a labelled stub: it probes two direct peers and nothing calls their tools.

## Bugs the tests caught while building (all fixed)

Safety form overwritten by a late policy response (regression test verified to fail on the old code); Help search leaking across tabs; dev proxy prefix `/api` swallowing `/api-docs`; log entry field names; annotation serialisation.

## Next actions

1. **Decide**: build the Tauri/NSIS installer now? Needs a licence call (simulator-only vs bundling GPL cflib), a multi-GB Rust build, and an install/uninstall smoke test on your machine.
2. Decide whether to make the repo public (currently private) and whether to cut a release.
3. Order the T1b kit (about $433), then the bench test in Onboarding. Until then the Crazyflie path is unproven.
4. Install the `.mcpb` in Claude Desktop and confirm `${__dirname}` / `uv run --with` behave (unverified).
5. Run `assfix open-drone-mcp` for an independent assessment.
6. Phase 4: MAVLink backend, after reading DroneServer's `docs/reproduce.md` and safety code.

## Observations outside this project

- `fleet_lock.py --verify` reports one pre-existing collision: backend port 10764 claimed by both `autohotkey-test` and `autohotkey-tools`.
- `operations/MASTER_MCP_CONFIG.json` has someone else's uncommitted edit that changes a credential value. Not touched, not committed here.
- `operations/fleet.lock.json` was not regenerated after my `fleet-start.config.ps1` appeared, and other people's changes are uncommitted in it, so I left it.

## Changelog

- 2026-09-29: Pack created (research, plan, status).
- 2026-09-29: Decisions recorded; phase 1 scaffold; relicensed MIT; web layer, console, MCPB, registration, launcher verification.
- 2026-09-29: Camera stage 1 (room camera via devices-mcp) built and pushed.
- 2026-09-30: MAVLink backend (ArduPilot Copter, pymavlink) built and pushed; tested against a declared fake autopilot only, not SITL, not flown. PX4 refused. Onboard-camera hardware options in PLAN section 5.
- 2026-10-04: Backend verified against ArduPilot 4.5.7 SITL. Onboard-camera stage 2 designed (open-drone-mcp docs/ONBOARD_CAMERA.md), not built.
- 2026-10-04: Hardware decision: Holybro X500 v2 (Pixhawk 6C, $609). Sub-README and console Help section written; findings: HARD_LIMITS (6x6x2.5 m, 1 m/s) too small for outdoor use, no yaw operation, no heading in telemetry.
