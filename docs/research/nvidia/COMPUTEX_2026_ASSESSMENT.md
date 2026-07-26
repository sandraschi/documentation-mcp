# COMPUTEX / GTC Taipei 2026 — NVIDIA × Microsoft Windows AI stack

**Assessment date:** 2026-06-03  
**Event anchor:** NVIDIA keynote at COMPUTEX 2026 (31 May 2026); aligned announcements at **GTC Taipei** and **Microsoft Build** (2–3 Jun 2026).  
**Analyst context:** Sandra fleet — local agents, MCP, Windows-first dev; **affordable tier** vs **lottery-tier** enterprise deskside.

---

## Executive summary

NVIDIA and Microsoft are selling a **three-rung ladder** on Windows, all framed around **on-device agents** and **OpenShell** on new OS security primitives:

| Rung | Product line | Silicon | Memory | Model class (marketing) | Price band (2026) |
|------|----------------|--------|--------|-------------------------|-------------------|
| **Personal / dev** | RTX Spark PCs (incl. Surface) | Blackwell RTX + 20-core Grace (Arm) | Up to **128 GB** unified | ~**120B** LLM, 1M-token context (claimed) | **No MSRP yet**; DGX Spark FE **~$4,699** is the closest shipped reference; premium laptops likely **$2k–$5k+** |
| **Compact desktop dev** | Surface RTX Spark Dev Box, SFF OEMs | Same RTX Spark class | **128 GB** (stated) | Fine-tune / agents / CUDA stack | Pre-order list only; FCC pending |
| **Enterprise deskside** | DGX Station for Windows | **GB300** Grace Blackwell Ultra | Up to **748 GB** coherent | Up to **1T** parameters (claimed) | **~$100k+** (no official MSRP; OEM quote) |

**Verdict for “I could actually afford this”:** The **RTX Spark / Surface** tier is the realistic target — not DGX Station. Budget for **high four figures** if you want 128 GB unified (memory shortage already moved **DGX Spark** from $3,999 → **$4,699**). Do not plan purchases from keynote FLOP claims alone; wait for **independent benchmarks** and **EU pricing**.

**Verdict for startups / uni labs (non-elite):** One RTX Spark-class **shared dev box** or **2–3 laptops** beats one DGX Station for most teaching and product R&D. DGX Station is **capital equipment**, not a desk upgrade.

**Verdict vs last year’s DGX Spark:** The **2025 GB10 box** failed on **sustained GPU / bandwidth**, not OS. **GB300 / DGX Station** is the disclosed big silicon step. For **Surface / RTX Spark**, public press mostly still says **GB10/N1X** — but **~2 years to fall 2026** makes a **silent die improvement** plausible; **~10× sustained** vs GB10 is the rational **buy bar** (see **[dgx-spark-lessons-vs-2026-silicon.md](dgx-spark-lessons-vs-2026-silicon.md)**). Without launch benchmarks, assume **GB10 + Windows = deco piece**; if **`nvidia-smi` bandwidth** jumps toward **HBM-class** or decode **~10×**, reassess.

---

## Announcement map (Computex week)

### Tier A — Platform (defines everything else)

1. **[RTX Spark superchip](products/rtx-spark-platform.md)** — Windows “personal AI computer”; CUDA + full RTX stack on Arm SoC; fall 2026 OEM wave.
2. **Windows platform work** — WPS scheduling, MPTF thermals, unified-memory GPU limits, larger pages in shared regions, Prism tuned for Spark, Windows ML + TensorRT, Copilot+ NPU category.
3. **Agent security** — OS identity/containment/policy; **NVIDIA OpenShell**; Hermes Agent + OpenClaw native Windows apps; NemoClaw on Linux/WSL across RTX/DGX.
4. **Inference software wave** — 2× llama.cpp, 2.6× vLLM on agentic models; multi-GPU bumps; Adobe/Blender/ComfyUI RTX Spark rebuilds.

### Tier B — Microsoft Surface (your affordable-interest products)

5. **[Surface RTX Spark Dev Box](products/surface-rtx-spark-dev-box.md)** — Desktop, developer-first Windows 11 Pro image, 100 W thermal story.
6. **[Surface Laptop Ultra](products/surface-laptop-ultra.md)** — 15″ portable, sustained performance, repairable SSD, iFixit path.

### Tier C — Enterprise (previous conversation)

7. **[DGX Station for Windows](products/dgx-station-windows.md)** — GB300, Q4 2026, trillion-parameter narrative.

### Tier D — Same week, adjacent (not Windows PC purchase guides)

- DLSS 4.5 Ray Reconstruction (games + Blender 5.3 fall).
- 1000+ RTX apps milestone; 11 more DLSS 4.5 games.
- GeForce partner SKUs at COMPUTEX.
- Other GTC Taipei newsroom items: TSMC fab AI, Foxconn/Taiwan health, Isaac GR00T academic humanoid, DRIVE Hyperion robotaxi platform, open-source physical-AI agent tools.

---

## Deep assessment: RTX Spark platform

### What is actually new

Historically **Windows on Arm + GPU** meant compromise (Prism, driver gaps, no CUDA parity). NVIDIA’s pitch is the inverse: **CUDA-first personal SoC** with Microsoft doing scheduler/memory/Prism work so Arm is not the bottleneck for dev and agents.

**Silicon (from NVIDIA newsroom, consistent across GeForce post):**

- **GPU:** Blackwell RTX, **6,144 CUDA cores**, 5th-gen Tensor Cores with **FP4**.
- **CPU:** **20-core Grace** (Arm); **MediaTek** co-designed custom CPU for efficiency/connectivity.
- **Interconnect:** NVLink-C2C between CPU and GPU.
- **AI peak:** Up to **1 petaflop** (FP4/marketing — treat as upper-bound label).
- **Memory:** Up to **128 GB unified** — the enabler for large local models and big 3D/video working sets.

**Workload claims (marketing — verify at launch):**

- **Agents:** 120B-parameter LLM, up to **1M token** context locally.
- **Create:** 90 GB+ 3D scenes (OptiX/DLSS), 12K 4:2:2 video, 4K AI video gen.
- **Game:** AAA **1440p @ 100+ FPS** with RT + DLSS + Reflex.
- **Form:** Laptops **14–16″**, as thin as **14 mm**, ~**3 lb**; compact desktops.

**Software moat (real if shipped):**

- Full **CUDA / TensorRT / OptiX** on primary Windows device — not “cloud API only.”
- **OpenShell** + Windows primitives — aligns with [NeMoClaw/OpenShell research](../research/NVIDIA_NEMOCLAW_ANALYSIS.md).
- Adobe **re-architecting** Premiere/Photoshop for Spark (2× AI/graphics claimed); many ISVs named (Blender DLSS RR, ComfyUI RTX Video frame gen, etc.).

### Risks and skepticism

| Risk | Detail |
|------|--------|
| **GB10 déjà vu** | **DGX Spark (2025)** sold poorly: **bandwidth-bound** GPU, **~35–40 tok/s** decode class on large models despite 128 GB. **RTX Spark may reuse GB10** — “2026 silicon” for *affordable* tier might mean **Windows + 2× software**, not a faster die. |
| **Naming collision** | **DGX Spark** (GB10, Linux-first mini PC, **$4,699**) vs **RTX Spark** (Windows consumer brand). Same “1 PFLOP / 128 GB” messaging confuses buyers. |
| **Arm + Prism** | Windows blog promises Prism + AVX2 path; legacy x64 tools may still lag native Arm builds. |
| **“1M tokens”** | Requires memory + software stack proof; likely extreme quant + offload patterns, not “full quality chat with GPT-4-class at speed.” |
| **Memory economics** | Feb 2026 DGX Spark **+18%** price on LPDDR5X — RTX Spark SKUs will inherit DRAM pressure. |
| **Agent hype** | Taskbar agents + OpenClaw/Hermes are ecosystem bets; security primitives at Build must be concrete (APIs, audit, enterprise policy). |
| **No consumer pricing** | Fall 2026; FCC disclaimers on Surface pages — not shippable yet. |

### Affordability model (for Sandra)

Use **DGX Spark Founders Edition ($4,699)** as a **floor anchor** for a **128 GB unified** NVIDIA box with AI positioning — not a ceiling. Surface/Microsoft premium will add margin. Reasonable planning bands:

- **Entry RTX Spark laptop** (if exists): unlikely below **~$1,800** (analyst chatter); may be GPU-cut SKUs not 128 GB.
- **Serious dev (128 GB):** **$3,500–$5,500** guess until SKUs leak.
- **Surface RTX Spark Dev Box:** expect **at or above DGX Spark** plus Windows OEM tax unless Microsoft subsidizes dev channel.

**Compared to current fleet (e.g. RTX 4090 tower):** 4090 wins raw bandwidth and mature tooling today; Spark wins **unified 128 GB** and **laptop/SFF** form for agents + travel. Not a automatic upgrade — a **role split** (desktop inference vs. agent/dev mobile node).

---

## Deep assessment: Microsoft Surface pair

See dedicated briefs:

- [Surface RTX Spark Dev Box](products/surface-rtx-spark-dev-box.md)
- [Surface Laptop Ultra](products/surface-laptop-ultra.md)

**Cross-cutting Surface assessment:**

| Dimension | Dev Box | Laptop Ultra |
|-----------|---------|----------------|
| **Role** | Fixed desk; “code on day one” | Mobile “world makers”; sustained load |
| **Thermal** | 100 W envelope, aluminum grid chassis | **2.5×** thermal capacity vs Surface Laptop 7 15″ (MS claim) |
| **Out-of-box** | VS Code, Copilot in Terminal, WSL, PS7 | Copilot+ PC; creative/gaming positioning |
| **Enterprise** | Secured-core, BitLocker, Entra, Intune | Hello, secured-core narrative, repair guides |
| **Status** | Pre-release, FCC, email capture | Pre-release, FCC, email capture |
| **Buy signal** | Best if you want **Microsoft-curated AI dev image** on Spark silicon | Best if you need **portable** 128 GB-class with display for color work |

**Honest gap:** Neither page lists **CPU model, GPU TDP, RAM tiers, storage, or price**. Treat both as **intent prototypes** until Microsoft Store SKUs appear.

---

## Deep assessment: DGX Station for Windows (contrast only)

Full brief: [products/dgx-station-windows.md](products/dgx-station-windows.md).

- **GB300** Grace Blackwell Ultra: **72-core Grace**, Blackwell Ultra GPU, **748 GB** coherent memory, **20 PFLOPS FP4** (peak).
- Optional **RTX PRO 6000** for viz/sim; **ConnectX-8** up to **800 Gb/s** for multi-node.
- **Q4 2026** via ASUS, Dell, GIGABYTE, HP, MSI, Supermicro.
- **Use case:** Enterprise always-on agents tied to Windows LOB apps, hundred-agent concurrency, frontier local models — **not** personal affordability.

Same **OpenShell** story as Spark, but hardware tier is datacenter-class shrunk to deskside.

---

## Fleet / MCP implications

| Area | Action |
|------|--------|
| **local-llm-mcp** | Plan test matrix for **128 GB unified** Windows when hardware available; validate Ollama/vLLM/llama.cpp against Microsoft’s 2× claims on *your* models. |
| **OpenShell / NemoClaw** | Track Build 2026 docs for containment APIs; don’t rewrite fleet security until primitives are documented. |
| **MCD RAG** | Ingest this `nvidia/` folder on next `just mcd-sync` if docs MCP indexes `mcp-central-docs`. |
| **Procurement** | Short term: **DGX Spark** or **4090 + RAM** if budget locked; medium term: **Surface Dev Box** when priced; long shot: uni grant for DGX Station. |

---

## Hype vs. reality checklist

Before spending:

1. **Independent review** of 120B / context claims on shipping SKU.
2. **WSL2 CUDA** parity vs. native Windows for your MCP servers.
3. **EU availability** and **Austria VAT** on US-priced DGX Spark reference.
4. **Power draw** at desk (Dev Box 100 W claim is package — wall draw higher).
5. **Repair** — Laptop Ultra iFixit story is positive; Dev Box 3D-printed chassis may complicate RMA.

---

## Document history

| Date | Change |
|------|--------|
| 2026-06-03 | Initial assessment from Computex/GTC Taipei + Surface pages |
