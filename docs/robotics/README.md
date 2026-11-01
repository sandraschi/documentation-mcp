# Robotics Integration Documentation (RE-DIRECTED)

> [!IMPORTANT]
> **Technical Source of Truth (TSOT) Discovered:**
> As of April 2026 (SOTA v16.16), all core robotics technical documentation, hardware guides, and operational protocols have been migrated to the **[robotics-mcp](file:///D:/Dev/repos/robotics-mcp/README.md)** repository.

## 🏛️ The New World Order: Android Doctrine
The canonical strategic documentation now resides in:
- **[Android Doctrine Master Index](file:///D:/Dev/repos/robotics-mcp/docs/android-doctrine/ANDROID_DOCTRINE_INDEX.md)**: Vision, Governance, Manipulation, and Public Acceptance.

## 📂 Local Directory Status
The folders in this repository are now categorized as follows:

| Directory | Status | Purpose |
| :--- | :--- | :--- |
| **`docs/agentic chats/`** | **ACTIVE** | Archive of architectural and philosophical AI/LLM sessions. |
| **`research/`** | **ACTIVE** | Research and third-party adoption assessments (Embodied AI, Ethics, VLA, skill discovery). |
| **`hardware/`** | **ACTIVE** | Fleet notes on sourcing (e.g. [Shenzhen humanoid actuators](./hardware/SHENZHEN_HUMANOID_ACTUATORS.md)). |
| **`_archive/`** | **ARCHIVED** | Legacy Dec 2025/Early 2026 content (Moorebot Scout, ROS 1.4, old VROBs). |

### Adoption assessments (research/)

Adopt-or-borrow calls on third-party robotics work. Each ends with a recommendation and a reopen trigger, so a later session does not re-litigate it from memory.

| Date | Doc | Verdict |
| :--- | :--- | :--- |
| 2026-09-09 | [RoboSPA VLA benchmark](./research/2026-09-09_robospa-vla-assessment.md) | Borrow the taxonomy and eval interface; do not run the pi0.5 pipeline on one 4090 |
| 2026-10-21 | [ASPIRE skill discovery](./research/2026-10-21_aspire-skill-discovery-probe.md) | Borrow the contract layer and task-recipe format; add 3 primitives to `mujoco-mcp`; no new repo yet |

## 🕹️ Fleet Control Centers
For real-time control and dashboarding, refer to the individual MCP project hubs:
- **[yahboom-mcp](file:///D:/Dev/repos/yahboom-mcp)**: Home of the Raspbot V2 (Boomy). Operator starter: **[docs/robotics/yahboom/STARTUP_AND_BRINGUP.md](../docs/robotics/yahboom/STARTUP_AND_BRINGUP.md)** (also in repo `yahboom-mcp/docs/ops/STARTUP_AND_BRINGUP.md`).
- **[bumi-mcp](file:///D:/Dev/repos/bumi-mcp)**: Home of the Noetix Android (T80).

---
*Last Updated: 2026-10-21*
*Status: Synchronized with SOTA v16.16*
