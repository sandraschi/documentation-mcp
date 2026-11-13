# Craft Showcase

**Version**: v0.1.0 (2026-11-10) — In-browser WebAssembly studio, client landing page, dynamic ROI calculator, and video pitch storyboard for the Sovereign Back-Office Suite.

## Ports

| Port | Service |
|------|---------|
| 11270 | Web Showcase & In-Browser WASM Studio (`web/`) |

## Architecture

```
crates/craft-showcase-wasm (egui / eframe 0.37 -> wasm32)
                          │ (compiled via trunk)
                          ▼
            web/wasm/ (HTML5 Canvas via WebGL2/WebGPU)
                          ▲
                          │ embedded in <iframe>
            web/index.html (Client Landing Page, ROI Calculator, Video Storyboard)
```

## Quick Start

```powershell
# Smoke check
mcp-central-docs\starts\craft-showcase-start.bat --smoke

# Launch local preview server on port 11270
mcp-central-docs\starts\craft-showcase-start.bat
```

## Status

- **v0.1.0** — Shipped. Pure Rust WebAssembly in-browser studio, dynamic ROI calculator, interactive domino flow, video pitch script.

## Links

- **Repository**: [craft-showcase](file:///D:/Dev/repos/craft-showcase)
- **Spoke Assessment**: [craft-showcase.md](../craft-fleet/craft-showcase.md)
