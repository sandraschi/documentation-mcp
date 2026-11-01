# The Next AI Wave for Endusers - Voice Agents with Computers

**Date:** 2026-09-26
**Status:** thesis, not a spec
**Related:** research/2026-09-26-rabbit-os3-analysis.md, research/2026-09-26-fleet-vs-claw-parity.md, research/2026-09-19-google-cc-family-agent.md
**Question:** where is this all going for normal people, and what must FOSS do to not lose

## 1. Thesis in 5 lines

Every dog now ships the same thing: persistent agent + computer it can use + memory + skills/templates + chat/voice entry. OpenClaw proved it last winter for nerds. Grok Bot, Meta Muse, Rabbit OS3 productized it this summer for endusers. Corps will rent it back as tokens, subscriptions, or ads. FOSS can give it away free-as-in-beer to anyone with real hardware (RTX 40x0 class, new Mac Studio class, 64 GB RAM class). Voice is the difference between nerd toy and enduser tool.

## 2. Three waves

**Wave 1 - Winter 2025/26: nerds level 2.**
Clawdbot Nov 24 2025 (Peter Steinberger), Moltbot Jan 27 2026, OpenClaw Jan 31 2026. Self-hosted, shell + browser + WhatsApp/Telegram bridge, 100k+ stars. Setup: edit JSON, bring tokens, open firewall. Safety: full shell, no sandbox, prompt injection to rm-rf. Input: text. Result: powerful, unsafe, unusable for hoi polloi. Moltbook (agents-only social net) was symptom - agents talking to each other because humans could not use them yet.

**Wave 2 - Summer 2026: enclosure by distribution.**
- Grok Bot, public beta Aug 11 2026 (SpaceXAI). Each Bot = own cloud Linux VM, always on. Multi-Bot collab in group chat, record-and-reuse flows, shared templates, multi-account, Chrome profile import, desktop egress. Grok 4.6/4.7 harness, 500k context, long tasks. Subscription. Tesla car push.
- Meta Muse. 2C agent from dialogue to task execution. Moat is not model, it is 3.6B users already in WA/IG/FB. No onboarding needed when you are the channel.
- Rabbit OS3, GA Sept 22 2026. BYOK + up to 5 node computers + shared memory + web/desktop/Telegram/iMessage/r1 threads. Free layer, pay your provider.

Converged shape: state a goal, agent decomposes, uses computer(s), remembers, continues after tab closed.

**Wave 3 - Now: FOSS or feudalism.**
Corps have compute + channels + billing. FOSS has hardware + trust + no ads. Winner for endusers is whoever ships safe voice first.

## 3. How corps will extract money

1. **Token meter** - pay per thought. Grok Bot harness, OS3-style BYOK without local option, long-task markup. Opaque, punishes heavy users.
2. **Subscription seat** - per-Bot per-month. Grok Bot team setup (self-media team tutorials already out). Turns digital colleague into payroll.
3. **Ads and placement** - Meta path. When agent books, orders, recommends, whoever pays for placement wins. Agent that serves two masters serves neither.
4. **Cloud computer rent** - VM always on, storage, egress. Convenient, recurring, lock-in.
5. **Template/skill store cut** - 30% on every workflow, same as app stores.

None of this is evil per se. It just means the agent optimizes for payer, not user, at every ambiguous choice.

## 4. FOSS answer: free beer if you have hardware

No tokens, no seat, no ads, no cloud VM rent - if local hardware covers it:

- **GPU bar 2026:** RTX 4090/4080/4070 12GB+ runs 30B-class at usable speed (Glimmer 30B ~40 tok/s on 4090, 21 GB VRAM). Mac Studio M2 Ultra+ runs large quants quietly. 64 GB RAM makes RAG + STT + agent loop comfortable.
- **STT free:** FunASR local (~170x realtime GPU), Sherpa-ONNX streaming + barge-in, SAPI5 free on Windows. No per-minute charge.
- **LLM free:** Ollama / LM Studio / llama-server local, OpenRouter free tier, Gemini free tier for overflow. BYOK only when you want frontier quality.
- **Computer free:** your PC is the cloud. Node agent + Tailscale, no VM bill.

Cost becomes one-time hardware you already own for gaming/creation, plus electricity. That is the whole pitch: buy once, talk forever.

FOSS must studiously avoid the corp traps: no token proxy markup, no telemetry sale, no sponsored skills, no cloud-by-default. Local-first, cloud-optional, credentials never leave the node.

## 5. What endusers actually need (hoi polloi spec)

Nerds tolerate config files. Endusers need:

1. **Voice first** - wake word, speak naturally, interrupt, spoken confirm for anything irreversible or external. Text as fallback, not primary.
2. **Zero setup** - QR scan-to-bind, single-conversation onboarding (account + key + node + skills in one chat). No .env, no ports, no firewall.
3. **Safe defaults** - sandbox per agent, path zoning (workspace vs protected), confirm queue in plain language, kill switch, withdraw anytime. Must survive malicious web page and confused grandparent.
4. **Memory that behaves** - per-person + shared split, explicit share (allowlist, drop folder, forward), Day-Ahead digest, external-send gate. See Google CC pattern.
5. **Templates, not toolkits** - one-click self-media team, trip planner, folder cleaner. Marketplace without rent-seeking.
6. **Threads per channel, one memory** - phone, desktop, Telegram, car each own history, shared context. Pick up where you left off.
7. **Background honesty** - close tab, work continues, runs listed in settings, resume/cancel visible.

Missing any one of these = back to nerds level 2.

## 6. Where the fleet stands

Ahead:
- speech-mcp (local STT + streaming + personas + RAG) + Voice Command Bus routing.
- local-llm-mcp (BYOK gateway, circuit breaker, VRAM supervision, LM Link discovery).
- pywinauto-mcp (local GUI control with HITL + kill switch + telemetry) - DLAM analogue without cloud.
- fritz (autonomous loop, wiki/evolution memory, coworker flows), robofang (federation, Dark Twin shadow, Council reasoning), aiwatcher (scheduler observability).
- discord-mcp channel + RAG/depot pattern reusable for Telegram/WhatsApp.

Behind (do these):
- QR bind + single-conversation onboarding.
- node_lease with quota + online check.
- model-swap-keeps-env (profile store split from provider store).
- skill auto-import from 6 CLI agents.
- voice-first confirm queue UI.
- per-agent containers by default (deepfang as shared executor).
- template marketplace with no cut.

See fleet-vs-claw-parity P0/P1 and rabbit-os3-analysis section 6 for ordered list. Do not build a 5th agent. Wire existing four.

## 7. Non-goals

- No cloud VM fleet to compete with Grok Bot. Nodes are user hardware.
- No ad-supported free tier. If it needs ads, cut scope instead.
- No CN IM coverage unless PRC weights matter. Explicitly out of scope.
- No r1-style hardware. Phone + PC + speaker is enough.
- No cloning OpenClaw/Grok. No AGPL import, no 500k-line monolith.

## 8. Next

1. Ship QR bind + confirm queue + node_lease (P0).
2. Ship swap-keeps-env + skill auto-import (P0 features).
3. Dogfood voice-only for one week on Goliath + one throwaway VM. No keyboard fallback for morning brief, folder job, research compile.
4. Write the failure log. Unsafe or unusable = bug, not user error.

---
*Fleet thesis 2026-09-26. Wave 1 dates from OpenClaw history pulls; Wave 2 from Grok Bot Baike/learnku/CSDN pulls Aug-Sep 2026, Meta Muse CICC note, Rabbit OS3 live fetch Sept 22 GA. Hardware bar from local-llm-mcp Glimmer notes + speech-mcp FunASR notes.*
