# open-drone-mcp - planning pack

**Status**: Repo built (safety engine, simulator, Crazyflie backend, web console, MCPB); not flown on hardware.
**Type**: MCP server + webapp (robotics lane), repo at `D:\Dev\repos\open-drone-mcp`.
**Idea**: FOSS drone control from an LLM. Crazyflie nano quads for living-room demos, MAVLink
(ArduPilot/PX4) for bigger DIY builds. Explicitly not DJI.

`README.md`, `CHANGELOG.md`, `INSTALL.md`, `docs_*.md`, `llms.txt` and `pyproject.toml` in this folder are
**synced copies from the repo** (PROJECT_PAGE_STANDARD). This file and the three below are the planning
pack, which only lives here.

## Docs

| File | What |
|------|------|
| [RESEARCH.md](./RESEARCH.md) | Platforms, existing MCP repos, Crazyflie deep dive, prices, Windows caveats, regulation, gaps |
| [PLAN.md](./PLAN.md) | Architecture, safety design, phases, decisions |
| [STATUS.md](./STATUS.md) | Where things stand and next actions |
| [README.md](./README.md) | Synced repo README (usage, screenshots) |

## One-paragraph summary

Four small MAVLink MCP servers already exist (DroneServer, MAVLinkMCP, mavlink-mcp,
ardupilot-mcp), all young (3-24 stars). No Crazyflie MCP was found in three searches, and
Crazyflie is the only sensible indoor platform. Proposal: build a Crazyflie backend first behind a
backend-independent safety engine (geofence box, caps, tiers, audit), then add a MAVLink backend
by studying the existing repos rather than reimplementing them. Decided 2026-09-29: standalone
repo, **MIT** (switched from GPL-3.0-or-later at the operator's request; `cflib` is an optional, never-bundled
extra), Python 3.12, camera in scope but staged (room camera first), hardware in tiers with Crazyflie 2.1+
kit (~$433) as the first buy.

## Related

- Fleet robotics: [robotics-mcp](../robotics-mcp/), [yahboom-mcp](../yahboom-mcp/), [norirobotics-mcp](../norirobotics-mcp/README.md)
- Standards gate: `standards/AGENTS.md` section 4.1 (New Repo Gate), `standards/FLEET_CROSSCONNECT_STANDARD.md`
- Existing external work: [DroneServer](https://github.com/PeterJBurke/droneserver),
  [betaflight-mcp](https://github.com/SebGalina/betaflight-mcp)
