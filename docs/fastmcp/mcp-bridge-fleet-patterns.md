# MCP Bridge: Fleet ProxyProvider Patterns

**Standard:** FastMCP 3.4+ `create_proxy()` / ProxyProvider  
**Env var:** `MCP_BRIDGE_URLS` (comma-separated HTTP/SSE MCP URLs)  
**Remote stdio clients:** [3.4-features.md](3.4-features.md) — `uvx fastmcp-remote <url>`

---

## 0. FastMCP 3.4 proxy behavior (read first)

As of **3.4.0**, proxies forward **`initialize` and `ping`** to the upstream server. A bridge only succeeds after the upstream handshake succeeds.

| Before 3.4 | From 3.4 onward |
|------------|-----------------|
| Proxy could connect with empty tool list if URL wrong | Handshake fails immediately — wrong URL, dead server, auth denied |
| Silent `except: pass` on `create_proxy()` hid misconfig | Log or raise; use startup probes for `MCP_BRIDGE_URLS` |

For Cursor hosts that cannot use HTTP directly, prefer **`fastmcp-remote`** instead of embedding a broken proxy inside a stdio server.

## 1. What ProxyProvider Actually Does

`ProxyProvider` connects server A to server B's SSE endpoint, discovers B's tools, and **re-exposes them to A's client**. That's it — it merges tool lists, not execution.

```
Client ──connects to──→ Server A (bridged to B)
                           ├── A:speak()
                           ├── A:search_docs()
                           └── B:store_memory()   ← visible through the bridge
```

The client still calls B's tools explicitly. There is **no automatic triggering** — when A's `speak()` runs, it does not automatically call B's `store_memory()` unless the client sequences them.

**What the bridge is good for:**
- Reducing connection count (client connects to 1 server instead of 3)
- Making tools discoverable through a single endpoint
- Hiding network topology from the client

**What the bridge is NOT:**
- Not orchestration — tools don't call each other automatically
- Not a workflow engine — no sequencing, branching, or error handling
- Not a proxy for the client's LLM — the client still decides what to call

---

## 2. The Architectural Options for Multi-Tool Workflows

Consider a concrete request:

> *"Read spreadsheet A, read the first line in a nice Vincent Price voice."*

This requires:
1. A spreadsheet reader (opens `.xlsx`, extracts cell values)
2. A TTS engine (synthesizes text with a Vincent Price style)
3. Sequencing: read → extract first line → hand text to TTS

Here are the three architectural patterns, ranked by client exertion.

---

### Pattern A: Client Orchestrates (Current MCP Norm)

The client connects to both a spreadsheet MCP server and speech-mcp. The client's own LLM plans and executes the two-step sequence.

```
Client (Claude Desktop)
  │
  ├── connected to: spreadsheet-mcp
  │     tool: read_sheet(path, range)
  │
  └── connected to: speech-mcp
        tool: text_to_speech(text, provider, voice_id)

Flow:
  1. Client calls  spreadsheet:read_sheet("A.xlsx", "A1")      → "Total revenue: €42,000"
  2. Client calls  speech:text_to_speech("Total revenue: €42,000", "hume", "ito")
```

**Pros:** Simplest. No extra infrastructure. Each server is single-purpose.
**Cons:** Client needs to connect to N servers. Client LLM must reason about the sequence every time. No reusability — every client reconstructs the same pipe.

**The bridge does NOT change this flow** — it only reduces the connection count. With a bridge, client connects to spreadsheet-mcp which proxies speech-mcp's tools:

```
Client ──→ spreadsheet-mcp (bridged to speech-mcp)
  1. Client calls  read_sheet("A.xlsx", "A1")
  2. Client calls  speech:text_to_speech(...)    ← visible through bridge
```

Same two calls, one connection. No automatic sequencing.

---

### Pattern B: Domain Agentic Tool (ctx.sample() + next_steps)

A domain server (e.g., speech-mcp) has an agentic tool that uses `ctx.sample()` to plan a sequence, then returns steps for the client to execute. **No embedded MCP client in the server.**

```
Client ──→ speech-mcp (agentic tool + bridge to spreadsheet-mcp)
              tool: agentic_conversation_workflow(goal)

  1. Client calls  agentic_conversation_workflow("Read spreadsheet A, Vincent Price voice")
  2. Server's ctx.sample() plans:
     → "Call spreadsheet:read_sheet('A.xlsx','A1'), then call text_to_speech with result"
  3. Server returns {"next_steps": ["read_sheet(...)", "text_to_speech(...)"]}
  4. Client executes each step, using bridged tools
```

**Pros:** Domain expertise in planning (speech-mcp knows which voices fit "Vincent Price"). No embedded MCP client. Lightweight — just `ctx.sample()`.
**Cons:** Still requires client to execute steps. The plan is static — no real-time feedback between steps.

speech-mcp already has this: `agentic_conversation_workflow` returns `next_steps`. The pattern is:
- **Plan** in the server (uses `ctx.sample()` for domain reasoning)
- **Execute** in the client (runs the returned steps)
- **Bridge** to make all needed tools visible through one connection

---

### Pattern C: Dedicated Orchestrator Server

A meta-server (meta-mcp, federation-hub) bridges to multiple domain servers and has agentic tools that orchestrate across them. This is where a full internal MCP client (`create_proxy()`) could live if needed.

```
Client ──→ federation-hub (bridged to spreadsheet-mcp + speech-mcp + memops + ...)
              tool: execute_mission(goal)
              tool: workflow_build(goal)
              tool: chain_execute(steps)

  1. Client calls  execute_mission("Read spreadsheet A in Vincent Price voice")
  2. Hub uses ctx.sample() to build a plan
  3. Hub executes each step internally (reading spreadsheet, calling TTS)
  4. Hub returns the final result
```

**Pros:** One call from the client. Hub handles sequencing, error handling, retries. Central governance.
**Cons:** More infrastructure. The hub needs to either:
  - **Use `ctx.sample()` + return `next_steps`** (same as Pattern B, just in a central server)
  - **Embed an MCP client via `create_proxy()`** to call bridged tools internally — this IS embedding a client in a server, which is appropriate for a central orchestrator but overkill for domain servers

---

## 3. The Natural Partnership: Bridge + Agentic Workflow

These two compose naturally:

```
Bridge (ProxyProvider)    makes tools visible          ──┐
Agentic workflow          plans the sequence (ctx.sample)  ├── one connection, one plan
Client                    executes the steps            ──┘
```

The server uses `ctx.sample()` to reason about which tools to call and in what order — contributing its domain expertise (voice selection, timing, fallback logic). The bridge ensures the client already sees all those tools. The client executes the steps against visible tools.

```
Client
  │
  └── one connection → speech-mcp (bridged to spreadsheet-mcp + memops)
        │
        ├── agentic tool: "Read spreadsheet A in Vincent Price voice"
        │     ctx.sample() plans:
        │       "Use spreadsheet:read_sheet('A.xlsx', 'A1')
        │        → text_to_speech(result, provider='hume', voice='ito')
        │        → memops:store_memory(result, tags=['tts','spreadsheet'])"
        │
        └── client executes all 3 steps — tools are visible through the bridge
```

This is the fleet's recommended default pattern for any server that needs cross-domain workflows.

---

## 4. Three Architectural Patterns

| Pattern | Bridge? | Agentic? | Client does | Best for |
|---------|---------|----------|-------------|----------|
| **A — Client sequences** | Optional | No | All tool calls | Two tools, simple pipes |
| **B — Agentic + Bridge** (recommended) | Yes | Server plans | Executes steps | Domain servers needing cross-tool workflows |
| **C — Orchestrator server** | Yes | Server plans + executes | Single call | Meta-orchestrators (federation-hub, meta-mcp) |

For the spreadsheet + Vincent Price example through each:

**Pattern A** — Client has 2 connections, makes 2 sequential calls:
```
Client → spreadsheet:read_sheet("A.xlsx", "A1")
Client → speech:text_to_speech("Total revenue: €42,000", "hume", "ito")
```

**Pattern B (recommended)** — Client has 1 connection (bridged), makes 1 planning call + executes steps:
```
Client → speech:agentic_conversation_workflow("Read spreadsheet A in Vincent Price voice")
  ctx.sample() returns:
    next_steps: [
      "spreadsheet:read_sheet('A.xlsx', 'A1')",
      "text_to_speech('Total revenue: €42,000', 'hume', 'ito')",
      "memops:store_memory('Total revenue: €42,000', tags=['tts','spreadsheet'])"
    ]
Client executes each step using tools visible through the bridge.
```

**Pattern C** — Client makes 1 call, orchestrator does everything:
```
Client → federation:execute_mission("Read spreadsheet A in Vincent Price voice")
  Hub bridges to spreadsheet + speech + memops
  Hub plans (ctx.sample) + executes internally (create_proxy)
  Hub returns final result
```

---

## 4. Setup

### Per-repo: set the env var

```env
# .env
MCP_BRIDGE_URLS=http://127.0.0.1:10909/mcp,http://127.0.0.1:10704/mcp
```

### How it works at the code level

Every retrofitted repo does this at startup:

```python
from fastmcp.providers import ProxyProvider

bridge_urls = os.getenv("MCP_BRIDGE_URLS", "")
for url in bridge_urls.split(","):
    url = url.strip()
    if url:
        try:
            mcp.add_provider(ProxyProvider(url=url))
        except Exception:
            pass
```

The `ProxyProvider` connects to the target SSE endpoint, discovers tools, and registers them into the local `mcp` instance. The client sees a merged tool list.

---

## 5. Fleet Pairing Catalogue

These are the most useful bridge pairings in the fleet. Every repo listed has been retrofitted — just set `MCP_BRIDGE_URLS`.

### Voice + Memory (speech-mcp + memops)

```
speech-mcp (10909)  ←──  memops (advanced-memory-mcp, 10704)
```

**What it makes visible:** speech-mcp's client can call memops tools — `store_memory`, `recall`, `search`.

**Setup (in speech-mcp/.env):**
```env
MCP_BRIDGE_URLS=http://127.0.0.1:10704/mcp
```

**Usage (Pattern A — client orchestrates):**
1. Client calls `speech:text_to_speech("Hello world", "gemini")`
2. Client calls `memops:store_memory("TTS: Hello world", tags=["tts"])`

**Usage (Pattern B — agentic tool):**
1. Client calls `speech:agentic_conversation_workflow("Remember everything I say")`
2. Server plans: `next_steps: ["text_to_speech(...)", "memops:store_memory(...)"]`
3. Client executes both steps using visible tools

The reverse (memops bridging to speech-mcp) gives memory agents a voice.

### Video + OSC (davinci-resolve-mcp + osc-mcp)

```
davinci-resolve-mcp (10843)  ←──  osc-mcp (10767)
```

**Setup (in davinci-resolve-mcp/.env):**
```env
MCP_BRIDGE_URLS=http://127.0.0.1:10767/mcp
```

**Now visible:** `osc_send`, `osc_listen` alongside DaVinci timeline tools.

### Docker + FastSearch (docker-mcp + fastsearch-mcp)

```
docker-mcp (10807)  ←──  fastsearch-mcp (10845)
```

**Setup (in docker-mcp/.env):**
```env
MCP_BRIDGE_URLS=http://127.0.0.1:10845/mcp
```

### AI Watcher Hub (aiwatcher-mcp)

```
aiwatcher-mcp (10946)  ←──  speech-mcp, email-mcp, calibre-mcp
```

**Setup (in aiwatcher-mcp/.env):**
```env
MCP_BRIDGE_URLS=http://127.0.0.1:10909/mcp,http://127.0.0.1:10813/mcp,http://127.0.0.1:10721/mcp
```

### Home Assistant + speech-mcp

```
home-assistant-mcp (10782)  ←──  speech-mcp (10909)
```

**Setup (in home-assistant-mcp/.env):**
```env
MCP_BRIDGE_URLS=http://127.0.0.1:10909/mcp
```

### Federation Hub (mcp-federation-hub)

The hub can bridge every server. Add `NamespaceTransform` for clean prefixes:

```python
from fastmcp.providers import ProxyProvider
from fastmcp.transforms import NamespaceTransform

for url in bridge_urls:
    name = url.split("/")[2].split(":")[0]
    mcp.add_provider(
        ProxyProvider(url=url),
        transforms=[NamespaceTransform(prefix=name)]
    )
```

---

## 6. Multi-Hop Visibility

Bridges chain for **visibility**, not execution:

```
Client  →  hub (bridged to speech)  →  speech (bridged to memops)
```

Client sees hub's tools + speech's tools. But client does **not** see memops' tools through the double bridge — `ProxyProvider` only exposes one level. Each server must be explicitly bridged to the entry point.

---

## 7. Verifying a Bridge

```powershell
Invoke-RestMethod http://127.0.0.1:10909/api/capabilities
# → features.mcp_bridge: true
# → bridges: ["http://127.0.0.1:10704/mcp"]
```

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Handshake fails at startup (3.4+) | Upstream unreachable, wrong path, or auth | Verify URL ends in `/mcp`; target server running; check OAuth |
| Tools not appearing (pre-3.4 or bypassed init) | Target server not running | Verify target MCP endpoint is reachable |
| `ECONNREFUSED` | Wrong port or server down | `Get-NetTCPConnection -LocalPort <port>` |
| Bridge added, tools missing | URL doesn't end in `/mcp` or MCP route not mounted | Check `app.mount("/mcp", ...)` on target |
| Slow responses | Target server timing out | Each bridge adds ~50-100ms latency |
| stdio host, HTTP server elsewhere | Host only supports stdio commands | `uvx fastmcp-remote http://127.0.0.1:<port>/mcp` — see [3.4-features.md](3.4-features.md) |

---

## 9. Reference

- Reusable module: `mcp-central-docs\standards\rules\mcp_bridge.py`
- `setup_mcp_bridge(mcp, logger)` — one-call retrofitting
- `probe_bridges(bridges, logger)` — startup check
- `add_bridge_to_capabilities(bridges)` — capabilities fragment
