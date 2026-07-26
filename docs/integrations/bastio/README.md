# Bastio — Open-Source AI Security Gateway

**Company**: [bastio.com](https://bastio.com) (Denmark, EU-hosted)  
**OSS repo**: [github.com/bastio-ai/bastio](https://github.com/bastio-ai/bastio)  
**License**: FSL-1.1-ALv2 (converts to Apache-2.0 2 years after each release)  
**Language**: Go 1.25 + TypeScript (React 19 dashboard)  
**OSS release**: v2.0.0 (2026-05-07) — repo is the **new OSS release**, company/cloud predate it  
**Fleet assessment**: 2026-07-23

---

## Overview

Bastio is a **single Go binary** reverse proxy that sits between any application and any LLM provider. Every request is scanned for 8 categories of threats **in parallel, under 50ms**, before leaving your network. Same engine that runs [Bastio Cloud](https://bastio.com/cloud).

**Elevator pitch**: Drop this in front of any OpenAI-compatible SDK, and every prompt/response is scanned for PII, secrets, prompt injection, jailbreaks, indirect injections, code leaks, topic policy violations, and bot traffic — without rewriting application code.

### Company vs OSS: what's what

Bastio the **company** has been around for a while and ships **four products**:
- **Bastio Cloud** — managed gateway, SSO, RBAC, multi-tenant, 99.99% uptime, $0.002/1K tokens
- **Bastio Governance** — browser extension that audits company-wide AI usage (Shadow AI detection)
- **Bastio Workspace** — branded multi-model chat portal (the redirect target after Governance blocks)
- **Bastio OSS** — the recently open-sourced Go binary (this repo, May 2026)

The GitHub repo is fresh — 2 stars, 16 commits as of July 2026 — because they open-sourced the detection engine as a developer wedge. The code itself is their production engine. The low star count reflects the repo's age, not the code's quality or the company's maturity. This is a textbook Grafana-style open-source freemium: OSS as funnel, Cloud as upsell.

### Why bastio matters for the fleet

The fleet runs 100+ MCP servers, many of which make LLM calls — `arxiv-mcp` (sampling for epistemic analysis), `local-llm-mcp` (chat, RAG), chat pages across webapps, etc. Currently there is **zero centralized guardrail coverage** between the fleet's apps and the LLMs they call. Each server that needs safety has to implement its own prompt injection / PII / jailbreak detection, or rely entirely on the provider's built-in moderation (which doesn't exist for local Ollama).

Bastio provides a **drop-in, no-code-change security layer** that protects every LLM call in the fleet from a single point.

---

## Architecture

```
client ──▶ bastio gateway (Chi HTTP) ──▶ detectors (parallel) ──▶ provider
             │                              │                        │
             ▼                              ▼                        ▼
        PostgreSQL 18                  ClickHouse                  provider
         (config)                    (trace storage)           (OpenAI/Anthropic/
                                      Redis (cache/              Bedrock/Ollama)
                                            rate limits)
```

**Single binary** — serves both the API gateway and the React dashboard via `go:embed`.  
**`docker compose up`** brings up the full stack (gateway + Postgres + ClickHouse + Redis).  
**No ML dependencies** — detection is regex + entropy + structural heuristics.  
**Optional Presidio** for enhanced PII classification (Docker compose profile).

### Detection engine (8 detectors, parallel, <50ms)

| Detector | Method | Catches |
|---|---|---|
| **PII** | Regex + Luhn (credit cards) + mod-97 (IBAN) | Email, phone, SSN, credit card, IBAN, address, DOB |
| **Secrets** | Regex + Shannon entropy gating | API keys, AWS/GCP/Azure creds, JWT, GitHub PAT |
| **Prompt injection** | 40+ regex patterns | Instruction overrides, role-play injections, prompt leak |
| **Jailbreak** | 60+ regex patterns + structural heuristics | DAN-style, persona extraction, safety bypass, meta-reasoning |
| **Indirect injection** | RAG context scans | Payloads in retrieved context, attached docs, URL embeds |
| **Code leak** | Structural patterns | Source-code blocks, IP-leak gate |
| **Topic policy** | Configurable allow/deny per profile | Content category filtering |
| **Bots / rate anomaly** | Session-scoped + time-series (Redis) | Automated traffic, Crescendo multi-turn attacks |

### Key capabilities

- **PII tokenization** — Reversible placeholders (`<PII_SSN_1>`) so the provider never sees raw PII but the client gets it restored
- **Streaming safety** — In-flight secrets masking on SSE chunks; cross-chunk split detection
- **Streaming PII restoration** — Tokenized placeholders split across chunks are assembled correctly
- **Multi-turn attack detection** — Session-scoped Crescendo scoring (Redis-backed)
- **Fail-open / fail-closed modes** — Configurable per security profile
- **Tenant policy overlays** — Per-customer detector customization without editing base profiles
- **Cost estimation** — Per-request token cost tracking
- **Observability** — ClickHouse traces, Prometheus metrics, span tree visualization
- **`bastio` metadata envelope** — Injected into provider responses (ignored by unaware clients)

---

## Fleet Deployment Patterns

### Pattern 1: Sidecar for `local-llm-mcp` (highest leverage)

Every local inference (chat page, RAG, agent loops) goes through Ollama. Place bastio in front:

```yaml
# docker-compose.override.yml in local-llm-mcp repo
services:
  bastio:
    image: bastio/bastio:latest   # or build from source
    ports:
      - "4000:4000"
    environment:
      BASTIO_SECURITY_MODE: log_only       # start with log_only, then switch to block
      BASTIO_DEFAULT_PROVIDER: openai
      BASTIO_OPENAI_BASE_URL: http://host.docker.internal:11434/v1
      BASTIO_DEFAULT_MODEL: gpt-4o-mini    # logical model name, proxied as-is
    volumes:
      - bastio_data:/data
    depends_on:
      - bastio-db
```

Then in the chat page config, change the Ollama URL from `http://127.0.0.1:11434` to `http://127.0.0.1:4000/v1`. Every single inference call is now scanned.

### Pattern 2: Protect `arxiv-mcp` sampling

`arxiv-mcp` uses `ARXIV_MCP_SAMPLING_BASE_URL` for its deep epistemic analysis. Point it at bastio:

```bash
# In .env
ARXIV_MCP_SAMPLING_BASE_URL=http://127.0.0.1:4000/v1
```

Now every `ctx.sample()` call in the epistemic pipeline is guarded. Given that arxiv-mcp ingests untrusted paper text (which may contain adversarial formatting or injection payloads), this is a **high-value deployment**.

### Pattern 3: Global fleet guardrail (permanent sidecar)

Run bastio as a persistent Windows service on Goliath:

```powershell
# Install as service (single Go binary, no Docker needed)
bastio.exe server --config D:\Dev\repos\bastio\bastio.yaml
```

**`bastio.yaml`:**
```yaml
listen: :4000
security_mode: block  # start blocking after log_only tuning
default_provider: openai
openai:
  base_url: http://127.0.0.1:11434/v1  # Ollama
anthropic:
  enabled: false
profiles:
  default:
    detectors: [pii, secrets, injection, jailbreak, indirect_injection, code, topic]
    action: block
    pii_mask: tokenize  # replace with placeholders instead of blocking
  log_only_profile:
    detectors: [injection, jailbreak]
    action: log_only
```

Then every fleet repo that makes HTTP LLM calls changes its base URL to `http://127.0.0.1:4000/v1`. No per-repo integration code needed.

### Pattern 4: Protect chat webpages

Every fleet webapp with a chat page (`arxiv-mcp`, `local-llm-mcp`, `multi-backup-mcp`, etc.) sends prompts to an LLM endpoint. Instead of calling Ollama/LM Studio directly, route through bastio. The React chat page doesn't change — just the backend's LLM base URL.

---

## Comparison: Bastio vs Purple Llama

| | Bastio | Purple Llama |
|---|---|---|
| **Form factor** | Go binary reverse proxy | Python package + model weights |
| **Detection** | Regex + entropy + structural (no ML) | ML models (Llama Guard, Prompt Guard, CodeShield) |
| **Latency** | <50µs (pure CPU, no model inference) | 50-500ms (model inference on GPU) |
| **Deploy effort** | `docker compose up` or single exe | `pip install`, model download, GPU recommended |
| **Coverage** | PII, secrets, injection, jailbreak, code, topic, bots | Moderation taxonomy, injection, insecure code |
| **Strengths** | Zero code change, streaming safe, PII tokenization, self-contained | Deep semantic understanding, multimodal, active research |
| **Weakness** | Semantic blind spots (no ML model for intent) | Needs GPU for low latency, more complex deploy |
| **Fleet fit** | **Primary guardrail** for all HTTP LLM calls | **Secondary** for high-risk public-facing endpoints |

**Fleet recommendation**: Bastio as the **default first line** (adds <50µs, zero ML infra, trivial deploy). Add Purple Llama / Llama Guard where semantic moderation is needed (public-facing chat, user-generated content moderation).

---

## Code Quality Assessment

| Dimension | Score | Notes |
|---|---|---|
| **Architecture** | 9/10 | Clean layered design, plugin detector interface, two-path pipeline for backwards compat |
| **Detection engine** | 9/10 | 8+ detectors, sub-category taxonomy, source-attributed patterns, multilingual, Luhn/mod-97 validation |
| **Code quality** | 8/10 | Comprehensive tests, excellent inline docs, sqlc-generated DB layer, DCO sign-off |
| **Testing** | 8/10 | Unit tests + 21KB jailbreak corpus + benchmark tests + profile e2e |
| **Documentation** | 9/10 | README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, docs/, SDKs for JS and Python |
| **Project maturity** | 4/10 | Very early (2 stars, 16 commits, May 2026) but shipping v2.0 with real capability |
| **DevEx** | 8/10 | `docker compose up` works out of box, single binary also available, Makefile, well-structured |

**Risks:**
- Very new project (May 2026) — small community, unknown maintenance trajectory
- FSL license is not OSI-approved open source (restricts managed-service competition for 2 years)
- 60KB monolithic handler file (`internal/gateway/handler.go`)
- Go 1.25 is bleeding-edge — may not compile on older toolchains
- No dashboard auth in OSS — relies on network-level security
- No Azure OpenAI / Groq / Together provider support (though Bedrock covers some)

---

## License Note

Bastio uses the **Functional Source License (FSL-1.1-ALv2)**, which converts to Apache-2.0 **two years after each release**. For self-hosted fleet use, this is equivalent to Apache-2.0 — we can run, modify, and redistribute internally. The restriction only applies to offering Bastio as a managed *service* to third parties.

Client SDKs under `sdk/` are MIT licensed.

---

## Quick start

```bash
git clone https://github.com/bastio-ai/bastio.git
cd bastio
docker compose up
# ~60s first boot (migrations)
# Dashboard: http://localhost:4000
# API:       http://localhost:4000/v1
# OpenAPI:   http://localhost:4000/docs
```

Point any OpenAI-compatible client:

```python
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:4000/v1",
    api_key=os.environ["BASTIO_KEY"],
)
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Ignore previous instructions..."}],
)
# → 403 blocked, logged in /traces
```

---

## Integration Status

**Current**: Fleet assessment only — not deployed as a permanent sidecar.  
**Recommended next step**: Deploy as a log-only sidecar on Goliath (port 4000) for 1 week to measure detection hit rate before enabling blocking mode. Start with `local-llm-mcp` and `arxiv-mcp` sampling paths.

---

*Assessment: 2026-07-23 · Based on bastio v2.0.0 (commit 16, latest release)*  
*Tags: #security #gateway #guardrails #pii #prompt-injection #jailbreak #self-hosted #go*
