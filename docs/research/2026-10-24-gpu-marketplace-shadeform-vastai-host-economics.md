# GPU marketplace check: Shadeform vs Vast.ai hosting on Goliath (2026-10-24)

**Date:** 2026-10-24 (Europe/Vienna)
**Box:** Goliath - Ryzen 9 5900X, RTX 4090 24GB, 64GB RAM, Vienna residential power
**Question:** Can we use shadeform.com? Do they let you rent out your GPU? Does vast.ai work today, and does it beat power + wear?
**Verdict:** Shadeform = consume-only for us. Vast.ai = works, but single home 4090 = lunch money, not a business. Documented so we stop re-asking.

## 1. Shadeform - what it is

- GPU cloud marketplace / broker across 30+ clouds (Lambda, Nebius, DigitalOcean, etc.). No markup - you pay cloud rate.
- One console + REST API + `shade` CLI + hosted MCP server at `https://mcp.shadeform.ai` (header `MCP-SHADEFORM-API-API-KEY-AUTH`).
- Product: plain VMs you SSH into as `shadeform` user, optional startup script / Docker container / persistent volumes.
- Types: on-demand (billed by second), spot (interruptible, cheaper), multi-GPU clusters, reserved commitments.
- Guides in docs: vLLM serving, SkyPilot, lm-eval-harness, Jupyter, UFW, SSH keys.
- Use for us: burst overflow when 4090 is not enough (H100/B200 test, multi-GPU, parallel evals). Local-first stays default.

Refs fetched 2026-10-24: `shadeform.com`, `shadeform.com/prices`, `docs.shadeform.ai`, `docs.shadeform.ai/interfaces/mcp.md`, `getting-started/concepts.md`, `getting-started/faq.md`.

## 2. Shadeform - can we supply our GPU?

Yes, program exists. No, not with Goliath at home.

- Program name: **Flex VMs** - they virtualize partner bare-metal into single-tenant VMs. Same launch API, `flex_vm: true` badge in catalog.
- Enrollment: run a script on your node. See `shadeform.com/flex-vms`.
- Catch (FAQ + Concepts, 2026-10-24):
  > "I'm a GPU provider and want to offer my machines through Shadeform... We currently only work with machines that [are] located in Tier 3 and Tier 4 datacenters. Contact support@shadeform.ai."

So: datacenter/colo bare-metal only. No home-PC sharing model. If we ever colo, then relevant. For monetizing idle Goliath, wrong platform.

Contrast: Vast.ai, Salad, Golem = allow home/workstation hosts. Shadeform = curated providers.

## 3. Vast.ai - does it work today?

Yes. Live marketplace, 2026-10-24 state:

- Claims: 200k+ devs, 20k+ GPUs listed. `vast.ai/hosting` active.
- Model: install client, list hardware, set price / rental type (on-demand, interruptible, reserved), Vast brings customers, handles billing + 24/7 support.
- Host tiers: Data Center / Colo (verified trust label, enterprise deal flow) + GPU farms + single workstation ("from a single workstation to your first rack").
- So single 4090 home host is an explicit supported case, unlike Shadeform.

Pricing seen 2026-10-24 (search receipts, hourly, varies by availability):
- RTX 4090 on-demand: ~$0.35/hr typical (Sept 2026), range $0.136-0.349 (July capture), RunPod $0.34-0.69 for comparison
- RTX 4090 spot / interruptible: from ~$0.14-0.15, wide range $0.08-0.59
- RTX 5090: $0.30-0.60 host earn range quoted by Vast
- Host fee: ~15% internal surcharge (MiningBoard 2026 comparison: RunPod ~7%, Vast ~15%, io.net ~20%) + other sources cite ~25% all-in. Plan on 75-85% net of list.

## 4. Goliath math in Vienna - not a get-rich-quick scheme

Power (Vienna household all-in 2026):
- Median ~0.25 EUR/kWh, VERBUND Klassik 0.30, Eurostat H1 2026 0.326, wholesale Vienna ~0.23. Use **0.30 EUR/kWh** planning.
- Host load: 4090 ~350W + system 100-150W = 0.45-0.5 kW at wall.
- Cost when rented: 0.5 * 0.30 = **~0.15 EUR/hr (~$0.16/hr)**. Idle still ~0.03-0.04/hr.

Profit when rented (example list $0.35 on-demand):
- Net after Vast: $0.35 * 0.8 = ~$0.28
- Minus power $0.16 = **~+$0.11-0.12/hr**

Monthly:
- 100% utilization: 720h * $0.11 = ~$80/mo
- Realistic home single-card (residential IP, no badge, competes with farms): 30-50% fill = **30-50 EUR/mo**
- Race to bottom spot at $0.15 list: $0.15*0.8 - $0.16 = ~zero. You mine for the power company.

Not in spreadsheet:
- Wear: 24/7 at 75-80C = fans, thermal pads, VRAM aging on a ~2000 EUR card. One RMA wipes years of profit.
- Opportunity cost: Goliath is Sandra's daily driver. Rented = unusable. Renters get Docker, need uptime + reliability score or ranking sinks.
- Home costs: heat/noise in flat, upload bandwidth, reboots kill jobs and rating, security exposure of Vast agent on main box.
- Price erosion: 4090 is 2022 silicon, 5090 supply grows, rates drift down.

Rule of thumb: makes sense for farms/colo with cheap power + multi-card + high uptime. Does not make sense to sacrifice workstation for ~lunch money.

If we test anyway: list as interruptible-only, $0.30-0.35, 1-week trial, measure fill rate. No long contracts, no opening firewall beyond Vast client, stop if utilization <40% or temps/noise annoying.

## 5. Decision for fleet

- Shadeform: keep as **consume** option for burst GPU (H100 eval, multi-GPU, vLLM spike). No supply action. Revisit only if we colo bare-metal.
- Vast.ai hosting Goliath 4090: **do not** pursue as income. Optional 1-week experiment only if idle time is truly free.
- This note is the canonical pointer for next "rent out GPU?" ask. No new research needed unless power tariff or Vast fee changes >5pts.

Sources: shadeform.com/llms.txt, /prices, /features/on-demand-instances, /flex-vms, docs.shadeform.ai llms.txt + mcp.md + concepts.md + faq.md; vast.ai/hosting; vast.ai/article/how-much-money-can-you-earn-renting-out-your-gpu; openSERP + DuckDuckGo 2026-10-24 (4090 rates, Vienna 0.23-0.33 EUR/kWh, Vast 15-25% fee).
