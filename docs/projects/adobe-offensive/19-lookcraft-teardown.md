# 19 - LookCraft Teardown: Mailspring (source-read) + new Outlook (web-app)

Date: 2026-10-14. Method: `12-artcraft-ux-teardown.md`. Mailspring via repo
source read (UI + Mailspring-Sync READMEs, component tree — observed, not
inferred). New Outlook via public docs + reporting (marked where inferred).
Feeds `18-lookcraft-prd.md` §6 and settles scaffold decisions.

## 1. Mailspring architecture (the thing worth stealing is the SHAPE)

Two processes, clean split, both GPLv3:

- **mailsync** (C++/Mailcore2, repo `Foundry376/Mailspring-Sync`): one process
  PER ACCOUNT, CLI-runnable standalone (`stdin` account args — testable without
  any UI). stdout = newline-delimited JSON object changes; stdin = JSON tasks.
  Tasks split local-op (applies instantly, reactive UI updates) + remote-op
  (queued in sqlite, retried). Kill-safe by construction: everything in sqlite
  transactions, quit = force-kill. This is EXACTLY the `lookcraft-cli sync`
  shape from 18 §5 — steal the protocol (JSONL over stdio), not the code.
- **Sync algorithm**: two threads, two IMAP connections. Background worker
  sweeps folders (CONDSTORE/XYZRESYNC when available, else UID-window local or
  deep sync). Foreground worker IDLEs the primary folder + fetches bodies
  on demand. Steal the shape; melib already knows these verbs.
- **Store**: sqlite "fat rows" (full JSON blob + queryable columns; migrations
  only for new columns). 3-month body window, headers-only beyond; header-hash
  stable IDs; metadata sidecar thread. Weak spots (do NOT copy): fat rows make
  SCAN slow (their own retrospective admits it — index properly from day one,
  tantivy decision in 18 §12); stable-ID hash collisions silently drop mail
  (content-hash + UID pair instead); Gmail virtual-folder handling is
  special-cased (X-GM-LABELS) — generalise labels as first-class from day one.
- **UI** (TS + Electron + React, Flux observable queries, CSS themes, plugin
  arch via `injected-component-*`): component inventory that maps 1:1 onto an
  Outlook copy — `nav-rail`, `multiselect-list` + `multiselect-toolbar`,
  `tokenizing-text-field` (To: chips), `composer-editor`, `lazy-rendered-list`,
  `swipe-container`, `mini-month-view`, `syncing-list-state`,
  `empty-list-state`. The plugin points (`injected-component-set`) are the
  contributor funnel made concrete — copy the MECHANISM for the AI-harness era
  (an MCP tool is a plugin that never needs a UI review).

## 2. New Outlook (web app in a WebView2 shell)

Observed via docs/reporting: WebView2 (Edge Chromium) wrapper over the
Outlook-web experience; installable as PWA from Edge (Microsoft documents the
flow). Office add-ins are Fluent UI React (Microsoft docs) — the chrome
vocabulary (command bars, nav, tokens) is open source even if the app is not.
Inference (marked): the new-Outlook IA is the classic Outlook tri-pane
(folder tree | message list | reading pane) with the M365 app-bar rail —
that rail (Mail/Calendar/People/To-Do) IS the two-tier nav from 12 §2
(global rail moves between tools; each tool owns its menus). Teardown rule
carried over: **the rail is the product** — copy its order, icons, and
responsive collapse; everything else is content.

## 3. Verb split for mail (12 §2 applied)

ArtCraft: Create (nothing yet) vs Studio (have something). Mail equivalent:
**TRIAGE** (something arrived — decide fast: archive/snooze/reply/delegate)
vs **FILE** (find it again later) vs **SEND** (compose from nothing).
Mailspring's feature list sorts itself: Unified Inbox + Snooze + Mail Rules +
Templates = triage accelerators; search/labels = file; composer + send-later =
send. R1 chrome is three modes, not forty menu items. Mailspring Pro (link
tracking, read receipts, analytics, contact profiles) stays OUT of R1-R2 —
all client-side per their README, all skippable, none load-bearing.

## 4. Scaffold decisions this teardown settles (18 §12)

- **Sync core**: melib (Mailspring-shape protocol: JSONL tasks/changes over
  stdio, one worker per account, local-op-first). Do NOT write an IMAP engine.
- **Store**: sqlite + proper indexes from day one (Mailspring's fat-row regret
  is free advice); tantivy only if sqlite-FTS measures slow on 100k messages.
- **Shell**: webview (Tauri) over egui — the copy target is a web app and the
  theme system is CSS; egui would re-derive every token by hand. Revisit only
  if WebView2 proves unshippable.
- **CLI-first**: `lookcraft-cli sync` must run headless before any pixel
  exists (mailsync ran on a command line; so do we).
- **Round-trip corpus from R1**: `lookcraft-corpus` starts with EML fixtures;
  PST fixtures join at R2 (gridcraft-corpus pattern).

## 5. Do-not-copy list

Mailspring: fat-row scans, hash-only stable IDs, Gmail special-casing,
Electron (ship weight), metadata-via-vendor-cloud (keep metadata local —
privacy posture is a differentiator, cf. FairEmail). New Outlook: WebView2
as an excuse for no offline story (local-first is OUR wedge); M365 upsell
chrome in app nav (same complaint as 12 §2 RESOURCES links).
