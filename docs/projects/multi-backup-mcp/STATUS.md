# Multi-Backup MCP — Project Status

**Last Updated**: 2026-06-15
**Repo**: `D:\Dev\repos\multi-backup-mcp` | [GitHub](https://github.com/sandraschi/multi-backup-mcp)
**Version**: v0.6.0-dev (Unreleased)
**Python**: 3.12+ | **Build**: uv + pyproject.toml
**Status**: 🟢 PRODUCTION READY

---

## What It Is

A FastMCP server providing two-tier backup via MCP tools with a React dashboard.

**Tier 1 — Hasleo Backup Suite** (disk-level):
- System/partition images via `BackupCmdUI.exe` CLI (v5.6.2.0)
- Full, incremental, differential backups
- Image verification, mount/unmount
- 2 configured tasks: System Backup + File Backup

**Tier 2 — Repo Archival** (code-level):
- Git-tracked source & docs only (via `git ls-files`)
- SHA256 deduplication (skips identical backups)
- 3-destination distribution: Desktop, N: drive, OneDrive (per-repo subdirs)
- Retry logic with exponential backoff
- Nuclear backup (batch all repos)

---

## Architecture

```
MCP Tools ──┬──► backup_tools.py ──► BackupCmdUI.exe (Hasleo system images)
            │
            └──► repo_tools.py ──► archive_utils.py (git ls-files, SHA256 dedup, 3 dests)

REST API ───┬──► /api/backups/* ──► Hasleo CLI
            └──► /api/repos/*   ──► archive_utils.py
```

---

## Current State (v0.6.0-dev)

### What Works

| Feature | Status | Notes |
|---------|--------|-------|
| **Hasleo CLI** | Working | v5.6.2.0, list tasks + run by GUID |
| **Hasleo tasks** | 2 configured | System Backup + File Backup |
| **Hasleo verify/mount** | Working | Image integrity + virtual drive |
| git ls-files backup | Working | Tracked source & docs only |
| SHA256 deduplication | Working | Skips identical ZIPs per destination |
| 3 destinations | Working | Desktop + N: + OneDrive |
| Per-repo subdirectories | Working | `{dest}/{repo_name}/` |
| Retry with backoff | Working | 3 retries, doubling delay |
| Dry-run mode | Working | Returns file count + dest preview |
| Repository scanning | Working | Excludes junk/external/hidden |
| Nuclear backup | Working | All repos, reports skipped count |
| Webapp Repos page | Working | Archive button, Heavy toggle, backup history |
| CI (GitHub Actions) | Working | Windows-only: ruff lint + format + pytest |
| Ruff green | Working | Zero lint errors |
| No gaslighting | Fixed | All mocks/fakes removed or replaced with 501 |

### What's Dead / Deprecated

| Component | Status | Notes |
|-----------|--------|-------|
| `sota_tools.py` | Deprecated | Stub pointing to repo_tools |
| `integrations.py` (Claude) | 501 | Never implemented, now honest |
| `backup_service._simulate_backup` | Removed | Was faking progress on a working CLI |
| `backup_service.py` (service layer) | Import error | `MCPRuntimeError` not exported; Hasleo tools work via `backup_tools.py` directly |

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| Frontend | 10798 | Active |
| Backend | 10799 | Active |

---

## CI

```yaml
# .github/workflows/ci.yml — Windows-only
- ruff check src/ tests/
- ruff format --check src/ tests/
- pytest tests/ -q --tb=short
```

---

## Next Actions

1. **Hasleo webapp page**: Dashboard showing task status, run buttons, last backup time
2. **Scheduled backups**: Cron-style recurring backup (Hasleo tasks + repo archival)
3. **Retention policy**: Keep last N backups per repo, prune old
4. **Cloud targets**: S3/B2 for off-site redundancy
5. **Remove dead service layer**: Delete `backup_service.py` or fix exports — Hasleo works via `backup_tools.py` directly
