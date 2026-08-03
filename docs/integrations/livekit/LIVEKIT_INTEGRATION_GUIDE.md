# LiveKit Integration Guide

**Last Updated:** 2026-04-06 (v2.0.0 Teams++)
**Status:** SOTA Compliance
**Reference Implementation:** myconf (Teams++) at `d:/Dev/repos/myconf`

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [LiveKit Server](#livekit-server)
4. [Web Client Integration](#web-client-integration)
5. [AI Voice Agents](#ai-voice-agents)
6. [MCP Integration](#mcp-integration)
7. [Configuration](#configuration)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Overview

### What is LiveKit?

LiveKit is an open-source **WebRTC SFU (Selective Forwarding Unit)** that provides:

- **Real-time video/audio** - Low-latency WebRTC streaming
- **Room-based sessions** - Multi-participant conferencing with named rooms
- **Token-based auth** - JWT tokens for secure room access
- **Data channels** - Real-time messaging alongside media
- **Agent framework** - Python SDK for voice AI participants

### Key Features

| Feature | Description |
|--------|-------------|
| **SFU Architecture** | Selective forwarding reduces bandwidth; each participant sends one stream |
| **Adaptive Bitrate** | Automatic quality adjustment based on network conditions |
| **Screen Sharing** | Native track publishing for screen capture |
| **Recording** | Egress services for cloud recording (optional) |
| **Agents** | Python/TypeScript SDK for bot participants (voice, transcription) |

### When to Use LiveKit

- **Video conferencing** - Standups, code reviews, team meetings
- **Voice AI** - Real-time voice agents with STT/LLM/TTS pipelines
- **Live streaming** - Low-latency broadcast with interactive participants
- **Self-hosted** - Full control over infrastructure and data

---

## Architecture

### Component Diagram

```
+------------------+     +------------------+     +------------------+
|   Web Client     |     |  LiveKit Server  |     |  Voice Agent     |
|  (Next.js/React) |---->|  (Docker)        |<----|  (Python)        |
|  livekit-client  |     |  Port 7880       |     |  livekit-agents  |
+------------------+     +------------------+     +------------------+
        |                         |                         |
        | Token API                | WebRTC                  | Worker
        v                         v                         v
+------------------+     +------------------+     +------------------+
|  Next.js API     |     |  Redis (optional)|     |  Ollama / Whisper|
|  /api/token      |     |  Room state      |     |  Piper TTS       |
+------------------+     +------------------+     +------------------+
```

### Data Flow

1. **Join flow**: Client requests token from API -> API signs JWT with LiveKit keys -> Client connects to server with token
2. **Media flow**: Client publishes video/audio tracks -> Server forwards to other participants
3. **Agent flow**: Agent worker subscribes to room -> Receives audio -> STT -> LLM -> TTS -> Publishes response
4. **Data flow**: Participants can send data messages via `Room.LocalParticipant.publishData()`; agent can receive via `RoomEvent.DataReceived`

---

## LiveKit Server

> **Fleet deployment (Goliath, 2026-08-03):** the fleet SFU runs as a **Windows service**
> (`LiveKitSFU`, NSSM, native `livekit-server` 1.7.0, config `myconf/livekit.yaml`, auto-start +
> crash-restart) — **not** Docker. Verify: `Get-Service LiveKitSFU`; logs:
> `D:\Dev\repos\myconf\logs\livekit.out.log`; reinstall (elevated):
> `D:\Dev\repos\teleoperator-mcp\scripts\install-livekit-service.ps1`.
> The Docker instructions below remain valid for non-Windows / dev machines.

### Docker Setup

```yaml
# docker-compose.yaml
services:
  livekit:
    image: livekit/livekit-server:latest
    command: --config /etc/livekit.yaml
    volumes:
      - ./livekit.yaml:/etc/livekit.yaml
    ports:
      - "7880:7880"   # HTTP/WebSocket
      - "7881:7881"   # WebRTC
      - "7882:7882/udp"  # TURN (if needed)
    restart: always
```

### Configuration (livekit.yaml)

```yaml
port: 7880
rtc:
  port_range_start: 50000
  port_range_end: 60000
  use_external_ip: false
keys:
  devkey: secret   # API key
  # In production: use env vars or secrets
logging:
  level: info
```

### Token Generation

Tokens are JWTs signed with the API key and secret. Include room name, participant identity, and optional metadata.

**Node.js (Next.js API route):**

```typescript
import { AccessToken } from "livekit-server-sdk";

export async function POST(req: Request) {
  const { roomName, participantName } = await req.json();
  const apiKey = process.env.LIVEKIT_API_KEY ?? "devkey";
  const apiSecret = process.env.LIVEKIT_API_SECRET ?? "secret";

  const token = new AccessToken(apiKey, apiSecret, {
    identity: participantName,
    name: participantName,
  });
  token.addGrant({
    roomJoin: true,
    room: roomName,
  });

  return Response.json({ token: await token.toJwt() });
}
```

**Python (FastAPI):**

```python
from livekit import api

token = api.AccessToken(api_key, api_secret)
token.with_identity(participant_name).with_name(participant_name)
token.with_grants(api.VideoGrants(room_join=True, room=room_name))
jwt = token.to_jwt()
```

---

## Web Client Integration

### Dependencies

```json
{
  "dependencies": {
    "@livekit/components-react": "^2.9.19",
    "livekit-client": "^2.17.0",
    "livekit-server-sdk": "^2.15.0"
  }
}
```

### Core Components

- **LiveKitRoom** - Wraps the room connection; provides context for child components
- **VideoConference** - Grid layout for participants
- **ControlBar** - Mute, camera toggle, screen share, leave
- **ParticipantTile** - Individual participant video/audio display

### Room Connection

```tsx
import { LiveKitRoom, VideoConference } from "@livekit/components-react";

<LiveKitRoom
  token={token}
  serverUrl={livekitUrl}
  connect={true}
  audio={true}
  video={true}
  onDisconnected={handleDisconnect}
>
  <VideoConference />
</LiveKitRoom>
```

### Device Settings

Pass preferred device IDs to `LiveKitRoom` for camera/microphone:

```tsx
<LiveKitRoom
  videoCaptureDefaults={{
    deviceId: { ideal: settings.preferredVideoInput },
  }}
  audioCaptureDefaults={{
    deviceId: { ideal: settings.preferredAudioInput },
  }}
  // ...
/>
```

### Data Channels and Transcription

Listen for agent transcription via data messages:

```tsx
room.on(RoomEvent.DataReceived, (payload, participant) => {
  const data = JSON.parse(new TextDecoder().decode(payload));
  if (data.type === "transcription") {
    setTranscripts((prev) => [...prev, data]);
  }
});
```

### Hooks

- `useParticipants()` - List of connected participants
- `useLocalParticipant()` - Local user's tracks and state
- `useTracks()` - All tracks in the room
- `useChat()` - Chat messages (if using LiveKit chat)
- `useConnectionState()` - Connection status

---

## AI Voice Agents

### livekit-agents Framework

The Python `livekit-agents` package provides:

- **Agent** - Unified orchestrator for voice/multimodal sessions
- **Worker/AgentServer** - Agent subscribes to rooms and joins when requested
- **Plugins** - Silero VAD, Whisper STT, Piper/Kokoro TTS, OpenAI/Anthropic/Ollama LLM

### Pipeline Architecture

```
User Speech --> VAD --> STT (Whisper) --> LLM (Ollama) --> TTS (Piper) --> Room Audio
```

### Dependencies

```txt
livekit-agents
livekit-plugins-silero    # Voice Activity Detection
livekit-plugins-whisper   # Speech-to-Text
piper-tts                # Text-to-Speech (or kokoro-tts)
ollama                    # Local LLM (or openai, anthropic)
python-dotenv
```

### Agent Entrypoint

```python
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import piper, silero, whisper

async def entrypoint(ctx: JobContext):
    """SOTA 2026: FastMCP 3.2+ entrypoint."""
    vad = silero.VAD.load()
    stt = whisper.STT()
    tts = piper.TTS()
    llm_engine = SOTAOllamaLLM(model="gemma3-27b") # Upgraded for Teams++

    agent = Agent(
        vad=vad,
        stt=stt,
        llm=llm_engine,
        tts=tts,
        chat_ctx=initial_context,
    )

    @agent.on("user_speech_committed")
    def on_speech(msg: llm.ChatMessage):
        # Custom logic: trigger on keywords, jargon detection, etc.
        pass

    agent.start(ctx.room)
    await agent.say("Agent operational.")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
```

### Custom LLM Integration

Implement `llm.LLM` interface for Ollama or other backends:

```python
class SOTAOllamaLLMStream(llm.LLMStream):
    async def _run(self) -> None:
        # 1.x Pattern: Generate chunks and send to internal channel
        # response = await self._client.chat(...)
        # self._event_ch.send_nowait(llm.ChatChunk(...))
        pass
```

### Agent Configuration (Environment)

```bash
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

Run: `python agent.py dev`

---

## MCP Integration

### Why MCP in LiveKit Projects?

- **Dev tooling** - Query logs, room status, agent health from Claude/Cursor
- **Orchestration** - Start/stop services, check Docker status
- **Observability** - Aggregate telemetry from web + agent

### MCP Server Placement (Teams++ Standard)

In a modernized monorepo (e.g. `myconf`):

```
packages/remoting_mcp/       # Python FastMCP 3.2+
  - move_mouse, click_mouse, type_text
packages/conferencing_mcp/   # Python FastMCP 3.2+
  - generate_meeting_summary, conference_schedule
```

### Example: FastMCP 3.2+ async tool discovery

```typescript
// packages/mcp-server - tools for LiveKit project dev
const LIVEKIT_ROOM_TOOL = {
  name: "livekit_room_status",
  description: "Get active LiveKit rooms and participant counts",
  inputSchema: {
    type: "object",
    properties: { livekit_url: { type: "string", default: "http://localhost:7880" } },
  },
};
```

Implementation would call LiveKit HTTP API (room list) or Redis for room state.

### Cursor/Claude Config

```json
{
  "mcpServers": {
    "ag-visio-mcp": {
      "command": "node",
      "args": ["packages/mcp-server/dist/index.js"],
      "cwd": "d:/Dev/repos/myconf"
    }
  }
}
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|---------|-------------|---------|
| `LIVEKIT_URL` | WebSocket URL for LiveKit server | `ws://localhost:7880` |
| `LIVEKIT_API_KEY` | API key for token signing | `devkey` |
| `LIVEKIT_API_SECRET` | API secret for token signing | `secret` |
| `NEXT_PUBLIC_LIVEKIT_URL` | Public URL for web client (must match server) | - |
| `OLLAMA_BASE_URL` | Ollama API URL (agent; in Docker use `http://host.docker.internal:11434/v1` or `http://ollama:11434/v1`) | `http://localhost:11434/v1` |
| `OLLAMA_MODEL` | Ollama model name for agent | `gemma2` |

### Client Settings (localStorage)

- `preferredVideoInput` - Camera device ID
- `preferredAudioInput` - Microphone device ID
- `preferredAudioOutput` - Speaker device ID
- `defaultRoom` - Default room name
- `theme` - dark | light | system

---

## Deployment

### Development

```powershell
# 1. Start infrastructure
docker compose up -d

# 2. Start agent (separate terminal)
cd apps/agent
.\venv\Scripts\activate
python agent.py dev

# 3. Start web app
npm run dev --workspace=web
```

### Production Checklist

- [ ] Replace `devkey`/`secret` with strong secrets from env
- [ ] Use `wss://` for LiveKit URL (TLS)
- [ ] Enable HTTPS on web server
- [ ] Configure `use_external_ip: true` in livekit.yaml if behind NAT
- [ ] Set up TURN server for restrictive networks
- [ ] Monitor agent logs and room metrics
- [ ] Consider LiveKit Cloud for scaling (optional)

### Docker Compose Full Stack (myconf reference)

Full dockerization: livekit, redis, web, and **agent** in one stack. **Ollama runs outside Docker on your PC**; the agent container reaches it via `OLLAMA_BASE_URL=http://host.docker.internal:11434/v1`. On Linux use `extra_hosts: host.docker.internal:host-gateway`. Optional: add `ollama` service and set agent `OLLAMA_BASE_URL=http://ollama:11434/v1` for all-in-Docker.

```yaml
services:
  livekit:
    image: livekit/livekit-server:latest
    # ... (see above)

  redis:
    image: redis:7-alpine
    # ...

  web:
    build: .
    environment:
      - NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
    depends_on: [livekit]

  agent:
    build: ./apps/agent
    environment:
      - LIVEKIT_URL=ws://livekit:7880
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
      - OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
      - OLLAMA_MODEL=gemma2
    depends_on: [livekit]
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

---

## Troubleshooting

### Connection Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Failed to connect" | Wrong URL or port | Verify `NEXT_PUBLIC_LIVEKIT_URL` matches server (ws://host:7880) |
| "Invalid token" | Key/secret mismatch | Ensure API key/secret match livekit.yaml keys |
| "Permission denied" | Camera/mic blocked | Check browser permissions; use /test page to verify devices |

### Agent Not Joining

| Symptom | Cause | Fix |
|---------|-------|-----|
| Agent never appears | Worker not running | Run `python agent.py dev`; check LIVEKIT_URL |
| Agent joins then disconnects | LLM/Ollama unreachable | Ensure Ollama is running; check agent logs |
| No voice response | VAD too strict | Adjust Silero threshold or trigger keywords |

### Audio/Video Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| No video | Wrong device ID | Use device test page; persist preferred devices |
| Echo | Multiple outputs | Use headphones or ensure single speaker path |
| Choppy audio | Network | Check bandwidth; reduce video resolution |

### Ports

- **7880** - HTTP/WebSocket (primary)
- **7881** - WebRTC
- **50000-60000** - RTP (configurable in livekit.yaml)

---

## Best Practices

### Security

- Never commit API keys; use environment variables
- Use short-lived tokens (default 1h); refresh if needed
- In production, validate participant identity server-side before issuing token

### Performance

- Use adaptive layout (grid) for many participants; consider speaker focus
- Limit transcription history (e.g. 50 entries) to avoid memory bloat
- Agent: Use compact LLM (e.g. gemma2, phi) for low latency

### UX

- Pre-join device validation prevents "black screen" on join
- Reconnection banner and status indicators reduce confusion
- Room link sharing + QR code improves join flow

### Code Quality

- Use TypeScript strict mode for web client
- Centralize LiveKit URL and token logic in API routes
- Log agent events (join, speech, errors) for debugging

---

## Roadmap (Reference: myconf / AG-Visio)

**Phase 2.5: Full self-host calendaring & invitations**

- **Event store** – SQLite/Postgres or CalDAV server (Radicale, Baïkal) for standards-based calendars
- **Scheduling UI** – Create meetings (title, datetime, duration, room); generate room link + optional QR
- **Invitations** – Send "Join room at &lt;time&gt;" link via email (self-hosted SMTP or Email MCP); copy-link fallback
- **No external calendar dependency** – No Google/Microsoft OAuth; optional CalDAV sync for clients
- **MCP tools** – List today's meetings, create meeting, send invite (for Claude/Cursor)

See reference implementation (myconf) `PRD.md` for full Phase 2, 2.5, and 3 roadmap.

---

## References

- [LiveKit Documentation](https://docs.livekit.io/)
- [LiveKit Agents](https://docs.livekit.io/agents/)
- [livekit-server-sdk (Node)](https://www.npmjs.com/package/livekit-server-sdk)
- [@livekit/components-react](https://www.npmjs.com/package/@livekit/components-react)
- [Turborepo MCP Monorepo Pattern](../../docs/patterns/TURBOREPO_MCP_MONOREPO_PATTERN.md)
