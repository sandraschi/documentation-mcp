# World Labs MCP Integration

The **World Labs MCP** server provides an industrial-grade gateway to the [World Labs Marble API](https://docs.worldlabs.ai/api), enabling high-fidelity 3D world generation and exploration.

## Overview

World Labs focuses on **Spatial Intelligence**, generating 3D Gaussian Splats and meshes that are persistent and navigable. This integration enables the agentic fleet to "ground" its reasoning within physical 3D spaces.

## SOTA Features (2026)

### 1. Spark 2.0 Renderer
The integration utilizes the **Spark 2.0 WebGL2/Rust** engine for progressive LoD (Level-of-Detail) exploration. It supports datasets exceeding **100 Million splats**, providing production-quality visuals directly in the browser.

### 2. Spatial Voice Agent
Grounds AI narration in 3D space.
- **Engine**: Gemini 3.1 Pro Flash TTS.
- **Audio Output**: 6-DOF Spatial Audio (HRTF) tracking player position.
- **Tooling**: `broadcast_spatial_notification` enables agents to "stand" at specific coordinates and speak to the user.

### 3. Progressive LoD (.RAD) support
Native support for the **.RAD** chunked streaming format, ensuring massive environments load instantly on Desktop, Mobile, and WebXR.

## Fleet Tools

| Tool | Capability |
|------|------------|
| `generate_world_from_text` | Text prompt to explorable 3D Splat/Mesh. |
| `broadcast_spatial_notification` | Localize voice at `[x, y, z]` coordinates. |
| `upload_and_generate` | Lift local media into 3D. |
| `list_worlds` | Fleet-wide generation history audit. |

## Implementation Note

The server includes a **Sovereign Asset Bridge** (Port 10865), allowing for local file serving of high-res assets to bypass cloud latency and additional generation costs.

## Fleet game product

**[Marble Adventure](../docs/games/MARBLE_ADVENTURE.md)** — competition Godot hub that opens MCP-generated Marble worlds in the browser. Ship via `worldlabs-mcp/competition/ship-itch.ps1` (not godot-mcp `upload_dir` validation). itch: [sandraschi.itch.io/marble-adventure](https://sandraschi.itch.io/marble-adventure) (draft).

---
*Maintained by the Industrial Fleet Registry.*
