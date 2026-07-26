# BUG-007: Ctrl+Scroll Zoom Broken in Dev Browser

## Severity
**P2** — Medium (UI Malformation)

## Repos Affected (14)
aiwatcher-mcp, blender-mcp, calibre-mcp, chip-design-mcp, filesystem-mcp, godot-mcp, kicad-mcp, plex-mcp, pywinauto-mcp, qcad-mcp, teleoperator-mcp, vla-mcp, worldlabs-mcp, yahboom-mcp

## Symptom
Ctrl+scroll wheel does nothing in dev browser (Vite). The zoom levels [0.8, 1.0, 1.25, 1.5, 2.0, 3.0] are never applied.

## Root Cause
Every repo's `useZoom` hook follows this pattern:
1. `e.preventDefault()` kills the browser's native Ctrl+scroll zoom
2. Calls `@tauri-apps/api/window` `setZoom()` which is a Tauri WebView API
3. In dev browser, `import("@tauri-apps/api/window")` fails (not a Tauri context)
4. The `catch` block is empty — no fallback applied
5. Result: native zoom is prevented AND the Tauri zoom fails → nothing happens

## Resolution
Replace the empty catch block with a CSS `transform: scale()` fallback:

```ts
} catch {
  const root = document.documentElement;
  root.style.transform = `scale(${level})`;
  root.style.transformOrigin = "top left";
  root.style.width = `${100 / level}%`;
  root.style.height = `${100 / level}%`;
}
```

## SOTA Impact
- Added to `TAURI_PRODUCTION_PITFALLS.md` dev-vs-production mismatches table
- All 14 repos fixed in BUG-007 sweep
