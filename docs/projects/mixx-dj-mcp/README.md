# Mixx-DJ-MCP

<p align="center">
  <a href="https://github.com/sandraschi/mixx-dj-mcp"><img src="https://img.shields.io/github/stars/sandraschi/mixx-dj-mcp?style=flat-square" alt="Stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="MIT"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square" alt="Python"></a>
  <a href="https://github.com/jlowin/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.4+-purple?style=flat-square" alt="FastMCP"></a>
  <a href="https://mixxx.org/"><img src="https://img.shields.io/badge/Mixxx-2.5+-orange?style=flat-square" alt="Mixxx"></a>
</p>

FastMCP server bridging AI agents to Mixxx via OSC. Companion to [mixxxxx](https://github.com/sandraschi/mixxxxx) (video-enabled Mixxx fork).

**12 portmanteau tools, ~84 operations** — decks, library, effects, mixer, crates, stems, set planning, skin manager, vinyl catalog, controller auto-detect, DAW export, AI transitions, audio-reactive visuals.

## Ports

| Port | Service |
|------|---------|
| 11116 | Backend (FastAPI + FastMCP HTTP `/mcp`) |
| 11117 | Frontend (Vite React webapp) |
| 11118 | OSC listener (Mixxx feedback) |
| 11119 | OSC sender (commands to Mixxx) |

## Tools

| Tool | Ops | Purpose |
|------|-----|---------|
| `mixx_deck` | 19 | Deck transport + video |
| `mixx_library` | 8 | Library search/browse |
| `mixx_effects` | 7 | Effect chains |
| `mixx_mixer` | 8 | Crossfader, EQ, mixer |
| `mixx_crate` | 5 | Smart + agentic crates via Ollama |
| `mixx_stems` | 6 | Demucs stem separation |
| `mixx_set` | 3 | Set sequencing + recording |
| `mixx_skin` | 7 | Skin browser + Inkscape generator |
| `mixx_vinyl` | 5 | Vinyl catalog + gig pick |
| `mixx_controller` | 5 | USB auto-detect |
| `mixx_daw` | 8 | DAW export/visuals bridge |
| `mixx_transition` | 3 | AI-powered transitions |

## Key Features

- **Cross-MCP Cockpit** — Plex search, SFX browser, deck status, AI assistant
- **AI Transitions** — LLM picks echo/filter/stem-swap between tracks
- **Audio-Reactive Visuals** — BPM/beat phase → Resolume OSC
- **Demucs Stems** — Vocal/drums/bass separation, stem-aware crossfades
- **REST Deck Handoff** — `/api/v1/deck/{id}/{load|play_pause|sync|cue}`
- **DAW Bridge** — Export to Reaper, Fairlight, Resolume
- **Vinyl Catalog** — OCR + Ollama catalog for 3000 records
- **Controller Auto-Detect** — VID/PID database for 40+ DJ controllers
- **SOTA Webapp** — React 19 / Vite 6 / Tailwind 4 / Zustand 5 — 8 pages

## Status

- **v0.1.0** — All 12 tools shipped. Webapp, Tauri scaffold, MCPB, CI, docs.
