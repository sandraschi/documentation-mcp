# Fleet Development Notebook

Daily log of what was worked on, fixed, or noteworthy across the fleet.

---

## 2026-07-14

### New Repos
- **fleet-public-relations-mcp** — scaffolded (FastMCP server + Starlette REST + Vite webapp).
  - Tools: `register_thread`, `scan_threads_now`, `get_pr_dashboard`, `fleet_pr_help`, `fleet_pr_shutdown`
  - Webapp: Dashboard, Threads, Feedback, Chat, Settings + Logger/Help modals + useZoom hook
  - Dual transport (stdio + HTTP), SkillsDirectoryProvider, Prefab dashboard card, RahRah Shield spam filter
  - Ports: 11094 (backend), 11095 (frontend)

### SOP Updates
- **assfix SOP** (`patterns/repo-assess-and-fix.md`):
  - Repo type detection (Standard MCP / Container Stack / Infrastructure)
  - Git repo check, README completeness, port compliance, container stack audit
  - Error/empty/loading states check, keyboard shortcuts, Pydantic v2 patterns
  - Report persistence to `docs/assess-reports/` + `.assess-fix-timestamp`
  - Conditional `[if:]` markers so non-standard repos (games-app, myai) aren't falsely penalized

### Reference Docs
- **TOOLS_GLOSSARY.md** — 90+ entries across 12 categories (package mgrs, linters, MCP stack, web stack, backend, ML/GPU, etc.)

### meta-mcp
- **assess_reports_ops** tool (list/get/stats) — scans all fleet repos for assess-fix reports
- **Assess Reports** webapp page — KPI cards, expandable report list with scores

### Bloat Cleanup
- **database-operations-mcp**: untracked 2,057 Rust build files from `target/` + `zed-extension/target/` (855 MB → 4.74 MB)
- **Fleet-wide scan**: found 6 more repos with tracked Rust build artifacts
- **Nuclear purge**: `git filter-repo --path target/ --invert-paths` + force push on all 7 repos
  - email-mcp (419 files), gimp-mcp (812), virtualization-mcp (814), robotics-mcp (792),
    vrchat-mcp (543), obs-mcp (421)
  - ~3,800 files / ~680 MB of `.rlib`/`.fingerprint`/`.pdb` bloat eliminated from history
- **Backup script**: added `.git` directory filter to skip non-repo folders

### Daemon-Proxy Pattern
- **advanced-memory-mcp**: registered as NSSM service (HTTP daemon on 10732, auto-start)
  - opencode stdio probes daemon → lightweight proxy via `create_proxy()`, no more readonly DB errors
- **arxiv-mcp**: added daemon-proxy probe to `__main__.py`, registered NSSM service on 10770
  - `ARXIV_MCP_API_URL` env var set in opencode config for automatic proxy detection
- **aiwatcher-mcp**: already had NSSM service running HTTP daemon — confirmed correct
- **fleet-agent-mcp**: already had daemon-proxy pattern + NSSM service — confirmed correct

### New MCP Servers
- **cline-mcp** — Node.js MCP server wrapping @cline/sdk (port 11096).
  10 tools: agent_run, sessions, schedules, team coordination.
  Supports Ollama/LM Studio for local inference.
- **agy-mcp** — FastMCP server for Antigravity IDE (port 11097).
  Tools: list/read/install skills, read config.
- **zed-mcp** — FastMCP server for Zed editor (port 11098).
  Tools: read settings, list extensions, open files.

### travelprep-mcp
- `hotel_extras` tool: wired remaining 5 Booking.com/hotelzero operations (find_hotels, compare,
  check_availability, reviews, price_calendar), REST capability layer (`/api/capabilities`,
  `/api/tools`, `/api/health`), Vite/React/Tailwind webapp scaffold
- `account` tool: Booking.com trips/wishlist/rewards via an isolated Playwright profile
  (interactive one-time login, not live-Chrome cookie import) -- unverified pending a real login
- `budget.py`: hardcoded MAX_NIGHTLY_RATE_EUR=300 / MAX_TOTAL_TRIP_EUR=1500 sanity pre-check;
  no booking-execution tool exists or is planned (deliberate)
- New `reference/GREY_TOOLS.md` -- catalog of borderline-legit tools worth knowing about
  (pycookiecheat, cli-printing-press/booking-com-pp-cli, hotelzero) started from this research
