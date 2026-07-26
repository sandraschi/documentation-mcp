# Fantasy Chains (requires capability/hardware the fleet doesn't have — dated, not dismissed)

Per [`README.md`](./README.md) template — full form, since these are the ones worth actually thinking through.

---

### Bumi fetches a beer, discovers a sensor problem, designs a PCB, gets it fabbed, assembles it, and files a patent

**Tier:** fantasy
**One-line pitch:** the maximal version of "recombinant capability" (see `POL_AND_RECOMBINANT_CAPABILITIES.md`) — a single robot errand cascades into original IP, filed autonomously. Sandra's own framing: "for 2035, haha." Taking the haha seriously enough to trace what "not haha" would actually require.

#### 1. Step chain (TODO list, with an honest existence-check per step)

1. **Bumi navigates to the fridge and opens it** — needs: reliable indoor SLAM/nav (yahboom's ROS2 bridge pattern, extended from wheeled-Boomy to bipedal-Bumi — NOT a small port, Bumi has entirely different locomotion dynamics), object recognition (beer bottle vs. everything else in a fridge — solvable today with existing CV, this is the easy part), and **a gripper with actual dexterity** (Bumi as currently speced is a ~94cm/12kg humanoid; whether it ships with anything beyond a simple end-effector is a hardware question, not a software one — check the actual spec before assuming a gripper exists at all).
2. **Bumi carries the beer back** — needs: balance/gait control robust enough to carry a shifting liquid load without faceplanting. This is where most affordable humanoids in 2026 are still visibly bad; the "carrying a full glass of water without spilling" demo is a genuine research bar, not a solved problem.
3. **Bumi "discovers a sensor problem"** — vague on purpose in the original pitch; the honest version is Bumi's own IMU or a yahboom-class sensor degrading and Fritz's `fritz_surveil` (deep analysis §1) flagging a `fleet`-domain anomaly. This step is actually the MOST plausible one on the list, because it's just `fritz_surveil` doing exactly what it's already scoped to do.
4. **Design a custom sensor PCB** — needs: `kicad-mcp` (does not exist yet, flagged as a real backlog candidate in the deep analysis §2.3.1 correction). Schematic capture for a simple breakout board is genuinely buildable software; **novel-enough-to-be-original circuit design** (as opposed to "wire an off-the-shelf IMU breakout the standard way") is a much higher bar — most sensor problems are solved by buying the right existing board, not inventing a new one. This step's fantasy-ness is less "the tool doesn't exist" and more "there's rarely a real reason to design a novel PCB when one already exists to buy."
5. **Order it from a PCB fab** — needs: a fab API integration (JLCPCB, PCBWay, OSH Park all have order APIs of varying quality) — **this step is actually NOT fantasy tier on its own.** Automated Gerber-file submission and ordering is a solved problem today; if kicad-mcp existed, this step could ship almost immediately after it. Correctly the least fantastical link in the chain.
6. **A dexterous hand assembles and solders SMD components** — this is the hardest single step in the entire list, harder than everything else combined. Robotic SMD assembly at hobbyist scale is a genuinely unsolved general problem — pick-and-place machines exist but are fixed-purpose industrial tools, not general dexterous hands improvising an assembly. A humanoid hand doing this reliably is a legitimate multi-year robotics research problem, not a "buy better hardware" problem. This is the load-bearing fantasy element; everything else on this list is closer to real than this step is.
7. **Test the assembled board** — needs: Messwarte-class bench-instrument integration (iOS backlog §5.6, also not built) — oscilloscope/multimeter MCP wrappers already exist per that entry's framing, so this step inherits Messwarte's honest "verify which bench servers are actually production vs. scaffold" caveat.
8. **File a patent** — needs: a patent-office e-filing API (these genuinely exist — USPTO has EFS-Web/Patent Center APIs, EPO has OPS) — so the *filing mechanics* aren't fantasy. What's fantasy is the idea that an autonomous pipeline should file without a patent attorney and a human inventor decision in the loop. This step should ALWAYS require an admiral-mcp approval gate (per the fleet's own action-permission hierarchy) even in the year this becomes technically possible — patent filing is an irreversible, legally consequential, expensive action, textbook "explicit permission required," never "regular."

#### 2. Feasibility / gap analysis

| Step | Exists today? | Real blocker |
|---|---|---|
| Navigate + open fridge | Partial (nav pattern exists for Boomy, not Bumi) | Bipedal locomotion + gripper hardware |
| Carry liquid without spilling | No | Balance/gait control — genuine research bar |
| Detect anomaly | **Yes, essentially** | `fritz_surveil` already scoped for this class of thing |
| Design PCB | No | kicad-mcp doesn't exist; also rarely the right solution vs. buying a board |
| Order from fab | **Nearly yes** | Just needs kicad-mcp to exist; fab APIs are mature |
| Robotic SMD assembly | No, and not close | The actual hard research problem in this whole chain |
| Bench test | Partial | Messwarte's bench-server inventory needs a truth pass |
| File patent | Mechanically yes, procedurally no | Should always stay human-gated regardless of automatability |

**Hardest single point of failure, fleet-wide honesty:** step 6. Everything else on this list is either already-real, plausibly-buildable-with-existing-fleet-patterns, or deliberately-kept-human-gated. Robotic fine manipulation for SMD assembly is the one item that isn't a fleet engineering problem at all — it's a robotics-research-frontier problem that money alone (even lottery money) may not solve by 2035 depending on how the field moves. Worth being honest that this is the item that could just... not happen on schedule, unlike the hardware-cost-gated items elsewhere in the fleet's aspirations.

#### 3. Effort estimate

Not before ~2032–2035, contingent on: (a) affordable dexterous-hand hardware reaching a capability level that doesn't currently exist in the consumer/prosumer market at any price, (b) Bumi-class humanoids gaining reliable bipedal carrying/balance, (c) kicad-mcp existing (this part is genuinely a few days of normal fleet work, whenever it's briefed), (d) Sandra deciding this is worth doing instead of just buying whatever board fixes the actual sensor problem, which — read honestly — is what a rational person does today and probably still would in 2035.

#### 4. Revenue potential

The joke premise (patent → product → sale) is worth taking at face value for a moment: IF the chain ever produced something genuinely novel and useful (a sensor board solving a real problem no off-the-shelf part solves), a filed patent is a real asset — licensing revenue, or the design itself sold as an open-hardware kit. But the honest read: the *reason* to build this chain would almost never be "we need a patent," it'd be curiosity in the pipeline itself. Revenue is a plausible side effect of a genuinely good outcome, not a reason to build it.

#### 5. Notes

This entry works partly because it's funny and partly because tracing it seriously turns out to be a good stress test of the whole fleet's honesty culture: it forces naming, per step, "is this real, is this buildable, or is this actually hard" — rather than the more common failure mode of hand-waving a whole ambitious idea as "just needs more integration work." Worth reusing this per-step existence-check format for other fantasy entries.

---

### Unitree G1 + real BCI, direct motor control

**Tier:** fantasy
**Pitch:** the robot-companion dream from earlier this session, chained through an actual brain-computer interface instead of a phone app or voice command.

#### 1. Step chain
1. openbci-mcp (dormant, see `POL_AND_RECOMBINANT_CAPABILITIES.md` §2) — EEG signal capture, needs affordable skull-sensor caps that don't exist yet at usable quality/price.
2. Intent decoding — band-power/pattern classification into discrete commands (openbci-mcp already has band-power OSC triggers; this is the closest-to-real piece).
3. Command dispatch via osc-mcp (already the fleet's universal actuator transport, per the recombinant-capabilities doc's observation that osc-mcp keeps being the shared final hop).
4. unitree-mcp — **already exists**, simulation side (Go2/H1/H1-2/G1/B2 via MuJoCo + ROS 2, 12 tests, per FLEET_INDEX). Real G1 hardware control would extend this from sim to physical.

#### 2. Feasibility / gap analysis
The simulation half of this chain is already built and tested TODAY. What's missing is entirely on the hardware-affordability side (real G1, real usable BCI), not the software side. This is the cleanest example in the whole catalog of "the fleet is ready; the world isn't affordable yet."

#### 3. Effort estimate
Software: could be prototyped in simulation now, cheaply, using unitree-mcp as-is with openbci-mcp's existing OSC triggers as a stand-in intent source. Hardware: 2030+, contingent on both G1-class hardware and BCI caps reaching consumer affordability — genuinely two separate bets, not one.

#### 4. Revenue potential
None contemplated — personal-use aspiration.

#### 5. Notes
Worth actually prototyping the SIMULATION version of this soon — openbci-mcp's OSC triggers driving unitree-mcp's simulated G1 in MuJoCo is buildable with zero new hardware, today, and would be a genuinely fun proof of concept that de-risks the software half well before the hardware half is even a question.

---

### The fleet reads a paper and ships its own PR, unsupervised

**Tier:** fantasy
**Pitch:** arxiv-mcp's codehunt/firefront scans find a technique, Fritz decides it applies to a fleet server, implements it, tests it, and merges — no human in the loop at any point.

#### 1. Step chain
1. arxiv-mcp firefront/codehunt — already scans and digests papers (real, built).
2. Fritz decides applicability — requires a reasoning step well beyond current triage-engine scope (§1 of the deep analysis is explicitly a router, not a research-applicability judge).
3. Autonomous implementation — gitops tools exist for the mechanics (branch, commit, PR), but autonomous *design* decisions at this level are a different order of capability than anything currently asked of any fleet agent.
4. Autonomous merge — this is the part that should never happen without a human, full stop, regardless of how good the reasoning gets. deepfang's whole existence (sanitize→adjudicate→dispatch, fail-closed) is the fleet's own stated position that unsupervised code-changing action is exactly the risk category requiring isolation and gating, not the category to remove gates from as capability improves.

#### 2. Feasibility / gap analysis
The scanning/digesting part is real and done. The "decide, implement, merge" part isn't a gap that closes with more integration work — it's a deliberate line the fleet's own safety architecture (deepfang, admiral approvals) says shouldn't be crossed even when it becomes technically possible. Different in kind from the other two entries in this file, which are blocked by capability; this one is blocked by design intent as much as capability.

#### 3. Effort estimate
Technically approaching plausible within the fleet's current 2026 tooling for narrow, low-risk changes (a version bump, a lint fix) — genuinely fantasy-tier only for anything touching logic. Worth being precise: this isn't "not before 2035," it's "narrow slices of this are close to real now, and the interesting boundary is exactly where deepfang's gates should stay closed regardless of capability."

#### 4. Revenue potential
None — internal tooling.

#### 5. Notes
Filed mostly as a reminder that not every fantasy-tier entry is fantasy because of hardware cost — some are fantasy because they'd be a bad idea even once they're possible, and that distinction is worth keeping visible in a catalog like this one rather than only tracking "can we" and never "should we."
