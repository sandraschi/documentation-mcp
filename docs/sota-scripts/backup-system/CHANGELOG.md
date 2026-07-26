# Changelog - backup-repo.ps1

## [Unreleased] - 2026-07-18

### Fixed
- **Crash on unset `$env:OneDrive`** — script threw a bare
  `Cannot bind argument to parameter 'Path' because it is null` at
  startup (before touching any repo files) whenever `$env:OneDrive` was
  unset in the calling process's environment — which happens for any
  process not launched from an interactive session the OneDrive client
  has initialized into (services, scheduled tasks, some MCP server
  hosts). One destination's missing env var took down all three.

### Changed
- **Per-destination resolution and directory creation** — Desktop, N:
  Drive, and OneDrive are now each resolved and `New-Item`'d
  independently inside their own try/catch. A destination that can't be
  resolved (unset env var, unmapped drive, permission error) is skipped
  with an explicit `SKIP <name>: <reason>` message; the other
  destinations still get backed up. Only aborts (exit 1) if every
  destination fails, with a clear "see SKIP messages above" pointer.
- **OneDrive fallback** — if `$env:OneDrive` is unset, falls back to
  `%USERPROFILE%\OneDrive` (the conventional path OneDrive actually
  creates) before giving up on that destination.

### Note
- README.md's `-Folder` and multi-repository mode (documented as of
  3.1.0 below) do not exist in the current script's `param()` block —
  flagged here, not fixed, out of scope for this pass.

## [3.1.0] - 2025-11-01

### Added
- **`-Folder` parameter** - Backup all repositories in a specified folder in one command
- **Multi-repository mode** - Automatically detects repositories (`.git`, `pyproject.toml`, `package.json`) and backs them up sequentially
- **Bulk backup summary** - Comprehensive summary showing successful/skipped/errored repositories
- **Repository detection functions** - `Test-IsRepository` and `Find-Repositories` helper functions
- **Smart directory filtering** - Automatically excludes temporary/non-repository directories:
  - `temp`, `tmp`, `node_modules`, `.venv`, `venv`, `env`
  - `cache`, `build`, `dist`, `backup*`, `old*`, `archive*`
  - `test*`, `scratch`, `playground`, `sandbox*`, `quarantine`
  - And other common temporary directory patterns

### Changed
- **Recursive script invocation** - When `-Folder` is used, script calls itself for each repository (without `-Folder` to avoid recursion)
- **Enhanced error handling** - Individual repository errors don't stop the bulk backup process
- **Improved repository detection** - Filters out common temporary directories and build artifacts to avoid false positives

## [3.0.0] - 2025-11-01

### Added
- **Triple-location backups** - Added OneDrive as third backup location
- **Duplicate detection** - SHA256 hash comparison to skip unchanged backups
- **Backup history viewer** - `-List` flag to show backup statistics and history
- **Dry-run mode** - `-WhatIf` flag to preview backups without creating files
- **Verbose output** - `-Verbose` flag for detailed progress, timing, and hash computation
- **JSON output** - `-OutputFormat json` for programmatic/scripted use
- **Progress bars** - Visual progress indicators during ZIP creation
- **Metrics export** - JSONL metrics exported to `%APPDATA%\backup-metrics\`
- **Enhanced statistics** - Shows created/skipped locations, compression ratios, space saved
- **Helper functions** - Modular code with `Get-FileHashSHA256`, `Write-ProgressBar`, `Test-BackupDuplicate`, `Show-BackupHistory`, `New-BackupZip`
- **CmdletBinding support** - Proper PowerShell parameter binding with `SupportsShouldProcess`

### Changed
- **Backup locations** - Now creates backups in Desktop, N: drive, AND OneDrive
- **Duplicate handling** - Automatically removes duplicate backups to save space
- **Output formatting** - Enhanced statistics display with location status indicators
- **Error handling** - Better tracking of created vs skipped backups
- **Timing information** - Script execution time and ZIP creation duration tracking

### Improved
- **ZIP creation** - More efficient with progress reporting
- **Hash computation** - Optional progress display for hash calculations
- **Statistics** - More comprehensive backup statistics with location breakdown
- **User experience** - Clear indication when backups are skipped due to duplicates

## [2.1.0] - 2025-10-25

### Added
- Database-aware exclusions (selective .db file handling)
- Regex pattern fix for PowerShell compatibility
- Forward-slash path handling for Windows

### Changed
- Improved exclusion patterns for better compatibility
- Enhanced error reporting

### Fixed
- Regex escaping issues with backslashes in paths
- Database exclusion patterns (samples/metadata.db, test_data/*.db)

## [2.0.0] - 2025-10-24

### Added
- Dual-location backup (Desktop + N: drive)
- Windows native compression (Compress-Archive)
- Size analytics and reporting
- Compression ratio calculation
- Progress indicators with colors

### Changed
- Migrated from 7-Zip to Windows native
- Improved exclusion list
- Better error handling

## [1.0.0] - 2025-10-21

### Initial Release
- Basic repository backup functionality
- Git-aware name detection
- Standard exclusions (.venv, node_modules, .git)
- Single backup location

