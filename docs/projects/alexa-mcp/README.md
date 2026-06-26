# Alexa MCP (fleet documentation)

**Canonical repository**: [alexa-mcp on GitHub](https://github.com/sandraschi/alexa-mcp) — `D:\Dev\repos\alexa-mcp`  
**Version** (see upstream `pyproject.toml`): **0.3.x**  
**Changelog (authoritative)**: [alexa-mcp/CHANGELOG.md](file:///D:/Dev/repos/alexa-mcp/CHANGELOG.md) in the main repo. This folder holds a **short mirror** in [CHANGELOG.md](./CHANGELOG.md).

## What it is

An **acoustic bridge**: agents send text, the host **speaks** it (neural TTS) so a physical **Alexa / Echo** hears it, then a **microphone** captures the reply and **Whisper** transcribes it. No official Alexa control API is required; the “API” is air and sound.

## Current stack (high level)

- **MCP**: FastMCP 3.2+ (`interact`, `speak_command`, `listen_for_response`, `docs_help`, prefab tools as configured).
- **TTS**: `edge-tts` → temp MP3 → **miniaudio** decode → **sounddevice** to a **selectable** output; volume persisted server-side.
- **STT**: `faster-whisper` (local).
- **Web**: `web_sota` dashboard (Vite React), API under FastAPI; default dev ports **10800** (frontend) / **10801** (backend) per fleet registry.
- **Safety**: optional **TTS shopping guard** blocks obvious **Amazon order / buy / cart** phrasing (env `ALEXA_SHOPPING_GUARD`, default on). See upstream README for limits.

## Quick links

| Doc | Location |
|-----|----------|
| Full README | [D:/Dev/repos/alexa-mcp/README.md](file:///D:/Dev/repos/alexa-mcp/README.md) |
| Changelog | [D:/Dev/repos/alexa-mcp/CHANGELOG.md](file:///D:/Dev/repos/alexa-mcp/CHANGELOG.md) |
| Project status (this tree) | [STATUS.md](./STATUS.md) |
| Web ports | [operations/WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) (alexa-mcp) |

## Run

```text
# From repo root, after uv sync
just dev
# or start web_sota via start.ps1; see upstream README.
```

## Notes for fleet index consumers

- **Not** a substitute for Amazon account **voice purchase** and **skill** settings; the bridge is an actuator for whatever Alexa would do if a human spoke the same words.
- **Web UI auth** is **not** production-hardened; do not expose to the public internet without a gate (VPN / reverse proxy with auth). Documented as roadmap upstream.
