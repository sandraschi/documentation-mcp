# CLM Evaluation: Contrastive Language Models as Fast Verifier / Router

**Date:** 2026-09-26
**Status:** Evaluated - pilot recommended, do not adopt blindly
**Sources:**
- Repo: https://github.com/Contrastive-LM/CLM
- Models and data: https://huggingface.co/Contrastive-LM
- Blog: https://contrastive-lm.notion.site
- Discord: https://discord.gg/5dAQEDJBs
- Release under test: `CLM-v0.1-8B` (release_date 2026-09-19), Apache 2.0 code + weights

---

## 1. What CLM is

CLM is a **System-One scorer**, not a generator. It does one thing: `score(state, candidate)` via contrastive alignment, then softmax over a closed candidate set.

| | CLM-8B reference |
|---|---|
| **Category** | Contrastive verifier / ranker / typed decision head |
| **Backbone** | Frozen Qwen3-8B embeddings (last-token pooling), served via vLLM `--runner pooling` on :8090 |
| **Trainable part** | 20M projection head (`state_head` + `action_head` + `logit_scale`), 75 MB `CLM_v0.1-8B.pt`, served by `clm-serve` (FastAPI) on :8700 |
| **API** | `POST /v1/systemone` (typed `Noul` / `Choice` / `Score`, TypeSafe-compatible), `POST /v1/rank` (free-form candidates), `GET /v1/models`, `GET /health`, playground at `GET /` |
| **Training** | Pre 60M Nemotron DQA Q&A pairs, mid 30M synthetic hard negatives (Gemini 2.5 Flash-Lite), post 1M agentic trajectories (ADP + Endless-Terminals + LiteCoder-Terminal-SFT), 40% DQA replay during post |
| **Loss** | Bidirectional InfoNCE, extended with hard negatives for mid-training; reported power-law scaling in C/D/N/N_enc, optimum ~310 tokens per head parameter |
| **Cache** | Reserved vector arena (`--action-cache 0.02` default), LRU, shared across heads, hot-reload safe; hits skip encoder + head forward pass |
| **License** | Apache 2.0 (code + weights) |
| **Backing** | Kwok, Kang, Suresh, Saad-Falcon, Pavone, Re, Mirhoseini; research repo split from inference branch |
| **Deploy** | `pip install contrastive-lm`, `vllm serve Qwen/Qwen3-8B --runner pooling --port 8090` + `clm-serve`; `clm-serve --no-ui --port 8700`, `CLM_API_KEY`, `CLM_DEVICE`, `CLM_EMB_URL` envs |

Typed example (from README):

```python
from clm import CLMClient, Choice, Noul, Score
client = CLMClient()  # CLM_BASE_URL default http://127.0.0.1:8700
r = client.system_one(
    state="Customer: my invoice was charged twice!",
    questions={
        "urgency": Noul(instructions="Is this urgent?"),
        "department": Choice(instructions="Which team?",
                             criteria={"billing": "Charges, invoices, refunds",
                                       "technical": "Bugs and outages"}),
        "frustration": Score(instructions="How frustrated?",
                             criteria=["Calm", "Frustrated", "Very angry"]),
    },
)
```

---

## 2. Claimed results (unreproduced - treat as vendor numbers)

### Zero-shot: CLM-8B vs Jev baseline

Across computer-use, gaming, tool-calling (T-Rex runner ships in `examples/t_rex`, plus BFCL v4, WikiRacing, Super Mario): par with Jev at **up to 9x lower latency**. Largest wins when candidate count is large (WikiRacing) or actions repeat across states (T-Rex).

### Agentic verifier: best-of-N selection

Per task sample N candidates (**Opus 5** for DeepSWE, **Fable 5** for Terminal-Bench 2.1), CLM or Jev picks best. Heldout: 38 DeepSWE tasks, 30 Terminal-Bench 2.1 tasks, latency on H100.

| | DeepSWE | Terminal-Bench 2.1 | Verifier latency vs Jev |
|---|---|---|---|
| CLM fine-tuned | **81.6% (31/38)** | **87.6%** | **4.1-5.7x faster** |
| Jev | below pass@1 (fails as verifier on long horizon) | below pass@1 | baseline |

Repro commands from README:

```bash
hf download Contrastive-LM/deepswe-clm-heads-8k --local-dir heads/deepswe
python evaluation/bon_eval.py --hf-dataset Contrastive-LM/deepswe-clm-embeddings-8k \
  --checkpoint heads/deepswe/best_head.pt \
  --tasks-file heads/deepswe/heldout_tasks.json --n 4 --window 12
python train/finetune.py --task clm --init-ckpt "$(clm-download)" --out-dir runs/deepswe \
  --holdout-tasks heads/deepswe/heldout_tasks.json --batch 512
```

### What makes it interesting for the fleet

- **Cheap-first-verify pattern with a real learned verifier.** Maestro promised this but shipped mock-only verify. CLM ships a trained head + fine-tune script (`train/finetune.py`, adapters for agentic traces + typed decisions).
- **Fits Goliath.** Reference numbers captured on single RTX 4090. Qwen3-8B pooling + 20M head is servable alongside existing vLLM/Ollama load.
- **Cacheable by design.** States/actions disaggregated, embeddings reused independently. Reported server-side p50 on 4090 with fixed action set: new state every call ~28 ms, revisited states ~0.6-0.7 ms (about 2.8x faster on loops). `usage.input_tokens` counts cache misses only.
- **TypeSafe-compatible typed decisions.** `Noul/Choice/Score` maps directly to voice intent, tool routing, triage rubrics without per-task prompt engineering.
- **Apache 2.0 + fine-tunable.** Any head in same checkpoint format (`state_head` / `action_head` / `logit_scale` / `cfg`) served via `--ckpt`, `--ckpt-dir`, `--model NAME=PATH`.

### Concerns

- **v0.1, 7 days old at eval time.** No paper, only Notion blog + README charts. Scaling-law figures live in research-branch, not the inference branch we install.
- **2048 token default truncation.** Long agent traces need `--max-tokens 8192` + matching 8k head + more VRAM. Long-horizon is exactly where verifier value is highest.
- **Generator still required.** CLM ranks candidates, it does not write them. Budget remains Opus/Fable/local-generator + encoder GPU.
- **Baseline naming is thin.** README says "Jev" throughout with no version/pin. Assume frontier LLM judge, but cannot compare cost/quality until we pin our own baseline (Claude/GPT/local).
- **Hard-negative recipe matters.** Their own ablation: pre-only 52.1% top-1 on hard-negative set, pre+mid 69.2%, hard-negatives-from-start peaks 62.4% then overfits. Fine-tuning our own head without replay drops Nemotron hard-negative top-1 69% to 56.2%. We must keep replay if we fine-tune.
- **Another GPU service to run.** vLLM pooling encoder :8090 + `clm-serve` :8700, port claims + NSSM/start-script wiring required.

---

## 3. Comparison matrix

### 3a. Head-to-head

| Dimension | CLM-8B (reference head) | Frontier LLM-as-judge (Opus 5 / Fable 5 / Jev-class) | Raw cosine (`clm-raw` / Qwen3-8B pooling, no head) | Heuristic router (Maestro-style regex) | Per-task reward model / fine-tuned verifier head |
|---|---|---|---|---|---|
| **Role** | Learned state-action scorer, zero-shot + fine-tunable | General reasoner prompted as judge | Ablation baseline, no training | Zero-cost keyword rules | Same CLM stack, head fine-tuned on fleet traces (e.g. DeepSWE-8k head) |
| **Latency** | ~28 ms new state, ~0.6 ms cache hit (4090 p50, vendor); 4-9x faster than Jev per README | 1-10+ s per judgment, dominates loop | Same encoder cost as CLM, minus head forward (negligible diff) | Microseconds | Same as CLM-8B serving cost |
| **Cost** | 1x GPU (Qwen3-8B pooling) + CPU head; no per-token API fee; cache cuts encoder tokens | Per-token API fee, highest at scale | Same GPU as CLM, no head download | Free | + one-time fine-tune (their recipe: batch 512, replay mix) |
| **Quality signal** | Vendor: par with Jev zero-shot, SOTA fine-tuned on 2 agentic coding benches; independent repro pending | Strongest zero-setup reasoning, but vendor shows below pass@1 as long-horizon verifier | Weak - README ships it as ablation only | Capped, brittle outside known patterns | Vendor: 81.6% / 87.6% on heldouts; risk of overfit to head's task window |
| **Token / state limit** | 2048 default, 8k with head+VRAM bump | 100k+ context | Same as CLM encoder setting | Unlimited (string ops) | Tied to head training window (e.g. 8k head + `--window 12`) |
| **Cacheability** | First-class (state/action vectors, LRU arena, hit-rate on `/health`) | Response cache only (exact prompt match) | Same as CLM | N/A | Same as CLM |
| **Fine-tune cost** | `train/finetune.py --task clm|choice`, adapters included, replay required | Prompt-only, no weights | N/A | Edit regex | Same script, needs fleet trace adapter |
| **Maturity / license** | v0.1, Apache 2.0, single-org, Discord + HF active | Production APIs, commercial terms | Same repo, trivially available | Maestro v0.1, 27 stars, mock verifier | Same repo, example-only datasets |
| **Fleet integration** | New service (`clm-serve`), Python client `CLMClient`/`Engine`, playground for labeling | Already integrated (API calls) | Zero extra work beyond encoder | Already evaluated, skipped | Same as CLM + dataset pipeline (`preprocessing/hf_embeddings.py`, `evaluation/bon_eval.py`) |

### 3b. Fleet fit

| Need | CLM solves it? | Notes |
|---|---|---|
| Best-of-N verifier for coding agents (assfix, fleet-reviewer) | Yes, if repro holds | Start with DeepSWE head repro, then fleet-trace head |
| Fast tool routing / intent classification (voice bus, MCP gateway) | Yes | `Choice` over tool descriptions; embeddings cached; replaces LLM judge call |
| Inbox / digest / Discord triage (`Noul` urgency, `Score` severity) | Yes | Typed rubrics without per-task prompts; playground speeds rubric design |
| Computer-use / robot next-action scoring | Partial | Zero-shot T-Rex/WikiRacing promising; vision/multimodal on roadmap, not shipped |
| Replace generator LLM | No | Still need proposer; CLM is scorer only |
| Drop-in cost saver with zero ops | No | Requires vLLM encoder + `clm-serve` + port + health wiring |

---

## 4. Honest assessment

The question CLM answers:

> "I sample N cheap/mid candidates and need a fast learned scorer that picks the best without paying frontier-judge latency on every step, and I can fine-tune it on my own traces."

We have this problem in three places: coding-agent best-of-N, tool/intent routing, triage scoring. Our current options are frontier-judge (slow/pricey), regex (brittle), or raw cosine (weak). CLM sits in the gap Maestro identified but did not fill.

Reasons to pilot, not adopt:

- Numbers are vendor-heldout, small-n (38 + 30 tasks), single baseline ("Jev"), no independent repro yet.
- Serving cost is real but bounded and fits hardware we already own.
- Failure mode is silent misranking, same as any verifier. Needs `bon_eval.py`-style harness on fleet tasks before it gates anything.

---

## 5. Conclusion

| Option | Verdict | Rationale |
|---|---|---|
| **CLM-8B reference head** | **Pilot** | Only learned verifier in this weight class with Apache 2.0, 4090-servable stack, TypeSafe-compatible API. Repro T-Rex + tool-routing bench first. |
| **Fine-tuned fleet head** | **Pilot phase 2, if phase 1 holds** | Follow their replay recipe (40% DQA replay), hold out fleet tasks task-disjoint, report pass@1 + latency vs frontier judge. |
| **Frontier LLM-as-judge** | **Keep as baseline/oracle** | Still needed as proposer and as oracle for head training/eval. Do not rip out. |
| **Raw cosine / heuristic** | **Keep as floor baselines** | `clm-raw` + regex in every bench so we know the head earns its GPU. |
| **Blind rollout** | **Skip** | No gating of assfix/reviewer merges on CLM scores until repro + fleet-heldout numbers exist. |

### Revisit / kill triggers

- Kill/park if: T-Rex repro or fleet tool-routing bench shows no win over `clm-raw` + frontier-judge sample, or 8k-context serving breaks Goliath VRAM budget.
- Expand if: fleet-heldout best-of-N win with 3-5x latency cut, or fine-tuned head beats frontier judge on our traces.
- Re-evaluate on: larger backbone release, vision/multimodal support (robotics/computer-use), paper with pinned baselines.

### Next steps (proposed)

1. `serve_qwen3_8b.sh` + `clm-serve` on Goliath (claim ports,atorias: encoder :8090 already? check `operations/WEBAPP_PORTS.md` + `fleet-start.config.ps1` before binding; do not hardcode).
2. Repro `examples/t_rex --model clm|jev` + `Engine.rank` microbench on fleet tool list; log latency + hit-rate from `/health`.
3. Bench `system_one Choice` for voice-intent + MCP tool routing vs frontier judge; keep `clm-raw` floor.
4. If steps 2-3 hold, fine-tune `runs/fleet` head on fleet traces with replay; eval task-disjoint via `evaluation/bon_eval.py`.
5. Write bench log to `reports/` and link here; update Status line above.

### Links

- Inference package: `src/clm/` (`client.py`, `engine.py`, `heads.py`, `embedder.py`, `cache.py`, `server.py`, `static/` playground, `tools/playground_mock.py` for no-GPU UI check)
- Training: `train/finetune.py`, `train/adapters.py`, `train/embed_utils.py`, `docs/FINETUNING.md`
- Eval: `evaluation/bon_eval.py`, `preprocessing/hf_embeddings.py`, HF datasets `deepswe-clm-embeddings-8k`, heads `deepswe-clm-heads-8k`
