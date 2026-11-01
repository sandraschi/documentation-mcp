# Troubleshooting

## Slow `docker ps` / endlessly spinning webapp pages

Time `docker ps` natively first. If the CLI itself takes ~10s with an idle
host, find the stalling container: time one full inspect per container —
healthy ones answer in milliseconds, a wedged one takes seconds (case
2026-10-03: exactly 3.0s each on three containers). Then check its network
endpoints (`docker inspect <name>` → `NetworkSettings.Networks`): empty
endpoints with a network mode set = broken record. Every daemon list call
stalls on it, running or stopped, across daemon restarts. Fix: `docker rm` +
recreate via compose; stopping is NOT enough.

## Web dashboard: HTTP 500

1. Confirm the API bridge is running on **10807** (backend PowerShell window from `start.ps1`).
2. Check `customization.server` exports `app` (`from server import web_app as app`).
3. `curl http://127.0.0.1:10807/api/health` should return `healthy`.

## MCPB install fails

- Rebuild from repo root: `just mcpb-pack` or `npx @anthropic-ai/mcpb pack . dist/docker-mcp-v3.3.0.mcpb`.
- Use root `manifest.json` and `assets/prompts/` (there is no `mcpb/` subfolder).
- Ensure `fastmcp>=3.3` in your environment matches `manifest.json`.

## Sampling / agentic workflow unavailable

- Start **Ollama** (11434) or **LM Studio** (1234).
- Set `DOCKER_MCP_SAMPLING_BASE_URL` if not using default Ollama.
- Use a client that supports MCP sampling (Cursor, Claude Desktop).

## Tauri build

- Run `native/ensure-sidecar-stub.ps1` before `cargo check` if sidecar is missing.
- Full release: `just build-native` (requires Rust toolchain).
- Webapp for Tauri must be built with `VITE_API_BASE=http://127.0.0.1:10807`.

## Docker daemon errors

- Verify Docker Desktop is running: `docker ps` in a terminal.
- On Windows, socket default: `//./pipe/docker_engine`.
