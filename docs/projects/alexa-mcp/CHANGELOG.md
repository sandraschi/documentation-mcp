# Alexa MCP — MCP Central mirror

**Authoritative changelog**: the git repository at `D:\Dev\repos\alexa-mcp` — file **[CHANGELOG.md](file:///D:/Dev/repos/alexa-mcp/CHANGELOG.md)**.

## Summary of 0.3.0 (2026-04-21)

- **TTS shopping guard** (default on) for Amazon-shaped purchase phrasing; env `ALEXA_SHOPPING_GUARD=0` to disable.
- **Playback** API and persisted device + volume; Audio page and test chime / test “Hello”.
- **Web**: Status, Audio, Logs, Help, AI Command with listen-after-speak; in-memory process log.
- **Docs**: Alexa+ ecosystem, Austria rollout note, security (prompt injection, web auth roadmap) in upstream README and Help; `docs_help` tool expanded.
- **TTS path**: miniaudio + sounddevice; Windows-friendly temp file handling; no ffmpeg required for MP3 decode on that path.
- **Ruff** hygiene across `src` and tests.

For full entries, always read the **canonical** [CHANGELOG.md in alexa-mcp](file:///D:/Dev/repos/alexa-mcp/CHANGELOG.md).
