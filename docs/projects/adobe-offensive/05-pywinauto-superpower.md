# 05 - pywinauto-mcp Is the Magical Superpower (Reversal Engine)

Repo: D:/Dev/repos/pywinauto-mcp (README title windows-computer-use-mcp).
MIT. Ports 10788 web UI + 10789 backend + stdio. Built on pywinauto (UIA/Win32).

## Why it matters for Adobe-style reversal

Thomas proves scaffolding is cheap with Opus. The bottleneck is NOT code.
It is: enumerate every control, drive every workflow, verify every pixel and file.
That is exactly what pywinauto-mcp was built for, before this hype.

Capabilities that map 1:1 to reversal:

- Window management: find/activate/maximize/position/close by title/regex/process.
- Mouse + keyboard: click/drag/type/hotkeys/app shortcuts. Sends real input, not API calls.
- UI elements: inspect via UIA/Win32, click/read/verify state. Adaptive location cascade:
  title -> auto_id -> control_id -> class -> OCR. Survives renames/reskins that kill brittle scripts.
- Visual intelligence: screenshots (full/region), OCR via Tesseract, template matching.
  Enables vision loop: edit -> snapshot -> assess -> refine (same loop gimp-mcp uses with get_state_snapshot).
- Autonomous missions: `automation_mission(run="install app, verify UI, screenshot result")`
  plans, executes, retries, verifies, reports. Exhibit A in README: 100 Tauri/NSIS installers,
  one unattended run, $2 LLM cost. That is parity-harness at scale.
- Macro record/replay: record any UI sequence, replay, verify outcomes. Workflow mining for free.
- Multi-app: chain Notepad/Calc/Paint or Photoshop/Premiere/Blender in one mission.
- Telemetry: every action to SQLite, query failure patterns by tool. Turns 2000 issues into stats.
- Safety: docs/SAFETY.md, HITL, kill switch, opt-in face recog (off default). Required before crawling third-party apps on user machines.
- Friends: autohotkey-mcp (raw input record/replay), browser-mcp (Playwright for HTML/DOM/web),
  virtualization-mcp (sandbox/VM isolation), windows-operations-mcp (registry/services/accounts).
  Rule: desktop Win32/UIA = pywinauto-mcp. Web/DOM = browser-mcp. Run both profiles side by side,
  let LLM pick target.

## Reversal loop built from existing ops (no new code to start)

1. Probe: `window list + inspect` dump of target app (e.g. Photoshop Curves dialog).
   Save UIA tree JSON + screenshot + OCR text as baseline.
2. Crawl: mission walks every menu/tab/slider, screenshots before/after, saves preset/config/file
   produced. Macro recorder stores replay.
3. Spec mine: mission output + official docs + tutorial transcripts -> SPEC.md per panel
   (inputs, outputs, shortcuts, file effects). Store under projects/adobe-offensive/specs/.
4. Reimplement: fresh Rust/Python from spec only (see 02 clean-room).
5. Verify: pywinauto drives BOTH Adobe original and Craft rebuild with same mission,
   compares screenshots (template match threshold) + file round-trip diff + UIA state.
   Logs to SQLite, publishes Prefab card + webapp Crawler/Logs tabs.
6. Regression: missions become permanent tests. See standards/rules/cua_nsis_smoke_testing.md
   and cua_webapp_testing.md. Dogfood pattern already documented: cua-nsis-certification.md
   (tool tests its own installer).

## Concrete mission sketches for Opus

- `mission: enumerate Photoshop Filter Gallery`: open app, list menus via inspect, click each filter,
  screenshot canvas delta, save PSD, record macro, emit SPEC rows.
- `mission: Premiere scopes parity`: load Charade clip (public domain), open scopes, screenshot
  vectorscope/waveform before/after Lumetri-style adjustment in both FilmCraft and Premiere,
  compute image hash distance, fail if > threshold.
- `mission: 100-installer sweep`: reuse Exhibit A pattern for all 7 Crafts x Mac/Win/Linux/Web,
  install/screenshot/verify/report unattended, file issues with screenshot + UIA dump attached.

## Limits and mitigations

- OCR/Tesseract fails on custom-drawn canvases (timeline, scopes). Mitigate with template matching
  + viewport PNG + model vision (local LLM first per LOCAL_LLM_FIRST_DOCTRINE) + human HITL confirm.
- Timing/flakiness: app launch, GPU render, HMR reload. Mitigate with retry + backoff + SQLite
  timing stats + explicit wait-for-control (not sleep).
- Admin/UAC/isolation: crawl in VM via virtualization-mcp snapshot/rollback. Never crawl
  banking/DRM/anti-cheat targets (see 04 non-targets).
- Cost: missions burn tokens. Mitigate with local LLM for plan/exec, cloud Opus only for spec synthesis.
  Track per TOOLING_COST_MODEL.

## What to build next in pywinauto-mcp (for this project)

- `spec_emit` op: UIA dump + screenshots + macro -> SPEC.md skeleton automatically.
- `diff_pair` op: run same mission on App A vs App B, return screenshot + file diff bundle.
- `suite` op: mission list as nightly gate with coverage.py semantics (distinguish looked-and-clean
  vs never-looked, per AGENT_READING_ORDER section 6).
- All with dialogic returns (success/operation/result/error/recommendations/next_steps per TOOL_DESIGN_STANDARDS).

Bottom line: anyone can prompt Opus to write a Curves dialog. Only a fleet with pywinauto-mcp
can prove it matches Photoshop on 500 cases overnight for $2. That is the moat.
