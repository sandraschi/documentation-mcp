# Diffusion Language Models — Field Research

## Nomenclature: dLLM (acronym du jour, June 2026)

After **LWM** (large world models) and **VLA** (vision-language-action), **dLLM** — diffusion large language model — has the buzzword slot. vLLM's first-class dLLM support and DiffusionGemma's Apache 2.0 release canonized the term. Expect papers, product pages, and PRC fine-tunes to adopt it within the quarter.

---

```
2021  D3PM (Austin et al.) — discrete diffusion on text
2023  MDLM / masked diffusion revival (Lou, Sahoo, Ou)
2024  MDLM NeurIPS — SUBS parameterization, SAR samplers
2025  LLaDA 8B — first credible AR-competitive diffusion LM at scale
2025  Dream 7B, MMaDA, Mercury Coder — parallel ecosystem growth
2025  Gemini Diffusion (closed) — Google internal validation
2026  DiffusionGemma — first open-weights dLLM with native vLLM support
```

---

## Primary References

### Google / DeepMind (DiffusionGemma)

| Resource | URL | Notes |
|----------|-----|-------|
| DeepMind product page | https://deepmind.google/models/gemma/diffusiongemma/ | Positioning, 4× speed claim |
| Model card | https://ai.google.dev/gemma/docs/diffusiongemma/model_card | Params, architecture, limitations |
| Diffusion explained | https://ai.google.dev/gemma/docs/diffusiongemma/explained | Uniform state diffusion, dual-mode backbone |
| Model overview | https://ai.google.dev/gemma/docs/diffusiongemma | Deployment guidance |
| HuggingFace weights | https://huggingface.co/google/diffusiongemma-26B-A4B-it | Apache 2.0 |
| vLLM integration | https://blog.vllm.ai/ (search "DiffusionGemma") | ModelState abstraction for dLLMs |

**Key technical contributions from Google:**
- **Uniform State Diffusion** — random vocabulary noise instead of `[MASK]`; tokens can be re-noised if confidence drops.
- **Block-autoregressive diffusion** — 256-token canvases chained via KV cache commits.
- **Dual-mode single backbone** — causal encoder + bidirectional decoder sharing weights.
- **Entropy-Bounded sampler** — adaptive stopping, temperature decay 0.8→0.4.

**Predecessor (closed):** Gemini Diffusion — internal proof that the paradigm works at Google production scale before open-weights release.

---

## Foundational Papers (arXiv)

### Discrete diffusion origins

| Paper | arXiv | Authors / Year | Contribution |
|-------|-------|----------------|--------------|
| Structured Denoising Diffusion Models in Discrete State-Spaces | [2107.03006](https://arxiv.org/abs/2107.03006) | Austin et al., 2021 | D3PM — discrete diffusion framework for text |
| Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution | [2303.00848](https://arxiv.org/abs/2303.00848) | Lou et al., 2023 | Score-based discrete diffusion |

### Masked diffusion (the dominant 2024–2025 thread)

| Paper | arXiv | Authors / Year | Contribution |
|-------|-------|----------------|--------------|
| Simple and Effective Masked Diffusion Language Models (MDLM) | [2406.07524](https://arxiv.org/abs/2406.07524) | Sahoo et al., NeurIPS 2024 | SUBS parameterization; MLM-equivalent objective; SAR samplers |
| Large Language Diffusion Models (LLaDA) | [2502.09992](https://arxiv.org/abs/2502.09992) | Nie et al. (GSAI-ML), 2025 | 8B MDM from scratch; rivals LLaMA3-8B |
| LLaDA 1.5: VRPO | [2505.19223](https://arxiv.org/abs/2505.19223) | GSAI-ML, 2025 | Preference optimization for MDMs |
| Dream 7B: Diffusion Large Language Models | [2508.15487](https://arxiv.org/abs/2508.15487) | 2025 | 7B-scale; AR weight init + context-adaptive noise |
| MMaDA: Multimodal Large Diffusion Language Models | [2505.15809](https://arxiv.org/abs/2505.15809) | Gen-Verse, 2025 | Multimodal diffusion LM — text + image unified |

### Related theoretical work

| Paper | arXiv | Notes |
|-------|-------|-------|
| RADD | [2406.03736](https://arxiv.org/abs/2406.03736) | LLaDA theoretical foundation — ELBO bound |
| SMDM | [2410.18514](https://arxiv.org/abs/2410.18514) | Scalable MDM training |
| MD4 | [2406.04329](https://arxiv.org/abs/2406.04329) | Theoretical MDM connections |

---

## Model Family Comparison

| Model | Params | Paradigm | Open weights | Production tooling | Quality vs AR peer |
|-------|--------|----------|--------------|-------------------|-------------------|
| MDLM | ~1B scale | Masked diffusion | ✓ (code) | Research | Approaches AR perplexity at small scale |
| LLaDA 8B | 8B dense | Masked diffusion | ✓ | HF, demos | ≈ LLaMA3-8B |
| LLaDA 2.0 | 100B (announced) | AR→diffusion conversion | In progress | — | Scaling law tests |
| Dream 7B | 7B | Masked diffusion | ✓ | HF | Competitive with AR 7B |
| MMaDA | Multi-modal | Masked diffusion | ✓ | HF demo | Multimodal unified |
| Mercury Coder | Commercial | Diffusion | Closed API | Production | Code gen efficiency |
| **DiffusionGemma** | **26B/3.8B MoE** | **Uniform state + block** | **✓ Apache 2.0** | **vLLM, HF, llama.cpp PR** | **Below Gemma 4 AR on most benches; HLE no-tools 11.0% > 8.7%** |

---

## Why DiffusionGemma Matters vs Prior dLLMs

Earlier diffusion LMs (LLaDA, Dream, MDLM) were **research artifacts with demos**. DiffusionGemma is the first to ship with:

1. **Native vLLM support** — new `ModelState` abstraction built for diffusion inference.
2. **Apache 2.0 at 26B MoE scale** — not a 7–8B demo model.
3. **Multimodal inputs** — text, image, video → text.
4. **Consumer GPU path** — quantized to 16–18 GB.
5. **Ecosystem partners day one** — Unsloth, MLX, HuggingFace Transformers.

LLaDA proved the science. DiffusionGemma proves the **infrastructure intent**.

---

## Open Questions in the Field

| Question | Status |
|----------|--------|
| Can dLLMs match AR quality at 26B+ scale? | Not on saturated benchmarks (MMLU etc.) — but DiffusionGemma beats Gemma 4 AR on HLE no-tools (11.0% vs 8.7%). HLE (CAIS/Scale) is an anti-saturation frontier eval, same design intent as ARC-AGI: built to stump models, not measure incremental knowledge retrieval |
| Does preference optimization (VRPO-style) close the gap? | LLaDA 1.5 says yes at 8B; untested at 26B MoE |
| Is block size (256) optimal? | Unknown — trade-off between parallelism and boundary artifacts |
| Can streaming be faked (block → pseudo-stream)? | UX hack possible; true token streaming incompatible with bidirectional denoise |
| Will AR models adopt hybrid decode (speculative + diffusion blocks)? | Plausible convergence path |

---

## Suggested Reading Order

1. [Google — Diffusion explained](https://ai.google.dev/gemma/docs/diffusiongemma/explained) — best single explainer
2. [LLaDA paper](https://arxiv.org/abs/2502.09992) — scientific foundation
3. [MDLM paper](https://arxiv.org/abs/2406.07524) — masked diffusion engineering
4. [DiffusionGemma model card](https://ai.google.dev/gemma/docs/diffusiongemma/model_card) — deployment specs
5. [MMaDA](https://arxiv.org/abs/2505.15809) — if multimodal diffusion path interests the fleet

---

*See [PROGNOSIS.md](./PROGNOSIS.md) for competitive dynamics and [ASSESSMENT.md](./ASSESSMENT.md) for the early-SD analogy.*
