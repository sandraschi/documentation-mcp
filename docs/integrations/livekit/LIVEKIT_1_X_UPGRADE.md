# LiveKit Agents 1.x Upgrade Guide

**Last Updated:** 2026-09-06 (agents v1.8.0, server v1.13.6)
**Fleet status:** `teleconference-mcp` runs agents >= 1.8.0, server 1.13.6 (`LiveKitSFU`).

This document outlines the major changes in the **LiveKit Agents 1.0 (Python SDK)** release and how to leverage the new features in our architecture.

## 1. Core Architecture Changes

### Unified Agent Interface
The specialized `VoicePipelineAgent` and `MultimodalAgent` classes from 0.x are now merged into a unified `Agent` (and `AgentSession`) system. This allows for a more flexible orchestrator that handles speech-to-speech, pipelined, and multimodal models under one interface.

### Worker -> AgentServer
The `Worker` class has been renamed to `AgentServer`. While `WorkerOptions` remains for backward compatibility in some CLI wrappers, the underlying architecture has moved to a more robust "server" model.

### LLM Streaming Interface
The 0.x `__aiter__` pattern for custom LLMs is deprecated. 1.x uses `LLMStream._run()` as a coroutine that pushes chunks to an internal channel.

## 2. New Features & Patterns

### Simplified Tool Definition
No more `llm.FunctionContext` boilerplate. Use the `@llm.function_tool` decorator directly on your logic methods.

```python
@assistant.function_tool
async def control_iot_device(state: bool):
    """Control local smart home devices."""
    # Logic here
    return f"Device set to {state}"
```

### Enhanced Chat Context Management
Context management is now more robust. Use `agent.update_chat_ctx()` instead of manually modifying list indices.

### Native Text Input Handling
Agents 1.x automatically receives text input from the `lk.chat` topic, enabling seamless hybrid (voice + text) interaction without additional `ChatManager` configuration.

## 3. Why We Need These Features

### "Local Mode" Efficiency
The unified interface simplifies our "Local Mode" (Ollama/Whisper/Piper) significantly, as the same orchestration logic can handle different plugin substrates without switching agent classes.

### Industrial Precision
The move to `LLMStream._run()` allows for better error handling and "Reductionist" logging during the generation phase, reducing "Ontological Drift" in the SOTA pipeline.

### Lower Latency
1.x features optimized turn detection and improved VAD integration, critical for the high-intensity interactions required by AG-Visio.

---

**Status:** Maintained (covers through agents 1.8.0 / server 1.13.6)
**Integration:** `agent.py` and `LIVEKIT_INTEGRATION_GUIDE.md` follow these patterns.

---

## 4. Agents 1.5 -> 1.8: What Changed (fleet-relevant)

| Release | Change | Fleet impact |
|---------|--------|--------------|
| 1.5.8 | Barge-in cooldown window | Smoother interruptions in Visio; keep default |
| 1.5.9 | Answering Machine Detection | Available for SIP/telephone call flows; not wired yet |
| 1.5.10 | Model swaps via `update_options` | Swap STT/LLM/TTS mid-call; candidate, not wired yet |
| 1.5.12 | `UserTurnLimitOptions` | Wired: caps user speech at 60 s (`agent.py`) |
| 1.6.x | `RUF006` fails CI on dangling `asyncio.create_task` | Kept two `# noqa: RUF006` in `agent.py` (fire-and-forget by design) |
| 1.7.0 | Expressive mode (`AgentSession(expressive=True)` + inference TTS), PII redaction (`lk.pii.*` trace keys), full OTel GenAI conventions | Expressive OFF (needs inference TTS; fleet runs local Piper). Transcripts kept at DEBUG for Loki |
| 1.7.1/1.8.0 | Adaptive interruption without word timestamps, preemptive generation cancel, `transcription_delay ~0` fix, RoomIO mic-track replacement, `reasoning_tokens` in LLM metrics | Direct Visio barge-in/latency win; no code change required |

`cli.run_app(WorkerOptions(entrypoint_fnc, job_restart_policy=ALWAYS))` survives to 1.8.0 unchanged.

## 5. Server 1.10 -> 1.13: What Changed (fleet-relevant)

| Release | Change | Fleet impact |
|---------|--------|--------------|
| 1.10 | Log key `pID` -> `participantID`; agent auto-restart support | Updated Loki/Grafana filters; `AutoRestartPolicy.ALWAYS` wired |
| 1.11 | Data tracks on by default | Transcripts/intel broadcasts can move to ordered data tracks |
| 1.12 | Room auto-create via `roomCreate` grant; TURN `ttl_seconds` (default 300) + CIDR allow/deny | `roomCreate:true` wired in `/api/token`; TURN still disabled in `livekit.yaml` |
| 1.13.1 | **Removed no-TTL TURN compat**; CLI moved to `urfave/cli` v3.10 | Old TURN creds stop working — rotate `turn.secret` when enabling |
| 1.13.2 | Egress v2 API; `ParticipantInfo.capabilities`; join-latency + `rtc_success` metrics; async participant attributes (data blob) | Real `createRoomCompositeEgress` wired in `/api/egress` |
| 1.13.6 | Per-participant TURN quota (12), WS read-size + API body-size limits, H.264 baseline `42001f` removed, Safari relay-ICE fix | No config change needed; Safari guests benefit automatically |

Docker pin: `livekit/livekit-server:v1.13.6` (never `:latest`). Windows service binary at
`C:\Users\sandr\AppData\Local\Programs\LiveKit\livekit-server.exe` (NSSM `LiveKitSFU`).
