# Strata: Qwen3.8-Flash-Next 125B on a Gaming PC — Local Frontier, 12k Stars in Days

**Date:** 2026-10-05 (Europe/Vienna) | **Author:** Fleet Research (Goliath, with Sandra)
**Status:** Living research + integration doc | **Location:** `mcp-central-docs/research/`
**Companion to:** `2026-09-05-open-weight-models-us-prc-nvidia-hf.md`, `2026-10-01-glm-5.3-opencode-fleet-integration.md`, `llms/LOCAL_VLLM_CODING_AGENT_RECIPE.md`
**Repo:** https://github.com/Niko1221/Strata | **Found via:** HN front page (user report 2026-10-05), NOT via fleet intel stack

## 0. TL;DR + Verification Matrix

Strata runs **Qwen3.8-Flash-Next (125B MoE)** on one consumer GPU + system RAM (12GB VRAM min, 32GB RAM min, 64GB recommended) and serves **OpenAI-compat + Anthropic-compat + Responses API** on localhost. MIT licensed. One-click `START-HERE.bat` / `setup.sh`, plus its own MCP server (`tools/strata_mcp.py`) so coding agents can install/start/stop it. On Goliath (4090 24GB + 64GB RAM) this is the first credible local 100B+ coding/general model at >reading speed.

| Claim | Status 2026-10-05 | Source |
|---|---|---|
| Repo exists, 11,975 stars / 1,031 forks / 105 issues, desc "Qwen3.8-Flash-Next on any consumer hardware" | **VERIFIED** | `github_ops repo_view Niko1221/Strata` 2026-10-05 |
| 12k stars in a few days, HN front page | **USER-REPORTED, PLAUSIBLE** — star count verified, velocity + HN rank not independently fetched | user report; star count from API |
| RTX 5070 12GB: Q2_0 94 tok/s write / 2650 tok/s prefill; IQ2_XS 79/2090; IQ3_S 53/1620. RX 9070 XT: 60/1160, 52/1110, coder 44/1420 | **VERIFIED (vendor-reported, setup-measured)** | README + `docs/MODELS.md` fetched 2026-10-05 |
| RTX 3090 24GB ~100-140 tok/s projection | **VENDOR ESTIMATE, NOT MEASURED** | MODELS.md estimate line |
| Requirements: NVIDIA RTX 20/30/40/50 or listed AMD, 12GB+ VRAM, 32GB+ RAM, ~80GB SSD, driver NVIDIA 580+, Win10/11 or Ubuntu 22.04/24.04 | **VERIFIED** | README + `docs/AI_SETUP.md` |
| Goliath fit: IQ2_XS recommended at 64GB, IQ3_XXS/IQ3_S fit with little else open, Coder fits 32GB | **VERIFIED (table)** | MODELS.md Pick-by-RAM |
| Coder = 256/512 experts, 91% SWE-bench Verified / 99% LiveCodeBench per authors, weak off-code + CJK (#438) | **VENDOR/AUTHOR-REPORTED** | MODELS.md Coder section |
| OpenAI base `127.0.0.1:8080/v1`, Anthropic `/v1/messages`, Responses `/v1/responses`, `reasoning_effort none/low/medium/high`, `parallel N` batching | **VERIFIED** | README Using-it + AI_SETUP.md s8 |
| MCP server with `strata_status/models/install/start/stop/logs/benchmark/connect_info`, stdio, py3.10+, safety-gated (no shell, no free paths, confirm-gated 58-111GB download) | **VERIFIED** | `docs/MCP_SERVER.md` fetched 2026-10-05 |
| Architecture: 24,576 experts, 10 active/token, GPU=hot experts / RAM=all / SSD=29GB lookup shard, MTP draft guess-and-check 1.6-1.8x, 8k-token chunked prefill 1000+ tok/s | **VERIFIED (project description)** | README How-it-works + `docs/HOW_IT_WORKS.md` referenced, paper PDF referenced but NOT fetched |
| Model dl ~70GB (94GB UD-IQ4_XS, 111GB UD-Q4_K_XL), resumable, first-start freeze 1-3min loading 35-55GB RAM is normal | **VERIFIED** | AI_SETUP.md s4-s6 |
| Independent benchmark / Goliath measurement | **NOT VERIFIED — no local run yet** | next step `--check` + `--calibrate` |

Do NOT quote vendor speed/quality rows as fleet-measured. Re-verify on Goliath before promoting to `standards/LOCAL_LLM_*`.

## 1. What Strata Is

One model (`Qwen3.8-Flash-Next` by Qwen team, quants by ISTA-DASLab / UkisAI Swift 1.5 / Unsloth), several sizes (Q2_0 / IQ2_XS / IQ3_XXS / IQ3_S), several versions (qwen / coder / swift / unsloth). Installer picks engine by card (CUDA/HIP, AMD Windows engine new in 0.1.34, ~550MB, no compile), asks model + context + vision, downloads (~70GB), writes `run-<model>.bat/.sh`, opens browser app at `127.0.0.1:8080` with Chat + live Monitor (GPU/CPU/RAM) + About.

Agent path (preferred for us): `START-HERE.bat --yes --family qwen --model IQ2_XS --no-start` then start detached and poll `/health`. Full flag table in AI_SETUP.md s4 (`--context`, `--vision yes/no/gpu/cpu`, `--gpu/--gpus`, `--backend`, `--data-dir`, `--port`, `--host/--api-key`, `--setup`, `--check`, `--calibrate`).

## 2. Why 12k Stars in Days Matters

Pent-up demand signal, not hype:

- Local 100B+ that actually runs on a 12GB gaming card at 50-90 tok/s did not exist in the fleet's 2026-09 open-weight map (that doc: monsters for DGX vs 30B-class quants for 4090). Strata bridges it via MoE-offload + speculative decode, with a Windows double-click installer.
- Distribution solved the way GLM-5.3 doc noted: one `git clone`, recommended answers on Enter, resumable HF download, OpenAI/Anthropic endpoints every agent already speaks, MCP tools so the agent does it for the user.
- HN front-page discovery proves the fleet gap (see s7): our arXiv/firefront/codehunt stack would never have surfaced this — it is not a paper, it is a release with benchmarks in docs/.

## 3. Goliath Fit (RTX 4090 24GB, 64GB RAM, Ryzen 9 5900X)

| RAM | Take | Notes |
|---|---|---|
| 64GB (us) | **IQ2_XS (recommended)** | 39.2GB RAM+VRAM, fast + better quality. IQ3_XXS (47GB) / IQ3_S (54.8GB, best=full-model parity) also fit with little else open |
| 48GB | IQ2_XS or Q2_0 (fastest, 37.6GB) | larger sizes do not fit |
| 32GB | Coder (IQ1_M, 29.6GB shard) | code-only; off-code + CJK weak. With 24GB VRAM, Q2_0/IQ2_XS run in low-RAM mmap mode |

Expectation on 24GB VRAM: more experts resident than the 12GB reference, so above the 53-94 tok/s table — 100-140 tok/s projection is plausible but UNVERIFIED until `strata_benchmark` / `--calibrate` runs here. Context default by VRAM: 32k (<14GB), 64k (<20GB), else 128k; up to 524k via `--context` + rope scaling (experimental).

Constraints: D: near-full — weights MUST go to `--data-dir` on a drive with 80GB+ free (recipe precedent: `N:\AI\hf`, never D:). GPU shared with Plex/ComfyUI — close or profile accordingly. First start pins 35-55GB RAM; page file must be System-managed on Windows or `cudaMalloc ExpertCache` fails despite free VRAM.

## 4. Fleet Integration

- **Runtime model lane:** point any OpenAI-compat client at `http://127.0.0.1:<port>/v1` (any key/name). Claude Code: `ANTHROPIC_BASE_URL=http://127.0.0.1:<port>`. Codex CLI: `/v1/responses`. Thinking via `reasoning_effort none/low/medium/high` (off=fastest). Single-flight default; `"parallel": 2` for concurrency at per-request cost.
- **Sampling lane:** candidate `ctx.sample()` / `ARXIV_MCP_SAMPLING_BASE_URL` backend for local agents (replaces/augments Ollama per `LOCAL_LLM_FIRST_DOCTRINE.md`). Needs bake-off vs vLLM recipe (`llms/LOCAL_VLLM_CODING_AGENT_RECIPE.md`: Qwen3-Coder-30B-A3B AWQ @150+ tok/s, prefix caching, continuous batching) — Strata wins on model size/quality, vLLM wins on batching/caching/tool parsers. Test both, do not assume.
- **Management lane:** add `tools/strata_mcp.py` as `strata` MCP server (Claude Code `claude mcp add`, Desktop `claude_desktop_config.json`, Cursor `.cursor/mcp.json`). Tools: status/models/install(confirm-gated)/start/stop/logs/benchmark/connect_info.
- **PORT (hard):** default 8080 is FORBIDDEN per `operations/WEBAPP_PORTS.md`. Claim a fresh 10700-15000 port via `fleet-gate/claim_ports.py` BEFORE install (`--port N`), register in WEBAPP_PORTS.md.

## 5. Versions

- **qwen** (all 4 sizes, +vision, +experimental speed projection). Default.
- **coder** (`--family coder`, IQ1_M): half experts kept on code+agentic+image data. Fastest prefill (2180 tok/s ref). General-use fallback: Q2_0/IQ2_XS whenever RAM allows.
- **swift** (Swift 1.5 fine-tune, Q2_0/IQ2_XS/IQ3_XXS): shorter chain-of-thought, sooner first token, ~same quality. Interesting for agent loops where latency dominates.
- **unsloth** (UD-IQ4_XS 94GB / UD-Q4_K_XL 111GB experimental, NVIDIA+NVMe only, no images on XL): needs ~80GB+ RAM to avoid SSD-read decode penalty (7-8.5 tok/s on 64GB for XL). Skip unless RAM grows.
- **OrcaRouter Uncensored IQ3_XXS:** manual packing conversion only, not in installer menu. Note + skip (fleet promotion/guardrail posture per `standards/FLEET_PROMOTION.md`).

## 6. What We Did NOT Verify

1. No Goliath run: `--check`, install, `/health`, `/v1/chat/completions`, `strata_benchmark`, `--calibrate` all pending.
2. Paper (`docs/paper/Strata-Paper.pdf`), DETAILS.md speed tables per card, COMMUNITY_BENCHMARKS.md, AMD_HIP.md, BATCHING.md, TROUBLESHOOTING beyond the common table — referenced, not fetched.
3. License split: Strata MIT verified; per-model licenses (Qwen, Swift, Unsloth) apply — read before any redistribution/packaging.
4. Security: share-via-`--host 0.0.0.0` ONLY with `--api-key`; never tunnel/keyless. MCP server itself is local-only by design (refuses `--host 0.0.0.0`).

## 7. The HN Lesson (Intel-Stack Gap) — CORRECTED 2026-10-05 12:30

Strata arrived via HN front page, and the first audit (s7 as written 12:00) wrongly claimed "no HN source wired". Correction: HN keyword search via hnrss.org IS wired — `operations/bundles.json` ide-host-signal carries five hnrss keyword feeds, and aiwatcher DB defaults carry `HN / AI/ML` (`q=AI+machine+learning&points=50`). Strata still missed, and the miss is now proven structurally:

- Smoking gun, fetched live 2026-10-05 12:30 from `https://hnrss.org/frontpage`: `Run Qwen 3.8 Flash Next (125B) on consumer hardware (RTX 4090) at 100T/s` → github.com/Niko1221/Strata, item 49953495, **781 points / 350 comments**, posted 2026-10-04 12:51 UTC by snehesht. Still on the front page a day later.
- Title autopsy: contains "Qwen", "125B", "consumer hardware", "RTX 4090". Contains NONE of the watched keywords ("AI", "machine learning", "cursor", "MCP", "IDE", "zed", "windsurf"). Every existing keyword feed whiffed by design, not by outage.
- Fix applied this session (zero code): `HN Frontpage (no keyword filter)` added to ide-host-signal sources in `bundles.json`, so rss-mcp bundle import and aiwatcher polling both see the unfiltered front page. Verified the endpoint live before adding.
- Remaining delta (still open, `sandraschi/aiwatcher-mcp#11` updated 12:30): front-page RSS carries points only inside description HTML, not as machine fields — no velocity scoring, no GH star enrichment. The Algolia front-page + star-velocity poller in #11 is the scored complement, not a duplicate.
- **Superseded first-audit bullets (kept for honesty, struck 12:30):** the 12:00 audit claimed no HN source wired and proposed HN-from-scratch. Both wrong per the correction above — keyword HN existed, frontpage is now wired via bundles.json, and only the scored/velocity layer remains open (#11).
## 8. Next Steps

1. `START-HERE.bat --check` on Goliath (GPU/driver/RAM/disk report), claim `--port`, confirm 80GB data dir.
2. `--yes --family qwen --model IQ2_XS --no-start` install in background (resumable), then detached start, poll `/health`, `curl /v1/models` + chat smoke, `strata_benchmark`.
3. `--calibrate` 5-10min, record tok/s + prefill at 4k/32k/128k context; bake-off vs vLLM recipe endpoint.
4. On success: update `llms/LOCAL_VLLM_CODING_AGENT_RECIPE.md` (Strata lane), log decision in `standards/LOCAL_LLM_FIRST_DOCTRINE.md` scope, add session-log entry. On failure: `strata_logs source=setup/engine` + TROUBLESHOOTING.md table.
5. File HN-source issue (aiwatcher-mcp or rss-mcp, TBD by maintainer): Algolia front-page poll + star/download velocity thresholds. Do not build before maintainer picks home.

## 9. Goliath Verification Pass 2026-10-05 ~23:30 Europe/Vienna (infra, no local tok/s yet)

**Telemetry block resolved:** no `bench_*.txt` exists locally because no Goliath benchmark has run yet. `search_files bench_.*\.txt` over `_upstream/Strata` = 0 hits; `aiwatcher-mcp/logs` holds only `service-stdout/stderr.log` (~122MB). `bench/results/` holds 18 *vendor* result dirs, not local runs. Closest 24GB-VRAM proxy is `bench/results/2026-09-29-rtx3090-epyc-milan` (1x/2x RTX 3090 24GB, EPYC 7453, 165GiB RAM, engine v0.1.26):

- IQ3_XXS 1x3090: decode median 79-93 tok/s (1K 93.0 / 4K 89.2 / 32K 90.6 / 128K 79.3 / 262K 67.3), prefill 869-2173 tok/s, TTFT 1.33s@1K / 14.83s@32K / 60.53s@128K, draft accept ~0.70-0.76, needles 3/3 @8K/16K/28K.
- Coder IQ1_M 1x3090 32K: decode 66.8 median; 2x3090 auto K=19: 98.6 median. K-sweep best K=22 at 103.3 median (unpaired prompts, indicative only).
- Our config is IQ2_XS (lighter than IQ3_XXS), so >=90 tok/s decode on 4090 24GB is plausible but UNVERIFIED. Do NOT quote as measured.

**Install state (verified on disk):**

- `Strata-data/` = 71.2GB / 53 files (matches ~70GB IQ2_XS expectation).
- `engine/strata.exe` present (112MB) + `strata-vision.exe`; `engine/BUILD.json` = v0.1.39, CUDA 13.0, archs 75/86/89/120, ptx true (ready-made engine, no compile).
- `strata-iq2_xs.json` generated: 2-shard IQ2_XS (`...-00001-of-00002.gguf` + `...-00002-of-00002.gguf`), `--max-context 131072`, `--kv int8`, `--kv-resident 32768`, `--spec 4`, `--mtp .../mtp/rt`, port 11235 (FORBIDDEN-8080 avoided, matches claim).
- `run-iq2_xs.bat` wraps `serve/server.py --engine strata --config strata-iq2_xs.json --port 11235`.
- `strata-iq2_xs.log` NOT present = server has not started since config generation. `GET 127.0.0.1:11235/health` = transport error (down). `GET 127.0.0.1:11236/health` = transport error (Newsroom down too).
- No `*.log` at Strata top level (recursive `*.log` listing hits only venv noise).

**Host (verified):**

- D: free 323.8GB / 2000GB (83.8% used) — weights fit with headroom. C: 74GB free (96.3% used, tight). N: 569GB free (recipe precedent `N:\AI\hf` viable if D: pressure grows).
- RAM 68.6GB total, 28.9GB avail / 39.7GB used (57.9%), swap 1.9% used. CPU 40.8%. Boot 2026-10-03. `strata` process query timed out (host loaded) — treat as unknown, not as running.
- Gate holds: **no `--calibrate` until peak VRAM <24GB is confirmed stable on Goliath.** Next gated sequence: detached start (`run-iq2_xs.bat` or `START-HERE.bat --check` first), poll `/health`, `curl /v1/models` + chat smoke, `tools/calibrate.py` + needle bench at 4K/32K/128K, record tok/s + prefill + VRAM.

## 10. Goliath Live Run 2026-10-13 (Sandra session — s6 TODO-1 closed)

**Date:** 2026-10-13 (Europe/Vienna) | **Operator:** Sandra + Cowork agent

- Fresh `git clone https://github.com/Niko1221/Strata.git` → `D:\Dev\Strata` (main). Model data MOVED, not copied: `D:\Dev\repos\_upstream\Strata-data` → `D:\Dev\Strata-data` (71.2GB / 53 files, IQ2_XS complete). `_upstream` left clean (frozen-third-party rule).
- Setup gotcha: first `START-HERE.bat --yes --family qwen --model IQ2_XS --no-start` WITHOUT `--data-dir` recreated the OLD data path and re-downloaded ~26GB there before timeout-kill (partial deleted after). Reran WITH `--data-dir D:\Dev\Strata-data` → both ggufs verified present, prepare OK, `run-iq2_xs.bat` written. Lesson: always pass `--data-dir` explicitly when data was moved; setup does not auto-discover it (why it preferred the old path is unverified).
- Install result: engine 0.1.43.1 (CUDA 13.0, ready-made, no compile), context 131072, KV int8, kv-resident 32768, spec 4, MTP draft, images OFF. Server in own window via `run-iq2_xs.bat`.
- PORT DEVIATION: running on upstream default **8080**, NOT the 11235 from the Oct-05 pass (s4/s9). 8080 is fleet-forbidden for webapps per `operations/WEBAPP_PORTS.md`; kept for now because everything (opencode provider, MCP server, docs) agrees on it and it is localhost-only. Migration to a claimed 10700-15000 port remains open.
- First load stalled exactly as feared: 33GB arena vs ~13GB free (48GB already resident) — engine log froze at `expert cache` line, box swapped. Freed RAM (Ollama down helped; Podman stack killed later — see `sandraschi/podman-mcp#1`) and it completed. First-start 1-3min freeze is real on a loaded 64GB box.
- MEASURED Goliath (4090 24GB, IQ2_XS): **129 tok/s generation, 409 tok/s prompt** (383-prompt / 310-gen sample from `/health last_request`). s3 projection (100-140 tok/s) CONFIRMED within range. Browser chat works, t/s described as "quite high" by operator.
- opencode wired: provider `strata` → `http://127.0.0.1:8080/v1`, model `strata/strata-iq2_xs` (131k ctx / 16k out, tools+attachment flags); MCP server `tools/strata_mcp.py` added as `mcp.strata` (venv Python 3.13, 180s timeout). Verified: `opencode mcp list` = `strata ✓ connected` (28 servers); stdio initialize + `tools/call strata_status` returns live data (idle, uptime, VRAM 21.0/24GB, RAM 60.2/63.9, engine 0.1.43.1).
- DRAM lesson: IQ2_XS permanently owns ~half the box (26GB DRAM + 21GB VRAM observed). Podman kill freed only ~1GB (VM was 767MB) — small fish. Real levers: `wsl --shutdown`, one browser, idle Electron apps (Cursor/Claude/Discord/OpenCode all open at once). Structural fallback: Coder variant (23GB arena, ~10GB saved, weaker off-code/CJK).
- Still open: `--calibrate` + needle bench 4K/32K/128K, vLLM-recipe bake-off, `llms/LOCAL_VLLM_CODING_AGENT_RECIPE.md` Strata lane, `LOCAL_LLM_FIRST_DOCTRINE.md` scope note, port 8080→claimed migration decision.
