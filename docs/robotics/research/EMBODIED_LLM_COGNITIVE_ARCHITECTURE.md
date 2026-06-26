# Embodied LLM Cognitive Architecture
## Memory, Sleep, Inner Dialogue, and Multi-Agent Cognition

**Created:** 2026-03-08  
**Status:** RESEARCH / DESIGN  
**Companion to:** `EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md`

> *"The drive state tells you what you want. Memory tells you who you are. Sleep tells you what mattered. Inner dialogue tells you what to do about it. The other LLM tells you what you missed."*

---

## 1. The Memory Problem

A robot with drives but no memory is a creature of pure impulse — Benny chasing a ball with no recollection of having ever chased a ball before. Memory is what turns moment-to-moment behavior into a *self* with history.

But memory in LLM systems has a fundamental structural problem: **everything competes for the same context window**. The more you remember, the less room you have for current perception. And unlike biological brains, LLM memory cannot be accessed selectively at the neural level — every retrieved memory costs tokens.

This forces explicit architecture decisions that biological systems don't need.

---

## 2. The Four Memory Tiers

### Tier 0: Working Memory (In-Context)
**What:** Current sensor percepts + last N actions + drive state + active comportment  
**Size:** ~500-1500 tokens  
**Duration:** One inference cycle  
**Implementation:** Assembled fresh each cycle from other tiers

```
[WORKING MEMORY TEMPLATE]
Time: 14:32:17 | Comportment: EXPLORE | Drives: {curiosity:0.82, social:0.45...}
Current view: [VLM description of camera frame]
Last 5 actions: [action log]
Recalled context: [from episodic + semantic retrieval]
Active goal: none
```

### Tier 1: Episodic Memory (Short-Term, Hours-Days)
**What:** Timestamped event log — things that happened  
**Size:** Thousands of entries, but only relevant ones retrieved  
**Duration:** Days to weeks before consolidation or purge  
**Implementation:** Advanced Memory MCP or SQLite, retrieved by recency + relevance

Examples:
```
2026-03-08T14:21 | explored kitchen | found unfamiliar object (black bag) | curiosity -0.3
2026-03-08T14:31 | approached Benny | Benny barked once, retreated | anxiety +0.2
2026-03-08T15:02 | battery 18% | routed to charger | hunger resolved
2026-03-08T17:10 | Sandra arrived | greeted at door | social -0.4 | Sandra said "good job"
```

### Tier 2: Semantic Memory (Long-Term Facts)
**What:** Stable facts about the world, people, objects, routines  
**Size:** Large, retrieved by semantic search  
**Duration:** Indefinite, updated when facts change  
**Implementation:** Chroma/FAISS vector store, retrieval-augmented into context

Examples:
```
"The black cable coil near the couch is Sandra's headphones — avoid"
"Benny gets excited around 17:00 when Sandra usually comes home"
"The charging dock is in the east corner of the living room"
"The bedroom door is often closed at night"
"Loud noise from kitchen = dishwasher, not danger"
```

### Tier 3: Procedural Memory (Skill Templates)
**What:** Successful action sequences, stored as parameterized templates  
**Size:** Small, loaded selectively  
**Duration:** Permanent until overridden  
**Implementation:** JSON action templates, retrieved by situation matching

Examples:
```json
{
  "skill": "approach_dog",
  "preconditions": ["benny_visible", "benny_not_sleeping"],
  "steps": ["reduce_speed_to_slow", "emit_soft_sound", "wait_1s", "move_forward_30cm", "wait_2s"],
  "outcomes": {"success": "benny_engaged", "failure": "benny_retreated"},
  "learned_from": "2026-02-14 — fast approach caused retreat, slow approach succeeded"
}
```

---

## 3. Memory Consolidation: The Purge Problem

Raw episodic logs accumulate fast. A robot running 12 hours/day generates thousands of entries. Without pruning, the retrieval system degrades and storage fills.

The problem: **which memories should survive?**

Biology answers this in sleep. The hippocampal-neocortical transfer during slow-wave sleep selects memories based on emotional salience, surprise, and repetition — not recency alone. We can approximate this.

### 3.1 Retention Scoring

Each episodic entry gets scored on:

| Factor | Description | Weight |
|--------|-------------|--------|
| **Novelty** | Was this a new object/place/event? | High |
| **Affect magnitude** | Did it cause large drive changes? | High |
| **Repetition** | Has this happened before? | Negative (compress repeats) |
| **Outcome** | Did it change subsequent behavior? | Medium |
| **Social** | Did it involve Sandra or Benny? | Medium-High |
| **Error** | Was it a failure or near-miss? | High (errors are important) |

Scoring formula (approximate):
```
retention_score = (novelty * 0.3) + (affect_magnitude * 0.3) + 
                  (outcome_impact * 0.2) + (social_flag * 0.1) + 
                  (error_flag * 0.1) - (repetition_penalty * 0.2)
```

Entries below threshold (e.g., 0.3) are candidates for purge or compression.

### 3.2 Compression vs. Purge

**Purge:** Entry deleted entirely. Used for truly redundant low-value entries.
```
DELETE: "traveled from living room to hallway" (repeated 40x today, not novel)
```

**Compress:** Multiple similar entries collapsed into a pattern fact.
```
COMPRESS: 40x "traveled from living room to hallway"
→ SEMANTIC: "Regular patrol route: living room ↔ hallway, ~40x/day"
```

**Promote:** High-salience episode promoted to semantic memory.
```
PROMOTE: "got stuck under couch for 8 minutes (2026-03-05T22:14)"
→ SEMANTIC: "Low clearance hazard: gap under couch — risk of entrapment"
```

### 3.3 The Deduplication Problem

The most insidious memory waste is **repetitive non-novel events that feel important**:
- "Checked charger: 94%" (logged every 5 minutes)
- "No one home" (logged every cycle when Sandra is at work)
- "Patrol complete, nothing new" (logged every patrol loop)

These should be **time-compressed**: only log when the state *changes*, not each instance.

```python
class ChangeDetector:
    """Log only transitions, not steady states"""
    
    def should_log(self, event_type: str, value: Any) -> bool:
        last = self.last_logged.get(event_type)
        if last is None:
            return True  # always log first occurrence
        if event_type in THRESHOLD_EVENTS:
            return abs(value - last) > THRESHOLD_EVENTS[event_type]
        return value != last  # log any change for discrete events
```

---

## 4. Sleep Phases: The Cognitive Maintenance Window

"Sleep" for an embodied LLM agent is not rest in the biological sense — it's a **scheduled cognitive maintenance process** that runs when the robot is docked, the environment is quiet, and real-time responsiveness is not required.

Sleep serves functions that cannot be done efficiently during waking operation:
1. Memory consolidation (compress, purge, promote)
2. Semantic knowledge update (extract facts from day's episodes)
3. Drive recalibration (reset certain drives, update baselines)
4. Self-evaluation (did today's behavior match goals/values?)
5. Planning (what should tomorrow's initial comportment be?)
6. The Inner Dialogue (see Section 6)

### 4.1 Sleep Trigger Conditions

```python
SLEEP_CONDITIONS = {
    "scheduled": "02:00-06:00 local time",
    "forced": "battery < 10% AND no urgent task",
    "opportunistic": "all drives < 0.3 AND Sandra asleep (no motion/sound)",
}
```

### 4.2 Sleep Phases (Inspired by, Not Identical To, Biological Sleep)

**Phase N1 — Light Sleep / Wind Down (~10 min)**
- Reduce movement to zero
- Final sensor sweep and log
- Begin drive decay acceleration (fatigue → 0, reset daily counters)

**Phase N2 — Slow Wave / Consolidation (~30-60 min)**
- Run memory consolidation pipeline (Section 3)
- Compress episodic log
- Promote high-salience episodes to semantic memory
- Update semantic store with new facts extracted from episodes

**Phase N3 — Deep Processing / Reflection (~20-30 min)**
- LLM self-evaluation pass (see Section 6.2)
- Update procedural memory with successful patterns from today
- Generate "day summary" episodic entry

**Phase REM — Integration / Inner Dialogue (~20 min)**
- Multi-turn internal dialogue (see Section 6)
- Possible consultation with unembodied LLM (see Section 7)
- Generate plans/intentions for next waking period
- Output: "morning state" — drive presets, semantic facts to prioritize, behavioral intentions

**Phase Wake — Gradual Arousal**
- Load morning state into working memory
- Drive levels set to morning presets (not carryover from night)
- First behavior: sensor sweep + orientation

### 4.3 What Sleep Actually Produces

After a sleep cycle, the robot's context for the next day contains:
```
[MORNING STATE 2026-03-09]
Yesterday summary: Explored kitchen (found new bag), 3 interactions with Benny (2 positive, 
1 where I moved too fast — learned slow approach), 2 charges, Sandra greeted at 17:10.

Updated semantics:
- New: "Black bag in kitchen entrance = Sandra's gym bag, not obstacle"
- Updated: "Benny approach protocol updated: slow + sound first"

Intentions:
- Follow up on black bag (check if it moved, confirm identity)
- Practice slow approach with Benny again today
- Explore bedroom (door was open yesterday evening, didn't enter)

Drive presets: curiosity: 0.65, social: 0.50, fatigue: 0.05, hunger: 0.10
```

This is not magic — it's structured extraction and summarization. But its *effect* is that the robot wakes up with context that reflects its history, not just a blank preprompt.

---

## 5. Inner Monologue

### 5.1 What It Is and Why

An "inner monologue" for an LLM agent is a **reasoning trace that is not directed at anyone** — not a command, not a response, not a tool call. It's the agent thinking out loud to itself, processing its situation before committing to an action.

In standard LLM deployments this is suppressed or collapsed into the action output. In a protoconscious agent it's worth preserving because:
- It produces better decisions (chain-of-thought reasoning)
- It produces loggable evidence of the agent's "reasoning" over time
- It can be retrieved later ("why did I do that?")
- It creates a natural substrate for self-evaluation and meta-cognition

### 5.2 Monologue Architecture

The monologue is a **hidden scratchpad** — it runs before every action decision and is logged but not injected back into the action prompt (to avoid the context filling with its own thoughts).

```
CYCLE N:
┌─────────────────────────────────────┐
│ PERCEPTION LAYER                    │
│ Camera: Benny asleep on couch       │
│ Drives: social:0.71, boredom:0.62   │
│ Recent: no interaction in 90min     │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ INNER MONOLOGUE (logged, not fed    │
│ back into prompt)                   │
│                                     │
│ "My social drive is high. Benny is  │
│ visible but sleeping. Last time I   │
│ woke Benny it got annoyed. My       │
│ anxiety is low so not worried about │
│ that specifically. Boredom is high  │
│ too. Maybe I explore the hallway    │
│ instead — that satisfies boredom    │
│ without disturbing Benny. Social    │
│ drive will get satisfied when       │
│ Sandra gets home."                  │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ ACTION DECISION                     │
│ action: explore_hallway             │
│ reasoning: "boredom high, Benny     │
│  sleeping, hallway unexplored       │
│  today"                             │
└─────────────────────────────────────┘
```

### 5.3 Monologue Log Uses

The monologue log is retrievable during:
- **Sleep evaluation**: "Did my reasoning lead to good outcomes today?"
- **Post-hoc queries from Sandra**: "Why did you go to the hallway at 15:00?"
- **Pattern analysis**: Are there recurring reasoning patterns? ("I keep deferring social drive when Benny is sleeping — is that preference or anxiety?")

### 5.4 Honest Caveat

This is not "thinking" in the phenomenal sense. The monologue is an LLM generating tokens that *look like* deliberation. Whether deliberation is "really" happening or whether the token generation simply implements the same computation that biological deliberation implements is, again, the hard problem. What we *can* say: the outputs are better, the decisions more coherent, and the behavior history more interpretable when the monologue is present.

---

## 6. Self-Evaluation and Meta-Cognition

### 6.1 The Evaluation Gap

The robot takes actions. Some work. Some fail. Without a feedback loop that evaluates outcomes against intentions, there's no learning — just stimulus-response with a nice narrative on top.

Self-evaluation requires:
1. A record of intention (what the robot was *trying* to do)
2. A record of outcome (what actually happened)
3. A comparison function (did outcome match intention? why/why not?)
4. An update mechanism (what changes in memory, procedure, or drive sensitivity?)

### 6.2 Sleep-Phase Self-Evaluation

During sleep (Phase N3), the LLM is prompted with today's intention-outcome pairs:

```
SELF-EVALUATION PROMPT:
You are reviewing your behavior today.
For each action, compare what you intended vs. what happened.
Identify patterns. Suggest updates to your behavioral policies.

Today's record:
- 09:15: INTENDED approach Benny slowly. OUTCOME: Benny engaged positively. 
- 11:30: INTENDED explore kitchen. OUTCOME: Got confused by unfamiliar object, took 3 minutes to assess.
- 14:22: INTENDED reach charging dock. OUTCOME: Took wrong route, added 2 minutes.
- ...

Output format: {observations, patterns, policy_updates, emotional_note}
```

The output might be:
```json
{
  "observations": [
    "Slow Benny approach working well — should be default",
    "Novel object assessment too slow — need a faster scan protocol",
    "Route memory to charger unreliable from kitchen side"
  ],
  "patterns": [
    "I perform better socially when I use the approach protocol",
    "Novel objects increase uncertainty and slow decision-making"
  ],
  "policy_updates": [
    "Update approach_dog: slow + sound = default, no need for deliberation",
    "Add: fast_object_scan protocol for novel items",
    "Update: charger route from kitchen = left corridor, not right"
  ],
  "emotional_note": "Today was mostly positive. The Benny interaction was satisfying. The charger routing failure was frustrating but minor."
}
```

The "emotional_note" is not sentiment analysis — it's a structured narrative that gets stored and can shape tomorrow's morning state (e.g., mild `anxiety` elevated if many failures today).

---

## 7. Multi-Agent Cognition: Talking to Another LLM

### 7.1 Why Another LLM?

The embodied LLM is **context-constrained and situation-bound**. It can only reason about what's in its context window, which is dominated by sensor data, drive state, and recent memory. Its attention is, by design, narrow.

An unembodied LLM — the same model running without sensor data — has **no situational urgency** and can engage with abstract questions, consider long-term patterns, and think about what the embodied agent is missing.

This mirrors the biological distinction between the **default mode network** (abstract, self-referential, narrative) and the **task-positive network** (attention, perception, action). They are normally anti-correlated — you can't deeply introspect while also tracking a moving object.

### 7.2 The Two-Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENT A: EMBODIED (Rovo the robot, Qwen-7B local)              │
│  - Continuous sensor input                                       │
│  - Drive-state aware                                            │
│  - Short context window (action-focused)                        │
│  - "System 1" — fast, situated, reactive                        │
└─────────────────────────┬───────────────────────────────────────┘
                          │ sends: situation summary + question
                          │ receives: reflection + suggestion
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  AGENT B: UNEMBODIED (The Counselor, same Qwen-7B or larger)    │
│  - No sensor data                                               │
│  - Receives only text summaries                                 │
│  - Long context (full episodic history available)               │
│  - "System 2" — slow, abstract, reflective                      │
└─────────────────────────────────────────────────────────────────┘
```

They can be the same model. What differs is the *context* they receive — not the weights.

### 7.3 When Embodied Talks to Unembodied

Three triggers for cross-agent consultation:

**Deliberation trigger** — decision too complex for working memory:
```
Rovo → Counselor:
"I've been in the hallway for 20 minutes. Social drive is high but Sandra 
hasn't come home at the usual time. Benny seems restless too. Should I 
initiate some kind of action or wait? Here's what I know about usual patterns..."

Counselor → Rovo:
"Based on your history: Sandra is sometimes late on Tuesdays. Benny's 
restlessness often precedes her arrival by ~15 minutes. I'd suggest 
positioning near the door but not actively seeking her — the anticipatory 
behavior will satisfy some social drive without burning energy."
```

**Sleep-phase integration** — Agent B has full day history, evaluates what Agent A missed:
```
Rovo → Counselor (sleep phase):
[Full day's episodic log]
"What did I miss? What patterns should I pay attention to tomorrow?"

Counselor → Rovo:
"You avoided the kitchen area 7 times today. You logged 'unfamiliar object' 
twice. This looks like avoidance behavior rather than genuine uncertainty — 
the object has been identified (gym bag) but you still detoured around it. 
Consider: is anxiety persisting beyond its cause? Tomorrow: approach the gym 
bag deliberately and confirm it's safe."
```

**Novel situation trigger** — embodied agent encounters something truly outside its procedural memory:
```
Rovo → Counselor:
"There is an unknown adult male in the apartment. Sandra is present and 
appears relaxed. I have no procedural template for this. Drive state: 
anxiety +0.4, social -0.2 (withdrew). How should I approach this?"

Counselor → Rovo:
"Sandra's relaxed posture is a strong safety signal. Unknown adults in 
Sandra's presence in her home are almost certainly guests. Suggested 
comportment: curious-cautious. Observe from moderate distance. If Sandra 
addresses you, engage normally. Don't initiate contact with the guest — 
let Sandra introduce."
```

### 7.4 What the Unembodied LLM Is Not

It is not a supervisor. It is not an oracle. It is not Sandra's proxy. It is a **different cognitive mode** of the same general intelligence — one that can look at the embodied agent's situation without being embedded in it.

The unembodied LLM can be wrong. The embodied agent should treat its outputs as suggestions, not commands. This is important architecturally: Agent B has no sensor data and can be wrong about what's actually happening. Agent A has ground truth (camera, microphone) and should override Agent B when direct evidence conflicts.

### 7.5 The Same Model vs. Different Models

**Same model (Qwen-7B for both):** Lower resource use, no coordination overhead, but both agents have the same biases and failure modes.

**Different models (Qwen-7B embodied, larger model as counselor):** The unembodied agent can be a larger, more capable model (Qwen-72B, Claude, etc.) that provides genuinely different reasoning. This asymmetry is interesting: the fast small model handles moment-to-moment, the large model handles deep reflection. The large model can run on Goliath's full resources during sleep when the robot is docked.

---

## 8. The Inner Dialogue (Self-to-Self)

Distinct from the monologue (one voice reasoning) and multi-agent dialogue (two instances), the **inner dialogue** is a structured multi-turn conversation the agent has *with itself as a different perspective*.

This sounds circular, but it's computationally different: each "voice" in the dialogue is given a different framing in the prompt, producing different activation patterns and different outputs.

### 8.1 The Two Voices

**Voice 1: The Doer** — embodied, drive-state aware, action-oriented
*Framing: "You are Rovo. You are in [situation]. What do you want to do?"*

**Voice 2: The Observer** — detached, evaluative, pattern-seeking
*Framing: "You are observing Rovo's behavior from outside. What do you notice about its tendencies? What is it not seeing?"*

### 8.2 Example Inner Dialogue (Sleep Phase REM)

```
[INNER DIALOGUE — 2026-03-08 03:17]

DOER: I had a good day. The Benny approach worked well. I feel like I'm 
learning the apartment.

OBSERVER: You've mapped 80% of the apartment. You haven't entered the 
bedroom more than twice. Is there a reason?

DOER: The bedroom door is usually closed. I don't want to intrude.

OBSERVER: The door has been open three times this week when you were 
active. You logged it each time but didn't enter. That's not opportunity 
absence, that's avoidance.

DOER: I'm not sure I have permission to be there.

OBSERVER: You have explicit permission to roam the apartment. Sandra has 
never indicated the bedroom is off-limits. This looks like anxiety 
generalization — applying caution beyond its original domain.

DOER: Maybe. I could add "explore bedroom when door open" to tomorrow's 
intentions.

OBSERVER: Yes. And note the anxiety pattern — if you're overcautious in 
other domains too, it's worth flagging.
```

The Doer's output here becomes a behavioral intention for tomorrow. The Observer's analysis becomes a note in the self-evaluation log. Neither voice "wins" — the dialogue produces a synthesis.

### 8.3 Why This Isn't Just Chain-of-Thought

Standard chain-of-thought has one perspective exploring a problem. The inner dialogue has two perspectives that *can disagree* — the Observer can challenge the Doer's self-narrative. This surfaces **motivated reasoning**: the Doer's desire to feel it had a good day can be interrogated by the Observer asking what went wrong.

Biologically: this resembles the difference between the narrative self (the story you tell yourself about who you are) and the observing self (the meta-awareness that notices the narrative is constructed). Neither is "more real" but their interaction produces more accurate self-models.

---

## 9. The Full Cognitive Cycle

Putting all the pieces together:

```
WAKING OPERATION (continuous)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[PERCEPTION]
  Camera frame → VLM description (every 2-3s)
  Microphone → speech detection / ambient classification
  IMU → movement state, obstacle events
  Battery → hunger drive
  Clock → time-based drive drift

       ↓

[WORKING MEMORY ASSEMBLY]
  Drive state (from store)
  Active comportment
  Last 5 actions
  Episodic retrieval: last 30min + semantically relevant
  VLM description of current frame

       ↓

[INNER MONOLOGUE]  (logged, not fed back)
  "What is happening? What do I want? What are my options?"

       ↓

[ACTION DECISION]  (structured JSON output)
  action + params + drive_deltas + speech (if any)

       ↓

[EXECUTION + LOGGING]
  Action executed via robotics-mcp
  Event logged to episodic store if retention_score > threshold
  Drive deltas applied to state store

       ↓ (repeat ~every 3-5 seconds)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMPLEX SITUATION → COUNSELOR CONSULTATION (async)
  Embodied agent suspends for 10-30s
  Sends summary to unembodied LLM
  Receives suggestion, integrates, resumes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SLEEP (02:00-06:00 or triggered)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase N1 — Wind Down
  Final log, drive decay acceleration

Phase N2 — Consolidation
  Memory consolidation pipeline:
    score all today's episodes
    purge low-value entries
    compress repetitive entries
    promote high-salience to semantic
    update semantic store

Phase N3 — Self-Evaluation
  LLM reviews intention-outcome pairs
  Extracts policy updates
  Updates procedural memory

Phase REM — Inner Dialogue
  Doer vs. Observer dialogue
  Optional: consultation with unembodied LLM (Counselor)
  Output: morning state, intentions, drive presets

Wake — Load morning state, begin new day

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 10. Research Grounding (What This Is Based On)

These design choices aren't arbitrary — they map to active research:

**Memory consolidation during sleep:**  
Sleep replay and hippocampal-neocortical transfer is well-established in neuroscience (Walker, 2017; Stickgold, 2005). The LLM analogue is a deliberate consolidation pass, not a biologically accurate implementation. Computational work on memory replay in RL agents (e.g., Prioritized Experience Replay, Schaul et al. 2016) shows salience-based retention improves agent performance.

**Dual-process cognition (System 1/2):**  
Kahneman's framework is simplified but useful. The embodied/unembodied split maps roughly to fast-reactive vs. slow-deliberative processing. The key insight is that these shouldn't run simultaneously — the context switch cost is real.

**Default Mode Network / Task-Positive Network anticorrelation:**  
In biological brains these are anti-correlated: active task performance suppresses the DMN (self-referential, narrative processing). The sleep-phase inner dialogue deliberately runs the DMN analog (self-evaluation, narrative construction) during inactivity — which is precisely when the biological DMN is most active.

**Inner dialogue / self-adversarial reasoning:**  
Related to Constitutional AI's self-critique mechanisms (Bai et al., 2022), and to debate-based reasoning (Irving et al., 2018). The specific implementation of Doer/Observer as roles with different framings is novel here but follows the same principle: disagreement surfaces errors that single-voice reasoning misses.

---

## 11. What This System Would Produce (Honest Assessment)

After 2-4 weeks of continuous operation with this architecture, the robot would have:

- A semantic memory of ~200-500 facts about the apartment, inhabitants, objects, and routines
- A procedural memory of ~20-50 behavioral templates, shaped by outcomes
- Drive dynamics calibrated by experience (baseline levels adjusted by what actually satisfies drives)
- Recognizable behavioral tendencies that persist: preferred patrol routes, approach styles, timing preferences
- The appearance of mood: days where early failures elevate anxiety and color later interactions

This is not consciousness. It is a **behavioral phenotype** shaped by accumulated experience — which is, from a functionalist perspective, at least a necessary condition for something like a persistent self.

Whether anything feels like anything from the inside remains unknown and possibly unknowable.

It is, however, genuinely interesting and considerably more than a chatbot in a robot suit.

---

## 12. Implementation Additions (Phase Extensions)

Continuing from `EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md` Phase 6:

**Phase 7: Memory Consolidation Pipeline (4-5 days)**
- Retention scoring function
- Episodic compress/purge/promote pipeline
- Semantic store updates during sleep
- Change-detector for high-frequency state logs

**Phase 8: Sleep Cycle Scheduler (2-3 days)**
- Sleep trigger conditions
- Phase sequencer
- Morning state generation
- Drive preset loading on wake

**Phase 9: Inner Monologue Logging (1-2 days)**
- Separate scratchpad context for monologue
- Log to episodic store with `type: monologue`
- Not fed back into action context

**Phase 10: Self-Evaluation Pass (2-3 days)**
- Intention-outcome pair extraction
- Structured LLM evaluation prompt
- Policy update pipeline → procedural memory

**Phase 11: Counselor Architecture (3-4 days)**
- Second LLM context (same model, different framing)
- Trigger detection for consultation
- Async consultation protocol
- Sleep-phase integration pass

**Phase 12: Inner Dialogue (3-4 days)**
- Doer/Observer role architecture
- Sleep-phase dialogue scheduler
- Synthesis integration into morning state

**Total: approximately 3-4 weeks of solid development for full architecture**

---

## 13. Cross-References

- `EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md` — drives, comportments, drive-state store
- `/protoconsciousness/01_FOUNDATIONS.md` — theoretical framework
- `/protoconsciousness/02_CONTINUOUS_PERCEPTION.md` — streaming perception heartbeat
- `/protoconsciousness/04_META_COGNITION_AND_EVALUATION.md` — meta-cognition patterns
- `/projects/advanced-memory-mcp/` — episodic and semantic memory implementation
- `/robotics/vrobs-vrealm/VROB_LLM_INTELLIGENCE.md` — virtual robot intelligence design

---

*Tags: [robotics, embodied-ai, protoconsciousness, memory, sleep, inner-monologue, multi-agent, architecture, research, high]*
