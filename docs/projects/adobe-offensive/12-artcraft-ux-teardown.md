# 12 - ArtCraft UX Teardown: Webapp Sidebar, Tokens, Apps Site

Date: 2026-10-11. Method: live inspection of app.getartcraft.com and
getartcraft.com/apps + /pricing + /apps/photocraft in the built-in browser at
1440x900 and 800x600, DOM and CSS read via JS, repo tree via GitHub. Everything
below was observed, not inferred, unless marked.

## 1. Stack correction: the webapp is not Rust

Common claim: "Rust webapp". Observed reality:

- Frontend: React (root mount), Vite (`/assets/index-<hash>.js`), Nx workspace
  under `frontend/` with npm + package-lock, shared libs `@storyteller/ui-*`,
  Vitest. Same family as our WEBAPP_SOTA stack (React/Vite/Tailwind), minus Bun
  and Zustand (unverified which store they use).
- Rust lives in: backend crates (`crates/`, `.sqlx`, SQL migrations), the Tauri
  desktop shell (bundles the Vite output), and WASM modules.
- Video editor (`/video-editor`) loads `opencut_wasm_bg-<hash>.wasm`: OpenCut
  (open-source CapCut alternative) engine compiled to WASM. They reused a FOSS
  editor core instead of writing one.
- Edit 3D (`/edit-3d`) is three.js with `jsm/libs/ammo.wasm.js` (Bullet physics
  port from the three.js examples tree).
- The seven Craft apps ARE pure Rust native (GPU canvas on Metal/Vulkan/DX12/
  WebGPU, no Electron, no webview). Two different products, two different stacks.
  See 13 for why that split matters for the business model.

## 2. The sidebar (the thing worth stealing)

Implementation: stock **shadcn/ui Sidebar** primitive. Evidence: `data-sidebar=
sidebar|header|trigger|content|group|group-label|group-content|menu|menu-item|
menu-button|footer` attributes, `sidebar_state` cookie for persisted collapse,
`group-data-[variant=floating]` classes, `rounded-[3px]`. Variant: floating.
Collapsible mode: icon rail.

### Information architecture

| Group | Items | Organizing question |
|---|---|---|
| (top) | Home | Overview / launcher |
| CREATE | Image, Video, Audio, 3D Object, 3D World | "I have nothing yet" - one entry per output modality |
| STUDIO | Edit Image, Edit 3D, Edit Video [BETA], BG Change, Moodboard [BETA], Frame Extract [NEW] | "I have something, change it" |
| ASSETS | Library, Unfoldered, Folders | "My stuff" - unsorted is a first-class destination |
| RESOURCES | Tutorials, News, FAQ | External links (marketing site) |
| SUPPORT | Join Discord | External link |
| footer | DOWNLOAD ARTCRAFT | The single primary CTA, pinned |

The key move is the **verb split: Create (generate from nothing) vs Studio
(transform an existing thing)**. It answers "do I have an input yet?" before the
user has to know any tool name. Feature-area sidebars (Image tools / Video tools)
force the user to know the taxonomy first.

### Visual grammar

- Group labels: tiny uppercase Geist Mono, wide letter-spacing, muted.
- Items: Lucide-style 16px icon + label, body font.
- Active item: left accent bar (2px, primary blue) + `--sidebar-accent` fill.
  The bar survives into the collapsed icon rail, so position is never lost.
- Maturity badges: right-aligned mono uppercase chips with colored border
  (BETA amber, NEW violet). Honest maturity signalling at near-zero noise cost.
- Header: breadcrumb chip `CREATE > IMAGE` in mono, echoing the sidebar group.
  Right side: view toggles (on create pages), PRICING, LOGIN, SIGN UP.

### Two-tier navigation for heavy tools

On Edit 3D the global sidebar collapses to the icon rail and the page brings its
own chrome: FILE menu, OUTLINER, SHORTCUTS, VIEWPORT, aspect selector, a scene
panel, a bottom timeline. Rule: **the global nav moves you between tools; each
tool owns its own menus.** No 40-item sidebar trying to also be a toolbar.

### Home mirrors the sidebar

Home = hero ("What will you craft today?") + a card grid with the exact same
entries and order as the sidebar, each with a one-line description and a
distinct icon tint. Almost certainly one route registry feeding both. One
source of truth for nav, discoverability for new users, zero drift.

### Create page pattern

Empty state center ("Create Image - Describe anything. See it in seconds." +
SIGN UP TO CREATE when logged out) and a **docked bottom composer**: reference
image slot, prompt textarea, model picker chip (Nano Banana 2), aspect chip,
resolution chip, count, cost indicator, submit. Same composer across modalities.

### Weak spots (do not copy)

- Overflow: at 800x600 the list scrolls and "Folders" is clipped. 20+ items with
  two groups that are pure external links.
- RESOURCES and SUPPORT (one item) are marketing links in app nav. Belongs in a
  help popover or footer menu.
- Auth gating inconsistent: Create Image and Edit 3D usable logged out,
  Edit Video hard-redirects to `/login?from=%2Fvideo-editor` (the `from` param
  preservation is good).

## 3. Design tokens

From `:root` (dark only, `color-scheme: dark`):

```css
--sidebar-bg: #1e1f22;  --sidebar-fg: rgba(255,255,255,.72);
--sidebar-border: rgba(255,255,255,.15);  --sidebar-accent: rgba(255,255,255,.08);
--sidebar-accent-fg: #fff;  --sidebar-ring: #74aaff;
--background: 225 10% 8%;  --card: 240 11% 7%;  --primary: 216 100% 59%;
--muted-foreground: 0 0% 64%;  --border: 0 0% 100% / .15;  --ring: 217 100% 73%;
--ease-out: cubic-bezier(.22,1,.36,1);    --ease-in-out: cubic-bezier(.65,0,.35,1);
--ease-spring: cubic-bezier(.34,1.56,.64,1); --ease-emphasis: cubic-bezier(.32,.72,0,1);
--dur-fast: .14s; --dur-base: .22s; --dur-slow: .34s; --dur-page: .26s;
```

Notes:
- Sidebar tokens are separate from page tokens and the sidebar is lighter than
  the page (#1e1f22 vs ~#121317). Reads as a raised floating panel.
- **Motion tokens** (4 easings, 4 durations) are something the fleet does not
  standardize yet. Cheap to adopt, big consistency win.
- Typography triad: Archivo (display headings), Geist Mono (labels, buttons,
  chips, breadcrumbs), system-ui (body). The mono-for-chrome choice is most of
  the "tool, not website" feel.
- Analytics: GA4 (gtag). Auth: email/username + Google Identity Services.

## 4. Marketing site: getartcraft.com/apps

- Top nav: HOME, IMAGE, VIDEO, RESOURCES (menu), DOWNLOAD, SUPPORT, then a
  highlighted CRAFT APPS tab, right side PRICING, Discord icon, theme toggle,
  LAUNCH APP (white, primary).
- Hero: "Seven apps. One craft." + eyebrow `01 / CRAFTING APPS` and
  `SEVEN APPS - OPEN SOURCE - PURE RUST`. Primary CTA DOWNLOAD LAUNCHER (OS
  sniffed: "FOR WINDOWS - INSTALLER (64-BIT)"), secondary JOIN THE DISCORD,
  BROWSE ON GITHUB. Share row (copy link, X, Reddit, Bluesky, LinkedIn).
- Icon row: seven engraved-animal app icons on saturated squares. Clearly not
  Adobe's two-letter periodic-table squares. Deliberate trade-dress distance.
- Lineup cards: number, category eyebrow, name in two-tone, one-line pitch,
  status chips (EARLY ALPHA / IN DEVELOPMENT + INSTALLERS READY), platform chips
  (MACOS, WINDOWS, LINUX, WEB), EXPLORE link.
- "Next up: more crafts on the way. Tell us what to rebuild next" -> Discord.
  The community picks the next target; the tracker becomes the roadmap.
- Footer sitemap: Product / Craft Apps / Resources / Community.

### Per-app page template (PhotoCraft observed, identical skeleton for all 7)

1. Hero: number, category + maturity, H1 promise ("The image editor you already
   know how to use."), one-paragraph capability list, platform line.
2. Screenshot.
3. Highlights: six numbered cards. PhotoCraft: Familiar by design / Native GPU
   canvas / Real layered files (**"134 of 135 real-world test files round-trip
   byte for byte"**) / Non-destructive editing (16 adjustment layers, 70+
   filters, smart objects) / On-device selection / Serious color (8/16/32-bit,
   RGB/CMYK/Lab, ICC, soft proof).
4. Get it: Option 1 Launcher (recommended, v0.2.0, every Craft + one-click
   updates + verified downloads), Option 2 standalone per platform with an
   expander of every artifact: macOS universal DMG + CLI; Windows x64/x86/ARM64
   MSI + portable zips; Linux x86_64 + aarch64 AppImage/Flatpak/deb/rpm/tarball;
   FreeBSD tarball; self-hostable web build zip; SHA256SUMS. Build from source
   (Rust 1.90+).
5. "More from the family" cross-sell grid.
6. Discord CTA.

Lessons: one measurable claim (134/135) beats ten adjectives; the platform
matrix is absurdly complete and is itself the marketing; **a headless CLI "for
scripts and agents" ships next to every GUI build** (photocraft-cli). That last
item is directly MCP-wrappable, see 15 section 8.

Weakness: most page body content is invisible to `innerText` and only present
in `textContent` (animate-in visibility). Possible accessibility / crawler cost,
unverified.

## 5. Fleet adoption checklist (for WEBAPP_SOTA_STANDARDS proposal)

- [ ] Sidebar groups by user intent (verbs), not by feature area. For
      reversing-mcp: e.g. INGEST (by input kind) / WORKBENCH (tools that
      transform an existing target) / ARTIFACTS (library, unsorted, projects).
      Map from actual routes before committing; do not invent pages.
- [ ] One route registry drives sidebar AND home card grid.
- [ ] Maturity badges (BETA/NEW/ALPHA) as standard component.
- [ ] Mono uppercase group labels + breadcrumb chip echoing the group.
- [ ] Collapsible icon rail with persisted state; heavy tools auto-collapse and
      own their local chrome.
- [ ] External links out of the primary nav into a help popover.
- [ ] Motion tokens (easings + durations) in the shared token file.
- [ ] Measure overflow at 800x600; group count <= 4 visible without scroll.
