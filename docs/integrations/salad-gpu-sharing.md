# Salad.com GPU Sharing — Goliath Integration Notes

**Status:** Evaluating / Not yet active  
**Last updated:** 2026-05-01  
**Relevant hardware:** Goliath (RTX 4090 24GB, AMD Ryzen 9 5900X, 64GB RAM)

---

## What Is Salad?

Salad.com is a distributed GPU compute marketplace with two sides:

- **SaladCloud** — the enterprise/developer side. Businesses rent idle consumer GPUs for AI inference, image generation, LLM hosting, video transcoding, and other GPU workloads.
- **Salad Chef app** — the contributor side. You install a lightweight Windows app, and when your machine is idle it picks up jobs from the queue and earns you Salad Balance, redeemable for cash (PayPal), Steam games, gift cards, etc.

The community framing is deliberate and genuine: your RTX 4090 might be running inference for a startup in Lagos or a researcher in Nairobi who could never afford datacenter GPU time. Decentralized compute democratizes access to hardware that would otherwise be locked behind AWS/GCP pricing.

---

## Why This Is Interesting for Goliath

Goliath runs 24/7 as a home lab server. Outside of active dev sessions, the RTX 4090 sits largely idle — MCP servers are CPU-bound, Plex transcoding is occasional, and local LLM inference (Ollama/LM Studio) is intermittent. That idle VRAM is a wasted resource.

Key numbers (from Salad's published rates, May 2026). Electricity at Vienna Sozialtarif subsidised rate (~€0.08/kWh estimate — update with actual):

| Metric | Value |
|---|---|
| RTX 4090 hourly rate | ~$0.20/hr |
| Theoretical max (100% utilization) | ~$148/month |
| Realistic (50% utilization) | ~$122/month gross |
| Power draw during AI workloads | ~350W |
| Power cost at ~€0.08/kWh, 50% util | ~€10/month |
| Net at 50% utilization | ~€100/month |
| Open frame thermal risk | None |

The 4090 is specifically listed as a **guaranteed best-workload** GPU — Salad prioritizes it for LLM inference and high-end diffusion jobs, which command the highest rates.

---

## Economics vs. the AI Subscription Stack

Current monthly AI tooling spend (approximate):
- Claude Pro: ~€20
- Cursor Pro: ~€20
- Windsurf Pro: ~€20 (may drop)
- DeepSeek API: variable, low with cache hits

At realistic utilization, Salad earnings could **fully offset DeepSeek API costs** and partially offset one subscription. Not life-changing money, but the hardware cost is already sunk and the electricity is the only marginal cost.

More importantly: idle GPU doing nothing has zero return. Any positive number beats zero.

---

## The Community Angle

Salad's network spans 191+ countries with 400k+ contributing nodes. The workloads that land on a Goliath-class machine are often inference jobs from researchers, small startups, or developers in regions where cloud GPU pricing is prohibitive relative to local income. 

A 4090 in Vienna's 9th district running inference for someone in Nigeria, Nairobi, or Manila at a price point they can actually afford — there's something genuinely appealing about that. Compute as a shared resource rather than a hyperscaler monopoly.

---

## Practical Setup

### Prerequisites
- Windows (required — contributor app is Windows-only) ✓
- NVIDIA GPU (RTX 30/40 series) ✓
- Stable internet (200+ Mbps recommended for large model jobs)
- Account at salad.com

### Installation
1. Download the Salad Chef app from salad.com
2. Sign in / create account
3. The app runs in the system tray and starts/stops earning automatically
4. Configure idle detection threshold (start earning after N minutes idle)

### Config path
The Salad app manages itself — no config files to edit. Earnings dashboard and payout settings are web-based.

---

## Operational Considerations for Goliath

### Thermal

Goliath runs in an open frame — excellent ambient airflow, no enclosure heat buildup. Sustained inference workloads are not a thermal concern. No fan curve tuning needed.

HWiNFO64 monitoring is still worthwhile for a baseline but is not a blocker for going live.

### Conflict with Local Use

The GPU will be occupied when Salad is active. Potential conflicts:

| Activity | Conflict? | Resolution |
|---|---|---|
| MCP servers (CPU-bound) | None | Fine |
| Plex transcoding (NVENC) | Minor | Salad releases GPU on demand |
| Ollama / LM Studio | Yes — same VRAM | Pause Salad before starting local LLM |
| Blender render (GPU) | Yes | Pause Salad before rendering |
| Gaming | Yes | Salad auto-pauses when foreground GPU load detected |

The Salad app has configurable auto-pause triggers (foreground app, CPU load threshold, user activity). Set these appropriately so it doesn't fight with active work.

### DeepSeek V4 Open Weights (June 2026 target)

If/when DeepSeek releases downloadable open weights for V4 (MoE architecture), the 4090's 24GB VRAM may be viable for running it locally — particularly because MoE active parameter count (~3B active per forward pass) is what matters for VRAM, not the total parameter count. This would create a direct conflict with Salad: can't share the GPU and run local inference simultaneously.

**Decision point:** If local DS V4 becomes a daily driver, Salad stops making sense during active hours. If local DS V4 is only used for testing/offline scenarios, Salad remains viable during idle time.

---

## Alternatives Considered

| Platform | RTX 4090 Rate | Notes |
|---|---|---|
| Salad.com | ~$0.20/hr | Best-workload guarantee for 4090, Windows app |
| Vast.ai | ~$0.34–0.45/hr | **Under review** — higher rate, Docker already on Goliath, pending daemon stability fix. See `vastai-gpu-hosting.md` |
| RunPod | ~$0.44/hr | Similar to Vast, more enterprise-oriented |
| ShareAI | ~€2.50/hr (AI jobs) | Higher ceiling, less passive |

Salad wins on **simplicity and passivity** — install and forget. Vast/RunPod require active container management. ShareAI is higher earning but higher effort. For a home lab running 24/7 with no babysitting, Salad is the right fit.

---

## Status / Next Steps

- [ ] Install Salad Chef app and configure idle thresholds
- [ ] Run for one week, monitor thermals and earnings
- [ ] Set fan curve in Afterburner if hotspot temps exceed 88°C under sustained load
- [ ] Confirm auto-pause works correctly when starting Ollama or Blender
- [ ] Revisit in June when DeepSeek open weights situation clarifies

---

## Related

- `integrations/local-llm/` — Ollama, LM Studio, vLLM on Goliath
- `integrations/ollama/` — local inference setup
- `standards/LOCAL_LLM_STANDARDS.md` — fleet local LLM patterns
- DeepSeek V4 Flash API is current daily driver via OpenCode; local weights pending June 2026 release
