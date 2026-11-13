# Back-office craft suite: egui plan (Tier 2)

Date: 2026-11-09. Status: plan, nothing built yet. Scope: all nine suite apps
(buchcraft, taskcraft, teamcraft, assetcraft, contractcraft, deskcraft,
gaincraft, formcraft, wikicraft).

## Goals (from Sandra)

1. A native egui window for every suite app.
2. Beautiful, including a proper kanban.
3. All aspects shown, every task doable from the window, every bus signal visible or sendable.
4. Where an app replaces a known product, the window follows that product's layout and workflow so users can move over without retraining.
5. Highly functional, not a demo skin.

## Ground rules

- **Same code path.** Every window action builds a `Command` and calls the same `dispatch` as CLI and MCP (as buchcraft-app does today). No business logic in the UI crate.
- **"Looks like X" means layout and workflow, not brand.** Same panel placement, same names for the same concepts, same keyboard habits. No logos, product names, icons or brand colours of the original; own visual identity from the shared theme.
- **Plain egui/eframe 0.37 from crates.io** (as buchcraft-app). Not the storytold fork used by craft-deck.
- **Zero-panic lints apply to the app crate too.** DE/EN text from day one (craft-biz i18n).

## 1. Shared kit: `craft-biz-ui` (new crate in the craft-biz repo)

One kit so nine apps look like one suite and fixes land once.

| Part | What it does |
|---|---|
| Theme | Design tokens (spacing, radii, type scale, light/dark), semantic colours (ok / warn / danger / info, band green/yellow/red), Inter-like UI font, tabular figures for money. |
| Shell | Left nav rail + top bar (search, command palette, sync/bus badge) + main area + collapsible right detail panel + status bar. Window size and position persisted. |
| Kanban | Columns from a state machine, drag and drop between allowed transitions only (forbidden drops show why), WIP limits, swimlanes (assignee, priority, epic), quick filters, collapsed columns, card density setting, keyboard moves (arrows + Shift+arrows), undo of the last move. |
| DataTable | Sort, multi-filter chips, column chooser, saved views, virtual scrolling for 10k+ rows, inline edit where the tool allows it, CSV export of the current view. |
| Detail panel | Fields with inline edit, tabs (details, activity, links), history feed with actor. |
| Command palette (Ctrl+K) | Lists every MCP tool of the app with its description; picking one opens a form generated from the tool's `inputSchema`. This is the guarantee that every task is doable even before a purpose-built screen exists. |
| Signals dock | Bus view for this app: incoming pending (apply one / drain all), applied, rejected with reason (retry), outgoing events this app emitted and whether the target acked or rejected them. Badge in the top bar. Plus "send" buttons where the app emits (escalate, emit signals, deadlines). |
| Charts | Sparklines, bars, timelines, calendar month/week (egui_plot where it fits). |
| Feedback | Toasts for results, confirm dialog for irreversible steps (book, seal, execute, close week), inline validation messages straight from core errors. |
| Files | Native file dialogs (rfd), always passed through `Confinement`. |

## 2. Per-app windows

| App | Moves users from | Window |
|---|---|---|
| buchcraft | lexoffice / sevDesk / BMD | Exists (v0.2.0). Re-home onto the kit. Dashboard (cash, open items, UVA due), receipts inbox with preview, journal table, booking dialog with EKR search, UVA / annual views, bus drafts from assetcraft with approve. |
| taskcraft | Jira | The kanban flagship. Board (columns = workflow, swimlanes, quick filters, WIP), Backlog (ranked list, drag to sprint), issue view (description left, fields right: status, assignee, priority, labels, links), Ctrl+K, "C" to create, capacity per week from teamcraft shown above the board. Git sync status. |
| deskcraft | Zendesk / Freshdesk | Views sidebar (my open, unassigned, urgent, pending, breaching SLA), ticket table with SLA badges, ticket page: conversation thread centre, properties right (status, priority, assignee, tags), reply composer with macro picker, draft list, escalate button, "unhappy" signal list with emit. Optional board view by status. |
| gaincraft | Gainsight / ChurnZero | Accounts table with band, score, sparkline, ARR, CTAs; Customer 360 (scorecard with the four components, trend, signals timeline, contract dates, triage with reason); CTA cockpit as list and kanban (open / in work / done), renewals timeline, CSV import wizard with header check preview, weights editor. |
| contractcraft | Juro / DocuSign CLM | Pipeline kanban by status (draft, review, signature, executed), contract page with text, versions and redline diff, risk findings with clause highlights, seal and verify, terms form, deadline calendar, template gallery. |
| teamcraft | Personio / Clockodo | People directory, week timesheet grid (AZG warnings inline, week lock), absence calendar (team month view, half days), leave requests and balances, KV check, capacity per week (emits to taskcraft). |
| assetcraft | Snipe-IT | Asset table with status pills, asset page (details, assignment history, depreciation schedule chart, documents), check-out / check-in, QR label sheet preview and print/export, depreciation run with buchcraft events. Status board view. |
| formcraft | Typeform / Google Forms | Builder (question list left, preview right, logic), share/local server settings, responses table, per-question summary charts, negative responses sent to gaincraft. Built together with its Tier 1. |
| wikicraft | Confluence / Notion | Space and page tree left, page view with rendered markdown, editor with live preview, backlinks, page history and diff, search. Built together with its Tier 1. |

## 3. "Nothing missing" checks (new gate 7)

1. **Tool coverage test** per app: a table in the app crate maps every tool name from `tools()` to at least one purpose-built UI entry point. A new tool without a UI entry fails the build. The palette is the fallback, not the excuse.
2. **Bus coverage test:** every event kind the app emits or consumes appears in the Signals dock.
3. **Headless flow tests** with egui_kittest: the main jobs from each PRD clicked through on an in-memory database (e.g. taskcraft: create issue, drag to In Progress, blocked drop shows the reason; gaincraft: drain inbox, open red account, resolve CTA).
4. **Snapshots:** PNGs of every main screen, light and dark, at 1280x800 and at 150% scale, attached to the commit message notes and sent for review.
5. Startup under 1 s with a demo database; no panics; DE and EN complete.

Gates per app become: clippy, tests (incl. coverage + kittest), fmt, MCP probe, clean git, docs, **GUI coverage and snapshot review**.

## 4. Order and timeline (AI-assisted, working days)

| Step | Work | Days |
|---|---|---|
| 1 | craft-biz-ui kit (theme, shell, table, detail, palette with schema forms, signals dock, kanban) + kittest harness; buchcraft re-homed as pilot | 2.5 |
| 2 | taskcraft (Jira board, backlog, issue view) | 2 |
| 3 | deskcraft (Zendesk layout) | 1.5 |
| 4 | gaincraft (360 + cockpit) | 1.5 |
| 5 | contractcraft (pipeline, redline) | 1.5 |
| 6 | teamcraft (timesheet grid, absence calendar) | 1.5 |
| 7 | assetcraft (Snipe-IT layout, labels) | 1 |
| 8 | formcraft Tier 1 + window | 2.5 |
| 9 | wikicraft Tier 1 + window | 2.5 |
|   | **Total** | **about 16-17** |

Each step ends with gates green, a commit per repo, snapshots sent, and the mcd page updated.

## 5. Risks

- Kanban drag and drop in egui is hand-built (no off-the-shelf widget). It gets its own kittest tests for allowed and forbidden drops.
- Some screens need read queries the cores do not expose yet (e.g. a board-shaped issue list). Those are added to core as tools first, so MCP gains them too.
- Text editing of long documents (wikicraft, contractcraft) in egui is adequate, not Word-grade.
- Printing QR labels goes via PDF/PNG export, not a native print dialog.
