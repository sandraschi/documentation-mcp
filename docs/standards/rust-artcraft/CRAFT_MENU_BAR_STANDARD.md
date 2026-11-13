---
title: "Storytold Craft App Menu Bar & Command Hierarchy Standard"
category: standard
status: active
audience: all-craft-agents
last_updated: 2026-11-11
---

# Storytold Craft App Menu Bar & Command Hierarchy Standard

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)
**Related Standards:** [EGUI_DESKTOP_UI_AND_PARITY.md](EGUI_DESKTOP_UI_AND_PARITY.md), [CRAFT_COMMAND_BUS.md](CRAFT_COMMAND_BUS.md)
**Reference Implementations:** `cadcraft`, `filmcraft`, `photocraft`, `deckcraft`, `celcraft` (`D:\Dev\repos\celcraft`)

---

## 1. Executive Summary

Across the Storytold Craft application ecosystem (`cadcraft`, `filmcraft`, `photocraft`, `vectorcraft`, `deckcraft`, `anicraft`, `celcraft`), every native desktop workstation implements a **standardized, keyboard-driven top menu bar**.

This standard establishes the universal menu hierarchy, submenu anatomy, `switch_on_hover` behavior, modal help dialogs, and the contract between the menu bar and the headless `Command::dispatch` bus.

```
+---------------------------------------------------------------------------------------------------------------------+
| File   Edit   View   [Domain: Insert   Modify   Commands]   Window   Help                 Safe Rust (0 unsafe)  [x] |
+---------------------------------------------------------------------------------------------------------------------+
```

---

## 2. The Universal 8-Menu Anatomy (The Bookend Standard)

Every Storytold Craft application organizes its top menu bar with an immutable **Front Bookend** (`File`, `Edit`, `View`), domain-specific action menus in the middle, and an immutable **Tail Bookend** (`Window`, `Help`).

### 2.1 Front Bookend (Universal across ALL Craft Apps)

> [!NOTE]
> **Document-Centric vs. Non-File Apps:** The `File` menu is mandatory for document-based workstations (`celcraft`, `cadcraft`, `filmcraft`, `photocraft`, `deckcraft`) where users create, open, and save standalone files. In non-file/service-oriented apps (hardware daemons, network monitors, database inspectors), `File` is omitted or replaced by `Session`/`Connection`, and the immutable baseline menus become: **`Edit`**, **`Insert`** (or **`Add`**), **`View`**, **`Command`**, and **`Help`**.

| Menu | Submenu Item | Default Hotkey | Universal Action / Command Mapping |
| :--- | :--- | :--- | :--- |
| **`File`** | **New...** | `Ctrl/Cmd+N` | Create a new project AST / canvas document |
| | **Open...** | `Ctrl/Cmd+O` | Open an existing project file from disk |
| | **Open Recent ▸** | — | Submenu of recent files + `Clear Recent Files` |
| | **Save** | `Ctrl/Cmd+S` | Save current project in-place |
| | **Save As...** | `Ctrl/Cmd+Shift+S` | Prompt save file location |
| | *--- separator ---* | — | — |
| | **Export...** | `Ctrl/Cmd+E` | Open delivery export dialog (OpenEXR, ProRes, PDF, DXF) |
| | *--- separator ---* | — | — |
| | **Close Project** | `Ctrl/Cmd+W` | Unload active project AST to start screen |
| | **Quit** | `Ctrl/Cmd+Q` | Request clean application exit |
| **`Edit`** | **Undo** | `Ctrl/Cmd+Z` | Pop last transaction from undo stack |
| | **Redo** | `Ctrl/Cmd+Y` / `Cmd+Shift+Z` | Re-apply reverted transaction |
| | *--- separator ---* | — | — |
| | **Cut** | `Ctrl/Cmd+X` | Copy active selection to clipboard and delete |
| | **Copy** | `Ctrl/Cmd+C` | Copy active selection to clipboard |
| | **Paste** | `Ctrl/Cmd+V` | Paste clipboard contents at active cursor/frame |
| | **Select All** | `Ctrl/Cmd+A` | Select all elements/cells in active pane |
| | *--- separator ---* | — | — |
| | **Preferences...** | `Ctrl/Cmd+,` | Open workstation settings and theme preferences |
| **`View`** | **Zoom In** | `Ctrl/Cmd+=` | Increment stage/canvas magnification |
| | **Zoom Out** | `Ctrl/Cmd+-` | Decrement stage/canvas magnification |
| | **Fit to Window** | `Ctrl/Cmd+0` | Frame canvas centered at optimal scale |
| | **Reset Zoom (100%)** | `Ctrl/Cmd+1` | Exact 1:1 pixel rendering |
| | *--- separator ---* | — | — |
| | **Toggle Grid** | `Ctrl/Cmd+'` | Show/hide pixel or alignment grid |
| | **Toggle Guides** | `Ctrl/Cmd+;` | Show/hide vector guide segments / rulers |
| | **Onion Skinning** | `Ctrl/Cmd+Alt+O` | Toggle forward/backward ghosting overlays |
| | *--- separator ---* | — | — |
| | **Interface Theme ▸** | — | Submenu: `Dark`, `Light`, `Use System Setting` |

---

### 2.2 Domain-Specific Middle Menus (AniCraft / CelCraft Standard)

For animation and classical 2D production applications (`anicraft`, `celcraft`), the three middle menus are **`Insert`**, **`Modify`**, and **`Commands`**:

#### A. `Insert` (Asset & Exposure Additions)
- **New Drawing / Exposure** (`F7`)
- **Insert Keyframe** (`K`)
- **Insert Blank Inbetween** (`F5`)
- **Insert Vector Tape Guide** (`T`)
- *--- separator ---*
- **Import Audio Dialogue Track...**
- **Import Acme/Oxberry Scanned Peg Sheet...**

#### B. `Modify` (Transformations & Cell Adjustments)
- **Clear Exposure** (`Delete` / `Backspace`)
- **Toggle Hold** (`H`)
- **Extend Hold (+1 Frame)** (`+` / `=`)
- **Reduce Exposure (-1 Frame)** (`-`)
- *--- separator ---*
- **Bridge Linework (Directional Autogap)**
- **Flood Fill Region Under Ink (Anti-Aliasing Aware)**
- **Isolate Active Swatch (Audit Mode)**

#### C. `Commands` (Algorithmic & Compute Passes)
- **Synthesize 2.5D Surface Normal Map**
- **Propagate Paint Seeds (Block Optical Flow)**
- **Extract Anime Mouth Exposures (Levinson-Durbin LPC Lip-Sync)**
- **Align Peg Hole Centroids (Affine Bilinear Warp)**
- **Adaptive Scan Binarization (Sauvola SAT $O(1)$)**
- *--- separator ---*
- **Render Frame Composite (Evaluator DAG)**

*(Note: Other domains use their own middle menus: CADCraft uses `Insert`, `Format`, `Tools`, `Draw`, `Dimension`, `Modify`; FilmCraft uses `Clip`, `Sequence`, `Markers`, `Graphics and Titles`; DeckCraft uses `Insert`, `Format`, `Arrange`, `Slide Show`).*

---

### 2.3 Tail Bookend (Universal across ALL Craft Apps)

#### A. `Window` (Panel Layouts & Docks)
- **Reset Panel Layout** (Restore default docking arrangement)
- *--- separator ---*
- **Toolbox** (Toggle left toolbar)
- **Stage Viewport** (Toggle central canvas)
- **Exposure Sheet / Timeline** (Toggle bottom grid)
- **Palette Studio** (Toggle color swatch inspector)
- **Render & Lip-Sync Controls** (Toggle compute sidebars)

#### B. `Help` (The Standardized 5-Item Transparency Suite)
Every Storytold Craft application MUST implement these exact five items under `Help`:

| Help Item | Hotkey | Function |
| :--- | :--- | :--- |
| **Command Palette...** | `Ctrl/Cmd+Shift+P` or `Ctrl/Cmd+K` | Fuzzy-searchable overlay listing every engine tool, command, and UI shortcut. Pressing Enter executes the command immediately. |
| **Keyboard Shortcuts...** | `Ctrl/Cmd+/` or `F1` | Modal cheat sheet displaying all categorized hotkeys, studio keystrokes, and navigation controls. |
| **Project Files & Docs...** | — | Opens direct links/modals to local repository documentation (`PRD.md`, `ARCHITECTURE.md`, `TIERED_PLAN.md`, `HANDOVER.md`). |
| **Licenses & Notices...** | — | Comprehensive third-party open source attributions, `#![forbid(unsafe_code)]` compliance declaration, and MIT/Apache-2.0 legal notices. |
| **About `<AppName>`** | — | Application name, SemVer version, 100% Safe Rust guarantee, build date, commit SHA, and links. |

---

## 3. UI/UX Behavioral Mechanics

### 3.1 The `switch_on_hover` Rule
To ensure desktop-native feel matching macOS and Windows standard menus:
- Clicking a top menu header opens its popup menu.
- **While any menu popup is open, hovering over any other top menu title automatically switches the open menu to that title without requiring a second click.**
- Clicking anywhere outside closes all popups cleanly.

```rust
/// SOTA switch_on_hover implementation for egui top menu bars
fn switch_on_hover(ctx: &egui::Context, titles: &[egui::Response]) {
    let is_open = |t: &egui::Response| egui::Popup::is_id_open(ctx, egui::Popup::default_response_id(t));
    if !titles.iter().any(is_open) {
        return;
    }
    if let Some(title) = titles.iter().find(|t| t.hovered() && !t.clicked() && !is_open(t)) {
        egui::Popup::open_id(ctx, egui::Popup::default_response_id(title));
    }
}
```

### 3.2 Pure Rust & Zero Unsafe
Menu bar rendering and popup dialogs MUST abide by workspace `#![forbid(unsafe_code)]`. All popups run in immediate-mode without external web views or foreign runtimes.

---

## 4. Verification Checklist for Craft Apps

When verifying a Craft application against this standard:
- [ ] Top menu bar is present and pinned to the top of the window (`egui::Panel::top`).
- [ ] `File`, `Edit`, `View` bookend the left; `Window`, `Help` bookend the right.
- [ ] Domain-specific action menus occupy the center (e.g. `Insert`, `Modify`, `Commands` for animation).
- [ ] `Help` contains: `Command Palette`, `Keyboard Shortcuts`, `Project Files & Docs`, `Licenses & Notices`, `About <AppName>`.
- [ ] `switch_on_hover` operates smoothly when moving between open top menus.
- [ ] All menu actions dispatch directly into the universal `Command::dispatch` bus.
- [ ] Headless `--smoke` runs without window initialization and verifies menu command dispatch parity.

---

## 5. Fleet UI/UX Pattern Separation (Dashboard vs. Workstation)

Our fleet deliberately maintains clean separation between three distinct interaction patterns:

| Dimension | Pattern 1: Page-Centric Dashboard (Web SOTA / `devices-mcp`) | Pattern 2: Viewport-Centric Craft Workstation (`celcraft`, `cadcraft`, `filmcraft`) | Pattern 3: Minimalist Inspector Sidecar |
| :--- | :--- | :--- | :--- |
| **Metaphor** | Multi-page admin console / hardware controller | Creative studio suite (Photoshop, AutoCAD, Premiere) | Floating telemetry HUD |
| **Primary Navigation** | Retractable left sidebar with 3-column routing (Sidebar -> List/Master -> Detail card) | Persistent canvas/stage surrounded by dockable toolbars, top menu bar, and quick button row | Single floating panel / drawer |
| **Central Area** | Completely swapped out when selecting a different page | Persistent 2D/3D viewport or virtualized sheet that is never unloaded during navigation | Telemetry, logs, or prompt stream |
| **Top Bar** | Telemetry banner, connection pills, dark mode toggle | Full 8-menu bar (`File`, `Edit`, `View`, `Insert`, `Modify`, `Commands`, `Window`, `Help`) + mode button row | Minimal drag handle + close icon |
| **Extension Contract** | **To add a new handler (e.g. Shelly in `devices-mcp`):**<br>1. Add a row in the navigation sidebar.<br>2. Author the device handler page view. | **To add a new tool/capability in a Craft app:**<br>1. Add an entry in the `View` / `Window` menu (visibility/toggle).<br>2. Add an entry in the sidebar Toolbox / Inspector.<br>3. Optionally expose a shortcut on the top quick button row.<br>4. Wire to `Command::dispatch` for Command Palette access. | Add a tab or telemetry row. |
