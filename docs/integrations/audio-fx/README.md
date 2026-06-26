# Audio FX & Neural Foley Hub

Welcome to the **Audio FX** integration hub. This section documents the transition from traditional sample libraries to SOTA 2026 generative acoustic models.

## 🥥 What is "Foley"?
**Foley** is the reproduction of everyday sound effects (footsteps, cloth rustling, breaking glass) that are added to media in post-production to enhance audio quality. 

### [Jack Foley: The Pioneer](jack-foley.md)
The term is named after **Jack Foley** (1891–1967), a sound pioneer at Universal Studios. In 1927, during the transition from silent to "talkie" films, Foley developed a technique of performing sound effects live and in sync with the film on a "Foley stage."
- He is indeed the **"Pioneer of Clipeddy-Clop,"** famously using coconut halves to simulate horse hooves—a technique that remains a staple of sound design 100 years later.

---

## 🚀 SOTA 2026 Landscape
In the current MCP ecosystem, we have moved beyond Jack Foley's physical stage into **Neural Foley**—where AI models generate high-fidelity, context-aware sounds from simple text or video prompts.

### Primary Generative Models

| Service | Architecture | Primary Use Case |
| :--- | :--- | :--- |
| **[ElevenLabs SFX](elevenlabs-sfx.md)** | Text-to-SFX | High-fidelity one-shots, cinematic impacts, and clean transients. |
| **[Noiz AI](noiz-ai.md)** | Foley Physics Model | Granular control over material physics (wood, stone, metal) and ADSR. |
| **[Stable Audio](stable-audio.md)** | Latent Diffusion | Long-form environmental soundscapes and non-musical atmospheres. |
| **[FoleyCrafter](foleycrafter.md)** | Video-to-Audio | Automatically synchronizing sounds to video frame events. |

---

## 🛠️ Integration Patterns
Audio FX integrations in the fleet typically follow one of two patterns:

1. **Direct API Retrieval**: Fetching a specific sample via an MCP tool (e.g., `get_sfx(prompt="laser blast")`).
2. **Procedural Embedding**: Dynamically generating and layering sounds within a DAW bridge (e.g., Reaper or Audiotool Nexus).

---
> [!NOTE]
> For core voice synthesis (TTS), see the **[Gemini Hub](../gemini.md)** or **[Hume AI](../hume/README.md)** sections.
