# OmniMCP Inspiration

**Source:** https://github.com/Travor278/OmniMCP
**Analyzed:** 2026-07-15
**Status:** Reference / inspiration

## What It Is

A monorepo-structured MCP workspace with 8 registered services in a single `.vscode/mcp.json` — a "multimodal engineering automation framework." The custom server (`omni_mcp.py`) is a 1757-line single file with 54 tools across 15 modules (Office, PDF, Image, FFmpeg, Blender, FreeCAD, Godot, GIMP, Inkscape, MATLAB, SVG, Chart, Utils). All tools use `@mcp.tool()` with JSON-string parameters and stdio transport.

## Key Takeaway: The Unified mcp.json Pattern

The most valuable idea is not the 54-tool monolith (that's an anti-pattern we already avoid), but the **workspace-level MCP config** that wires together a suite of specialized servers:

```json
{
  "servers": {
    "playwright":    { "command": "npx @playwright/mcp@latest" },
    "github":        { "type": "http", "url": "https://api.githubcopilot.com/mcp/" },
    "blender-mcp":   { "command": "uvx blender-mcp" },
    "freecad-mcp":   { "command": "uvx freecad-mcp" },
    "godot-mcp":     { "command": "npx @satelliteoflove/godot-mcp" },
    "matlab":        { "command": "D:\\MCP\\matlab-mcp-core-server.exe" },
    "scrapling":     { "command": "uvx --from scrapling[ai] scrapling mcp" },
    "arxiv":         { "command": "uvx arxiv-mcp-server" },
    "omni-mcp":      { "command": "python d:\\MCP\\omni_mcp.py" }
  }
}
```

Each server is independently maintained, launched on demand via stdio, and provides a focused domain surface. The IDE (VS Code Copilot) dispatches to the right tool via MCP protocol.

## What We Can Use

| Aspect | Apply To |
|--------|----------|
| **Unified workspace config** | Our `opencode.json` `mcpServers` — we have 90+ repos each with a standalone server. A "fleet workspace" config that loads a curated subset (arxiv, email, plex, gitops, winops, fileops, etc.) would let the agent serve the user's current task from any repo without manual config |
| **External MCP composition** | The pattern of composing third-party MCP services (playwright, scrapling, matlab) alongside custom ones — we do this ad-hoc but should standardise |
| **`_find()` executable discovery** | The glob-based `_find()` helper scanning known install dirs — useful for our host-software MCPs (blender, freecad, gimp, godot) |
| **`img_process` pipeline** | 15+ operation image processing chain — worth extracting to a dedicated image-mcp or folding into fileops |
| **`chart_create`/`chart_subplot`** | 13 chart types via matplotlib with CJK font auto-detect — candidate for a lightweight charts-mcp |
| **PDF toolchain** | reportlab + PyMuPDF (create, merge, split, watermark, to-images) — fills a gap in our fleet |
| **Office tools** | python-pptx/python-docx/openpyxl wrappers — useful for report generation |

## What To Avoid

| Pitfall | Our Standard |
|---------|-------------|
| Single-file 54-tool monolithic server | Modular `src/{package}/tools/` with portmanteau pattern |
| JSON-string parameters (no typed schema) | Pydantic models + `Annotated[T, Field()]` |
| `shell=True` for FFmpeg | `subprocess.run` with arg list |
| Bare `except: pass` blocks | Logged exceptions via `_error_response` |
| No tests (only output artifacts) | pytest + Playwright E2E |
| Hardcoded Windows paths | Config/env resolution |

## Relationship to Existing Fleet Patterns

- **Multi-Server Orchestration Pattern** (`patterns/MULTI_SERVER_ORCHESTRATION.md`) — OmniMCP is a concrete instance of this abstract pattern
- **Turborepo MCP Monorepo Pattern** (`patterns/TURBOREPO_MCP_MONOREPO_PATTERN.md`) — different approach (Turborepo JS/TS vs OmniMCP's flat Python + `mcp.json` orchestration)
- Our fleet has the *servers* but not the *workspace-level config* that loads them as a suite
