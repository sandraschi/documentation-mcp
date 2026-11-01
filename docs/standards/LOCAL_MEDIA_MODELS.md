---
title: "LOCAL_MEDIA_MODELS.md - local audio and image generation for the fleet"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-10-21
---

# Local media models (audio, image)

Scope: models we run **ourselves** to produce fleet assets - demo-video music and
effects, posters, README art, placeholder imagery. This is not a licence to bolt
generative features into wrappers of apps that do not have them (PhotoCraft wraps a
photo editor; the wrappee-first rule still applies).

All numbers below were measured on Goliath (2026-10-21) or quoted from the vendor's own
model card, and each row says which.

## What to use for what

| Need | Use | Why |
|---|---|---|
| Background bed for a demo video | Stable Audio 3 `sm-music` (local) | 19.3 s for 60 s, 2.0 GB, no key, no network |
| One-shot sound effects | FreeSound if it must sound real, Stable Audio `sm-sfx` otherwise | Real recordings beat synthetic clicks; FreeSound needs a key and has commercial terms |
| Repository poster / README hero | FLUX 3 Image Klein via BFL API | $0.009 per 1K image; local is 26 GB FP8 at 1MP |
| Image editing by instruction | FLUX 3 Klein (API or INT8 ComfyUI) | 10 reference images, pixel-preserving edits |
| Audio for a product feature | stop and re-read the wrappee rule | do not add generative features a wrappee lacks |

## Stable Audio 3 (local, CPU)

Route: `optimized/tflite` (LiteRT + XNNPACK, no PyTorch). Windows x64 supported.

| Model | Params | Max length | Measured |
|---|---|---|---|
| `sm-music` | 433M | 120 s | 60 s bed in **19.3 s** wall (0.32x realtime), 2.0 GB peak working set |
| `sm-sfx` | 433M | 120 s | 1-3 s effects in **5.2-5.9 s** wall each |
| `medium` | 1.4B | 380 s | not used: needs Flash-Attention 2, TensorRT route is Linux-only |

Findings that change integration:

- **Per-call model load dominates short clips.** 4-5 s of every effect request is reloading
  the DiT; only the TFLite CLI exists, and everything lives inside `main()`. A warm service
  needs an upstream refactor, or the cache described below.
- **Short effects come out quiet.** A 1 s UI click measured peak -13.5 dB against -0.2 dB for
  a boom. Normalise to about -3 dB peak before mixing or they vanish under narration.
- **`--decoder` is mandatory non-interactively** (`--decoder same-s`); without it the CLI
  opens an arrow picker and dies with `EOFError` in a script.
- Windows needs Python 3.10-3.13 for `ai_edge_litert`; `python` on PATH is not guaranteed.

Spike repo: `D:\Dev\repos\stable-audio-spike` (measured results in `docs/DECISION.md`).
Weights are vendored at `D:\Dev\models\stable-audio-3` (2.65 GB) with upstream pinned at
`77e0398c26f7d22d801ec1bb036307e8b231f741`, so the model survives Hugging Face or the
company disappearing. Never commit weights.

The spike also runs a local service (`service/app.py`, port 11250) that is drop-in for
`demo-vid-mcp`: an MCP `sfx_search` tool mirroring `sfx-mcp`, and a songgeneration-compatible
`POST /api/generate`. Verified through demo-vid's own modules: 8.5 s per effect uncached,
0.4-1.2 s cached; 14.6 s for a 30 s bed uncached. It is **not warm** - the upstream CLI loads
the model per call - so the cache is the only reason a rebuild is fast.

`sm-music` caps at 120 s per call. The service builds longer beds from 110 s windows joined
with a 3 s crossfade and trimmed to the requested length (each window gets a distinct seed,
otherwise the cache returns the same audio three times - a real bug caught on the first
attempt). Measured: a 283 s bed took 107-114 s uncached, then the full demo re-record used it
as one continuous track. For 200+ s beds budget ~2 s of wall time per second of audio on this
CPU, and expect the three windows to differ in character - it is a continuous bed, not one
musical arc.

Licence: Stability AI Community License. Free for research and for commercial use by
individuals or organisations under **US$1M** annual revenue; above that an Enterprise
licence is required. Revocable for violation of terms, not at will. As between you and
Stability you own the outputs.

## FLUX 3 Image Klein (open weights, 5.6B)

Released 2026-10-15. Text-to-image, instruction editing and multi-reference generation
(up to 10 images) in one model, Qwen3-VL-4B text encoder, native 4K, bounding boxes on a
0-1000 grid for placing text and elements.

Licence: **FLUX Kommunity License v1.0** - non-commercial, plus commercial *output*
generation for Qualifying Users under **US$5M** gross annual revenue including affiliates.
Not blanket permission for commercial fine-tuning or redistribution. Use restrictions
apply (surveillance, biometrics, military, improving a competing model).

Hardware, and the two sources disagree:

| Source | Claim |
|---|---|
| BFL blog | INT8 on 8 GB VRAM via ComfyUI; 1MP in ~4 s on a 5090 |
| HF model card | reference code peaks at **26 GB FP8** (31 GB BF16) at 1024x1024 |
| HF model card | prompt upsampler is a separate 9B model, 18.8 GB download, ~28 GB resident |

On a 24 GB card the reference code does not fit as shipped, and the upsampler cannot sit
beside it. Local use means INT8/ComfyUI with offload, and replacing their upsampler with
our own LLM using `system_prompts.json`. Prompts must be expanded: short prompts give
generic output.

Cheapest correct path for fleet assets: the BFL API at **$0.009 per 1K image**. A poster
for 200 repos costs under $2 and needs no GPU work.

## FreeSound (sfx-mcp)

- Key: log in at <https://freesound.org>, then <https://freesound.org/apiv2/apply/>.
  One key per application. Put it in `sfx-mcp/.env` as `FREESOUND_API_KEY` (gitignored).
- Terms: free for non-commercial use; commercial use is negotiated case by case with UPF.
  Per-sound licences still apply (CC0 needs nothing, CC-BY needs attribution). No bulk
  database copying; delete intermediate copies.
- Service: dual stdio + HTTP. Endpoint accepts `/mcp` and `/mcp/`; see BUG-083 for why that
  was broken and what the fix looks like.

## Integration rules

1. **Claim the port.** `fleet-gate/claim_ports.py --repo <name> --apply`. Never hand-pick.
2. **Normalise audio** to a target peak before mixing; never trust generated levels.
3. **Cache by (model, prompt, seconds, seed)** and say in the response whether it was a hit.
   Cold generation is minutes of CPU; a warm cache is free.
4. **Stamp the engine version in every artifact** (see `democraft-mcp` run manifests), so a
   regenerated asset says which build produced it.
5. **Keep a fallback.** Network engines stay configured; the local engine is an option, not
   a hard dependency, until it has passed an A/B on real output.
6. **Licence check before publishing**, not after: $1M (Stability) and $5M (BFL) thresholds,
   FreeSound commercial terms, and per-sound CC licences for effects.

## Related pitfalls

- BUG-083: mounting a FastMCP app on FastAPI without its lifespan, and the `/mcp` 405.
- BUG-084: audio drifting ahead of video when per-page dwell is variable.
