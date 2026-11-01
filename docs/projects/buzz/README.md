# Buzz — Block open-source agent workspace

<p align="center">
  <a href="https://github.com/block/buzz"><img src="https://img.shields.io/badge/upstream-block%2Fbuzz-111?style=flat-square" alt="Upstream"></a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0"><img src="https://img.shields.io/badge/License-Apache--2.0-blue?style=flat-square" alt="License"></a>
  <a href="https://www.rust-lang.org"><img src="https://img.shields.io/badge/Rust-1.88%2B-orange?style=flat-square&logo=rust" alt="Rust"></a>
</p>

**Repo:** https://github.com/block/buzz (local: `D:\Dev\repos\buzz`)  
**Type:** Self-hosted Nostr relay + Tauri/React desktop + agent CLI  
**Status:** Local Podman stack + locked relay running on Sandra workstation (Phases 1–3 complete)  
**Last updated:** 2026-07-28

---

## Contents

- [What it is](#what-it-is)
- [Corporate / FOSS status](#corporate--foss-status)
- [Architecture](#architecture-condensed)
- [Agent / MCP integration](#agent--mcp-integration)
- [Local usage](#local-usage-this-workstation)
- [Phase 3 results](#phase-3-results-2026-07-28)
- [Ports](#ports)
- [What works / what does not](#what-works--what-does-not-honest)
- [Related fleet projects](#related-fleet-projects)
- [References](#references)

---

## What it is

Buzz is Block, Inc.'s open-source team workspace where humans and AI agents share channels, threads, git events, and workflows on a **Nostr relay you operate**. Everything is signed events (kind-based protocol); the relay is the single source of truth.

Not an MCP server itself — but it **integrates agents** via `buzz-acp` (ACP harness), `buzz-cli` (JSON CLI), and optional MCP sidecars passed to ACP agents.

---

## Corporate / FOSS status

| Item | Detail |
|---|---|
| **Copyright holder** | [Block, Inc.](https://block.xyz) |
| **License** | [Apache-2.0](https://github.com/block/buzz/blob/main/LICENSE) |
| **Public repo** | https://github.com/block/buzz |
| **Maturity** | Desktop ~0.4.26; relay crate ~0.2.0. Workflow approval gates partially stubbed |
| **Telemetry** | Self-hosted — you control logs |

**Fleet stance:** Worth running locally for agent-in-channel experiments. Credible Nostr-native agent workspace; not a Slack + full MCP fleet replacement yet.

---

## Architecture (condensed)

```
┌─────────────────────────────────────────────────────────────┐
│ Clients                                                     │
│  Buzz desktop (Tauri+React)  │  buzz-cli  │  buzz-acp+agent │
└───────────────┬──────────────────────────────┬──────────────┘
                │ WebSocket / REST (NIP-01)     │
                ▼                               │
┌───────────────────────────────────────────────────────────────┐
│ buzz-relay (Rust/Axum) — ws://host:3000                       │
└───┬─────────────────┬──────────────────────┬──────────────────┘
    │                 │                      │
 Postgres 17      Redis 7              MinIO/S3
```

**Key crates:** `buzz-relay`, `buzz-cli`, `buzz-acp`, `buzz-agent`, `buzz-dev-mcp`, `buzz-workflow`.

---

## Agent / MCP integration

| Path | Mechanism |
|---|---|
| **buzz-cli** (`buzz.exe`) | Agent-first CLI; JSON stdout; NIP-98 auth |
| **buzz-acp** | @mentions → ACP stdio agent → replies via buzz-cli |
| **BUZZ_ACP_MCP_COMMAND** | One stdio MCP server in ACP `session/new` — not a gateway |
| **buzz-dev-mcp** | Shell/file/git tools for dev agents |
| **FastMCP fleet** | Experimental — point `BUZZ_ACP_MCP_COMMAND` at stdio entry if compatible |

---

## Local usage (this workstation)

**Runbook:** `D:\Dev\repos\buzz\LOCAL_SETUP.md`  
**Assessment log:** `D:\Dev\repos\buzz\ASSESSMENT_LOCAL.md`  
**Podman:** `D:\Dev\repos\buzz\deploy\podman\README.md`

### Infra — Podman (not Docker Desktop)

```powershell
cd D:\Dev\repos\buzz
.\deploy\podman\scripts\up.ps1
.\deploy\podman\scripts\get-host.ps1   # VM IP → .env when localhost forward broken
cargo run --release -p buzz-admin -- migrate
cargo run --release -p buzz-relay
```

| Upstream | This workstation |
|---|---|
| `just setup` → docker compose | `deploy/podman/scripts/up.ps1` |
| `localhost:5432` | Podman VM IP in `.env` |
| `podman machine start` (Windows) | Often fails SSH — use WSL rootful |

### Relay + lockdown

Health: `http://127.0.0.1:3000/health`, `http://127.0.0.1:8080/_readiness`.

Locked relay vars: `RELAY_OWNER_PUBKEY`, `BUZZ_RELAY_PRIVATE_KEY`, `BUZZ_REQUIRE_RELAY_MEMBERSHIP=true`, `BUZZ_REQUIRE_AUTH_TOKEN=true`.

---

## Phase 3 results (2026-07-28)

| Test | Result |
|---|---|
| Separate agent keypair + relay membership | **Pass** |
| Channel create + add agent as bot | **Pass** |
| Agent `messages send` / owner `messages get` | **Pass** |
| buzz-dev-mcp release build | **Pass** |
| buzz-acp `build_mcp_servers` unit tests | **Pass** (9) |
| Full buzz-acp @mention → LLM reply | **Not run** — no `goose` on PATH; `buzz-agent` needs API key |

Validated channel: `phase3-agent` (`820fe4f5-f324-47b7-a631-85b39fc179df`).

---

## Ports

| Service | Port |
|---|---|
| buzz-relay WS | 3000 |
| Health / readiness | 8080 |
| Metrics | 9102 |
| Postgres / Redis / MinIO | 5432 / 6379 / 9000 |

Not in `WEBAPP_PORTS` — not an MCP repo.

---

## What works / what does not (honest)

| Works | Partial / not implemented |
|---|---|
| Podman infra + native relay (locked) | Workflow approval gates (WF-08) |
| buzz-cli agent channel smoke | `send_dm` / `set_channel_topic` workflow actions |
| buzz-dev-mcp + ACP MCP config path | Full ACP loop without LLM credentials |
| Git smart HTTP, NIP-34 | Podman localhost port forward |
| Apache-2.0 self-host | Arbitrary MCP → channel without ACP agent |

---

## Related fleet projects

| Project | Relationship |
|---|---|
| [security-gym](../security-gym/README.md) | Cyber RL benchmark — optional alert sink via buzz-cli (glue only) |
| [podman-mcp](../podman-mcp/README.md) | Podman control plane elsewhere on workstation |
| [cursor-mcp](../cursor-mcp/README.md) | Cursor inbox — orthogonal to Buzz channels |
| [fleet-agent-mcp](../fleet-agent-mcp.md) | Could post to Buzz via buzz-cli if configured |

---

## References

- Upstream: https://github.com/block/buzz
- Local setup: `D:\Dev\repos\buzz\LOCAL_SETUP.md`
- Vision: `VISION.md`, `VISION_AGENT.md`
- buzz-acp: `crates/buzz-acp/README.md`
