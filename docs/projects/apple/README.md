# Fleet-connected iPad apps

**Status**: Active ideation + **CalFolio** pre-scaffold (2026-05-29)  
**Backend pattern**: iPad ÔåÆ Tailscale ÔåÆ fleet FastAPI bridge (calibreops, arxiv-mcp, ÔÇª)

This folder is the **project home** for new fleet-connected iOS/iPad apps. Generic Apple workflow (Xcode agentic IDE, StoreKit, hardware) stays in [`../../apple/`](../../apple/).

---

## Start here

| Project | Doc | Status |
|---------|-----|--------|
| **CalFolio** (Calibre library on iPad) | [CALFOLIO.md](./CALFOLIO.md) | CONCEPT / PRE-SCAFFOLD ÔÇö **first Apple dev, Mac start** |
| EPUB reader (Readium vs hand-off) | [EPUB_READER.md](./EPUB_READER.md) | Decision record |
| Scaffolding, TestFlight, Apple Developer | [IOS_PUBLISHING.md](./IOS_PUBLISHING.md) | Planning |
| Full idea backlog (20 apps; #1 = CalFolio) | [IOS_PROJECT_IDEAS.md](./IOS_PROJECT_IDEAS.md) | Ideation |

**Backend**: [calibre-mcp / calibreops](https://github.com/sandraschi/calibremcp) ÔÇö fleet port **10750** (verify in repo `WEBAPP_PORTS` / `start.ps1` before wiring the app).

---

## Two Apple doc trees (do not confuse)

| Path | Use for |
|------|---------|
| **`projects/apple/`** (this folder) | CalFolio + fleet-iPad product specs |
| **`apple/`** | Agentic Xcode 26, VRMDance, Boomy Commander, App Store guides |

Cross-links from the legacy portfolio index: [apple/projects/README.md](../../apple/projects/README.md).

---

## Related

- [translate-mcp](../translate-mcp/TRANSLATE_MCP.md) ÔÇö spoken translation for CalFolio ÔÇ£listen in any languageÔÇØ
- [calibre-mcp](../calibre-mcp/) ÔÇö MCP project docs (backend for CalFolio)
- [FLEET_INDEX.md](../FLEET_INDEX.md) ÔÇö add `calfolio` when GitHub repo exists

---
*Last updated: 2026-05-29*
