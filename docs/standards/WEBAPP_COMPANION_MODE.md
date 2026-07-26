# Webapp Companion Mode Standard (SOTA 2026)

**Established**: 2026-07-14
**Reference impl**: `gimp-mcp` — `webapp/frontend/src/store.ts`, `Navbar.tsx`, `AppLayout.tsx`

## Problem

MCP webapps run **alongside** a host creative application (Blender, GIMP, Inkscape, FreeCAD, DaVinci Resolve, etc.). Both compete for the same screen. A full-width webapp dashboard with sidebar, glassmorphism decor, and large cards is unusable when docked beside a 3D viewport or timeline.

The user needs the webapp to **get out of the way**:
- Sit in a compact panel on a second monitor
- Collapse to a narrow companion strip beside the host app
- Minimize to a floating control bar when not in active use

## Solution: Three Modes

Every creative-webapp MCP repo SHOULD implement these three webapp modes:

| Mode | When | Layout |
|------|------|--------|
| **Full** | Primary interaction | Full sidebar, wide content, decorative glassmorphism |
| **Companion** | Side-by-side with host app | Dropdown nav (no sidebar), max-width constrained content, no decor |
| **Pop-out** | Second monitor | Separate browser window ~480×720, compact mode active by default |

---

## Implementation

### 1. Zustand Store: `compactMode` + `popOutWindow`

Add to the existing Zustand store:

```typescript
interface AppState {
  // ... existing state
  compactMode: boolean;
  popOutWindow: Window | null;
  toggleCompactMode: () => void;
  setPopOutWindow: (w: Window | null) => void;
}
```

Initialise from `localStorage` so the preference survives page reload:

```typescript
compactMode: localStorage.getItem("{repo}-compact") === "true",
```

Toggle persists:

```typescript
toggleCompactMode: () =>
  set((s) => {
    const next = !s.compactMode;
    localStorage.setItem("{repo}-compact", String(next));
    return { compactMode: next };
  }),
```

### 2. Navbar: Mode controls

Add two buttons to the top-right of the navbar:

```
[Pop Out] [Compact Toggle] [Help]
```

**Compact toggle** button toggles `compactMode`:

```tsx
<button onClick={toggleCompactMode} title={compactMode ? "Full mode" : "Companion mode"}>
  {compactMode ? <Maximize2 /> : <Minimize2 />}
</button>
```

**Pop Out** opens a new window:

```tsx
const handlePopOut = () => {
  window.open(
    window.location.href,
    "{repo}",
    "width=480,height=720,menubar=no,toolbar=no,location=no"
  );
};
```

**Amber top-border indicator** in compact mode:

```tsx
<nav className={`h-12 ... ${compactMode ? "border-t-2 border-t-amber-500/30" : ""}`}>
```

### 3. Navbar: Dropdown navigation (compact mode only)

When `compactMode` is true, replace the sidebar with a dropdown menu:

```tsx
{compactMode ? (
  <div className="relative">
    <button onClick={() => setNavOpen(!navOpen)} className="...">
      <Menu className="w-3.5 h-3.5" />
      <span>{currentPageLabel}</span>
      <ChevronDown className="w-3 h-3" />
    </button>
    {navOpen && (
      <>
        <div className="fixed inset-0 z-10" onClick={() => setNavOpen(false)} />
        <div className="absolute top-full left-0 mt-1 w-44 ... z-20">
          {pages.map(({ id, label }) => (
            <button key={id} onClick={() => { setCurrentPage(id); setNavOpen(false); }}>
              {label}
            </button>
          ))}
        </div>
      </>
    )}
  </div>
) : (
  <h1 className="text-sm font-semibold">{currentPageLabel}</h1>
)}
```

### 4. AppLayout: Conditional rendering

The layout component renders differently based on mode:

```tsx
export function AppLayout({ children }: AppLayoutProps) {
  const compactMode = useStore((s) => s.compactMode);

  if (compactMode) {
    return (
      <div className="flex h-screen bg-background">
        <div className="flex-1 flex flex-col min-w-0">
          <Navbar />
          <main className="flex-1 overflow-y-auto p-3">
            <div className="max-w-2xl mx-auto">{children}</div>
          </main>
        </div>
      </div>
    );
  }

  // Full mode: sidebar + decorative elements
  return (
    <div className="flex h-screen bg-background">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="animate-in fade-in ...">{children}</div>
          {/* decorative blur elements */}
        </main>
      </div>
    </div>
  );
}
```

Key differences in compact mode:
| Aspect | Full | Companion |
|--------|------|-----------|
| Sidebar | Visible (w-48+) | Hidden, replaced by dropdown |
| Content max-width | Full width | `max-w-2xl` (~672px) |
| Padding | `p-6` | `p-3` |
| Glassmorphism decor | Present | Removed |
| Top bar indicator | None | Amber border (`border-t-amber-500/30`) |
| Status labels | Visible ("healthy", "Live Bridge") | Dot only |

---

## Reference Implementation

See `gimp-mcp` for the complete working implementation:

| File | What |
|------|------|
| `webapp/frontend/src/store.ts` | State: `compactMode`, `popOutWindow`, `toggleCompactMode` |
| `webapp/frontend/src/components/Navbar.tsx` | Compact dropdown nav, pop-out button, toggle button |
| `webapp/frontend/src/components/AppLayout.tsx` | Conditional layout rendering |

## Porting to Other Repos

For each creative repo (blender-mcp, inkscape-mcp, freecad-mcp, qcad-mcp, daVinci-resolve-mcp):

1. Copy the `compactMode` state + `toggleCompactMode` action to the Zustand store
2. Add the two mode-toggle buttons + pop-out button to the topbar/navbar
3. Add the dropdown nav in the navbar (render conditionally on `compactMode`)
4. Make `AppLayout` render differently based on `compactMode`

**Estimated effort**: 30 minutes per repo (3 files to modify: store, navbar, layout).

## Example: Blender Sidebar

Blender users often have a vertical workspace (viewport top, timeline bottom, properties right). The companion webapp can sit in a narrow strip:

```
┌──────────────────────────────────────────────┐
│  Blender 3D Viewport                          │
│                                                │
│                                                │
├──────────────────────┬───────────────────────┤
│  Timeline / Dope Sheet │  Webapp Companion    │
│                        │  (pop-out, compact)  │
└──────────────────────┴───────────────────────┘
```
