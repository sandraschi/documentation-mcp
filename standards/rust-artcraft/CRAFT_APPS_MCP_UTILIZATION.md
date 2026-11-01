---
title: "Craft Apps MCP Utilization Strategy (Commercial ArtCraft Suite as Fleet Engines)"
category: standard
status: active
audience: all-agents
last_updated: 2026-10-20
---

# Craft Apps MCP Utilization Strategy

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)
**Sibling:** `CONTAINMENT_AND_CRATES.md`, `FLEET_CONVERSION_STANDARD.md`, `FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md`
**Command bus / two planes:** [CRAFT_COMMAND_BUS.md](./CRAFT_COMMAND_BUS.md) - the non-obvious part: every app is headless *and* live, the command registry, per-app attach flags, verified examples, config shapes, traps.
**Reference wrapper:** `D:\Dev\repos\democraft-mcp` (`craft` portmanteau, outbox pattern)
**First consumer:** `D:\Dev\repos\pdf-mcp` + `C:\Program Files\PdfCraft\pdfcraft-cli.exe`

> Terminology guard: "ArtCraft harness" = the Pure-Rust containment pattern (L1 core / L2 CLI+MCP / L3 egui, `deny(unwrap_used)`, `Command::dispatch`) borrowed from Brandon Thomas (`storytold`). "Craft apps" = his commercial Rust product suite (PdfCraft, PhotoCraft, ...). Same author, same philosophy, different artifact. This doc is about using the second as engines inside the first. Do not conflate.

## 1. Why this doc exists

The Craft apps ship at a rapid clip (measured 2026-10-25: all 13 CLIs installed 2026-10-25, versions 0.10.0-0.17.0, full release trains on 2026-10-20 and 2026-10-22 upstream at `github.com/storytold/*craft`). Each is a native Rust engine with a headless CLI, a stdio MCP server, and a live-app control port. Reimplementing their cores in Python (PDF merge, photo develop, vector render, audio bounce) is wasted tokens and worse quality. Fleet doctrine: **wrap, don't reimplement. The engine is the oracle.**

## 2. Inventory (measured 2026-10-25, Goliath)

Source of truth: `C:\Program Files\<Craft>\<craft>-cli.exe --version` + `LastWriteTime`. Re-measure with:

```powershell
foreach ($d in @("CADCraft","DeckCraft","DesignCraft","EffectCraft","FigCraft","FilmCraft","GridCraft","LightCraft","PdfCraft","PhotoCraft","SoundCraft","VectorCraft","WordCraft")) { $f = Get-Item "C:\Program Files\$d\*-cli.exe" | Select-Object -First 1; & $f.FullName --version }
```

| App | CLI | Version (2026-10-25) | GUI | pdf-mcp relevance |
|---|---|---|---|---|
| CADCraft | `cadcraft-cli.exe` (51 MB) | 0.13.0 | `cadcraft.exe` | low - DXF plan -> PDF via `convert` |
| DeckCraft | `deckcraft-cli.exe` (71 MB) | 0.11.1 | yes | medium - slides -> PDF export |
| DesignCraft | `designcraft-cli.exe` (71 MB) | 0.13.0 | yes | low |
| EffectCraft | `effectcraft-cli.exe` (85 MB) | 0.17.0 | yes | low - title stills for covers |
| FigCraft | `figcraft-cli.exe` (77 MB) | 0.11.2 | yes | low |
| FilmCraft | `filmcraft-cli.exe` (66 MB) | 0.13.0 | yes | low |
| GridCraft | `gridcraft-cli.exe` (14 MB) | 0.12.1 | yes | medium - sheets/XLSX + PDF |
| LightCraft | `lightcraft-cli.exe` (108 MB) | 0.14.0 | yes | low - grade scanned pages |
| PdfCraft | `pdfcraft-cli.exe` (66 MB) | 0.14.0 | `pdfcraft.exe` (94 MB) | **primary - see S3** |
| PhotoCraft | `photocraft-cli.exe` (75 MB) | 0.16.0 | yes | medium - `convert` + `info` pipeline |
| SoundCraft | `soundcraft-cli.exe` (8 MB) | 0.13.1 | yes | none |
| VectorCraft | `vectorcraft-cli.exe` (106 MB) | 0.17.0 | yes | medium - SVG -> PDF |
| WordCraft | `wordcraft-cli.exe` (76 MB) | 0.11.0 | yes | high - md/docx/pdf round-trips, seed PDFs |

Sizes and versions re-measured 2026-10-25 with the loop above (installed 10-25 13:23-14:04 local; upstream tags published 2026-10-25 13:27-14:17 UTC). This table is a snapshot, never a pin - track head.

**SoundCraft 0.13.1 (installed 2026-10-25 13:39)**: BUG-082 still open - a premature fixed claim entered 2026-10-25 was retracted the same day after a proper retest: VST3 instruments (Surge XT, Dexed) render silence headless on 0.13.1 (peak 1, RMS 0.5 vs built-in control 1,154,880 peak), exactly the 0.10.0 signature; no release between 0.10.0 and 0.13.1 mentions an instrument fix. Candidate vehicle #400 (merged 2026-10-13) did not resolve the audible path; PR #347 still open ("hand host-set parameter values to the controller before saving state", merged 2026-10-13) plus #410/#342 parameter hardening; PR #347 is still open but is no longer the vehicle. `democraft-mcp`'s `sound/melody-vst3` demo may now swap `mix.instrument` to Surge. See `projects/adobe-offensive/22-soundcraft-status.md` and `guides/daw-plugins.md`.

Every CLI supports the same three control planes (verified on PdfCraft, spot-checked on Photo/Vector/Word):

```
<craft>-cli.exe <verb> ...          # headless domain verbs
<craft>-cli.exe tools               # automation tools + JSON Schemas
<craft>-cli.exe run <tool> k=v ...  # single tool run
<craft>-cli.exe run --script steps.json [--report]  # batch script
<craft>-cli.exe mcp [--root DIR] [--compact] [--automation-read-root DIR] [--automation-write-root DIR]
<craft>-cli.exe ui --control FILE <method> [k=v] [--out shot.png]
```

Docs: `https://getartcraft.com/apps/<lower>craft`, source `https://github.com/storytold/<lower>craft`, feedback `https://discord.gg/artcraft`.

## 3. PdfCraft x pdf-mcp bridge (reference implementation)

PdfCraft verbs (from `pdfcraft-cli.exe --help`):

```
info <file.pdf> | render <file.pdf> --page N --dpi 96 --out x.png
text <file.pdf> [--page N] | edit <in.pdf> --out out.pdf [--rotate/--delete/--move/--insert-blank/--title/--author/--full]
combine <a.pdf> <b.pdf> --out combined.pdf | extract --pages 1,3,5-8 | split (--every N | --before 3,7)
check <files|dirs> [--json out.json] | audit <file.pdf> (finds faux redactions, fails when found)
batch --steps convert,ocr,optimize --out-dir DIR [--ppi 150] [--quality 60] [--dpi 300] [--language en]
```

`tools` reveals the session model: `doc_open / doc_list / doc_info / doc_close / doc_save / doc_batch` with `input_schema` per tool.

### 3.1 Lane A - headless subprocess (build first)

New `pdf_mcp/services/pdfcraft_engine.py`, patterned on `democraft-mcp/src/democraft_mcp/crafts.py`:

```python
PDFCRAFT_CLI = Path(os.environ.get("PDFCRAFT_CLI", r"C:\Program Files\PdfCraft\pdfcraft-cli.exe"))
def cli_run(args, run_dir) -> {ok, stdout, stderr, ms}
```

Ops: `pdfcraft_info, pdfcraft_render, pdfcraft_combine, pdfcraft_split, pdfcraft_text, pdfcraft_audit, pdfcraft_batch`. All writes go to `data/pdfcraft/<job>/`, never in place. Fallback chain per op: engine ok -> return bytes; binary missing -> `{success:false, error:"wrappee_missing"}`; account-gated -> `needs_account`. This unblocks Workbench thumbnail rail, combine, and real redaction audit with zero MCP lifecycle risk.

Fit map: keep RAG/forms/classify/redact-regex/recipes in Python (LanceDB + pdfplumber); delegate render/combine/split/edit/OCR/optimize/audit to the engine.

### 3.2 Lane B - native MCP sidecar (build second)

```
pdfcraft-cli mcp --compact --automation-read-root <inbox> --automation-write-root <outbox>
```

pdf-mcp spawns it as a stdio child, exposes `pdf_craft_run(tool, args)` and `pdf_craft_script(steps.json)` passthrough (`tool_search`/`tool_call` when `--compact`). Gate with `PDFCRAFT_MCP=0/1`, default 0 until Lane A is green. Benefits: typed schemas, `doc_open` sessions, atomic `doc_save`. Cost: process supervision.

### 3.3 Lane C - live app drive (interactive only)

Start `pdfcraft.exe --control <pipe/file>`, then `pdfcraft-cli ui --control <file> <method> --out shot.png`. Use only for Fill&Sign bake review and visual sign-off behind an explicit "Open in PdfCraft" button. Hands-out rule: automation never mutates the user's open document; it works in the job outbox.

## 4. Fleet-wide smorgasbord map

| Fleet MCP | Craft engine | Delegated verbs |
|---|---|---|
| pdf-mcp | PdfCraft (primary), WordCraft (seed) | render/combine/split/audit/batch-ocr + `convert brief.md brief.pdf` |
| libreoffice-mcp, calibre-mcp | WordCraft | md/docx/pdf round-trips, Report template styling |
| ocr-mcp | PdfCraft `batch --steps ocr` | OCR with installed models, `--language`, `--ocr-all-pages` |
| photo/image flows, obs-mcp covers | PhotoCraft `convert/info`, LightCraft grade, DesignCraft | pelican benchmark pattern from democraft |
| cad/vector/fig/deck/grid | CADCraft/VectorCraft/FigCraft/DeckCraft/GridCraft | DXF->PDF, SVG->PDF, XLSX+PDF, slide decks |
| video/audio | FilmCraft/EffectCraft/SoundCraft | stills, bounces (AI writes words only, engine renders pixels) |

`democraft-mcp` remains the conformance harness: every bridge must pass a real `run_demo + ai_flow` producing real artifacts in `outbox/<app>/<demo>/`. Shapes may be AI-drawn, pixels must be engine-rendered. No fake pixels.

## 5. Release-tracking SOP (rapid-clip upstream)

Upstream merges aggressively; the fleet must not pin-and-forget.

1. **Runtime guard, not a cadence.** Capture `<cli> --version` plus a hash of the sorted verb list from `commands --json` on first use in a session, cached by (path, mtime, size). `craft_commands` compares against the recorded pair and returns `engine_drift` with the added and removed verbs. No schedule can be frequent enough: measured 2026-10-20, the launcher wrote designcraft 0.10.0, figcraft 0.8.0, gridcraft 0.9.0 and soundcraft 0.10.0 into `C:\Program Files` at 10:29-10:43 UTC, while GitHub published those same tags at 14:34-16:48 UTC. Installs land about four hours before the release announcement, so a release-feed poll reports a version you have already been running.
2. **Release watch is informational only.** Poll `https://github.com/storytold/<app>/releases.atom` on the existing digest cadence. A new tag schedules the regression gate; it never gates work, because the binary on disk can be newer than the tag.
3. **Regression gate fires on drift, not on a calendar.** Version or schema change -> `democraft run_demo pdf portfolio` + `pdf-mcp` engine smoke (`info/render/audit` on golden PDFs in `tests/fixtures/`), then append a dated row (app, from, to, added/removed verbs) to the compat table. Generated by the drift event, so the table stops going stale by hand. Log deltas in `BUILD_LOG.md`.
4. **Version parsing trap.** The CLIs print at least three shapes: `cadcraft-cli 0.8.0`, `SoundCraft CLI 0.10.0`, `photocraft-cli 0.10.0 (8407d9ccb, 2026-10-18)`, and `pdfcraft-cli 0.9.0` followed by three extra lines of Discord/web/source links. Extract `(\d+)\.(\d+)\.(\d+)` into a tuple; never compare raw `--version` output, or the guard false-fires on every build hash.
5. **No vendoring:** never copy engine binaries into repos. Reference `C:\Program Files\<Craft>` via env (`PDFCRAFT_CLI`, `DEMOCRAFT_PROGRAM_FILES`). Naked-PC install = "install the Craft apps" (wrappees are the product).

## 6. Security and honesty gates

* **Root confinement:** always pass `--automation-read-root` / `--automation-write-root` (or `--root`) scoped to the job inbox/outbox. Links followed; a root left out grants nothing. Never grant Documents wholesale.
* **Outbox isolation:** hands-in (run from webapp/chat, inspect real outputs) / hands-out (never modify user Craft documents).
* **Declared degradations:** `wrappee_missing` (CLI not installed), `needs_account` (engine feature gated), `llm_down` (Ollama :11434 unreachable, brief.md skipped). No undeclared mocks; no stub verbs advertised in TOOLS.md.
* **Crossconnect discipline:** see `FLEET_CROSSCONNECT_STANDARD.md` + `FLEET_MESHING_PHILOSOPHY.md`. One hop, soft degradation. pdf-mcp does not call PhotoCraft directly; it calls PdfCraft, which may consume a WordCraft-seeded PDF.

## 7. Relation to repconv / rustification

PdfCraft *is* already the Rust core for PDF manipulation. Do not `repconv` pdf-mcp just to rewrite `combine` in Rust. If pdf-mcp is ever Rustified (Bucket A candidate), the L1 `pdf-core` keeps RAG/store/dispatch and continues to delegate render/combine/OCR/audit to the PdfCraft engine via Lanes A/B. The 70% reusable fleet kernel (`bridge.rs`, `llm.rs`, `vault.rs`, `registry.rs`) still applies; the engine boundary stays.

## 8. Cutover checklist for any `<domain>-mcp` adopting its Craft engine

* [ ] `GET /api/<domain>/craft/status` reports CLI path, `--version`, missing list.
* [ ] Headless Lane A green on golden fixtures; `wrappee_missing` path tested (rename env).
* [ ] Sidecar Lane B behind env flag with root confinement; `tools` schema **or CLI version** drift surfaces `engine_drift`.
* [ ] `docs/ONBOARDING.md` compat table updated with measured versions/dates.
* [ ] `docs/TOOLS.md` documents which ops are engine-backed vs Python-native.
* [ ] `democraft-mcp` demo for the app still passes with real artifacts.

## 9. Footprint (measured 2026-10-20, Windows 11, idle)

The small-footprint claim belongs to the **agent-facing binary**, not the GUI.

| Process | Working set | Peak | Private |
|---|---|---|---|
| `figcraft-cli mcp` | 20.9 MB | 21.3 MB | 1.2 MB |
| `gridcraft-cli mcp` | 4.3 MB | 4.8 MB | 0.8 MB |
| `photocraft-cli mcp` | 13.5 MB | 14.3 MB | 6.0 MB |
| FigCraft GUI | 280.6 MB | 287.0 MB | 423.9 MB |
| GridCraft GUI | 328.3 MB | 371.6 MB | 471.7 MB |
| PhotoCraft GUI | 267.3 MB | 270.4 MB | 411.7 MB |

A stdio MCP server is 4-21 MB, versus ~150 MB for a bundled Python FastMCP
interpreter. The GUI pays for wgpu, fonts and shared GPU memory and lands at
~270-330 MB - comparable to a mid-size Office app, not a fraction of one.

Method: start each process, wait 8 s (GUI) or 4 s (CLI) idle, read
`WorkingSet64` / `PeakWorkingSet64` / `PrivateMemorySize64`, close. One sample,
not a benchmark. Do not quote "17 MB" for the GUI; that is the CLI.
