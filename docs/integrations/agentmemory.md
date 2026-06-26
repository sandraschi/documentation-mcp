# Agentmemory — Persistent Memory for AI Coding Agents

**Category**: AI Assistants & Agent Platforms
**Repo**: [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)
**License**: Apache 2.0

Agentmemory is a persistent memory engine for coding agents. It silently captures tool use, compresses observations into searchable memory, and injects relevant context on session start — eliminating the "re-explain your stack" tax. 13.1k GitHub stars, 53 MCP tools, 12 auto-capture hooks.

## How It Works

```
Session 1: agent adds JWT auth → agentmemory captures every tool call, result, decision
Session 2: agent is asked about rate limiting → agentmemory injects: "JWT uses jose middleware
            in src/middleware/auth.ts, tests cover token validation, chose jose over jsonwebtoken
            for Edge compatibility" → agent starts working immediately
```

- **93% semantic recall** (LongMemEval-S benchmark, `all-MiniLM-L6-v2` local embeddings)
- **~1,900 tokens/session** injected vs 22K+ for full CLAUDE.md (92% less)
- **4-tier consolidation**: working → episodic → semantic → procedural; Ebbinghaus decay curve
- **Triple-stream search**: BM25 keyword + vector cosine + knowledge graph BFS, fused via RRF
- **Zero external DBs**: SQLite + local embeddings; no cloud, no API keys needed

## Architecture

| Component | Role |
|---|---|
| **`@agentmemory/agentmemory`** | Main Node.js server (REST on `:3111`, viewer on `:3113`) |
| **`iii-engine`** (v0.11.2) | Native Rust backend — function registry (`mem::*`), WebSocket on `:49134` |
| **`@agentmemory/mcp`** | Thin MCP shim — proxies 53 tools when server is reachable, 7-tool local fallback |
| **`plugin/opencode/`** | OpenCode-native plugin: 22 hooks, 2 slash commands (`/recall`, `/remember`) |

## Fleet Relevance

Every fleet agent that uses `CLAUDE.md`, `MEMORY.md`, or manual context re-explanation benefits from agentmemory. The memory surface is shared across all connected agents via MCP — OpenCode, Claude Code, Cursor, Gemini CLI, OpenClaw, Hermes, and OpenManus all share the same memory server.

| Fleet Agent | Integration Path |
|---|---|
| **OpenCode** | 22 hooks + MCP + plugin (`plugin/opencode/`) |
| **Claude Code** | Native plugin (marketplace: `rohitg00/agentmemory`) + 12 hooks + MCP |
| **OpenClaw / Hermes** | MCP block + deeper memory-slot plugin |
| **OpenManus** | MCP via `mcp.json` |
| **Any agent** | MCP (`mcpServers` block) or REST API `:3111` |

## MCP Tool Surface (53 tools)

Core tools: `memory_recall`, `memory_save`, `memory_smart_search`, `memory_sessions`, `memory_file_history`, `memory_patterns`, `memory_governance_delete`, `memory_export`, `memory_audit`, `memory_import_jsonl`, `memory_health`, `memory_stats`, `memory_consolidate`, `memory_auto_forget`, `memory_graph_search`, `memory_graph_expand`, `memory_compress_file`, `memory_replay_load`, `memory_replay_sessions`, `memory_search_entities`, `memory_list_entities`, `memory_citation`, `memory_viewer_launch`, `memory_doctor`, `memory_upgrade`, plus 28 more (leases, signals, routines, actions, slots, teams, git snapshots, config management, cron jobs).

## Windows Setup (SOTA Fleet)

```powershell
# 1. Download iii-engine binary from:
#    https://github.com/iii-hq/iii/releases/tag/iii%2Fv0.11.2
#    → iii-x86_64-pc-windows-msvc.zip (or aarch64 for ARM)
# 2. Extract iii.exe to %USERPROFILE%\.local\bin\iii.exe
# 3. Verify:
iii --version   # should print 0.11.2

# 4. Start agentmemory:
npx -y @agentmemory/agentmemory

# 5. Health check:
Invoke-WebRequest -Uri "http://localhost:3111/agentmemory/health"

# 6. OpenCode wiring — add to opencode.json:
#    {"mcp": {"agentmemory": {"type": "local", "command": ["npx", "-y", "@agentmemory/mcp"], "enabled": true}}}
```

## Ports

| Port | Service | Notes |
|---|---|---|
| 3111 | REST API + MCP proxy | Agent-facing API |
| 3113 | Real-time viewer | Browser dashboard for memory inspection |
| 49134 | iii-engine WebSocket | Internal Rust backend (local only) |

> These ports are **outside** the fleet range (10700–11000) — agentmemory is an external service, not a fleet MCP server. No port conflict with fleet webapps.

## Token Economics

| Approach | Tokens/year | Cost/year (DeepSeek V3) |
|---|---|---|
| Paste full context | 19.5M+ | Exceeds context window |
| LLM-summarized | ~650K | ~$500 |
| **agentmemory (local embeddings)** | **~170K** | **~$10** |
| agentmemory + local embeddings | ~170K | $0 (free) |

## Caveats

- Windows: no scoop/winget package; manual `iii-engine` binary download required
- ~80MB RAM for local embeddings (`all-MiniLM-L6-v2`)
- SessionStart hook adds latency (~1-3s) for memory injection
- Semantic search misfire risk with sparse/early memory; improves over time
- Stale memory accumulation requires occasional manual cleanup via `memory_governance_delete`
- `iii-engine` pins to v0.11.2; v0.11.6+ sandbox model not yet supported

## Reference

- Repo: https://github.com/rohitg00/agentmemory
- Landing: https://agent-memory.dev
- Design doc: https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- Benchmarks: `benchmark/LONGMEMEVAL.md`, `benchmark/COMPARISON.md`
- OpenCode plugin: `plugin/opencode/README.md` (22-hook table + gap analysis)

---
*Status: Active — external service, MCP integration tested with OpenCode, Claude Code, Cursor*
*Tags: #memory #agent-memory #opencode #claude-code #mcp #coding-agents #token-optimization*
