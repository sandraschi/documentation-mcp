# Glimmer Fleet Strategy — The 4090 Monopoly (2026-08)

**Status**: Strategy / operations
**Date**: 2026-08-14
**Cross-references**: [`models/MUSE_GLIMMER_30B.md`](../models/MUSE_GLIMMER_30B.md) (model card) · [`patterns/LLAMA_CPP_NATIVE_MODEL_SERVING.md`](../patterns/LLAMA_CPP_NATIVE_MODEL_SERVING.md) (serving playbook) · `local-llm-mcp/docs/GLIMMER.md` (full guide) · [`deepseek-v4-fleet-strategy.md`](./deepseek-v4-fleet-strategy.md) (cloud lane) · [`llm-token-market-2026-08.md`](./llm-token-market-2026-08.md) (price-war hedge)

---

## TL;DR

Muse Glimmer 30B is the fleet's local workhorse: free, agentic-class (MCP-Atlas 75.5 vs Gemma4-31B's 54.2), multimodal, Apache 2.0, ~40 tok/s with the DFlash drafter. Its one cost is **exclusivity**: ~21 GB of the 4090's 24.5 GB resident, always — Ollama models cannot run concurrently, and Ollama cannot even load its kquant GGUF (native llama.cpp is the only path).

The scheduling rule follows from that:

1. **Long runners use Glimmer directly** (`llama-server` :11439 via the :11435 proxy) when quality matters or nothing else needs the GPU.
2. **Purge → Ollama (e.g. Gemma 4 12B) → restart Glimmer** only when the job needs VRAM elasticity, raw throughput, or headroom for parallel GPU work.
3. **Never pick Gemma for quality.** It is not better than Glimmer — it is better *differently* (below).

---

## 1. Why Glimmer Is the Default

| Dimension | Value |
|-----------|-------|
| Cost | Free — own GPU, own electricity; the exact hedge the token-market doc §5 wants |
| Agentic | MCP-Atlas 75.5 — beats Gemma4-31B (+21), Qwen3.6-27B (+13) |
| Multimodal | Screenshots, charts, documents (4K visual tokens/image) |
| Context | 131K native |
| Speed | ~40 tok/s with DFlash speculative decoding (RTX 4090) |
| License | Apache 2.0, open weights on HF |
| Reasoning | Controllable effort (low/medium/high/xhigh), `reasoning_content` extraction |
| Consumers | opencode (`local-llama/muse-glimmer-30b`), aiwatcher distillation, arxiv-mcp epistemic jobs |

**The asymmetric win**: cloud DeepSeek V4 Flash costs zero VRAM, so Glimmer and Flash are tandem by role, never rivals — Glimmer owns the GPU lane, Flash owns the always-on lane (see `local-llm-mcp/docs/GLIMMER.md` §8). The only real contention is **intra-GPU**: Glimmer vs Ollama.

---

## 2. The Contention Problem

```
RTX 4090 — 24.5 GB VRAM
├── Glimmer resident:  ~21 GB   (15.6 GB kquant-17gb + mmproj + 3.5 GB KV cache @131K + drafter)
└── Leftover:           ~3.5 GB (nothing meaningful fits)
```

- Ollama models **cannot** load while Glimmer runs.
- Ollama **cannot** load Glimmer's kquant GGUF at all (as of 2026-08-11) — native llama.cpp is mandatory for Glimmer.
- Glimmer holds its VRAM **even when idle** — it is a resident monopoly, not a demand-loaded service.

So the fleet's two local worlds are mutually exclusive: the Glimmer world (agentic, multimodal, native llama.cpp) and the Ollama world (Gemma 4 12B, Qwen3, small models, demand-loaded, self-healing).

---

## 3. The Decision Matrix — Engine per Job Type

| Job | Engine | Why |
|-----|--------|-----|
| Agentic tool loop (opencode session, deep research) | **Glimmer** | Agent-class quality, tool use, reasoning |
| Multimodal (screenshots, charts, docs) | **Glimmer** | Only local engine with vision |
| Privacy-sensitive / offline | **Glimmer** | Zero telemetry, works air-gapped |
| Bulk distillation / mass token processing (aiwatcher-style) | **Ollama + Gemma 4 12B** | 2-3x tok/s on a 12B; elastic VRAM; per-request load/unload |
| Quick classify / summarize / extract between other GPU work | **Ollama + Gemma 4 12B** | Loads on demand, releases VRAM when idle (`keep_alive`); does not pin the GPU |
| Anything while the 4090 is ALSO needed (training, image gen, VLA sim, video) | **Ollama + Gemma 4 12B** | ~8-9 GB footprint leaves the GPU usable for the second workload |
| Anything when Glimmer is down (crash, cold restart) | **Ollama + Gemma 4 12B** | Ollama self-heals per request; Glimmer cold-load is 60-90s and manual |
| Scheduled runner at a fixed hour | **Glimmer** if GPU idle then; **Ollama** if the window collides with other GPU work | Peak-avoidance, same logic as cloud peak-hour pricing |

### "Why would Gemma 4 12B ever be better than Glimmer?"

Straight answer: **it is never better on quality — it is better on four operational axes:**

1. **Throughput, not latency.** Glimmer's ~40 tok/s is a ~30B model decoding with a 131K KV cache. A 12B at Q4 decodes at 2-3x that rate. For jobs measured in megatokens (distillation passes, bulk summarization), wall-clock time wins — the model is *dumb enough to be fast*.
2. **VRAM elasticity.** Ollama loads on demand and (with default keep_alive or explicit `keep_alive=0`) **releases VRAM when idle**. Glimmer pins 21 GB forever, even at 3 AM doing nothing. On a machine where the 4090 is a shared resource (image gen, training, MuJoCo sim, video pipelines), the elastic model is the courteous one.
3. **Self-healing.** Ollama restarts a crashed model on the next request, automatically. Glimmer is a single long-lived `llama-server` — if it dies at 2 AM, the scheduled job dies with it, and nothing restarts it.
4. **Headroom.** Gemma 4 12B (~8-9 GB) coexists with a second GPU workload; Glimmer leaves ~3.5 GB, which fits nothing.

And one honest **anti-reason**: if the 4090 is dedicated to Glimmer anyway (nothing else ever needs it), none of the four apply — then Glimmer is strictly better and Gemma is a downgrade. Do not add the purge/restart dance without the contention.

---

## 4. Operating Playbook — The Purge / Restart Cycle

Supervision: `llm_engine(operation="status")` (local-llm-mcp) — processes, ports, VRAM per engine, loaded models. Start/stop engines via `llm_engine(operation="start|stop", engine="llama")`.

### Purging Glimmer (before an Ollama job)

```powershell
# 1. Stop the supervisor-managed engine (kills llama-server + proxy)
#    llm_engine(operation="stop", engine="llama")   # or manually:
# 2. Verify VRAM actually freed (nvidia-smi VRAM % of the 4090 back near idle)
nvidia-smi --query-gpu=memory.used --format=csv
# 3. Start the Ollama job (Gemma 4 12B etc.). Ollama demand-loads and unloads.
```

### Restarting Glimmer (after the Ollama job)

```powershell
# 1. Ollama idle-unloads by itself; force it if the job lingers
#    (ollama stop <model> or keep_alive=0 on the runner)
# 2. Bring Glimmer back — ops script lives at D:\Dev\models\muse-glimmer\
& D:\Dev\models\muse-glimmer\start-muse-glimmer.ps1
# 3. Cold load is 60-90s. Verify:
#    GET http://127.0.0.1:11439/health   (llama-server)
#    GET http://127.0.0.1:11435/health   (truncating proxy)
```

### Consumer rewiring (when the runner is a fleet server, not a shell)

| Consumer | Glimmer config | Ollama config |
|----------|----------------|---------------|
| aiwatcher distillation | `LLM_BASE_URL=http://127.0.0.1:11435/v1` | `LLM_BASE_URL=http://127.0.0.1:11434/v1` |
| arxiv-mcp epistemic jobs | `ARXIV_MCP_SAMPLING_BASE_URL=...:11435/v1` | `...:11434/v1` |
| opencode | provider `local-llama/muse-glimmer-30b` | provider `ollama` |

**Rule**: a long runner that will outlive its window should be pointed at Glimmer from the start (no mid-job engine swap). Plan the engine *before* launching the job — the purge/restart cycle costs 5 minutes either way.

---

## 5. Failure Modes & Quick Hits

| Symptom | Cause / Fix |
|---------|-------------|
| 1-3 tok/s on Glimmer | Something else holds the GPU — stop the other engine |
| "Ready." / "Context loaded." | Agent-mode flip — system truncation slipped; restart the proxy (start-muse-glimmer.ps1) |
| Ollama model won't start (OOM) | Glimmer still resident — purge first, verify with nvidia-smi |
| Scheduled job died overnight | See §5.1 — the watchdog is the insurance; job-side fallback is the second layer |
| Empty answer after thinking | Reasoning consumed the 1024 budget — shorten prompt |

### 5.1 Insurance — The 3 AM Watchdog (INSTALLED 2026-08-14)

A lone `llama-server` has no self-healing: it dies at 3 AM and the 9 AM discover is
the real failure. Two layers of insurance:

**Layer 1 — `watch-glimmer.ps1` (system-side, implemented):**

- Lives at `D:\Dev\models\muse-glimmer\watch-glimmer.ps1`; registered as scheduled
  task **`Watch-MuseGlimmer`** (every 5 min, `-StartWhenAvailable`, 3 restarts).
- Each run: health-checks `:11435` (proxy) and `:11439` (llama-server). Healthy =
  silent exit, zero log spam. Any endpoint down = kill stale processes → wait for
  port release → relaunch via `start-muse-glimmer.ps1` (which itself waits up to
  5 min for health) → log `RESTARTED OK` / `RESTART FAILED` to `watchdog.log`.
- Log: `D:\Dev\models\muse-glimmer\watchdog.log`. Sandra's 9 AM check is one
  `Get-Content watchdog.log -Tail 20` — every 3 AM death is a timestamped line.
- **Paging (wired 2026-08-15)**: on `RESTART FAILED` the watchdog alerts via a
  three-rung ladder, each rung logged (never a silent swallow):
  1. robofang `POST :10871/api/v1/events` (event `GLIMMER_RESTART_FAILED`, urgency 10)
  2. speech-mcp TTS `POST :10909/api/v1/tts` (provider `windows`) — the real gateway;
     the old `:10895` was a phantom endpoint
  3. **SAPI5 spoken fallback** (`System.Speech` — works with no external services)
  Test: `watch-glimmer.ps1 -TestAlert`. All rungs verified 2026-08-15 02:48
  (robofang + TTS green; SAPI is the guaranteed last rung).
- Reinstall after edits: `powershell -File D:\Dev\models\muse-glimmer\watch-glimmer.ps1 -Install`
- Uninstall: `Unregister-ScheduledTask -TaskName Watch-MuseGlimmer -Confirm:$false`

**Layer 2 — job-side fallback chain (doctrine for runners):**

The watchdog restarts within minutes, but a scheduled runner whose timeout is
shorter than the 60-90 s cold load (or that fires during a restart window) still
dies. Consumers must therefore declare a fallback chain, Glimmer first:

```
Glimmer (:11435)  ->  Ollama Gemma 4 12B (:11434)  ->  DeepSeek V4 Flash (cloud)
     local/agentic          local/elastic                always-on, zero VRAM
```

- Probe `http://127.0.0.1:11435/health` (5 s timeout) before the job; on failure
  advance one link. Do not retry a dead Glimmer 20 times.
- Config so far: aiwatcher (`LLM_BASE_URL`), arxiv-mcp epistemic jobs
  (`ARXIV_MCP_SAMPLING_BASE_URL`). Add the fallback probe to any new runner.
- The chain is why the token-market hedge (DeepSeek cloud) and the Glimmer local
  lane are not rivals: the cloud lane IS the last rung of the availability ladder.

---

## 6. Fleet Doctrine Summary

1. **Glimmer is the local default** for anything agentic, multimodal, private, or quality-sensitive.
2. **Gemma 4 12B (Ollama) is a throughput/elasticity tool, not a quality tool** — use it when tokens-per-second, VRAM release, or GPU headroom matter more than intelligence.
3. **Never run both local worlds at once** — 21 GB resident means no coexistence. Plan the engine before the job, not during it.
4. **Cloud (DeepSeek V4 Flash) is the zero-VRAM lane** — tandem with either local engine, never a rival.
5. **The purge/restart cycle is the price of the monopoly** — keep `start-muse-glimmer.ps1` and the two health checks in the ops toolkit; a 60-90s cold load is acceptable, a dead-at-2-AM runner is not. The `Watch-MuseGlimmer` scheduled task (§5.1) is the standing answer to the dead-at-2-AM case; runners add the Glimmer→Ollama→DeepSeek fallback chain as their own insurance.

---

## 7. References

- [Muse Glimmer 30B — model card](../models/MUSE_GLIMMER_30B.md)
- [Native llama.cpp serving pattern](../patterns/LLAMA_CPP_NATIVE_MODEL_SERVING.md)
- [Muse Glimmer complete guide — local-llm-mcp](https://github.com/sandraschi/local-llm-mcp/blob/master/docs/GLIMMER.md)
- Ops: `D:\Dev\models\muse-glimmer\STATUS.md` + `start-muse-glimmer.ps1`
- Cloud lane: [`deepseek-v4-fleet-strategy.md`](./deepseek-v4-fleet-strategy.md) · [`llm-token-market-2026-08.md`](./llm-token-market-2026-08.md)
