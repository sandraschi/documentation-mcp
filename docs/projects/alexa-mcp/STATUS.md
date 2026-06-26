# Alexa MCP -- Project Status

**Last Updated**: 2026-04-21  
**Repo**: `D:\Dev\repos\alexa-mcp` | [GitHub](https://github.com/sandraschi/alexa-mcp)  
**Version**: **0.3.x** (see `pyproject.toml` in repo) | **Changelog**: [alexa-mcp/CHANGELOG.md](file:///D:/Dev/repos/alexa-mcp/CHANGELOG.md)  
**Python**: 3.12+ | **Build**: `uv` + **hatchling**  
**Status**: Active — **Industrial** web bridge + **acoustic** MCP tools

---

## What It Is

An acoustic bridge for controlling physical Alexa/Echo devices from AI agents: **TTS out** and **STT in** on the same machine that sits in earshot of the device.

**Workflow**: Agent → TTS (edge-tts, miniaudio, sounddevice) → Speaker → **Alexa** → room audio → Microphone → STT (faster-whisper) → Agent.

---

## Notable capabilities (0.3+)

| Area | Notes |
|------|--------|
| TTS / playback | Selectable output device; in-app volume; `~/.alexa-mcp/playback.json` on server |
| Web UI | `web_sota`: Status, Audio, Logs, Help, AI Command; optional listen after speak |
| Security | TTS **shopping guard** (heuristic); full narrative in repo README and Help page |
| Docs | Alexa+ ecosystem (press pointers), Austria testing limits, Bostrom-adjacent “don’t paperclip the shopping cart” cautions in prose upstream |

---

## Port allocation (fleet)

| Service | Port | Notes |
|---------|------|--------|
| Web dashboard (Vite) | 10800 | See `web_sota/start.ps1` / `just dev` |
| API / bridge | 10801 | Uvicorn alongside dashboard |

(Older notes in this file that referenced 10705 are **stale**; use [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md).)

---

## Central docs in this tree

- [README.md](./README.md) — fleet-facing summary and links.  
- [CHANGELOG.md](./CHANGELOG.md) — mirror; canonical changelog in the main repo.  
- [llms.txt](./llms.txt) — short index for LLM context.
