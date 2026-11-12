# VmCraft — Assessment

**Repo:** `D:\Dev\repos\vmcraft` · **Date:** 2026-11-09 · **Grade: B+** · **Origin:** fleet-owned

> Supersedes the Nov-4 Python scaffold `virtucraft` (`sandraschi/virtucraft`). `vmcraft` is the canonical Pure-Rust ArtCraft 3-tier hypervisor studio.

## What it is

Pure-Rust local-first virtual machine and hypervisor workstation (`v0.2.0`, `2,821 LOC`, `25 tests`, 3 crates) wrapping VirtualBox (`VBoxManage`) with a strict confirmation gate for mutating operations, a 19-tool stdio MCP server, and an 8-page native `eframe`/`egui` desktop app. Live-verified on Goliath against VirtualBox 7.1.12 (4 real VMs inspected, headless start/stop verified).

## Model / verbs

- **Model:** Hypervisor host + VM inventory + snapshots + host-only/NAT networks + optical/disk media + guest metrics.
- **19 MCP tools / CLI verbs (`v0.2.0`):**
  - Read-only inspection: `vm_status`, `vm_list`, `vm_info`, `vm_ostypes`, `vm_snapshots`, `vm_networks`, `vm_storage`, `vm_metrics`, `vm_guestproperty`, `vm_showvminfo_raw`, `vm_doctor`, `vm_events`
  - Gated mutating verbs (require `confirm: true` or `--confirm`, plus immutable VM blocklist): `vm_start`, `vm_stop`, `vm_pause`, `vm_resume`, `vm_snapshot_take`, `vm_snapshot_restore`, `vm_snapshot_delete`

## Architecture

3-crate Pure-Rust ArtCraft workspace (`vmcraft-core`, `vmcraft-mcp`, `vmcraft-app`), `2,821 LOC`, `25 tests`, `clippy -D warnings` clean:
- `vmcraft-core`: `VBoxManage` discovery (standard Windows/Linux/macOS paths + `VBOX_MSI_INSTALL_PATH` + `PATH`), machine-readable `--machinereadable` parser, confirmation gate, protected-VM blocklist, audit event log.
- `vmcraft-mcp`: 19 stdio MCP tools sharing `dispatch`.
- `vmcraft-app`: 8-page native `eframe`/`egui` desktop workstation (Dashboard, Machines, Snapshots, Networks, Storage, Metrics, Doctor, Help) with live refresh and headless start/stop controls.

## Strengths

- Live-verified against real VirtualBox 7.1.12 VMs on Goliath (not just mock tests).
- Mutating operations (`start`, `stop`, `snapshot_restore`, `snapshot_delete`) require explicit `confirm: true` and check a protected-VM blocklist before invoking `VBoxManage`.
- Cleanly replaces the Python `virtucraft` scaffold with a single native binary (`vmcraft.exe`).

## Gaps / risks

- Currently focused on VirtualBox (`VBoxManage`); Hyper-V (`vmcompute`) and QEMU/WSL2 backends are out of scope for `v0.2.0` and documented as non-goals in `docs/PARITY.md`.
- Long-running guest provisioning (ISO unattended install) is not yet wrapped.

## Next 3 steps

1. Wire 3 `democraft` recipes (`vm/doctor-and-list`, `vm/inspect-machinereadable`, `vm/confirm-gate-refusal`).
2. Add screenshot capture verb (`VBoxManage controlvm <vm> screenshotpng`) for visual agent inspection.
3. Mark `sandraschi/virtucraft` on GitHub as archived/superseded by `sandraschi/vmcraft`.

## Verdict

Grade B+: a textbook ArtCraft 3-tier build — 2,821 LOC of clean Rust, 19 MCP tools, 25 tests, confirmation gates in code, and live-tested on Goliath's hypervisor.
