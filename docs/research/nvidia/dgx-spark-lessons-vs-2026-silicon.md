# DGX Spark (2025) lessons vs 2026 silicon claims

**Last updated:** 2026-06-30

> **June 2026 update:** DeepSeek DSpark speculative decoding roughly **doubles** effective throughput on DGX Spark (19-42 tok/s -> ~60 tok/s), making 2x DGX Spark **marginally usable** for local DeepSeek V4 Flash inference. See **[deepseek-dspark-on-dgx-spark.md](deepseek-dspark-on-dgx-spark.md)** for the full viability reassessment. This does **not** change the bandwidth-wall physics -- 60 tok/s is still slow -- but it moves the hardware from "dud" to "usable for deep-context agent work if you can find cheap used units."  
**Context:** Field consensus — last year’s **DGX Spark** disappointed; **128 GB unified RAM did not fix a slow GPU**. This note separates what actually failed, what is **genuinely new silicon**, and what is **rebranding + software**.

---

## Why DGX Spark was a dud (not hype — physics + product)

The **GB10 “Grace Blackwell” Superchip** in DGX Spark was a **capacity play**, not a **throughput play**. Buyers expecting “mini supercomputer” speed for daily inference were burned.

| Factor | Reality |
|--------|---------|
| **Memory bandwidth** | **~273 GB/s** LPDDR5X unified — an order of magnitude below discrete **GDDR7** cards (e.g. RTX 5090 ~1.8 TB/s class). Decode/token generation is **memory-bound**. |
| **GPU scale** | ~**6,144 CUDA** cores, arch between **RTX 5070 / 5070 Ti** laptop class — not a datacenter Blackwell part. |
| **“1 PFLOP”** | **Sparse FP4** marketing peak — not comparable to sustained FP16/BF16 on a desktop GPU. |
| **128 GB unified** | Lets you **fit** ~200B NVFP4 / large contexts; does **not** make weights feed the cores faster. |
| **Thermals** | Early adopters reported **throttling**, loud fans, chassis heat under sustained load. |
| **Software maturity** | **SM12.1 (GB10)** lagged optimized kernels; community **vLLM / NVFP4** friction; January 2026 stack updates helped **software** more than **silicon**. |
| **Price / market** | **$3,999 → $4,699** (Feb 2026) on memory shortage; **~$4k–$5k** for hardware that loses token races to **M-series Studio** (higher bandwidth) and **Strix Halo** (lower price). Reviews describe **returns** and shelf-sitting units. |

**Bottom line:** Unified RAM answered “can I load the model?” not “will it feel fast?” **Nobody bought** is directionally fair — sales were niche dev curiosity, not a consumer or lab standard.

### Why GB10 **FP4 tensor** did not pan out (not “no models on HF”)

| Factor | What happened |
|--------|----------------|
| **Format** | **NVFP4** is NVIDIA’s **ModelOpt / vLLM** path — not mainstream **GGUF Q4** on Hugging Face. Ecosystem default is **AWQ/GPTQ/GGUF**; FP4 checkpoints are **few** (e.g. Nemotron-3-Super/Nano NVFP4, some **Qwen3.5 NVFP4** community ports). |
| **Software on SM12.1** | Stock **vLLM** / NVIDIA containers: **illegal instruction**, missing PTX (`cvt.rn.satfinite.e2m1x2.f32`), **CUDA graph** failures on **ARM64 + GB10**. Forum thread: buyer with **9 Sparks** bought **for NVFP4** — feature **broken** without community forks (`avarok/dgx-vllm`, `nologik/vllm-dgx-spark`). |
| **Die vs datacenter Blackwell** | GB10 **SM12.1** lacks full **tcgen05 / TMEM / TMA** paths datacenter kernels expect; playbooks note **dense FP4 peak** not marketed like **sparse 1 PFLOP** headline. Hardware FP4 exists; **kernels shipped for SM100**, not **memory-starved LPDDR SoC**. |
| **Physics** | Even patched NVFP4 on Spark lands **~19–42 tok/s** on big MoE — **bandwidth wall** (~273 GB/s). FP4 **shrinks weights** (fits 120B) but **decode still crawls**. |
| **Chinese FOSS** | **Qwen / DeepSeek / Yi** on HF are overwhelmingly **BF16 / GGUF / AWQ** — you were never one `modelopt_fp4` download away; **4090 + Q4_K** was already the practical path. |

**Summary:** FP4 failed on **stack maturity + wrong silicon class + LPDDR bottleneck**, with a **small NVFP4 model catalog** as a secondary issue — not because HF has no models at all.

---

## What is a *different kettle of fish* in 2026

### Tier 1 — **Actually new silicon: GB300 / DGX Station**

**[DGX Station for Windows](products/dgx-station-windows.md)** uses **GB300 Grace Blackwell Ultra**, not GB10:

| | GB10 (DGX Spark) | GB300 (DGX Station) |
|---|------------------|---------------------|
| CPU | 20-core Grace (consumer SoC) | **72-core** Grace |
| GPU | Blackwell **consumer** die (~5070 class) | **Blackwell Ultra** (datacenter-class pairing) |
| Memory | **128 GB** LPDDR5X, ~273 GB/s | Up to **748 GB coherent**, **HBM-class** bandwidth story |
| AI peak (marketing) | ~1 PFLOP FP4 | **~20 PFLOPS FP4** |
| Model narrative | ~200B fit | Up to **1T** parameters |
| Price | ~$4.7k | **~$100k+** |

This is the generational step the keynote implies for **frontier local** work. It fixes the **bandwidth + scale** complaint that killed DGX Spark — at a price almost no individual buys.

### Tier 2 — **RTX Spark / Surface (affordable interest) — caveat**

Press and teardown-minded coverage (e.g. Pokde, Memeburn) align **RTX Spark** specs with **the same GB10 class**: 20-core Grace, **6,144 CUDA**, **128 GB LPDDR5X**, NVLink-C2C, ~300 GB/s bandwidth band.

If that holds at ship:

- It is **not** new GPU silicon — it is **GB10 in Windows OEM clothes** + **Microsoft platform tuning** (WPS, MPTF, unified-memory limits, Prism, TensorRT in Windows ML).
- **2× llama.cpp / 2.6× vLLM** claims are **software** wins on the **same memory wall**.
- **Adobe/Blender rebuilds** help creators, not magic faster tokens for agents.

**Honest affordable-tier verdict:** Treat **Surface RTX Spark Dev Box** and **Laptop Ultra** as **“DGX Spark done right for Windows dev UX”** until independent benchmarks show **>273 GB/s** or a new SoC name from NVIDIA. Do **not** assume 2026 marketing erases last year’s molasses GPU without **decode tok/s** proof.

If NVIDIA ships a **revved die** (new stepping, higher TDP, faster LPDDR) under the RTX Spark brand without renaming GB10, update this doc with die ID / `nvidia-smi` arch string.

### CEO-desk ornament risk (market thesis, 2026-06)

If **Surface Laptop Ultra** or **Surface RTX Spark Dev Box** ship on **GB10-equivalent** silicon (same ~273–300 GB/s LPDDR band, ~5070-class throughput):

- Expect **volume in the low hundreds** globally — bought as **executive desk sculpture**, IT trophy, or one-off eval units, not as working dev fleet.
- Moving **DGX Spark 2025** to **Windows + OpenShell** does **not** fix a **slow GPU**; it only changes the installer and Intune story. **Jensen’s Windows pivot does not repeal memory bandwidth.**
- **Surface RTX Spark Dev Box “100 W thermal envelope”** is a **negative signal**: it caps sustained GPU power in a chassis that already markets **1 PFLOP** headlines. Long fine-tune or agent runs will **throttle** like DGX Spark unless the die is genuinely faster per watt *and* the envelope is mislabeled (burst vs sustained). Compare: discrete dev boxes often **200–350 W** GPU alone; **100 W total package** is ultrabook territory, not “desk supercomputer.”

**Pass criteria before any fleet or personal buy:** public **SoC name ≠ GB10**, **`nvidia-smi` bandwidth** well above ~300 GB/s *or* measured **decode tok/s** beating a **4090** on your target model at same quant — not another FP4 slide.

---

## Plausible vs disclosed: did NVIDIA improve the GPU in ~2 years?

**Engineering logic (agree):** Project Digits was teased **CES 2025**; RTX Spark / Surface ship **fall 2026** — **~18–24 months** of silicon iteration is normal. A straight **GB10 re-export** at the same **~273–300 GB/s** would be commercial suicide after DGX Spark’s reputation. A serious second attempt needs roughly **~10× sustained decode** (or equivalent bandwidth/compute) vs GB10 field results — not **10× FP4 sparse peaks** on a slide.

**What “10× sustained” would mean in practice (order-of-magnitude):**

| Metric | GB10 / DGX Spark (observed band) | ~10× bar |
|--------|----------------------------------|----------|
| Memory bandwidth | ~273–300 GB/s LPDDR5X | **~2.5–3 TB/s** (HBM-class) *or* die + clocks that deliver **~350–400+ tok/s** on same quant/model reviewers used |
| Sustained GPU power (desktop) | Throttled box; ~100 W marketing on Surface Dev Box | **150–250 W+** GPU-sustained class for serious local training |
| SoC branding | GB10, N1X | Public name like **GB20** / new **Spark die** — not cosmetic **RTX** prefix only |

**Public disclosure as of Computex (conflicts with “must be new GPU”):**

- Multiple outlets (**The Register**, **ServeTheHome**, **Pokde**, **Wccftech**) map **RTX Spark = GB10 / codename N1X**, same **6,144 CUDA**, **128 GB LPDDR5X**.
- **Wccftech** adds a lighter **N1** SKU (“lighter configuration”) — could mean **fused-off cores**, not faster silicon.
- **NVIDIA newsroom** does **not** announce a new consumer die name — still **20-core Grace + Blackwell RTX 6144 CUDA**.
- **Roadmap slide (VideoCardz / Overcentral):** **Gen-1 Spark 2026** = **Grace + Blackwell + LPDDR5X**; **Gen-2 ~2028** = **Vera Rubin Spark + LPDDR6**; **Gen-3 ~2030** = **Rosa Feynman Spark**. The big generational jump may be **post-2026**, not fall launch.
- **GB300** is **DGX Station** tier (often mis-heard as “GB30”); **~20× PFLOPS marketing vs GB10** but **not** the Surface/RTX Spark price band.
- **GB100** in industry parlance is **datacenter Blackwell**, not a Windows SoC.

**Reconciliation (both can be true):**

1. **Marketing pass (likely):** Same GB10 silicon, Windows stack, OEM chassis — matches “Jensen thinks Windows saves it” cynicism.
2. **Silent silicon pass (possible, unproven):** New stepping, faster LPDDR bin, higher TDP in **desktop-only** Dev Box — might yield **&lt;2×**, not **10×**, without HBM.
3. **User is right to demand proof:** Fall 2026 ship is late enough that **NVIDIA could** ship improved die but **has not shown it**. Treat **10× sustained** as the **buy bar**, not as announced fact.

**Naming guess (GB100 / GB30):** Do not plan purchases around rumoured names. Watch **`nvidia-smi`**, **PCI/device ID**, **memory bandwidth readout**, and **Surface/NVIDIA whitepapers** at launch.

### Tier 3 — **What still wins today (fleet reality)**

For **fast** local inference on models that **fit in 24–32 GB VRAM**, a **discrete RTX 4090/5090 tower** remains the rational default. Unified 128 GB on GB10 does not beat **GDDR bandwidth** for chat decode.

**Fleet pattern (validated):** **RTX 4090 workstation + RustDesk (or similar) remote-in** — full CUDA throughput at desk, access from laptop/iPad anywhere. Beats **$4k+ GB10** boxes that are **far too expensive for the sustained GPU you actually get**. NVIDIA’s Spark push is free marketing for “keep the 4090.”

**Used 4090 market (2026):** Prices stay **stubborn** (~**$2.1k–$2.4k** US used vs **~$1.6k** launch MSRP) because **local LLM devs do not sell** — same sit as you: card runs until **~2030**, 24 GB is still the practical single-GPU tier, **5090** scarce/overpriced, Spark/GB10 does not tempt upgrades. **Nobody lists; you wouldn’t either.** Supply is “inheritance / upgrade to 5090 when forced,” not a healthy secondary market.

---

## Decision matrix (updated)

| Goal | Buy / wait |
|------|------------|
| Fast daily agents, 7B–70B quant, MCP fleet | **Keep discrete GPU box**; cloud burst for frontier |
| Must run 120B+ local, tolerate slow decode | GB10 class **only if** priced &lt; emotional “supercomputer” tax |
| Windows-native agent dev, minimal setup | **Surface Dev Box** when priced — value is **image + OpenShell**, not guaranteed new die |
| Frontier local, grant money | **DGX Station GB300** — real silicon step |
| Repeat DGX Spark mistake | Paying **$4k+** for **FP4 FLOP headlines** without **bandwidth benchmarks** |

---

## Quotes to remember (review synthesis)

- *“The DGX Spark is a capacity play, not a throughput play.”* — field reviews, 2026.
- *“Memory bandwidth is still 273 GB/s. This is a physics problem, not a software problem.”*
- Backend.ai GB10 analysis: die area favors **FP4 / tcgen05** tradeoffs that **do not help** when **LPDDR is already the bottleneck**.

---

## Doc links

- [COMPUTEX_2026_ASSESSMENT.md](COMPUTEX_2026_ASSESSMENT.md)
- [products/rtx-spark-platform.md](products/rtx-spark-platform.md)
- [products/surface-rtx-spark-dev-box.md](products/surface-rtx-spark-dev-box.md)
