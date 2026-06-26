---
title: "MCP Mesh Architecture - Capability Matrix"
category: reference
status: active
audience: mcp-dev
skill_candidate: false
related:
  - architecture/AGENTIC_MESH_ARCHITECTURE.md
  - operations/WEBAPP_PORTS.md
last_updated: 2026-02-01
---

# MCP Mesh Architecture: Capability Matrix

This document provides a comprehensive overview of the integration facilities (Import, Export, Edit) and network topography for the 3D/VR/Multimedia MCP ecosystem.

## Integration Mesh

| MCP Server | Domain | Primary Import | Primary Export | Edit Facilities | Dashboard |
|------------|--------|----------------|----------------|-----------------|-----------|
| **WorldLabs** | AI Gen | Text/Img/Video | SPZ, GLB | Local LLM Refinement | [10864](http://localhost:10864) |
| **Resonite** | VR Script | GLB, SPZ, Media | Snapshots, Logs | ProtoFlux, Component Props | [10714](http://localhost:10714) |
| **Unity3D** | Build/Rig | VRM, Assets | Packages, Builds | Scene/Component Config | [10830](http://localhost:10830) |
| **Blender** | Mod/Anim | GLB, FBX, OBJ | GLB, FBX, VRM | AI-Assisted Modeling | [10848](http://localhost:10848) |
| **Avatar** | Manage | VRM 2.0 | VRM 2.0, Screens | Bone Rot, Morphs, Anim | [10792](http://localhost:10792) |
| **OSC** | Transport | OSC Messages | OSC Messages | Real-time Param Routing | [10766](http://localhost:10766) |
| **Plex** | Media | Movies/Shows | Stream, Metadata | Config, RAG Semantic Search | [10720](http://localhost:10720) |
| **Calibre** | Books | EPUB/PDF | EPUB/PDF | Metadata, RAG Semantic Search | [10730](http://localhost:10730) |
| **robofang** | Agent/RAG | System Data | AI Actions | Multi-agent Orchestration | [10750](http://localhost:10750) |

## Network Topology (SOTA 2026)

All webapps follow the **Sandra Adjacency Rule** (Frontend/Backend port adjacency).

| Project | Frontend | Backend (API) | Notes |
|---------|----------|---------------|-------|
| WorldLabs | 10864 | 10865 | Connects to 11434 (Ollama) |
| Unity3D | 10830 | 10831 | Base dashboard on 10710 |
| Resonite | 10714 | 10715 | High-speed OSC bridge |
| Blender | 10848 | 10849 | AI modeling interface |
| Avatar | 10792 | 10793 | Animation sequence recorder |
| OSC | 10766 | 10767 | Bidirectional message hub |
