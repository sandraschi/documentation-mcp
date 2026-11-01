# Fleet-connected iPad apps

**Status**: Active ideation + **CalFolio** pre-scaffold (no `calfolio` repo yet as of 2026-10-28)
**Backend pattern**: iPad -> Tailscale -> fleet FastAPI bridge (calibreops, arxiv-mcp, ...)
**Target**: Xcode 27.2, iOS/iPadOS 27 SDK (see [research hub](../../research/apple/README.md))

This folder is the **project home** for new fleet-connected iOS/iPad apps. Generic Apple workflow (Xcode agentic IDE, StoreKit, hardware) stays in [`research/apple/`](../../research/apple/README.md).

---

## Start here

| Project | Doc | Status |
|---------|-----|--------|
| **CalFolio** (Calibre library on iPad) | [CALFOLIO.md](./CALFOLIO.md) | CONCEPT / PRE-SCAFFOLD — **first Apple dev, Mac start** |
| EPUB reader (Readium vs hand-off) | [EPUB_READER.md](./EPUB_READER.md) | Decision record |
| Scaffolding, TestFlight, Apple Developer | [IOS_PUBLISHING.md](./IOS_PUBLISHING.md) | Planning |
| Full idea backlog (20 apps; #1 = CalFolio) | [IOS_PROJECT_IDEAS.md](./IOS_PROJECT_IDEAS.md) | Ideation |

**Backend**: [calibre-mcp / calibreops](https://github.com/sandraschi/calibremcp) — fleet ports **10720/10721** (backend/frontend per `operations/WEBAPP_PORTS.md`; re-check in repo `start.ps1` before wiring the app).

---

## Two Apple doc trees (do not confuse)

| Path | Use for |
|------|---------|
| **`projects/apple/`** (this folder) | CalFolio + fleet-iPad product specs |
| **`research/apple/`** | Agentic Xcode 26–27, VRMDance, Boomy Commander, App Store guides |

Cross-links from the portfolio index: [research/apple/projects/README.md](../../research/apple/projects/README.md).

---

## Related

- [translate-mcp](../translate-mcp/TRANSLATE_MCP.md) — spoken translation for CalFolio "listen in any language"
- [calibre-mcp](../calibre-mcp/) — MCP project docs (backend for CalFolio)
- [FLEET_INDEX.md](../FLEET_INDEX.md) — add `calfolio` when GitHub repo exists

---
*Last updated: 2026-10-28 (27.2 generation; port + link fixes)*
