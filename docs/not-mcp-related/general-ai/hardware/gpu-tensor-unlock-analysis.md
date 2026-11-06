# GPU Tensor Core Unlock (gpu-unlock) Analysis: RTX 4090 & FP8/Diffusion

**Status:** Reference & Decision Record (Evaluated & Deprioritized / Ignored)  
**Date:** 2026-11-04  
**Context:** Goliath server (NVIDIA GeForce RTX 4090 24GB, capped at 300W)  
**Related:** `gpu-power-limiting.md`, `COMPUTE_LIMITS_SINGLE_GPU.md`  

---

## 1. What is `gpu-unlock`?

Community projects (`zagitta/gpu-unlock` for Ampere, and forks like `gpu-unlock-ada` / `AD103_win_unlocker` for Ada Lovelace / RTX 4090) target NVIDIA's artificial firmware segmentation on consumer GeForce cards.

* **NVIDIA's Artificial Limiter:** On consumer GeForce silicon, matrix math instructions executing **FP16, BF16, or TF32 with FP32 accumulation** are locked in early firmware to **half issue rate** compared to professional/workstation counterparts (e.g., RTX 6000 Ada, A100, H100).
* **The Exploit:** An early-boot kernel module (Linux initramfs) or UEFI pre-boot payload writes to SM speed-select registers (`FULL_SPEED`) before the proprietary NVIDIA driver binds.
* **Peak Metric Gain:** Doubles theoretical FP16/BF16 tensor throughput on an RTX 4090 from ~165 TFLOPS to ~330 TFLOPS.

---

## 2. Why It Is Irrelevant for FP8 & Sub-FP8 LLM Workloads

1. **FP8 is Unthrottled by Default:**
   * NVIDIA's artificial rate cap specifically targets tensor operations with **FP32 accumulation** (FP16/BF16/TF32 $\rightarrow$ FP32).
   * Ada Lovelace (AD102) native **FP8 tensor operations are NOT rate-limited**. Benchmarks on `gpu-unlock-ada` show ~0% change in FP8 GEMM throughput ($\pm0.3\%$).

2. **Quantized LLM Inference is Memory-Bound, Not Compute-Bound:**
   * Token generation using **FP8, INT8, INT4, AWQ, or EXL2/GGUF** is bottlenecked by the 4090's memory bandwidth (~1,008 GB/s), not tensor compute.
   * Doubling theoretical compute TFLOPS yields 0% faster token generation because the tensor cores are constantly stalled waiting for weights to arrive from VRAM.

---

## 3. What About Modern Diffusion Models (FLUX.2, FLUX.3, SDXL)?

At first glance, image diffusion appears to be a compute-heavy GEMM workload where FP16/BF16 unlock could help. However, on a 24GB RTX 4090:

1. **Modern Diffusion Architectures are Native FP8 / Quantized:**
   * Modern generations (**FLUX.2**, **FLUX.3** / Klein) and contemporary rectified flow transformers were designed with FP8 and low-bit quantization as first-class citizens.
   * Full unquantized BF16 checkpoints easily exceed 24GB VRAM (or leave zero headroom for activations/latents), forcing heavy CPU offload where PCIe transfers become the bottleneck.
2. **Zero Speedup on Native FP8:**
   * On 24GB consumer cards, community and production deployments run in **FP8** (or GGUF/NF4) to fit in VRAM and maximize inference speed.
   * Because Ada's FP8 tensor core pipeline is already unthrottled, `gpu-unlock` yields **zero speedup** for native FP8 FLUX pipelines.
3. **Smaller Legacy Models in FP16 (SDXL / SD 1.5):**
   * While SDXL fits in 24GB in pure FP16 and could theoretically see faster raw GEMMs, modern attention kernels (FlashAttention, SageAttention, xFormers) already eliminate most compute bottlenecks.

---

## 4. Risks & Operational Cost

1. **Host Instability & Boot Complexity:**
   * Requires injecting early boot hooks or UEFI firmware payloads before Windows driver verification.
   * Breaks or triggers BSODs / black screens upon Windows driver updates or Secure Boot checks.
2. **Thermal & Power Budget:**
   * Our 4090 is power-capped at 300W (`gpu-power-limiting.md`) to maintain quiet, low-heat operation in the Goliath chassis.
   * Unlocking full-rate FP16 GEMMs increases SM power draw and would immediately collide with power/thermal ceilings.

---

## 5. Decision

**IGNORE / DO NOT IMPLEMENT.**
* All primary LLM workloads run in **FP8, AWQ, or GGUF**, which are either memory-bandwidth bound or already run unthrottled.
* Flux.1 on 24GB VRAM requires **FP8 / GGUF** to fit in VRAM, which does not benefit from the unlock.
* The maintenance risk on a production Windows host far outweighs any isolated gains for unquantized SDXL diffusion.
