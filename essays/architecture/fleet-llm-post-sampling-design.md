# Fleet LLM — Post-Sampling Architecture (2026-08)

**Context**: `ctx.sample()` is removed in FastMCP 4 / MCP 2026-07-28 spec. 13+ fleet servers depend on it. We must migrate to server-side LLM.

**Premise**: We already have an RTX 4090 running Ollama 24/7. We already have `learnbot-mcp` and `advanced-memory-mcp` doing server-side LLM calls. We just need one shared library instead of three inconsistent implementations.

---

## 1. The Migration Target

The goal is a **drop-in replacement for ctx.sample()** that calls Ollama directly:

```python
# BEFORE (dead in FastMCP 4):
@mcp.tool()
async def analyze_paper(paper_id: str, ctx: Context) -> dict:
    text = fetch_text(paper_id)
    result = await ctx.sample(f"Analyze: {text}")
    return {"analysis": result}

# AFTER (FastMCP 4 + fleet-llm):
from fleet_llm import llm

@mcp.tool()
async def analyze_paper(paper_id: str) -> dict:
    text = fetch_text(paper_id)
    result = await llm.ask(f"Analyze: {text}")
    return {"analysis": result}
```

One import. One rename. `ctx` parameter removed. Everything else stays the same.

---

## 2. Package: `fleet-llm`

A shared pip-installable package at `D:\Dev\repos\fleet-llm\`. Every fleet server adds it as a dependency.

### 2.1 API Surface

```python
from fleet_llm import LLM

llm = LLM()  # auto-detects Ollama on :11434, LM Studio on :1234, vLLM on :8000

# --- TIER 1: Simple inference (replaces ctx.sample string prompt) ---
result: str = await llm.ask(
    prompt="Summarize this paper",
    system="You are a research assistant. Be concise.",  # optional
    model="qwen3:14b",                                     # optional override
    max_tokens=2000,                                       # optional
    temperature=0.7,                                       # optional
)

# --- TIER 2: Structured output ---
result: dict = await llm.ask_json(
    prompt="Extract title, authors, year from this text",
    schema={"title": str, "authors": list[str], "year": int},
)

# --- TIER 3: Agentic tool calling (replaces ctx.sample with SEP-1577 tools) ---
result: str = await llm.agent(
    goal="Research quantum computing advances",
    tools=[search_papers, fetch_text, compare_papers],  # actual Python functions
    max_rounds=5,                                         # safety limit
    model="qwen3:14b",                                    # needs a smart model
)

# --- TIER 4: Streaming (for chat pages) ---
async for chunk in llm.stream("Tell me about quantum computing"):
    yield chunk

# --- UTILITY ---
status = await llm.health()
# {"ollama": {"status": "ok", "models": ["qwen3:14b", "llama3.2:3b"]},
#  "lmstudio": {"status": "not_found"},
#  "vllm": {"status": "not_found"}}

llm.set_default_model("qwen3:14b")
llm.set_default_provider("ollama")
```

### 2.2 Directory Structure

```
fleet-llm/
├── pyproject.toml
├── README.md
├── src/fleet_llm/
│   ├── __init__.py              # LLM class, module-level singleton
│   ├── client.py                # ask(), ask_json(), stream()
│   ├── agent.py                 # agent() — tool-calling loop
│   ├── providers/
│   │   ├── base.py              # BaseProvider ABC
│   │   ├── ollama.py            # Ollama native API (/api/generate, /api/chat)
│   │   └── openai_compat.py     # OpenAI-compatible (/v1/chat/completions)
│   ├── cache.py                 # LRU prompt/response cache
│   ├── health.py                # Auto-detection, health probes, circuit breaker
│   └── config.py                # Env vars, model registry, defaults
└── tests/
    ├── test_client.py
    ├── test_agent.py
    └── test_providers.py
```

### 2.3 Dependencies

```toml
[project]
name = "fleet-llm"
version = "0.1.0"
dependencies = [
    "httpx>=0.28",        # HTTP client (or httpx2 when fleet migrates)
    "pydantic>=2.12",     # Structured output
    "cachetools>=5.5",    # LRU cache for prompts
]
```

Minimal. No `openai` SDK, no `anthropic` SDK. Just `httpx` + `pydantic`. The Ollama REST API and OpenAI-compatible APIs are both trivial HTTP calls.

---

## 3. Provider Architecture

### 3.1 Auto-Detection

On `LLM()` construction, probe in priority order:

```python
PROBE_ORDER = [
    ("ollama",      "http://localhost:11434", "/api/tags"),
    ("lmstudio",    "http://localhost:1234",  "/v1/models"),
    ("vllm",        "http://localhost:8000",  "/v1/models"),
]
```

First to respond 200 with valid JSON wins. Result cached with 30s TTL.

If nothing responds: `llm.ask()` raises `LLMNotAvailable("No LLM provider detected. Start Ollama.")`.

### 3.2 Ollama Provider (Primary)

Uses Ollama's native API — not the OpenAI compatibility layer. Two endpoints:

- **`/api/generate`** — simple completion, no chat template needed. Best for `llm.ask()`.
- **`/api/chat`** — chat completion with tool calling. Used by `llm.agent()`.

```python
class OllamaProvider(BaseProvider):
    async def generate(self, prompt: str, system: str | None, model: str, **kwargs) -> str:
        payload = {"model": model, "prompt": prompt, "stream": False, **kwargs}
        if system:
            payload["system"] = system
        r = await self.client.post(f"{self.base_url}/api/generate", json=payload)
        return r.json()["response"]

    async def chat(self, messages: list[dict], model: str, tools: list | None, **kwargs) -> dict:
        payload = {"model": model, "messages": messages, "stream": False, **kwargs}
        if tools:
            payload["tools"] = [self._tool_to_ollama(t) for t in tools]
        r = await self.client.post(f"{self.base_url}/api/chat", json=payload)
        return r.json()["message"]

    async def list_models(self) -> list[str]:
        r = await self.client.get(f"{self.base_url}/api/tags")
        return [m["name"] for m in r.json().get("models", [])]
```

### 3.3 OpenAI-Compatible Provider (LM Studio, vLLM, cloud fallback)

Single provider class parameterized by `base_url`:

```python
class OpenAICompatProvider(BaseProvider):
    async def chat(self, messages, model, tools=None, **kwargs):
        payload = {"model": model, "messages": messages, **kwargs}
        if tools:
            payload["tools"] = [self._tool_to_openai(t) for t in tools]
        r = await self.client.post(f"{self.base_url}/v1/chat/completions", json=payload)
        choice = r.json()["choices"][0]["message"]
        # Return tool_calls if present, content if not
        return {
            "content": choice.get("content", ""),
            "tool_calls": choice.get("tool_calls"),
        }
```

### 3.4 Provider Interface (ABC)

```python
class BaseProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system: str | None, model: str, **kwargs) -> str: ...

    @abstractmethod
    async def chat(self, messages: list[dict], model: str, tools: list | None, **kwargs) -> dict: ...

    @abstractmethod
    async def list_models(self) -> list[str]: ...

    async def health(self) -> bool:
        """Return True if provider is reachable."""
```

---

## 4. Agentic Tool Calling (The ctx.sample SEP-1577 Replacement)

This is the hardest feature to replace. `ctx.sample(tools=[fn1, fn2], result_type=Model)` let the client's LLM autonomously call tools in a loop. We need to implement this loop ourselves.

### 4.1 The Loop

```python
async def agent(self, goal: str, tools: list[Callable], max_rounds: int = 5,
                model: str | None = None, system: str | None = None) -> str:
    """
    Autonomous agentic loop.
    Replaces: result = await ctx.sample(messages, tools=[...])

    The LLM sees tool definitions, decides which to call, we execute the tool,
    feed the result back, LLM decides next step. Repeat until LLM returns a
    final answer or we hit max_rounds.
    """
    provider = self._get_provider()
    model = model or self.default_model

    messages = [{"role": "system", "content": system or "You are a helpful assistant."},
                {"role": "user", "content": goal}]

    tool_map = {fn.__name__: fn for fn in tools}
    tool_schemas = [self._function_to_schema(fn) for fn in tools]

    for round_num in range(max_rounds):
        response = await provider.chat(messages, model, tools=tool_schemas)

        if response["content"] and not response.get("tool_calls"):
            return response["content"]  # LLM gave final answer

        if response.get("tool_calls"):
            messages.append({"role": "assistant", "content": response.get("content", ""),
                            "tool_calls": response["tool_calls"]})

            for tc in response["tool_calls"]:
                func = tool_map.get(tc["function"]["name"])
                if func:
                    args = json.loads(tc["function"]["arguments"])
                    result = await func(**args) if asyncio.iscoroutinefunction(func) else func(**args)
                    messages.append({"role": "tool", "content": json.dumps(result),
                                    "tool_call_id": tc["id"]})
                else:
                    messages.append({"role": "tool", "content": f"Unknown tool: {tc['function']['name']}",
                                    "tool_call_id": tc["id"]})

    return "Agent reached maximum rounds without final answer."
```

### 4.2 Safety Guards

```python
MAX_ROUNDS = 5          # hard cap — prevent infinite loops
MAX_TOKENS_PER_ROUND = 4096
TOKEN_BUDGET_PER_CALL = 32768  # total across all rounds
CACHE_TTL = 300         # 5 min cache for identical prompts
CIRCUIT_BREAKER = 3     # 3 failures → 60s cooldown
```

### 4.3 Tool Schema Conversion

Convert Python function signatures to OpenAI/Ollama tool schemas:

```python
def _function_to_schema(self, fn: Callable) -> dict:
    """Convert a Python function to an OpenAI tool schema using type hints."""
    sig = inspect.signature(fn)
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls", "ctx"):
            continue
        annotation = param.annotation
        if annotation is inspect.Parameter.empty:
            annotation = str
        json_type = self._python_to_json_type(annotation)
        if param.default is inspect.Parameter.empty:
            required.append(name)
        # Extract Field description from Annotated types
        desc = self._extract_field_description(param)
        properties[name] = {"type": json_type, "description": desc}

    return {
        "type": "function",
        "function": {
            "name": fn.__name__,
            "description": fn.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            }
        }
    }
```

---

## 5. Caching

Identical prompts should not re-run the LLM. LRU cache keyed on `(prompt, system, model, temperature)`:

```python
from cachetools import LRUCache
import hashlib

class PromptCache:
    def __init__(self, maxsize: int = 256, ttl: int = 300):
        self.cache = LRUCache(maxsize)
        self.ttl = ttl

    def _key(self, prompt: str, system: str | None, model: str, **kwargs) -> str:
        raw = f"{prompt}|{system}|{model}|{kwargs}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, prompt, system, model, **kwargs) -> str | None:
        key = self._key(prompt, system, model, **kwargs)
        entry = self.cache.get(key)
        if entry and time.time() - entry["ts"] < self.ttl:
            return entry["response"]
        return None

    def set(self, prompt, system, model, response, **kwargs):
        key = self._key(prompt, system, model, **kwargs)
        self.cache[key] = {"response": response, "ts": time.time()}
```

---

## 6. Configuration

### 6.1 Env Vars

```bash
# .env (repo root)
FLEET_LLM_PROVIDER=ollama          # ollama | lmstudio | vllm | openai
FLEET_LLM_BASE_URL=http://localhost:11434
FLEET_LLM_DEFAULT_MODEL=qwen3:14b
FLEET_LLM_MAX_TOKENS=4096
FLEET_LLM_TEMPERATURE=0.7
FLEET_LLM_CACHE_TTL=300
FLEET_LLM_AGENT_MAX_ROUNDS=5
```

### 6.2 Per-Tool Model Overrides

Some tools need smart models (agentic reasoning), some need fast models (summarization):

```python
from fleet_llm import llm, use_model

@mcp.tool()
@use_model("qwen3:14b")       # big model for reasoning
async def agentic_research(topic: str) -> dict:
    return await llm.agent(f"Research: {topic}", tools=[...])

@mcp.tool()
@use_model("llama3.2:3b")     # small model for fast classification
async def classify_intent(text: str) -> str:
    return await llm.ask(f"Classify: {text}")
```

### 6.3 Per-Server Overrides

Each fleet server can override the global config:

```python
# arxiv-mcp: needs a big model for paper analysis
from fleet_llm import LLM
llm = LLM(default_model="qwen3:14b", max_tokens=4096)

# quicknotes-mcp: needs a fast model for summaries
from fleet_llm import LLM
llm = LLM(default_model="llama3.2:3b", temperature=0.0)
```

---

## 7. Migration Path Per Fleet Server

### 7.1 Tier 1 — Simple string calls (mechanical rename)

```python
# Find:  result = await ctx.sample("prompt")
#        result = await ctx.sample(f"prompt {var}")
#        result = await ctx.sample(messages=[...])
#        result = await ctx.sample(messages=[...], max_tokens=N)
#
# Replace with:
#        result = await llm.ask("prompt")
#        result = await llm.ask(f"prompt {var}")
#        result = await llm.chat(messages=[...])
#        result = await llm.chat(messages=[...], max_tokens=N)
```

Affected: alexa-mcp, beyondcompare-mcp, home-assistant-mcp, yahboom-mcp — 1-2 calls each. 5 minutes per server.

### 7.2 Tier 2 — SamplingMessage objects (medium)

```python
# Find: ctx.sample(messages=[SamplingMessage(role="user", content=TextContent(...))])
#       ctx.sample(system_prompt=..., messages=...)
#
# Replace with:
#       llm.chat(messages=[{"role": "user", "content": "..."}])
#       llm.chat(messages, system="...")
```

Affected: arxiv-mcp, calibre-mcp, autohotkey-mcp. ~30 minutes per server.

### 7.3 Tier 3 — Agentic tool calling (hard)

```python
# Find: ctx.sample(messages=[...], tools=[fn1, fn2], result_type=Model)
#       ctx.sample_step(...)
#
# Replace with:
#       llm.agent(goal="...", tools=[fn1, fn2])
```

Affected: advanced-memory-mcp, blender-mcp, arr-mcp. ~2 hours per server. Requires implementing the tool-calling loop (see §4).

### 7.4 Tier 4 — Sampling handlers (full rewrite)

```python
# Find: FastMCP(sampling_handler=MyHandler())
#       FastMCP(sampling_handler_behavior="fallback")
#       SamplingTool
#
# Replacement: Remove entirely. Replace with llm.ask()/llm.agent() in tool code.
```

Affected: discord-mcp, arr-mcp. Full redesign required.

---

## 8. Migration Script

A script that automates Tier 1-2 migrations:

```python
# scripts/migrate-to-fleet-llm.py
# Scans a fleet repo and rewrites ctx.sample() → llm.ask() / llm.chat()

MIGRATIONS = [
    # ctx.sample("string") → llm.ask("string")
    (r'await ctx\.sample\("([^"]+)"\)', r'await llm.ask("\1")'),
    # ctx.sample(f"...") → llm.ask(f"...")
    (r'await ctx\.sample\(f(".*?")\)', r'await llm.ask(f\1)'),
    # ctx.sample(messages=[...]) → llm.chat(messages=[...])
    (r'await ctx\.sample\((.*?messages=.*?)\)', r'await llm.chat(\1)'),
    # Remove ctx: Context from function signatures
    (r',?\s*ctx:\s*Context\s*=\s*None', ''),
]

# Also: add "from fleet_llm import llm" to imports
# Also: remove SamplingTool / sampling_handler references
```

---

## 9. Advantages Over ctx.sample()

Once migrated, the fleet gains capabilities that `ctx.sample()` could never provide:

| Capability | ctx.sample() | fleet-llm |
|-----------|-------------|-----------|
| **Works with any client** | Only clients that implement sampling | Every client — stdio, HTTP, Tauri |
| **Model control** | Client chooses model (may be wrong) | Server chooses the right model per tool |
| **Prompt caching** | None — every call fresh | LRU cache — identical prompts instant |
| **Token budgeting** | Client pays, server can't control | Server budgets per tool, per call |
| **Streaming** | Not supported | Native async streaming |
| **Tool calling** | SEP-1577 (few clients implement) | Built-in — works with any Ollama model |
| **Structured output** | Not supported | JSON mode with schema validation |
| **Provider fallback** | None | Ollama → LM Studio → cloud |
| **Health monitoring** | None | Circuit breaker, model listing |
| **Consistent behavior** | Depends on client implementation | Identical across all clients |
| **Offline capable** | No (needs client LLM) | Yes (local Ollama) |
| **No protocol dependency** | Depends on sampling extension | Plain HTTP — works forever |

---

## 10. Rollout Plan

| Phase | Servers | Effort | Timeline |
|-------|---------|--------|----------|
| **Phase 0** | Build `fleet-llm` package | 2-3 days | Before any server migration |
| **Phase 1** | learnbot-mcp (already server-side), quicknotes-mcp, tiny-* tools | 1h each | Pilot — validate the package |
| **Phase 2** | alexa-mcp, beyondcompare-mcp, bumi-mcp, home-assistant-mcp, yahboom-mcp | 5m each (Tier 1) | Mechanical rename wave |
| **Phase 3** | arxiv-mcp, calibre-mcp, autohotkey-mcp, avatar-mcp | 30m each (Tier 2) | SamplingMessage → dict conversion |
| **Phase 4** | advanced-memory-mcp, blender-mcp, arr-mcp | 2h each (Tier 3) | Agentic loop implementation |
| **Phase 5** | discord-mcp | 3h (Tier 4) | Sampling handler redesign |

Total: ~5 days to build the package, then ~12 hours across the fleet, spread over 2-3 weeks.

---

## 11. Cost Analysis — The Real Problem with Cloud APIs

### The $20 Problem

`ctx.sample()` routed through the connected client's LLM. For Claude Desktop users with a $20/month Claude Pro subscription, this meant **frontier model inference at zero marginal cost**. Opus 5, included with weekly limits, free.

Direct Anthropic API pricing for the same model: **$15/M input, $75/M output**. One fleet epistemic analysis call (8K in, 2K out): $0.27. Agentic workflow (5 rounds): $1-3. Run it 20 times a day: $600+/month. That's a 30x cost increase for the same capability.

Anthropic burned their bridge with this deprecation. The subscription model was the deal — `ctx.sample()` was the mechanism. Without it, their direct API pricing is absurd for agentic workloads.

### DeepSeek V4 Flash — The Escape Hatch

Pricing as of 2026-07-31 (**STALE** — see `llms/models/deepseek/CONTEXT_CACHING.md` for the confirmed 2026-08-30 rate sheet; flash is now $0.007/$0.22/$0.66 off-peak, 2x peak):

| Model | 1M Input | 1M Output | 1M Input (Cache Hit) |
|-------|---------|-----------|----------------------|
| **DeepSeek V4 Flash** | $0.14 | $0.28 | $0.0028 |
| DeepSeek V4 Pro | $0.435 | $0.87 | $0.003625 |
| Anthropic Opus 4.8 | $15.00 | $75.00 | — |
| Anthropic Sonnet 4.6 | $3.00 | $15.00 | — |

Fleet workload costs:

| Workload | Tokens | Anthropic Opus | Anthropic Sonnet | DeepSeek V4 Flash |
|----------|--------|---------------|-----------------|-------------------|
| Single analysis (epistemic) | 8K in, 2K out | $0.27 | $0.054 | **$0.00168** |
| Agentic workflow (5 rounds) | 40K in, 10K out | $1.35 | $0.27 | **$0.0084** |
| 100 analyses/day | — | $27/day | $5.40/day | **$0.17/day** |
| 30-day month | — | $810/mo | $162/mo | **$5/mo** |

**DeepSeek V4 Flash is 160x cheaper than Anthropic Opus for fleet workloads.** At $5/month for heavy usage, it's actually cheaper than the Claude Pro subscription was.

And V4 Flash has everything the fleet needs:
- Thinking mode (for epistemic analysis, agentic reasoning)
- Tool calling (replaces SEP-1577 `ctx.sample(tools=[...])`)
- JSON output mode (structured returns)
- 1M token context window
- 384K max output
- **Context caching at 1/50th the price** — repeated prompts about similar papers become nearly free

### The Three-Tier Model Strategy (Revised)

```
cpu-tier:  llama3.2:3b on CPU → classification, extraction, trivial tasks → FREE
gpu-tier:  qwen3:14b on 4090 → mid-complexity analysis, synthesis → FREE (electricity)
cloud-tier: DeepSeek V4 Flash → epistemic analysis, agentic reasoning → practically FREE
```

With revised pricing, the cloud tier doesn't need a "use sparingly" warning. At $0.00168 per paper analysis, you can run it 594 times before hitting ONE DOLLAR. The entire monthly fleet cloud bill will be under $10.

```python
from fleet_llm import llm, Tier

llm = LLM(
    cpu_model="llama3.2:3b",
    gpu_model="qwen3:14b",
    cloud_model="deepseek-v4-flash",
    cloud_api_key=os.environ["DEEPSEEK_API_KEY"],
)

@mcp.tool()
async def classify(text: str) -> str:
    return await llm.ask(text, tier=Tier.CPU)        # free, instant

@mcp.tool()
async def synthesize(topics: list) -> str:
    return await llm.ask(topics, tier=Tier.GPU)       # free, fast

@mcp.tool()
async def deep_epistemic_analysis(paper_text: str) -> dict:
    return await llm.agent(paper_text, tier=Tier.CLOUD)  # $0.00168
```

### The Poison Pill

Anthropic's core maintainers deprecated the very feature that made their subscription model valuable for power users. `ctx.sample()` was the bridge between Claude Pro subscriptions ($20/mo) and MCP server ecosystems. Kill the bridge, and server authors who previously used Anthropic via subscription now face a choice between:

1. Pay Anthropic API rates (30-160x more expensive than alternatives)
2. Switch to DeepSeek V4 Flash (equally capable, 160x cheaper)

The fleet chooses option 2. Anthropic's models were never the product — the $20 subscription including them was. Without the subscription bridge, there is zero reason to pay Anthropic's API rates.

---

## 12. The July 31 Bombshell

DeepSeek released **V4-Flash-0731** yesterday (2026-07-31). Same model architecture and size as the preview — only re-post-trained. But the agent benchmarks are staggering:

| Task | V4-Flash-Preview | V4-Flash-0731 | Change |
|------|-----------------|---------------|--------|
| Terminal Bench 2.1 | — | 82.7 | New SOTA |
| NL2Repo | — | 54.2 | New SOTA |
| Cybergym | — | 76.7 | New SOTA |
| DeepSWE | — | 54.4 | New SOTA |
| Toolathlon verified | — | 70.3 | New SOTA |
| Agent Last Exam | — | 25.2 | New SOTA |

They explicitly state: *"Significantly enhanced agent capabilities, with benchmark results far exceeding V4-Pro-Preview."* The Flash model now beats the old Pro on agentic tasks.

And it costs the same: **$0.14/M input, $0.28/M output**. Still 160x cheaper than Anthropic Opus.

The update also ships **native Responses API** support, specifically adapted for Codex-style agents. This is tool-calling infrastructure built directly into the model API — not bolted on. Exactly what `llm.agent()` needs under the hood.

**V4-Pro official release "will follow soon."** At $0.435/M input, $0.87/M output — still 35x cheaper than Anthropic Opus for the rare cases where Flash isn't enough.

The timing is impeccable. Anthropic deprecates sampling on July 28. DeepSeek ships a model explicitly optimized for agentic tool calling on July 31.

---

## 13. What This Buys Us

The fleet becomes **protocol-independent and Anthropic-independent**. FastMCP 3, FastMCP 4, a future MCP 2028 spec — doesn't matter. `llm.ask()` calls Ollama or DeepSeek over plain HTTP. The MCP protocol can deprecate whatever it wants; our servers call the LLM directly and the protocol just routes tool calls and results.

The cost structure shifts from "$20/month subscription, free sampling" to "$0/month fixed, ~$5/month variable for cloud tier." Cheaper, faster, more capable, no single-vendor dependency.

This is the architectural move the core maintainers should have made: provide a reference LLM client in the framework instead of relying on a protocol extension that required bidirectional streams and client cooperation.

We're doing it ourselves.
