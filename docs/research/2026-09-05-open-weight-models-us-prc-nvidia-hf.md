# Open-Weight Frontier 2026-09: US (Meta) vs PRC Biweekly, DGX Monsters & 4090 Quants, Nvidia x Hugging Face

**Date:** 2026-09-05 (Europe/Vienna) | **Author:** Sandra S. / Fleet Research (Goliath)
**Status:** Research doc - living, update biweekly
**Context:** Spark 1.3 `xhigh` -> 61 AA Index (2026-09-02), Glimmer 30B local (2026-08-09) as 4090 backstop for `muse-spark-1.3-contributor` ($0.20/M). PRC open models now ship biweekly, some trained without Nvidia, weights on HF. Nvidia -> HF $10B+ acquisition (reported 2026-09, per user + GH chatter) signals Jensen all-in on open weights.

---

## TL;DR

- **US open-weight = Meta alone.** OpenAI (GPT-5.6), Anthropic (Claude 5.x), Google (Gemini 3.8), xAI (Grok 4.6) are API-closed. **Meta Superintelligence Lab** is the sole US lab shipping Apache 2.0 / MIT frontier weights at cadence: **Muse Spark 1.3** (API, 61-62 AA Index), **Muse Glimmer 30B** (open, 18GB Q4, 4090-able), plus **audio transcription** (this week) and **picture-gen** (last week) - velocity noted as *commendable*.
- **PRC open-weight = biweekly deluge.** **DeepSeek V4 / V4-Flash**, **Qwen3 / Qwen3.5-MoE**, **Moonshot Kimi K2**, **Zhipu GLM-4.x** ship every ~2 weeks, Apache 2.0 / MIT. Some trained on **Huawei Ascend 910B** (no Nvidia) to dodge export controls; some are **huge MoE monsters** (400B-1T active) for DGX boxes. HF downloads: `Qwen3-0.6B 21M`, `Qwen3.6-35B-A3B-FP8 13M`, `DeepSeek-V4-Flash 4.5M`.
- **Weights = HF. Corp vs solo split:** Full BF16/FP8 monsters for DGX/H100 clusters; **quants** (GGUF Q4_K_M, AWQ INT4, GPTQ, MLX 4-bit, NVFP4) for solo dev 4090 24GB. Same repo, different artifact.
- **Nvidia + HF ($10B+):** If closed, Jensen vertically owns **distribution + inference** (HF Hub + DGX + NIM + NIMS + Blackwell). Open weights become Nvidia's moat against closed APIs - contrary to 2023-24 "open is dead" narrative.

---

## 1. US: Meta as Sole Open-Weight Competitor

### 1.1 What "sole" means in 2026
| Lab | Frontier model | Weight | License | AA Index (2026-09-02) |
|-----|---------------|--------|---------|----------------------|
| **Meta** | **Muse Spark 1.3 xhigh / max** | API only (for now) | - (API) | **61 / 62** |
| **Meta** | **Muse Glimmer 30B** | **Open** | Apache 2.0 | ~48-50 est (tool-use tuned) |
| **Meta** | Llama 4 family (heritage) | Open | Custom | - |
| OpenAI | GPT-5.6 Sol max | Closed | - | 61 (tie) |
| Anthropic | Claude Fable 5.1 max / Opus 5 max | Closed | - | 66 / 63 |
| Google | Gemini 3.8 Flash high | Closed | - | 59 |
| xAI | Grok 4.6 high | Closed | - | 61 |

Only Meta ships **both** a frontier API (Spark) *and* an open 4090-class model (Glimmer) under Apache 2.0.

### 1.2 Meta Superintelligence Lab velocity (Aug-Sep 2026)
Per `research.meta.ai/blog/introducing-muse-spark-1-3` + fleet notes:

- **Spark 1.3** (2026-09-02): +4 AA (57->61 xhigh, 62 max), Tau3-Banking 35%->47%/52% (#1), GDPval +94/+139 Elo, ~20% fewer tool calls / ~25% fewer tokens vs 1.2 on coding (Meta engineers). 128K, text+image, $1.25/$4.25 standard / $0.20 contributor.
- **Glimmer 30B** (2026-08-09): `meta-models/Muse-Glimmer-30B` 633k pulls, `unsloth GGUF` 1M pulls, `ollama: muse-glimmer:30b` 18GB Q4 - single-GPU agent model. Tuned for tool-use / failure recovery.
- **Audio transcription** (week of 2026-09-01, new) + **picture-gen** (prior week, new) - not detailed in this doc but noted as Lab shipping breadth (speech + vision + code + agents in 14 days). See `ai/muse-glimmer-30b-local-on-rtx-4090-backstop-for-spark-contributor`.

**Take:** Lab is executing the "open core + cheap API" play that US peers abandoned in 2024-25.

### 1.3 Why US peers went closed
Economics: inference at scale favors closed + caching + $20/user/mo bundles. Open weights cannibalize. Meta's ad stack subsidizes open as distribution.

---

## 2. PRC: Biweekly Open-Weight Cadence

### 2.1 Cadence & protagonists (mid-2026)
Via `huggingface.co/api/models?search=...` (2026-09-05 snapshot):

- **DeepSeek:** `DeepSeek-V4-Flash-0731` 4.5M pulls (MIT), `DeepSeek-OCR` 2.4M, `deepseek-v4-gguf` 1.9M (GGUF quants). V4 family is MoE, FP8, context caching focus. Sister `DeepSeek V4 Pro` is fleet default pre-Spark.
- **Qwen (Alibaba):** `Qwen3-0.6B` **21M** pulls (Apache 2.0), `Qwen3.6-35B-A3B-FP8` **13M**, `Qwen3-8B` 13M. Qwen3/Qwen3.5-MoE ships dense + MoE variants, 0.6B to 35B-A3B to ~400B.
- **Kimi (Moonshot) / GLM (Zhipu):** K2, GLM-4.x ship interleaved biweekly with DeepSeek/Qwen. Pattern: one PRC lab drops MoE monster, next week another drops dense + quants.
- **Cadence proof:** In 5 months, Muse *alone* did 4 Spark releases; PRC side did ~8-10 across 4 labs (~1 per 1.5 weeks).

### 2.2 Trained without Nvidia?
Multiple PRC releases note **Huawei Ascend 910B / 910C** training (papers cite `arxiv:2504...`, `arxiv:2602...` on Glimmer tags as analog). Not all, but a growing slice explicitly markets "Nvidia-free" to signal export-control resilience. Implication: CUDA moat eroding at training layer, even if inference still Nvidia-dominated.

### 2.3 Huge & Hungry
PRC MoEs are **monster scale**: base checkpoints often **200GB-400GB BF16** (e.g., DeepSeek V4 ~ 400B MoE, Qwen3-235B-A22B). Designed for **DGX H100 x8 / B200** clusters, not single GPU. That's the "corp dl monster" tier.

---

## 3. Hugging Face as the Commons

### 3.1 Weights live on HF, not GitHub Releases
All models above publish **full weights** to `huggingface.co/meta-models`, `Qwen/*`, `deepseek-ai/*`. HF is the `npm` for weights.

Snapshot 2026-09-05 (downloads = all-time):
- `Qwen/Qwen3-0.6B` 21.9M, `Qwen3.6-35B-A3B-FP8` 13.5M, `Qwen/Qwen3-8B` 13.5M
- `deepseek-ai/DeepSeek-V4-Flash-0731` 4.5M
- `meta-models/Muse-Glimmer-30B` 633k, `unsloth GGUF` 1,038k, `lmstudio-community GGUF` 438k

### 3.2 Two artifact tiers from one repo
| Tier | Artifact | Size | Runs on | User |
|------|----------|------|---------|------|
| **Corp / DGX** | `BF16` / `FP8` / `NVFP4` safetensors | 40-400GB | DGX H100x8, B200, local NVLink | Corp datacenter, inference provider |
| **Solo / 4090** | `GGUF Q4_K_M`, `Q6_K`, `AWQ INT4`, `GPTQ`, `MLX 4-bit`, `EXL3` | 18-35GB | RTX 4090 24GB, 4080 16GB (with offload) | Solo dev, fleet opencode local |

Example: Glimmer 30B offers `18GB Q4` (4090) **and** `59GB BF16` (DGX) from same base. DeepSeek V4 offers `antirez/deepseek-v4-gguf` 1.9M pulls alongside FP8 base. Qwen offers FP8 + GGUF in same org.

**Fleet relevance:** `opencode` can flip `model: ollama/muse-glimmer:30b` (local, free) <-> `meta/muse-spark-1.3-contributor` (cloud, $0.20/M) with zero code change - same prompt, different deployment.

---

## 4. Hardware Divergence: With vs Without Nvidia

- **With Nvidia:** Still dominant for frontier training & all inference. DGX + Blackwell + NIM stack is the deployment path for monster weights. Solo quants exist *because* Nvidia consumer cards (4090) are ubiquitous.
- **Without Nvidia:** Ascend 910B trails H100 in raw FLOPs but PRC labs report competitive training via **MoE sparsity** (fewer active params) + **FP8** + **longer wall-clock**. Signal is **sovereignty**, not speed: they can ship biweekly even under export controls.

**Result:** Open-weight ecosystem is now **hardware-heterogeneous by design** - weights are portable, kernels are not.

---

## 5. Nvidia Acquires Hugging Face ($10B+, 2026-09)

### 5.1 What was reported
Per user report + GH repo `musman550/musfira-ai-nvidia-buying-hf-isnt-a-good-thing-for-open-source` (2026-09), **Nvidia announced acquisition of Hugging Face for $10B+**. `duckduckgo` fetch for `nvidia acquires hugging face 10 billion` was connection-reset on 2026-09-05, so treat as **reported, not independently verified** here - awaiting filing/PR.

### 5.2 Why Jensen would go all-in on open weights
If true, it's vertical integration:

- **Before:** Nvidia sold shovels (DGX/GB200), HF sold the map (Hub). Labs sold picks (weights) via HF.
- **After:** Nvidia owns **map + shovels + storefront** (Hub + DGX Cloud + NIM/NIMS + Blackwell). Open weights become **Nvidia's distribution moat** against closed-API peers (OpenAI/Anthropic). Every `Qwen`/`DeepSeek`/`Glimmer` pull drives a DGX deployment.

This inverts 2023 thesis ("open is dead, closed wins"). Jensen betting **open wins, and Nvidia captures the runtime**.

### 5.3 Implications
- **For PRC labs:** HF was neutral commons; under Nvidia, PRC weights still hostable but distribution is now US-vendor-owned. Expect mirrors (`modelscope.cn`, `wisemodel.cn`) to gain.
- **For solo devs:** HF remains free for pulls; risk is **Hub + inference bundling** (NIM-first). Mitigation: `git lfs clone` + local GGUF already cached; fleet keeps local ollama path.
- **For Meta:** Sole US open-weight peer now *distributes via competitor's store*. Incentive to mirror via `meta.com` direct pulls (already does for Glimmer).

---

## 6. Implications for Fleet / Corp / Solo

| Actor | Play |
|-------|------|
| **Corp (DGX boxes)** | `git lfs` monster `BF16/FP8` to DGX, run via `vLLM` / `TensorRT-LLM` / NIM. Use for internal rag/coding agents where data can't leave. PRC MoEs are cheap to try, expensive to serve (MoE router overhead). |
| **Solo dev (4090)** | `GGUF Q4_K_M` via Ollama/LM Studio. Glimmer 30B is the *current* best 4090 open-agent (18GB, 32K ctx safe). Qwen3 30B / DeepSeek V4 GGUF are alternatives. Keep `muse-spark-1.3-contributor` as primary ($0.20/M), Glimmer as fallback. |
| **Fleet (213 repos)** | Fleet hub `opencode.json` stays `muse-spark-1.3-contributor` (cheap frontier at 61 AA). Documented fallback path to `ollama/muse-glimmer:30b` in `docs/opencode/CONFIG.md`. HF acquisition does not change `ollama` local path - already cached. |

---

## 7. Risks & Watch Items (update biweekly)

1. **PRC cadence fatigue:** Biweekly is unsustainable - watch for quality vs churn. Track AA Index per PRC drop, not just HF pulls.
2. **Nvidia-HF close conditions:** Regulatory (CFIUS) + PRC mirror drift. If HF Hub throttles PRC weights, fleet needs `modelscope` mirror fallback.
3. **License drift:** Meta Apache 2.0 vs PRC Apache 2.0/MIT stable *today*; watch for custom "open but not commercial" clauses.
4. **Quant quality:** Q4_K_M vs Q8_0 vs FP8 spread is 2-4 AA points. Solo devs should bench at `Q6_K` before assuming Q4 is enough for agentic tasks (Tau3-Banking sensitive).
5. **Training-hardware claims:** "No Nvidia" papers need independent verification - watch MLPerf, not marketing.

---

## 8. Sources & Provenance

- **HF API 2026-09-05:** `huggingface.co/api/models?search=muse-glimmer` (633k/1M pulls), `?search=Qwen3` (21M/13M), `?search=DeepSeek` (4.5M) - fetched via `curl.exe` on Goliath.
- **Ollama:** `ollama.com/library/muse-glimmer` + `/tags` (18GB Q4, 59GB BF16, 19GB MLX, 128K) - fetched 2026-09-05.
- **Meta:** `research.meta.ai/blog/introducing-muse-spark-1-3` (Spark 1.3, Glimmer 30B) + `developer.meta.com/ai/models/muse-spark` snippets.
- **AA:** `artificialanalysis.ai/articles/muse-spark-1-3` (61/62, Tau3 47%/52%, GDPval +94/+139) - fetched 2026-09-05.
- **Nvidia x HF:** User report 2026-09-05 + `api.github.com/search/repositories?q=hugging+face+nvidia+acquisition` (repo `musman550/...` describing acquisition) - **not yet verified via primary PR**, marked as reported.

---

## 9. Next Steps for MCD

- [ ] Mirror this doc to `llms/models/OPEN_WEIGHT_2026.md` index + `docs/opencode/CONFIG.md` fleet default stays linked here.
- [ ] Add `scripts/just` recipe `just hf-pull` for DGX monster vs 4090 quant tier selection.
- [ ] Biweekly cron: `huggingface.co/api/models?search=Qwen|DeepSeek|Kimi|GLM` + `ollama tags` snapshot -> append to this doc's appendix.
- [ ] Track Nvidia-HF filing; if confirmed, add `standards/HF_MIRROR_STRATEGY.md`.

---

## 10. Addendum 2026-09-05 - Claude / Antigravity $20 pcm overage

**User observation (Sandra, Goliath):** Both **Claude** and **Antigravity** on **$20 pcm** accounts now permit **multi-hour dev sessions** with little timeout/rate-limit annoyance - a change from earlier throttling. **Sonnet** and **Gemini 3.1 Flash** are powerful at this tier and handle fleet `assfix` sweeps.

**Catch: $1/min overage.** Activating usage tokens **over allowance** bills ~**$1 per minute** (wall-clock, not per-token). That's $60/hr - *ka-ching* - vs Spark contributor $0.20/M output or Glimmer local $0 watts. At Spark's $0.55/task (AA Index), $1/min is worse than contributor even at 60 tok/s.

**Fleet take:**
- $20 tier is now viable for sustained sessions - no need to jump to Pro/Max for multi-hour runs. Keep a hard cap at ~80% allowance and fallback to `muse-glimmer:30b` / `qwen3` local.
- Track `$1/min` as the cliff in cost docs - memops note `fleet/claude-antigravity-20-pcm-multi-hour-dev-sessions-1-per-minute-overage` is canonical for this.

---

## 11. Addendum 2026-10-05 - Strata: 125B local on a gaming PC (HN front page, ~12k stars in days)

**Repo:** https://github.com/Niko1221/Strata | **Found via:** HN front page, NOT fleet intel (see s7 gap note in full doc).
**Full doc:** `research/2026-10-05-strata-qwen38-flash-next-local-125b.md` (canonical for Strata; this section is the landscape-level summary).

- **What:** Qwen3.8-Flash-Next 125B MoE on one consumer GPU + RAM (12GB VRAM / 32GB RAM min, 64GB recommended). OpenAI + Anthropic + Responses APIs on localhost. MIT. `START-HERE.bat` / `setup.sh` + own MCP server (`strata_status/models/install/start/stop/logs/benchmark/connect_info`).
- **Speed (vendor-measured, RTX 5070 12GB):** Q2_0 94 tok/s write / 2650 tok/s prefill; IQ2_XS 79/2090; IQ3_S 53/1620. 24GB cards projected ~100-140 tok/s (UNVERIFIED until Goliath `--calibrate`).
- **Goliath fit:** IQ2_XS recommended at 64GB (39.2GB); IQ3_XXS/IQ3_S fit with little else open; Coder (half experts, 91% SWE-bench Verified per authors) for 32GB rigs.
- **Landscape shift:** breaks the "monsters for DGX vs 30B quants for 4090" split in s2-s3 above. First credible local 100B+ at >reading speed on a 4090, with a Windows double-click installer. Versions: qwen / coder / swift (short-think fine-tune) / unsloth 4-bit (needs ~80GB RAM, skip).
- **Hard constraints:** default port 8080 is FORBIDDEN per `operations/WEBAPP_PORTS.md` (claim 10700-15000 first); ~70GB download to a drive with 80GB+ free (never D:); first start pins 35-55GB RAM for 1-3min (normal); page file must be System-managed.
- **Intel lesson:** firefront/codehunt scan arXiv only and would never surface a GitHub-release like this. Filed `sandraschi/aiwatcher-mcp#11` (HN front-page + GH star-velocity discovery) as the fix direction.

---

*Fleet note: This doc is the canonical open-weight landscape for `mcp-central-docs`. Link from `ai/muse-glimmer-30b-local-on-rtx-4090-backstop-for-spark-contributor`, `fleet/claude-antigravity-20-pcm-multi-hour-dev-sessions-1-per-minute-overage` and `docs/opencode/CONFIG.md`. Update on every PRC biweekly drop and Meta Lab ship.*
