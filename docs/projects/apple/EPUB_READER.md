# CalFolio -- EPUB reader strategy

**Private -- Sandra S. + collaborators only. Not for public distribution.**

**Status**: DECISION RECORD
**Date**: 2026-05-29 (reaffirmed 2026-10-28)
**Parent**: [CALFOLIO.md](./CALFOLIO.md)

---

## Summary

| Approach | v1 | Long term |
|----------|----|-----------|
| **Hand off** (Open in Books / KyBook / Marvin) | GO - Ship first | Keep as escape hatch |
| **Readium Swift Toolkit** (SPM) | PoC in alpha | Primary in-app reader |
| **FolioReaderKit** | NO - Do not use | Unmaintained (~2019) |
| **epub.js in WKWebView** | NO - Avoid | More glue than Readium |

**Engine rule:** Do not implement custom EPUB parsing/rendering. Use Readium or hand off.

---

## Where iOS devs get this

| Source | Use |
|--------|-----|
| **GitHub + Swift Package Manager** | Add dependency: `https://github.com/readium/swift-toolkit.git` |
| **Readium TestApp** | Reference UI integration (`swift-toolkit/TestApp`) |
| **Readium guides** | [Getting Started](https://github.com/readium/swift-toolkit/blob/develop/docs/Guides/Getting%20Started.md), [Navigator](https://github.com/readium/swift-toolkit/blob/develop/docs/Guides/Navigator/Navigator.md) |
| **readium.org** | Ecosystem index -- [awesome-readium](https://readium.org/awesome-readium/) |
| Apple docs / WWDC | SwiftUI, file sandbox, `WKWebView` policy -- not EPUB layout |

There is no separate "EPUB App Store" for components. Libraries live on GitHub; apps own the shell.

---

## Recommended stack: Readium 3.x

Pin a released tag contemporary with your Xcode at integration time (3.8.x line as of May 2026 -- verify latest before adding the package).

| Module | Role |
|--------|------|
| `ReadiumShared` | `Publication`, `Locator`, shared models |
| `ReadiumStreamer` | Parse `.epub` -> `Publication` |
| `ReadiumNavigator` | `EPUBNavigatorViewController` -- reading surface |

**License:** BSD-3 -- fine for App Store apps; hundreds of production readers use it.

**Readium does not ship a product UI.** The navigator renders publication content only. CalFolio provides:

- Toolbars, TOC sheet, settings (font, theme)
- Progress bar / "time left" (optional)
- Integration with library browse (SwiftUI shell)

**Reference implementation:** clone [readium/swift-toolkit](https://github.com/readium/swift-toolkit), build **TestApp** (EPUB 2/3 reflow + fixed layout, night/sepia, custom fonts). Copy *patterns*, not the app wholesale.

**Minimal flow** (see also [discussion #266](https://github.com/readium/swift-toolkit/discussions/266)):

1. `PublicationOpener` opens local EPUB file -> `Publication`
2. Publication served via Readium's **local HTTP server** (required for EPUB web content)
3. Present `EPUBNavigatorViewController` (UIKit) -- wrap in `UIViewControllerRepresentable` for SwiftUI
4. Implement `navigator(_:locationDidChange:)` -> persist `Locator` for Calibre sync

---

## What not to copy

| Project | Why skip |
|---------|----------|
| **FolioReaderKit** | Last meaningful maintenance ~2019; old Swift/Xcode assumptions |
| **Raw epub.js** | Possible in `WKWebView` but worse accessibility/App Store polish vs Readium's native path |
| **Apple Books as embedded reader** | No API to inject arbitrary EPUBs into Books programmatically -- hand-off only |

---

## Phased rollout (aligned with CALFOLIO phases)

| Phase | Reader deliverable |
|-------|-------------------|
| **1 -- PoC** | Download EPUB from calibreops; **Open in...** share sheet; optional "last opened" in app only |
| **2 -- Alpha** | Readium: open EPUB in-app; TOC; theme (day/sepia/night); save `Locator` locally |
| **3 -- Beta** | Sync `Locator` to Calibre (custom column / comment); highlights via Readium **Decoration API** |
| **4+** | Fleet TTS ("Listen") via speechops -- complements Readium TTS, not a replacement in v1 |

Do **not** block PoC on in-app reader. Browse + Tailscale + hand-off validates the product.

---

## MOBI and other formats

Readium is **EPUB- and PDF-centric**. For Calibre libraries with MOBI:

- Prefer delivering **EPUB** from calibreops when both exist
- Or convert on the fleet before download (Calibre conversion)

Do not promise in-app MOBI in v1 unless server-side conversion is implemented.

---

## Doing it well (quality bar)

| Concern | Approach |
|---------|----------|
| **Progress sync** | Serialize Readium `Locator` (JSON) -> calibreops -> Calibre custom column e.g. `#calibrefolio:last_locator` |
| **Offline** | EPUB under `Application Support`; metadata in SwiftData |
| **Typography** | Readium user settings + limited theme set (match TestApp) |
| **Fixed-layout EPUB** | Test early (comics, picture books) -- Readium supports FXL |
| **Apple Pencil** | Highlights via Decoration API first; freehand annotations later |
| **Large files** | Stream via Readium; avoid loading entire book into memory |
| **LCP / store DRM** | Out of scope for personal Calibre libraries in v1 |

---

## Hand-off implementation (v1)

1. `manage_files` (calibreops) downloads EPUB to app sandbox
2. Present `UIActivityViewController` / document export / **Open in...**
3. User reads in Apple Books, KyBook, Marvin, etc.
4. Optional: deep link back to CalFolio book detail when user returns

CalFolio still wins on: library UX, series, RAG, fleet features -- not on being the only renderer.

---

## SwiftUI integration sketch

```
Library (SwiftUI)
  +-- BookDetail
        +-- ReaderView (UIViewControllerRepresentable)
              +-- EPUBNavigatorViewController + chrome overlay
```

- Tap reader surface -> toggle chrome (Readium `VisualNavigatorDelegate.didTap`)
- Sidebar + detail columns unchanged on large iPad; reader full-screen or third column

---

## Mac day-one checklist

1. Xcode -> **File -> Add Package** -> `https://github.com/readium/swift-toolkit.git`
2. Clone repo; open **TestApp**; run on iPad simulator with a sample EPUB
3. Find `locationDidChange` / last-location restore in TestApp
4. Scaffold `ReaderView` wrapper in `calfolio` repo (empty chrome OK)

---

## Related

- [CALFOLIO.md](./CALFOLIO.md) -- product scope
- [IOS_PUBLISHING.md](./IOS_PUBLISHING.md) -- repo scaffold on Mac
- [calibre-mcp](../calibre-mcp/) -- backend; confirm HTTP bridge paths for file download
- [translate-mcp](../translate-mcp/TRANSLATE_MCP.md) -- spoken translation (post-reader)

---
*Last updated: 2026-10-28 (ASCII cleanup, Readium pin reaffirmed). Decision record from 2026-05-29.*
