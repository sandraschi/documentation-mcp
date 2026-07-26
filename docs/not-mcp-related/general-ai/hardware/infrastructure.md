# AI Infrastructure: The Gigawatt Era

**Status:** When datacenters become power plants

---

## The Wall We've Hit

AI scaling laws have driven progress for years: more compute produces
better models. Double the training compute, get measurably better results.
This has held with remarkable consistency through GPT-2 to GPT-3 to GPT-4
to the current generation.

But scaling laws run into physical constraints. The current constraint
isn't algorithms or data or even chip supply. It's electricity.

Training a GPT-5 class model consumes gigawatt-hours of energy—comparable
to the annual electricity consumption of small cities. Running inference
at scale (the billions of API calls that make AI useful) requires sustained
power that existing grid infrastructure cannot reliably provide.

The hyperscalers have discovered that the limiting factor for AI ambitions
is often the power company. US and EU grids are congested, aging, and have
multi-year waitlists for new industrial connections. You can have the
budget for a million GPUs and nowhere to plug them in.

This has driven a fundamental shift in how AI infrastructure is built.

---

## The Nuclear Renaissance

The tech giants have concluded that depending on grid utilities is
unacceptable. Their solution: generate your own power, preferably nuclear.

### Microsoft x Constellation

In 2024, Microsoft signed a 20-year power purchase agreement to restart
Three Mile Island Unit 1—yes, the reactor next to the one that partially
melted down in 1979. The restarted plant will be dedicated entirely to
Microsoft data centers.

This isn't green virtue signaling. It's hard-nosed infrastructure planning.
Nuclear provides reliable baseload power at scales relevant to AI training.
The Three Mile Island deal gives Microsoft approximately 835 megawatts of
guaranteed capacity independent of grid constraints.

### Amazon's Direct Connection

AWS took a different approach: buying a data center campus physically
connected to the Susquehanna nuclear plant in Pennsylvania. No grid
intermediary. Direct power from reactor to servers.

This solves the grid congestion problem by eliminating the grid entirely.
It also demonstrates how seriously hyperscalers take power security—they're
willing to spend billions on captive generation rather than depend on
utilities.

### Google's SMR Bet

Google is investing in Small Modular Reactors (SMRs) through a deal with
Kairos Power, targeting deployment by 2030. SMRs promise faster construction
and more flexible siting than traditional nuclear plants.

Whether SMRs can deliver on their promise remains uncertain—no commercial
SMR has reached full operation yet. But the investment signals where Google
sees the infrastructure future heading.

### The Pattern

The pattern is clear: AI compute is so power-hungry, and power supply so
constrained, that the largest tech companies are essentially becoming
power companies. They're building or buying generation capacity at scales
that would have seemed absurd a decade ago.

This has implications beyond AI. Nuclear plants that might otherwise be
decommissioned are finding new life powering data centers. Energy policy
and AI policy are becoming entangled in ways policymakers haven't fully
grasped.

---

## The Superclusters: Compute Cities

The scale of AI infrastructure has evolved from "data centers" to something
more like "compute cities"—concentrated installations that rival industrial
facilities in size and power consumption.

### Project Horizon (West Texas)

Poolside—or whoever ends up operating this facility—is building a 2-gigawatt
AI compute campus in West Texas. To put that in perspective: 2 gigawatts
is enough to power roughly 1.5 million American homes. This single facility
will consume more electricity than many small countries.

The location isn't random. West Texas has abundant land, relatively cheap
power (from wind and natural gas), and minimal interference from the grid
congestion plaguing coastal regions. The concept is "Stargate-level"
infrastructure—named after OpenAI's own massive compute ambitions.

The installation will house over 100,000 GPUs. The cooling requirements
are enormous. The network infrastructure to connect those GPUs operates
at bandwidths that would have seemed impossible a few years ago.

### xAI Colossus (Memphis)

Elon Musk's xAI built "Colossus" in Memphis in 19 days—a feat that sounds
impossible until you realize it meant deploying containerized, pre-built
compute modules rather than constructing a traditional data center.

The initial deployment: 100,000 H100 GPUs. The expansion target: 300,000
B200 GPUs by 2025. The water consumption for cooling has driven local
infrastructure upgrades that the surrounding community is still processing.

Speed matters when you're racing for AGI. xAI apparently decided that
conventional construction timelines were unacceptable.

### Huawei Atlas 950 Cluster (China)

China's answer to Western superclusters takes a different approach. Cut off
from the most advanced Western chips, they compensate with scale: over
500,000 Ascend NPUs networked together.

The domestic chips are individually less powerful than Nvidia's best. But
"less powerful" at that scale still adds up to extraordinary aggregate
capability. The architecture suggests China has concluded that scale can
compensate for per-chip performance—at least well enough to stay competitive.

---

## Cooling: The Thermal Wall

Advanced AI chips don't just consume electricity. They convert it to heat.
An Nvidia Blackwell GPU draws over 1000 watts—think of a small space heater
running continuously. Multiply that by tens of thousands of chips in a
single facility.

Traditional air conditioning cannot cope. The future of AI infrastructure
is liquid-cooled.

### Direct-to-Chip Cooling

The current standard for high-end deployments involves cold plates that
sit directly on the GPU die. Liquid circulates through the plates, carrying
heat away far more efficiently than air ever could.

Nvidia Blackwell essentially requires this approach. The chips cannot run
at full performance with air cooling. The thermal design power exceeds
what any air-based system can dissipate.

### Immersion Cooling

The next evolution submerges entire server racks in dielectric fluid—
specialized liquids that conduct heat but not electricity. In two-phase
systems, the fluid boils at contact with hot components, carrying heat
away as it vaporizes, then condenses and returns.

Immersion cooling eliminates the massive fans that consume significant
energy in traditional data centers. Efficiency gains of 30% or more are
possible. The approach also enables higher compute density—you can pack
more chips into smaller spaces when cooling isn't constrained by airflow
requirements.

The downside: immersion systems are more complex to maintain. You can't
just swap out a failed component; you're reaching into a tank of fluid.
The operational practices are different from anything traditional IT
infrastructure teams are trained for.

---

## The Sovereignty Cloud Fragmentation

AI infrastructure is fragmenting along geopolitical lines, not just for
competitive reasons but for sovereignty concerns.

### European Sovereign Clouds

The EU is explicitly building compute infrastructure designed to keep data
out of US and Chinese jurisdictions. Orange, T-Systems, and others are
constructing "sovereign clouds" that comply with European data protection
requirements and operate under European legal frameworks.

The motivation is GDPR compliance and strategic autonomy. If European AI
development depends on American or Chinese infrastructure, European values
and regulations become unenforceable. Building domestic capacity is
expensive but maintains sovereignty.

### Gulf State Compute Ambitions

The UAE (through G42) and Saudi Arabia are building massive compute
installations, positioning themselves as AI infrastructure hubs. Their
strategy: play the US and China against each other for chip access,
accumulate compute capacity, and monetize it to the highest bidder.

Geography matters here. The Gulf states offer cheap energy (from hydrocarbons),
available land, and political frameworks that accommodate both Western and
Chinese business relationships. They're aiming to become the Switzerland
of AI compute.

Whether this works depends on continued chip access, which depends on
navigating US export controls, which depends on geopolitics that could
shift at any moment.

---

## What This Means

The era of AI infrastructure as "just another IT workload" is over. The
power requirements, cooling demands, and capital costs have pushed AI
compute into a category of its own—closer to industrial infrastructure
than to traditional data centers.

The companies that win the AI race will be the ones that solve the
infrastructure problem. Building the best models doesn't matter if you
can't power the training runs. Having the best chips doesn't matter if
you can't cool them.

This creates advantages for incumbents with existing infrastructure
relationships and capital access. It creates barriers for startups that
might have algorithmic innovations but lack the resources to build
gigawatt-scale facilities. It creates geopolitical leverage for regions
that can offer power, land, and regulatory accommodation.

The AI revolution isn't just a software revolution. It's an infrastructure
revolution, with all the physical constraints and capital requirements
that implies.

Follow the power lines. That's where the future is being built.
