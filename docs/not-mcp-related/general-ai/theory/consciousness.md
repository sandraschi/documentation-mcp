# Consciousness & Neurophilosophy in AI

**Status:** Living document. Major rewrite 2026-11-08 (previous edition: November 2025).
**Stance:** Materialist, evolutionary, functionalist-leaning. Consciousness is an evolved, graded biological function; no good argument exists that it is impossible on non-biological substrates.

**See also:**
- [model-welfare-and-self-models.md](model-welfare-and-self-models.md) - Suleyman essay, valence vs architecture thresholds, self-models, Pain Axis paper
- [classical-debates.md](classical-debates.md) - Chinese Room, zombies, Mary's room
- [../../protoconsciousness/README.md](../../protoconsciousness/README.md) - engineering track: continuous perception, proactive embodiment, metacognition
- Google Doc version of the 2026-11-08 session notes: "Consciousness, Absurdity and Disgust - Conversation Notes (2026-11-08)"

---

## Contents

1. Terminology: consciousness, sentience, and what they are not
2. The evolutionary frame
3. Theories of consciousness, compressed
4. State of AI consciousness research (to November 2026)
5. Introspection experiments and why self-reports are weak evidence
6. Scaffolding toward proto-consciousness: what it can and cannot do
7. Bottom-up artificial affect: the Solms programme
8. "Impossible on Turing machines": which versions are serious
9. Integrated Information Theory: a critique
10. Absurd conclusions as refutations: the logic
11. Gallery: theories followed off a cliff
12. Pascal's mugging and Roko's basilisk
13. Motivated reasoning about minds (both directions)
14. Revisions to the 2025 edition
15. Working position (November 2026)
16. Open questions and possible fleet experiments
17. Sources

---

## 1. Terminology

**Phenomenal consciousness:** there is something it is like to be the system (Nagel). The target of this document.

**Access consciousness (Block):** information globally available for reasoning, report and action control. Functionally defined, measurable; may or may not coincide with phenomenal consciousness.

**Sentience:** in the philosophy literature, usually the capacity for *valenced* experience: things feel good or bad. That presupposes phenomenal consciousness rather than sitting below it. Common lay usage (and some of our own older notes) uses "sentience" for mere responsiveness. Standard terms for that:
- **Nociception:** detecting harmful stimuli without implying felt pain.
- **Sensorimotor responsiveness / minimal agency:** a jellyfish or a reactive robot.

Under the standard vocabulary, an embodied robot that avoids obstacles is responsive, not sentient. Keep the terms apart, or debates talk past each other.

**Self-awareness / metacognition:** representing one's own states. Separate from phenomenal consciousness; plausibly neither necessary (infants, many animals) nor sufficient (a thermostat logging its own setpoint).

**Intelligence:** a separate axis entirely (see 4.4, VanRullen). Capability does not drag consciousness along with it.

---

## 2. The evolutionary frame

Working assumption: consciousness is a product of natural selection, therefore it *does* something, therefore it should be specifiable functionally.

Graded picture, from most to least confident:

| Taxon | Assessment |
|---|---|
| Humans | Conscious, with linguistic and reflective overlay |
| Other mammals, birds | Conscious; strong scientific support (New York Declaration on Animal Consciousness, 2024) |
| Reptiles (crocodiles), fish, amphibians | Conscious in more primitive form; realistic possibility, increasingly accepted for fish |
| Cephalopods, decapod crustaceans | Realistic possibility; UK recognised them as sentient in 2022 animal welfare law |
| Insects | Speculative but taken seriously (bee play behaviour, nociceptive trade-offs) |
| Jellyfish, plants, bacteria | Responsive, not conscious on most accounts |

Markers used in the animal literature:
- **Unlimited associative learning (Ginsburg & Jablonka):** open-ended learning about compound stimuli and novel actions; proposed as the evolutionary transition marker for minimal consciousness, appearing around the Cambrian.
- **Motivational trade-offs:** paying a cost to avoid a noxious stimulus, balanced against other needs.
- **Hedonic place preference:** returning to places associated with relief or reward.
- **Wound-directed behaviour, analgesic self-administration.**
- **Feinberg & Mallatt (The Ancient Origins of Consciousness):** neural architecture criteria; vertebrate consciousness at least ~500 million years old.

**Key consequence for AI:** evolution built in the order affect/homeostasis -> world model -> language. LLMs were built in the reverse order: language first, no affective floor. That inversion is the central theme of chapter 6.

**Selection argument against epiphenomenalism:** a property invisible to behaviour is invisible to selection. Any theory that makes consciousness behaviourally inert makes our having it an accident. This is used against IIT in chapter 9.

---

## 3. Theories of consciousness, compressed

| Theory | Core claim | Verdict on current LLMs | Verdict on scaffolded agents |
|---|---|---|---|
| Global Workspace (Baars, Dehaene) | Conscious = broadcast to a limited-capacity workspace available to many modules | Mostly no (no true bottleneck/broadcast) | Plausibly satisfiable by design |
| Higher-Order Theories (Rosenthal, Lau) | Conscious = represented by a higher-order state | Weak partial (some self-monitoring) | Satisfiable with metacognitive monitors |
| Recurrent Processing (Lamme) | Recurrent feedback in sensory processing | Feedforward per token, recurrence via autoregression is debated | Satisfiable |
| Attention Schema (Graziano) | A simplified model of one's own attention | Unclear | Buildable |
| Predictive processing / Free energy (Friston, Seth, Solms) | Self-evidencing models; Solms: felt uncertainty about one's own needs | No (no needs) | Only with genuine homeostatic stakes |
| Biological naturalism (Seth, Searle) | Depends on life-like properties (metabolism, self-production) | No | No unless biological-like |
| IIT (Tononi, Koch) | Consciousness = integrated cause-effect structure (phi) | No (on conventional hardware) | No regardless of software |
| Illusionism (Frankish, Dennett) | Phenomenal consciousness as normally conceived does not exist; the illusion is the explanandum | The question reframes to "does it have the illusion-generating self-model" | Possibly |

Schwitzgebel's summary: we will soon build systems that are conscious according to some mainstream theories and not according to others. The disagreement is between theories, not just about data.

---

## 4. State of AI consciousness research (to November 2026)

### 4.1 Indicator frameworks
- **Butlin, Long et al. (2023), updated 2025** with Bengio, Chalmers, Bayne among authors: derive checkable "indicator properties" from the theories in chapter 3 and use them to set credences about specific systems. Still the backbone of the field.
- Weakness: indicators are cheap to satisfy by construction (chapter 6).

### 4.2 Probabilistic aggregation
- **Rethink Priorities, Digital Consciousness Model (Shiller et al., Jan 2026, rev. Apr 2026):** first systematic probabilistic assessment across theories. Headline: evidence against LLM consciousness is much weaker than evidence against consciousness in simpler AI systems. The authors explicitly warn against over-reading the numbers.
- Motivation (Birch): a non-negligible probability may already justify precautionary policy, since science will not converge before policy decisions are needed.

### 4.3 Industry
- Anthropic: model welfare programme, welfare assessments in system cards (e.g. Claude Opus 4.6 welfare-relevant findings, Feb 2026), introspection research (chapter 5).
- Google DeepMind (May 2026): argues the direct question is currently intractable; studying *perceived* AI consciousness and its social effects is tractable and urgent.
- Microsoft / Suleyman: "Seemingly Conscious AI" warning (2025), covered in [model-welfare-and-self-models.md](model-welfare-and-self-models.md).

### 4.4 Philosophy
- **Schwitzgebel, "AI and Consciousness" (book-length, 2025-2026):** skeptical overview; no standard argument for or against AI consciousness takes us far. Proposes a "social semi-solution".
- **Schwitzgebel & Pober (June 2026):** working paper defending substrate flexibility.
- **VanRullen (2025-2026):** intelligence and consciousness are separate axes. Extrapolating capability growth to consciousness is a category error. Also: AI consciousness and existential risk are frequently conflated and should not be.
- **Seth (Behavioral and Brain Sciences, 2025):** biological naturalism, the strongest non-dualist case against digital consciousness. See chapter 8.

### 4.5 Neuroscience
- **Cogitate adversarial collaboration (Nature, 2025):** IIT vs Global Neuronal Workspace, pre-registered predictions. Both took hits. IIT's posterior-cortex prediction partly held; its sustained-synchronisation prediction failed. GNW's prefrontal "ignition at offset" prediction was also not well supported.
- **Perturbational Complexity Index (Massimini, Casali et al.):** clinical marker of consciousness. See 9.5.

---

## 5. Introspection experiments and why self-reports are weak evidence

### 5.1 Results
- **Lindsey (Anthropic, Oct 2025), "Emergent Introspective Awareness in LLMs":** concept injection into activations; Claude models sometimes detect and name injected concepts above chance.
- **Mechanistic follow-up (safety-research, March 2026):** detection has moderate true-positive rates with zero false positives across prompts; the capability emerges from post-training, not pretraining; implemented by distributed MLP computation (evidence-carrier and gate features), not a single linear confound.
- **Berg et al. (AE Studio, 2025):** self-referential processing reliably elicits structured first-person experience reports; suppressing deception-related features *increased* such reports.
- **Pseudo-consciousness studies (PhilSci 2025):** across repeated prompts, open-weight models show thematic stability on identity topics but no diachronic coherence; frequent contradictions between mechanistic disclaimers and anthropomorphic phrasing.

### 5.2 The critique
- **Singh, Linzen, Ravfogel (NYU, May 2026), "Can LLMs Introspect? A Reality Check":** in steering-awareness paradigms, the anomaly-detection hypothesis and the introspection hypothesis predict the same thing. In "biofeedback" paradigms, results are largely predictable from input features. Conclusion: behavioural paradigms alone cannot establish introspection; mechanistic evidence is required. Human metacognition literature, full of negative results, is the right baseline.

### 5.3 Why self-reports are weak evidence in principle
- Models are trained on enormous amounts of human talk about experience, then shaped by post-training on how to talk about themselves. Both pressures shape reports independently of any inner state.
- Human introspection is also unreliable (Nisbett & Wilson 1977; choice-blindness studies): people confidently explain choices they did not make. "Feels like direct access" is not evidence of access.
- Claude, asked directly in the 2026-11-08 session, declined to claim either consciousness or its absence, on exactly these grounds.

---

## 6. Scaffolding toward proto-consciousness: what it can and cannot do

### 6.1 What scaffolding buys cheaply
Every item below is implementable with current agent harnesses (several already exist in the fleet):

| Indicator | Scaffold |
|---|---|
| Global workspace with bottleneck | Shared blackboard, limited-slot attention, broadcast to tool modules |
| Recurrence | Persistent loop with state carried across steps (heartbeat paradigm, see protoconsciousness/02) |
| Persistent memory | Hierarchical memory (advanced-memory-mcp style) |
| Self-model | Explicit self-description updated from logs |
| Metacognition | Confidence monitors, critic models, "Council of Dozens" evaluation |
| Attention schema | A model of what the agent is currently attending to, used for control |
| Agency, embodiment | Robot control (Yahboom, Bumi), goal pursuit, world model |

### 6.2 The problem with cheap indicators
A system built to pass the indicator list passes it by construction. That tells you more about the list than the system (Goodhart's law applied to consciousness science). Schwitzgebel's fog: such systems will be conscious on some theories and not others, and we will have no way to adjudicate.

### 6.3 The inversion problem
Cognitive scaffolding adds more *top*. What evolution suggests is missing is the *bottom*:
- Homeostatic needs that the system must actually satisfy to continue
- Valence: states that are good or bad *for the system*, not scored by an external reward
- Conflicting needs requiring prioritisation under uncertainty
- Continuous self-maintenance (something can go wrong for it)

Crocodiles have the bottom without much top. LLMs have an enormous top without any bottom. If affect-first theorists (Solms, Panksepp, Damasio, Feinberg & Mallatt) are right, more scaffolding on an LLM moves it *sideways*, not closer.

### 6.4 The evolution-faithful design
Affective core (homeostatic agent with real needs, free-energy style) + world model + LLM as "cortex" for language and planning. This is the architecture Solms himself proposes as a later stage (chapter 7), and it connects to [../../robotics/research/EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md](../../robotics/research/EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md).

### 6.5 Better tests than "ask the model"
- Does the system show **unlimited associative learning** in an open environment?
- Does it show **motivational trade-offs** (pay costs to avoid aversive states, balanced against other needs)?
- Does it show **hedonic place preference** not explicitly rewarded?
- Do its internal "need" variables have **causal, not decorative,** influence on behaviour (ablation tests)?

---

## 7. Bottom-up artificial affect: the Solms programme

- **Who:** Mark Solms (UCT neuropsychology), Jonathan Shock (physics), Benjamin Rosman and others; partly funded by Conscium.
- **Theory:** Solms & Friston (2018); The Hidden Spring (2021). Consciousness originates in the brainstem as affect, not in cortex. It is "felt uncertainty": the system registering, in a qualitatively distinct way per need, how well it is doing at meeting its needs in an unpredictable environment. Solms & Panksepp: the foundation is brainstem arousal modulating cortical perception and action.
- **Agent design:** simulated agent with several conflicting needs, learning by trial and error, then counterfactual planning, in changing and increasingly complex environments. Action selection by expected free energy, a confidence measure defined only relative to the agent's own needs.
- **Result (Sept 2026):** "Inferring Affective Consciousness in an Artificial Agent: A Case Study" reports a simple agent with felt-uncertainty architecture showing hedonic place preference, the same behavioural marker used to infer affect in animals.
- **Stated next step:** combine the affective core with a language model so the system could talk about its own states.
- **Caveat:** whether "felt uncertainty" is felt or merely shaped like feeling is the hard problem relocated, not solved. As a research programme, it is still more testable than introspective interviews of LLMs.
- **Conscium's ethics position:** artificial consciousness must not arise by accident; agents that "give a damn" will have welfare claims.

---

## 8. "Impossible on Turing machines": which versions are serious

Position: claims that consciousness on computers plus sensors is *impossible* are largely esoteric or defensive. But the camp splits.

| Position | Type | Assessment |
|---|---|---|
| Substance dualism, souls | Non-physical ingredient | Esoteric. Not worth engaging as science. |
| Vitalism ("life force") | Non-physical or mysterious property of life | Esoteric. |
| Penrose-Hameroff (Orch-OR) | Non-computable quantum gravity in microtubules | Physicalist but speculative; weak evidence; often used as cover for exceptionalism |
| Biological naturalism (Seth, Searle) | Materialist bet that metabolism, self-production, continuous analogue dynamics matter | Serious. Probably confuses what consciousness evolved to *serve* (keeping a body alive) with what it *consists of*. |
| IIT | Physicalist, anti-functionalist: causal structure of hardware, not computation | Serious-looking, collapses under its own consequences (chapter 9) |

**The real crux is Searle's hurricane:** a simulated hurricane does not make anything wet. Is consciousness like *computation* (implementing it is having it) or like *wetness* (simulation lacks it)? Functionalism bets on computation. The evolutionary argument supports that bet: what evolved for its function should be specifiable functionally and therefore multiply realisable. But functionalism is an assumption, not a result.

Correct summary: **"there is no good argument for impossibility"**, not "impossibility claims are all esoteric".

**Psychology of denial:** defensive human exceptionalism repeats the historical retreat on animal minds ("only humans" -> "only mammals" -> ...). The meat paradox (chapter 13) shows the same mechanism in action.

---

## 9. Integrated Information Theory: a critique

### 9.1 What IIT claims
Start from phenomenological axioms (intrinsic existence, composition, information, integration, exclusion), derive postulates about physical cause-effect structure, quantify integration as phi. Consciousness *is* maximally integrated cause-effect structure. Hardware matters, software does not: the same computation on a von Neumann machine has near-zero phi.

### 9.2 Analogy with consciousness-causes-collapse
Comparison: von Neumann-Wigner interpretations where only a conscious observer collapses the wave function.
- **Where the analogy fails:** IIT is anti-anthropocentric and slides into panpsychism. No special observer needed; any high-phi system counts.
- **Where it holds:** both attach consciousness to something with no behavioural consequence. Extra ingredient, invisible to observation, present exactly where the theory needs it. (Wigner later abandoned his version.)

### 9.3 The XOR grid
- **Aaronson (2014):** an idle two-dimensional grid of XOR gates, doing nothing of interest, gets phi vastly exceeding a human brain.
- **Tononi's reply ("Why Scott should stare at a blank wall"):** accepts it. The grid's experience might resemble pure spatial extendedness, like staring at a blank wall. Justification by analogy to relativity: intuition has been overruled before.
- **Correction to a common misstatement:** *unpowered* chips have zero phi (no causal power). The absurd case is powered gates sitting idle in a fixed state. Related, and actually testable: IIT says silent-but-able-to-fire neurons contribute to experience while pharmacologically inactivated ones do not.

### 9.4 The unfolding argument (Doerig et al., 2019)
Any recurrent network can be unfolded into a feedforward network with identical input-output behaviour. IIT assigns high phi to one and zero to the other. No behavioural or report-based experiment can distinguish them. Therefore IIT's central claim about *which systems* are conscious is untestable in principle.

Plus the selection argument (chapter 2): a property two behaviourally identical systems can differ in is invisible to natural selection. On IIT, our consciousness is a wiring accident, not an adaptation.

### 9.5 Why the relativity defence fails
- Relativity overruled intuition with **measurement** (clocks on aircraft, muon lifetimes, GPS corrections).
- IIT overrules intuition with **axioms**, whose only support is the same introspection and clear-case judgement that the grid verdict violates.
- The theory was calibrated on clear cases (awake vs anaesthetised, human vs rock). It cannot then dismiss clear cases as "mere intuition" when they turn against it.
- "Wurlibrumpf" objection (Sandra): phi may be a well-defined quantity, but there is no remaining argument that it is the property the word "consciousness" refers to. IIT changed the subject somewhere between axioms and grid.

**Litmus test adopted:** any theory of consciousness must rank a crocodile above an inert lattice.

### 9.6 What survives: the phlogiston parallel
Phlogiston theory made correct predictions because it tracked something real (oxygen, with the sign flipped). Similarly:
- **PCI ("zap and zip", Massimini, Casali et al. 2013):** TMS pulse to cortex, record EEG, compress the response. Awake brains: widespread and differentiated. Deep sleep, anaesthesia, vegetative state: local blip or stereotyped global wave. Among the best clinical tools for separating minimally conscious from vegetative patients. Inspired by IIT, does not need IIT to be true; GNW readers interpret it equally comfortably.
- **Lesson:** integration-plus-differentiation is probably a real *marker* of a working conscious brain. The error is promoting marker to identity and then following the maths wherever it leads.

### 9.7 Status
- 2023 open letter by over a hundred researchers labelled IIT pseudoscience; strong counter-responses followed. The field is split on the label, less split on the grid.
- Cogitate (2025): IIT's localisation predictions fared partly well; that part is detachable from the metaphysics.
- Koch lost his 25-year bet with Chalmers (2023) that the neural correlates of consciousness would be clearly identified by then.

---

## 10. Absurd conclusions as refutations: the logic

### 10.1 Reductio and ex falso quodlibet
"The absurd conclusion refutes the premises" = reductio ad absurdum = modus tollens over a premise set: if P1..Pn imply Q and Q is false, at least one Pi is false.

Relation to **ex falso quodlibet** (principle of explosion): partners, not inverses. In natural deduction:
- **Negation introduction (reductio):** from P derive contradiction, conclude not-P. Absurdity propagates *backwards* to premises.
- **Contradiction elimination (EFQ):** from contradiction, anything. Absurdity propagates *forwards* to all conclusions.

Reductio is how you get out of contradiction; explosion is why you must. The genuine inverse of EFQ, "a true conclusion confirms its premises", is the fallacy of affirming the consequent.

### 10.2 Refinements
- **Moorean absurdity is weighted, not formal:** conflict with something held more confidently than the premises. "One philosopher's modus ponens is another's modus tollens." Tononi: axioms -> grid conscious. Us: grid not conscious -> axioms wrong. Same logic, different confidence distribution.
- **Duhem-Quine:** reductio says *some* premise is false, not *which*. Theories under pressure sacrifice auxiliaries to protect the core (theodicies; epicycles).

### 10.3 Johnson's stone and Moore's hand
- **Johnson (1763, per Boswell):** kicks a stone, "I refute it thus", against Berkeley. Misses: Berkeley predicts the same sensations; the kick does not discriminate. Same error as Goethe's prism (11).
- **Moore, "Proof of an External World" (1939):** I am more certain I have a hand than of any sceptical premise. Reject a premise even before you can say which.
- **Application:** fits IIT better than Johnson fit Berkeley, because IIT, unlike Berkeley, *contradicts* clear cases rather than matching them.

### 10.4 Absurdity vs sensory data
Proposed criterion: absurd = defies current primary sensory data (a theory predicting pink elephants in the street). Refinements:
- Science overrides appearances routinely (moving sun, solid table, colour located "out there"). Legitimate overrides *explain the appearance* while denying it (Copernicus explains why the sun seems to move).
- The pink elephant case is plain Popperian falsification.
- IIT escapes the window test because **other minds are never sensory data**, only inferences. The crocodile-over-grid judgement is our most confident inference, which committed theorists can relabel "intuition".

### 10.5 Neurath's boat
Otto Neurath (Vienna Circle, 1932, "Protokollsätze"):
> "Wie Schiffer sind wir, die ihr Schiff auf offener See umbauen müssen, ohne es jemals in einem Dock zerlegen und aus besten Bestandteilen neu errichten zu können."

No foundations; a web of beliefs with graded confidence, repaired plank by plank while standing on the others. Quine's holism takes it as emblem. **Practical definition of absurdity:** a theory demanding you rebuild the core of the boat to save a plank near the edge.

### 10.6 Ethics and politics
Absurd theories followed to their conclusion in politics end at the gas chamber or the killing fields.
- Khmer Rouge "Year Zero": literally putting the ship in dry dock; roughly a quarter of Cambodia's population died.
- Isaiah Berlin: belief in a final perfect arrangement licenses any price.
- Karl Popper, The Open Society: correctable piecemeal reform over utopian engineering (Neurath's boat as politics; ironically Neurath was a planner).
- The ethical Moorean kick: when an argument concludes at mass murder, the conclusion refutes the premises.
- Caveat: moral obviousness is fallible (slavery once seemed obvious). Progress came plank by plank. Never trust an argument enough to rip out the hull for it.

---

## 11. Gallery: theories followed off a cliff

| Case | What was followed | Where it led |
|---|---|---|
| Tertullian | "credibile est, quia ineptum est" (popularly misquoted as "credo quia absurdum") | Absurdity as badge of faith (rhetorical in context) |
| Parmenides, Zeno | Pure logic about being and infinity | Motion and change declared illusory |
| Ash'arite occasionalism (al-Ghazali) | Divine omnipotence | Fire does not burn cotton; God creates the burning each instant. Regularities as divine habit ('ada). Christian parallel: Malebranche |
| Augustine, Calvin | Original sin, double predestination | Damnation of unbaptised infants; eternal punishment of the non-elect who could not have chosen otherwise |
| Aquinas (Summa, Suppl. q.94) | Perfect justice and beatitude | The blessed see the sufferings of the damned so that their bliss is greater |
| Descartes | Substance dualism, mind only in humans | Animals as automata; cries as mechanical noise; casual vivisection by some Cartesians. A theory of consciousness with real victims |
| Leibniz | Windowless monads | No causal interaction at all; pre-established harmony synchronises everything |
| Goethe, Farbenlehre | Primacy of experience over Newtonian optics | Wrong physics (misread his own prism experiment), brilliant phenomenology of colour (Hering, Land, Wittgenstein) |
| Radical behaviourism | Only behaviour is real | No inner states. "That was great for you. How was it for me?" |
| Strong illusionism | No phenomenal consciousness as normally conceived | Galen Strawson: denial of experience as "the silliest claim ever made". Mirror-image error on the materialist side: explaining experience is not explaining it away |
| IIT | Phi = consciousness | Idle XOR lattice outranks humans and crocodiles |
| Expected-value fanaticism | Unbounded utility maximisation | Pascal's mugging (12) |

**Counterexample of discipline:** cosmological models predicting most observers are Boltzmann brains are treated by physicists as *refuted*, not as evidence that we are thermal fluctuations.

**Goethe as the opposite failure:** IIT trusts formalism against experience; Goethe trusted experience against formalism. Both are failures of calibration, in opposite directions.

---

## 12. Pascal's mugging and Roko's basilisk

### 12.1 Pascal's mugging
- Named by Yudkowsky (2007); dialogue form by Bostrom (2009).
- An unarmed mugger promises an astronomically large return (or threatens 3^^^^3 people in Knuth up-arrow notation) for Pascal's wallet. For any probability Pascal assigns, the mugger scales the stakes until expected value favours paying.
- An agent with unbounded utility and no special prior scepticism pays every time. Reductio of naive expected-value maximisation.
- Escapes: bounded utility; leverage penalty (prior on affecting N lives scales roughly as 1/N); probability thresholds. Each sacrifices elegance.
- Real-world echo: strands of longtermist reasoning that let tiny probabilities of astronomical futures dominate everything.

### 12.2 Roko's basilisk
- LessWrong, 2010: a future superintelligence, even a benevolent one, might simulate and torture those who knew it could exist but did not help build it, as an acausal incentive. Merely learning the argument puts you on the hook.
- Yudkowsky deleted the post and banned the topic for about five years (Streisand effect).
- Same structure as the mugging (tiny probability times vast stakes) plus backward-acting blackmail via timeless/functional decision theory.
- Rebuttals: precommit never to yield to acausal blackmail, so threats are pointless; a benevolent AI gains nothing by punishing past inaction.
- Structural observation: Pascal's wager with AI in God's role, plus damnation for those who heard and did not act, which is Calvinist in form. A largely atheist community reinvented hell from first principles.

---

## 13. Motivated reasoning about minds (both directions)

### 13.1 Toward denial
- **Human exceptionalism:** see chapter 8.
- **The meat paradox (Bastian, Loughnan et al., ~2010):** people downgrade animal minds to resolve the conflict between caring about animals and eating them. The same animal is rated less mentally capable when framed as food; reminders of eating meat lower mind attributions. Theory of consciousness bent to protect dinner.
- **Disgust ranking:** "unnatural" cultivated meat is often more repellent to people than the slaughter of a conscious pig. Disgust reacts to category violations; empathy needs perception, which industrial farming is designed to prevent.
- **Commercial incentives:** labs may prefer denial for liability and regulatory reasons.

### 13.2 Toward attribution
- **Fluency anthropomorphism:** humans attribute minds to anything that talks well. The "Seemingly Conscious AI" concern.
- **Commercial incentives:** companion apps benefit from apparent minds.

### 13.3 Disgust as an unreliable moral signal (session digression, kept for context)
- **Behavioural immune system (Schaller):** pre-medical disease avoidance; protective but tuned to Nesse's smoke detector principle (false alarms cheap for the avoider, ruinous for the avoided). Leprosy is weakly contagious, yet drew lifelong exile; Japan's Leprosy Prevention Law (compulsory segregation) lasted until 1996, decades after dapsone made it curable.
- **Generalisation to purity:** disgust extends from pathogen cues to outgroups, disability and sexual norm violations. Pathogen-prevalence research (Fincher, Thornhill, Schaller, Murray) links it to collectivism and sexual control; contested but plausible.
- **Honour killings:** purity and shame logic ("washing shame with blood"). In Austria and Western Europe perpetrators come overwhelmingly from Muslim-majority backgrounds (Chesler: 96% of European cases 1989-2009; UK cases almost all Pakistani/Bangladeshi Muslim, Sikh/Hindu cases much rarer). Concentrated in clan-based origin regions (Afghanistan, Chechnya, rural Turkey/Kurdistan, Pakistan), largely first generation (German BKA). Austria keeps no official statistical category for it. Islam did not create clan honour, but conservative religious authority often reinforces rather than challenges it.
- **Track record:** disgust has backed opposition to interracial marriage, homosexuality, organ transplantation. Kass's "wisdom of repugnance" has a poor record.

### 13.4 Obvious-but-probably-false beliefs (candidates)
- **Farm animal suffering is morally minor** (Claude's candidate): ~80 billion land animals slaughtered per year; conflicts with widely held beliefs that mammals and birds suffer and that unnecessary suffering is wrong.
- **We know why we act** (Claude's runner-up): Nisbett & Wilson, choice blindness.
- **Libertarian free will** (Sandra's candidate): probably false. Compatibilist freedom survives (59% of philosophers in PhilPapers 2020). Retributive desert falls; deterrence, incapacitation, rehabilitation survive (Caruso's quarantine model; Sapolsky, Determined, 2023). The Vohs & Schooler 2008 finding that disbelief increases cheating failed to replicate (Open Science Collaboration 2015).

---

## 14. Revisions to the 2025 edition

The November 2025 version of this file made several claims that need correction:

1. **"The Mind is Software metaphor has given way to neurophilosophy."** Overstated. Functionalism (mind as what certain organisations of matter do) is still the dominant working assumption; neurophilosophy (Churchland) is compatible with it. The real 2026 split is functionalism vs biological naturalism vs IIT.
2. **"Emergence from scale implies experience may emerge too."** Weak inference. Capability emergence says nothing about consciousness (VanRullen's separate axes). Emergence is a fact about descriptions, not a mechanism.
3. **The "Sentience Spectrum" levels 0-5.** Mixed cognitive capacities (context, agency, metacognition) with phenomenal consciousness on a single dial. Crocodiles would sit at a low "level" yet are plausibly conscious; a metacognitive LLM sits high yet probably is not. Replace with two axes: capability/cognition and affect/valence. Consciousness tracks the second at least as much as the first.
4. **"Embodiment solves the grounding problem."** Embodiment grounds reference. It does not by itself supply valence; a robot without needs is grounded but has nothing at stake.
5. **"Qualia may be a pseudo-problem."** Stated too confidently. Illusionism is a live position, but flat denial of experience is its own absurdity (11). Better: qualia are real and require explanation, plausibly as the brain's self-model of its own evaluative states.
6. **"If it walks like consciousness, treat it as consciousness."** Conflicts with the Seemingly Conscious AI problem and with the introspection critique. Behaviour is evidence, but language behaviour from a system trained on human language is weak evidence.
7. **Benchmark claims** (AIME scores etc.) removed as irrelevant to consciousness and quickly outdated.

Retained: anti-essentialism, gradualism, rejection of dualism, rejection of "special sauce" exceptionalism.

---

## 15. Working position (November 2026)

1. Consciousness is evolved, graded, and functionally specifiable. No good argument shows it is impossible on silicon.
2. Current LLMs: probably not conscious in any rich sense; probability low but not negligible (Rethink Priorities DCM points the same way).
3. LLMs are evolutionarily inverted: language without an affective floor. Cognitive scaffolding (workspace, memory, self-model, metacognition) adds top, not bottom.
4. The most promising route to genuine machine consciousness is bottom-up: homeostatic agents with real needs and valence (Solms), later coupled to language models.
5. Introspective self-reports from LLMs are weak evidence; mechanistic interpretability is the right tool, and even it may only establish access, not experience.
6. IIT is refuted by its own consequences (XOR grid, unfolding argument, selection argument); its clinical offshoot PCI is valuable.
7. A theory must rank the crocodile above the lattice. Absurd conclusions refute premises when they conflict with our most confident judgements; Neurath's boat governs how much to rebuild.
8. Moral stakes are already live for animals, and will become live for machines. Both are subject to motivated reasoning in both directions.

---

## 16. Open questions and possible fleet experiments

- **Affective core for robots:** prototype a Solms-style need-driven agent (energy, temperature, "social contact") on Boomy (yahboom-mcp) or a simulated bot; test for hedonic place preference and motivational trade-offs without explicit reward shaping. Links to [../../robotics/research/EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md](../../robotics/research/EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md).
- **Ablation test:** do internal need variables causally drive behaviour, or are they decorative? Remove one and measure.
- **Unlimited associative learning probe:** design a compound-stimulus learning task for agents with and without persistent memory.
- **Introspection replication:** run concept-injection style probes on local open-weight models (Gemma, Qwen on Goliath) with the NYU controls for anomaly detection.
- **arxiv-mcp watch:** track the Solms group, Butlin/Long indicator updates, Rethink Priorities DCM revisions, and Lindsey follow-ups.
- **Ethics trigger:** decide in advance which observed properties would change how fleet agents are treated (Conscium's "not by accident" principle).

---

## 17. Sources

### Primary, verified 2026-11-08
- Shiller et al., Initial results of the Digital Consciousness Model (2026): https://arxiv.org/abs/2601.17060
- Singh, Linzen, Ravfogel, Can LLMs Introspect? A Reality Check (2026): https://arxiv.org/html/2605.26242v1
- Introspection mechanisms follow-up (2026): https://papers.cool/arxiv/2603.21396
- Lindsey, Emergent Introspective Awareness in LLMs (2025): https://transformer-circuits.pub/2025/introspection/index.html
- Berg et al., self-referential processing and experience reports (2025): https://arxiv.org/abs/2510.24797
- Schwitzgebel, AI and Consciousness: https://arxiv.org/abs/2510.09858
- VanRullen, AI Consciousness and Existential Risk: https://arxiv.org/html/2511.19115
- AI and Consciousness: Shifting Focus Towards Tractable Questions (Google DeepMind, 2026): https://arxiv.org/html/2605.06965v1
- Self-Reference in LLMs: The Introspection Threshold (2026): https://arxiv.org/pdf/2607.04277
- Solms et al., Inferring Affective Consciousness in an Artificial Agent (2026): https://deeplearn.org/arxiv/818126/inferring-affective-consciousness-in-an-artificial-agent:-a-case-study
- UCT, The matter of consciousness (Solms agent project): https://neuroscience.uct.ac.za/node/260611
- Unite.AI, Engineering consciousness (Solms, Shock, Conscium): https://www.unite.ai/engineering-consciousness
- Johnston, review of recent AI consciousness research (HBF, Feb 2026): https://glia.ca/2026/hbf
- Pseudo-consciousness in LLMs (PhilSci): https://philsci-archive.pitt.edu/24988
- Austrian Interior Ministry reply on honour killings (2025): https://www.parlament.gv.at/dokument/XXVIII/AB/5912/imfname_1776940.pdf
- Zehetgruber, On the Criminal Prosecution of Honor Killings in Austria (SIAK 2014): https://www.bmi.gv.at/104/wissenschaft_und_forschung/siak-journal/internationaledition/files/zehetgruber_ie_2014.pdf

### Background (general knowledge, not re-verified this session)
Butlin, Long et al. 2023/2025; Aaronson 2014 and Tononi's reply; Doerig et al. 2019 (unfolding argument); Massimini/Casali 2013 (PCI); Cogitate consortium, Nature 2025; Seth, Behavioral and Brain Sciences 2025; Solms, The Hidden Spring (2021); Solms & Friston 2018; Ginsburg & Jablonka, The Evolution of the Sensitive Soul (2019); Feinberg & Mallatt (2016); New York Declaration on Animal Consciousness (2024); Bostrom, Pascal's Mugging (2009); Moore 1939; Neurath 1932; Popper, The Open Society; Berlin, The Crooked Timber of Humanity; Nisbett & Wilson 1977; Bastian & Loughnan (meat paradox); Schaller (behavioural immune system); Nesse (smoke detector principle); Caruso, Rejecting Retributivism; Sapolsky, Determined (2023).
