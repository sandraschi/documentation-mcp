# Salad.com GPU Sharing — Fleet Integration & Evaluation Guide

**Status:** Evaluated / Integration Reference  
**Last updated:** 2026-08-25  
**Relevant hardware:** Goliath (NVIDIA RTX 4090 24GB VRAM, AMD Ryzen 9 5900X, 64GB RAM, 2TB NVMe)  
**See also:** `integrations/vastai-gpu-hosting.md`

---

## Executive Summary

Salad (`salad.com`) is a distributed consumer GPU compute marketplace. Node providers ("Chefs") run the desktop client on idle Windows PCs to earn Salad Balance (redeemable via PayPal, crypto, store gift cards, or Visa prepaid cards). The client-facing cloud platform (**SaladCloud**) rents this hardware to developers and enterprise clients for AI/ML inference, image generation, audio transcription, and video processing container workloads.

For an **NVIDIA RTX 4090 (24GB VRAM)**, Salad offers one of the simplest set-and-forget Windows sharing options, though net profitability is highly dependent on local electricity costs and network workload demand.

---

## Expected Income PCM (Per Calendar Month)

Earnings on Salad are derived from **container job fulfillment** rather than traditional crypto mining. 

### Gross Income Rates (RTX 4090)
* **Hourly Rate (Active Container Job):** ~$0.12 – $0.22 / hour
* **Daily Average (24/7 Availability):** ~$3.00 – $5.50 / day (subject to demand)
* **Gross Income PCM:** **~$90 – $160 / month**

### Net Profitability Matrix (Factoring Power Costs)
An RTX 4090 system running full AI container workloads draws approximately **400W – 500W total wall power** (~10.8 – 12 kWh/day = **~324 – 360 kWh/month**).

| Electricity Tariff | Monthly Power Cost | Estimated Net Profit PCM | Feasibility |
| :--- | :--- | :--- | :--- |
| **Subsidized / Free / Solar** (€0.05 / $0.05 per kWh) | ~$16 – $18 / month | **~$75 – $140 / month** | Highly Profitable |
| **Standard US Rate** ($0.15 per kWh) | ~$48 – $54 / month | **~$45 – $100 / month** | Profitable |
| **Standard EU Rate** (€0.28 – €0.35 per kWh) | ~$90 – $120 / month | **~$0 – $35 / month** | Marginal / Loss Risk |

> [!IMPORTANT]
> **Hardware Prerequisites for High-Tier Container Jobs:**  
> Salad prioritizes nodes with at least **32 GB System RAM** (64 GB recommended), **500 GB+ SSD space**, and an unmetered, high-speed internet connection (100+ Mbps). Nodes below 32 GB RAM will miss out on top-paying LLM and Stable Diffusion jobs.

---

## Comprehensive Pros & Cons

### Pros
1. **Low Friction & Set-and-Forget:** Simple Windows desktop application (`Salad Chef`). Auto-detects system idle state and manages container workloads automatically.
2. **Top-Tier Card Priority:** The RTX 4090's 24 GB VRAM places it in the highest demand tier for enterprise container rentals (e.g., vLLM inference, SDXL/FLUX image generation, Whisper transcription).
3. **Container Sandbox Isolation:** Workloads execute inside Windows Subsystem for Linux 2 (WSL2) / Hyper-V containers, preventing jobs from accessing host files or OS state.
4. **Flexible Cashout Options:** Earnings can be cashed out to PayPal, pre-paid Visa cards, crypto (BTC/ETH), or digital platforms (Steam, Discord Nitro, Amazon).

### Cons
1. **Heavy Electricity Sensitivity:** Under sustained 400W–450W GPU load, power consumption eats 40% to 80%+ of gross revenue on non-subsidized utility tariffs.
2. **Demand Fluctuation & Idle Downtime:** Payouts are non-guaranteed. During low demand cycles, machines sit idle or drop to minimal earnings.
3. **Thermal & Hardware Degradation:** Continuous 24/7 high-power utilization produces substantial room heat (~450W thermal output) and accelerates fan and thermal pad degradation.
4. **ISP Data & Proxy Risks:** The optional "Bandwidth Sharing" feature turns your node into a residential proxy exit node, which can trigger ISP data cap warnings or security flags if left unmonitored.

---

## Community Acceptance, Security & Reputation

* **Platform Legitimacy:** Salad is an established, widely accepted service with a large community (tens of thousands of active nodes on `r/SaladChefs`).
* **Antivirus Detections:** The installer occasionally triggers antivirus alerts (false positives) due to legacy cryptomining executables bundled as fallback payloads. The client itself is legitimate and safe to whitelist.
* **Privacy & ISP Stance:** Salad claims residential proxy traffic is restricted to streaming domains (e.g., Netflix, Hulu unblocking). However, community consensus strongly advises **disabling "Bandwidth Sharing"** in settings while keeping **"GPU Container Workloads" enabled** to avoid ISP flagging or data quota exhaustion.

---

## Commercial Competitors Matrix (Paid GPU Hosting)

If higher yield or direct marketplace hosting is desired, consider these alternatives:

| Platform | Model | RTX 4090 Rates | Key Pros | Key Cons / Requirements |
| :--- | :--- | :--- | :--- | :--- |
| **[Salad.com](https://salad.com)** | Managed Queue | ~$0.12–$0.22/hr | Passive Windows app, simple cashout | Lower hourly rate, variable demand |
| **[Vast.ai](https://vast.ai)** | Direct P2P Marketplace | ~$0.34–$0.45/hr | ~70% higher payouts, host control | Requires Linux, static IP, Docker maintenance |
| **[RunPod Community](https://runpod.io)** | Cloud Rental | ~$0.35–$0.44/hr | Enterprise reputation, steady demand | Strict host verification, Linux required |
| **[io.net](https://io.net)** | DePIN AI Cluster | Variable (Tokenized) | High yields during token reward campaigns | Paid in $IO token (crypto market volatility) |
| **[Akash Network](https://akash.network)** | Decentralized Cloud | Variable ($AKT) | Open-source Kubernetes network | Requires Cosmos wallet & K8s host setup |
| **[Clore.ai](https://clore.ai)** | P2P Compute | Variable ($CLORE) | Simple portal for host rigs | Price tied to native altcoin |

---

## FOSS & Free Alternatives (Share Compute for Open Source / Science)

For users who wish to donate their RTX 4090 compute power to open-source AI models, medical research, or scientific computing for free:

### 1. Open AI & P2P LLM Inference
* **[Petals](https://petals.dev)** (FOSS, MIT License): BitTorrent-style peer-to-peer network for running large language models (e.g., Llama-3, Mixtral). You donate your 4090's 24 GB VRAM to host specific model layers, allowing researchers and the public to run massive LLMs for free without cloud subscriptions.
* **[Exo](https://github.com/exo-explore/exo)** (FOSS, Apache-2.0): Combines your local 4090 with other devices across your local network (Macs, secondary PCs, single-board computers) into a unified virtual GPU for home LLM inference.
* **[Hivemind](https://github.com/learning-at-home/hivemind)** (FOSS, MIT): Framework for collaborative, decentralized neural network training across internet nodes using Decentralized Mixture of Experts (DMoE).

### 2. Volunteer Scientific Research
* **[Folding@home](https://foldingathome.org)**: Donates GPU cycles to perform molecular dynamics simulations for disease research (cancer, Alzheimer's, Parkinson's). An RTX 4090 achieves millions of points per day (PPD) and is highly efficient.
* **[BOINC](https://boinc.berkeley.edu)** (FOSS, LGPL): The classic volunteer computing platform. Dedicated GPU projects include:
  * **GPUGrid.net**: High-performance biomedical and molecular simulations.
  * **Einstein@Home**: Searching for radio pulsars and gravitational waves from neutron stars.

---

## Goliath Fleet Integration Stance

1. **Current Fleet Posture:** Goliath runs 24/7 as a home lab server hosting MCP services, Ollama/vLLM local inference, and media servers.
2. **Salad Usage Mode:** If activated on Goliath, Salad should run strictly in **GPU Container mode** with **Bandwidth Sharing disabled**, with auto-pause enabled when local LLMs (Ollama) or Blender renders are launched.
3. **Net Profit Decision Threshold:** At local Austrian/German electricity rates, hosting is only viable if power cost stays below €0.15/kWh or when surplus solar energy is available.

---

## Related Documentation

* `integrations/vastai-gpu-hosting.md` — Direct P2P GPU marketplace hosting guide
* `integrations/local-llm/README.md` — Goliath local LLM stack (Ollama, LM Studio, vLLM)
* `standards/LOCAL_LLM_STANDARDS.md` — Fleet standards for local inference vs cloud APIs
