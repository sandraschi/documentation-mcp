# Agent Client Protocol (ACP) Standard (SOTA v12.2)

## 1. Overview

The **Agent Client Protocol (ACP)** is an open standard created by Zed Industries (released in August 2025) and subsequently integrated by Apple into **Xcode 27 Beta**.

Much like the Language Server Protocol (LSP) standardized how code editors communicate with compiler/language intelligence engines, **ACP standardizes the interface between a development environment (IDE/Editor) and an AI Coding Agent** (such as Claude Code, Gemini CLI, OpenCode, or custom orchestrators).

---

## 2. Core Differences: ACP vs. MCP

It is critical not to confuse **ACP** (Agent Client Protocol) and **MCP** (Model Context Protocol). They operate at different layers of the SOTA AI engineering stack:

```
┌─────────────────────────────────┐
│        Editor / IDE             │  (e.g., Xcode 27, Zed, Cursor)
└────────────────┬────────────────┘
                 │
                 │  ◄── ACP (Agent Client Protocol)
                 ▼
┌─────────────────────────────────┐
│        AI Coding Agent          │  (e.g., Claude Code, Custom Agent CLI)
└────────────────┬────────────────┘
                 │
                 │  ◄── MCP (Model Context Protocol)
                 ▼
┌─────────────────────────────────┐
│        MCP Server / Tools       │  (e.g., immich-mcp, calibre-mcp, git-mcp)
└─────────────────────────────────┘
```

*   **ACP (Editor ↔ Agent)**: Standardizes how the IDE hosts the agent. It manages chat panel UI, file buffers, project diagnostics, and user approval workflows.
*   **MCP (Agent ↔ Capabilities)**: Standardizes how the agent accesses tools, resources, and contextual data (such as external databases, API wrappers, or local system command utilities).

---

## 3. Repository Classification: Who Uses What?

### A. Who should implement ACP? (The Agent Repositories)
An ACP implementation is required for **Agent Repositories**—runtimes whose primary job is acting as an autonomous executor/co-pilot.
*   **Examples**: Claude Code, Gemini CLI, customized engineering loops, autonomous refactoring bots.
*   If you are building an AI tool that runs commands, edits files, and interacts directly with the user inside an editor panel, you should implement the **ACP standard** so your tool can be plugged into Zed's ACP registry or configured as a Custom Agent in Xcode 27.

### B. Who should implement MCP? (The Tool Repositories)
MCP is used by **Integration / Capability Repositories**—servers whose primary job is wrapping APIs, databases, or local workflows into tools for an LLM to call.
*   **Examples**: `immich-mcp`, `calibre-mcp`, `gimp-mcp`, database-operations.
*   These repositories do **not** need ACP. By remaining MCP servers, they are automatically compatible with *any* ACP-native agent that connects to them.
