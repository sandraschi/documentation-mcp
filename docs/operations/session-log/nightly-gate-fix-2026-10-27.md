# Nightly gate fix 2026-10-27 (evening session)

Nightly 2026-10-27 shard 6/7 failed with 6 failed steps. Fixed 5 with verified
root causes; 1 (install-matrix) is a weekly infra job that cannot green tonight.

## Fixed

1. **compose-ports** (verified: 0 collisions after fix)
   - `docker-mcp/docker-compose.yml`: `10784:8000` -> `11255:8000`
     (was notebooklm-fleet-mcp frontend), `10785:3000` -> `11256:3000`
     (was ai-games-collection edax per registry). 11255/11256 from
     `allocate.py --list-free` (free across registry+configs+compose+running).
   - `myai/docker-compose.yml`: stale `voice-ai-backend` service
     `10776:8000` -> `11257:8000` (was glance-mcp backend). The canonical
     voice_ai_suite stack already lives in
     `projects/voice_ai_suite/docker-compose.yml` on fleet-allocated
     11234/11233; top-level entry is a stale duplicate. Comment notes this.
   - Note: compose parser ends the `ports:` block on comment lines containing
     `:`, so the explanatory comment had to move above the service, not inside
     the ports block.

2. **sakana-mcp health-probe DOWN** (verified live: `/api/health` 200)
   - `fleet-start.config.ps1`: added `WorkDir = 'webapp\backend'` --
     `UvicornTarget app:app` resolves to `webapp\backend\app.py`, but without
     WorkDir the launcher ran it from the repo root (import failure).
   - `start.ps1`: was `uv run -m sakana_mcp` (stdio only, never starts the
     webapp the health probe expects). Now delegates to `webapp\start.ps1`
     like kyutai-mcp.

3. **vroidstudio-mcp smoke** (`backend_ok`, frontend never ready; same on 10-25)
   - `fleet-start.config.ps1`: `WebRoot 'web_sota'` -> `'webapp'`.
     `web_sota/` holds only launcher scripts (no package.json), so
     `npm run dev` always failed there. Real frontend is `webapp/`
     (vite hardcoded to 10880 + proxy to backend 10881, matching config).

4. **kyutai-mcp smoke TIMEOUT** (every shard covering it: 10-05/06/17/24/27)
   - Root cause: `webapp/backend/app.py` imports `kyutai_mcp.backends.*`
     (common, manager, pocket_tts, unmute) and `kyutai_mcp.moshi_discovery`,
     none of which existed (`backends/` was an empty dir, never in git).
     Backend crashed on import -> probe waited the full gate timeout.
   - Implemented for real (ruff clean, live-verified `/api/health`,
     `/api/backends/config`, `/api/backends/status`):
     `src/kyutai_mcp/backends/{__init__,common,manager,pocket_tts,unmute}.py`
     + `src/kyutai_mcp/moshi_discovery.py`. JSON-file-backed config,
     subprocess lifecycle for pocket-tts, live HTTP availability probes,
     Moshi binary discovery. Unconfigured backends report
     `available: false` honestly -- no fake-healthy stubs.

5. **freecad-mcp smoke TIMEOUT** (passed 10-20, environmental)
   - `scripts/ensure-bridge.ps1`: added portable-build search pattern
     `D:\Dev\repos\FreeCAD\*\FreeCAD.exe`. The only pattern covering the
     local checkout was `*\bin\FreeCAD.exe`, but the portable build keeps
     the exe at the version-dir root -- resolver returned null, bridge never
     started, backend never answered. Verified the new glob resolves to
     `FreeCAD_1.1.1-Windows-x86_64-py311\FreeCAD.exe`.

## Not fixed tonight

6. **heartbeat install-matrix**: weekly job (last 10-25, next 11-01), 46/46
   FAIL -- alternating "Sandbox never booted twice in a row (singleton
   wedge)" (Windows Sandbox host flakiness under parallel nightly load) and
   "Health check did not return 200 within 90s". Host-infra issue, needs a
   4.5h re-run plus sandbox reliability work; out of scope for this session.
   Heartbeat will stay red until the 11-01 run.

## Backups

Timestamped `.bak` files left next to every edited file (fleet Batch Mutation
rule); all are gitignored. Remove after the next green nightly verifies the
fixes: `sakana-mcp/*.{config,start}.ps1`, `docker-mcp/docker-compose.yml`,
`myai/docker-compose.yml`, `vroidstudio-mcp/fleet-start.config.ps1`,
`freecad-mcp/scripts/ensure-bridge.ps1`.
