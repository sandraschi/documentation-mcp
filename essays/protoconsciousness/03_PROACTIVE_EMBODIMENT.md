# 03. Proactive Embodiment & Anticipatory Intelligence

**Last Updated:** February 2026

When an LLM is fed a continuous temporal stream ([02_CONTINUOUS_PERCEPTION.md](02_CONTINUOUS_PERCEPTION.md)), its operational paradigm shifts. It stops being a reactive question-answer engine and becomes an **embodied observer**. 

But observation alone is not protoconsciousness. The next architectural pillar is **Proactive Anticipation**. The agent must build a World Model and act upon it before being explicitly prompted.

## Anticipatory Intelligence

A stateless oracle only speaks when spoken to. A protoconscious agent speaks when the environmental state dictates that it *should* speak. 

**Recent Lit on Proactive Agents:**

### 1. Eyes Wide Open (Ego-Proactive Video-LLMs)
This research focuses on egocentric video (e.g., streaming from a wearable camera or a robot's front-facing sensor). The goal is for the AI to understand, anticipate, and formulate a response to unfolding events *before* the user prompts it. This requires:
- **Proactive Coherence:** Maintaining long-term context of what the user is doing.
- **Just-in-Time Responsiveness:** Firing the output at the exact optimal moment.

### 2. ContextAgent
*ContextAgent* incorporates constant multimodal sensory context to predict the necessity of proactive services. If the robot hears a glass shatter in the kitchen, it shouldn't wait for the human to type "What was that noise?". Its continuous perception tracker registers the anomaly, forwards the audio/video context to the reasoning heavy-LLM, and the LLM proactively outputs: *"I detected a breaking sound in the kitchen. Should I navigate there to assess?"*

### 3. StreamAgent & Predictive Spatiotemporal Tracking
*StreamAgent* takes anticipation a step further. It actively predicts the temporal intervals and spatial regions that will contain future task-relevant information. It is not just watching the video; it is predicting *where to look next* and updating its goal-state autonomously based on what it finds.

---

## Fusing LLMs with World Models

LLMs are excellent at semantic planning and logical reasoning, but historically, they have no intuition for real-world physics (gravity, momentum, spatial persistence). 

To achieve true embodied protoconsciousness in our physical robotic platforms (e.g., Unitree Go2/G1, Moorebot Scout), we must architect a fusion:

1. **Semantic Engine (LLM):** Handles high-level goal decomposition ("Find the user and deliver this message").
2. **World Model (WM):** A physics-grounded simulator (often running locally in ROS or a lightweight Unity/Omniverse headless instance). The WM predicts the physical consequences of the semantic plans.

By locking the LLM into a tight loop with a grounded World Model, the agent can simulate its actions internally *before* executing them externally—a hallmark of conscious planning.
