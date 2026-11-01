# GitHub fleet maintainer heartbeat (PRs & issues)

**Status:** Fleet pattern · **Last updated:** 2026-06-05  
**Audience:** Maintainers of multiple small repos; **robofang** / **OpenManus** / **OpenClaw** operators; **git-github-mcp** users  

---

## Problem

Silence on open PRs and issues reads as indifference. Solo maintainers often **do not notice** activity until it is late. **MCP servers do not run cron** — something **outside** the server must trigger periodic checks.

---

## Tooling (canonical)

| Piece | Role |
|-------|------|
| **[git-github-mcp](https://github.com/sandraschi/git-github-mcp)** | **`github_ops`** — `pr_list`, `issue_list`, `pr_comment`, `issue_comment`, etc. (`gh` CLI under the hood). |
| **`fleet_morning_digest`** | **Breakfast runner** — fleet PR/issue scan + stale flags + notifications since last run. CLI: `scripts/run_morning_digest.py`; schedule: `scripts/install_morning_task.ps1`. |
| **`fleet_ops`** | **Full maintainer toolkit** — `registry_load`, `port_audit`, `docs_gate`, `ci_pulse`, `dependabot_digest`, `ack_drafts`, `local_dirty`, `release_drift`, `grade_snapshot`, etc. Use **`full_suite`** for one-shot morning + all checks. HTTP: `POST /api/fleet-suite`; web: **`/breakfast`**. |
| **Web inbox** | With the app running, **`/inbox`** — combined PR/issue view, optional **fleet** mode (many `owner/repo` lines), stale hints. Backend default **10702** (see [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)). |
| **Supervisor / orchestrator** | **OpenClaw**, **OpenManus**, **robofang** Hub, **OpenClaude**, or any **scheduled agent** that can invoke MCP tools on a **daily** (or weekly) cadence. |

---

## Standard daily job

**Automated (preferred):**

```powershell
cd D:\Dev\repos\git-github-mcp
copy config\fleet-repos.example.txt config\fleet-repos.txt
.\scripts\install_morning_task.ps1   # daily 07:00, deliver file + aiwatcher
```

**MCP / agent (digest only):**

```
fleet_morning_digest(
  fleet_repos_file="D:/Dev/repos/git-github-mcp/config/fleet-repos.txt",
  stale_days=7,
  deliver="file,aiwatcher"
)
```

**MCP / agent (full suite):**

```
fleet_ops(
  operation="full_suite",
  use_registry=true,
  stale_days=7,
  deliver="file,aiwatcher"
)
```

**Manual agent prompt sketch:**  
*“Using `github_ops`, list open PRs for each repo in our fleet list; flag items with no maintainer activity in 7+ days; draft a polite acknowledgment comment for each.”*

---

## What the breakfast runner does

1. For each `owner/repo` in the fleet list: `pr_list` + `issue_list` (open).
2. Flags **stale** threads (default ≥7 days; heuristic on comment count + `updatedAt`).
3. Fetches **GitHub notifications** since the previous successful run (`gh api /notifications`).
4. Writes markdown digest + optional delivery:
   - **file** — `%LOCALAPPDATA%\git-github-mcp\morning-digest.md`
   - **aiwatcher** — `POST http://127.0.0.1:10946/api/fleet/ingest`
   - **robofang** — bridge pulse check (council can read file / aiwatcher)

---

## Where the schedule lives

| Approach | Notes |
|----------|--------|
| **Windows Task Scheduler** | `git-github-mcp/scripts/install_morning_task.ps1` — canonical for Sandra's desktop fleet. |
| **Supervisor heartbeat** | Fits **robofang** “council” or Hub **scheduled workflows** — call `fleet_morning_digest` MCP tool. |
| **CI (GitHub Actions)** | `on: schedule` in a **private** workflow that only **notifies** (Slack/email) or opens a **tracking issue** — avoid noisy auto-comments unless you accept the tradeoff. |
| **Manual** | Open **`/inbox`** once a week — still better than never. |

---

## Related

- [GITHUB_CLI_CURSOR_PATH.md](../operations/GITHUB_CLI_CURSOR_PATH.md) — `gh` paths, `github_ops` topics note  
- [AGENTIC_MESH_ROBOFANG_INTEGRATION.md](../architecture/AGENTIC_MESH_ROBOFANG_INTEGRATION.md) — maintainer council hook  
- Upstream **git-github-mcp** README — maintainer triage, **`/inbox`**, `fleet_morning_digest`  

---

*Tags: #github #fleet #maintainer #robofang #git-github-mcp #breakfast*
