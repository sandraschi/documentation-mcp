# 📦 Backup System - Repository Backup Script

## Overview

**Single-repo:** `backup-repo.ps1` – Professional repository backup (triple-location, duplicate detection, exclusions, Windows native ZIP).

**Mass backup (this folder):** `backup-all-repos.ps1` – Runs backup-repo.ps1 in every repo under ReposRoot (no MCP filter; uses each repo’s `scripts\backup-repo.ps1` or this folder’s backup-repo.ps1).

**Mass backup (MCP-only, advanced):** `scripts/backup_all_repos.ps1` (in mcp-central-docs) – MCP filter (-MCPOnly), -IncludeBuild, -TargetDir, -SaveIdent, -Help; uses this folder’s backup-repo.ps1.

**Run mass backup (all repos):** from repo root, run `.\sota-scripts\backup-system\backup-all-repos.ps1` or from mcp-central-docs/scripts run `..\sota-scripts\backup-system\backup-all-repos.ps1`.

---

## 🎯 Features

- ✅ **Triple-location backups** (Desktop + N: drive + OneDrive)
- ✅ **Intelligent exclusions** (.venv, node_modules, __pycache__, etc.)
- ✅ **Windows native compression** (.NET ZIP API with folder structure preserved)
- ✅ **Duplicate detection** (SHA256 hash comparison, skips unchanged backups)
- ✅ **Backup history viewer** (`-List` flag to see backup statistics)
- ✅ **Dry-run mode** (`-WhatIf` to preview without creating files)
- ✅ **Verbose output** (`-Verbose` for detailed progress and timing)
- ✅ **JSON output** (`-OutputFormat json` for programmatic use)
- ✅ **Size analytics** (before/after, compression ratio, space saved)
- ✅ **Database-aware** (selective .db file exclusion)
- ✅ **Git repository aware** (auto-detects repo name, includes .git folder)
- ✅ **Progress reporting** with color-coded output and progress bars
- ✅ **Metrics export** (JSONL format to `%APPDATA%\backup-metrics`)
- ✅ **Error handling** and validation

---

## 📋 Usage

### **Basic Usage:**

```powershell
# Must run from repository root
cd D:\Dev\repos\your-repo
.\scripts\backup-repo.ps1
```

### **With Parameters:**

```powershell
# Include build artifacts
.\backup-repo.ps1 -IncludeBuild

# Preview what would be backed up (dry-run)
.\backup-repo.ps1 -WhatIf

# Verbose output with detailed progress
.\backup-repo.ps1 -Verbose

# Show backup history and statistics
.\backup-repo.ps1 -List

# Backup all repositories in a folder (one command!)
.\backup-repo.ps1 -Folder "D:\Dev\repos"

# JSON output for scripting
.\backup-repo.ps1 -OutputFormat json

# Combine flags
.\backup-repo.ps1 -IncludeBuild -Verbose
.\backup-repo.ps1 -Folder "D:\Dev\repos" -Verbose
```

---

## ⚙️ Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `IncludeBuild` | switch | No | `$false` | Include `dist/` and `build/` folders |
| `List` | switch | No | `$false` | Show backup history and statistics |
| `Verbose` | switch | No | `$false` | Detailed progress and timing information |
| `WhatIf` | switch | No | `$false` | Preview what would be backed up (dry-run) |
| `Folder` | string | No | `$null` | Backup all repositories in the specified folder (e.g., `D:\Dev\repos`) |
| `OutputFormat` | string | No | `text` | Output format: `text` or `json` |

**Note:** 
- `Verbose` and `WhatIf` are PowerShell common parameters available via `CmdletBinding`.
- When `-Folder` is specified, the script automatically detects all repositories (directories with `.git`, `pyproject.toml`, or `package.json`) and backs them up sequentially.
- **Repository Detection:** The script excludes common temporary/non-repository directories:
  - `temp`, `tmp`, `node_modules`, `.venv`, `venv`, `env`
  - `cache`, `build`, `dist`, `backup*`, `old*`, `archive*`
  - `test*`, `scratch`, `playground`, `sandbox*`, `quarantine`
  - And other common temporary directory patterns

---

## 🚫 Excluded Files/Folders

### **Always Excluded:**
- `.venv`, `venv`, `env` - Virtual environments
- `node_modules` - Node.js dependencies
- `__pycache__`, `.mypy_cache`, `.ruff_cache`, `.pytest_cache` - Python caches
- `.git` - Git repository data
- `.windsurf`, `.cursor` - IDE files
- `*.pyc`, `*.pyo`, `*.pyd` - Python bytecode
- `dist`, `build`, `*.whl`, `*.tar.gz` - Build artifacts

### **Database Exclusions (Selective):**
- `samples/metadata.db` - Large Calibre test databases (3.9 MB)
- `samples/test_library.db` - Large test libraries
- `test_data/*.db` - Test data databases in any test_data directory
- **Note:** Small sample databases ARE backed up!

### **Large File Exclusions:**
- `*.vdi`, `*.vmdk`, `*.vhd` - Virtual machine disks
- `*.vbox`, `*.vbox-prev` - VirtualBox files
- `` - Calibre cache files

---

## 📊 Output

### **Progress Display:**
```
╔═══════════════════════════════════════════════════════════╗
║       📦 Repository Backup (Windows Native ZIP) 📦      ║
╚═══════════════════════════════════════════════════════════╝

📋 Backup Configuration:
  Repository:    your-repo
  Timestamp:     2025-11-01_02-52-43
  Destination 1: C:\Users\...\Desktop\repo backup\your-repo\
  Destination 2: N:\backup\dev\repos2\your-repo\
  Destination 3: C:\Users\...\OneDrive\repo-backups\your-repo\
  Include build: No
  Method:        .NET ZIP API (folder structure preserved)

🚫 Excluding:
  - .venv
  - __pycache__
  - .ruff_cache
  ...

📊 Analyzing repository size...
  Total size:    15.23 MB
  Excluded:      12.45 MB
  Backup size:   2.78 MB
  Reduction:     81.7%

🔄 Creating backups...
  → Desktop\repo backup...
  ✅ Desktop backup complete (folder structure preserved)
  → N:\backup\dev\repos2...
  ✅ N: drive backup complete (folder structure preserved)
  → OneDrive\repo-backups...
  ✅ OneDrive backup complete (folder structure preserved)

✅ Backups created: Desktop, N: drive, OneDrive

╔═══════════════════════════════════════════════════════════╗
║              📦 Backup Complete! 📦                     ║
╚═══════════════════════════════════════════════════════════╝

📊 Backup Statistics:
  Created:        3 of 3 locations
  File:           your-repo_backup_2025-11-01_02-52-43.zip
  Location 1:     Desktop ✅
  Location 2:     N: drive ✅
  Location 3:     OneDrive ✅
  Size:           1.85 MB
  Original:       2.78 MB
  Compression:    66.5%
  Space saved:    13.38 MB
  Method:         .NET ZIP API (folder structure preserved)
  Duplicate check: Enabled (skips unchanged backups)
```

### **Duplicate Detection:**
When a backup is identical to the previous backup (SHA256 hash match), it's automatically removed to save space:
```
  ⏭️  Desktop backup identical to previous - removing duplicate
  ⏭️  Backups skipped (unchanged): Desktop, N: drive, OneDrive
  📌 No new backups created - repository unchanged since last backup
```

### **Backup History (`-List` flag):**
```
╔═══════════════════════════════════════════════════════════╗
║        📊 Backup History: your-repo 📊         ║
╚═══════════════════════════════════════════════════════════╝

📍 Desktop\repo backup
   Total backups: 5
   Oldest:       2025-10-25 14:30:00
   Newest:       2025-11-01 02:52:43
   Total size:   9.25 MB
   Avg size:     1.85 MB
```

### **Multi-Repository Mode (`-Folder` flag):**
```
╔═══════════════════════════════════════════════════════════╗
║     📦 Multi-Repository Backup Mode 📦                  ║
╚═══════════════════════════════════════════════════════════╝

🔍 Scanning folder: D:\Dev\repos
✅ Found 12 repositories:

  📁 calibremcp
  📁 database-operations-mcp
  📁 unity3d-mcp
  ...

======================================================================
[1/12] Backing up: calibremcp
======================================================================

[Standard backup output for each repository...]

======================================================================
╔═══════════════════════════════════════════════════════════╗
║            📊 Multi-Repository Backup Summary 📊        ║
╚═══════════════════════════════════════════════════════════╝

📁 Folder:        D:\Dev\repos
📦 Repositories:  12
✅ Successful:    11
⏭️  Skipped:       0
❌ Errors:        1

⏱️  Total duration: 245.3s
```

---

## 🎯 Use Cases

1. **Daily Backups** - Before major changes
2. **Pre-Release** - Before tagging releases
3. **Archive** - Long-term storage
4. **Migration** - Moving to new machine
5. **Disaster Recovery** - System failures
6. **Bulk Backups** - Backup entire `repos/` folder in one command with `-Folder` parameter

---

## 💡 Best Practices

1. **Run regularly** - Daily or before major changes
2. **Check backup size** - Ensure reasonable compression
3. **Use `-WhatIf` first** - Preview before creating large backups
4. **Review history** - Use `-List` to monitor backup frequency and sizes
5. **Verify exclusions** - Review excluded file list
6. **Test restore** - Periodically test backup restoration
7. **Monitor storage** - Check Desktop, N: drive, and OneDrive space
8. **Leverage duplicates** - Let duplicate detection save space automatically

---

## 🔧 Troubleshooting

### **"Must run from repository root"**
- Solution: `cd` to repository root first

### **"N: drive not accessible"**
- Solution: Backup still completes to Desktop and OneDrive
- Check N: drive mounting
- Script continues with available locations

### **"OneDrive not accessible"**
- Solution: Backup still completes to Desktop and N: drive
- Check OneDrive sync status
- Script continues with available locations

### **Backups always skipped as duplicates**
- Solution: This is expected if repository hasn't changed
- Use `-Verbose` to see hash comparison details
- Check with `-List` to see backup history

### **Regex pattern errors**
- Solution: Update to latest version from central docs
- Use forward slashes in exclusion patterns

### **Metrics not exporting**
- Solution: Check write permissions to `%APPDATA%\backup-metrics\`
- Script continues even if metrics export fails

### **`-Folder` parameter finds no repositories**
- Solution: Verify the folder path is correct
- Check that subdirectories contain `.git`, `pyproject.toml`, or `package.json`
- Script only detects immediate subdirectories (not nested repos)
- **Note:** Directories with names like `temp`, `node_modules`, `venv`, `backup*`, etc. are automatically excluded
- If a legitimate repository is excluded, rename it or modify the `$excludeDirNames` array in the script

### **One repository fails in bulk backup**
- Solution: The script continues with other repositories
- Check the error output for the specific repository
- Failed repositories are listed in the summary
- Individual repository errors don't stop the bulk backup process

---

## 📈 Version History

See `CHANGELOG.md` for complete version history.

**Current Version:** 3.1.0
**Last Updated:** 2025-11-01

---

## 🔗 Related

- **SOTA Scripts Master README** - `../README.md`
- **Central Docs** - `../../README.md`
- **Propagation Script** - `../propagation-tools/propagate-backup-script.ps1`

---

**Part of the SOTA Scripts collection** ✨


