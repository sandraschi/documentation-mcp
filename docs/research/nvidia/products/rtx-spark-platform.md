# RTX Spark platform (superchip + OEM ecosystem)

**Sources:** [NVIDIA press release](https://nvidianews.nvidia.com/news/nvidia-microsoft-windows-pcs-agents-rtx-spark), [Windows Experience Blog](https://blogs.windows.com/windowsexperience/2026/05/31/introducing-a-powerful-new-chapter-for-windows-pcs-accelerated-by-nvidia-rtx-spark/), [GeForce COMPUTEX 2026](https://www.nvidia.com/en-us/geforce/news/computex-2026-nvidia-geforce-rtx-announcements/)  
**Status:** Announced 2026-05-31; **availability fall 2026**; pricing **TBD**.

---

## Product definition

**NVIDIA RTX Spark™** is a **superchip** (not a single SKU name for one PC). OEMs build laptops and compact desktops around it. Microsoft positions the result as the first Windows PCs **purpose-built for personal agents**, with the full **CUDA + RTX** stack on **Arm**.

Do not confuse with **NVIDIA DGX Spark** (GB10, Linux-oriented mini PC, separate product line, **~$4,699** MSRP as of Feb 2026).

**Market reality (GB10 generation):** DGX Spark was widely judged **too slow for the price** — LPDDR bandwidth (~273 GB/s) caps decode; 128 GB only helps **fit** large quant models. Several outlets map **RTX Spark to the same GB10 class**; treat throughput claims as **unproven** until ship. See **[../dgx-spark-lessons-vs-2026-silicon.md](../dgx-spark-lessons-vs-2026-silicon.md)**.

---

## Silicon specification (disclosed)

| Component | Specification |
|-----------|---------------|
| GPU | NVIDIA Blackwell **RTX**, **6,144 CUDA** cores, 5th-gen Tensor Cores (**FP4**) |
| CPU | **20-core** NVIDIA **Grace** (Arm); custom design with **MediaTek** |
| Interconnect | **NVLink-C2C** (chip-to-chip) |
| AI compute (peak) | Up to **1 petaflop** (marketing; precision not always stated in headlines) |
| Memory | Up to **128 GB unified** memory |
| Display ecosystem | Tandem OLED, **G-SYNC** (OEM-dependent) |

---

## Microsoft Windows optimizations (platform layer)

From Windows Experience Blog — these are **OS differentiators**, not GPU specs:

- **Workload Profile Scheduling (WPS)** tuned for 20-core heterogeneous scheduling.
- **Microsoft Power and Thermal Framework (MPTF)** on RTX Spark for efficiency under load.
- **Unified memory:** higher GPU-accessible system memory cap; improved **page size** behavior in shared regions for large AI/render workloads.
- **Prism** emulator: AVX/AVX2 path, microarchitecture tuning for x86 apps on Arm.
- **Windows ML** + **TensorRT** native path for local AI dev.
- **DirectX 12** neural rendering / RT tuning for Blackwell GPU.
- Category: **Copilot+ PC** (includes NPU in addition to discrete-class GPU).

---

## Agent + security stack

| Layer | Responsibility |
|-------|----------------|
| Windows primitives | Identity, containment, policy, E2E security for native agents |
| **NVIDIA OpenShell** | Per-agent sandbox; policy outside model reach; local vs cloud routing by privacy rules; PII masking for cloud queries |
| Apps | **Hermes Agent**, **OpenClaw** integrating OpenShell + primitives in Windows apps |
| Linux path | **NemoClaw** installers across RTX/DGX via WSL |

Build 2026 (Jun 2–3) expected to detail developer-facing security APIs.

---

## Software performance claims (verify at launch)

| Claim | Source |
|-------|--------|
| **120B** LLM, **1M** token context local | NVIDIA newsroom |
| **2×** Adobe Premiere/Photoshop AI & graphics (re-architecture) | NVIDIA + Adobe quotes |
| **2×** llama.cpp, **2.6×** vLLM on top agentic models | GeForce COMPUTEX post |
| Multi-GPU **2×** extra in llama.cpp / ComfyUI | GeForce COMPUTEX post |
| DLSS **4.5** Ray Reconstruction; RTX Video **4×** frame gen in ComfyUI | GeForce / newsroom |

---

## OEM devices (fall 2026)

**Launch wave:** ASUS, Dell, HP, Lenovo, **Microsoft Surface**, MSI.  
**Follow:** Acer, GIGABYTE.

Named examples from Windows blog:

- ASUS ProArt P16 / P14  
- Dell XPS 16 Creator Edition  
- HP OmniBook Ultra 16 / OmniBook X 14  
- Lenovo Yoga Pro 9  
- MSI Prestige N16 Flip AI+  
- **Surface Laptop Ultra** — see [surface-laptop-ultra.md](surface-laptop-ultra.md)  
- **Surface RTX Spark Dev Box** — see [surface-rtx-spark-dev-box.md](surface-rtx-spark-dev-box.md)

Physical targets (NVIDIA): laptops **14 mm** thin, **~3 lb**; aluminum chassis; 14–16″.

---

## Assessment: who should care

**Strong fit:** Windows-native agent developers, creators needing **large unified memory** on laptop/SFF, CUDA researchers who refuse Linux-only desks.

**Weak fit:** Pure gamers optimizing $/FPS (RTX 50 desktop may win value), teams needing **>200B** local without cloud, buyers needing **price certainty** today.

**Pricing expectation:** No MSRP. Use **DGX Spark $4,699** (128 GB class) as reference; laptop premiums and memory shortage likely push **meaningful configs** into **high four figures**.

---

## Fleet link

- Parent: [COMPUTEX_2026_ASSESSMENT.md](../COMPUTEX_2026_ASSESSMENT.md)  
- Related: [NVIDIA_NEMOCLAW_ANALYSIS.md](../../research/NVIDIA_NEMOCLAW_ANALYSIS.md)
