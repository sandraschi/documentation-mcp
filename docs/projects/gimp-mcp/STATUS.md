# GIMP MCP -- Project Status

**Last Updated**: 2026-05-28
**Repo**: `D:\Dev\repos\gimp-mcp` | [GitHub](https://github.com/sandraschi/gimp-mcp)
**Version**: v4.6.0 (Agent Lab Phase 6 complete)
**Python**: 3.12+ | **Build**: Setuptools / MCPB / GHCR
**Status**: PRODUCTION READY — Agent Lab complete (Phases 1–6)

---

## What It Is

Professional image editing through Model Context Protocol (MCP) using GIMP. Agent Lab v4.6.0 adds PBR pack batch, decal UV sheets, AI refine loops, and CI fleet E2E smoke.

**Core Innovation**: Fleet texture pipelines (blender → gimp → unity) with live bridge + headless CLI dual mode.

---

## Agent Lab (Phases 1–6 complete)

| Phase | Theme |
|-------|-------|
| 1–4 | Bridge, vision, fleet handoff, telemetry/Docker |
| 5 | Sim art (Gazebo, VRChat, robotics staging) |
| 6 | PBR packs, decal sheets, Tripo/Rodin handoff, CI E2E |

---

## Architecture

Consolidates 63+ legacy operations into **8 master portmanteau tools**:
- `generate_image`: AI generation with GIMP post-processing.
- `gimp_file`: IO, conversions, and validation.
- `gimp_transform`: Resize, crop, rotate, perspective.
- `gimp_color`: Levels, curves, HSL, auto-adjustments.
- `gimp_filter`: Blur, sharpen, artistic effects.
- `gimp_layer`: Layer management and compositing.
- `gimp_analysis`: Statistics, histograms, quality assessment.
- `gimp_system`: Diagnostics, help, and performance.

---

## Current State

| Feature | Status | Notes |
|---------|--------|-------|
| AI Generation | Working | Flux-dev & nano-banana-pro support |
| Portmanteau Logic | Working | Surgical tool reduction to 8 tools |
| GIMP Integration | Working | Reliable CLI-driven automation |
| Asset Repository | Working | Intelligent search and versioning |
| MCPB Packaging | Working | SOTA 2026 compliant bundle |

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| Frontend | 10772 | Reserved |
| Backend | 10773 | Reserved |
