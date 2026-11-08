# VirtuCraft — Assessment

**Repo:** `D:\Dev\repos\virtucraft` · **Date:** 2026-11-05 · **Grade: C**

> Capitalisation note: README titles it `VirtuCraft`; dir and PLAN use
> `virtucraft`. Keep `virtucraft` (lowercase, like every other craft).

## What it is

Craft-pattern headless VM + hypervisor workstation. Rebuild-PLAN pilot #1
(from `virtualization-mcp` `virtops_*`: `vm_management`, `snapshot_management`,
`network_management`, `storage_management`, `hyperv_management`,
`libvirt_management`, `sandbox_management`, `system_management`).

## Model / verbs

- **Model:** VM (name/os/RAM/disk/snapshots/NICs/disks).
- **Verbs (README):** `vm list|info`, `snapshot list|create|delete`,
  `network list`, `host info`, `sandbox run`, `tools`, `mcp`.
- **Surface:** richest of the Python six —
  `cli/hypervisor/models/sandbox/mcp_server` modules. 2 test files.

## Architecture

Python FastMCP, `uv.lock`, `pyproject`, `justfile`, `AGENTS.md`
("VirtuCraft is the fleet craft for VMs…"). Scaffold committed 2026-11-04.

## Strengths

- Pilot #1 for a reason: VM verbs are genuinely headless and file-adjacent
  (snapshot roundtrip with ms measures is an ideal recipe).
- Module split (hypervisor/models/sandbox) already exceeds the other Python
  scaffolds' single-`cli.py` shape.
- PLAN wants `serve --port` from day 1 (VM start/snapshot are long-lived;
  gallery wants `shot --out png` polling) — specced, not yet built.

## Gaps / risks

- Hyper-V needs admin; recipes must skip gracefully (`hyperv_present` capability
  gate) — unproven.
- `sandbox run --code` executes arbitrary code: confinement story must match
  the ArtCraft `--allow-path`/`--root` discipline, not just exist.
- Long-lived-session design (`serve`) vs one-shot verbs tension unresolved.
- Deepest module tree of the six but still no `docs/` and no engine tests at triage.

## Next 3 steps

1. Hypervisor-presence gate + skip-with-receipt in tests.
2. 3 recipes: `virt/list-and-info`, `virt/snapshot-roundtrip`, `virt/network-create-delete`.
3. `serve` spec decision (file the `virtucraft#serve` issue or defer with rationale).

## Verdict

Grade C, top of the C band: best-shaped Python scaffold and pilot status, but
still pre-proof. Presence gates + snapshot roundtrip promote it first.
