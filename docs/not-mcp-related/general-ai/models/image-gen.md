# Image Generation Models - November 2025

**Status:** The Open Weights Renaissance

---

## The Landscape

2025 solidified the split between closed API giants and open-weights insurgents. The closed models (Midjourney, DALL-E 3, **Nano Banana Pro**) offer polish, ecosystem integration, and safety rails. The open models (FLUX.2, Stable Diffusion) offer control, local deployment, and freedom from content policies.

**The November 2025 showdown:**
- **FLUX.2** (Black Forest Labs) — open weights, 4MP, 10-image multi-ref
- **Nano Banana Pro** (Google) — closed, 4K, 14-image blending, Knowledge Graph context

For anyone with a 4090, open models win on flexibility. For ecosystem users (Google Workspace, Adobe CC), Nano Banana Pro is compelling.

---

## FLUX.2 - The New King (November 2025)

**Black Forest Labs** (the Stable Diffusion alumni) dropped FLUX.2 and it's a generational leap.

### What's New

| Feature | FLUX.1 | FLUX.2 |
|---------|--------|--------|
| Max Resolution | 2MP | **4MP** |
| Multi-Reference | No | **Up to 10 images** |
| Text Rendering | Okay | **Excellent** |
| Prompt Following | Good | **Near-perfect** |
| Character Consistency | Manual LoRAs | **Built-in** |

### Model Variants

| Variant | Weights | Use Case | Hardware |
|---------|---------|----------|----------|
| **FLUX.2 [pro]** | Closed (API) | Best quality, fast | Cloud |
| **FLUX.2 [flex]** | Closed (API) | Full param control | Cloud |
| **FLUX.2 [dev]** | Open (HuggingFace) | Local deployment | 24GB VRAM (4090 ✓) |
| **FLUX.2 [klein]** | Open (Beta) | Distilled/compact | 12GB VRAM |

### Running Locally (4090)

```bash
# ComfyUI (recommended)
# 1. Download FLUX.2-dev from HuggingFace
# 2. Place in ComfyUI/models/checkpoints/
# 3. Use FLUX workflow nodes

# Or via diffusers
pip install diffusers transformers accelerate
```

**VRAM Usage:**
- Full precision: ~20-22GB
- FP16: ~12-14GB  
- Quantized (GGUF): ~8-10GB

The 4090's 24GB handles FLUX.2-dev at full resolution without quantization. Finally.

### Strengths

- **Typography:** Actually renders text correctly. Signs, UI mockups, infographics — all work.
- **Multi-reference:** Feed it 10 images of a character, get consistent output.
- **Photorealism:** Closes the gap with real photography.
- **Prompt adherence:** Complex compositional prompts actually work.

### The "Open Source" Drama

Some purists complain FLUX.2 isn't "truly open" because training data/process isn't disclosed. Weights are available. That's what matters for local deployment. Move on.

---

## The Competition

### Stable Diffusion 3.5 (Stability AI)

- Still relevant for specific use cases
- Lighter weight options available
- Community LoRA ecosystem remains strong
- **Status:** Overshadowed by FLUX.2

### Midjourney v7

- Closed API only (Discord/Web)
- Exceptional aesthetic quality
- Strong at "vibe" prompts
- **Limitation:** No local deployment, content policies

### DALL-E 3 (OpenAI)

- Integrated into ChatGPT
- Good for quick generations
- Strong safety rails (limiting for some use cases)
- **Limitation:** No local, API costs add up

### Google Nano Banana Pro (November 20, 2025)

**Also known as:** Gemini 3 Pro Image

The real competitor to FLUX.2 from the closed side. Launched alongside Gemini 3.

**Capabilities:**
- **4K resolution** output
- **14-image blending** (beats FLUX.2's 10) with visual consistency
- **Multilingual text rendering** — excellent for infographics, posters
- **Studio-quality editing** — camera angles, lighting, color grading
- **SynthID integration** — can detect AI-generated images
- **Context-enriched** via Google Knowledge Graph

**Availability:**
- Gemini App (Android/iOS)
- Google Search AI Mode (Pro/Ultra users, US)
- NotebookLM
- Gemini API / Google AI Studio
- **Adobe Firefly & Photoshop** — unlimited gen through Dec 1 for CC Pro subscribers
- Antigravity IDE, Flow

**Access Tiers:**
- Free Gemini: Limited
- AI Plus/Pro/Ultra: Higher limits

**Limitations:**
- Still struggles with small faces, fine details
- Google ecosystem lock-in
- No local deployment (obviously)

**Sources:** [TechRadar](https://www.techradar.com/ai-platforms-assistants/gemini/google-launches-nano-banana-pro-a-massive-leap-in-ai-image-editing-powered-by-gemini-3-pro), [Tom's Guide](https://www.tomsguide.com/ai/nano-banana-pro-is-here-these-are-all-of-the-new-features-in-googles-latest-ai-image-generator), [DeepMind](https://deepmind.google/models/gemini-image/pro/)

---

## Practical Recommendations

### For Local Deployment (You have hardware)

**→ FLUX.2-dev** 

No contest. 4090 runs it beautifully. Download from HuggingFace, use ComfyUI.

### For Quick Web Use

**→ Midjourney** (aesthetics) or **FLUX.2 Playground** (control)

### For API Integration

**→ FLUX.2 [pro] API** or **Replicate** (hosts FLUX models)

### For Specific Styles/Characters

**→ FLUX.2-dev + LoRAs** 

The LoRA ecosystem is growing fast. Train your own or use community models.

---

## The Takeaway

The 4090 is now the "reference card" for local image gen. FLUX.2-dev runs at full quality without compromises. The open-weights insurgency won this round.

Closed models still have their place (Midjourney for aesthetics, DALL-E for convenience), but if you own the hardware, you own the capability. No API costs, no content filters, no rate limits.

**Source:** [Black Forest Labs](https://bfl.ai/flux2)

