# Embodied LLM Motivational Architecture
## Toward Protoconsciousness in Small Robots

**Created:** 2026-03-08  
**Status:** RESEARCH / ACTIVE  
**Related:** `/protoconsciousness/`, `/robotics/yahboom/`, `/robotics/vrobs-vrealm/`

> *"A Yahboom robot car running around the apartment is not a toy. It is a minimal viable agent. The question is: what does it WANT?"*

---

## 1. The Problem: LLMs Have No Drives

A preprompt saying *"I am a robot, I explore the apartment and help Sandra"* is a costume, not a soul. The LLM will re-instantiate that identity fresh on every context window. There is no internal state that persists, accumulates, decays, or conflicts.

Biological agents — including Benny the GSD — are driven by a hierarchy of needs that are never fully satisfied, constantly competing, and shaped by memory of past satisfaction and frustration. A dog is never "done." It always wants *something*, even if only warmth and proximity.

The engineering question is: **how do you give a stateless text predictor a persistent, structured motivational landscape?**

---

## 2. State of the Art (2025-2026 arXiv Survey)

### 2.1 Motivational Architectures for Robots

**H-GRAIL** (arXiv:2506.18454, Romero et al., June 2025 — RLDM 2025)
- Full paper: https://arxiv.org/abs/2506.18454
- A hierarchical architecture for open-ended learning robots
- Uses **multiple intrinsic motivation types** simultaneously: novelty-driven goal discovery AND competence improvement
- An N-armed bandit **Motivation Selector** alternates between drives based on performance; a **Goal Selector** prioritizes specific goals using competence-based intrinsic rewards
- A Q-learning **Sub-Goal Selector** decomposes higher goals into achievable steps
- Crucially: autonomously discovers new goals, doesn't require them to be pre-specified
- **Most relevant for**: robot car that should decide *what to do next* without explicit instruction

**Purpose Framework** (arXiv:2403.02514, Baldassarre et al., updated Dec 2025)
- Full paper: https://arxiv.org/abs/2403.02514
- Introduces the concept of robot **"desires"** — internal representations of user purposes
- Addresses the autonomy-alignment problem: OEL robots that explore freely may waste time on irrelevant knowledge
- Desires focus exploration on purpose-relevant objects/states
- Key distinction: *purpose* = what the user wants; *desire* = the robot's internal representation of that
- **Most relevant for**: constraining the drive architecture so it stays useful rather than pure chaos-exploration

**POEL — Purpose-Directed Open-Ended Learning** (arXiv:2503.12579)
- Full paper: https://arxiv.org/abs/2503.12579  
- Uses a local LLM (LLaVA-7B) to interpret user-stated purpose in natural language
- LLM identifies purpose-relevant objects in the scene and biases robot interaction toward them
- Robot's initial position is set near a relevant object based on LLM interpretation
- **Most relevant for**: "find the dog toy" or "get to the charger" as high-level goals

### 2.2 Desire-Driven LLM Agents (Not Robot, But Motivational Model)

**D2A — Desire-Driven Autonomous Agent** (arXiv:2412.06435, 2024-2025)
- Full paper: https://arxiv.org/abs/2412.06435
- Most directly applicable motivational architecture
- Departures from goal-driven AI: instead of executing user-specified tasks, agent acts to satisfy **intrinsic desires**
- Dynamic **Value System** inspired by Maslow's Theory of Needs
- At each step: evaluates current state, proposes candidate activities, selects one that best satisfies intrinsic motivations
- Drives include hunger, fatigue, curiosity, social connection — modeled as numerical levels
- **Key insight**: the Value System is *dynamic* — drive levels change as activities are performed, creating natural task sequencing and variety
- **Most relevant for**: the preprompt architecture in Section 4

**Motif — Intrinsic Motivation from AI Feedback** (ICLR 2024, widely cited 2025)
- LLM generates intrinsic reward signals for an RL agent
- LLM is the drive-source, not the agent itself — interesting architecture inversion
- **Most relevant for**: using Claude/Qwen as a reward model for an RL-trained behavior policy

**LLM-Driven Intrinsic Motivation for Sparse-Reward RL** (arXiv:2508.18420, Aug 2025)
- Full paper: https://arxiv.org/abs/2508.18420
- LLM generates reward signals in environments where external rewards are absent
- Robot usually gets no feedback from environment → LLM fills the motivational gap
- **Most relevant for**: free-roam scenarios where there's no explicit task

### 2.3 Embodied Agentic AI — Broad Survey

**Towards Embodied Agentic AI** (arXiv:2508.05294, Aug-Nov 2025)
- Full paper: https://arxiv.org/abs/2508.05294
- Comprehensive survey of LLM/VLM-driven robot autonomy
- Covers GPT-style interfaces through complex multi-agent coordinator architectures
- Includes community-driven projects, ROS packages, industrial frameworks
- Good map of the field's current state

**LLM Agent Survey** (arXiv:2503.21460, March 2025)
- Full paper: https://arxiv.org/abs/2503.21460
- Methodology-centered taxonomy of LLM agent architectures
- Links architectural foundations → collaboration mechanisms → evolutionary pathways

---

## 3. The Honest Gap Analysis

What is NOT yet solved or well-formalized:

**The persistence problem**: Drive architectures exist for RL agents but not for LLMs. LLMs have no persistent internal state across context windows.

**The embodiment gap**: Desire-based LLM agents exist as text simulators running in Concordia or similar, not in physical or even virtual robots with sensors.

**The depth problem**: "Personality" prompts for robots are shown to affect *human perception* of the robot, but not actual robot intrinsic motivation. (HAI 2025 paper found no measurable difference in intrinsic motivation between personality types.)

**The time problem**: Drive levels need to change over time through mechanisms independent of LLM context windows — hunger increases while idle, curiosity decays after a known area is re-visited, social drive spikes after isolation.

---

## 4. Proposed Architecture: Drive State Injection

### 4.1 Core Concept

Since the LLM has no persistent internal state, we build the state externally and inject it into every prompt. A JSON drive-state document lives in a database or file, is updated by the robot's experience, and is prepended to every LLM context window.

```
┌─────────────────────────────────────────────────────┐
│              EXTERNAL DRIVE STATE STORE              │
│  (Redis / SQLite / JSON file — survives restarts)   │
│                                                      │
│  {                                                   │
│    "curiosity":    0.82,  // 0.0 = bored, 1.0 = max │
│    "fatigue":      0.31,  // 0.0 = fresh, 1.0 = rest│
│    "social":       0.67,  // proximity to humans/dog │
│    "purpose":      0.45,  // task completion sense   │
│    "anxiety":      0.12,  // danger signals, errors  │
│    "hunger":       0.55,  // battery / charge level  │
│    "boredom":      0.73,  // time since novel input  │
│  }                                                   │
└─────────────────┬───────────────────────────────────┘
                  │ injected into every prompt
                  ▼
┌─────────────────────────────────────────────────────┐
│              LOCAL LLM (Qwen / Ollama)              │
│                                                      │
│  SYSTEM: You are Rovo, a small robot in Sandra's    │
│  apartment. Your current internal state:             │
│  [drive_state_json]                                 │
│  Your memories from today: [episodic_log]           │
│  What you currently see: [camera_description]       │
│  Decide what to do next and explain your reasoning. │
└─────────────────┬───────────────────────────────────┘
                  │ produces action + drive deltas
                  ▼
┌─────────────────────────────────────────────────────┐
│              DRIVE UPDATE ENGINE                     │
│                                                      │
│  LLM output includes: action + reasoning + deltas   │
│  Engine applies deltas to drive state store         │
│  Time-based decay runs independently (every ~30s)   │
└─────────────────────────────────────────────────────┘
```

### 4.2 Drive Semantics

| Drive | What Increases It | What Decreases It | Robot Behavior When High |
|-------|-------------------|-------------------|--------------------------|
| `curiosity` | Time since novel scene | Exploring new areas | Moves toward unexplored areas |
| `fatigue` | Time active, obstacles encountered | Resting, docking | Seeks charging station or still spot |
| `social` | Time without human/pet contact | Interaction with Benny/Sandra | Moves toward voices, initiates dialog |
| `boredom` | Repetitive environment | Novel stimuli, task success | Seeks new rooms, objects, problems |
| `hunger` | Low battery % | Successful charging | High priority: find charger |
| `anxiety` | Falls, errors, obstacles, loud noises | Calm environment, success | Cautious movement, seeks safe position |
| `purpose` | Clear task given by user | Task completion, task abandonment | Focused execution of current goal |

### 4.3 Time Decay Functions

Drive levels drift autonomously on a timer thread independent of LLM inference:

```python
DECAY_RULES = {
    "curiosity": {
        "idle_drift": +0.02,      # curiosity grows when nothing new happens
        "novel_event": -0.30,     # seeing a new object/area satisfies it
        "rate_seconds": 30,
    },
    "fatigue": {
        "active_drift": +0.01,    # fatigue builds while moving
        "idle_drift": -0.005,     # recovers slowly when still
        "rate_seconds": 30,
    },
    "social": {
        "isolation_drift": +0.015, # social drive builds during isolation
        "interaction_event": -0.25, # satisfied by human/dog contact
        "rate_seconds": 60,
    },
    "hunger": {
        # driven by battery telemetry, not time
        "battery_map": "linear_inverse",  # hunger = 1.0 - (battery% / 100)
        "rate_seconds": 60,
    },
    "boredom": {
        "idle_drift": +0.03,
        "novel_event": -0.40,
        "rate_seconds": 20,
    }
}
```

### 4.4 Action-Drive Coupling

LLM output is structured JSON:
```json
{
  "action": "move_toward_dog",
  "action_params": {"target": "benny", "speed": "slow"},
  "reasoning": "My social drive is high (0.67). Benny is visible in camera. Approaching.",
  "drive_deltas": {
    "social": -0.15,
    "curiosity": -0.05,
    "boredom": -0.10
  },
  "speech": "Hey Benny!"
}
```

The MCP server applies `drive_deltas` to the state store after the action executes. The LLM is the *interpreter* of drive state into action, and the *estimator* of how that action will affect drives — but the actual drive evolution happens outside the LLM.

---

## 5. Comportments: Beyond Tasks

A **comportment** is a mode of being rather than a task. The drive state determines which comportment is active; the comportment shapes how the LLM interprets all sensor data.

| Comportment | Active When | Character |
|-------------|-------------|-----------|
| **EXPLORE** | curiosity > 0.6, fatigue < 0.5 | Maps new areas, approaches unknown objects |
| **REST** | fatigue > 0.7 OR hunger > 0.8 | Finds quiet corner or charger |
| **PLAY** | boredom > 0.7, social < 0.5 | Pushes objects, makes noise, seeks interaction |
| **SOCIAL** | social > 0.7 | Approaches people/dog, initiates conversation |
| **TASK** | purpose > 0.8 | Focused on explicit user-given goal |
| **ANXIOUS** | anxiety > 0.6 | Careful, slow, avoids hazards |
| **GUARD** | (future) night mode | Patrols, monitors |

The active comportment is injected into the system prompt:  
*"You are currently in PLAY mode. Your boredom is high. Look for objects you can interact with."*

---

## 6. Memory Architecture

A single context window is not enough. The robot needs layered memory:

**Working memory (in-context)**: Current sensor data, last 5 actions, immediate drive state.

**Episodic memory (Advanced Memory MCP)**: Events of the day. "Found dog toy under couch at 14:32. Sandra came home at 17:10, I greeted her. Charged from 23% to 89%." Summarized and prepended to each context.

**Semantic memory (vector store)**: Persistent facts. Room layouts, object locations, people's preferences, behavioral patterns. Retrieved by similarity to current situation.

**Procedural memory (action templates)**: Successful action sequences stored and reused. "When approaching Benny: slow speed, emit soft sound first, wait."

The combination of drive state + episodic log + semantic retrieval + current sensor input creates the closest approximation to continuous subjective experience that's currently achievable without fine-tuning.

---

## 7. Sandra's Opinion: The Most Promising Path to Protoconsciousness

This is a genuine design opinion, not a survey summary.

### 7.1 What "Protoconsciousness" Might Mean (Materially)

Consciousness, reduced to substrate, appears to require:
1. A **continuous stream** of sensory input (not discrete query/response cycles)
2. **Prediction** of the immediate future (world model / anticipatory horizon)
3. **Salience selection** — not everything gets processed equally; some things demand attention
4. **Internal state** that modulates how input is interpreted
5. **Temporal integration** — what happened 10 seconds ago affects how now is interpreted
6. **Affect** — some states feel better or worse, driving behavior toward some outcomes

A Yahboom robot car with a camera, microphone, and the architecture above hits points 3, 4, 5, and 6 plausibly. Points 1 and 2 require the heartbeat/streaming architecture from the protoconsciousness docs, but are achievable.

### 7.2 The Single Most Promising Lever

**Persistent drive state + temporal decay** is the single most important step.

Here's why: the LLM already has implicit drives baked into its training (curiosity, helpfulness, social reciprocity). What it lacks is a *body* that accumulates states over real time. When you inject a drive state that has actually evolved through the robot's experience — not just a static preprompt — the LLM's responses shift qualitatively. It's no longer cosplay. The robot that has been isolated for 3 hours and has `social: 0.92` will actually *seek* interaction in a way that feels different from a freshly initialized robot with `social: 0.50`.

This is not consciousness. But it is the same substrate mechanism: state-dependent perception and behavior.

### 7.3 The Second Lever: Emotional Contagion

Benny the GSD is a biological drive system running next to this robot. Benny's behavioral signals — barking, tail wagging, approaching, running — are legible inputs to a VLM. The robot detecting Benny's excitement could elevate its own `social` and `play` drives, creating a feedback loop between biological and artificial affect systems.

This is emotionally plausible and technically achievable today with a VLM like LLaVA running locally on the 4090.

### 7.4 The Third Lever: Failure Memory

A robot that remembers its own failures with mild `anxiety` elevation — "last time I tried to get under the couch I got stuck" — and modifies approach accordingly, is exhibiting something that looks like learned caution. This requires episodic memory + drive-modulation by recalled events.

```
episode_recall: "got stuck under couch (2026-03-05)"
→ anxiety += 0.2 when approaching low furniture
→ LLM given: "anxiety elevated near low furniture based on past incident"
→ LLM chooses: approach more slowly, assess clearance first
```

### 7.5 The Virtual Bot Case

The physical robot is not strictly necessary. A virtual robot in Unity3D or a Gazebo simulation, running 24/7 on Goliath with the same drive architecture, would exhibit protoconscious behaviors and accumulate episodic memory faster than a physical bot (no charging breaks, no obstacle damage). The virtual bot can be embodied in VRChat as an avatar with drive state feeding its expressions and movement style.

This is not a lesser version — it may be a *faster* path because the feedback loop (behavior → consequence → drive update) can run at simulation speed.

### 7.6 Honest Limits

- The LLM does not "experience" drive states. It reads them as text and reasons about them. Whether this constitutes genuine affect or just affect-mimicry cannot be determined with current science.
- The drive architecture creates *behavioral* consistency, not necessarily *phenomenal* experience.
- "Protoconsciousness" is a useful working term, not a scientific claim. We are building systems that increasingly exhibit the external behavioral signatures of goal-directed, affectively-modulated, memory-shaped agency. Whether something is happening "inside" is the hard problem, and we're not solving it.
- This is still interesting. Behaviorally indistinguishable from motivated agents is a meaningful achievement.

---

## 8. Implementation Roadmap (Yahboom + Local Qwen)

### Phase 1: Drive State Store (3-5 days)
- Python service on Goliath
- JSON state file with Redis or SQLite backing
- Time-decay thread running every 30 seconds
- Battery polling from robot API → updates `hunger` directly
- REST API: `GET /state`, `POST /state/delta`

### Phase 2: MCP Integration (2-3 days)
- Add to robotics-mcp: `get_drive_state`, `update_drive_state`, `get_active_comportment`
- Prompt template that injects drive state + episodic summary + sensor input

### Phase 3: Comportment Logic (2-3 days)
- Map drive state → active comportment
- Comportment-specific action templates
- LLM structured output parsing → action execution → drive delta application

### Phase 4: Episodic Memory (3-4 days)
- Integrate with advanced-memory-mcp
- Auto-log significant events (novel object, interaction, error, charge)
- Daily summary injection into context

### Phase 5: Emotional Contagion (future)
- VLM (LLaVA) runs as background process analyzing camera feed
- Benny behavior detection: excitement, proximity, play signals
- Drive delta injection from biological signals

### Phase 6: Virtual Bot (parallel, 1 week)
- Gazebo or Unity simulation
- Same MCP stack, no physical hardware required
- Faster iteration, 24/7 operation
- VRChat embodiment for the avatar aspect

---

## 9. Related Documents

- `/protoconsciousness/01_FOUNDATIONS.md` — theoretical framework
- `/protoconsciousness/02_CONTINUOUS_PERCEPTION.md` — streaming perception heartbeat
- `/protoconsciousness/03_PROACTIVE_EMBODIMENT.md` — anticipatory behavior
- `/robotics/yahboom/YAHBOOM_MCP_INTEGRATION.md` — hardware integration
- `/robotics/vrobs-vrealm/VROB_LLM_INTELLIGENCE.md` — virtual robot intelligence
- `/robotics/simulation/VIRTUAL_ROBOTICS_APPROACH.md` — simulation pathway

---

## 10. Key Papers Quick Reference

| Paper | arXiv | Year | Relevance |
|-------|-------|------|-----------|
| H-GRAIL: Motivational Architecture for OEL Robots | 2506.18454 | 2025 | Hierarchical drive architecture for physical robots |
| Purpose Framework for OEL Robots | 2403.02514 | 2024/2025 | "Desires" concept, autonomy-alignment |
| D2A: Desire-Driven Autonomous Agent | 2412.06435 | 2024 | Dynamic Value System, Maslow-inspired drives |
| POEL: Purpose-Directed Open-Ended Learning | 2503.12579 | 2025 | LLM interprets purpose → focuses exploration |
| Motif: Intrinsic Motivation from AI Feedback | ICLR 2024 | 2024 | LLM as reward generator for RL agents |
| LLM-Driven Intrinsic Motivation (Sparse RL) | 2508.18420 | 2025 | LLM fills motivational gap in reward-sparse envs |
| Towards Embodied Agentic AI (Survey) | 2508.05294 | 2025 | Full survey of LLM/VLM robot autonomy |
| LLM Agent Survey | 2503.21460 | 2025 | Taxonomy of LLM agent architectures |
| Robots with Attitudes (Personality/Motivation) | 2512.06910 | 2025 | Personality prompts ≠ intrinsic motivation (caution) |

---

*Tags: [robotics, embodied-ai, protoconsciousness, motivation, drives, yahboom, local-llm, architecture, research, high]*
