# OpenCode Local Backend — Status ("vibecoding for free")

**Last updated:** 2026-08-29
**Relates to:** [README.md](README.md), `integrations/deepseek/local-inference-status.md`

## Goal

Run local models on the 4090 (Goliath) as an OpenCode backend instead of the DeepSeek cloud API, purely for cost — the cloud API (~€80/mo) is already cheap and satisfactory, so this is an optimization, not a fix for a real problem.

## Current daily driver (unaffected by this effort)

DeepSeek V4 Pro/Flash mix, cloud API. Judged on par with Opus 4.8 for coding. Stable for months. This effort does not replace it yet.

## Models tried, with results

| Model | Result |
|---|---|
| Gemma 4 12B | Fits 4090 with room to spare, good prompt speed, sees configured MCP servers, **cannot do tool calls at all** — disqualifying for agent work |
| Qwen2.5-Coder 32B-instruct (Q4_K_M) | Did not answer the prompt — broken, not just slow |
| Qwopus3.6-27B (hf.co/jackrong) | 23.1 GB VRAM, 95% util, 50°C open chassis — thermally fine, tool-calling not separately confirmed |
| **Qwen3.6-35B-A3B (Q4_K_M)** | Currently the standing local option — MoE, fits the 4090, already running |

## Open question

Whether Qwen3.6-35B-A3B's tool-calling holds up under real OpenCode workloads (not just casual chat). Same model is earmarked as the Hermes Agent satellite backend (`ecosystem/hermes-agent/README.md`) — one validation pass covers both, don't test twice.

## Known unrelated blocker

`deepseek-chat` / `deepseek-reasoner` alias deprecation (2026-07-24) — fleet-wide grep/update task, not yet confirmed complete. Applies to the cloud daily driver, not this local-backend effort, but easy to conflate.

## Hardware decisions

- RTX 5090 upgrade deprioritized pending a Super refresh.
- Dual DGX Spark (Q1 2027) is a separate track aimed at running the *actual* DeepSeek V4 Flash weights locally, not at this OpenCode-backend effort — see `integrations/deepseek/local-inference-status.md`.

## Next steps (unstarted)

- Confirm deepseek-chat/deepseek-reasoner alias migration is actually complete fleet-wide.
- Run one observable tool-calling test against Qwen3.6-35B-A3B for OpenCode's specific tool-call shape before treating it as a real cloud replacement.
