# virtucraft — Dossier (draft 2026-11-02)

Source: `D:\Dev\repos\virtualization-mcp` (`virtops_*` portmanteaus)
Target: `D:\Dev\repos\virtucraft` (Bucket A → Pure-Rust ArtCraft 3-tier, or Python pilot first)
MCP key: `virtucraft` — binary `virtucraft-cli.exe` — `virtucraft-cli mcp --allow-path D:\Dev\repos`
Democraft family: `core` if Storytold-owned, else `community`. Ports: claim from `WEBAPP_PORTS.md` (10700-15000, never 3000/5000/5173/8000/8080).

## 1. Model

VM = {name, os_type, memory_mb, disk_gb, snapshots[], nics[], disks[], state}
Network = {name, type nat|bridged|hostonly|internal, ip, netmask}
Snapshot = {vm, name, created, description}
Disk = {path, size_gb, controller, attached_to}

All JSON-serializable. `run.json` must contain VM name + ms + state, never creds.

## 2. Verb map (from current virtops_*)

| virtucraft CLI | maps from | params | notes |
|---|---|---|---|
| `virtucraft vm list [--json]` | `vm_management(action=list)` | limit, offset | read-only, always safe in ci |
| `virtucraft vm info --vm NAME` | `vm_management(action=info)` | vm_name | read-only |
| `virtucraft vm create --vm NAME --os Ubuntu_64 --mem 4096 --disk-gb 40` | `vm_management(action=create)` | os_type, memory_mb, disk_size_gb | NOT in default ci (mutating). Recipe with `--dry-run` or VBox `create` guarded by flag. |
| `virtucraft vm start|stop|pause|resume|reset|delete --vm NAME [--force]` | `vm_management` + `hyperv_management(start/stop)` | vm_name, force | Mutating. Recipes use disposable `virt-ci-tmp-*`, delete after. Hyper-V needs admin — skip with `down` receipt if not elevated. |
| `virtucraft vm clone --src A --new B` | `vm_management(action=clone)` | source_vm, new_vm_name | Mutating, same guard. |
| `virtucraft snapshot list --vm NAME` | `snapshot_management(action=list)` | vm_name | read-only |
| `virtucraft snapshot create|restore|delete --vm NAME --snap S [--desc D]` | `snapshot_management` | vm_name, snapshot_name | Mutating, tmp-only in ci. |
| `virtucraft network list` | `network_management(action=list_networks)` | — | read-only |
| `virtucraft network create|remove --net NET [--ip IP --mask MASK --type hostonly]` | `network_management` | network_name, ip_address, netmask | Mutating, host-only only in ci (never touch NAT/bridged on Goliath). |
| `virtucraft nic list|attach --vm NAME [--slot N --type hostonly --net NET]` | `network_management(list_adapters/configure_adapter)` | vm_name, adapter_slot | Mutating, tmp VM only. |
| `virtucraft disk list|create|attach --vm NAME` | `storage_management` | disk_name, size, controller | Mutating, tmp only. |
| `virtucraft host info|vbox-version|metrics --vm NAME` | `system_management` | vm_name | read-only, `metrics` may be slow — timeout 60s. |
| `virtucraft hyperv list|get --vm NAME` | `hyperv_management(list/get)` | vm_name | Windows-only. Skip with `down` on non-Windows. |
| `virtucraft sandbox run --code "print('hi')"` | `sandbox_management(execute_code)` | code, language, timeout | Ephemeral, safe. Good ci recipe (no VM needed). |
| `virtucraft shot --vm NAME --out shot.png` | `system_management(screenshot)` | vm_name, output_file | Writes PNG to outbox, democraft gallery loves it. |

Out of scope for pilot: `vm_agentic_workflow(suggest_config/sandbox_workflow/workflow)` (sampling, not verbs), `win_sandbox_naked_test` (needs full sandbox), `libvirt` unless WSL2 present (probe, skip if absent).

## 3. CLI spec (craft-conformant)

```
virtucraft-cli vm list [--json] [--limit N]
virtucraft-cli vm info --vm NAME
virtucraft-cli snapshot list --vm NAME
virtucraft-cli network list
virtucraft-cli host info
virtucraft-cli sandbox run --lang python --code "..."
virtucraft-cli mcp [--allow-path D:\Dev\repos]   # stdio JSON-RPC
virtucraft-cli tools                              # list verbs + JSON schemas
virtucraft-cli run --script steps.json [--report] # batch, for democraft do_with
```

- `--help` must work for every verb (pdfcraft precedent).
- `--json` always prints one JSON doc to stdout (for `run.json` capture).
- Exit non-zero on fail. Mutating verbs require `--yes` or env `VIRTUCRAFT_ALLOW_MUTATE=1` in ci (never default-on).
- Roots: `--allow-path D:\Dev\repos` confines VDI/snapshot writes. No `C:\` writes in recipes.

## 4. MCP spec (thin)

- `type: local`, `command: [virtucraft-cli.exe, mcp, --allow-path, D:\Dev\repos]`, `enabled: true`, `timeout: 60000` (120000 for start/stop/clone).
- Tools: `vm_list`, `vm_info`, `snapshot_list`, `network_list`, `host_info`, `sandbox_run` (read-only/safe subset). Mutating tools behind same `VIRTUCRAFT_ALLOW_MUTATE` gate or separate `virtucraft_mutate` toolset (democraft `capabilities` must list which).
- No ports. Webapp only if Phase 2 (reuse democraft gallery, don't build new webapp in pilot).

## 5. Democraft recipes (required 3, all green to ship)

1. `virt/list-and-info` — `vm list --json` → pick first → `vm info --vm`. Assert keys `vms[]`, `vm_info.state`. `run.json` + 200-word report with counts + ms. Read-only, always runs.
2. `virt/sandbox-echo` — `sandbox run --lang python --code "print('hi-virt')"`. Assert stdout. No hypervisor needed. Always runs.
3. `virt/snapshot-roundtrip-tmp` — guarded: only if `VIRTUCRAFT_ALLOW_MUTATE=1` + disposable VM exists. `snapshot create --vm TMP --snap ci-TIMESTAMP` → `snapshot list` → assert present → `snapshot delete`. Measure ms. If no hypervisor/admin, write `down` receipt (`hyperv_present:false`), do NOT fail ci. This is the SearchStudio rule: dead pipes reported, not silent zeros.

Each writes `outbox/virt/<demo>/run.json` + `*-report.md` with measured numbers (not ok:true alone — must show state change + timings).

## 6. Gates

- `just ci` (ruff/pyright/pytest or cargo clippy/test/fmt per track) green.
- `data/craft_compat.json` baselines updated (gitignored).
- `crafts.py` entry: exe, verbs, HERO facts, family, maker, `hyperv_present`, `vbox_present` capabilities.
- `appMeta.ts` hue/icon, ContactSheet tile, Ctrl+K entry.
- `opencode.json` entry validated via `ConvertFrom-Json` (see pdfcraft/craft-anything precedent 2026-11-02).
- `.bak` for 3+ file edits, max 10 files per commit.

## 7. Risks

- Admin/Hyper-V absent → recipes skip, not fail. Probe first.
- Mutating VM ops on Goliath (daily driver) → tmp-only, `--yes` gate, never touch prod VMs (name allowlist `virt-ci-*`).
- VBox vs Hyper-V divergence → verbs abstract, `host info` reports provider. Do not expose both verb sets; one `vm list` that merges.
- Sandbox escape → `sandbox run` timeout 30s, no network by default (`network_enabled:false`).
- NSSM stale python.exe (HANDOVER 2026-11-02 notes hundreds) → ram weeder scan before bench, never `taskkill` prod children.

## 8. Effort

S (1-2 days) for read-only + sandbox recipes. M (1 week) with guarded mutate recipes + Rust scaffold if Bucket A chosen. Recommend Python pilot first (wrap existing `virtops`), Rust 3-tier only after 3 recipes green.

## 9. Next step after dossier approval

`just new-rust virtucraft` (if Rust) or copy `democraft-mcp/fleet-start.config.ps1` pattern, add `crafts.py` entry, write 3 recipes, `just ci`, screenshots via `node webapp/scripts/shots.mjs`, tag v0.1.0.
