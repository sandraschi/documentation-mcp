# sandraschi.com — fleet ops console (built 2026-10-25)

Collaborator-only ops console + fleet showcase in one static-ish site. The
vision doc below it was written the same morning as a "build LATER" parking
lot — the build happened that afternoon. Vision kept for the parts that are
still parked (pitch pages, public boundary); everything else here describes
what is live.

**Red line (unchanged):** collaborator-only surface. No public hosting, no
custom domain (`sandraschi.com` resolves nowhere — internal name only).
Session logs, digests and triage receipts assume a private audience. There
is no auth on the site; the trust boundary is the tailnet + who gets the URL.

## What it is

- **Site:** `D:\Dev\repos\sandraschi-com\webapp` (React + Vite + Tailwind,
  fleet webapp standard minus the backend). Not a git repo — no commits.
- **Model:** static snapshot, no live API calls from the browser. The site
  fetches `/data/*.json` at runtime and re-polls every 60s (+ on tab focus),
  so a snapshot refresh propagates with no rebuild. `src/data/` holds the
  build-time fallback for first paint.
- **Live URLs (tailnet):** `http://100.118.171.110:4173` (plain HTTP —
  everything except the camera page) and
  `https://goliath.<tailnet>.ts.net:4443/` (TLS via tailscale serve —
  required for camera/GPS permission prompts in mobile Safari).

## Data pipeline

`webapp/scripts/snapshot.ps1` (gh queries, raw passthrough) +
`webapp/scripts/snapshot_db.py` (stdlib Python: sqlite, markdown, REST —
never writes to sources). Dual-writes every feed to `src/data/` and
`public/data/`. Runs every 30 min via task `sandraschi-com-snapshot`
(next: `scripts/register-snapshot-task.ps1`).

| Feed file | Source | Cadence |
|---|---|---|
| `snapshot.json` | gh needs-sandra/author PRs + session logs | 30 min |
| `gh-issues.json` / `gh-prs.json` / `gh-merged.json` | fleet-wide `gh search` (raw stdout, see gotcha) | 30 min |
| `digest-history.json` / `top-items.json` | aiwatcher.db (read-only) | 30 min |
| `daily-ops.json` | morning-digest.md, wip-sweep, naked-test RESULTs, Fritz/AIWatcher logs, Discord REST, `docker ps`, devices-mcp, memops, qgiscraft, schtasks, voice registry | 30 min |
| `fleet-inventory.json` | fleet-registry.json + local git tags + assess reports + signals CSV + gh counts | 30 min |
| `docs-index.json` | curated mcd walk (standards/operations/patterns/troubleshooting/handovers, 600 docs, no session logs) | 30 min |
| `history.jsonl` / `history.json` | rollup appended per day (deduped) | daily |

**PS 5.1 gotcha (2026-10-25, cost ~1h):** `ConvertFrom-Json` on a large
top-level array returns a single `{"value":[...]}` wrapper instead of N
rows under Windows PowerShell 5.1 (fine in pwsh 7). Rule: snapshot.ps1 must
NEVER parse big gh payloads — it passes raw stdout to files and Python does
all parsing. The safe 5.1 pattern is assign-then-wrap
(`$p = $raw | ConvertFrom-Json; @($p)`), never `@($raw | C-F-J)` inline.

## Pages (12)

| Route | Purpose | Key data |
|---|---|---|
| `/` Today | daily ops: pipeline strip, sweep bars, test donut, trends, merged, discussions, Discord, sweep, Fritz, AIWatcher | daily-ops, history |
| `/queue` | review queue: search, label filter, sort, stale toggle | snapshot |
| `/chat` | keyword-ranked fleet search (repos, issues, PRs, memory, docs, infra) + mermaid link graphs; memops status | inventory + gh/docs indexes |
| `/fleet` | 239-repo inventory: grade, assfix, release, issues, PRs, histograms | fleet-inventory |
| `/mesh` | crossconnect hub graph + voice-bus roster | inventory, voice |
| `/infra` | docker stack (45), Goliath headroom, gitops status, task table, feed freshness | daily-ops |
| `/map` | Leaflet map of qgiscraft layers (58 Overpass points, Vienna) | gis |
| `/viewer` | procedural demo bot + client-side STL/OBJ/PLY inspector (point clouds) | none (local files) |
| `/phone` | iPhone cam/GPS/IMU in Safari — rear/front camera + snapshots, GPS fix, motion readout | none (live sensors) |
| `/home` | devices-mcp: 17 devices, Hue rooms, console links | devices |
| `/activity` | session-log timeline | snapshot |
| `/morning` | digest archive + hot items | digest-history, top-items |

Global: VoiceBar (mic commands → routes/refresh/read-aloud via Web Speech
API, no backend), live/static badge, 60s auto-refresh, 15px base type with
zinc-300 floor (accessibility pass 2026-10-25).

## External connections (all read-only, best-effort, never fatal)

- **memops** (`:10705`): projects + recent memory entries, searchable in chat.
- **gitops** (`:10713` backend up, breakfast `:10714` down as of 2026-10-25):
  status card on Infra; digest markdown remains the data source.
- **Discord**: live via bot token from `discord-mcp/.env` (runtime only,
  never logged) — #fleet-overview on Today. No token/DOWN → honest empty card.
- **Docker**: `docker ps --format json` parsed in-process (no creds).
  2026-10-25: 45 containers, authentik ×2 unhealthy, disk 96%.
- **devices-mcp** (`:10717`): health, device census, Hue rooms, climate demo flag.
- **qgiscraft** (`:11254`): layer catalog + `/api/features` points. There is
  no `qgis-mcp` repo — the GIS backend is qgiscraft.
- **Voice bus**: roster parsed from `config/voice_command_bus.yaml`
  (wake words, default entity fritz, 9 receivers incl. japanophile caveat).

## Tailscale serve/funnel map (2026-10-25)

`goliath.<tailnet>.ts.net`, MagicDNS + funnel on :443, serve entries tailnet-only:

| Path / port | Target | Scope |
|---|---|---|
| `/` (:443) | 127.0.0.1:11157 | **public funnel** (pre-existing — do not touch) |
| `/games/` | :11158 | public funnel (pre-existing) |
| `/intel/` | :11027 | public funnel (pre-existing) |
| `/multigpu/` | :11136 | public funnel (pre-existing) |
| `/` (:4443) | 127.0.0.1:4173 sandraschi.com | **tailnet-only serve** (new) |

**Incident 2026-10-25:** a bare `tailscale serve --bg 4173` silently removed
the whole public funnel (no confirmation). Restored all four paths with
`tailscale funnel --bg --set-path=<path> --yes <port>` and verified. Lessons:
serve + funnel share one path table; serve edits drop the funnel flag, so
always re-run the funnel commands after any serve change (the fleet helper
`scripts/setup-funnel-routes.ps1` does both halves; prerequisites must be
RUNNING first or the mounts 502).

**Incident 2026-10-25, part 2 — /games/ was a stale shortcut.** First fix
pointed funnel `/games/` at the vite dev server (:10986), which 403s on the
funnel Host header. Canonical design (TailscaleFunnel.md §5b): a stdlib
path-strip proxy on :11158 (`scripts/start-funnel-path-proxy.ps1`, no Vite
needed — backend :10987 serves SPA+API on one port). Restored that, reverted
an unneeded `allowedHosts` experiment in the games repo (tree pristine),
started the landing server (`start-funnel-landing.ps1` runs forever by
design — launch it in its own window, never awaited), reverified all three
public paths 200. Still down from before, untouched: `/multigpu/` (playbook
has no `build/` output — needs a Docusaurus build + static serve on :11136).
Still open: which game backend, if any, was ever on :11157-adjacent ports is
moot — `/` is the static landing page by design.

**Incident 2026-10-25, part 3 — game cards did nothing.** Symptom: `/games/`
loaded, clicking a game card went nowhere. Cause chain, each verified:
1. The proxy was stripping the mount a second time (tailscaled already
   strips). Proof: `/games/games/games/board-games/chess.html` = 200 through
   the funnel, 404 direct on the proxy. Fix: `-NoStrip`.
2. Game pages mix relative and root-absolute refs. Under the mount, relative
   sibling refs work (single strip lands on the real path) but root-absolute
   `/js/x` escapes the mount and hits the landing page. Fix: the proxy gained
   `--rewrite-prefix`, splitting rules by content type (html attributes vs
   code literals) — applying both to one HTML file double-prefixed everything
   (`/games/games/js/x`), which was its own hour of confusion.
3. Root-level relative assets (`styles.css`, icons, manifest) on nested pages
   needed prefixing; sibling css (`css/chess.css`) must not be — hence a
   whitelist rather than a generic `*.css` rule.
Verified: 12 pages across 6 categories, 217 refs, 0 failures; all three
public paths 200. The games repo is untouched (my one speculative edit there
was reverted; tree pristine).
Known gap, not fixed: AI moves. `js/api-config.js` calls engines on
`:11211/:11212/:11213` directly and the funnel exposes none of those, so pages
load and play-vs-AI fails off-host. Needs a gateway engine proxy
(`/api/engine/<name>/*`) + api-config using it when `!isLocal`.
funnel is per-name:port (the whole :443 goes public together — never put the
console on `/` of :443), and `serve` + `funnel` share one path table, so
always `serve status` before touching either. The LAN preview task serves the
console; vite `preview.allowedHosts` must list the tailnet name or every page
is a 403 (found via curl Host-header probe).

## iPhone / iPad access

Requirements: Tailscale app connected (same tailnet), Safari, the URLs above.
Use the `:4443` https URL for anything needing permissions (camera/GPS/motion
require a secure context — plain-http tailnet IP blocks `getUserMedia`
silently). `/phone` is the sensor page: rear/front camera + JPEG snapshots,
one-shot GPS fix with OSM link, live IMU after the iOS motion prompt. Limits:
sensing only works with the page open and the phone awake — no background
tracking. For that (no Xcode): Sensor Logger app (IMU streaming), Traccar
Client + a traccar container (GPS history), IP-camera app → devices-mcp
(camera tile on Home), Shortcuts → POST to fleet endpoints. A native Swift
app is only justified for always-on capture, ARKit/LiDAR, BLE peripheral or
push — free sideloading expires every 7 days (AltStore refreshes), paid is
$99/yr.

## Fleet-nightly-gate repair (2026-10-25, exit 1 → partial green)

Fixed + committed: E3 cross-ref (`opencode-plugins/README.md` ↔
`rust-crates/README.md`, mcd d07882fa); `mcp-federation-hub` root start.ps1
ran a nonexistent module — replaced with the canonical fleet shim
(federation-hub 9b2de50); start-integrity 4 remaining NEW verified benign
(etherpad/plex ports match config, norirobotics code defaults match,
qgiscraft Rust ArtCraft needs no PS shim) and accepted via the gate's own
`--update-baseline` ratchet; pywinauto backend revived (NSSM service was
disabled → set demand + started, `/api/v1/health` 200).
Verified green: standards-audit (0 NEW), start-integrity (exit 0),
pywinauto probe UP.

Still red, correctly so (do not baseline these away):
- **health-probe:** kyutai/openmanus/sysinternals/vrchat backends down (no
  services; they die overnight while vite frontends persist), gazebo zombie
  python since 10-23 holding :10991. Decision needed: service-manage fleet
  backends (RAM 81% — capacity question) or accept IDLE.
- **heartbeat → install-matrix:** 08:04 run exit 1, 46/46 naked tests
  FINISHED-not-clean (23 harness, 21 start, 2 just-list). The Windows Sandbox
  harness is systemically broken (Session-0/wedge/boot failures) — needs a
  virtualization-mcp harness sprint, not gate config.
- **smoke:** dark-app-factory + leanforge-mcp hang on cold start (leanforge
  has no node_modules), vroidstudio frontend never ready in 125s. Per-repo
  cold-start debugging outstanding.
- Smell for gate maintainers: the canonical PS shim itself assigns `$args`
  (email-mcp start.ps1:130) against the fleet's own automatic-variable rule —
  renaming it would rehash 61 repos, so left alone.

## Open items / deliberately not done

- `sandraschi-com-snapshot` task registered (30 min) but first scheduled run
  pending verification; `sandraschi-com-lan` (logon) running, verified 200 on
  :4443 — no reboot survival test yet.
- gitops breakfast `:10714` down (nobody runs the frontend) — digest markdown
  covers the data; restarting it is a one-liner when wanted.
- install-matrix result `0x3` on the 02:30 run vs exit-1 beat at 08:04:
  two different runs; the 0x3 was the Session-0 refusal path, superseded.
- webapp `dist/` is served, not committed; `*.bak` files accumulate next to
  edited sources (fleet gitignore pattern covers repos; sandraschi-com has
  no git).
- Pitch pages (why-fleet, catalog, books) from the original vision are still
  parked — ops console came first by request.

## Original vision (2026-10-25 morning, kept for the parked parts)

One beautiful website: the pitch (why-fleet, catalog, books, rustification)
for strangers, and the ops console for Sandra + collaborators — with a
publish boundary enforced in the feed renderer (`publish: true/false`
frontmatter defaulting FALSE; renderer drops non-publishable entries, no
redacted placeholders). Still valid for whenever the pitch pages get built.
Phasing from the morning (runt cleanup → feed inventory → static build →
remaining pages → cron) executed same-day, ops-first: review queue, fleet,
activity, morning archive all live; landing/pitch still parked.

## iPad field report 2026-10-25 (ports, funnel, tailnet)

Symptoms from iPad 9th gen (online on tailnet): funnel `/intel/` loads a login
page, funnel `/games/` and tailnet `:4443` hang.

Findings (all verified from Goliath, no guessing):
- `AllowFunnel: {"goliath.<tailnet>.ts.net:443": true}` — funnel is
  **per-name:port**, not per-path. Anything served on :443 is public; anything
  tailnet-only must live on another port (:4443) or another name. This is why
  the console went to :4443 instead of a :443 subpath.
- Tailnet ACLs are wide open for Goliath (netmap filter: all tailnet nodes →
  Goliath all ports 0-65535, TCP+UDP). A hang is never the ACL here.
- `/intel/` → 127.0.0.1:11027 answers **401, no body** — live auth-walled app,
  working as designed. (Local plain-HTTP curl also gets the 401; earlier
  "FAIL" readings were the 5.1 error-formatting quirk, not dead ports.)
- `/games/` → 502 and `/` → 502: **backends down, connection refused.**
  Nothing listens on 11157/11158/10900; no game server processes, services,
  tasks, or installs found (Steam client only; `D:\Server` is the *arr media
  configs; `C:\games-mcp` is an MCP server project, unrelated). The game
  backend needs identifying (which game, how is it normally started?) before
  it can be revived and autostarted.
- `:4443` tailnet-only serve: backend up, TLS valid, `curl` from Goliath via
  the tailnet name → 200. iPad hang with open ACLs means either the iPad's
  tailnet data path is down (funnel paths are PUBLIC — they prove internet,
  not tailnet) or something port-specific. Decisive 20-second test on the
  iPad: open `http://100.118.171.110:4173` — loads ⇒ tailnet fine, :4443 is
  port-specific (report back, options ready); hangs ⇒ toggle Tailscale
  off/on in the iOS app and check login/expiry, then :4443 works unchanged.
- vite `preview.allowedHosts` must list the tailnet name or every page is a
  403 (found via Host-header curl probe; fixed in `vite.config.ts`).
