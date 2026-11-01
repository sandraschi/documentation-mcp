---
title: "Pure-Rust Desktop UI (egui / eframe), UI Parity Loop & Desktop Polish Patterns"
category: standard
status: active
audience: all-agents
last_updated: 2026-10-17
---

# Pure-Rust Desktop UI (`egui` / `eframe`), UI Parity Loop & Desktop Polish Patterns

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)  
**Pilot Reference Implementation:** [`rust-devices-mcp`](../../projects/rust-devices-mcp/README.md) (`D:\Dev\repos\rust-devices-mcp\crates\devices-app`)

---

## 1. Goodbye to the 15-Layer Web/Backend Cruft Tower

Just as L1 + L2 eliminate `Python`, `uv`, `FastMCP`, `FastAPI`, `Starlette`, `Uvicorn`, and `Pydantic`, **L3 (`crates/<domain>-app`) eliminates the entire JavaScript / CSS / WebView industrial complex** (`Node`, `Bun`, `npm`, `node_modules/`, `Vite`, `React`, `Tailwind`, `PostCSS`, `Zustand`, `Lucide`, `Biome`, `tsc`, `CORS`, and `WebView2`).

### 1.1 The Retired 15-Layer Cruft Stack
Previously, to put a single button on screen that toggles a smart plug or reads an oscilloscope channel, a fleet repo had to maintain **15 separate layers across 3 languages**:
1. Python `pysomething` driver
2. FastMCP `@mcp.tool` wrapper
3. Pydantic request/response schema
4. FastAPI / Starlette HTTP route (`/api/plug/toggle`)
5. Uvicorn ASGI server + lifespan manager
6. `WEBAPP_PORTS.md` port-pair reservation + `claim_ports.py`
7. CORS middleware + `/api/capabilities` + `/health` polling in `start.ps1`
8. TypeScript `fetch()` client + duplicated `.ts` interface definitions
9. Zustand store / React state + `useEffect` hardening (`REACT_HARDENING.md`)
10. React `.tsx` component hierarchy + `data-testid` attributes
11. Tailwind CSS config + PostCSS + class string soup
12. Vite bundler + `package.json` + `bun.lock` + `300 MB node_modules/`
13. Biome linter + TypeScript compiler (`tsc --noEmit`)
14. Tauri IPC bridge + `tauri.conf.json` sidecar spawning
15. OS WebView2 / Chromium runtime eating **200-400 MB of RAM** per open app window

### 1.2 The Pure-Rust Replacement: `egui` + `eframe` Over `Command::dispatch`

Following the **ArtCraft native stack principle** (used across FilmCraft, PhotoCraft, CADCraft, etc.), L3 (`crates/<domain>-app`) is a pure-Rust immediate-mode GPU application using **`egui` + `eframe`**:

```rust
// In crates/<domain>-app: one button = 3 lines of pure Rust, zero HTTP, zero JS/CSS!
if ui.button("Toggle Plug").clicked() {
    self.last_result = Some(run(Command::PlugToggle {
        vendor: self.vendor,
        device_ip: self.ip.clone(),
        state: !self.is_on,
        creds: self.creds.clone(),
    }));
}
```

### 1.3 Why `egui` + `Command::dispatch` Beats Vite + Tailwind + FastAPI on Every Axis

| Dimension | Legacy (`FastAPI` + `Vite` + `React` + `Tailwind` + `WebView2`) | Pure-Rust ArtCraft (`devices-core` + `egui` / `eframe`) |
|---|---|---|
| **Total Dependencies & Toolchains** | Python + `uv` + Node/Bun + Vite + Tailwind + Biome + Ruff + WebView2 | **`cargo build --release` (1 toolchain, 1 lockfile)** |
| **Disk Footprint per Repo** | ~450 MB (`.venv` + `node_modules` + `dist`) | **Zero `node_modules`, zero `.venv`; single ~4-12 MB `.exe`** |
| **RAM Usage at Idle** | 250 - 500 MB (Python interpreter + Uvicorn + Chromium WebView2) | **15 - 30 MB (native `wgpu` / OpenGL surface)** |
| **Frame Rate & Latency** | DOM layout + IPC + localhost HTTP serialization | **60-144 FPS immediate-mode GPU rendering; sub-millisecond in-process call** |
| **Platform Agnosticism** | Tied to WebView2 quirks (`WEBVIEW2_VS_LEGACY.md`) and port availability | **Runs natively on Windows, Linux, macOS, AND compiles to WebAssembly (`wasm32-unknown-unknown`) if a browser build is ever needed** |
| **Agent Authoring Velocity** | Agent must edit 6 files across Python, TS, and CSS to add 1 button; high risk of CORS/type/hook bugs | **Agent adds 1 `Command` variant in L1 and 5 lines of `ui.horizontal(...)` in L3; compiler verifies types end-to-end** |
| **Headless Snapshot & CI Testing** | Requires starting Uvicorn + Vite + headless Playwright browser (`playwright_e2e_sota.md`) | **`egui_kittest` renders UI frames in pure `cargo test` in milliseconds with zero browser** |

---

## 2. The Last Laugh of GPU-Rendered UI (`gpui`, `egui`, `wgpu`): "Who Does UI on the GPU?!"

When Zed's creators (Nathan Sobo & team, who previously built Atom on Electron) announced **`gpui`** -- a custom Rust UI framework that renders every character, border, and shadow directly on the GPU like a 3D video game -- Hacker News and Reddit mocked it relentlessly:
- *"Why are you writing custom Metal/Vulkan shaders just to draw a text box?!"*
- *"Just use Electron / DOM / SwiftUI / GTK like normal people!"*

Look who is laughing in 2026:
1. **The Irony of the Critics:** The people yelling *"Who does UI on the GPU?!"* were running **Electron / WebView2 / Chrome**, which runs a **15-million-line C++ compositor (`Skia` + `Blink` + `Dawn`) that translates HTML/CSS into... GPU triangles anyway**, after burning 300 MB of RAM and 8 layers of DOM layout, CSS cascade, and JavaScript garbage collection!
2. **`egui` and `gpui` Just Cut Out the 15-Million-Line Middleman:**
   - Every modern machine (from an RTX 4090 on `Goliath` to an M-series MacBook or integrated laptop iGPU) has a massively parallel GPU sitting 99% idle during desktop work.
   - By treating a 2D application like a **120 FPS video game frame** (compute layout in flat Rust arrays -> upload vertex buffer -> draw in `< 0.5 ms` via `wgpu`/Metal/DX12/Vulkan), you throw away the DOM, CSS, React Virtual DOM diffing, IPC bridges, and OS widget toolkits in one stroke.
3. **Why Video-Game-Style Immediate-Mode UI Is the Ultimate Agent Architecture:**
   - Retained-mode UIs (DOM / React / SwiftUI / Qt) suffer from **state synchronization bugs**: the UI tree holds one copy of state, the backend holds another, and `useEffect` / callbacks drift out of sync.
   - In GPU immediate-mode (`egui`) or hybrid-GPU (`gpui`), **the UI is a pure function of current Rust structs every frame**: `fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame)`. There is no shadow DOM to go stale, no CSS specificity war, and no callback spaghetti -- which is why ArtCraft's agent loops could build 7 pro creative apps (`FilmCraft`, `PhotoCraft`, `CADCraft`) without getting lost in frontend state bugs.

---

## 3. The Mechanical UI Parity Loop (`UI_PARITY.md`), `egui_kittest` Goldens & The Tofu Glyph Guard

OpenCode established a **6-step mechanical UI parity workflow** (`docs/UI_PARITY.md` in `rust-devices-mcp`) that treats the legacy Python/React webapp as a **visual oracle** and locks the pure-Rust `egui` clone with headless PNG golden snapshots:

```text
1. ORACLE    Capture reference PNGs of the running legacy Python webapp (1280x860 dark, Playwright)
     |
     v
2. CLONE     Build the matching sidebar + view cards in crates/<domain>-app/src/app.rs (eframe/egui)
     |
     v
3. CAPTURE   Launch target/release/<domain>-app.exe and capture the live Win32 window via PrintWindow/BitBlt
     |
     v
4. COMPARE   Diff docs/parity/legacy/<page>.png against docs/parity/rust/<page>.png
     |
     v
5. CONVERGE  Fix layout, typography, colors, or missing controls in app.rs until every view matches
     |
     v
6. LOCK      Write an egui_kittest + image golden test in crates/<domain>-app/tests/kittest_ui.rs
```

### Mandatory `egui` Desktop Guardrails Proven in `v0.2.0`
1. **High-Contrast `slate-950` Visuals (`harsh_visuals`):**
   - Stock `egui::Visuals::dark()` uses washed-out `#1b1b1b` backgrounds, `#8c8c8c` muted text (~4:1 contrast), and cramped `12.5px` body fonts.
   - Fleet `egui` apps apply a canonical `harsh_visuals()` preset at startup: `slate-950` (`#0a0d12`) canvas, `#101a2e` card fill, `#f5f7fa` primary text (~18:1 contrast), `#bac2ce` secondary text (~10:1 contrast), `1px` `#263452` card strokes, and bumped typography (`16px` Body/Button, `14px` Monospace, `23px` Heading).
2. **The Tofu (`□`) Glyph Guard (`glyph_allowlist` Test):**
   - `egui 0.37` ships with `Ubuntu-Light` + `egui-icons`, which covers Latin-1 and general punctuation (`°`, `×`, `·`, `…`) **but does NOT include geometric symbols, emojis, or dingbats** (`●`, `○`, `◆`, `▸`, `▾`, `✓`, `⚠`, `★`, `☀`, `🌙`). Any agent that puts those characters into `ui.label(...)` produces ugly tofu boxes (`□`) on screen.
   - **Rule:** Status indicators (online/offline dots, sun/moon theme icons, badges, chevrons) MUST be drawn with `ui.painter()` vector shapes (`circle_filled`, `line_segment`) or ASCII (`[v]`, `[ ]`, `- Menu`, `+ Menu`), and `crates/<domain>-app/src/app.rs` MUST include a `glyph_allowlist` unit test that scans its own source (`include_str!("app.rs")`) and fails `cargo test` if any non-ASCII char outside the verified safe set (`°` `U+00B0`, `×` `U+00D7`, `·` `U+00B7`, `…` `U+2026`, `U+2014`) appears.
3. **Browserless Golden Snapshot Locking (`egui_kittest`):**
   - Unlike Playwright E2E suites that require spinning up Uvicorn + Vite + Chromium, `egui_kittest` (`0.37` with `wgpu` + `snapshot` features) renders individual `egui` panels in pure `cargo test` and diffs them against `crates/<domain>-app/tests/snapshots/*.png`.

---

## 4. Pure-Rust Desktop Feature Parity & Polish Patterns (`egui 0.37`)

When bringing a pure-Rust `egui` desktop app to 100% visual and interactive parity with a SOTA React/Tailwind webapp, use these four zero-bloat Rust patterns:

### 4.1 `Ctrl + MouseWheel` (and `Ctrl + +`/`-`/`0`) Global UI Zoom
`egui::Context` has a built-in **`zoom_factor`** multiplier that scales every font, card border, vector icon, and layout margin on the GPU in one call. Keyboard `Ctrl + Plus` / `Ctrl + Minus` / `Ctrl + 0` works automatically, and adding **`Ctrl + MouseWheel`** takes 12 lines at the top of `eframe::App::ui`:

```rust
fn handle_zoom(ctx: &egui::Context) {
    let scroll_y = ctx.input(|i| {
        if i.modifiers.ctrl || i.modifiers.command {
            i.raw_scroll_delta.y
        } else {
            0.0
        }
    });
    if scroll_y.abs() > 0.0 {
        let step = if scroll_y > 0.0 { 1.1_f32 } else { 1.0 / 1.1_f32 };
        let next = (ctx.zoom_factor() * step).clamp(0.6, 2.5);
        ctx.set_zoom_factor(next);
    }
}
```
- Persist `zoom_factor: f32` in `UiStore` (`ui.json`) and render a clickable `"100%"` pill in the topbar that calls `ctx.set_zoom_factor(1.0)` to reset.

### 4.2 Light / Dark Theme Switcher + Vector-Painted Sun / Crescent Moon in Topbar
Because Unicode `☀` (`U+2600`) and `🌙` (`U+1F319`) are absent from `egui`'s default font and would trigger tofu (`□`), paint an anti-aliased vector **Sun** (core circle + 8 radial rays) or **Crescent Moon** (circle minus offset cutout circle) directly onto a `28x28` button `Rect` using `ui.painter()`:

```rust
fn theme_toggle_button(ui: &mut egui::Ui, dark_mode: &mut bool) -> bool {
    let size = egui::vec2(28.0, 28.0);
    let (rect, resp) = ui.allocate_exact_size(size, egui::Sense::click());
    if ui.is_rect_visible(rect) {
        let visuals = ui.style().interact(&resp);
        ui.painter().rect(
            rect,
            egui::CornerRadius::same(6),
            visuals.bg_fill,
            visuals.bg_stroke,
            egui::StrokeKind::Inside,
        );
        let center = rect.center();
        let painter = ui.painter();
        if *dark_mode {
            // Golden Sun icon (click to switch to Light mode)
            let sun_color = egui::Color32::from_rgb(251, 191, 36);
            painter.circle_filled(center, 4.5, sun_color);
            for i in 0..8 {
                let angle = (i as f32) * std::f32::consts::TAU / 8.0;
                let dir = egui::vec2(angle.cos(), angle.sin());
                painter.line_segment(
                    [center + dir * 6.5, center + dir * 9.2],
                    egui::Stroke::new(1.6, sun_color),
                );
            }
        } else {
            // Slate-indigo Crescent Moon icon (click to switch to Dark mode)
            let moon_color = egui::Color32::from_rgb(51, 65, 85);
            painter.circle_filled(center, 6.5, moon_color);
            painter.circle_filled(center + egui::vec2(3.0, -2.2), 5.5, visuals.bg_fill);
        }
    }
    let clicked = resp.on_hover_text("Toggle Light / Dark theme").clicked();
    if clicked {
        *dark_mode = !*dark_mode;
        ui.ctx().set_visuals(if *dark_mode {
            harsh_visuals()
        } else {
            crisp_light_visuals()
        });
    }
    clicked
}
```
- **Light Theme Companion (`crisp_light_visuals()`):** Pair `harsh_visuals()` (`slate-950` dark) with `crisp_light_visuals()` based on `egui::Visuals::light()` using `#f8fafc` (`slate-50`) panel fill, `#ffffff` card fill, `#0f172a` (`slate-900`) text, and `1px` `#cbd5e1` (`slate-300`) hairline borders.

### 4.3 Energy & Weather Telemetry Graphs in Pure Rust
You have two clean options for rendering **Energy (Watts / kWh)** and **Weather (24h Temperature / Humidity / Wind)** charts:

#### Option A: Zero-Dependency GPU Canvas Charts (`ui.painter()`) -- *Zero New Crates, Instant Compile*
Use `ui.allocate_exact_size(..., egui::Sense::hover())` + `ui.painter_at(rect)` to draw horizontal reference gridlines, anti-aliased polylines (`egui::Shape::line`), data point nodes (`circle_filled`), bar comparisons (`rect_filled`), and interactive hover crosshairs (`resp.hover_pos()`):

```rust
fn spark_chart(
    ui: &mut egui::Ui,
    title: &str,
    unit: &str,
    samples: &[(String, f64)],
    stroke_color: egui::Color32,
) {
    card_frame(ui, |ui| {
        ui.label(egui::RichText::new(title).strong());
        let desired = egui::vec2(ui.available_width().max(240.0), 140.0);
        let (rect, resp) = ui.allocate_exact_size(desired, egui::Sense::hover());
        let painter = ui.painter_at(rect);

        // 1. Horizontal reference gridlines (0%, 50%, 100%)
        let grid_stroke = egui::Stroke::new(1.0, ui.visuals().widgets.noninteractive.bg_stroke.color);
        for frac in [0.0_f32, 0.5, 1.0] {
            let y = egui::lerp(rect.top() + 8.0..=rect.bottom() - 18.0, frac);
            painter.line_segment([egui::pos2(rect.left(), y), egui::pos2(rect.right(), y)], grid_stroke);
        }

        if samples.len() < 2 {
            painter.text(
                rect.center(),
                egui::Align2::CENTER_CENTER,
                "Collecting telemetry samples...",
                egui::FontId::proportional(14.0),
                ui.visuals().text_color(),
            );
            return;
        }

        // 2. Normalize values into screen coordinates
        let min_v = samples.iter().map(|(_, v)| *v).fold(f64::INFINITY, f64::min);
        let max_v = samples.iter().map(|(_, v)| *v).fold(f64::NEG_INFINITY, f64::max);
        let span = (max_v - min_v).abs().max(1.0);
        let plot = rect.shrink2(egui::vec2(6.0, 14.0));
        let n_minus_1 = (samples.len().saturating_sub(1)).max(1) as f32;

        let pts: Vec<egui::Pos2> = samples
            .iter()
            .enumerate()
            .map(|(idx, (_, val))| {
                let tx = (idx as f32) / n_minus_1;
                let ty = ((*val - min_v) / span) as f32;
                egui::pos2(
                    egui::lerp(plot.left()..=plot.right(), tx),
                    egui::lerp(plot.bottom()..=plot.top(), ty),
                )
            })
            .collect();

        // 3. Anti-aliased curve + nodes + hover crosshair
        painter.add(egui::Shape::line(pts.clone(), egui::Stroke::new(2.2, stroke_color)));
        for pt in &pts {
            painter.circle_filled(*pt, 3.5, stroke_color);
        }
        if let Some(mouse) = resp.hover_pos() {
            if let Some((idx, pt)) = pts
                .iter()
                .enumerate()
                .min_by(|(_, a), (_, b)| (a.x - mouse.x).abs().total_cmp(&(b.x - mouse.x).abs()))
            {
                if let Some((label, val)) = samples.get(idx) {
                    painter.vline(pt.x, plot.y_range(), egui::Stroke::new(1.0, stroke_color));
                    painter.circle_stroke(*pt, 6.0, egui::Stroke::new(2.0, egui::Color32::WHITE));
                    resp.on_hover_text(format!("{label}: {val:.1} {unit}"));
                }
            }
        }
    });
}
```
- **Energy Page:** Maintain a bounded `VecDeque<(String, f64)>` (last 60 power samples) + a horizontal per-plug bar chart comparing live wattage across all imported plugs (`.38` Server `290 W` vs `.156` Lamp vs `.178` Dishwasher).
- **Weather Page:** Append `&hourly=temperature_2m,relative_humidity_2m,precipitation_probability&forecast_days=1` to the keyless Open-Meteo query in `weather.rs` so the Weather page renders a **live 24-hour temperature and humidity curve** on first paint.

#### Option B: `egui_plot` Crate (`0.37`) -- *For Multi-Axis Pan/Box-Zoom/Oscilloscope Traces*
When a tool needs multi-series legends, box-zoom, or log scales, add `egui_plot = "0.37"` and render `Plot::new("id").height(180.0).show(ui, |plot_ui| plot_ui.line(...))`.

### 4.4 Prettification with Crisp Border Lines (Panels, Inputs & Accent Cards)
1. **Panel Separator Hairlines (Topbar bottom border, Sidebar right border, Statusbar top border):**
   `egui::Panel::top` and `Panel::left` draw their dividing border using `visuals.widgets.noninteractive.bg_stroke`. Explicitly set it in both `harsh_visuals()` and `crisp_light_visuals()`:
   ```rust
   // Dark mode: 1px slate-800 hairline on topbar, sidebar, status bar, and ui.separator()
   visuals.widgets.noninteractive.bg_stroke =
       egui::Stroke::new(1.0, egui::Color32::from_rgb(38, 54, 84));
   ```
2. **Button & Text-Input Outlines:**
   ```rust
   visuals.widgets.inactive.bg_stroke =
       egui::Stroke::new(1.0, egui::Color32::from_rgb(48, 66, 102));
   visuals.widgets.hovered.bg_stroke =
       egui::Stroke::new(1.5, ACCENT);
   ```
3. **Domain-Colored Accent Stripes on KPI & Section Cards:**
   In `card_frame`, paint a `3px` accent bar along the left or top edge of the card (`ENERGY` amber for plugs, `HUE_YELLOW` for lighting, `SKY` for weather, `RING_BLUE` for security) to mirror Tailwind `border-l-4` cards in pure GPU geometry.

---

### 4.5 The Full Structural Parity Law ("Clone, Not Inspired By")
A critical failure mode in conversion is building a toy dashboard that misses most of the original webapp's functionality.
- **Rule:** Rustification does NOT mean "inspired by old app". The Rust desktop application MUST look and act like a real clone of the legacy webapp.
- **Mandatory Step 0:** Inspect `sidebar.tsx` and all page routes (`app/**/page.tsx` or `pages/**`). Every navigational category (e.g. `CONTENT`, `DISCOVER`, `MANAGE`, `AI & FLEET`, `SYSTEM`) and every single subpage (e.g., `Libraries`, `Books`, `Authors`, `Series`, `Tags`, `Publishers`, `Duplicates`, `Reading`, `Health`, `Chat`, `Logs`, `Settings`, `Help`, `Raw JSON`) MUST have an explicit `Page` enum variant and dedicated view in `crates/<domain>-app/src/app.rs`.

---

### 4.6 Mandatory Fleet Standard LLM Settings Card
Every converted ArtCraft app's Settings page MUST include the canonical Fleet LLM Settings Card:
1. **Provider Selector:** Ollama (`http://127.0.0.1:11434/v1`), LM Studio (`http://127.0.0.1:1234/v1`), OpenAI (`https://api.openai.com/v1`), Anthropic (`https://api.anthropic.com`), Custom.
2. **Editable Base URL & Default Models:** Pre-fills `gemma4:12b` for Ollama, `gpt-4o-mini` for OpenAI, `claude-sonnet-4-20250514` for Anthropic.
3. **OS Credential Manager Vault:** API keys entered by the user are stored strictly via `keyring` in Windows Credential Manager / macOS Keychain / Secret Service under the repo name (e.g. `rust-<domain>-mcp`). Secrets never touch plain text files on disk.
4. **Live Dynamic Model Elicitation:** A button that dispatches a query to `/api/tags` (Ollama) or `/v1/models` (OpenAI/LM Studio), populating a dynamic `egui::ComboBox` dropdown picker so the user selects from live downloaded/served models without typing strings manually.
5. **Live Connection Test Button:** Dispatches a minimal non-streaming prompt (`"Ping"`) to verify connectivity and displays a green/red status pill with latency and response note.
