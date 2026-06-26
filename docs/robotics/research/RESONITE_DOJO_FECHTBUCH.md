# Resonite Dojo: Teaching Bots Medieval Swordfighting from Fechtbücher
## Architecture for LLM-Driven Combat Agents with Historical Source Material

**Created:** 2026-03-08  
**Status:** DESIGN / RESEARCH  
**Context:** Extension of `COMPUTE_LIMITS_SINGLE_GPU.md` dojo scenario  
**Related:** `EMBODIED_LLM_COGNITIVE_ARCHITECTURE.md`, `EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md`

> *"Medieval Fechtmeister manuals as training data for virtual combat agents."*  
> *This is not a metaphor. The manuals are structured, systematic, named, and directly translatable to bot decision logic.*

---

## 1. Why the Fechtbücher Are Ideal Source Material

The surviving German and Italian fighting manuals (Liechtenauer, Fiore dei Liberi, Talhoffer, Ringeck, Kal, von Danzig) are not narrative descriptions of violence. They are **systematic martial taxonomies**: named techniques, prerequisite guards, attack lines, counters, and conditional transitions. They read like decision trees written in Middle High German.

Key structural properties that map well to bot architecture:

**Named techniques:** Every action has a name. *Zornhau, Zwerchau, Krumphau, Schielhau, Scheitelhau* — the five master strikes. Each has: a guard it attacks, a counter it defeats, conditions for use, follow-on options. This is already a skill library schema.

**Guard system:** Vom Tag, Ochs, Pflug, Alber, Eisenport — named positions with explicit strengths/weaknesses against other guards. A bot in Ochs (ox guard, point threatening the opponent's face) has a different action space than a bot in Alber (fool's guard, an invitation/trap). This is a state machine with named states.

**Conditional logic:** "If he strikes from the right, do X. If he binds strong, do Y. If he withdraws, do Z." The Fechtbücher are full of if-then-else encoded in verse and prose. Direct translation to decision context.

**Fehler and Nachreisen:** Feinting (Fehler) and following the opponent's retreating weapon (Nachreisen) are explicit concepts with descriptions. A bot can have these as named skills with conditions for deployment.

**Talhoffer specifically** — the one you presumably have — includes wrestling, dagger work, judicial combat, and siege weapons. Notably pragmatic: techniques designed to end fights quickly, including eye attacks, groin strikes, and throws from a clinch. The "bloodcurdling" quality you mention is that these aren't sport techniques — they're designed to kill or severely injure.

---

## 2. The Knowledge Pipeline: From PDF to Bot Skill

### Step 1: Source Processing

The manuals exist as:
- Scanned manuscripts (Getty, Wiktenauer archives — freely available)
- Modern transcriptions with translation (Wiktenauer.com is the canonical resource)
- Your personal collection (presumably PDFs, possibly with commentary)

The Wiktenauer corpus for Liechtenauer's Zettel alone runs to hundreds of techniques with commentary from multiple Fechtmeister traditions.

**Processing approach:**
```
PDF/scan → OCR (if needed) → structured extraction → technique database
```

Each technique gets a record:
```json
{
  "name": "Zornhau",
  "tradition": "Liechtenauer",
  "source": "Codex Döbringer",
  "guard_origin": "vom Tag",
  "guard_countered": "any upper guard",
  "technique_defeats": "strong upper strikes",
  "execution": "diagonal strike from shoulder, 'wrathful hitter'",
  "follow_ons": ["Zornhau Ort", "wind into Ochs", "Absetzen"],
  "counters": ["Zwerchau", "Krumphau"],
  "conditions": {
    "bind_hard": "wind to thrust",
    "bind_soft": "strike through",
    "opponent_withdraws": "Nachreisen"
  },
  "tags": ["meisterhau", "oberhau", "sword"]
}
```

This is a vector-searchable skill database. The bot doesn't memorize every technique — it retrieves relevant ones contextually during a fight.

### Step 2: Guard State Machine

The guards define the bot's state at any moment:

```
Guards (Huten):
  vom Tag (from the roof) — aggressive, waiting to strike
  Ochs (ox) — threatening thrust to face/chest, upper bind
  Pflug (plow) — threatening thrust to lower body, lower bind  
  Alber (fool) — invitation, counterattack trap
  Nebenhut (side guard) — defensive, off-side
  Eisenport (iron gate) — low, defensive

Transitions between guards are actions.
The opponent's guard determines which techniques are "open."
```

This is a **state-action-opponent_state → technique** mapping, which is exactly what the Fechtbücher provide.

### Step 3: The Nachschlag (Learning Loop)

After each exchange, the bot performs a *Nachschlag* (literally "after-strike" — in context, an after-action review):

> "I was in Alber as an invitation. He struck Oberhau (upper strike). I responded with Zornhau. He bound hard. I tried to wind to thrust but he had already withdrawn. I was hit. Counter: should have used Nachreisen when he withdrew, not the wind."

This maps exactly to the episodic memory + sleep-phase analysis architecture. The Fechtbücher even have a name for this: *Indes* — the concept of the "meanwhile," the critical moment of decision in a bind. The bots are training *Indes* judgment.

---

## 3. Resonite Implementation Architecture

### World Setup

Resonite provides:
- Physics (hitboxes, collision, weapon reach)
- Avatar bodies with skeletal animation
- Shared world state readable by both bots
- LogiX for world scripting (can write sensor data out to external systems)

What needs to be added:
- **Action interface:** A set of named actions the bot can invoke (strike from guard X, transition to guard Y, bind, withdraw, feint)
- **Sensor interface:** What does the bot "see"? Opponent guard, distance, weapon position, hit state
- **Communication bridge:** Resonite ↔ external LLM (websocket or local API call)

### Bot Decision Loop

```
Every ~500ms (action tick):

1. Read world state:
   - My current guard
   - Opponent's current guard  
   - Distance (far/measure/close/grapple)
   - Bind state (if weapons are crossed)
   - My health/hit state
   - Round history (last 5 exchanges)

2. Retrieve relevant techniques:
   - Vector search skill database for current state
   - Returns 3-5 relevant techniques with conditions
   
3. LLM reasoning (7B, fast):
   Context: [current state] + [retrieved techniques] + [recent history]
   Output: chosen action + brief reasoning

4. Execute action in Resonite

5. Log exchange to episodic memory
```

### Post-Round Analysis (Nachschlag)

```
After each round (~10-30 seconds):

1. Load full round log (all exchanges)
2. Run 72B analysis model:
   - Which techniques worked? Which failed?
   - Were there opportunities missed? (Indes failures)
   - Does the opponent show patterns?
   - What should change in the skill priority?
3. Update skill library weights
4. Write behavioral intentions for next round
5. (Optionally) add new technique derivations: 
   "Opponent consistently drops guard after Zwerchau — 
    this creates an opening not in the source material"
```

This last point is interesting: the bot can **derive novel techniques** not in the Fechtbücher, based on opponent-specific patterns. The source material is the starting knowledge; experience extends it. This is roughly what historical fighters actually did.

---

## 4. What Different Bot Architectures Produce

### Bot A: Pure Fechtbuch Follower
Only uses techniques explicitly from the source. Plays by the system. Predictable but coherent.

### Bot B: Adaptive Learner
Starts from Fechtbuch knowledge, actively derives opponent-specific counters. May develop "bad habits" from the opponent (learns cheesy tactics that work against Bot A but wouldn't work against a fresh opponent).

### Bot C: Different Tradition
Feed one bot Liechtenauer's longsword tradition and the other Fiore dei Liberi's Italian system. They have different guards, different named techniques, different tactical philosophy (Liechtenauer is aggressive and initiative-focused; Fiore is more patient and counter-oriented). This is historically plausible — these traditions competed in real judicial combats.

### Bot D: No Source Material Baseline
An LLM with no Fechtbuch knowledge, just told "fight with a sword." Probably discovers generic striking patterns. Comparison against Bot A shows whether the structured historical knowledge produces meaningfully better tactics.

---

## 5. Compute Requirements (Realistic)

### During combat (per bot):
- Model: Qwen-7B or Mistral-7B
- Context: ~2000 tokens (state + retrieved techniques + history)
- Latency: 200-400ms per action tick
- Both bots simultaneously: ~14GB VRAM — fits in 24GB ✅

### Post-round analysis:
- Model: Qwen-72B (CPU offload, 64GB RAM available)
- Context: ~8000 tokens (full round log + skill library)
- Latency: 15-30 seconds — fine between rounds ✅
- One instance, sequential: doesn't need to be parallel ✅

### Skill database:
- ~1000 techniques from major Fechtbücher: trivial (ChromaDB or FAISS, few MB)
- Vector search latency: <50ms ✅

### Total: Runs on Goliath without compromise. ✅

The only limitation: if you want both bots running full 70B models simultaneously during combat at reactive latency, that needs more VRAM. For the 7B combat loop with 72B post-round analysis, the 4090 + 64GB RAM is entirely sufficient.

---

## 6. The Research Questions This Actually Answers

Running this produces data on several genuinely open questions:

**Does structured domain knowledge improve LLM agent performance?**
Bot D (no source) vs. Bot A (Fechtbuch) tells you whether feeding historical technique databases produces meaningfully better behavior or whether the LLM re-derives similar patterns anyway.

**Does episodic learning produce genuine skill development or just pattern memorization?**
After 500 rounds, does Bot B develop tactics that transfer to a new opponent, or only tactics tuned to Bot A's specific patterns? This is the generalization question from the cognitive architecture doc.

**Can LLMs derive novel techniques from opponent observation?**
Does the post-round analysis produce actionable new tactics, or just restate what happened? The quality of the derived insights is testable against the source material: does the bot discover techniques the Fechtmeister knew about?

**Do different traditions produce stylistically distinct fighters?**
Liechtenauer vs. Fiore — does the different source material produce bots with recognizably different fighting styles, or does the LLM homogenize them?

---

## 7. The Fechtbücher as a General Pattern

The swordfighting case generalizes to a broader architectural pattern:

**Any structured domain knowledge + episodic experience + LLM reasoning = learnable skill agent**

The Fechtbücher work because they're already structured as: named states, conditional transitions, technique names with conditions. Other domains with this structure:

- Chess openings / endgame tablebases (already done extensively, less interesting)
- Go joseki (same)
- Poker hand taxonomy (done)
- **Martial arts kata** — other combat systems with named techniques and counters
- **Musical theory** — a jazz bot that learns from Real Book chord charts and develops its own voice over thousands of sessions
- **Cooking technique taxonomy** — a culinary agent that learns from Escoffier and develops novel dishes

The Fechtbücher are a particularly good case because: the source material is rich, the domain is well-defined, the performance is measurable (who wins), and the knowledge is historically interesting in its own right.

---

## 8. Source Material Availability

For the pipeline, the best sources beyond your personal collection:

**Wiktenauer** (wiktenauer.com): Complete digitized corpus of surviving Fechtbücher with transcription and translation. Free, comprehensive. The Liechtenauer tradition alone runs to ~20 major manuscripts.

**HEMA Alliance / HEMA Scholars**: Interpreted technique descriptions with video. Useful for disambiguation when the manuscript language is ambiguous.

**Specific manuscripts of interest:**
- Codex Döbringer (1389) — earliest Liechtenauer commentary
- Hans Talhoffer Fechtbuch (multiple versions, 1443–1467) — most illustrated, most brutal
- Fiore dei Liberi, Flos Duellatorum (1410) — Italian system, excellent structure
- Joachim Meyer (1570) — late tradition, very systematic and well-organized, good for extraction
- Paulus Kal (1470s) — guild master list + techniques

Meyer's 1570 manual is probably the most extraction-friendly due to its systematic organization. Talhoffer has the best illustrations but the most terse text.

---

## 9. Subproject: The Talhoffer Butler — Home Security Training

### Concept

The same pipeline that teaches dojo bots medieval swordfighting can train a household robot in *practical personal protection* — not sport, not performance, but the pragmatic threat-neutralization philosophy that Talhoffer's judicial combat clients paid for.

Talhoffer's manuals are explicitly calibrated for asymmetric, mortal encounters against motivated opponents. His techniques assume: the opponent is also trained, also trying to win, and there are no rules. This is precisely the threat model for home intrusion.

The bot's name is Rovo. The scenario: Sandra is in Tokyo. Goliath is home. Benny is home. An intruder enters.

This is **Home Alone VII**, but the traps are not paint cans and hot doorknobs. They are *systematically derived from a 15th-century Fechtmeister*.

---

### What Talhoffer Specifically Contributes

The 1467 Talhoffer manuscript (the one in the collection) is the most practically brutal of the surviving manuals. Relevant sections for a home defense agent:

**Messer (single-handed sword / large knife):** Shorter range, interior spaces. Talhoffer's messer work is fast and close — exactly right for hallways and rooms. Techniques include: closing the distance under a strike, redirecting the weapon arm, transitions to grapple when too close to use the blade.

**Dagger work:** When weapons are improvised (kitchen knives, tools). Sequential techniques for disarming, controlling, and neutralizing. Talhoffer is unusually detailed on what happens *after* the initial contact — the follow-through.

**Grappling / Ringen:** Unarmed or weapon-lost scenarios. Joint locks, throws, ground control. Plate sequences show the transition from standing to ground in explicit steps.

**The judicial combat dirty tricks:** These are the "bloodcurdling" sections — techniques explicitly designed for when losing means death. Eye attacks, throat grabs, groin strikes used as setup for a throw, sand/dust as a distraction tool. Talhoffer's implicit philosophy: *there is no such thing as fighting dirty when you are fighting for your life*.

This maps directly to home defense threat calculus: a robot protecting occupants has no sporting obligation to its opponent.

---

### Architecture

The home defense subproject extends the dojo architecture with:

**Threat assessment module:**
- VLM classifies incoming person: familiar/unfamiliar, posture (aggressive/neutral), carried objects
- Escalation states: Monitoring → Alert → Active threat
- Rovo does not engage until Active threat is confirmed (multiple sensor agreement)

**Talhoffer skill library (filtered):**
- Source: Talhoffer 1467, messer + dagger + ringen sections
- Extracted and tagged as before, but filtered for: close-quarters, improvised weapons, small spaces, single operator vs. single intruder
- Techniques rated by: required physical capability (Rovo's actuators), spatial requirement (hallway vs. room), risk of collateral damage (Benny is present)

**Deterrence-first hierarchy:**
Talhoffer himself understood escalation — his manuals include pre-fight posturing and verbal challenge. Rovo's decision tree:
1. Presence announcement ("This property is monitored. Identify yourself.")
2. Alert escalation ("You are being recorded. Leave now.")
3. Active deterrence (loud alarm, lights, Goliath wakes up and calls Sandra)
4. Physical intervention only if Benny or property is under active threat

Physical intervention is the last step, not the first. This is also good Talhoffer: he recommends winning before the fight starts when possible.

**Post-incident Nachschlag:**
Same analysis loop as the dojo — what happened, what worked, what to update. Over time, Rovo builds a model of common intrusion patterns (attempted entry points, times, methods) and adjusts monitoring priorities accordingly.

---

### The Research Question This Poses

Can an LLM-embodied robot develop genuine *threat judgment* — distinguishing a real threat from a false positive (delivery person, neighbor, Benny knocking something over) — and calibrate response appropriately?

This is harder than the dojo, because:
- In the dojo, everything is a valid target. In the home, almost nothing is.
- The cost of false positive (attacking an innocent person) vastly exceeds the cost of false negative (intruder escapes).
- Threat assessment requires multi-sensor fusion (VLM + audio + motion + time-of-day prior) not just opponent guard recognition.

Talhoffer knew this too: his judicial combat clients faced legal consequences for striking first without cause. The *Vorschlag* (first strike) had to be justified. The ethics were baked into the practice.

---

### Why This Is Actually Useful

Most home security robots are either:
- Passive monitors (camera, alarm trigger) with no physical capability
- Industrial robots repurposed for security — dangerous, unsubtle, not domestically viable

A small mobile robot (Yahboom class) with LLM reasoning, Talhoffer-derived threat assessment, and a clear escalation hierarchy is something different: *a domestically proportionate, legally defensible, historically-informed security agent*.

The "historically-informed" part is not a gimmick. Talhoffer's system was explicitly calibrated for: single operator, mortal stakes, small space, improvised environment, no rules. That is the actual threat model for home intrusion. His solutions are not elegant — they're *efficient*.

Rovo trained on Talhoffer, with explicit deterrence-first hierarchy and Benny-safe physical constraints, is a plausible and genuinely novel home security system. It would also be an extremely good demo for Ednaficator or any future commercial robotics application.

*Working title: Project Fechtmeister.*

---

*Tags: [resonite, dojo, fechtbuch, hema, talhoffer, multi-agent, embodied-ai, skill-learning, home-security, butlerbot, research, high]*
