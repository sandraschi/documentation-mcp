---
title: "CRAFT_LLM_PROVIDER_STANDARD - One LLM Contract for All Craft Apps"
category: standard
status: active
audience: craft-dev
last_updated: 2026-11-06
---

# CRAFT_LLM_PROVIDER_STANDARD — One LLM Contract for All Craft Apps

**Status: ACTIVE — normative for all new Rust craft apps (`*-craft` repos).**
Existing apps migrate on next touch; no flag-day.

## One-line rule

**Every craft app gets providers, models, and keys from `craft-ai-core`.
No per-app `llm.rs`. No settings UI that lies.**

## Why

Audit 2026-11-06 found the fleet in three incompatible states:

| App | State |
|---|---|
| codercraft | Own `LlmConfig` (provider/endpoint/model strings) in core; Settings tab wrote to it; nothing read it. The agent used `CraftAiConfig` from file. Settings lied. |
| gamecraft-forge | Own `llm.rs` (Ollama + OpenAI-compat + Anthropic + DeepSeek + Meta), own key storage in `AppConfig`. Good code, duplicated contract. |
| makercraft / moneycraft / writercraft / speechcraft / ... | No LLM layer at all. |

Meanwhile the Python fleet already standardized this exact surface
(`standards/LLM_AND_INSTALL_TIERS.md`, `standards/LOCAL_LLM_STANDARDS.md`,
`templates/llm/SETTINGS_LLM.md`, `templates/llm/llm_engine.py`).
This standard is the Rust port. Read those four first when in doubt.

## 1. Provider table (normative)

All eight live in `craft-ai-core::providers`. UI strings, config values,
and MCP contracts use the **ids**, never display names, never ad-hoc
aliases (aliases resolve, then canonicalize).

| id | label | endpoint default | key? | models source |
|---|---|---|---|---|
| `ollama` | Ollama (local) | `http://127.0.0.1:11434` | no | live `/api/tags` |
| `lmstudio` | LM Studio (local) | `http://127.0.0.1:1234` | no | live OpenAI-compat `/v1/models` |
| `openai` | OpenAI (cloud) | `https://api.openai.com` | yes | live `/v1/models` |
| `anthropic` | Anthropic (cloud) | `https://api.anthropic.com` | yes | **curated list only** (no list API) + free text |
| `deepseek` | DeepSeek (cloud) | `https://api.deepseek.com` | yes | live `/v1/models` |
| `meta` | Meta Llama API (cloud) | `https://api.llama.com/compat/v1` | yes | live `/v1/models` |
| `openrouter` | OpenRouter (cloud) | `https://openrouter.ai/api/v1` | yes | live `/v1/models` |
| `custom` | Custom OpenAI-compatible | empty (required) | optional | live `/v1/models` |

Accepted aliases (resolve, then store the canonical id):
`local`→ollama, `lms`/`lm-studio`→lmstudio, `cloud`/`gpt`→openai,
`claude`→anthropic, `llama`→meta, `vllm`/`compat`→custom.

## 2. Config: one file, layered

- **File:** `~/.craft/ai_config.json` (`CraftAiConfig`, `#[serde(default)]`
  so old files keep loading). Fields: `provider`, `model`,
  `ollama_endpoint`, `lmstudio_endpoint`, `endpoint_override`,
  `custom_endpoint`, `custom_api_key`, plus one key slot per cloud
  provider. New fields are always optional-with-default.
- **Env wins for routing (automation/CI), never for secrets storage:**
  `CRAFT_AI_PROVIDER`, `CRAFT_AI_MODEL`, `CRAFT_AI_BASE_URL`
  (→ endpoint override), `OLLAMA_HOST`. Keys resolve file → provider env
  (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`,
  `META_API_KEY`, `OPENROUTER_API_KEY`, `CUSTOM_API_KEY`).
- **Keys are presence-flags in every API.** `redacted_llm_view()` and the
  `keys_present` booleans are the only shapes that cross
  dispatch/MCP/UI boundaries. A key value in a log, JSON reply, or error
  string is a defect. Password fields start empty every launch; only
  non-empty entries are stored.
- **Missing pieces upstream:** `standards/patterns/api_key_management.md`
  is referenced by `LLM_AND_INSTALL_TIERS.md` but does not exist. Key
  handling for Rust craft apps is defined *here* until that file lands.

## 3. Transport rules (all hard-won, do not "simplify")

1. Ollama `/api/chat` sends `"stream": false` — otherwise the server
   returns NDJSON and single-JSON parsing silently degrades to fallback
   text (observed fleet-wide, 2026-11-05).
2. Small-context options on Ollama only (`num_ctx` 8192, `num_predict`
   cap): loop prompts are kilobytes; a 128k+ default KV cache burns VRAM
   and forces CPU offload. OpenAI-compatible endpoints must NOT receive
   the `options` field.
3. Thinking models get `"think": false` for agentic calls, or a short tool
   call drowns in a 60s reasoning trace (fleet BONSAI note: +11s preamble).
4. `curl.exe` with `--max-time`, argument arrays (no shell quoting needed).
   Sync helpers for UI/MCP; async `complete()` keeps its blocking spawn.
5. LM Studio needs no key; Anthropic has no list endpoint (rule 6 below).

## 4. Engine operations (port of `templates/llm/llm_engine.py`)

All in `craft-ai-core::providers`, sync, curl-based, zero new deps:

- `list_models(config, kind)` — live lists; errors (never fakes) when a
  required key is absent, including Anthropic-without-key.
- `probe(config, kind)` — `{reachable, models[], note}`.
- `switch_ollama_model(config, keep)` — evict every OTHER resident via
  `POST /api/generate {"keep_alive": 0}`, then warm `keep` (1-token
  generate). Empty `keep` evicts all. **Saving a selection switches VRAM,
  never just config** (SETTINGS_LLM rule 4).
- `ollama_residents(config)` / `gpu_vram()` — telemetry for Settings.

## 5. L3 Settings UI contract (egui port of SETTINGS_LLM.md's 7 rules)

1. **File is truth.** Settings reads `~/.craft/ai_config.json` (re-read on
   Refresh — this makes CLI/MCP edits visible live). No in-memory-only
   config structs that nothing reads.
2. **Never auto-pick.** Empty model = nothing selected. Fresh installs and
   provider switches start empty. (Fleet BUG-030 was `models[0]`.)
3. **Save switches VRAM** (Ollama: evict + warm) and reports both.
4. **Kick-out + telemetry.** One-click evict-all, used/total VRAM readout,
   residents list with MB each. No key ever displayed back.
5. **Test validates.** Test button runs a live short completion through the
   selected provider and reports `ok` only on a live reply. Curated names
   without a key are `ok: false` (fleet BUG-042).
6. **Send-time guard.** Agent paths re-read the live selection and refuse
   with "pick one in Settings" when empty. No fallback model, ever.
7. **Keys per provider, password fields, presence dots.** Save accepts
   empty = keep stored value.

Worker pattern (egui is immediate-mode): blocking provider calls run on a
`std::thread::spawn` + `mpsc` channel, polled non-blockingly per frame
with a spinner. Never block the UI thread on network.

## 6. L2 MCP contract (every craft app exposes the same six tools)

`<app>_llm_status` (redacted config + configured-provider probe),
`<app>_llm_list_models {provider?}`, `<app>_llm_select {provider, model}`
(persists + VRAM switch), `<app>_llm_set_key {provider, api_key}`
(local-only; never echoed), `<app>_llm_evict {keep?}`,
`<app>_llm_test {prompt?}` (capped, truncated reply).
CLI mirrors them 1:1 (`llm status|list|use|set-key|evict|test`).
Codercraft (`codercraft_llm_*`) is the reference implementation.

## 7. Migration

- **New apps:** depend on `craft-ai-core`, use `CraftAiConfig` +
  `providers::*` directly. No local provider enums.
- **gamecraft-forge:** keep `llm.rs` working; when touched, delegate
  provider table + listing to `craft-ai-core` (keep its `auto()` UX and
  JSON-schema discipline — it is the richer caller).
- **Docs:** INSTALL.md keeps the Tier A (Ollama/LM Studio) + Tier B
  (cloud key) sections per `LLM_AND_INSTALL_TIERS.md`; webapp/egui
  Settings implements §5; `docs/CONFIGURATION.md` documents the env vars.

## Changelog

| Date | Change |
|------|--------|
| 2026-11-06 | Initial: provider table, config layering, transport rules, engine ops, egui UI contract, MCP contract. Reference impl: `craft-ai-core::providers` + codercraft L1/L2/L3. |
