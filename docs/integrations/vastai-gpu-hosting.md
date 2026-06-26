# Vast.ai GPU Hosting — Goliath Integration Notes

**Status:** UNDER REVIEW — not yet active  
**Last updated:** 2026-05-01  
**Relevant hardware:** Goliath (RTX 4090 24GB, AMD Ryzen 9 5900X, 64GB RAM)  
**See also:** `integrations/salad-gpu-sharing.md`

---

## What Is Vast.ai?

Vast.ai is a peer-to-peer GPU marketplace. Unlike Salad's opaque job queue, Vast is a direct marketplace: you list your machine as a host with your own hourly rate, clients browse and rent it, and you get paid per hour of actual rental. Both consumer rigs and datacenter hardware coexist on the same marketplace.

The client-side rate for a 4090 on Vast sits around **$0.34/hr** (early 2026), roughly 70% higher than Salad's ~$0.20/hr. The difference is you're running Docker containers for direct renters rather than Salad's sandboxed opaque workloads — different effort level, different trust model.

---

## Why Vast.ai Over Salad for Goliath

The original objection to Vast was setup complexity. That objection is weaker now:

- Docker is already running on Goliath (albeit with daemon stability issues lately — see caveats below)
- AI-assisted setup means host configuration, pricing strategy, and Docker tuning is not a days-long manual job
- The ~70% rate premium is meaningful at scale: at 50% utilization that's ~€120–160/month gross vs ~€50–80 on Salad

The remaining tradeoff is the **trust model** — see Security section below.

---

## Economics

Based on published Vast.ai marketplace rates (May 2026). Electricity cost is low (Vienna Sozialtarif subsidised rate, ~€0.08/kWh estimate — update with actual rate). Power draw ~350W under load.

| Scenario | Rate | Utilization | Gross/month | Power cost | Net/month |
|---|---|---|---|---|---|
| Conservative | $0.34/hr | 35% | ~$86 | ~€7 | ~€72 |
| Realistic | $0.34/hr | 50% | ~$122 | ~€10 | ~€105 |
| Optimistic (verified host premium) | $0.45/hr | 60% | ~$194 | ~€12 | ~€175 |

At a subsidised electricity rate, power cost is nearly negligible and net earnings are close to gross. The open-frame setup eliminates thermal constraints entirely, so sustained high utilization is viable without hardware risk.

### vs. Salad comparison

| | Salad | Vast.ai |
|---|---|---|
| RTX 4090 rate | ~$0.20/hr | ~$0.34–0.45/hr |
| Setup effort | Near-zero | Moderate (Docker config, pricing, verification) |
| Passivity | Full set-and-forget | Needs occasional rate tuning |
| Trust model | Sandboxed opaque jobs | Docker containers, direct renters |
| Payout | Salad Balance (PayPal cashout) | Direct cash |
| Platform risk | Salad goes down = no jobs | Marketplace — many renters |

---

## How Vast.ai Host Setup Works

1. **Create account** at vast.ai, switch to the "Host" view
2. **Install the host daemon** — a lightweight agent that registers your machine and manages container lifecycle
3. **Configure the listing:**
   - GPU model auto-detected (RTX 4090)
   - Set your price ($/hr) — start slightly below comparable verified hosts, raise once reputation builds
   - Set storage allocation for container images
   - Set bandwidth limits if desired
4. **Get verified** — Vast runs benchmark jobs to validate your hardware and assigns a reliability score
5. **Go live** — the daemon accepts jobs automatically when your machine is idle

The daemon manages Docker container pulls, execution, and teardown. You don't interact with individual jobs.

### Pricing strategy
- Check current 4090 listings on the marketplace before setting your rate
- Undercut slightly initially to get first jobs and build reliability score
- Raise rate by $0.02–0.05/hr increments once verified and earning consistently
- Monitor weekly — supply/demand shifts with new hardware entering the market

---

## Operational Considerations for Goliath

### Docker Daemon Stability

This is the main current blocker. Docker Desktop on Goliath has been showing daemon instability (daemon going pfft). Vast.ai requires a reliably running Docker daemon — if it crashes during a rented job, the client's work is interrupted and your reliability score takes a hit.

**Before going live on Vast.ai, the Docker daemon stability issue must be resolved.**

Options to investigate:
- Switch from Docker Desktop to Docker Engine (WSL2 backend) — Desktop adds overhead and a GUI layer that can introduce instability not present in bare Engine
- Check Docker Desktop version, recent updates have had known issues
- Consider running Docker Engine directly in WSL2 (Ubuntu) rather than Docker Desktop on Windows — better for headless server use
- Review Windows Event Log for daemon crash signatures

Until Docker is stable for 48+ hours unattended, Vast.ai is not viable. Salad is more resilient to this since its workloads don't depend on Docker in the same way.

### Conflict with Local Use

Same conflicts as Salad, with one important difference — a Vast.ai renter has an active session they're paying for. Interrupting it (for Ollama, Blender, etc.) hurts your reliability score. Plan interruptions accordingly.

| Activity | Conflict? | Impact on host score |
|---|---|---|
| MCP servers (CPU-bound) | None | None |
| Plex transcoding (NVENC) | Minor VRAM overlap | Minimal |
| Ollama / LM Studio | Yes — full VRAM conflict | Score hit if renter is mid-job |
| Blender GPU render | Yes | Score hit if renter is mid-job |
| Active dev session needing GPU | Yes | Plan around active rentals |

**Mitigation:** Vast lets you set "unavailable" windows in your listing (e.g., scheduled maintenance). Use this during Blender sessions or local LLM testing rather than just yanking the GPU.

### Thermal

Goliath runs in an open frame — ambient airflow is excellent and the 4090 has no enclosure heat buildup. Sustained inference workloads are not a thermal concern in this configuration. No fan curve tuning or power limiting required before going live.

Basic monitoring with HWiNFO64 is still sensible just to have a baseline, but this is not a blocker.

### Network

Vast.ai clients pull Docker images (can be large — 10–40GB for model containers) and transfer data. A slow or capped connection hurts your utilization and can fail jobs.

- Verify upload speed is consistently 50+ Mbps (ideally 100+)
- Check whether your ISP has data caps — sustained hosting can consume 1–3TB/month

---

## Security / Trust Model

This is the key difference from Salad and deserves honest consideration.

**Salad:** jobs are opaque containerized workloads from vetted enterprise clients. You don't know what's running but you didn't spin up the containers — Salad did. The attack surface is narrow.

**Vast.ai:** arbitrary clients rent your machine and run Docker containers they specify. The containers are isolated (no host network access by default, limited filesystem mounts), but:
- The container could attempt GPU-assisted attacks or cryptomining alongside the stated workload
- Vast's ToS prohibits abuse but enforcement is reactive, not preventative
- A malicious container with a local privilege escalation exploit could potentially escape isolation

**Mitigations:**
- Keep Windows, Docker, and NVIDIA drivers current — most container escapes exploit known unpatched vulnerabilities
- Do not mount sensitive host directories into containers (Vast's default container config doesn't do this)
- Monitor GPU utilization patterns — unexpected cryptomining shows up as sustained 100% GPU load with no legitimate output
- The MCP fleet and dev environment live on the same machine — this is the realistic risk: a container escape could potentially reach `D:\Dev\repos`. Assess whether this risk is acceptable.

**Verdict:** For a dedicated renting machine this is a non-issue. For Goliath which also hosts the MCP fleet, it warrants a clear-eyed risk acceptance rather than ignoring it.

---

## DeepSeek V4 Open Weights (June 2026)

Same conflict as Salad — if local DS V4 becomes a daily driver, GPU sharing stops making sense during active hours. Vast.ai is slightly more affected because renters have active paid sessions, making opportunistic interruptions for local inference more costly to reputation.

If open weights land and are good enough, the calculus shifts: stop hosting, run local inference, accept the zero earning in exchange for zero API cost.

---

## Status / Next Steps

- [ ] **Prerequisite: Fix Docker daemon stability** — 48hr clean uptime required before proceeding
- [ ] Create Vast.ai host account
- [ ] Configure listing: rate, storage allocation, availability windows
- [ ] Complete verification process
- [ ] Run for two weeks, monitor reliability score and earnings
- [ ] Tune fan curve and power limit before first jobs
- [ ] Set up HWiNFO64 alert for VRAM hotspot > 88°C
- [ ] Revisit vs. Salad once both are evaluated empirically

---

## Related

- `integrations/salad-gpu-sharing.md` — simpler alternative, lower rate, no Docker dependency
- `integrations/local-llm/` — Ollama, LM Studio on Goliath
- Docker daemon stability issues — check `troubleshooting/BUGS_DEPOT.md`
- DeepSeek V4 open weights decision point: June 2026
