# Dependency Audit — SOP

**Trigger**: `audit deps`
**Reference macro**: `agentic_macros.md` → `audit deps`
**Scope**: Check all project dependencies for known vulnerabilities, stale versions, and fleet-incompatible licenses. Report findings — do NOT auto-upgrade.

---

## Why audit deps

Dependencies drift silently. A `>=3.4.2` pin in `pyproject.toml` was correct six months ago; today it allows a version with a known CVE. An `AGPL-3.0` license snuck in via a transitive dep. The audit finds these before they become production incidents.

**Rule**: Report, never fix. Auto-upgrading deps without testing breaks more things than it fixes. Present findings for the user to decide.

---

## Phase 1 — Python dependencies

### 1A. Security scan

Run if `pip-audit` is available:
```powershell
uv run pip-audit --require-hashes -r <(uv pip compile pyproject.toml)
```
If `pip-audit` is not installed, report: "pip-audit not found — install with `uv add --dev pip-audit` for CVE scanning."

### 1B. Freshness check

Compare key deps against latest on PyPI. These are the fleet's critical-path packages:

| Package | Minimum | Latest known | Why |
|---------|---------|-------------|-----|
| `fastmcp` | >=3.4.4 | Check PyPI | Core framework |
| `fastapi` | >=0.115 | Check PyPI | REST layer |
| `uvicorn` | >=0.32 | Check PyPI | ASGI server |
| `pydantic` | >=2.0 | Check PyPI | Data validation |
| `pydantic-settings` | >=2.0 | Check PyPI | Config management |
| `prefab-ui` | >=0.14.0 | Check PyPI | Rich in-chat UI |
| `httpx` | >=0.28 | Check PyPI | HTTP client |

For each: if pinned version is behind latest by a major or minor, flag as STALE.

### 1C. Lockfile staleness

```powershell
uv lock --check
```
If this fails, the lockfile is out of sync with `pyproject.toml`. Flag as STALE.

---

## Phase 2 — Node/JS dependencies

### 2A. Security scan

```powershell
cd webapp/
npm audit  # or bun audit
```
Report known vulnerabilities by severity. Flag CRITICAL and HIGH as blocking, MEDIUM and LOW as advisory.

### 2B. Freshness check

Check key webapp deps against latest:
- `react`, `react-dom` — latest 19.x
- `@tauri-apps/api` — latest 2.x
- `zustand` — latest 5.x
- `framer-motion` — latest 11.x
- `lucide-react` — latest 0.560+

---

## Phase 3 — License audit

Scan both Python and JS deps for fleet-incompatible licenses:

| License | Status | Notes |
|---------|--------|-------|
| MIT, Apache-2.0, BSD-2/3 | ✅ Allowed | Standard permissive |
| LGPL-2.1/3.0 | ✅ Allowed | Static linking OK |
| MPL-2.0 | ✅ Allowed | File-level copyleft |
| **AGPL-3.0** | ❌ **Flag** | Network copyleft — requires review |
| **GPL-2.0/3.0** | ⚠️ **Flag** | Requires review if not already approved |
| **SSPL, BUSL, custom** | ❌ **Block** | Source-available / non-OSI |

For Python: `uv run pip-licenses --format=json` (if available).
For JS: `npx license-checker --summary` (if available).

Report any flagged licenses with the package name, version, and a link to the license text.

---

## Phase 4 — Report

Format as a structured report:

```
=== Dependency Audit: {repo} ===

Python:
  Security: 0 critical, 0 high, 2 medium (pip-audit)
  Stale: fastapi 0.115.0 → 0.116.3 available (minor)
  Lockfile: up to date

Webapp:
  Security: 0 critical, 1 high (npm audit)
  Stale: zustand 4.5.0 → 5.0.0 available (major)

Licenses: all MIT/Apache-2.0 — clean

Recommendations:
1. Upgrade fastapi to 0.116.3 (minor — safe)
2. Review npm high-severity advisory ADVISORY-2026-001
3. Upgrade zustand to 5.x (major — requires migration)
```

**Do NOT make any changes.** Present the report and let the user decide.

## Phase 5 — Persist report

Write the dependency audit to `reports/deps-{YYYY-MM-DD}.md` in the repo root:

```powershell
$reportDir = Join-Path $RepoRoot "reports"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$reportPath = Join-Path $reportDir "deps-$(Get-Date -Format 'yyyy-MM-dd').md"
Set-Content -Path $reportPath -Value $reportText
```

Also write `.deps-timestamp` at the repo root (committed) with a CVE summary:

```powershell
@{ timestamp = (Get-Date -Format "o"); critical = $critCount; high = $highCount; stale = $staleCount; license_flags = $licenseCount } | ConvertTo-Json | Set-Content ".deps-timestamp"
```

The `reports/` directory MUST be in `.gitignore`. Check before writing.
