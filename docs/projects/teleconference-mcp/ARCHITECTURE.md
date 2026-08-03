# Teleconference MCP — Architecture

**Last Updated:** 2026-02-07
**Source Repo:** `D:\Dev\repos\teleconference-mcp`

---

## Component Diagram

```
+------------------+     +------------------+     +------------------+
|   Web Client     |     |  LiveKit Server  |     |  Voice Agent     |
|  (Next.js/React) |---->|  (Docker)        |<----|  (Python)        |
|  livekit-client  |     |  Port 7880       |     |  livekit-agents  |
+------------------+     +------------------+     +------------------+
        |                         |                         |
        | Token API               | WebRTC                  | Worker
        v                         v                         v
+------------------+     +------------------+     +------------------+
|  Next.js API     |     |  Redis (optional)|     |  Ollama / Whisper|
|  /api/token      |     |  Room state      |     |  Piper TTS       |
|  /api/discovery  |     +------------------+     +------------------+
|  /api/health     |
+------------------+
```

---

## Data Flow

### Join Flow
1. User opens web app (e.g. http://localhost:10800).
2. User enters participant name and selects room (or custom room).
3. Client POSTs to `/api/token` with room name and participant name.
4. API signs JWT with LIVEKIT_API_KEY/SECRET; returns token.
5. Client connects to LiveKit server (NEXT_PUBLIC_LIVEKIT_URL) with token.
6. LiveKitRoom mounts; VideoConference and sidebar (transcription, chat) render.

### Media Flow
- Client publishes video/audio tracks (optionally preferred device IDs from settings).
- LiveKit server forwards tracks to other participants (SFU).
- Screen share: client publishes screen track; grid prioritizes screen tile.

### Agent Flow
1. Agent worker runs (`python agent.py dev`); subscribes to LiveKit dispatcher.
2. When a room is created or participant joins, worker enters room via entrypoint.
3. Agent (LiveKit 1.x Unified): receives audio → STT → text.
4. On `user_speech_committed`: ReductionistLogic.analyze_saliency(text); if "visio" in text or dilution >= 0.7, agent responds.
5. LLM (Ollama gemma2) generates reply; TTS (Piper) synthesizes; agent publishes audio to room.
6. Transcription can be sent via data channel or participant metadata for sidebar display.

### Data Flow
- Participants: `Room.LocalParticipant.publishData()` for custom messages.
- Agent: can receive `RoomEvent.DataReceived`; can send transcription events.
- Chat: LiveKit useChat hook for in-room chat messages.

---

## Agent Pipeline (Visio)

```
User Speech (mic) --> Silero VAD --> Whisper STT --> text
       |
       v
ReductionistLogic.analyze_saliency(text)
       |
       +-- "visio" in text OR dilution >= 0.7 --> trigger reply
       |
       v
Ollama (gemma2) LLM --> response text --> Piper TTS --> audio track --> room
```

- **VAD:** Silero – voice activity detection; only process when user is speaking.
- **STT:** Whisper – speech-to-text.
- **LLM:** Custom SOTAOllamaLLM wrapping Ollama AsyncClient; streams chunks; ChatContext with system prompt (ReductionistLogic.reductionist_prompt).
- **TTS:** Piper – text-to-speech.
- **Hooks:** `user_speech_committed` injects refutation mode or keeps agent silent based on saliency.

---

## Web App Architecture

- **State:** React state for join form, room, transcripts, chat; localStorage for settings (lib/settings.ts).
- **LiveKit context:** LiveKitRoom provides room context; useParticipants, useLocalParticipant, useTracks, useChat, useConnectionState.
- **API routes:** Server-side token generation (livekit-server-sdk AccessToken); discovery and health for dashboard.
- **Device handling:** Preferred devices from settings passed to LiveKitRoom videoCaptureDefaults/audioCaptureDefaults; pre-join validation via usePreJoinValidation.

---

## MCP Integration (Fast_MCP 3.1+)

- **Placement:** `packages/mcp-server`; consumed via stdio.
- **Core Pattern**: SOTA 2026 industrial standards.
- **Context Injection**: All tools accept `ctx: Context` for correlation.
- **Logging**: Mandatory `correlation_id` logging for traceability.
- **Saliency Tools**: `get_dev_stats`, `query_system_logs`, `sample_log_analysis` (Iterative Sampling).
- **Role:** Dev tooling only; not used by web app or agent at runtime.
- **Future:** LiveKit room list, agent status tools, and CalDAV integration in Phase 2.5.

---

## Security

- **Tokens:** Short-lived JWTs; API key/secret in env; never exposed to client except in signed token.
- **No persistent auth:** No user DB; participant identity is name supplied at join.
- **Self-hosted:** All media and data stay on your infrastructure (LiveKit server, Redis, optional recording).

---

## Scalability

- **LiveKit:** Single server for small/medium teams; scale with LiveKit Cloud or multiple SFU nodes for large deployments.
- **Agent:** One worker per deployment; can scale workers for many concurrent rooms.
- **Web:** Stateless; scale behind load balancer; token API is lightweight.

