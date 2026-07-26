# DGX Station for Windows — product brief

**Source:** [NVIDIA Newsroom](https://nvidianews.nvidia.com/news/nvidia-dgx-station-for-windows-puts-a-trillion-parameter-ai-supercomputer-on-every-enterprise-desk)  
**Status:** Announced **2026-05-31** (GTC Taipei); **Q4 2026** via OEMs; **no public MSRP**.

---

## Positioning

**Enterprise deskside** AI supercomputer — Windows-managed **agent infrastructure** for orgs that live in Office, CAD, EDA, and LOB apps but today ship heavy AI to **Linux datacenters**.

Marketing: **up to 1 trillion parameters** locally; **hundreds of concurrent agents**; same **OpenShell** + Windows security primitives as RTX Spark tier.

**Not** the affordable product. Expect **~$100k+** system quotes (industry estimates; NVIDIA uses OEM inquiry model).

---

## Silicon and system

| Component | Specification |
|-----------|---------------|
| Superchip | **NVIDIA GB300 Grace Blackwell Ultra Desktop** |
| CPU | **72-core** NVIDIA **Grace** |
| GPU | **Blackwell Ultra** via **NVLink-C2C** to Grace |
| Memory | Up to **748 GB coherent** memory |
| AI peak | Up to **20 petaflops FP4** |
| Optional | **NVIDIA RTX PRO 6000 Blackwell** workstation GPU (viz / sim / physical AI) |
| Network | **ConnectX-8 SuperNIC**, up to **800 Gb/s**; multi-station scale-out |
| OS role | **Windows** primary; **WSL** for Linux AI toolchains |

---

## Workloads (NVIDIA taxonomy)

- **AI agents** — parallel frontier agents wired to Windows apps/workflows  
- **AI development** — pretrain, fine-tune, iterate (with WSL Linux stacks)  
- **Data science** — large in-memory datasets (748 GB pool)  
- **AI inference** — high throughput; trillion-parameter class (marketing)  
- **Physical AI** — GB300 + RTX PRO for sim + perception loops  

---

## Enterprise IT angle

- **Intune / Entra / Defender**-class fleet story (parallel to Spark Secured-core, but workstation scale).  
- Agents run in **managed** environment — policy at system layer via OpenShell + Windows primitives.  
- Scale path: deskside → **datacenter GB300** or cloud without abandoning Windows dev laptops (Spark tier).

---

## Assessment (short)

| Audience | Verdict |
|----------|---------|
| Fortune 500 AI platform team | Evaluate vs. cloud GPU OPEX; strong if **data residency** + Windows LOB integration mandatory |
| Startup / regional uni | **Overkill** unless shared regional facility or grant ≥ €100k |
| Sandra personal | **Lottery / inheritance tier** — correct instinct from prior chat |

**OEMs (Q4 2026):** ASUS, Dell, GIGABYTE, HP, MSI, Supermicro.

---

## Ladder context

| Tier | Product |
|------|---------|
| Personal | RTX Spark / Surface |
| Enterprise deskside | **DGX Station for Windows** |
| Datacenter | GB300 clusters / cloud |

Parent: [COMPUTEX_2026_ASSESSMENT.md](../COMPUTEX_2026_ASSESSMENT.md)
