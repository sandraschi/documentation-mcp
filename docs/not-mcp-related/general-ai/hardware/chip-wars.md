# AI Hardware: The Chip Wars

**Status:** The real battle for AI supremacy is fought in silicon fabs

---

## The Chokepoint Economy

Software gets the headlines, but hardware decides who wins. The ability to
train and run AI models depends entirely on access to specialized chips—
and that access is controlled by a remarkably small number of chokepoints.

One company in the Netherlands makes the machines that make advanced chips.
One foundry in Taiwan manufactures most of them. One American company
dominates the software stack that runs on them.

Whoever controls these chokepoints controls AI. The geopolitical implications
are staggering.

---

## The Western Stack

### Nvidia: The Incumbent Emperor

Nvidia's dominance in AI compute is difficult to overstate. The company
doesn't just lead the market—it effectively is the market. Every major AI
lab, every hyperscaler, every startup racing to build the next breakthrough
runs on Nvidia GPUs.

The moat isn't the hardware itself, impressive as it is. The moat is CUDA—
Nvidia's proprietary software stack that has become the lingua franca of AI
development. Decades of libraries, tools, and optimizations lock developers
into the ecosystem. Switching costs are enormous.

**The Rubin Architecture** (announced March 2025, expected late 2026)
represents Nvidia's next generation. The Vera Rubin CPU paired with
Blackwell Ultra GPUs promises another leap in performance and efficiency.
Jensen Huang's leather-jacket keynotes have become industry-defining events,
and the roadmap extends years into the future.

The strategy is straightforward: maintain lock-in through CUDA while
expanding into adjacent markets. Project GR00T targets embodied AI—robots
and physical systems. The more domains Nvidia dominates, the harder it
becomes for alternatives to gain traction.

But even emperors face challenges.

### Google TPU: The Only Real Alternative

Google's Tensor Processing Units represent the only mature alternative to
Nvidia at scale. Unlike startups promising future competition, Google is
already running production workloads—including Gemini 3 training—on TPUs.

#### What Is a TPU?

A TPU is an **ASIC** (Application-Specific Integrated Circuit)—custom silicon
designed for one purpose: matrix multiplication for neural networks. Unlike
GPUs, which evolved from graphics and retain general-purpose flexibility,
TPUs sacrifice versatility for raw efficiency at their specific task.

**The key architectural difference: Systolic Arrays**

GPUs use thousands of small cores that can each do independent work. TPUs use
**systolic arrays**—a grid of processing elements where data flows through in
waves, like blood pulsing through the heart (hence "systolic"). Each element
performs a multiply-accumulate and passes results to neighbors.

```
Data flows →
    ↓ ↓ ↓ ↓
  [●→●→●→●]  ← Weights loaded once
  [●→●→●→●]     Data streams through
  [●→●→●→●]     Results accumulate
  [●→●→●→●]
```

This is brutally efficient for matrix multiplication—the core operation of
neural networks—but useless for general computation. A TPU can't render
graphics or run arbitrary code. It does one thing, extremely well.

#### TPU Generations

| Generation | Year | Key Feature | Used For |
|------------|------|-------------|----------|
| TPU v1 | 2016 | Inference only | Internal Google services |
| TPU v2 | 2017 | Training support, HBM | First Cloud TPUs |
| TPU v3 | 2018 | Liquid cooling, 420 TFLOPS | Large model training |
| TPU v4 | 2021 | 4096-chip pods, optical interconnect | PaLM, Gemini 1 |
| TPU v5e | 2023 | Cost-optimized inference | Production serving |
| TPU v5p | 2023 | Training-optimized | Gemini 1.5 |
| **TPU v6 (Trillium)** | 2024 | 4.7x v5e performance | Gemini 2/3 |

Each generation roughly doubled performance while improving efficiency. The
v4 pods—interconnected clusters of 4096 chips—were among the largest AI
supercomputers ever built. TPU v6 "Trillium" powers the current Gemini 3 era.

#### bfloat16: Google's Gift to AI

Google invented **bfloat16** (brain floating point) for TPUs, and it became
an industry standard. The insight: neural networks don't need the precision
of standard FP32, but FP16's limited range causes training instability.

| Format | Bits | Exponent | Mantissa | Range |
|--------|------|----------|----------|-------|
| FP32 | 32 | 8 | 23 | Huge |
| FP16 | 16 | 5 | 10 | Limited (overflows) |
| **bfloat16** | 16 | 8 | 7 | Same as FP32 |

bfloat16 keeps FP32's range (8-bit exponent) but truncates precision (7-bit
mantissa). Neural networks tolerate the precision loss; they can't tolerate
overflow. This format is now standard across TPUs, Nvidia GPUs, and others.

#### JAX: Google's PyTorch Alternative

TPUs need software. Nvidia has CUDA and PyTorch. Google built **JAX**.

**What JAX is:**
- NumPy-like API (familiar to scientists)
- Automatic differentiation (like PyTorch autograd)
- **XLA compilation** (optimizes for TPU/GPU)
- Functional programming style (no hidden state)

**Why JAX matters:**

```python
# JAX code looks like NumPy
import jax.numpy as jnp
from jax import grad, jit, vmap

def loss(params, x, y):
    pred = jnp.dot(x, params)
    return jnp.mean((pred - y) ** 2)

# But you get automatic gradients
grad_loss = grad(loss)

# And automatic compilation to TPU/GPU
fast_grad = jit(grad_loss)

# And automatic vectorization
batched_grad = vmap(grad_loss)
```

JAX's functional style (no mutable state, explicit randomness) makes it
easier to compile efficiently and distribute across TPU pods. PyTorch's
imperative style is more intuitive but harder to optimize.

**The ecosystem split:**
- **PyTorch** → Nvidia GPUs → Most of industry, academia
- **JAX** → Google TPUs → Google internal, DeepMind, some researchers

Google trains Gemini on JAX/TPU. Most startups train on PyTorch/Nvidia.
This creates two parallel ecosystems with limited code portability.

#### The Vertical Integration Advantage

Google controls the entire stack:

```
Applications (Search, Gmail, Android)
         ↓
    Models (Gemini)
         ↓
   Framework (JAX)
         ↓
   Compiler (XLA)
         ↓
    Hardware (TPU)
```

This means optimization at every level. When Google's compiler team finds
a better way to map operations to TPU silicon, Gemini immediately benefits.
Nvidia customers wait for driver updates; Google ships the fix.

#### The Availability Limitation

**You can't buy TPUs.** Google doesn't sell them.

Options for using TPUs:
- **Google Cloud TPU** — rent by the hour
- **Colab/Kaggle** — free tier with TPU access
- **Google Research partnerships** — for academics

This limits adoption. A startup can buy Nvidia GPUs and own them forever.
TPU access depends on Google's pricing and availability. For Google itself,
this is fine—they have infinite TPUs. For everyone else, it's a constraint.

#### November 2025 Status

TPU v6 (Trillium) powers the "Google Unleashed" era. Gemini 3 training ran
on TPU pods. Inference for Search, Gmail, and all Google products runs on
TPUs. Google Cloud offers Trillium instances for external customers.

The TPU/JAX stack is the only proven alternative to Nvidia/CUDA at frontier
scale. Everyone else is promising future competition; Google is shipping.

#### The Meta Rumors: Google Enters the Hardware Business?

Persistent rumors in late 2025 suggest **Meta is negotiating with Google**
for large-scale TPU access—potentially purchasing or long-term leasing TPUs
for their hyperscale datacenters, alongside their existing Nvidia fleet.

**If true, this would be seismic:**

- Google would become a **chip vendor**, not just a cloud provider
- Meta would gain access to a non-Nvidia alternative at scale
- Nvidia's monopoly pricing power would face real pressure
- The "you can't buy TPUs" limitation would end for mega-customers

**Why Meta would want this:**
- Diversify away from Nvidia dependency
- TPUs excel at transformer inference (Meta runs Llama at massive scale)
- Negotiating leverage against Nvidia's pricing
- Hedge against supply constraints

**Why Google might sell:**
- Revenue from otherwise idle TPU capacity
- Weaken Nvidia's monopoly (enemy of my enemy)
- Establish TPU/JAX as industry standard, not just Google internal
- Meta's scale would validate TPU for external use

**Unconfirmed** as of late November 2025, but the logic is compelling. If
Google starts selling TPUs to hyperscalers, Jensen Huang's monopoly rent
faces its first serious threat. Watch this space.

### The Specialist Insurgents

Several companies are attacking Nvidia's dominance from specialized niches:

**Cerebras** went maximalist. Their Wafer Scale Engine 3 is literally the
size of a silicon wafer—900,000 cores on a single chip. The result is
extraordinary for specific workloads. They claim to train Llama2-70B in
a single day. The limitation is that not every workload fits the architecture.

**Groq** focused on inference speed. Their Language Processing Unit (LPU)
isn't for training models—it's for running them, fast. The Helsinki data
center announced in November 2025 targets the growing market for inference
at scale. Training happens once; inference happens billions of times.

**Qualcomm** is coming from mobile. Their AI200/AI250 inference accelerators
target the data center market, leveraging expertise built for smartphones
where power efficiency is existential.

None of these challengers threaten Nvidia's dominance today. But they
demonstrate that the moat has cracks. CUDA lock-in is real but not absolute.

---

## The Eastern Stack: China's Forced Independence

US export controls—particularly the October 2022 restrictions and subsequent
tightening—forced China into a "Sputnik moment." Cut off from leading-edge
Nvidia chips, Chinese companies had no choice but to develop domestic
alternatives.

The result has been impressive.

### Huawei: The National Champion

Huawei's transformation from telecommunications equipment maker to AI chip
leader illustrates what happens when a nation-state focuses its resources
on a strategic technology.

The **Atlas 950 SuperCluster** (announced September 2025) aggregates over
500,000 Ascend 950DT accelerators. The claimed performance—1 FP4 ZettaFLOPS
for inference, 524 FP8 ExaFLOPS for training—would rival any Western
installation if verified.

More important than raw performance is the **CANN** (Compute Architecture
for Neural Networks) software ecosystem. This is China's answer to CUDA—a
complete stack that allows developers to write AI code without depending
on American technology.

The software isn't as mature as CUDA. The tools aren't as polished. The
community isn't as large. But it works, and it's improving rapidly. Each
generation closes more of the gap.

### The Self-Sufficiency Drive

Huawei isn't alone. Baidu's Kunlun chips (M100 for inference, M300 for
training) provide alternatives within the Chinese ecosystem. Smaller players
are emerging. The investment levels are enormous—this is a strategic priority
for the Chinese state.

The goal isn't matching Western performance chip-for-chip. It's building a
complete, independent stack that allows Chinese AI development to continue
regardless of American policy. On that metric, they're succeeding.

---

## The Manufacturing Chokepoints

### TSMC: The Indispensable Foundry

Taiwan Semiconductor Manufacturing Company fabricates the majority of the
world's most advanced chips. Nvidia designs GPUs, but TSMC makes them.
Apple designs processors, but TSMC makes them. The pattern holds across
the industry.

This concentration of manufacturing capability in one company, on one
island, in the middle of escalating US-China tensions, is one of the most
consequential geopolitical facts of our time.

A Chinese military action against Taiwan wouldn't just be a humanitarian
catastrophe. It would cripple global chip supply for years. The AI
development trajectory of every major player depends on a factory sitting
100 miles from mainland China.

TSMC is building fabs in Arizona and Japan, but advanced production
remains concentrated in Taiwan. The diversification will take years.

### ASML: The Bottleneck's Bottleneck

One step further up the supply chain sits ASML, a Dutch company that makes
the machines that make advanced chips. Specifically, their Extreme
Ultraviolet (EUV) lithography systems are required for manufacturing at
the smallest process nodes.

No ASML machine, no advanced chips. Period.

The company has a complete monopoly on EUV technology. They spent decades
and tens of billions of dollars developing it. No competitor is close.

Export controls on ASML equipment are arguably more important than controls
on chips themselves. China can design chips. China can build older fabs.
But without EUV machines—which the Netherlands, under US pressure, refuses
to export—China cannot manufacture leading-edge chips domestically.

High-NA EUV (the next generation, enabling sub-2nm processes) tightens this
bottleneck further. The machines cost hundreds of millions of dollars each.
ASML can't build them fast enough to meet demand.

---

## The Scramble for Sovereignty

### US Reshoring

The concentration of chip manufacturing in Asia has become a national
security concern for the United States. The CHIPS Act allocated billions
for domestic semiconductor production. Intel, TSMC, Samsung, and others
are building American fabs.

The **OpenAI-Foxconn partnership** (November 2025) represents a different
approach: rather than manufacturing chips, building the data center
infrastructure within US borders. If you can't control chip fabrication,
at least control where the chips end up.

**Project Horizon** in West Texas exemplifies the scale of ambition: a
2-gigawatt AI compute campus with tens of thousands of Nvidia GB300 NVL72
GPUs. Vertical integration of power generation (possibly nuclear) with
compute deployment. The hyperscalers are building infrastructure at scales
that make traditional data centers look quaint.

### The Bifurcation Accelerates

The net effect of all this is an accelerating split between Western and
Chinese AI ecosystems. Each side is building self-sufficient stacks:
hardware, software, models, applications.

The Western stack runs on Nvidia (or Google TPU) hardware, CUDA (or JAX)
software, and models trained on English-dominated data.

The Eastern stack runs on Huawei (or Baidu) hardware, CANN (or MindSpore)
software, and models trained on Chinese data.

Cross-compatibility is decreasing. Code written for one stack doesn't run
on the other. Models trained in one ecosystem don't easily transfer.
The AI world is bifurcating the way the internet bifurcated, with two
separate technological realities emerging.

---

## What This Means

The chip wars aren't a sideshow to AI development. They're the foundation
on which everything else rests. Model architectures can be copied. Training
techniques can be published. But physical manufacturing requires physical
infrastructure that takes decades and hundreds of billions of dollars to
build.

The countries and companies that control chip production will control AI
development. The concentration of that control in a few vulnerable
chokepoints—a Dutch company's machines, a Taiwanese foundry, an American
software stack—creates systemic risks that most people haven't begun to
grapple with.

A war over Taiwan wouldn't just be about territory. It would be about who
controls the technological trajectory of the twenty-first century.

The chips are the thing.
