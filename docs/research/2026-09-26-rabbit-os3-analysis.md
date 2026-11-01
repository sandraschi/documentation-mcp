# Rabbit OS3 Analysis - Agentic OS with BYOK + Agent Nodes

**Source:** live fetch 2026-09-26 - `https://www.rabbit.tech/` (homepage + FAQ schema), `https://www.rabbit.tech/support/article/rabbitos-3`, `https://www.rabbit.tech/updates`, `https://news.17173.com/content/09242026/020923857.shtml` (IT之家 via 17173, 2026-09-24)
**Date noted:** 2026-09-26
**Related:** research/2026-09-26-fleet-vs-claw-parity.md, research/2026-09-19-google-cc-family-agent.md, research/2026-09-26-openclaw-alternatives-sandbox.md
**Question:** what is OS3, how does onboarding/BYOK work, is it PRC, how does it compare to our bots, what can we filch

## 1. What OS3 is

OS3 is an agentic operating system, not a kernel. Launched GA 2026-09-22 after ~1 year silence (previous官网 news was 2025-09). Tagline: `start with the thought`.

Core loop: describe outcome in chat, OS3 figures out model + computer + tools + steps, comes back only when a decision is genuinely yours. Persistent memory and context carry across requests. Long tasks continue after you close the tab.

Components:

1. **OS3 cloud workspace** - conversation + memory + skills + orchestration. Hybrid system: rabbit services + model provider you chose.
2. **rabbit agent (node)** - small local worker installed on each computer you connect (Windows, macOS, Linux, 1 command). Works primarily through that computer's terminal, uses supported local files/tools/commands. Up to 5 nodes per account. Multi-node = one project uses several machines.
3. **Channels** - web (`os3.rabbit.tech`), desktop app (Mac universal 173 MB, Win x64 79 MB, Win ARM 84 MB), Telegram paired bot, Messages via iMessage/RCS/SMS, r1 push-to-talk. Each keeps own thread, shared memory/context.
4. **Skills** - reusable capabilities. Imports from coding agents already on a connected machine: Claude Code, Codex, Gemini CLI, OpenClaw, Hermes, Cursor. Import converts skills to OS3 skills + carries standing instructions to profile. No credentials, no transcripts.
5. **DLAM** - screen-see + drive-apps path with permission. Descendant of LAM Playground (2024 web agent) + Android agent (2025). Used only when terminal path is not enough.
6. **Memory** - explicit: bring in what matters, correct when wrong. `you are the settings` = shape tone/length/follow-up via conversation, becomes ongoing context.

Pricing: OS3 free. You pay model provider directly per their API pricing. No subscription bundling by design.

Privacy claims (from FAQ): connecting a computer does NOT auto-upload whole machine. Files stay on your machines, OS3 works with computers + relevant files you choose. Credentials for connected apps stay on your machine (sign in there). Permissions section controls when OS3 must ask; sensitive/irreversible always confirms.

r1 role: optional physical channel. No r1 needed for OS3. Once web setup done, r1 active - press button, speak. Device settings (linking, lost mode, media, magic gallery/voice, dev mode) moved into OS3 settings > r1.

rabbit intern: retired as standalone product. Specialist capabilities folded into OS3. Existing creations stay, gallery is curated subset - export via delete-rabbit-data article for full copy.

## 2. Onboarding / BYOK flow (reconstructed, SPA blocks scrapers)

`os3.rabbit.tech` and `/try-os3` are client-rendered SPA - server fetchers return only `OS3`. Flow below is from homepage FAQ JSON-LD + support article, both fetched live.

1. **Account:** go to `os3.rabbit.tech`, log in or create rabbit account, finish setup in single conversation. No device update.
2. **BYOK connect (settings > model setup):**
   - Anthropic direct, OpenAI direct - OS3 lists known models.
   - Google Gemini, OpenRouter, Ollama, Z.ai as aggregators - reads model list from your account after key saved, refuses requests until you pick a model.
   - Model served from own connected computer, or own endpoint.
   - Phone calls extra: needs own OpenAI key + project ID.
   - Free paths admitted: OpenRouter free models, Gemini API free tier, local compatible models. Limits set by providers.
   - Swap = replace key. Memory/skills/nodes persist.
3. **Connect nodes (settings > rabbit agents):** run 1 setup command per machine, or 1-click install from desktop app on same machine. Node = connected computer. Machine doing local work must stay on + connected.
4. **Channels:** pair Telegram bot, enable Messages, link r1. Threads separate, memory shared.
5. **Skills import:** connect computer, OS3 offers detected agents to import. Choose which to bring, which to leave.
6. **Permissions:** set when OS3 should check before acting. Change/withdraw anytime.

Desktop vs agent (explicit FAQ): desktop app = OS3 workspace window, stays signed in. rabbit agent = separate smaller program that turns a computer into a node.

## 3. Updates timeline (from /updates, fetched live)

2026:
- OS3 GA - state outcome, works out rest across models + computers.
- 2.3 - Hermes agent to r1, proactive rabbit, OpenClaw protocol v4 support, DLAM with BYOK model support.
- 2.2 - Claude Code to r1, terminal mode back, building/creating tools.
- 2.1 - journal, magic camera+, personalization.
- DLAM + OpenClaw + voice, Project Cyberdeck announced.

2025:
- rabbitOS 2 (multi-agent cards + voice vibe-coding), rabbit intern launch, Red Dot Best of Best x2, iF Design Award, Android agent (generalist), intern trial.

2024:
- Teach mode beta, LAM Playground (generalist web agent), EU/UK expansion, beta rabbit multi-LLM router, magic camera, Perplexity partnership, CES launch (10k units in 24h), first shipments.

Takeaway: 2024 = LAM promise, 2025 = agents on r1, 2026 = decouple from r1 entirely (BYOK + nodes + OpenClaw compat). OS3 is the pivot from device to layer.

## 4. Company origin - PRC?

No. rabbit inc., founded 2022, HQ Santa Monica / Los Angeles, USA.

Founder/CEO Jesse Lyu (吕骋) is Chinese-born - ex Flow, Raven Tech (acquired by Baidu), Baidu. That is why Chinese tech press covers every move. Company, funding, product are US.

One China link inside OS3: Z.ai (Zhipu) is one optional BYOK aggregator. Optional, avoid if residency matters. Use Anthropic/OpenAI direct or Ollama local.

## 5. Fleet comparison

One-liner: BYOK = local-llm-mcp, nodes = fritz + robofang federation, memory = MemOps/Fritz wiki + LanceDB (speech/discord), voice = speech-mcp + fritz voice bus, desktop DLAM = pywinauto-mcp, channels = discord-mcp pattern (no native Telegram/r1 yet), skills = openclaw-molt clawd_skills + fritz SKILL.md importer + robofang hands.

| Capability | rabbit OS3 | fritz (fleet-agent-mcp) | robofang | speech-mcp | local-llm-mcp | pywinauto-mcp | discord-mcp | myai |
|---|---|---|---|---|---|---|---|---|
| Model decoupling (BYOK) | core - swap key, keep env | partial via ctx.sample + llm_client | no own LLM, orchestrates | multi-STT/TTS keys | yes - 13 tools, Ollama/LMStudio/vLLM + 28 cloud, circuit breaker | caller LLM only | bot token + optional Ollama | adapters ollama/lmstudio/gemini/anthropic/openai |
| Local execution nodes | rabbit agent, 5/account, terminal-first, multi-node | coordinator + workers, fleet_bridge to other MCPs | federated nodes over Tailscale, Dark Twin shadow | local FunASR + cloud TTS | stateless proxy, engine supervision, LM Link peer discovery | 100% local UIA/Win32 + OCR, telemetry SQLite | local server + Discord cloud API | Docker Compose 18+ svcs, GPU |
| Persistent memory | conversation-carried context + profile | wiki + pulse + evolution + session_log (ahead) | KV + LanceDB + ADN (ahead) | LanceDB RAG transcripts | none (stateless) | mission/snapshot/template stores | LanceDB history RAG + depot jsonl | Weaviate + Postgres |
| Skills import | auto-detect 6 CLI agents, 1-click convert | SKILL.md importer (seed) | hands + plugins Skill Manager | skills/ dir + personas | SKILL.md render only | app_profiles/ | bundled skills/prompts | none unified |
| Channels | web/desktop/Telegram/iMessage/r1, separate threads shared memory | voice bus + Discord crosspost + email + Intel Hub | hub UI + CLI + federation, chat-first | cockpit + REST/SSE + voice bus delegate | dashboard + OpenAI-compat API | operator UI, no Telegram | Discord native + dashboard + slack_bridge | per-service React UIs |
| GUI control | DLAM with permission | dev_ops timers/Plex only | via fleet cua, not integrated | - | - | automation_mission + smart click + macros + HITL kill switch (ahead) | - | - |
| Background/heartbeat | close tab, agents continue, settings lists runs | cron 30m heartbeat + coworker flows (best) | heartbeat, no cron | wake listener | health 60s + breaker | watchers | rag_sweep jobs | Prometheus/Grafana |
| Confirm gates | permissions section + sensitive always-ask | destructive:true annotation only (gap) | audit signoff non-blocking (gap) | - | - | HITL + BYPASS_HITL (good) | anti-spam limits | - |
| Onboarding | single-conversation setup + 1-command node | none (gap) | hand docs + /fleet/onboard | - | dashboard | NSIS single binary | QR-less manual | - |

Where we are ahead: Council reasoning, DTU atomic commits, flowforge gates, evolution memory, RAG+ADN depth, scheduler observability (aiwatcher APScheduler + Prometheus), pywinauto HITL + kill switch, local-llm circuit breaker + VRAM supervision.
Where behind: single-conversation onboarding, 1-command node lease, model-swap-keeps-env guarantee, multi-thread-shared-memory channels, third-party skill auto-import UX.

## 6. What to filch (ordered)

| # | Pattern | Fleet mapping | Effort |
|---|---|---|---|
| 1 | 1-command node lease (`settings > agents > curl ...`) with 5/node quota + online check | fritz + robofang: `node_lease` portmanteau (install, heartbeat, revoke, quota) via Tailscale, reuse tailscale-mcp | M - new ops + install script |
| 2 | Model-swap-keeps-env: memory/skills/nodes/versioned profile independent of provider key | local-llm-mcp + fritz memory: split `profile/env` store from `provider/key` store, swap test | M - schema split |
| 3 | Skill auto-import: detect Claude Code/Codex/Gemini CLI/OpenClaw/Cursor on node, offer convert | extend fritz SKILL.md importer + openclaw-molt clawd_skills + robofang hands | M - detector + converter |
| 4 | Separate threads, shared memory (web/desktop/Telegram/r1 each own history, one memory) | robofang + discord-mcp + comms-mcp: `thread_id` per channel, `memory_shared` scope | M - memory schema |
| 5 | Permissions section UX: per-op ask/always-allow + sensitive-always-ask + withdraw | fritz POLICIES.yaml + confirm queue UI in Inbox (see fleet-vs-claw P0) | S - already specced, copy wording |
| 6 | Background runs list: close tab, see runs in settings, resume | fritz Intel Hub + robofang hub: `background_runs` page | S - list existing jobs |
| 7 | Free-tier BYOK labels (OpenRouter free, Gemini free, Ollama local) in setup | local-llm-mcp dashboard setup wizard | S - copy list |
| 8 | Desktop app = signed-in workspace window, agent = separate small binary | package pywinauto-mcp NSIS pattern for node agent | M - reuse NSIS pipeline |
| 9 | DLAM-with-BYOK: vision model selectable per GUI task | pywinauto-mcp `automation_smart` + local-llm-mcp vision routing | M - model picker passthrough |
| 10 | Single-conversation onboarding (account + key + node + skills in one chat) | fritz + robofang onboarding: scripted sampling workflow | M - sampling workflow |

Not to copy: cloud-only orchestration (keep local-first), Z.ai default (residency), r1 hardware dependency (we have no device), phone-call via personal OpenAI key (cost trap).

## 7. Open questions

- rabbit agent install command + protocol not yet public in docs - needs live capture from `os3.rabbit.tech > settings > rabbit agents`. Track.
- DLAM model list with BYOK - which vision models actually work for GUI grounding.
- Context actually sent to rabbit services vs provider - FAQ says hybrid, no data-flow diagram.
- Multi-node scheduling - parallel vs delegated, failure handling.
- Rate/cost when using OpenRouter free tier for long background runs.

## 8. Next steps

1. Watch `https://www.rabbit.tech/updates` + `https://os3.rabbit.tech` for agent install command + protocol spec. Capture to this doc.
2. Prototype `node_lease` in fritz (P0 from fleet-vs-claw) using rabbit wording for permissions.
3. Extend local-llm-mcp setup wizard with free-tier labels + swap-keeps-env test.
4. Extend fritz SKILL.md importer with auto-detect for 6 CLI agents.
5. Test Ollama-local OS3 end-to-end from throwaway VM before touching Goliath main.

---
*Notes: homepage + support + updates fetched live 2026-09-26. try-os3/os3 app are JS SPA - server fetch returns only `OS3`, needs browser capture. Company origin from Baidu/Zhihu cross-check (founder Jesse Lyu, HQ LA, founded 2022).*

## 9. Industry trajectory - the next AI wave for endusers

Full thesis: `NEXT_AI_WAVE_ENDUSERS.md` (mcd root).

Short version: OpenClaw (Clawdbot Nov 2025, Moltbot Jan 2026, OpenClaw Jan 2026) proved the pattern but stayed nerds-level-2 - JSON config, own tokens, full shell, no sandbox, text-only. Summer 2026 enclosed it: Grok Bot public beta Aug 11 2026 (per-Bot cloud Linux VM, 24/7, multi-Bot group-chat collab, templates, Chrome import, Tesla push, subscription), Meta Muse (2C agent, 3.6B-user distribution via WA/IG/FB), Rabbit OS3 GA Sept 22 2026 (BYOK + 5 nodes + shared memory + web/Telegram/iMessage/r1). Same converged shape: persistent agent + computer + memory + skills/templates + chat/voice entry.

Voice is the hoi-polloi unlock. Nerds tolerate terminals and keys; endusers need wake-to-speak, spoken confirms, QR bind, safe defaults. Corps will charge token/subscription or ads for it. FOSS answer is free-as-in-beer if you have hardware (RTX 40x0, new Mac Studio class). Fleet edge: speech-mcp + Voice Bus + local-llm-mcp already exist; gaps are QR onboarding, template marketplace, per-agent containers, voice-first confirm queue - see section 6.
