# MCP Federation Hub (federation-mcp)

**Unified orchestration layer for MCP server ecosystems: one API and dashboard to discover, monitor, and call tools on many MCP servers, plus hub-to-hub mesh (peers) with encrypted links.**

---

## Summary

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\mcp-federation-hub` |
| **Ports** | Dashboard 10856, Bridge 10857 |
| **Start** | `webapp\start.bat` (starts bridge + Vite) or run bridge and webapp separately |
| **Dashboard** | http://localhost:10856 |
| **Bridge API** | http://localhost:10857 — Redoc: http://localhost:10857/redoc |

---

## What it does

- **Federation:** One bridge aggregates many MCP servers (and remote hub peers) behind one REST API. List servers, check health, route tool calls (local MCP or remote hub).
- **Mesh (peers):** Connect to other Federation Hub instances via invite links. Hub-to-hub calls use HTTPS and optional Bearer tokens (encrypted links). Add peers in Dashboard → Peers; share “Your invite link” so others can add you.
- **Optional:** AI routing (OpenAI/Ollama), FastMCP sampling, WorldLabs proxy, webapp registry/launcher (run start.bat for registered apps).

---

## Quick start

```powershell
cd D:\Dev\repos\mcp-federation-hub
cd bridge
uv sync
uv run python -m uvicorn app.main:app --host 127.0.0.1 --port 10857
```

In another terminal:

```powershell
cd D:\Dev\repos\mcp-federation-hub\webapp
npm install
npm run dev
```

Or from `webapp/`: run **start.bat** (starts bridge + Vite).

### Windows Service (NSSM)

The bridge is registered as a Windows service via NSSM for 24/7 operation:

```powershell
# Install (requires Administrator):
D:\Dev\repos\mcp-federation-hub\bridge\install-service.ps1

# Manage:
nssm status mcp-federation-hub       # check status
nssm restart mcp-federation-hub      # restart (Admin required)
nssm stop mcp-federation-hub         # stop (Admin required)
```

The service auto-starts at boot and restarts on failure.

---

## Docs (in repo)

- **docs/ARCHITECTURE.md** – Concepts (federation, bridge vs dashboard, server vs peer), components (FederationManager, peers module, tool routing, AI, sampling, apps, WorldLabs), data flow, config files.
- **docs/API.md** – Every endpoint (health, servers, tools, peers, AI, sampling, WorldLabs, apps), request/response shapes, federation config schema.
- **docs/PEERS_AND_MESH.md** – Hub-to-hub mesh: invite link, encrypted links, all functions in `bridge/app/peers.py`, bridge API behavior for peers, security, env vars, workflow to connect two hubs.

---

## Key concepts

- **Bridge:** FastAPI app in `bridge/`; loads `federation-config.json` and `bridge/peers.json`; exposes REST API; merges peers into the server list.
- **Peer / remote hub:** Another Federation Hub instance; added by URL (HTTPS required for encryption) and optional token; appears as a virtual server; tool calls are forwarded to the peer’s `/api/v1/peers/invoke`.
- **Invite link:** This hub’s public URL + token; share so others can add you as a peer (Dashboard → Peers → “Your invite link”).
- **Fleet Supervisor** (v1.4.0+): Background health monitor polls all fleet servers every 30s. Supervised servers are auto-restarted on 3 consecutive failures with exponential backoff (60s -> 120s -> 240s -> 300s). Gates: RAM<90%, fleet proc count<60. Max 1 concurrent restart. 120s startup grace period. See bridge/app/health_monitor.py.

---

## Config and persistence

- **federation-config.json** (repo root): Federation metadata, local `servers`, `categories`.
- **bridge/peers.json**: This hub’s `my_token`, `public_url`, and list of `remote_hubs` (id, name, base_url, peer_token).

---

## Categories (for MCP Central)

Orchestration, federation, dashboard, FastMCP, mesh, security (encrypted hub-to-hub links).
