# LiveKit Integration Guide

**Last Updated:** 2026-09-06 (server v1.13.6, agents v1.8.0, client v2.22.2, server-sdk v2.18.0)
**Status:** SOTA Compliance
**Reference Implementation:** teleconference-mcp at `D:\Dev\repos\teleconference-mcp`

---

## Table of Contents

1. [Overview](#overview)
2. [History](#history)
3. [Architecture](#architecture)
4. [LiveKit Server](#livekit-server)
5. [Web Client Integration](#web-client-integration)
6. [AI Voice Agents](#ai-voice-agents)
7. [MCP Integration](#mcp-integration)
8. [Configuration](#configuration)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)
12. [Who Uses LiveKit](#who-uses-livekit)
13. [Community](#community)
14. [Bibliography](#bibliography)

---

## Overview

### What is LiveKit?

LiveKit is an open-source **WebRTC SFU (Selective Forwarding Unit)** that provides:

- **Real-time video/audio** - Low-latency WebRTC streaming
- **Room-based sessions** - Multi-participant conferencing with named rooms
- **Token-based auth** - JWT tokens for secure room access
- **Data channels** - Real-time messaging alongside media
- **Agent framework** - Python SDK for voice AI participants

### Key Features (server v1.13.x)

| Feature | Description |
|--------|-------------|
| **SFU Architecture** | Selective forwarding reduces bandwidth; each participant sends one stream |
| **Adaptive Bitrate** | Automatic quality adjustment based on network conditions |
| **Screen Sharing** | Native track publishing for screen capture |
| **Recording** | Egress v2 (`createRoomCompositeEgress`, server v1.13.2+) with MP4/file/S3 output |
| **Agents** | Python/TypeScript SDK for bot participants (voice, transcription, vision) |
| **Data tracks** | Ordered, reliable data delivery on by default (server v1.11+) — replaces lossy data-channel for transcripts |
| **Room auto-create** | `roomCreate` JWT grant spawns rooms on first join (server v1.12+, no explicit `room_create`) |
| **SIP/Telephony** | PSTN ingress, call transfer RPC, Answering Machine Detection (agents) |

### When to Use LiveKit

- **Video conferencing** - Standups, code reviews, team meetings
- **Voice AI** - Real-time voice agents with STT/LLM/TTS pipelines
- **Live streaming** - Low-latency broadcast with interactive participants
- **Robotics teleoperation** - Low-latency video return (fleet: `teleoperator-mcp`, room `teleop-boomy`)
- **Self-hosted** - Full control over infrastructure and data

---

## History

Founded 2021 in San Francisco by **Russ d'Sa (CEO)** and **David Zhao (CTO)** as an open-source WebRTC SFU — self-hostable real-time media for the "metaverse" era (Twilio/Agora alternative). Demand for hosting from Spotify, Oracle, and Reddit produced **LiveKit Cloud**. After ChatGPT launched, d'Sa's LiveKit-powered voice demo won a deal to run **ChatGPT voice modes on LiveKit Cloud**, pivoting the company to voice-AI infrastructure: SDKs, UI components, SIP, egress, and the Agents framework. Funding: $7M seed (Redpoint, Dec 2021) + $8M (2022); $22M Series A (Altimeter, Jun 2024); $45M Series B (Altimeter, Apr 2025, $345M); **$100M Series C (Index Ventures, Jan 2026, $1B, $183M total)**. 300,000+ developers; `livekit/livekit` ~20.7k stars (Apache-2.0, Go); `livekit/agents` ~14k stars (Sep 2026). Fleet relevance: our `teleconference-mcp` + `teleoperator-mcp` both ride the `LiveKitSFU` Windows service (now v1.13.6).

---

## Architecture

### Component Diagram

```
+------------------+     +------------------+     +------------------+
|   Web Client     |     |  LiveKit Server  |     |  Voice Agent     |
|  (Next.js/React) |---->|  (Docker)        |<----|  (Python)        |
|  livekit-client  |     |  Port 15580      |     |  livekit-agents  |
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

> **Fleet deployment (Goliath):** the fleet SFU runs as a **Windows service**
> (`LiveKitSFU`, NSSM, native `livekit-server` **1.13.6** since 2026-09-06, config `teleconference-mcp/livekit.yaml`,
> auto-start + crash-restart) — **not** Docker. Verify: `Get-Service LiveKitSFU` + `& livekit-server --version`;
> logs: `D:\Dev\repos\teleconference-mcp\logs\livekit.out.log` / `.err.log` (a Windows CPU-monitor notice in
> `.err.log` is benign); reinstall (elevated):
> `D:\Dev\repos\teleoperator-mcp\scripts\install-livekit-service.ps1`.
> The Docker instructions below remain valid for non-Windows / dev machines.

### Docker Setup

```yaml
# docker-compose.yaml (dev / non-Windows; pin the version, never :latest)
services:
  livekit:
    image: livekit/livekit-server:v1.13.6
    command: --config /etc/livekit.yaml
    volumes:
      - ./livekit.yaml:/etc/livekit.yaml
    ports:
      - "15580:15580"   # HTTP/WebSocket (fleet port; upstream default is 7880)
      - "7881:7881"     # WebRTC TCP
      - "7882:7882/udp" # TURN (if needed)
    restart: always
```

### Configuration (livekit.yaml)

```yaml
port: 15580   # fleet port (upstream default 7880)
rtc:
  port_range_start: 50000
  port_range_end: 60000
  use_external_ip: false
  stun_servers:
    - stun.l.google.com:19302     # host:port — no stun: prefix
    - stun1.l.google.com:19302
  # TURN (server v1.12+, TTL ENFORCED since v1.13.1 — old no-TTL creds stop working):
  # turn:
  #   enabled: true
  #   secret: <rotate-me>
  #   ttl_seconds: 300
keys:
  devkey: secret   # API key
  # In production: use env vars or secrets
logging:
  level: info
```

> Server 1.10+ notes: log key `pID` was renamed `participantID` (update Loki/Grafana filters);
> 1.13.x enforces per-participant TURN quota (default 12), WS read-size and API body-size limits,
> and drops H.264 baseline (`42001f`) from default codecs.

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
    roomCreate: true, // server v1.12+: room auto-created on first join
    room: roomName,
    canPublish: true,
    canSubscribe: true,
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
    "@livekit/components-react": "^2.9.24",
    "livekit-client": "^2.22.2",
    "livekit-server-sdk": "^2.18.0"
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

### Dependencies (agents v1.8.0, Sep 2026)

```txt
livekit-agents[pipeline,silero,turn-detector]>=1.8.0
livekit-plugins-openai>=1.8.0
livekit-plugins-silero>=1.8.0
livekit-plugins-deepgram>=1.8.0
livekit-plugins-elevenlabs>=1.8.0
ollama>=0.4.0
python-dotenv>=1.0.0
```

> There is no `livekit-plugins-whisper` package — Whisper STT arrives via the OpenAI plugin
> (`livekit-plugins-openai`) or local inference. A stale reference to it once broke the agent Docker build.

### Agent Entrypoint

```python
from livekit.agents import (
    Agent, AgentSession, JobContext, WorkerOptions, cli,
    llm,
)
from livekit.agents.voice import AutoRestartPolicy
try:
    from livekit.agents.voice import UserTurnLimitOptions  # 1.5.12+
except ImportError:
    UserTurnLimitOptions = None

async def entrypoint(ctx: JobContext):
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(model="whisper-1"),   # or local Whisper
        llm=SOTAOllamaLLM(model="gemma2"),   # custom llm.LLM backend
        tts=piper.TTS(),                     # or cloud TTS
        turn_detection="auto",
        user_turn_limits=(UserTurnLimitOptions(max_user_turn_duration=60.0)
                          if UserTurnLimitOptions else None),
        # expressive=True needs an inference TTS voice — off for local Piper
    )
    await session.start(room=ctx.room, agent=Agent(instructions="..."))
    await session.say("Agent operational.")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint,
        job_restart_policy=AutoRestartPolicy.ALWAYS,
    ))
```

> Agents 1.7+ tag trace/log content keys as `lk.pii.*` (PII redaction) and speak full OTel GenAI
> conventions — keep transcripts at DEBUG so Loki stays clean.

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
LIVEKIT_URL=ws://localhost:15580
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

In a modernized monorepo (e.g. `teleconference-mcp`):

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
    properties: { livekit_url: { type: "string", default: "http://localhost:15580" } },
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
      "cwd": "D:\Dev\repos\teleconference-mcp"
    }
  }
}
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|---------|-------------|---------|
| `LIVEKIT_URL` | WebSocket URL for LiveKit server | `ws://localhost:15580` (fleet; upstream default `ws://localhost:7880`) |
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

### Docker Compose Full Stack (teleconference-mcp reference)

Full dockerization: livekit, redis, web, and **agent** in one stack. **Ollama runs outside Docker on your PC**; the agent container reaches it via `OLLAMA_BASE_URL=http://host.docker.internal:11434/v1`. On Linux use `extra_hosts: host.docker.internal:host-gateway`. Optional: add `ollama` service and set agent `OLLAMA_BASE_URL=http://ollama:11434/v1` for all-in-Docker.

```yaml
services:
  livekit:
    image: livekit/livekit-server:v1.13.6
    # ... (see above)

  redis:
    image: redis:7-alpine
    # ...

  web:
    build: .
    environment:
      - NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:15580
      - LIVEKIT_API_KEY=${LIVEKIT_API_KEY}
      - LIVEKIT_API_SECRET=${LIVEKIT_API_SECRET}
    depends_on: [livekit]

  agent:
    build: ./apps/agent
    environment:
      - LIVEKIT_URL=ws://livekit:15580
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
| "Failed to connect" | Wrong URL or port | Verify `NEXT_PUBLIC_LIVEKIT_URL` matches server (fleet `ws://host:15580`, upstream default `ws://host:7880`) |
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

### Ports (fleet / upstream default)

- **15580 / 7880** - HTTP/WebSocket (primary; fleet uses 15580)
- **7881** - WebRTC TCP
- **50000-60000** - RTP/ICE (configurable in livekit.yaml)

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

## Roadmap (Reference: teleconference-mcp / AG-Visio)

**Phase 2.5: Full self-host calendaring & invitations**

- **Event store** – SQLite/Postgres or CalDAV server (Radicale, Baïkal) for standards-based calendars
- **Scheduling UI** – Create meetings (title, datetime, duration, room); generate room link + optional QR
- **Invitations** – Send "Join room at &lt;time&gt;" link via email (self-hosted SMTP or Email MCP); copy-link fallback
- **No external calendar dependency** – No Google/Microsoft OAuth; optional CalDAV sync for clients
- **MCP tools** – List today's meetings, create meeting, send invite (for Claude/Cursor)

See reference implementation (teleconference-mcp) `PRD.md` for full Phase 2, 2.5, and 3 roadmap.

---

## Who Uses LiveKit

| User | What runs on LiveKit |
|------|----------------------|
| **OpenAI ChatGPT voice modes** | Realtime voice conversation on LiveKit Cloud |
| **Apple FaceTime (iOS 18)** | LiveKit embedded for emergency calls |
| **France's Visio** | Government video-conferencing platform on the OSS SFU |
| **Spotify / Oracle / Reddit / AT&T** | Early Cloud adopters (livestreaming, interactive audio) |
| **Salesforce, Meta** | Voice/video AI features (per company disclosures) |
| **911 emergency services (US)** | Real-time emergency-call media |
| **LiveKit Meet** (`livekit-examples/meet`, OSS) | Reference conferencing app our web UI descends from |
| **Fleet** | `teleconference-mcp` (conferencing + Visio agent) and `teleoperator-mcp` (robot video return) |

---

## Community

| Channel | Address |
|---------|---------|
| Docs (with `llms.txt`) | <https://docs.livekit.io> |
| GitHub org | <https://github.com/livekit> |
| Forum | <https://community.livekit.io> |
| Slack | <https://livekit.com/join-slack> |
| Blog | <https://livekit.io/blog> |
| YouTube | <https://www.youtube.com/@livekit_io> |
| Coding-agent support (MCP) | <https://docs.livekit.io/mcp> |

---

## Bibliography

* Docs — <https://docs.livekit.io> and `llms.txt` (<https://docs.livekit.io/llms.txt>)
* `livekit/livekit` (Go SFU, Apache-2.0) — <https://github.com/livekit/livekit>, releases <https://github.com/livekit/livekit/releases>
* `livekit/agents` — <https://github.com/livekit/agents>, releases <https://github.com/livekit/agents/releases>
* SDKs/components/server-SDKs under <https://github.com/livekit> (`client-sdk-js/swift/android/flutter`, `components-js`, `node-sdks`, `python-sdks`, `server-sdk-go/ruby`)
* Wikipedia, "LiveKit" — <https://en.wikipedia.org/wiki/LiveKit>
* Bass (2026-01-22), Bloomberg — <https://www.bloomberg.com/news/articles/2026-01-22/livekit-seller-of-voice-tools-to-openai-raises-100-million>
* Wiggers (2025-04-10), TechCrunch — <https://techcrunch.com/2025/04/10/livekits-tools-help-power-real-time-communications/>
* Shrivastava (2024-06-04), Forbes — <https://www.forbes.com/sites/rashishrivastava/2024/06/04/this-110-million-startup-is-building-a-nervous-system-for-ai/>
* Bovenziner (2026-02-11), The Stack (France Visio) — <https://www.thestack.technology/inside-the-open-source-project-powering-frances-video-platform-revolution/>
* Makaryan (2024-09-26), Center for Data Innovation (Q&A with Russ d'Sa) — <https://datainnovation.org/2024/09/5-qs-for-russell-dsa-co-founder-and-ceo-of-livekit/>
* [Turborepo MCP Monorepo Pattern](../../docs/patterns/TURBOREPO_MCP_MONOREPO_PATTERN.md)


