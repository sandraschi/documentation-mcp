# FOSS and Local AI Music Generation

> Last updated: 2026-03-04

The open-source landscape has reached a genuinely usable state as of early 2026. ACE-Step v1.5 in particular closes most of the quality gap with commercial tools while running locally, requiring no subscription, and having a clean licensing story.

---

## Why FOSS matters here specifically

For AI image generation, Stable Diffusion made local generation viable in 2022. The "Stable Diffusion moment for music" is ACE-Step v1.5 (January 2026) — explicitly their stated goal.

Key advantages of FOSS/local music gen:
1. **No subscription cost** — especially relevant for creative exploration
2. **No data collection** — your prompts and outputs don't train anyone's commercial model
3. **No content moderation** — generate what you actually want
4. **Permanent ownership** — model weights exist on your disk; no platform risk
5. **Fine-tuning** — LoRA training on your own style with a few reference songs
6. **No copyright liability** — you're running a model trained on licensed data
7. **Offline capable** — works without internet

---

## ACE-Step v1.5 (January 2026)

The current SOTA open-source music generator.

**Resources:**
- GitHub: https://github.com/ace-step/ACE-Step-1.5
- HuggingFace: https://huggingface.co/ACE-Step/Ace-Step1.5
- Paper: https://arxiv.org/abs/2602.00744
- License: MIT

**Hardware requirements:**
- Minimum: 4GB VRAM (enough for the base model)
- Recommended: RTX 3090/4090 (under 10 seconds for a full song)
- Your RTX 4090 will do ~0.5s per song in turbo mode

**Models available:**
- 4x Turbo variants (different shift hyperparameters — trade detail vs. structure)
- 1x SFT (supervised fine-tuned) model
- 1x Base model
- LM in 0.6B (faster) or 4B (better lyric understanding)

**Installation:**
```bash
# Using uv (recommended)
pip install uv
uv run acestep-download  # downloads default turbo + 1.7B LM
uv run acestep-download --all  # all models
uv run acestep-download --list  # see what's available

# Windows needs triton:
pip install triton-windows  # or equivalent
```

**Basic generation:**
```bash
# Start the gradio UI
uv run acestep --torch_compile true --cpu_offload true --overlapped_decode true

# CLI generation
uv run acestep generate \
  --tags "pop, female vocal, piano, melancholic" \
  --lyrics "verse 1: [your lyrics]" \
  --duration 180
```

**Turbo model selection guide:**
- High shift value → emphasis on large structure ("outline first then fill")
- Low shift value → more detail, but potentially noisier
- For vocals: try medium-high shift first
- For dense instrumental: try medium-low shift

**LoRA training:**
- Train on 5–10 reference songs in your target style
- ~few hours on a 4090
- Fine-grained style capture without full fine-tuning
- See TRAIN_INSTRUCTION.md in the repo

**ComfyUI integration:**
- ComfyUI_ACE-Step node available
- Full node-based workflow support
- Language note: non-English lyrics need transliteration first (e.g., [zh] prefix + phonetic)

**Known weaknesses:**
- Seed-sensitive (gacha variance — same prompt gives different quality on different seeds)
- Chinese rap (zh_rap) underperforms
- Repainting transitions are sometimes unnatural
- Voice quality lacks nuance compared to Suno v5

---

## Stable Audio Open (Stability AI)

**Resources:**
- HuggingFace: https://huggingface.co/stabilityai/stable-audio-open-1.0
- License: Stability AI Community License (non-commercial without license)

**What it does:** High-quality stereo instrumental generation at 44.1kHz, up to ~90 seconds.

**What it doesn't:** No vocals. No lyrics. Instrumental only.

**Architecture:** Diffusion with DCAE compression. Older architecture than ACE-Step.

**Use case:** Background music, ambient textures, loops. Fast, predictable, no vocal quality to worry about. Good for content creators who need clean instrumentals.

**Hardware:** More demanding than ACE-Step for equivalent quality — expect 16GB+ VRAM for comfortable use.

---

## MagentaRT (Google — open weights)

**Resources:**
- GitHub: https://github.com/magenta/magenta-realtime
- License: Apache 2.0 (permissive, commercial OK)

**What it does:** 800M parameter autoregressive model for **real-time streaming** music generation. Stereo, 48kHz.

**What it doesn't:** No vocals. Designed for live performance/interactive use, not production.

**Architecture:** Block autoregression, streaming output.

**Use case:** Generative ambient music, live performance tools, interactive installations. Can be controlled via MIDI.

**Note:** Separate from Lyria (which is closed). Google's open research contribution. Less polished than Lyria but you can run it locally.

---

## AudioCraft / MusicGen (Meta)

**Resources:**
- GitHub: https://github.com/facebookresearch/audiocraft
- License: CC-BY-NC-4.0 (non-commercial only for music models)

**What it does:** Text-to-music, audio continuation, melodic conditioning.

**What it doesn't:** No vocals. Limited duration. Getting old architecturally.

**Status:** Largely superseded by ACE-Step for quality, but still widely used in production pipelines because it's well-documented and integrates easily.

**Hardware:** MusicGen Large (~3.3B params) needs ~16GB VRAM.

---

## Practical comparison for Goliath (RTX 4090 + 64GB RAM)

| Model | VRAM needed | Speed | Vocals | Output quality | License |
|-------|-------------|-------|--------|----------------|---------|
| ACE-Step v1.5 turbo | 4GB | ~2-5s/song | Yes | Near Suno v5 | MIT |
| Stable Audio Open | 16GB+ | ~10-30s | No | Mid | Community |
| MagentaRT | 8GB+ | Real-time | No | Instrumental OK | Apache 2.0 |
| MusicGen Large | 16GB | ~60s/30s | No | OK | CC-BY-NC |

ACE-Step v1.5 is the clear winner for general use. On a 4090 you can be running batches of 8 songs in under a minute.

---

## The FOSS competitive moat

The thing the music labels can't easily fix: once a model is MIT-licensed and on Hugging Face with weights, it's out there. You can't DMCA a model's weights out of existence once they're distributed — too many copies, too many forks, too many mirrors. 

Chinese jurisdiction means US courts can't easily compel ACE Studio or StepFun to remove anything. Even if they did, the weights exist on every GPU server that downloaded them. The music industry can litigate against Suno (US-based, has assets) — but they can't litigate against ACE-Step v1.5 in any meaningful way.

This is precisely the "Stable Diffusion moment" — the point where the technology escapes the legal containment zone.

---

## Integration potential

ACE-Step v1.5 has a Python API and CLI. Wrapping it in an MCP server would be straightforward:

```python
# Rough sketch of what a music-mcp would look like
from acestep import ACEStepPipeline

pipeline = ACEStepPipeline.from_pretrained("default")

def generate_music(tags: str, lyrics: str, duration: int = 60) -> str:
    output_path = pipeline.generate(
        tags=tags,
        lyrics=lyrics, 
        audio_duration=duration,
        num_inference_steps=8  # turbo
    )
    return output_path
```

See `projects/songgeneration-mcp` in the fleet index — this is already in the project list.

### SongGeneration v2 (LeVo 2 / SG2) vs cloud (Mar 2026)

Fleet MCP **songgeneration-mcp** targets **local** SongGeneration-Studio with **SG2** (length tags, dual-track `vocal.wav` / `inst.wav`). As a complement—not a replacement—for **Gemini Lyria 3 Pro** in the cloud: Lyria is often **~$0.08 per song** in typical Gemini credit tiers (**verify** current pricing); SG2 shines for **classical**, **rubato**, and **instrumental** control and avoids a single vendor’s musical defaults. Many workflows use **both** (Google AI for speed, open weights for repertoire and sovereignty). Canonical write-up: [sandraschi/songgeneration-mcp](https://github.com/sandraschi/songgeneration-mcp) `docs/LYRIA_VS_SG2.md`.
