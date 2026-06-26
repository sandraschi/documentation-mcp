# Obsidian: Technical Specifications

This document outlines the vault architecture used by the Sandra fleet.

## 📂 Vault Structure

- **Main Vault**: `D:\Dev\repos\sandras-vault` (The core technical brain).
- **Format**: Standard CommonMark with **WikiLinks** (`[[Link]]`) enabled.
- **Attachments**: Stored in a dedicated `attachments/` folder within the vault root.

## ⚙️ Plugin Standards

- **Core Plugins**: Search, Backlinks, Canvas (for visual system architectures).
- **Mandatory Community Plugins**:
  - **Dataview**: For programmatic queries of note metadata.
  - **Templater**: For standardized node creation.
  - **Local REST API**: Enables the MCP interface (Port `27124`).

## 🏗️ Internal Logic

### Semantic Tagging
The vault uses a hierarchical tagging system:
- `#project/[Name]`
- `#tech/[Subject]`
- `#status/[In-Progress|Complete|Archived]`

---
*Last updated: 2026-02-14*
