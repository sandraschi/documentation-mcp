---
title: "WizTree Standards (SOTA 2026)"
category: standards
status: active
audience: mcp-dev
last_updated: 2026-04-20
---

# WizTree Standards

**Version**: 1.0  
**Status**: RECOMMENDED (Disk Auditing)  
**Substrate**: Windows (Antigravity Fleet)

## 1. Overview
WizTree is a powerful disk space analysis utility that reads the Master File Table (MFT) directly. It is optimized for large-scale metadata dumps and disk usage auditing, making it ideal for "heartbeat" scripts and RAG ingestion of file system states.

## 2. Canonical Configuration
- **Absolute Path**: `C:\Program Files\WizTree\WizTree64.exe`

## 3. CLI Integration Patterns
Use WizTree for automated disk snapshots and finding "bloat" candidates:

### 3.1. Large File Snapshot
To export the top 1000 largest files on a drive:
```powershell
& "C:\Program Files\WizTree\WizTree64.exe" "C:\" /export="C:\logs\hourly_bloat.csv" /exportfolders=0 /sortby=2 /maxfiles=1000 /quit
```

### 3.2. Project-Specific Metadata Dump
To isolate candidates for a "Documentation Push" (e.g., Markdown and source files):
```powershell
& "C:\Program Files\WizTree\WizTree64.exe" "D:/Dev/repos/Antigravity" /export="ag_snapshot.csv" /filter="*.md|*.py|*.ts" /quit
```

### 3.3. Key Parameters
- `[path]`: Target drive or folder to scan.
- `/export="filename.csv"`: Export results to CSV.
- `/exportfiles=0|1`: Include files in export (default 1).
- `/exportfolders=0|1`: Include folders in export (default 1).
- `/filter="pattern"`: File search filter.
- `/admin=1`: Force administrative privileges (for MFT access).
- `/quit`: Exit after completing the export.

## 4. Operational Context
WizTree should be utilized by agents when a recursive file system walk via `Get-ChildItem` would be too slow or when detailed size-based sorting is required for resource management.

---
👉 [WizFile Standards](./WIZFILE_STANDARDS.md) | [Fleet Control Plane](../operations/FLEET_CONTROL_PLANE.md)
