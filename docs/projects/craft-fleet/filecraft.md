# FileCraft — Assessment (Retired)

**Status:** Retired / Deleted from `D:\Dev\repos` (2026-11-09) · **Grade:** Retired · **Superseded by:** [wincraft](wincraft.md) (`D:\Dev\repos\wincraft`)

## Why it was retired

Code audit on 2026-11-09 showed `sandraschi/filecraft` (`498 LOC` Python) was a naive day-1 `os.walk` wrapper (`find_duplicates` read entire files into memory with `p.read_bytes()`; `grep_path` scanned files single-threaded in Python).

All filesystem analytics and file-safety operations are now natively implemented in Pure Rust inside **[wincraft](wincraft.md)** (`D:\Dev\repos\wincraft`):
- `win_fs_du`, `win_fs_large`, `win_fs_list`, `win_fs_grep`, `win_fs_hash`
- `win_fs_dups`: 3-stage streaming duplicate detector (size -> 4KB SHA-256 prefix -> 64KB streaming FIPS 180-4 SHA-256)
- `win_fs_backup_write` & `win_fs_undo_backup`: mandatory `.bak` pre-write backup and restore
- `win_lock_inspect`: native Win32 Restart Manager (`rstrtmgr.dll`) file-lock inspector
