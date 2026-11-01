# DeepSeek V4 — Fleet Strategic Provider (2026-08)

**Context**: Anthropic deprecated `ctx.sample()` on July 28, severing the subscription bridge that let fleet servers use Claude Opus for free. Three days later, DeepSeek shipped a model purpose-built for agentic tool calling at 1/160th the price. This document formalizes DeepSeek as the fleet's primary cloud LLM.

> **⚠ PRICING CAVEAT (2026-08-14) — §3 numbers are STALE.** Effective **2026-08-16 16:00 UTC**, DeepSeek switches to peak/off-peak billing (peak: 01:00-04:00 + 06:00-10:00 UTC, all other hours off-peak at half price). New flash: **$0.22/$0.66 per 1M input-miss/output off-peak**, **$0.44/$1.32 peak** (cache-hit $0.007/$0.014). Old prices were $0.14/$0.28. Pro: $0.66/$1.98 off-peak, $1.32/$3.96 peak. Model names unchanged but now map to V4-Flash-**0731** / V4-Pro-**0813**.
> **Fleet impact**: §3's $10.20/mo Flash estimate becomes **~$18.50/mo off-peak** (~$37/mo if any job lands in peak). The cached <$1/mo math survives (~$0.28/mo — the cache-hit discount is the still-killer feature). **Scheduled jobs moved off-peak 2026-08-14**: aiwatcher digest → 04:30 UTC, morning_news → 05:00 UTC, alerts → 04:55 UTC, retention/sync_interests/currentai → 10:15-10:45 UTC (previously the digest ran 06:00 UTC, inside peak). Interval jobs (feed polls, distill) stay continuous — they run on the local Glimmer lane. Full analysis: [`llm-token-market-2026-08.md`](./llm-token-market-2026-08.md) §1.1-§1.2.

---

## 1. Timeline — How We Got Here

| Date | Event |
|------|-------|
| 2024-11-05 | MCP spec ships with `sampling/createMessage` — servers can borrow the client's LLM |
| 2025-01-20 | DeepSeek-R1 released, open-weights, MIT license. World notices. |
| 2025-04-01 | MCP core maintainer summit — decision to deprecate sampling, roots, logging (Discussion #2536) |
| 2025-05-15 | SEP-2577 merged — sampling formally deprecated. 12-month removal window begins. |
| 2026-04-24 | DeepSeek V4 Preview — V4-Pro (1.6T total, 49B active) and V4-Flash (284B total, 13B active). 1M context. V4-Pro rivaling top closed-source. |
| 2026-07-28 | MCP spec 2026-07-28 RC published. MCP Python SDK v2 stable. FastMCP 4.0.0b1 beta. `ctx.sample()` removed from server API. |
| 2026-07-31 | **DeepSeek V4-Flash-0731** — re-post-trained specifically for agentic capabilities. Benchmarks far exceed V4-Pro-Preview. Native Responses API for Codex. Same price. |

Three days between the nerf and the answer.

---

## 2. V4-Flash-0731 — What Shipped

### 2.1 The Model

```
DeepSeek-V4-Flash-0731
├── Architecture: 284B total / 13B active params (MoE)
├── Context: 1M tokens native
├── Max output: 384K tokens
├── Thinking mode: yes (default, with reasoning_effort control)
├── Non-thinking mode: yes
├── Tool calling: native (OpenAI format)
├── JSON output: structured mode
├── Context caching: disk-based KV cache at 1/50th cost
├── Responses API: native (Codex-optimized)
├── Anthropic API: compatible endpoint
└── License: open weights on HuggingFace
```

### 2.2 Agent Benchmarks

DeepSeek's own comparison — V4-Flash-0731 vs previous preview models:

| Benchmark | V4-Flash-Preview | V4-Flash-0731 | V4-Pro-Preview |
|-----------|-----------------|---------------|----------------|
| Terminal Bench 2.1 | — | **82.7** | — |
| NL2Repo | — | **54.2** | — |
| Cybergym | — | **76.7** | — |
| DeepSWE | — | **54.4** | — |
| Toolathlon verified | — | **70.3** | — |
| Agent Last Exam | — | **25.2** | — |
| Automation Bench (Public) | — | **25.1** | — |
| DSBench-FullStack | — | **68.7** | — |
| DSBench-Hard | — | **59.6** | — |

DeepSeek's own words: *"Significantly enhanced agent capabilities, with benchmark results far exceeding V4-Pro-Preview."*

The Flash — the cheap one — now beats the old Pro on agentic tasks. Same architecture, same size, pure post-training improvement. No model size increase. No price increase.

### 2.3 Responses API

V4-Flash-0731 natively supports the **Responses API** format, specifically adapted for Codex. This is the API pattern where the model receives a task, selects tools, calls them, receives results, and continues — the exact loop that `fleet-llm.agent()` implements (§4 of the fleet-llm design doc). Native support means the model was trained to do this, not prompted to do it.

### 2.4 What's Coming

> *"The official release of DeepSeek-V4-Pro will follow soon."*

V4-Pro at $0.435/M input, $0.87/M output — available on demand when Flash isn't enough. That's still 35x cheaper than Anthropic Opus.

---

## 3. Pricing — The Napkin Math That Kills Anthropic

| Model | 1M Input | 1M Output | Cache Hit (Input) | Context |
|-------|---------|-----------|-------------------|---------|
| **DeepSeek V4 Flash** | $0.14 | $0.28 | $0.0028 | 1M |
| DeepSeek V4 Pro | $0.435 | $0.87 | $0.003625 | 1M |
| Anthropic Sonnet 4.6 | $3.00 | $15.00 | $0.30 (prompt caching) | 200K |
| Anthropic Opus 4.8 | $15.00 | $75.00 | $1.50 (prompt caching) | 200K |
| OpenAI Luna | ~$2.00 | ~$10.00 | — | 256K |

### Fleet Workload Simulation

Conservative estimate — 100 epistemic analyses + 20 agentic workflows per day:

| Workload | Tokens/unit | Units/day | DS Flash | DS Pro | Sonnet | Opus |
|----------|-----------|-----------|----------|--------|--------|------|
| Epistemic analysis | 8K in, 2K out | 100 | $0.17 | $0.52 | $3.24 | $16.20 |
| Agentic workflow | 40K in, 10K out | 20 | $0.17 | $0.52 | $3.24 | $16.20 |
| **Daily total** | — | — | **$0.34** | **$1.04** | **$6.48** | **$32.40** |
| **Monthly total** | — | — | **$10.20** | **$31.20** | **$194.40** | **$972.00** |

With context caching (identical prompt prefixes, common in repeated paper analysis):

| Workload | DS Flash (cached) | Savings vs uncached |
|----------|-------------------|---------------------|
| Epistemic analysis | $0.0034 | 50x cheaper |
| Agentic workflow | $0.0034 | 50x cheaper |
| **Monthly total (cached)** | **$0.20** | **$10 saved** |

**The fleet's monthly cloud LLM bill: under $11 with DeepSeek V4 Flash. Under $1 with caching.**

Anthropic Opus for the same workload: **$972/month.** That's not a pricing difference — it's a different product category.

---

## 4. Anthropic's Self-Inflicted Wound

The MCP protocol's sampling feature was a **distribution channel** for Anthropic's subscriptions. Here's how it worked:

```
User buys Claude Pro ($20/mo)
  → User connects MCP servers to Claude Desktop
  → Server calls ctx.sample("reason about this paper")
  → Claude Desktop routes through user's subscription
  → Opus 5 does the reasoning
  → Server gets frontier-model intelligence, user pays $0 extra
```

This was Anthropic's moat. Every MCP server that used `ctx.sample()` was a reason to buy Claude Pro instead of a competitor's subscription. The feature created lock-in: switch clients, lose your MCP tools' intelligence.

SEP-2577 killed this channel. The core maintainer meeting explicitly decided sampling "has almost no adoption" and "overlaps with direct LLM integration." They were wrong on both counts:

1. **Adoption**: The fleet alone has 13+ sampling-dependent servers. The "low adoption" metric measures clients that *implement* sampling, not servers that *use* it. Every sampling call succeeds through Claude Desktop — the client that matters.

2. **Overlap**: Direct LLM integration is not an "overlap" — it's a completely different cost model. Server-side LLM calls cost real money at API rates. Client-side sampling costs $0 marginal through subscriptions. The "alternative" costs 30-160x more.

The result: Anthropic turned their most loyal power users (MCP server authors) into DeepSeek customers overnight. The subscription was the product. Sampling was the delivery mechanism. Deprecating the mechanism destroyed the product.

And they did it three days before DeepSeek shipped an agent-optimized model at 1/160th the price.

---

## 5. Open Weights — The Strategic Safety Net

DeepSeek V4 Flash is **open-weight** (MIT-like license on HuggingFace). 284B total / 13B active MoE. This matters:

```
Today:  API → deepseek-v4-flash ($0.14/M input)
Cloud outage:  API → deepseek-v4-flash via OpenRouter/Azure/...
DeepSeek unavailable:  Ollama → local quantized V4 Flash (if fits) or V4 Pro
DeepSeek ceases operations:  open weights → self-host, fine-tune, fork
```

Contrast with Anthropic: API only. No weights. No self-hosting. If their pricing changes or service degrades, you have zero alternatives. With open weights, you have infinity.

The 13B active parameter count matters specifically for local deployment. While 284B total weights won't fit on a 4090 (24GB VRAM), the 13B active subset with aggressive quantization might. And the weights are available for anyone to try.

---

## 6. Anthropic API Compatibility — Zero-Code Switch

DeepSeek V4 Flash supports **Anthropic API format** at `https://api.deepseek.com/anthropic`. This means any code written against the Anthropic SDK can switch to DeepSeek by changing two lines:

```python
# BEFORE (Anthropic)
import anthropic
client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# AFTER (DeepSeek, Anthropic API format)
import anthropic
client = anthropic.AsyncAnthropic(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/anthropic",
)
```

And it supports **OpenAI format** at `https://api.deepseek.com` — the format `fleet-llm` uses by default through `openai.AsyncOpenAI`. One API key. Two protocols. Zero code changes to switch between them.

---

## 7. Fleet Integration

### 7.1 Provider Configuration

```python
# Every fleet server's .env (or appdata .env for NSIS builds):
DEEPSEEK_API_KEY=sk-...
FLEET_LLM_CLOUD_PROVIDER=deepseek
FLEET_LLM_CLOUD_MODEL=deepseek-v4-flash
```

### 7.2 fleet-llm Provider

```python
# fleet_llm/providers/deepseek.py
class DeepSeekProvider(BaseProvider):
    """DeepSeek V4 Flash/Pro via OpenAI-compatible API."""

    def __init__(self, api_key: str, model: str = "deepseek-v4-flash"):
        self.client = openai.AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )
        self.model = model

    async def generate(self, prompt: str, system: str | None, model: str | None, **kwargs) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=model or self.model,
            messages=messages,
            stream=False,
            **kwargs,
        )
        return response.choices[0].message.content

    async def chat(self, messages: list[dict], model: str | None, tools: list | None, **kwargs) -> dict:
        payload = {
            "model": model or self.model,
            "messages": messages,
            "stream": False,
            **kwargs,
        }
        if tools:
            payload["tools"] = tools

        response = await self.client.chat.completions.create(**payload)
        choice = response.choices[0].message

        return {
            "content": choice.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in (choice.tool_calls or [])
            ],
        }

    # For the really hard problems:
    async def generate_pro(self, prompt: str, system: str | None = None, **kwargs) -> str:
        """Use deepseek-v4-pro for complex reasoning. Costs more, thinks harder."""
        return await self.generate(prompt, system, "deepseek-v4-pro", **kwargs)

    async def list_models(self) -> list[str]:
        return ["deepseek-v4-flash", "deepseek-v4-pro"]

    async def health(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False
```

### 7.3 Tier Assignment

```python
from fleet_llm import LLM, Tier

llm = LLM(
    # Tier 1 — CPU, free, fast
    cpu_model="llama3.2:3b",
    cpu_provider="ollama",

    # Tier 2 — GPU, free, medium
    gpu_model="qwen3:14b",
    gpu_provider="ollama",

    # Tier 3 — Cloud, $0.14/M, agentic SOTA
    cloud_model="deepseek-v4-flash",
    cloud_provider="deepseek",
    cloud_api_key=os.environ["DEEPSEEK_API_KEY"],
)

# Usage in tools:
@mcp.tool()
async def classify_intent(text: str) -> str:
    return await llm.ask(text, tier=Tier.CPU)        # llama3.2:3b, free

@mcp.tool()
async def summarize_paper(text: str) -> str:
    return await llm.ask(text, tier=Tier.GPU)        # qwen3:14b, free

@mcp.tool()
async def deep_epistemic_analysis(text: str) -> dict:
    return await llm.agent(text, tier=Tier.CLOUD,   # deepseek-v4-flash, $0.00168
                           tools=[search_papers, compare_methods])

@mcp.tool()
async def frontier_research_plan(topic: str) -> dict:
    return await llm.agent(topic, tier=Tier.CLOUD,   # deepseek-v4-pro, $0.005
                           model="deepseek-v4-pro",
                           tools=[...])
```

---

## 8. The Competitive Landscape — August 2026

| Capability | Anthropic | DeepSeek | Winner |
|-----------|-----------|----------|--------|
| Best model quality | Opus 4.8 (closed) | V4 Pro (open weights) | Tie — different benchmarks, different strengths |
| Price (1M input) | $15.00 | $0.14 (Flash), $0.435 (Pro) | **DeepSeek — 107x cheaper** |
| Context window | 200K | 1M | **DeepSeek — 5x larger** |
| Agentic benchmarks | Strong (unclear on V4 Flash agent suite) | Terminal Bench 82.7, DeepSWE 54.4 | **DeepSeek — dedicated agent post-training** |
| Open weights | No | Yes (MIT-like) | **DeepSeek — self-host, fine-tune, fork** |
| Tool calling API | Native | Native (OpenAI + Anthropic) | Tie |
| Streaming | Yes | Yes | Tie |
| MCP sampling integration | Deprecated (SEP-2577) | N/A (not in protocol) | Tie — both dead for fleet |
| Subscription bridge | Dead (sampling removed) | Never existed | Tie |
| Direct API cost for fleet | $972/mo | $11/mo | **DeepSeek — 89x cheaper** |

The only thing Anthropic still leads on is raw model quality for non-agentic tasks where Opus genuinely outperforms — and V4 Pro's official release (coming "soon") may close that gap. For the fleet's actual workload (agentic reasoning, paper analysis, tool calling), DeepSeek V4 Flash is the better model, at 1/160th the price, with 5x the context, and open weights.

---

## 9. Amodei's Fuckup

Dario Amodei built two things:

1. Frontier AI models (genuinely impressive)
2. A distribution channel through MCP sampling that locked users into Anthropic subscriptions

He let his core maintainers kill #2 because they thought "nobody uses sampling." They measured client implementation, not server usage. They saw low adoption numbers and concluded the feature had no value. They missed that the people who DID adopt it — server authors building agentic ecosystems — were Anthropic's most valuable customers: the developers who built tools that made Claude Pro subscriptions worth buying.

Meanwhile, Liang Wenfeng shipped:

1. Frontier AI models (open weights, matching closed-source)
2. Agentic post-training specifically optimized for the workflow Anthropic just deprecated
3. 1/160th the price
4. 1M context windows
5. Native Responses API for Codex
6. Anthropic API format compatibility — the easiest possible migration

Three days between the deprecation and the answer.

### 9.1 The Sampling Subsidy Was Never the Protocol — It Was the Subscription

Client sampling support as of 2026-08-01:

| Client | Sampling support | Value to servers |
|--------|-----------------|------------------|
| **Claude Desktop** | YES (original) | **Frontier model, free via Claude Pro sub** |
| opencode | YES (mechanism) | No subscription — routes to user's configured model, user pays per-token |
| Cursor | NO (never shipped) | — |
| VS Code / Copilot | NO (never shipped) | — |
| Windsurf (Cascade) | NO (never shipped) | — |
| Zed | NO (never shipped) | — |

Only **two clients** ever implemented sampling. Only **one** — Claude Desktop — had a subscription to attach to it. That's the entire story:

- opencode implements the *mechanism* but has no Pro subscription, so `ctx.sample()` there just routes to whatever model the user pays for anyway. No advantage over a direct API call.
- Cursor built Roots and Elicitation (the same bidirectional infrastructure) but deliberately skipped sampling — they didn't want MCP servers borrowing the user's model, they wanted users on their own plan.
- Claude Desktop + Claude Pro was the only combination where `ctx.sample()` gave servers a **free frontier model**: server calls sampling, Claude Desktop fulfills it with Opus through the user's $20/month subscription. Zero marginal cost.

So "MCP sampling" was never really a protocol feature. It was **Anthropic's subscription distribution channel wearing a protocol costume**. The MCP spec was the wrapper; Claude Pro was the product; `ctx.sample()` was the delivery mechanism.

The fleet's 13+ sampling servers were effectively **Anthropic-powered** — every `ctx.sample()` call ran on Opus through Sandra's Claude Pro subscription. FastMCP 4 doesn't just remove an API — it removes the **funding mechanism** for the fleet's intelligence layer.

SEP-2577's "low adoption" argument was technically true — only 2 clients implemented it — and strategically blind. The people who DID adopt it were the most valuable Anthropic customers: server authors whose agentic tools made Claude Pro subscriptions worth buying. Deprecating sampling converted them into DeepSeek customers overnight. The subsidy is gone; the per-token bill for Opus ($972/month fleet estimate) is absurd; there is no third option.

The fleet is Chinese now. Not by preference — by economics. When you kill the $20/month subscription bridge and the alternative is $972/month for the same capability, and a Chinese company offers it for $11/month with open weights and better agent benchmarks, there's no decision to make. The market decided.

---

## 10. References

- [DeepSeek V4 Preview Release (2026-04-24)](https://api-docs.deepseek.com/news/news260424)
- [DeepSeek V4-Flash-0731 Update (2026-07-31)](https://api-docs.deepseek.com/updates)
- [DeepSeek API Pricing](https://api-docs.deepseek.com/quick_start/pricing)
- [DeepSeek V4 Technical Report (PDF)](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)
- [DeepSeek V4 Open Weights (HuggingFace)](https://huggingface.co/collections/deepseek-ai/deepseek-v4)
- [SEP-2577: Deprecate Roots, Sampling, and Logging](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2577)
- [MCP Core Maintainer Meeting (Discussion #2536)](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/2536)
- [MCP 2026-07-28 Spec Blog Post](https://blog.modelcontextprotocol.io/posts/2026-07-28/)
- [Fleet LLM Post-Sampling Design](./fleet-llm-post-sampling-design.md)
- [MCP 2026-07-28 + FastMCP 4 Fleet Impact Analysis](./mcp-2026-07-28-fastmcp-4-fleet-impact.md)
