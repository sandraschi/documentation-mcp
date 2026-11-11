# WinCraft — Assessment

**Repo:** `D:\Dev\repos\wincraft` · **Date:** 2026-11-09 · **Grade: A-** · **Origin:** fleet-owned

## What it is

Pure-Rust ArtCraft 3-tier Windows host, RAM Weeder, Restart Manager file-lock inspector, high-speed FileOps, and NSSM-safe SysAdmin studio (`v0.1.0`, 3 crates, 26 MCP tools, 12 unit tests, 8-page `eframe`/`egui` desktop app).

Subsumes five overlapping Windows/file Python MCP servers (`windows-operations-mcp`, `system-admin-mcp`, `sysinternals-mcp`, `filesystem-mcp`, `winrar-mcp`) plus the retired Python `filecraft` scaffold into one zero-tax native binary (`wincraft.exe`).

## Model / verbs

- **Model:** Windows Host (logical volumes + processes/ports + file locks + filesystem tree/duplicates + services/NSSM + registry/autoruns/event logs).
- **Outputs & Export (`wincraft_core::export`):** Every collection output in both L3 `wincraft-app` and L2 `wincraft` CLI defaults to **Cards** view and switches between **Cards (default)**, **List (table)**, and **JSON**, with live substring filtering, numeric-aware column sorting, pagination (`10`/`25`/`50`/`100`), and one-click/flag export to **`CSV`**, **`MD` (Markdown table)**, **`TXT`**, or **`JSON`**.
- **26 MCP tools / CLI verbs (`v0.1.0`):**
  - **System & Diagnostics:** `win_status`, `win_doctor`, `win_disk_list` (native Win32 `GetLogicalDrives` + `GetDiskFreeSpaceExW`), `win_env_audit` (flags dead/missing `PATH` entries and duplicates)
  - **Processes & Fleet Ports:** `win_proc_list`, `win_port_map` (maps TCP/UDP ports to PIDs and cross-references `mcp-central-docs/operations/WEBAPP_PORTS.md`)
  - **RAM Weeder:** `win_weeder_scan` (detects orphaned `<crate>-<16hex>.exe` cargo test binaries, headless engine workers, and runaway runtimes), `win_weeder_reap` (`confirm=true`, protected system/host process allowlist)
  - **File-Lock Inspector:** `win_lock_inspect` (native Win32 Restart Manager `rstrtmgr.dll` FFI: `RmStartSession` / `RmRegisterResources` / `RmGetList` — answers "Who locks this file or directory?" without kernel drivers)
  - **High-Speed FileOps:** `win_fs_list`, `win_fs_du`, `win_fs_large`, `win_fs_dups` (3-stage streaming duplicate finder: size -> 4KB SHA-256 prefix -> 64KB streaming FIPS 180-4 SHA-256), `win_fs_hash`, `win_fs_grep`, `win_fs_backup_write` (mandatory `.bak`), `win_fs_undo_backup`, `win_fs_archive_inspect`, `win_fs_archive_create`
  - **SysAdmin & Registry:** `win_svc_list`, `win_svc_control` (NSSM-aware `sc.exe stop/start`), `win_startup_list`, `win_task_list`, `win_reg_read`, `win_reg_write` (exports `.reg` backup before modifying `HKCU`), `win_event_tail`

## Architecture

3-crate Pure-Rust ArtCraft workspace (`wincraft-core`, `wincraft-mcp`, `wincraft-app`), clippy five-denies (`unwrap_used`, `expect_used`, `panic`, `unimplemented`, `todo` all denied), single `dispatch` bus shared by CLI, MCP, and L3 GUI (proven by `app_dispatch_matches_core_dispatch_and_defaults_to_cards`). Includes `docs/` (`PRD.md`, `TOOLS.md`, `PARITY.md`, `UI_PARITY.md`, `SAFETY.md`), `INSTALL.md`, `CHANGELOG.md`, `justfile`, `start.ps1`, `start.bat`.

## Strengths

- **Native Win32 FFI where it counts:** `rstrtmgr.dll` Restart Manager lock inspection and `kernel32.dll` logical volume metrics run in microseconds with zero external binary dependencies.
- **Interactive & headless output parity:** Cards (default), List/Table, and JSON modes with pagination, numeric-aware sorting, live filtering, and CSV/MD/TXT/JSON export work identically in `wincraft-app` and `wincraft` CLI.
- **Fleet-rule safety in code:** NSSM service detection, protected process allowlist, mandatory `.bak` file backups, mandatory `.reg` registry backups, `--read-only` mode, and `--root` path confinement.
- Replaces five Python venvs when inspecting or cleaning up Goliath.

## Gaps / risks

- Raw NTFS MFT undelete (`\\.\C:`) remains in `system-admin-mcp`'s elevated service bridge until Phase 2.
- `.rar` / `.7z` extraction delegates to `Rar.exe` / `7z.exe` (probed in `win_doctor`), while `.zip` is native pure Rust.

## Next 3 steps

1. Wire 3 `democraft` recipes (`win/status-and-doctor`, `win/dups-and-backup-roundtrip`, `win/lock-inspect-and-weeder`).
2. Add optional `robocopy` bulk directory mirror verb (`win_fs_mirror` with `dry_run` preview).
3. Add Authenticode signature reader (`WinVerifyTrust` FFI) in Phase 2.

## Verdict

Grade A-: built from day one to the BookCraft/VmCraft 6-gate ArtCraft standard — 26 tools, native Win32 Restart Manager FFI, 3-stage streaming duplicate detection, RAM Weeder, Cards/List/JSON switcher + pagination/sort/filter + CSV/MD/TXT export, and complete `docs/` coverage.
