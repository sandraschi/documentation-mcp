# God's Eye View — Voice Agent + MCP Server

Source: `src/voice/*`, `src/tools/*`, `server/mcp/*`, `docs/TOOLS.md`, `docs/MCP_SETUP.md`, `docs/VOICE-OWNERSHIP.md`, `.env.example` at HEAD `8b8ccc9`.

## 1. Voice (OpenAI Realtime over WebRTC)

- **Trigger:** GEV MIC → mic grant → talk. Auth: `OPENAI_API_KEY` (default) or opt-in local ChatGPT/Codex OAuth sign-in (experimental; mints short-lived Realtime credential server-side; `CODEX_HOME`/`CODEX_AUTH_JSON` must line up; Windows npm-Codex login button may fail → run `codex login` manually).
- **Models (env-overridable):** `OPENAI_REALTIME_MODEL=gpt-realtime-2`, `MINI=gpt-realtime-2.1-mini`, voice `marin`, reasoning `low`, HUD summary `gpt-5-nano`, transcribe `gpt-4o-mini-transcribe`. Context window deliberately short: `OPENAI_REALTIME_CONTEXT_TOKENS=3000`, retention `0.5`.
- **Grounding:** agent pulls live scene context (coords, street, layers, scale) before answering; street-level reads viewport screenshot, instructed never to hallucinate labels; entity Q&A uses clicked object's live telemetry.
- **Honesty rule:** only confirms actions that succeeded.
- **Key hygiene:** browser gets short-lived session token only. OAuth path refused for non-loopback clients.
- **Spend guards:** live spend readout, STD/MINI toggle, **$2 warning, $5 hard cap** (API-key path). OAuth usage tracked without dollar estimate/cap. Transcription billed separately + counted.
- **Debug:** `.gev-logs/realtime-conversations.jsonl` (rotated 32 MB, never expired) omits transcripts/tool args by default; `GEV_VOICE_LOG_CONTENT=1` to keep while debugging, then delete. Voice-auth check: `node scripts/qa-voice-auth.mjs <url> oauth|api-key microphone.wav` (3 s leading silence + short reply).

### Tool surface (30 tools, 4 jobs)

Defined once in `src/tools/` (`defineTool` + `composeCatalog`), exposed via two adapters: MCP (JSON-RPC) and function-calling (voice). `TOOL_SURFACES` in `src/tools/surfaces.js` toggles per surface.

- **Direct (camera verbs):** take me to X, orbit slowly, draw walking route A→B, fly the route, globe view, tilt 35°, north-up, reset.
- **Annotate (whiteboard):** outline Texas (real boundary, not circle), annotate Capitol grounds, distance LAX→DFW (arrow + spoken km), clear map. Manual DRAW mode: Area/Line/Pin, click vertices, double-click finish, label.
- **Interrogate (analyst):** count/filter/rank flights/ships/fires/quakes/satellites/datacenters/dams in view/Texas/above FL400; biggest fire near LA; ships headed to Oakland; ISS next pass (rise/peak/set + visibility).
- **Operate (console):** sensor 1–7, HUD (H), detection (D) + density %, cockpit (C), layers on/off, viewsheds, radio station near X, track plane, next contact (helicopters-only filter mid-cockpit), global infrastructure stage, play Orbital Watch scene, sharpen image, tactical layout, what's on.
- Biggest file: `src/voice/gevActions.js` (166 KB) + test 153 KB; turn engine `realtimeTurns.js` (40 KB).

## 2. MCP server (Claude / Codex in-conversation globe)

- **Server:** `server/mcp/stdio.js` → `node server/mcp/stdio.js --api-base http://localhost:4173`. Reads from a RUNNING app (`npm run dev`). Logs every call + failure reason to stderr (`mcp-server-gods-eye-view.log` in Claude Desktop logs).
- **Panel:** `npm run build:panel` builds the in-conversation globe; rerun after app changes.
- **Clients:**
  - Claude Code: `claude mcp add gods-eye-view -- node /abs/path/server/mcp/stdio.js --api-base http://localhost:4173`
  - Codex CLI: `codex mcp add gods-eye-view -- ...` (same); Desktop uses `~/.codex/config.toml` `[mcp_servers.gods-eye-view]` or Settings → MCP servers → Add (STDIO). WSL checkout → `wsl.exe -e <linux-node> <linux-stdio.js> --api-base ...`.
  - Claude Desktop: Settings → Developer → Edit Config JSON `mcpServers.gods-eye-view`.
- **Try:** restart client fully, new chat, *"Show San Diego in God's Eye View with military flights on."* Desktop shows live globe (10–20 s first load); CLI answers data + link.
- **Surfaces split:** MCP omits place search, routing, plain weather/wind, regional brief, HUD caption, radio, bikeshare, transit (assistants cover them or they add little without globe). Voice gets the full catalog.
- **Composition:** `composeCatalog({tools, services, replace, interceptors})` — services-gated inclusion, `(call, next)` interceptors, composite tools calling through catalog (sees `parent`). Portable exports (`gods-eye-view/tools`, `/tools/mcp`) enforced by `check-package-boundaries`.
