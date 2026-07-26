# DeltaDB — Keystroke-Level Version Control for Agentic Workflows
**Status:** Waitlist Requested (July 13, 2026)
**Category:** Version Control / CRDT / Agentic Worktrees
**Developer:** Zed Industries (Creators of the Zed Editor)
**Link:** [zed.dev/deltadb](https://zed.dev/deltadb)

---

## 💡 1. The Core Thesis: "Software is Made Between Commits"
Traditional version control (Git) is built on periodic, discrete snapshotting (commits). While this works for human-to-human asynchronous merging, it fails for AI-native codebases because:
1. **Loss of Context**: Git commits do not capture the conversational prompts, agent logs, or intermediate failures that led to a specific diff.
2. **Keystroke/Delta Level**: DeltaDB captures every keypress and operational edit in real-time, preserving the exact line history and stable identities of code blocks.
3. **CRDT Foundation**: Built on Conflict-free Replicated Data Types (CRDTs), enabling seamless collaborative multi-user/multi-agent editing without merge conflicts.

---

## 🛠️ 2. Core Features & Capabilities

* **Operation-Level History**: Instead of a history of file diffs, DeltaDB maintains a history of edits (deltas). You can trace a specific line of code directly back to the agent conversation or developer pairing session that produced it.
* **Virtual Worktrees**: Developers and AI agents can branch, test, and merge in real-time virtual worktrees without waiting for formal commit-and-push cycles.
* **LLM Rationale Binding**: Out-of-the-box support for tying code changes to LLM session logs, addressing the "RAG-Stack" information loss.

---

## 🔄 3. Integration Plan for the MCP Fleet
Once early access is granted, DeltaDB can be integrated into the fleet to solve several critical pain points:

| Scenario | Git Limitation | DeltaDB Advantage |
|----------|----------------|-------------------|
| **Multi-Agent Code Runs** | Agents lock the workspace or collide on the same files. | CRDTs allow parallel agents to execute edits concurrently. |
| **Agent Fix Cycles** | Commit histories get cluttered with "fix lints" or "test run" garbage commits. | Operation-level history filters out transient edits, keeping only semantic changes. |
| **RAG Long-Term Memory** | Agents must read whole files or diffs to understand history. | Agents can query DeltaDB for the *exact conversation* that modified a code block. |

---

## 📋 4. Next Steps & Tracking
* [x] Create research stub in MCD.
* [/] **Action Required (Sandra)**: Click [zed.dev/deltadb](https://zed.dev/deltadb) to join the early access waitlist with your developer credentials.
* [ ] Integrate DeltaDB daemon hooks once the private beta/CLI is available.
