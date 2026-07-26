# The US-China AI Race: The Great Bifurcation

**Status:** Two incompatible technological civilizations emerging

---

## The New Cold War Nobody Talks About

The competition between the United States and China over artificial
intelligence has become, arguably, the most consequential geopolitical
contest of the 21st century. It's not fought with missiles or troops
but with silicon chips, export controls, and competing visions of how
AI should be developed, governed, and deployed.

The stakes are difficult to overstate. Whoever achieves artificial general
intelligence first—or dominates the infrastructure that makes advanced AI
possible—will hold advantages that could last decades. Economic dominance,
military supremacy, and technological hegemony all flow from AI leadership.

Both sides understand this. Both are acting accordingly.

---

## The American Strategy: Innovate and Choke

US strategy combines two prongs: maintain technological leadership through
private sector innovation while denying China access to the inputs needed
to catch up.

### The Innovation Machine

America's AI advantage isn't government labs—it's a constellation of
private companies with resources and talent that dwarf state-sponsored
alternatives. OpenAI, Google DeepMind, Anthropic, and Meta collectively
employ most of the world's top AI researchers and command research budgets
in the tens of billions.

This wasn't planned. It emerged from decades of venture capital culture,
immigration policy that attracted global talent, and academic institutions
that trained researchers who went on to build companies. The US government
is now trying to support and channel this ecosystem without controlling it.

The risks of this approach are obvious. Private companies pursue profit,
not national interest. They compete with each other as fiercely as with
foreign rivals. Key researchers move between organizations, and some have
left for competitors entirely. But the dynamism this creates has, so far,
kept American AI at the frontier.

### The Chokehold

The other prong is denial. The October 2022 export controls—and subsequent
tightening—represent the most aggressive use of economic statecraft in
decades. The goal is simple: prevent China from acquiring the chips,
manufacturing equipment, and software tools needed to develop advanced AI.

ASML's EUV machines cannot be shipped to China. Nvidia's highest-end GPUs
cannot be sold there. Electronic design automation (EDA) software—needed to
design chips in the first place—faces restrictions. The intent is to create
a technology gap that Chinese innovation cannot close.

Whether this works is contested. Chinese companies are adapting, developing
domestic alternatives, finding workarounds. But the restrictions have
clearly slowed China's progress and forced enormous investments in
indigenous capabilities that might otherwise have gone to other priorities.

### The Infrastructure Push

The third element is reshoring. The OpenAI-Foxconn partnership announced
in late 2025 aims to build AI hardware infrastructure on American soil.
The CHIPS Act poured billions into domestic semiconductor manufacturing.
The goal is to reduce dependence on Asian supply chains—particularly
Taiwan—that could be disrupted by conflict.

This is a long-term play. Building fabs takes years. Training a workforce
takes longer. But the calculation is that AI is too important to depend
on factories 100 miles from China.

---

## The Chinese Strategy: Self-Reliance at All Costs

China's response to American pressure has been what Beijing calls
"self-reliance"—a massive push to build indigenous capabilities across
the entire AI stack, from chips to models to applications.

### The Model-Chip Alliance

The most interesting development is the tight integration between Chinese
AI labs and domestic chip makers. DeepSeek, one of China's leading AI
companies, optimizes its models specifically for Huawei's Ascend chips.
This isn't just adaptation—it's co-design, with model architectures and
chip features evolving together.

This integration bypasses CUDA entirely. CUDA is Nvidia's proprietary
software stack, and its dominance in the West creates lock-in that benefits
American companies. By building an independent software ecosystem—CANN,
MindSpore—China avoids this dependency even if it sacrifices some
performance and convenience.

The result is an AI development environment that shares almost nothing
with Western practice. Code written for one ecosystem doesn't run on the
other. Models trained on Chinese infrastructure can't easily be transferred
to American clouds. The technical stacks are diverging.

### Hardware Indigenization

Huawei's Ascend chips are the flagship, but the broader Chinese
semiconductor industry is scaling rapidly. Baidu's Kunlun chips (M100 for
inference, M300 for training) provide alternatives. Smaller players are
emerging. Government subsidies pour in.

#### Ascend Roadmap (2025–2028)

Huawei revealed a detailed NPU roadmap at Huawei Connect 2025, moving to a
new SIMD+SIMT architecture and proprietary HBM-like memory to bypass US
sanctions on TSMC/EUV/Samsung HBM.

| NPU | Release | Arch | FP8 / FP4 | Memory | Memory Type |
|-----|---------|------|-----------|--------|-------------|
| 910C | Q1 2025 | SIMD | — | 128 GB / 3.2 TB/s | HBM |
| **950PR** | **Q1 2026** | **SIMD+SIMT** | **1 / 2 PF** | **128 GB / 1.6 TB/s** | **HiBL 1.0** (cheap, prefill/rec) |
| **950DT** | **Q4 2026** | **SIMD+SIMT** | **1 / 2 PF** | **144 GB / 4.0 TB/s** | **HiZQ 2.0** (high-perf, training) |
| 960 | Q4 2027 | SIMD+SIMT | 2 / 4 PF | 288 GB / 9.6 TB/s | HiZQ (assumed) |
| 970 | Q4 2028 | SIMD+SIMT | 4 / 8 PF | 288 GB / 14.4 TB/s | TBD |

Key developments:

- **Same silicon, two products** — The 950PR and 950DT are identical compute
  dies (1/2 PF each) differentiated only by memory package. One tape-out,
  two market segments.
- **HiBL 1.0 / HiZQ 2.0** — Huawei's proprietary HBM-like memory, sourced
  domestically (CXMT). Bypasses Samsung/SK Hynix HBM sanctions entirely.
  HiBL is cheap/lower-bandwidth for inference-heavy workloads; HiZQ is
  full-bandwidth for training.
- **UnifiedBus (UB)** — Huawei's own interconnect protocol replaces PCIe,
  Ethernet, and TCP/IP in-datacenter. TB/s-scale, 2.1µs latency. Runs over
  standard Ethernet (UBoE) to reduce hardware costs.
- **Atlas 950 SuperCluster** — "Hundreds of thousands" of 950DT APUs, hitting
  1 ZettaFLOPS FP4. This is already deployable.

The 950DT is notable for being the chip DeepSeek V4 (1.6T parameters) was
reportedly trained on — a full-stack Chinese AI: Huawei silicon + CANN
runtime + DeepSeek model, zero US technology involved.

Source: [Tom's Hardware — Dec 2025](https://www.tomshardware.com/tech-industry/artificial-intelligence/huawei-ascend-npu-roadmap-examined-company-targets-4-zettaflops-fp4-performance-by-2028-amid-manufacturing-constraints)

### Science Leadership

Perhaps most significantly, China now leads in "AI for Science"
publications. Research applying AI to materials science, biology, physics,
and chemistry increasingly originates from Chinese institutions. The
2035 plan explicitly targets becoming the world's primary AI innovation
center.

This matters because scientific AI applications may be more strategically
important than consumer chatbots. AlphaFold's protein structure predictions
have implications for drug development and synthetic biology. Similar
breakthroughs in materials science or energy could confer advantages that
last decades.

China is betting that fundamental research will pay off even if consumer
AI remains a Western specialty.

---

## The European Position: Regulate and Compute

Europe occupies an uncomfortable middle ground. Unable to compete with
American innovation or Chinese scale, the EU has chosen a different
strategy: become the regulatory superpower while building enough compute
infrastructure to maintain sovereignty.

### The Brussels Effect

The EU AI Act, fully enforced in 2025, represents the most comprehensive
AI regulation anywhere. The "risk-based approach" bans certain applications
outright (social credit scoring, mass biometric surveillance) while
imposing heavy compliance requirements on high-risk uses and transparency
obligations on foundation model providers.

The theory is the "Brussels Effect"—global companies will adopt EU standards
everywhere because maintaining separate versions for different markets is
too expensive. This worked for GDPR and might work for AI. If OpenAI and
Google comply with EU rules to access European markets, EU values shape
global AI development.

The risk is brain drain. Compliance costs are real. Some startups relocate
to the US or UK rather than navigate European regulation. The balance
between protecting citizens and enabling innovation remains contested.

### Sovereign Compute

Europe is also building computational capacity. Jupiter, Germany's exascale
supercomputer, came online in mid-2025. Groq built inference infrastructure
in Helsinki, attracted by European power costs and regulatory environment.
The EU Chips Act 2.0 proposes €20 billion+ in funding to support ASML and
expand European manufacturing.

This isn't about matching American or Chinese scale—that's impossible with
European resources and coordination challenges. It's about maintaining
enough capacity to avoid complete dependence on foreign infrastructure.

---

## The Bifurcation Accelerates

Despite—or perhaps because of—export controls, the global AI ecosystem
is splitting into incompatible halves.

### Technical Divergence

Western AI runs on Nvidia GPUs, uses CUDA libraries, trains on English-
dominated data, and deploys through American cloud providers. Chinese AI
runs on Huawei/Baidu chips, uses CANN/MindSpore frameworks, trains on
Chinese data, and deploys through domestic clouds.

A model trained on one stack doesn't easily transfer to the other. A
researcher skilled in one ecosystem needs retraining for the other. The
technical communities are separating.

### Value Divergence

More fundamentally, the two ecosystems encode different values. Chinese
AI must reflect "core socialist values" and is vetted by state censors.
American AI tends toward liberal assumptions about free speech and
individual agency. Neither set of values is universal.

A Chinese AI won't discuss Tiananmen Square. An American AI won't refuse
to discuss democracy. When these systems interact—through translation,
through trade, through any global application—the value conflicts surface.

### The Control Theater Continues

Export controls haven't stopped Chinese AI development. Smuggling markets
exist. Cloud renting provides workarounds. Architectural innovations
(mixture-of-experts, efficient inference techniques) reduce the compute
needed for frontier results.

But the controls have forced China onto an independent trajectory. The
bifurcation isn't an unintended consequence of American policy—it's the
outcome, perhaps the goal. Two separate technological civilizations, with
different hardware, different software, different values, competing for
different futures.

We are watching the technological equivalent of the Reformation: a unified
system fragmenting into competing alternatives, each claiming legitimacy,
neither able to defeat the other.

---

## Dual vectors worth tracking (2026 addendum)

Beyond chip export controls, watch two PRC levers that do not show up in CUDA benchmarks:

1. **Open-weight soft power** — state-backed rhetoric for open source / collaboration (WAIC 2026) → FOSS teachers + distill factories → consumer GPUs run serious agents at zero token rent.
2. **GOES / transformer hard power** — majority share of grain-oriented electrical steel and transformer capacity → multi-year backlogs for the grid gear AI clusters need.

Full note: [prc-dual-vectors-openweights-and-goes.md](./prc-dual-vectors-openweights-and-goes.md).

## Where This Goes

The immediate future is continued competition. Neither side shows any
inclination to negotiate limits. The race continues.

The medium-term future probably involves crisis. Taiwan sits at the
intersection of these competing systems—manufacturing Western chips,
claimed by China, defended by America. Any conflict there would
simultaneously be an AI crisis, a semiconductor crisis, and a potential
great-power war.

The long-term future is genuinely uncertain. Does one side achieve
decisive advantage? Do both develop AGI around the same time, creating
a mutual deterrence dynamic? Does some catastrophic accident—AI-enabled
weapon gone wrong, autonomous system out of control—force cooperation?

Nobody knows. But the race is real, the stakes are existential, and the
bifurcation is accelerating. Two versions of the AI future are being
built simultaneously. Eventually, one will dominate—or they'll have to
learn to coexist.
