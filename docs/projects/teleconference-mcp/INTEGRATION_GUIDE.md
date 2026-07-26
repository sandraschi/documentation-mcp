# Teleconference MCP — Integration Guide

**Last Updated:** 2026-07-13
**Source Repo:** `D:\Dev\repos\myconf` (renamed to `teleconference-mcp`)

---

## Prerequisites

- **Node.js** 18+
- **Python** 3.12+ (SOTA-2026 recommended)
- **Fast_MCP** 3.1+ (GA Feb 18 2026)
- **LiveKit** 1.x (Unified Agent interface)
- **Docker** and Docker Compose (for LiveKit + Redis)
- **Ollama** (for AI agent; install gemma2: `ollama pull gemma2`)

---

## One-Time Setup

From repo root (PowerShell):

```powershell
.\setup.ps1
```

This script:
1. Installs root and workspace dependencies (npm)
2. Creates `apps/agent/venv` and installs agent dependencies from `requirements.txt`
3. Sets up `packages/mcp-server` with `pyproject.toml` standards.

---

## Running the Stack

### Option A: Full Dockerization (one-command)

1. **Ollama runs outside Docker on your PC.** Start Ollama on the host (e.g. `ollama serve`), then `ollama pull gemma2`. The agent container will reach the host's Ollama via `host.docker.internal:11434`.
2. From repo root:
   ```powershell
   docker compose up -d
   ```
3. Access: http://localhost:3000 (web), http://localhost:3000/health, http://localhost:3000/test

   The agent runs in a container and reaches Ollama on your PC (outside Docker) via `OLLAMA_BASE_URL=http://host.docker.internal:11434/v1`. On Linux, `extra_hosts` in compose provides `host.docker.internal`. Optional: add an `ollama` service to compose and set agent `OLLAMA_BASE_URL=http://ollama:11434/v1` for all-in-Docker.

### Option B: start.ps1 (dev: Docker + local web)

```powershell
.\start.ps1
```

- Starts Docker (LiveKit + Redis)
- Waits 3s for LiveKit
- Starts web app on port 10800 (npm run dev --workspace=web)
- Does **not** start the agent; run agent separately (see below)

Flags:
- `-DockerOnly` – Only start Docker; you run web and agent manually
- `-NoDocker` – Skip Docker; only start web (assumes LiveKit already running elsewhere)

### Option C: Manual (Docker + local agent + local web)

1. **Start infrastructure:**
   ```powershell
   docker compose up -d
   ```

2. **Run LiveKit agent** (requires Ollama with gemma2):
   ```powershell
   cd apps/agent
   .\venv\Scripts\activate
   python agent.py dev
   ```

3. **Run web client:**
   ```powershell
   npm run dev --workspace=web
   ```

4. **Access:**
   - Web UI: http://localhost:10800
   - Health: http://localhost:10800/health
   - Test page: http://localhost:10800/test
   - Settings: http://localhost:10800/settings
   - LiveKit: ws://localhost:7880 (when Docker running)

---

## Environment Configuration

### Web app (apps/web/.env.local)

```env
NEXT_PUBLIC_LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

- `NEXT_PUBLIC_*` is exposed to the browser; must match LiveKit server URL.
- For same-machine Docker: `ws://localhost:7880`. For LAN access from another device, use host IP (e.g. `ws://192.168.1.100:7880`) or ensure LiveKit is reachable.

### Agent (apps/agent)

Environment variables (optional; defaults in code):
- `LIVEKIT_URL` – default ws://localhost:7880
- `LIVEKIT_API_KEY` – default devkey
- `LIVEKIT_API_SECRET` – default secret

Use `.env` in apps/agent or set in shell when running `python agent.py dev`.

---

## MCP Server Usage (Fast_MCP 3.1+)

### Python (Refined Industrial Standard)

```powershell
cd packages/mcp-server
python mcp_server.py
```

### Cursor / Claude Desktop configuration

Example (stdio; cwd = myconf repo root):

```json
{
  "mcpServers": {
    "ag-visio-mcp": {
      "command": "python",
      "args": ["packages/mcp-server/mcp_server.py"],
      "cwd": "D:/Dev/repos/myconf"
    }
  }
}
```

### Available tools

- **get_dev_stats** – Git status (short), disk usage (Windows: PowerShell Get-PSDrive).
- **query_system_logs** – pattern (required), limit (optional); queries Windows Event Log (System).
- **sample_log_analysis** – **SOTA 3.1**: Iterative log sampling for AI-guided root cause analysis.
- **Context Injection**: All tools accept `ctx: Context` for correlation tracing (FastMCP 3.1 standard).

---

## Testing

### Web (Vitest + Playwright)

```powershell
cd apps/web
npm run test           # Unit/component
npm run test:e2e       # Playwright E2E
```

From root: `npm run test` (Turbo runs web tests).

### Agent (pytest)

```powershell
cd apps/agent
.\venv\Scripts\activate
pytest -v
```

Tests target `logic.py` (ReductionistLogic) only; no LiveKit or Ollama required.

### Linting

- **Web:** ESLint (see apps/web/package.json).
- **Agent / MCP Python:** `ruff check apps/agent packages/mcp-server`; `ruff format .`

---

## Troubleshooting

### Port 10800 in use

Change port in `apps/web/package.json`: `"dev": "next dev --port <NEW_PORT>"`.

### LiveKit connection fails

1. Ensure Docker is running: `docker compose ps`.
2. Check LiveKit logs: `docker compose logs livekit`.
3. Verify `NEXT_PUBLIC_LIVEKIT_URL` matches server (e.g. ws://localhost:7880).
4. Ensure firewall allows 7880, 7881, 7882.

### Agent not joining / not responding

1. Ensure Ollama is running: `ollama list`; `ollama run gemma2`.
2. Check agent terminal for errors (e.g. connection refused to Ollama).
3. Confirm agent env (LIVEKIT_URL, keys) matches LiveKit server.
4. In room, say "Visio" or use jargon-heavy phrase to trigger reply.

### Camera / microphone not working

1. Grant browser permissions for camera and microphone.
2. Use http://localhost:10800/test to verify devices.
3. Check settings: preferred camera/mic persisted; retry pre-join validation if shown.

### Token invalid

- API key/secret in `.env.local` must match `livekit.yaml` keys (dev: devkey/secret).
- Ensure token API is called with correct room name and participant identity.

---

## Production Considerations

- Replace devkey/secret with strong secrets from env.
- Use `wss://` for LiveKit URL (TLS); put web app behind HTTPS.
- Set `use_external_ip: true` in livekit.yaml if server is behind NAT.
- Configure TURN if participants are on restrictive networks.
- Optionally add monitoring (e.g. Prometheus/Grafana) for LiveKit and app health.
- See PRD.md and integrations/livekit/LIVEKIT_INTEGRATION_GUIDE.md for full checklist.
