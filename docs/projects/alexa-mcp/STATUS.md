# Alexa MCP -- Project Status

**Last Updated**: 2026-02-15
**Repo**: `D:\Dev\repos\alexa-mcp` | [GitHub](https://github.com/sandraschi/alexa-mcp)
**Version**: v1.0.0
**Python**: 3.10+ | **Build**: Setuptools
**Status**: 🟢 PRODUCTION READY

---

## What It Is

An acoustic bridge for controlling physical Alexa/Echo devices via AI agents. It bypasses API limitations by using a literal "audio loopback" (or speaker-to-mic air bridge).

**Workflow**: Agent -> TTS (edge-tts) -> Speaker -> Alexa (Physical) -> Response -> Microphone -> STT (faster-whisper) -> Agent.

---

## Architecture

Three high-impact tools:
1. `speak_command`: High-quality neural TTS (edge-tts) for issuing commands.
2. `listen_response`: High-performance local STT (faster-whisper) for capturing feedback.
3. `interact`: Atomic portmanteau for full command-response cycles.

---

## Current State

| Feature | Status | Notes |
|---------|--------|-------|
| TTS Engine | Working | Neural speech quality (edge-tts) |
| STT Engine | Working | High-accuracy local inference (Whisper) |
| Audio Bridge | Working | Clean IO via sounddevice |
| Interaction | Working | Unified conversational tool flow |

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| Backend | 10705 | Reserved (Bridge Server) |
