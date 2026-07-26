# Tool Reference

## Hasleo Backups
| Tool | Description |
|------|-------------|
| `list_backups` | List all Hasleo backup tasks |
| `create_backup` | Create a backup job (name, sources, destination, mode, type, compression, encryption) |
| `start_backup` | Start a backup job by GUID (full/incremental/differential) |
| `cancel_backup` | Cancel a running backup |
| `check_backup_image` | Verify .hbk/.hsi image integrity |
| `mount_backup_image` | Mount image as virtual drive |
| `unmount_backup_image` | Unmount virtual drive |
| `launch_hasleo_tool` | Open Hasleo GUI utility |

## Repo Archival
| Tool | Description |
|------|-------------|
| `scan_repositories` | List all git repos in D:/Dev/repos |
| `run_repo_backup` | Archive one repo to configured destinations (git ls-files, SHA256 dedup) |
| `run_nuclear_backup` | Archive ALL repos with per-repo progress |
| `list_repo_backups` | List existing backup ZIPs |
| `check_repo_freshness` | Check if a repo backup is current vs git remote |
| `check_all_freshness` | Check freshness for all repos |
| `bundle_backup_exports` | Package newest backup per repo into a single ZIP |

## Restore
| Tool | Description |
|------|-------------|
| (REST) `POST /api/repos/restore` | Extract backup ZIP to destination. Blocked on original path without explicit overwrite. |

## Schedules
| Tool | Description |
|------|-------------|
| `create_schedule` | Create a schedule (once/daily/weekly/monthly/calendar). Persisted to JSON. |
| `list_schedules` | List all schedules |
| `enable_schedule` / `disable_schedule` | Toggle schedule |
| `get_upcoming_backups` | Preview next runs |

## Archives (ZIP)
| Tool | Description |
|------|-------------|
| `create_archive` | Create ZIP with smart exclusions (.venv, node_modules, __pycache__, etc.) |
| `list_archives` | List ZIPs in a directory |
| `extract_archive` | Extract ZIP to destination |

## Cloud Backup
| Tool | Description |
|------|-------------|
| (REST) `GET /api/cloud/status` | Check cloud config status |
| Integrated into `run_repo_backup` | Auto-uploads to S3-compatible storage after each backup |

## UrBackup
| Tool | Description |
|------|-------------|
| `urbackup_status` | Check UrBackup server connectivity |
| `urbackup_list_backups` | List all backup jobs on UrBackup server |
| `urbackup_start_backup` | Start a backup job by ID |
| `urbackup_client_status` | Status of a specific client machine |

## Git/GitHub
| Tool | Description |
|------|-------------|
| `make_git` | Init a git repo with .gitignore and README |
| `make_github` | Create GitHub repo and push (requires `gh` CLI) |

## AI Stack
| Tool | Description |
|------|-------------|
| `list_ai_providers` | Detect Ollama, LM Studio, OpenAI |
| `list_ai_models` | List models for a provider |
| `pull_ai_model` | Download a model (Ollama only) |

## System
| Tool | Description |
|------|-------------|
| `get_system_info` | OS, disk, memory, CPU |
| `get_storage_info` | Free space analysis for backup targets |
| `list_usb_drives` | List USB flash drives |
| `create_emergency_disk` | Create WinPE emergency disk |
| `get_logs` | Retrieve logs with pagination/filtering |
| `export_logs` | Export logs to file |
| `rotate_logs` | Clear log file |

## Prefab UI (MCP Apps)
| Tool | Description |
|------|-------------|
| `show_status_app` | Server status as rich Prefab card |
| `show_backups_app` | Backup jobs as Prefab card |
| `show_repo_backups_app` | Repo backups as Prefab card |

## Meta
| Tool | Description |
|------|-------------|
| `help` | Get help documentation |
| `status` | Server status report (basic/intermediate/advanced) |
| `backup_workflow` | Multi-step orchestration (repo_archive/repo_to_github/hasleo_scheduled) |
| `autonomous_backup_agent` | Sampling-based autonomous agent for complex tasks |
