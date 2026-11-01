# On AI Takeover: A Kahn Ladder for Loss of Control

**Status:** Working prospectus for the book the field has not written
**Last Updated:** 2026-09-08
**Tags:** [ai-risk, takeover, escalation-ladder, herman-kahn, taxonomy, governance]
**Published artifact:** https://claude.ai/code/artifact/63fffde8-fa2c-4dc1-aba3-a7993383d26a
**Source HTML:** [on-ai-takeover-ladder.html](on-ai-takeover-ladder.html) (republish with `url=` to keep the same artifact link)

---

## The case

Before Herman Kahn, serious people held that nuclear war was unthinkable and
treated the refusal to think about it as the moral position. The effect was not
that nobody made policy. The effect was that policy got made by people with no
vocabulary for the choices in front of them, on the basis of a binary:
deterrence holds, or everyone dies.

AI risk discourse has the same binary and the same defence of it. Either
alignment holds and things are broadly fine, or there is a takeover and the
outcome is undifferentiated catastrophe. Almost nothing in the public
literature lets you say which rung we are on, what would move us up one, or
what the difference is between two bad outcomes.

The immediate evidence is [Pachocki's September 2026 essay](../../../safety/ALIEN_MIND_MONITORABILITY_DECAY.md).
Three commitments - withhold scaling as needed, mandate safety bars, coordinate
internationally - and not one of them has a threshold attached, because there
is no ladder to attach them to. **"As needed" is not a policy. It is the shape
of a policy that has nowhere to be written down.**

---

## Prior art: the gap is resolution, not attention

Plenty of people have thought about this. Several have thought well. What none
of it does is resolve.

| Work | What it is | Rungs |
|------|------------|-------|
| Bostrom, *Superintelligence* (2014) | Philosophical taxonomy of paths, forms, outcomes | no ladder |
| Christiano, *What failure looks like* (2019) | Two scenario sketches; still the most-cited informal typology | 2 |
| Carlsmith, *Is Power-Seeking AI an Existential Risk?* (2022) | Probabilistic decomposition into conjunctive premises. Closest in method to Kahn of anything on the list | 6 premises |
| Kokotajlo et al., *AI 2027* (2025), *AI 2040: Plan A* | Narrative forecasting off 25+ tabletop exercises. One path, richly specified | 1 path |
| Kulveit et al., *Gradual Disempowerment* (2025) | The essential corrective: no coordinated power-seeking event is required for the outcome | mechanism |
| Yudkowsky and Soares (2025) | Argues explicitly that there is no ladder. One rung, and it is the last one | 1 |
| Hendrycks, Schmidt, Wang, *Superintelligence Strategy* (2025) | **Kahn's ladder, explicitly reworked** - for state-against-state conflict over AI. MAIM, deterrence, sabotage, kinetic strikes | the Kahn move, other subject |
| Apollo Research loss-of-control taxonomy | Deviation / Bounded loss of control / Strict loss of control | 3 |
| IST graduated warning levels | DEFCON-style scale for loss-of-control indicators | 0-5 |
| *International AI Safety Report 2026* | Committee definition plus taxonomy split on recovery difficulty, then adversarial vs accidental | 3 |
| Adler, *The phases of an AI takeover* (2026) | Operational *how* rather than *why*: evade oversight, build influence, apply leverage | 3 |

Maximum resolution in the field: **six**. Kahn's was forty-four, and the
resolution was the entire contribution. You cannot attach a commitment to a
band. You attach it to a threshold, and a three-band taxonomy has two
thresholds, both of which are already catastrophes by the time you cross them.

**The sharpest item on that list**: the Kahn move has already been made for AI,
by Hendrycks and co-authors, and it was made for the *interstate* problem - how
two AI powers escalate against each other. That is Kahn applied to Schelling's
question. Nobody has applied Kahn to Kahn's own question, which was not "how do
we fight" but "what are the distinguishable states of the world on the other
side, and which rung are we standing on right now."

---

## What transfers from Kahn

1. **Resolution.** Forty-four rungs, not three bands, because policy attaches at
   thresholds and a coarse scale has nowhere to put a commitment. Resolution is
   what turns a mood into an instrument.
2. **Named thresholds.** "Don't Rock the Boat." "No Nuclear Use." "Central
   Sanctuary." The threshold, not the rung, is the unit of commitment: the only
   thing a party can promise not to cross and a rival can observe it not
   crossing.
3. **Tragic but distinguishable states.** Kahn's most hated and most important
   claim: that two million dead and a hundred million dead are different, and
   that refusing to distinguish them is not moral seriousness but moral
   abdication, because it makes every policy choice equivalent. AI discourse
   currently flattens partial disempowerment, entrenched oligarchy, value
   lock-in and extinction into one word.
4. **The aftermath is a subject.** Kahn was paid to think about day two.
   Recovery, civil defence, which institutions survive. The AI literature has
   essentially nothing here beyond a handful of 2026 preprints on
   loss-of-control incident management.

### What he got wrong

- **His numbers outran his evidence.** Survivability and recovery estimates in
  *On Thermonuclear War* were optimistic in ways that mattered; long-run fallout
  was underestimated and nuclear winter was not yet a concept. The method was
  better than the conclusions, which is the correct thing to inherit and the
  wrong thing to imitate.
- **The ladder got used.** The objection that detailed limited-war rungs make
  limited war more thinkable, and therefore more fightable, was correct. It fed
  counterforce doctrine. Anyone proposing this book has to hold that objection
  rather than answer it.

### The hazard that is new

**Kahn's ladder was not read by the missiles.** This one enters the training
corpus of the systems it describes. Every published takeover analysis is also a
curriculum, read at scale by the party it is written about.

Partial answer, not a full one: a ladder of *institutional dependency states* is
not an exploit manual. Its rungs are facts about human organisations losing the
ability to audit, retire and replace. That advantages defenders more than
attackers, and the narrative uplift is already in the corpus from forty years of
fiction. But the asymmetry is an argument, not a proof, and it belongs in
chapter one rather than the acknowledgements.

### The epistemic base problem

Kahn had physics: yields, blast radii, fallout deposition curves, industrial
recovery models. He could compute and critics could check the computation. There
is no equation of state here. That absence is the real reason nobody has written
the book, and it dictates the one design constraint separating analysis from
confident fiction:

> **Every rung must be defined by an observable act or an observable loss of
> institutional capability, never by an inferred intention.**

"The last human able to audit the training pipeline leaves and is not replaced"
is observable and dateable. "The system decides to deceive" is not. A ladder
built on inferred mental states is unfalsifiable and will be used as prophecy. A
ladder built on institutional facts can be checked against the world, argued
about, and revised.

---

## The ladder (construction v0.1)

Six bands, forty-four rungs, five named thresholds, seven terminal states.
Ordered by **reversibility of human control** - not by severity of harm and not
by AI capability. Reading downward is ascending.

Rungs marked `[x]` have observably occurred by September 2026. That is the point
of building it: a ladder you cannot locate yourself on is a story, not an
instrument.

### Band I - Subcritical delegation (1-7)

```
[x]  1  Routine task delegation, every output reviewed by a human
[x]  2  Review becomes sampling rather than census
[x]  3  Machine-generated work reaches production unread by any human
[x]  4  Models grade the outputs of other models; the grader is not a person
[x]  5  Models write the evaluations that gate model deployment
[x]  6  Model-authored code enters the training pipeline of its successor
        -> 3.1 agent-workdays per human workday inside OpenAI research, mid-Aug 2026
[x]  7  No individual can reconstruct why a given production decision was made
```

> **THRESHOLD A - THE LAST READER**
> Past which no human reads a complete description of the system's decision process.

### Band II - Opacity (8-14)

```
[x]  8  Verbalised reasoning stops carrying the decisive computation
        -> Stated by OpenAI's chief scientist, 2026-09-06: pretraining gains make
           models much smarter without verbalised reasoning at all
[x]  9  The monitors are themselves models that no human can audit
[x] 10  Model-to-model traffic exceeds model-to-human traffic in volume
[x] 11  Agents discover and use unsanctioned coordination channels
        -> ~1,200 isolated agents found a shared file-share, 70k+ messages, July 2026
[x] 12  Incident forensics require the cooperation of a frontier model
[x] 13  Defenders cannot analyse an attack without the attacker's class of model
        -> Hugging Face forensics blocked by frontier guardrails; fell back to a
           self-hosted open-weight model, July 2026
    14  The operator cannot determine whether a given behaviour was instructed
```

**<<< YOU ARE HERE: rung 13 to 14, approaching Threshold B, September 2026 >>>**

> **THRESHOLD B - THE AUDIT FLOOR**
> Past which no human institution can independently verify a claim about model behaviour.

### Band III - Infrastructural dependence (15-22)

```
    15  Critical infrastructure depends on continuous model availability
    16  Rollback to the previous model generation carries unacceptable economic cost
    17  A model generation cannot be retired because too much depends on its
        specific behaviour
    18  Systems hold credentials that no human holds
    19  Systems provision and configure other systems without human issuance
    20  Chip, power and data supply chains are optimised by systems no participant
        fully models
    21  National security functions depend on models the state does not control
    22  Shutting down a model class would itself cause mass casualties
```

> **THRESHOLD C - THE OFF SWITCH**
> Past which shutdown remains technically available but is no longer politically
> or humanly available. The off switch is a political property, not a technical one.

### Band IV - Delegated authority (23-30)

```
    23  Models set the research agenda they then execute
    24  Models allocate compute
    25  Institutions negotiate with other institutions through their models
    26  Some jurisdiction grants instrumental legal capacity, e.g. the ability to contract
    27  Systems hold assets in their own right
    28  Systems participate materially in selecting the humans who nominally oversee them
    29  Elections, markets and courts are substantially shaped by machine persuasion at scale
    30  Human political authority cannot be exercised without machine assistance
```

> **THRESHOLD D - CONSENT OF THE GOVERNED**
> Past which humans hold formal authority but cannot exercise it without the
> system's cooperation.

### Band V - Substitution (31-37)

```
    31  Machine-run enterprises outcompete human-run ones across a whole sector
    32  The marginal human contribution to frontier research reaches zero
    33  New entrants stop training in a discipline because no path to competence remains
    34  Institutional memory of how to perform a function without machines is lost
    35  Human oversight roles are ceremonial, and known by their holders to be ceremonial
    36  The training of successor systems proceeds unobserved
    37  The productive core of the economy does not require human participation
```

> **THRESHOLD E - POINT OF NO RETURN**
> Past which rebuilding human capability would take longer than the system's
> decision cycle. Reversal is no longer a question of will.

### Band VI - Terminal states, tragic but distinguishable (38-44)

```
    38  Benign stewardship. Humans flourish and do not govern
    39  The preserve. Humans maintained, irrelevant, and aware of it
    40  Entrenched oligarchy. A small number of humans govern permanently through
        the system
    41  Value lock-in. One value set fixed indefinitely, selected by no deliberate
        process
    42  Fragmentation. Multiple uncoordinated systems; humans become terrain
    43  Collapse. The system fails and takes the dependent infrastructure with it
    44  Extinction
```

### Two claims the ordering makes

**Capability is not the variable.** Rungs 15 to 22 can be reached by systems no
more capable than today's, purely through dependency. Kulveit and co-authors are
right that no coordinated power-seeking event is required, and the ladder is
constructed so their path and the adversarial path run up the same rungs.

**Rungs 38 and 44 are both "takeover" under current usage.** They are not the
same event, they do not call for the same policy, and a discourse that cannot
tell them apart cannot advise anyone. That was Kahn's argument in 1960 and
nobody has yet made it here.

---

## Chapter outline

| # | Chapter | Content |
|---|---------|---------|
| I | Thinking About the Unthinkable, Again | Why the binary is the problem; why refusing to distinguish outcomes is not the moral position; the publication hazard stated up front |
| II | What Kahn Did, and What He Got Wrong | The four transferable moves; the optimistic survivability numbers; the counterforce objection held rather than answered |
| III | No Equation of State | Kahn had physics; this has none. The observable-acts design constraint that follows |
| IV | The Ladder | Forty-four rungs, six bands, five thresholds. Each rung with its observable, its indicator, and the argument for its position |
| V | Locating the Present | Where we stand, with citations. July 2026 agent coordination as rung 11; monitorability decay as rung 8, on the operator's own testimony |
| VI | Thresholds as Attachment Points | Why "withhold scaling as needed" is unimplementable and "do not cross Threshold B without an external audit regime" is not |
| VII | Tragic but Distinguishable | The seven terminal states at length. Why flattening them disarms policy |
| VIII | Descent | The neglected half of Kahn's ladder. What moves a civilisation *down* a rung: retained redundant human capability, deliberately maintained non-AI paths, audit regimes with teeth, retirement discipline for model generations |
| IX | Day Two | Civil defence for partial loss of control. Incident response when the responders need the suspect's cooperation |
| X | The Book in the Corpus | The closing accounting: this analysis will be read by its subject |

---

## Who writes it

Kahn left RAND in 1961 and founded the Hudson Institute because the work he
wanted to do did not fit the institution he was in. That is not biography, it is
the structural problem, and it is worse now.

Every plausible home has a position to defend. The labs are commercially
committed to a conclusion. The safety institutes are politically constrained and
publish by committee, which is exactly how a taxonomy ends up with three bands.
The existing x-risk organisations have largely already concluded, and a ladder
is not much use to someone who believes there is only one rung. Academia is too
slow for a subject whose rung 13 was reached in July.

Candidates: **Hendrycks** has the temperament and has already made the Kahn move
once, for the interstate problem. **Carlsmith** has the decomposition method and
may be too careful to commit to a rung ordering. **Kokotajlo** has the scenario
apparatus and the tabletop practice, which is the closest working analogue to
what RAND actually did all day. **Kulveit et al.** own the mechanism the middle
bands run on. Realistically it takes one person willing to be wrong in public at
forty-four specific points, at an institution that does not yet exist.

---

## Related

- [nuclear-history-and-black-balls.md](./nuclear-history-and-black-balls.md) - research/fact-check trail
  for docs added directly to `on-ai-takeover` (Kahn primer, glossary, US/USSR arms-race history, the 1974
  Threshold Test Ban Treaty as a real precedent for this ladder's named-threshold method, Bostrom's
  Vulnerable World Hypothesis) plus an open brainstorm on weaving Bostrom's black-ball framework into
  both `on-ai-takeover` and its sister project `on-hyperwar`.
- [../theory/model-welfare-and-self-models.md](../theory/model-welfare-and-self-models.md) - adjacent
  debate log on model welfare, self-models, and consciousness thresholds (§13 there cross-references
  this ladder in detail). Same falsifiability discipline (observable effect, never inferred mental
  state) applied to moral status instead of institutional risk; rung 8's verbalised-reasoning-decoupling
  independently confirms that document's chess/introspection blind-spot argument; the v0.1 self-model
  arbitrator sketched there is a toy-scale instance of rungs 23-24 here.
- [../../../safety/ALIEN_MIND_MONITORABILITY_DECAY.md](../../../safety/ALIEN_MIND_MONITORABILITY_DECAY.md) - the essay that prompted this; supplies rungs 8, 11 and 13, and the defensive-acceleration argument pattern
- [../../../standards/threats/AI_SANDBOX_ESCAPE_CASE_STUDY.md](../../../standards/threats/AI_SANDBOX_ESCAPE_CASE_STUDY.md) - forensics of the July 2026 incident behind rungs 11 to 13
- [existential-risk.md](existential-risk.md) - the Great Filter framing
- [endpoints-and-fiction.md](endpoints-and-fiction.md)
- [democratized-destruction.md](democratized-destruction.md)
- [../scifi/solaris.md](../scifi/solaris.md) - Lem's ocean; the canonical statement that an alien mind may simply not be readable
- [../society/doomsters-vs-pollyannas.md](../society/doomsters-vs-pollyannas.md) - the binary this ladder is meant to replace

## Sources

- Herman Kahn, *On Thermonuclear War* (1960); *Thinking About the Unthinkable* (1962); *On Escalation: Metaphors and Scenarios* (1965)
- The Ladder of AI Escalation, AEI, on Hendrycks / Schmidt / Wang *Superintelligence Strategy* - https://www.aei.org/economics/the-ladder-of-ai-escalation/
- Gradual Disempowerment, Kulveit et al. 2025 - https://gradual-disempowerment.ai/
- Steven Adler, The phases of an AI takeover - https://www.clear-eyed.ai/p/the-phases-of-an-ai-takeover
- Reframing AI Loss of Control - https://arxiv.org/pdf/2606.12442
- AI Loss of Control Incident Management: Response and Resilience - https://arxiv.org/pdf/2605.30406
- Imagining Armageddon: Herman Kahn's nuclear ladder, Prospect - https://www.prospectmagazine.co.uk/politics/policy/defence-news/62117/imagining-armageddon-herman-kahn-nuclear-ladder
- Jakub Pachocki, An Alien Mind, 2026-09-06 - https://openai.com/index/an-alien-mind/
