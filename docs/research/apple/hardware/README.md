# Apple hardware: Silicon and agentic workloads (March 2026)

## Shipping Silicon (March 2026)

- **M4 series**: Current mainstream (MacBook Air, MacBook Pro, iMac, iPad Pro, etc.). Neural Engine, Unified Memory, Metal/MPS acceleration.
- **M3 series**: Still in use across many Macs and iPads; capable for local LLM and RAG at moderate sizes.
- **M2 / M1**: Minimum viable for lighter agentic and local-inference workloads; check RAM and thermal limits for large models.

**M5 / M6** in this doc set are **forward-looking or project-specific** (roadmap/rumor). For real requirements, use **shipping** M-series (M1–M4) and Apple’s official specs.

## Architecture (M-series in general)

- **Unified Memory (UMA)**: CPU, GPU, and Neural Engine share memory; reduces copies and helps large models.
- **Neural Engine**: Dedicated accelerators for framework-based inference (Core ML, and later Core AI); TOPS and capabilities improve each generation.
- **Metal / MPS**: GPU compute for custom and framework-driven ML; use for local LLMs and RAG when targeting Mac.

## Sizing for agentic and local LLM workloads

| Use case | Minimum (practical) | Recommended |
|----------|----------------------|-------------|
| Light RAG + small model | M1 / 16 GB | M2 Pro / 32 GB |
| Medium local LLM (7B–13B) + RAG | M2 Pro / 32 GB | M3 Max / 64 GB |
| Large local LLM + heavy RAG (e.g. 59k chunks) | M3 Max / 64 GB | M4 Max / 128 GB |

Thermal: Fanless MacBook Airs throttle under sustained heavy inference; Pro/Max and desktops handle longer runs better.

## Power and thermal

- Prefer **Metal Performance Shaders (MPS)** and **Core ML** (and **Core AI** when available) so the system can use Neural Engine and GPU efficiently.
- Avoid unnecessary high-quantization (e.g. Q8) on low-TDP chips if you need sustained throughput.

## SOTA 2026 project conventions

- **“Vibearchitect” workstations, M5/M6, VibeCore™**: Project or speculative naming; align actual development with **shipping** hardware (M1–M4) and official Apple documentation.
- **agentic-mcp / local RAG**: Minimum M1 Pro / 16 GB; recommended M3 Max / 64 GB; “best-in-class” M5 Pro / 128 GB is **project target**, not a current product.

---
*© 2026 Materialist-Reductionist Systems • Alsergrund Technical Campus*
