# ADN-002: Self-Hosted Forgejo VCS & CI Integration

*   **Status**: Proposed
*   **Deciders**: Sandra Schimanovich, LLM Agent
*   **Date**: 2026-07-20

---

## 1. Context and Problem Statement

Our model-driven development fleet needs a self-hosted, lightweight Version Control System (VCS) and CI/CD platform to mirror codebases, trigger local tests, and manage repositories offline. 

While GitHub or GitLab are standard, they introduce internet latency, API rate limits, and external hosting security concerns for private local models. We need a FOSS alternative that runs locally within a single container.

---

## 2. Decision

We chose to integrate **Forgejo** (a community-driven, soft-fork of Gitea focused on privacy and scaling) as our primary local VCS and CI engine:

1.  **Repository Management**: We will design a `forgejo-mcp` server that wraps Forgejo’s REST API (v1) to programmatically create repositories, configure webhooks, and manage SSH deploy keys.
2.  **Forgejo Actions (CI/CD)**: Forgejo utilizes `runner` (based on Gitea Action's `act` runner) which is fully compatible with GitHub Actions workflows (`.github/workflows/`).
3.  **Local Webhooks**: The `forgejo-mcp` server will listen for git-push webhooks, allowing LLM agents to automatically trigger tests or trigger audits upon commit.

---

## 3. Consequences

*   **Offline Development**: Entire code creation, repository committing, and testing runs locally on the host machine without external network requirements.
*   **Zero-latency Webhooks**: Push actions trigger immediate local runs.
*   **Compatability**: Workflows written for Forgejo Actions can be pushed to GitHub Actions without changing YAML schemas.
