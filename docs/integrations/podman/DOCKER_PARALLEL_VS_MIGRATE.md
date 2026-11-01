# Docker vs Podman on the Fleet (Windows dev)

**Status:** Normative guidance for Sandra's workstation and fleet repos (2026-09-13).  
**Related:** [podman-mcp](https://github.com/sandraschi/podman-mcp), [docker-mcp](https://github.com/sandraschi/docker-mcp), [COMPARISON.md](COMPARISON.md).

## Summary

| Approach | Verdict |
|----------|---------|
| **Primary runtime: Docker Desktop + docker-mcp** | Yes for daily dev and existing compose stacks. |
| **Parallel Podman pilot** | Yes, bounded (one repo, fix machine once, then evaluate). |
| **Fleet-wide migrate Docker to Podman now** | No until Podman machine health is boring and each stack has rollback. |

**Recommendation:** Stay on Docker as primary. Run Podman in parallel only for a deliberate pilot, not a big-bang migration.

---

## Why not migrate everything now

On Windows + WSL2, running both engines at once commonly surfaces:

- Two VM backends (`docker-desktop` and `podman-machine-default`).
- **Cgroup hybrid (v1) vs Podman 6** inside the Podman machine (`Cgroups v1 not supported`).
- **Named pipe / API forwarding** conflicts (`\\.\pipe\podman-machine-default: All pipe instances are busy`).
- Duplicate RAM, images, volumes, and mental overhead.

The fleet already standardizes on **docker-mcp** (ports 10806/10807 per repo docs). **podman-mcp** (11112/11113) is valuable for evaluation and Red Hat-style workflows, but cutover before the host is stable wastes time.

---

## When parallel makes sense

Use both runtimes only with a clear scope:

- Evaluate rootless/daemonless workflows and podman-mcp tools (`manage_migrate`, compose on Podman).
- Test **one or two** non-critical repos after compose compatibility checks.
- Keep Docker for stacks that must stay green (production-adjacent compose, existing volumes).

### Parallel rules (Windows)

1. **One primary runtime** for day-to-day work; quit the other's desktop/engine when not testing.
2. Do not assume Podman Desktop install implies a **running** machine; verify `podman machine list` (LAST UP, State).
3. **kubectl** is optional and separate from either MCP server (see below).
4. Fix WSL/Podman machine once for the pilot before expanding scope.

---

## Is migrating Docker to Podman a good idea?

**Good long-term** if you want: no central daemon, rootless defaults on Linux, RHEL/Fedora alignment, or OCI workflows without Docker Desktop licensing on servers.

**Poor as a sudden fleet migration** when: compose-on-Docker is the norm, Docker Desktop integrations are in use, and Windows Podman machine is still failing health checks.

**Strangler pattern:** CI or Linux targets move to `podman` first; Windows dev stays on Docker until `podman machine start` is reliable; migrate repos one at a time with `manage_migrate` / compose checks.

---

## kubectl and podman-mcp

| Tool | Role |
|------|------|
| **kubectl** | CLI for **Kubernetes** API (clusters, Deployments, Pods in K8s sense). |
| **podman-mcp** | Wraps the **Podman CLI** (containers, pods, images, compose, machine). **Does not invoke kubectl.** |
| **docker-mcp** | Wraps **Docker**; no kubectl integration. |

Installing kubectl does not fix Podman machine or dashboard connectivity. Podman can generate or apply kube YAML (`podman generate kube`, `podman kube play`); those are Podman CLI features, not exposed as dedicated podman-mcp tools today. Use kubectl only if you run a local or remote Kubernetes cluster on purpose.

---

## Host findings (Goliath, 2026-09-13)

Documented during podman-mcp dashboard debugging:

- CLI: `%LOCALAPPDATA%\Programs\Podman\podman.exe` (6.0.2), often on user PATH via Podman Desktop.
- Machine `podman-machine-default` (WSL): distro could be Running while Podman reported **State: stopped**, **LAST UP: Never**.
- `podman machine start` failed with pipe busy + SSH not in running state; inside the VM, `podman info` reported **Cgroups v1 not supported**.
- **docker-desktop** WSL distro also running; coordinate cgroup/WSL settings if both must coexist.

### podman-mcp fixes (v3.5.1)

- Dashboard no longer shows "Podman is not installed" when the CLI works but the engine is down.
- Backend classifies `podman_missing` vs `podman_not_started` on `/api/dashboard`.
- Windows discovers Podman Desktop CLI path; fleet `fleet-start.config.ps1` can set `PODMAN_CMD`.

---

## Next steps (pilot path)

1. Keep **Docker Desktop** as primary for fleet dev.
2. For Podman pilot only: quit Docker when testing Podman (or accept cgroup tuning tradeoffs).
3. Consolidate `%USERPROFILE%\.wslconfig` (single `[wsl2]` block); consider unified cgroup for Podman machine per Red Hat/WSL docs; `wsl --shutdown`; `podman machine start` or recreate machine.
4. One pilot repo + podman-mcp dashboard green before touching Vienna/production-style stacks.

---

## References

- [integrations/podman/README.md](README.md)
- [integrations/podman/COMPARISON.md](COMPARISON.md)
- [integrations/virtualization/podman.md](../virtualization/podman.md)
- podman-mcp `CHANGELOG.md` v3.5.1
