---
title: "PRC dual vectors — open-weight AI + GOES transformers"
category: analysis
status: active
audience: mcp-dev
last_updated: 2026-07-21
related:
  - not-mcp-related/general-ai/regions/us-china-race.md
  - not-mcp-related/general-ai/hardware/supply-chain.md
  - models/JACKRONG_DISTILL_FACTORY.md
  - standards/LOCAL_LLM_STANDARDS.md
---

# PRC dual vectors: open weights for the living room, GOES for the grid

Two chokepoints, different layers of the stack. Both reward “as long as Beijing is fine with it.”

## Vector 1 — Open-source / open-weight as soft power (Shenzhen hears Xi)

At the **2026 World AI Conference** (Shanghai, 2026-07-17), Xi’s keynote pushed **open source, openness, collaboration and sharing**, framed AI as a “symphony of international cooperation” rather than a single-country solo, and stood up **WAICO** (World Artificial Intelligence Cooperation Organization). Full text: [Xinhua](https://english.news.cn/20260717/893fe11097db460ea31b98f131e34ef0/c.html).

Fleet read (not press-release read):

- Policy cover for labs and startups to keep shipping **FOSS / open-weight** teachers (DeepSeek, Qwen, Kimi, GLM…).
- Distill factories ([Jackrong](../../../models/JACKRONG_DISTILL_FACTORY.md)) stay legal *inside the PRC industrial system* — self-host the teacher, automate traces, dump 9B/27B GGUFs onto HF.
- Downstream: **consumer GPUs (4090-class) vibecode at zero paid tokens** worldwide. Western closed APIs keep collecting rent; Chinese open-weight + distill collapses marginal cost for everyone who can download weights.
- A thousand Shenzhen ears: openness is not charity — it is **adoption capture** and dependency on the PRC model-supply ecosystem while US policy tries to choke *chips*.

If the state later clamps open weights, the Jackrong lane dies. While the speech holds, expect more FOSS giants → more distills → more zero-paid local agents.

## Vector 2 — Grain-oriented electrical steel (GOES) and the transformer backlog

Separate from silicon: **AI data centers and grid buildouts need step-down / distribution transformers**. Lead times in the US/EU have stretched to **years** (often cited 24–48 months; some DC-class orders into 2027).

Why the bottleneck is metallurgical, not “somebody forgot to order boxes”:

- Transformer cores use **thin sheets of grain-oriented electrical steel (GOES / Hi-B)** — silicon steel processed so magnetic domains align for low-loss cores.
- Capacity is highly concentrated. Credible industry writeups put **China at ~56% of global GOES** (Baowu/Baosteel et al.), not a casual plurality — see [ChinaTalk](https://www.chinatalk.media/p/yes-transformers-are-a-problem) and [Energy Solutions Intelligence](https://energy-solutions.co/reports/ai-grid-transformer-crisis/). (Viral “90%” figures are overstated; **majority + thin Hi-B grades** is the accurate claim.)
- China also holds on the order of **~60% of global transformer manufacturing capacity**, with export books flooded by AI/grid demand.
- US domestic GOES is thin (often one major producer, Cleveland-Cliffs / Butler Works) while tariffs complicate imports — backlog persists even when Chinese mills have steel to sell.

So: Western GPU clusters can clear export-control paperwork and still **wait on iron** — cores that depend on PRC-dominated specialty steel and PRC-dominated transformer shops.

## Why these belong in the same note

| Layer | US choke narrative | PRC counter / mirror |
| --- | --- | --- |
| Compute | ASML / advanced GPUs / EDA | Domestic silicon + efficient MoE |
| Models | Closed API rent + export controls | **Open-weight flood + distill to consumer GPUs** |
| Power delivery | Assume grid/transformers are background | **GOES + transformer capacity as silent brake on AI buildout** |

Open weights make **edge vibecoding** cheap everywhere PRC policy allows FOSS teachers. GOES makes **hyperscale power delivery** slow everywhere transformer steel is scarce. Same country, two levers — ideology/soft power on the model layer, commodity/industrial power on the grid layer.

## Pattern: surprising near-monopolies (industrial policy as compound interest)

GOES is not a one-off. PRC industrial policy has repeatedly picked **mid-tech + scale + patient capital** sectors where Western firms underinvested, then rode cost curves until the rest of the world discovered a multi-year rebuild would be needed. Approximate dominance (order-of-magnitude; recheck before citing in briefs):

| Domain | Rough PRC position | Notes |
| --- | --- | --- |
| Rare earths (mining + refining) | Majority refining; high share of NdFeB magnets | Classic chokepoint; Western mines still send ore east for processing |
| Solar PV (modules, wafers, polysilicon) | ~70–85% of many stages | Energy transition hardware is a PRC supply chain with logos |
| Li-ion batteries (cells + midstream) | Majority of cell capacity; anode/cathode chemicals heavily concentrated | EV + grid storage both sit on this |
| EVs (2 / 3 / 4 wheel) | World’s largest maker + exporter; BYD-class volume | Policy + battery vertical integration |
| Wind turbines | Leading OEM share + tower/nacelle supply | Same “build the factory that builds the factories” play |
| UHV / HVDC power gear | Global leader in UHV lines and converter tech | Domestic grid as learning curve, then export |
| High-speed rail | Largest network + rolling-stock export stack | Decades of standards + volume |
| Transformers + GOES | ~60% transformer capacity; ~56% GOES | AI datacenter grid brake — see above |
| Mature / trailing-edge chips | Large share of ≥28 nm and packaging/OSAT capacity | **Exception:** leading-edge logic ≲5 nm still TSMC/Samsung/Intel + ASML EUV |
| **Humanoid robots + joint actuators** | 100+ Shenzhen startups (platforms + parts) | High-torque mini motors w/ integrated reduction + harmonic / force feedback — **die halbe Miete**; rest is warehouse fab. Buy in Shenzhen → [`robotics/hardware/SHENZHEN_HUMANOID_ACTUATORS.md`](../../../robotics/hardware/SHENZHEN_HUMANOID_ACTUATORS.md) |
| Open-weight AI models + distill GGUFs | Soft power, not factory monopoly | WAIC openness line → Jackrong-style flood onto consumer GPUs |

**Fleet lens:** US/allied narrative obsesses over **sub-5 nm and EUV**. PRC policy also owns the boring layers that make civilization and AI *usable* — power, motors, panels, cells, mid-tier silicon, and now the FOSS model firehose. Future-oriented here means: subsidize learning curves early, accept overcapacity, export the surplus, and let dependents discover the chokepoint only when lead times hit years.

Rubber-duckies optional. Specialty steel and cathode chemistry are not.

## Fleet takeaway

- Prefer local open-weight + distill ([LOCAL_LLM_STANDARDS](../../../standards/LOCAL_LLM_STANDARDS.md), [Jackrong](../../../models/JACKRONG_DISTILL_FACTORY.md)) while the openness line holds.
- Do not assume “more Nvidia” alone equals “more AI capacity” — track transformer/GOES lead times for any serious colo or home-lab power upgrade.
- Correct the meme: **~half to three-fifths of GOES**, not magical 90%, is already enough leverage.
- When surprised by a PRC near-monopoly, ask: *was this a decade of deliberate scale policy while others optimized quarterly EPS?* Usually yes.
