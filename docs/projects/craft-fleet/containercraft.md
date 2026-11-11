# ContainerCraft — Assessment (Retired)

**Status:** Retired / Deleted from `D:\Dev\repos` (2026-11-09) · **Grade:** Retired · **Superseded by:** `docker-mcp` + [vmcraft](vmcraft.md)

## Why it was retired

Code audit on 2026-11-09 showed `sandraschi/containercraft` (`256 LOC` Python) was 6 thin `subprocess.run(["docker", ...])` wrappers (`ps`, `logs`, `exec`, `images`, `run-echo`, `compose-ps`). Container orchestration lives in `docker-mcp`, and hypervisor/VM management lives in Pure-Rust [vmcraft](vmcraft.md).
