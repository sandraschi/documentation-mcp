# Multi-Backup MCP — Product Requirements Document

**Version**: 0.6.0-dev
**Last Updated**: 2026-06-15
**Status**: Alpha → Production

---

## Problem Statement

Development repositories need reliable, automated backup to multiple destinations. Manual ZIP-and-copy workflows are error-prone, skip deduplication, and miss OneDrive/network targets. Existing solutions (Hasleo, UrBackup) add complexity without MCP integration.

## Solution

A FastMCP server providing two complementary backup methods via MCP tools and a React dashboard:

1. **Hasleo Backup Suite** (disk-level): System images, partition backups, incremental/differential via `BackupCmdUI.exe` CLI
2. **Repo Archival** (code-level): Git-tracked source & docs → ZIP → 3 destinations with SHA256 dedup

## Core Requirements

### Must Have (v0.6.0)

| Requirement | Status |
|---|---|
| Hasleo CLI integration (list tasks, run backup) | Done |
| Hasleo image verify + mount/unmount | Done |
| Backup git-tracked files only (source & docs) | Done |
| SHA256 deduplication (skip identical backups) | Done |
| 3 destinations: Desktop, N: drive, OneDrive | Done |
| Per-repo subdirectories at each destination | Done |
| Retry logic with exponential backoff | Done |
| Dry-run mode | Done |
| Repo scanning with junk exclusion | Done |
| Nuclear backup (all repos) | Done |
| Webapp Repos page with archive UI | Done |
| CI: ruff lint + format + pytest (Windows) | Done |
| No mocks/gaslighting in production paths | Done |

### Should Have (v0.7.0)

| Requirement | Status |
|---|---|
| Scheduled backups (cron-style) | Planned |
| Backup retention policy (keep last N) | Planned |
| Cloud targets (S3, B2, Azure Blob) | Planned |
| Post-backup verification (unzip + checksum) | Planned |
| Backup size trending / dashboard KPIs | Planned |

### Won't Have (out of scope)

- Cross-platform (Linux/Mac) — Windows-only fleet
- Encryption at rest (rely on BitLocker/OneDrive encryption)
- Custom Hasleo task creation via CLI (use GUI for setup, MCP for execution)

## Architecture

```
MCP Client (Cursor/Claude) ──► MCP Tools ──┐
                                            │
Webapp REST (React dashboard) ──► Routers ──┤
                                            │
                              ┌─────────────┴─────────────┐
                              ▼                           ▼
                    Hasleo CLI Bridge              archive_utils.py
                    (BackupCmdUI.exe)              (git ls-files + ZIP)
                         │                              │
                         ▼                     ┌────────┼────────┐
                  System/Partition              ▼        ▼        ▼
                  Images (.hbi)           Desktop/   N:/      OneDrive/
                                          repo backup repo-backups
```

## Ports

| Service | Port |
|---|---|
| Backend (FastAPI + MCP `/mcp`) | 10799 |
| Frontend (Vite React) | 10798 |

## Key Decisions

1. **Two-tier backup**: Hasleo for disk images, Python archiver for source code
2. **Python over PowerShell** (repo archival): Single code path, testable, no subprocess overhead
3. **git ls-files over os.walk**: Only tracked files = source & docs, no junk
4. **SHA256 dedup**: Prevents identical backup accumulation across destinations
5. **Per-repo subdirs**: Clean organization at each destination
6. **Hasleo for execution, not creation**: Tasks created in GUI, triggered via MCP

## Success Metrics

- Zero gaslighting: no mock data returned to users
- Ruff green: lint + format pass in CI
- All 3 destinations receive backups when available
- Dedup prevents >90% of redundant copies in daily-backup scenarios
