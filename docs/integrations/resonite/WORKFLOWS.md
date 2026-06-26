# Resonite Workflows: Spatial Orchestration

These workflows define the life-cycle of persistent virtual presence in Resonite.

## 🏛️ Workflow: "The Virtual Command Center"

Setting up a persistent hub for project monitoring.

1.  **Instantiation**: Agent triggers `spawn_object_vrm` to place the "Main Console" asset.
2.  **Telemetry Binding**: Agent uses `update_logix_node` to connect **System Admin MCP** data to in-world screens.
3.  **Security**: Agent sets the world access level to `Invite-Only`.
4.  **Sync**: The world ID is saved to the **Knowledge Management (ADN)** database.

## 🤖 Workflow: "Multi-Agent Presence Sync"

Coordinating social avatars across different platforms.

1.  **Format Prep**: Agent uses `avatar_mcp` to prepare a VRM compatible export.
2.  **Import**: Agent triggers the Resonite import sequence via the WebSocket bridge.
3.  **OSC Verification**: Agent verifies that the `/avatar/parameters` are flowing correctly from the **OSC MCP**.

---
*Last updated: 2026-02-14*
