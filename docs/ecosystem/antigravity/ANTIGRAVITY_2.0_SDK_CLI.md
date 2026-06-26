# Antigravity 2.0 — SDK & CLI (May 2026 Analysis)

**Analyzed:** 2026-05-19
**Sources:** `github.com/google-antigravity/antigravity-sdk-python`, `github.com/google-antigravity/antigravity-cli`
**Status:** Alpha (v0.1.0 SDK, CLI unreleased)

---

## What Changed in 2.0

Antigravity split into three products:

| Product | Type | Open Source | Status |
|---|---|---|---|
| **Antigravity IDE** | GUI (VS Code fork) | No | Stable (since Dec 2025) |
| **Antigravity SDK** (`google-antigravity`) | Python library | Apache 2.0 | Alpha v0.1.0 |
| **Antigravity CLI** (`antigravity-cli`) | Terminal TUI | No (placeholder repo) | Unreleased |

The SDK and CLI share a core agent engine — same agent loop, same tool set, same policies. The IDE is a separate product with its own engine.

---

## Antigravity SDK (Python)

### What It Is

A Python SDK for building AI coding agents locally, powered by Gemini. Thin orchestration layer over a **compiled Go binary** (`localharness`) that runs the actual agentic loop.

```
pip install google-antigravity
# Installs: Python SDK (~200 KB) + Go harness binary (~15 MB platform-specific)
```

### Architecture (3 Layers)

| Layer | Class | Role |
|---|---|---|
| **Layer 1 — Simplified** | `Agent` | `async with Agent(config) as agent:` — full lifecycle, tool wiring, hook registration, binary discovery |
| **Layer 2 — Session** | `Conversation`, `ChatResponse`, `Step`, `ToolCall` | Stateful session with history, turn tracking, streaming, compaction |
| **Layer 3 — Adapter** | `Connection`, `ConnectionStrategy`, `LocalConnection` | WebSocket + protobuf transport to Go harness. Strategy-per-backend pattern |

**Critical detail**: The Python code is pure orchestration. The agent's thinking loop, model calls, context management, subagent spawning — all run in the **closed-source Go binary**. Python serializes prompts as JSON/protobuf over WebSocket, deserializes step updates, dispatches tool calls, and enforces hooks/policies.

### Dependency Chain

```
google-genai>=1.0    # Gemini API client
mcp>=1.0             # MCP Python SDK (for MCP server connections)
pydantic>=2.0        # Type system (all public types are Pydantic v2)
uvicorn>=0.46        # Internal (likely for remote connection modes)
websockets>=12.0     # Transport to Go harness
protobuf>=4.25       # Wire protocol between Python ↔ Go
```

### Feature Depth

#### Built-in Tools (11)
`list_directory`, `search_directory`, `find_file`, `view_file`, `create_file`, `edit_file`, `run_command`, `ask_question`, `start_subagent`, `generate_image`, `finish`

Read-only by default. Write tools require explicit `CapabilitiesConfig()` opt-in.

#### Streaming
```python
# Zero-boilerplate text tokens
async for token in response: ...     # str deltas

# Typed substreams — all share one buffer, all independently cursorable
async for thought in response.thoughts: ...   # reasoning deltas
async for call in response.tool_calls: ...     # typed ToolCall objects
```

#### Policy System (Priority-Bucketed)

Six priority levels, evaluated high-to-low with short-circuit:

```
Specific Deny > Specific Ask > Specific Allow >
Wildcard Deny > Wildcard Ask > Wildcard Allow
```

Built-in factory functions:
- `deny_all()` / `allow_all()` — blanket policies
- `deny(tool, when=predicate)` — conditional deny (e.g., deny `run_command` when args contain `rm -rf`)
- `ask_user(tool, handler=fn)` — interactive approval
- `confirm_run_command()` — default: deny `run_command`, allow everything else
- `workspace_only(paths)` — restrict file tools to specific directories
- `safe_defaults(handler)` — allow read-only tools, ask for writes

#### Hooks (8 Types)
`pre_turn`, `post_turn`, `pre_tool_call_decide`, `post_tool_call`, `on_tool_error`, `on_compaction`, `on_interaction`, `on_session_start`, `on_session_end`

#### MCP Integration
Native support for three MCP transport types:
```python
McpStdioServer(command="npx", args=["my-mcp-server"])
McpSseServer(url="http://localhost:10996/sse")
McpStreamableHttpServer(url="http://localhost:10996/mcp")
```
MCP tools are merged into the agent's tool set automatically. The agent (running in the Go harness) can call fleet MCP servers as tools.

#### Subagents
Built-in `start_subagent` tool. Subagent trajectories are tracked independently, results surfaced to the parent via `TrajectoryStateUpdate`. Post-tool-call hooks fire on subagent completion with the subagent's final response.

#### Triggers
```python
triggers=[every(60, check_status)]        # Periodic
triggers=[on_file_change(watch_dir)]      # File watcher
```
Delivery modes: `SEND_IMMEDIATELY` (non-blocking push) or `WAIT_IDLE` (queue for next idle).

#### Multimodal
`Image`, `Document`, `Audio`, `Video` content classes with `from_file()` auto-resolution. In-memory bytes also supported. Mixed prompt lists: `[str, Image, str, Document]`.

#### Custom Tools
```python
def get_weather(city: str) -> str: ...
config = LocalAgentConfig(tools=[get_weather])
```
`ToolContext` injection for tools that need session access. Sync tools auto-wrapped in threads. Schema extracted via `google-genai` `FunctionDeclaration`.

#### Structured Output
```python
config = LocalAgentConfig(response_schema=MyPydanticModel)
result = await response.structured_output()
```
JSON schema, dict, or Pydantic model fed to the `finish` tool.

#### Compaction
Configurable token threshold (`compaction_threshold`). Context window auto-compacted by the Go harness.

#### Session Resume
`conversation_id` exposed after first message exchange. Pass to `SessionConfig` to resume.

---

## Antigravity CLI

### What It Is

Terminal agent (TUI) — think `opencode` or `Claude Code`. Shares the same core agent engine as the SDK.

```
curl -fsSL https://antigravity.google/cli/install.sh | bash   # macOS/Linux
irm https://antigravity.google/cli/install.ps1 | iex           # Windows
```

### Key Details

- **Not open-source** — the GitHub repo (`antigravity-cli`) is a placeholder: README + CHANGELOG + demo GIF. The binary is distributed via Google's infrastructure.
- **TUI, keyboard-first**, optimized for SSH/remote sessions
- **Shares settings bidirectionally** with the Antigravity 2.0 GUI
- **Sessions exportable** to the full GUI
- Authentication: system keyring → browser OAuth fallback → SSH prints URL for local login

### CLI vs IDE

| | CLI | IDE (GUI) |
|---|---|---|
| Interface | Terminal TUI | VS Code fork |
| Focus | Speed, keyboard, low overhead | Comprehensiveness, visual orchestration |
| Target | SSH/remote, keyboard-first | Local workspaces, heavy orchestration |
| Agent Engine | Shared core engine | Separate (IDE-specific) |

---

## Fleet Utility Assessment

### What Works

1. **MCP bridge direction works**: AG SDK/CLI can connect to fleet MCP servers (`McpStdioServer`, `McpSseServer`, `McpStreamableHttpServer`). An AG agent could use `filesystem-mcp`, `git-github-mcp`, `database-operations-mcp`, etc. as tools.

2. **Cross-validation agent**: AG CLI could serve as a "second opinion" coding agent alongside opencode. Different model (Gemini), different agent loop, independent verification.

3. **Embeddable library**: AG SDK is a Python library, not just a CLI. Could be embedded into fleet tools that need Gemini-powered coding capabilities.

4. **Skills ecosystem**: AG SDK supports `skills_paths` — skills loaded from filesystem. Fleet has 171+ Claude skills. Format compatibility unknown but worth investigating.

### What Doesn't Work

1. **Closed-source Go harness**: The agentic loop is a proprietary binary blob (`localharness`) distributed in the wheel. Violates fleet SOTA principle: *"Self-own the critical path."* The agent loop is the critical path.

2. **Google-only auth**: Requires Gemini API key (`GEMINI_API_KEY` or `gemini_config.api_key`). No support for other providers, no local model support in the Go harness.

3. **Telemetry**: CLI ToS states Google collects interaction data. Opt-out available but default is collection.

4. **Early alpha**: v0.1.0, single release tag, API surface likely unstable.

5. **Redundant with opencode**: Fleet already has opencode — fully open (MIT), multi-provider (Claude, Gemini, DeepSeek, Ollama), no proprietary runtime. Adding another coding agent framework creates fragmentation without clear ROI.

6. **Go harness is a black box**: You can't inspect what the agent loop does, how it manages context, what prompts it uses, what telemetry it sends.

### Verdict

| Factor | Score | Notes |
|---|---|---|
| Documentation | 7/10 | Well-documented README + component docs. No API reference. |
| Architecture | 8/10 | Clean 3-layer design, good separation of concerns, elegant streaming |
| Safety defaults | 9/10 | Read-only by default, explicit write opt-in, priority-bucketed policies |
| Openness | 3/10 | SDK code is open (Apache 2.0). Go harness is closed binary blob. CLI is fully closed. |
| Fleet compatibility | 4/10 | MCP bridge works. Google-only auth. Proprietary runtime. Redundant with opencode. |
| Maturity | 3/10 | Alpha v0.1.0. 1 release. 208 commits. API will change. |

**Bottom line for fleet**: Document and monitor. Do not integrate into fleet workflows. The closed-source Go harness is an unacceptable critical-path dependency. Fleet is well-served by opencode (fully open, multi-provider) as the primary coding agent. Antigravity IDE remains valuable as a GUI MCP client. AG SDK's primary fleet value is as a reference architecture for agent SDK design patterns — policy bucketing, concurrent-safe streaming, and MCP bridge integration are worth studying.

### If Integration Were Desired (Future)

```python
# Hypothetical: AG agent using fleet MCP servers
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.types import McpStdioServer, McpSseServer

config = LocalAgentConfig(
    api_key=os.environ["GEMINI_API_KEY"],
    mcp_servers=[
        McpSseServer(url="http://127.0.0.1:10742/sse"),   # filesystem-mcp
        McpSseServer(url="http://127.0.0.1:10702/sse"),   # git-github-mcp
        McpSseServer(url="http://127.0.0.1:10708/sse"),   # database-operations-mcp
    ],
    skills_paths=[r"C:\Users\sandr\.gemini\antigravity\skills"],
    policies=[policy.allow_all()],
)
async with Agent(config) as agent:
    response = await agent.chat("Analyze the fleet repos and report status.")
    print(await response.text())
```

This works technically but offers no advantage over opencode doing the same thing with an open runtime.

---

## Related Docs

- [Antigravity IDE (ecosystem overview)](README.md)
- [Antigravity IDE (detailed)](../../not-mcp-related/google-ecosystem/antigravity/README.md)
- [Antigravity IDE — MCP Client Reference](../../integrations/antigravity-ide/README.md)
- [Third-Party Antigravity Ecosystem](THIRD_PARTY_ECOSYSTEM.md)
- [Agentic IDE Comparison](../../not-mcp-related/development/AGENTIC_IDE_COMPARISON.md)
- [Fleet Agent MCP (Lumen)](../../projects/fleet-agent-mcp.md)
- [Local LLM Standards (Qwen 3.6 + Ollama)](../../integrations/local-llm/qwen3.6-agentic-coding.md)
