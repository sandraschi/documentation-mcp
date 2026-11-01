# AI Music Generation — Landscape Overview (Early 2026)

> Last updated: 2026-03-04

The music generation space has undergone a structural shift in early 2026: the gap between closed commercial tools and open-source alternatives has narrowed dramatically, and Chinese labs have entered with competitive models that operate outside Western IP jurisdiction.

---

## The main players

### Closed-source commercial (Western)

**Suno** (Cambridge, MA)
- Raised $250M Series C (Nov 2025) at a $2.45B valuation
- Best-known consumer-facing product — text prompt to full song with vocals in seconds
- v4.5 and v5 as of early 2026
- Ongoing legal battles with UMG and Sony; settled with Warner (Nov 2025)
- Co-founder famously described themselves as "the Ozempic of the music industry"

**Udio** (New York — team from ex-Google DeepMind)
- Settled with UMG (Oct 2025); licensing agreement for new platform in 2026
- Warner settlement followed; Sony case ongoing
- Technically strong but smaller user base than Suno

**ElevenLabs** (Eleven Music)
- Entered music gen alongside dominant voice synthesis business
- Closed-source, subscription model
- Licensing deal with Merlin (independent labels aggregator)

---

### Big tech (closed but licensed)

**Google** — The dominant player by resources
- **Lyria 3** (launched Feb 18 2026): 30-second tracks in Gemini app, vocal + lyrics, SynthID watermarking
- **Lyria RealTime API**: real-time streaming music with 2-second chunk generation, MIDI-controllable
- **ProducerAI** (acquired Feb 24 2026 — formerly Riffusion): conversational music production interface, full team to Google Labs + DeepMind
- **Music AI Sandbox**: pro tools for artists (Wyclef Jean, etc.)
- **YouTube Dream Track**: AI soundtrack generator for Shorts, now using Lyria 3
- Training data: YouTube/Google partner content, "responsible" development posture

**Apple** — Playing it cautious
- Logic Pro AI features (session players etc.) but not generative music in the Suno sense
- No major standalone product as of early 2026

**Meta / Amazon / Microsoft** — Watching rather than leading

---

### Open-source / FOSS

**ACE-Step v1.5** (ACE Studio + StepFun — China, Jan 2026)
- MIT license, commercially usable outputs
- Training data: licensed + royalty-free + MIDI-to-audio synthetic
- Under 4GB VRAM, runs locally
- Under 10 seconds for a full song on RTX 3090
- 2B-parameter DiT, Qwen3 LM planner
- Benchmarks: beats Suno v5 on SongEval
- See [CHINESE_PLAYERS.md](CHINESE_PLAYERS.md) and [TECHNICAL_ARCHITECTURES.md](TECHNICAL_ARCHITECTURES.md)

**Stable Audio Open** (Stability AI)
- Apache 2.0, instrumental only (no vocals)
- 44.1kHz stereo
- Less capable than ACE-Step v1.5 but established in the ecosystem

**MagentaRT** (Google — open weights)
- 800M parameter autoregressive model for real-time stereo music
- Permissive license
- Separate from Lyria (which is closed); Google's research/community contribution

**AudioCraft / MusicGen** (Meta)
- Apache 2.0
- Still widely used for integration work despite being older architecture
- No vocals

**Riffusion** (original open-source project, Dec 2022)
- Spectrogram diffusion — technically primitive by 2026 standards
- Now absorbed into ProducerAI/Google

---

## Capability snapshot (early 2026)

| Model | Vocals | Duration | Local | License | Quality tier |
|-------|--------|----------|-------|---------|-------------|
| Suno v5 | Yes | Unlimited | No | Proprietary | Commercial SOTA |
| Udio (post-settlement) | Yes | Full songs | No | Proprietary | Commercial SOTA |
| Google Lyria 3 | Yes | 30s (Gemini) | No | Proprietary | Near-commercial |
| ACE-Step v1.5 | Yes | 10s–10min | Yes (RTX 3090) | MIT | Between Suno v4.5–v5 |
| Stable Audio Open | No | ~90s | Yes | Apache 2.0 | Below Suno |
| MagentaRT | No | Streaming | Via API | Permissive | Instrumental |
| MusicGen (Meta) | No | 30s | Yes | Apache 2.0 | Below Suno |

---

## Structural trends

**The FOSS quality gap is closing fast.** ACE-Step v1.5 hitting near-Suno quality in January 2026 means the "you need Suno for good results" argument is no longer true. ACE-Step v2.0 is presumably in the pipeline.

**The legal situation is forcing commercial bifurcation.** Post-settlement, Suno and Udio are pivoting toward licensed training data and partnership deals with labels. This looks like convergence toward the Google model — expensive, slower, but legally defensible.

**FOSS + Chinese models are outside this settlement loop entirely.** ACE-Step can't be served with a US court order in any meaningful way. The model weights are on Hugging Face. Anyone with a 4090 can run it locally with no subscription, no data collection, no legal exposure.

**The content production economics are brutal for human musicians.** Udio was generating 864,000 audio files per day shortly after launch (per the RIAA complaint). At these scales, royalty pool dilution on streaming platforms is real and measurable.

---

## What to watch next

- ACE-Step v2.0 (inevitable; timeline unknown)
- Suno v5 legal exposure — Sony/UMG cases still live
- EU AI Act implications for training data transparency
- Whether Lyria 3 extends beyond 30 seconds
- OpenAI music product (rumored but not released as of Mar 2026)
- GEMA (Germany) cases — different legal system, potentially precedent-setting
