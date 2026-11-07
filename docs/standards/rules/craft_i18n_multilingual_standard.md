# Craft Ecosystem Multilingual Internationalization (i18n) Standard

**Status**: Active Fleet Standard  
**Date**: 2026-11-04  
**Scope**: All Craft sovereign applications (`*craft`)

---

## 1. Principles & Architecture

Every Craft application (`moneycraft`, `qgiscraft`, `sportscraft`, `robotcraft`, `writercraft`, `djcraft`, `makercraft`, `modcraft`, `lookcraft`, `codercraft`, `appcraft`, `travelcraft`) MUST adhere to the sovereign zero-panic Rust i18n standard.

1. **Pure Rust Compile-Time Dictionaries**:
   - Zero dynamic runtime asset loading or fragile runtime string files (no gettext `.po`/`.mo`, no JSON runtime parsing on startup).
   - All translations live in `crates/<app>-core/src/i18n.rs`.
   - Complete zero-panic compliance: `#![deny(clippy::unwrap_used)]`, `#![deny(clippy::expect_used)]`, `#![deny(clippy::panic)]`.

2. **Standard Target Locales (7 Fleet Locales)**:
   - `En` — English (US/UK) - Global Fleet Default (`🇬🇧` / `🇺🇸`)
   - `De` — Deutsch (DE/AT/CH) - Heritage German/Austrian (`🇩🇪` / `🇦🇹`)
   - `Fr` — Français (FR) (`🇫🇷`)
   - `Es` — Español (ES/LATAM) (`🇪🇸`)
   - `Ja` — 日本語 (JA) (`🇯🇵`)
   - `Ko` — 한국어 (KO) (`🇰🇷`)
   - `Zh` — 中文 (ZH) (`🇨🇳`)

3. **Type-Safe Key and Lookup Signature**:
   ```rust
   #[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize, Default)]
   pub enum AppLocale {
       #[default]
       En,
       De,
       Fr,
       Es,
       Ja,
       Ko,
       Zh,
   }

   #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
   pub enum I18nKey {
       // Domain-specific keys
   }

   pub fn t(key: I18nKey, locale: AppLocale) -> &'static str {
       match (key, locale) {
           // Exhaustive compile-time pattern matches
       }
   }
   ```

4. **Desktop GUI Selector Integration**:
   - Every Craft GUI application (`crates/<app>-app/src/main.rs`) includes `pub locale: <app>_core::i18n::AppLocale` in its primary state struct.
   - The top menu bar exposes a language dropdown selector:
     ```rust
     let cur_loc = self.locale;
     let loc_label = format!("{} {}", cur_loc.flag(), cur_loc.code().to_uppercase());
     egui::ComboBox::from_id_salt("topbar_locale_selector")
         .selected_text(loc_label)
         .show_ui(ui, |ui| {
             for loc_item in <app>_core::i18n::AppLocale::all() {
                 let text = format!("{} {}", loc_item.flag(), loc_item.display_name());
                 let _ = ui.selectable_value(&mut self.locale, *loc_item, text);
             }
         });
     ```
   - All menu headers, tab items, action buttons, and status lines dynamically consult `t(key, self.locale)`.

---

## 2. Roster of Compliant Craft Applications (13/13 Verified)

| Application | Core Crate Path | Port | Key Domains Localized |
|:---|:---|:---|:---|
| **MoneyCraft** | `crates/moneycraft-core/src/i18n.rs` | 14125 | Portfolio, checking/festgeld, historic panics (1850 London/EIC), real data providers |
| **QgisCraft** | `crates/qgiscraft-core/src/i18n.rs` | 14126 | QGIS menus, vector/raster GIS layers, geoprocessing tools, coordinate reference systems |
| **SportsCraft** | `crates/sportscraft-core/src/i18n.rs` | 14124 | Match simulation, player metrics, tactics, sports telemetry |
| **RobotCraft** | `crates/robotcraft-core/src/i18n.rs` | 14121 | Kinematics, trajectory planners, actuator safety limits, ROS2 bridge |
| **WriterCraft** | `crates/writercraft-core/src/i18n.rs` | 14118 | Sovereign Markdown editor, word counts, typography styling, document exporting |
| **DjCraft** | `crates/djcraft-core/src/i18n.rs` | 14123 | Turntables, pitch faders, stem separation, BPM synchronizer, Hercules DJ controllers |
| **MakerCraft** | `crates/makercraft-core/src/i18n.rs` | 14120 | CAD/CAM slicer, G-code preview, toolhead temperatures, Bed leveling |
| **ModCraft** | `crates/modcraft-core/src/i18n.rs` | 14127 | Reverse engineering engine, PE/ELF binary analysis, disassembler, entropy |
| **LookCraft** | `crates/lookcraft-core/src/i18n.rs` | 14116 | Desktop mail client, IMAP/SMTP, design systems, generative UI palettes |
| **CoderCraft** | `crates/codercraft-core/src/i18n.rs` | 14128 | Sovereign agentic IDE studio, swarm supervisor, multi-display quad, fleet depot |
| **AppCraft** | `crates/appcraft-core/src/i18n.rs` | 14115 | App scaffolding, template picker, domain blueprints, stigmergic ledger, compiler |
| **TravelCraft** | `crates/travelcraft-core/src/i18n.rs` | 14129 | Baedeker chrono-cartography, waypoint dossiers, sensory atmosphere, SightLens AI |
| **SpeechCraft** | `crates/speechcraft-core/src/i18n.rs` | 14132 | Wake word coordinator (`wakeywakey`), Voice Command Bus (10996), prosody, timeline |

---

## 3. Verification & Testing

Every compliant crate includes exhaustive unit tests ensuring all 7 locales have non-empty codes, display names, flags, and string entries for every `I18nKey`:
```bash
cargo test -p <app>-core
```
All 13 applications pass 100% of unit, integration, and GUI tests.
