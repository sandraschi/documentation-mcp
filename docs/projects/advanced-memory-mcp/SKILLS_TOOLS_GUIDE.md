# Advanced Memory MCP: Skills Tools Guide

**Comprehensive guide for utilizing the `adn_skills` toolset within `advanced-memory-mcp` across different Agentic IDEs.**

## 🎯 Overview

The `advanced-memory-mcp` server provides a sophisticated **Skill System** that goes beyond simple instruction sets. The `adn_skills` tool allows agents to manage, discover, and even *create* new specialized capabilities dynamically.

---

## 🛠️ The `adn_skills` Tool

The `adn_skills` tool is the primary interface for managing skills in the knowledge graph.

### Core Operations

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `create` | Define a new skill | `name`, `content`, `tags` |
| `read` | Retrieve skill details | `name` |
| `list` | List all available skills | - |
| `update` | Update existing skill | `name`, `content`, `tags` |
| `delete` | Remove a skill | `name` |
| `search` | Find skills by query | `query` |
| `creator` | AI-assisted skill generation | `content` (description of needed skill) |
| `advanced_create`| Create skill with complex params | `name`, `parameters` |

### The "Creator" Pattern
One of the most powerful features is `adn_skills("creator", content="...")`. This allows an agent (or user) to describe a desired capability, and the memory server will generate a structured `SKILL.md` compliant with Anthropic standards.

---

## 🎨 IDE Integration Patterns

### 1. Antigravity (Native)
Antigravity has the deepest integration with `advanced-memory-mcp`.

- **Native Tooling**: Agents in Antigravity can invoke `adn_skills` directly to load context for complex tasks.
- **Automated Discovery**: When a task is initiated, Antigravity queries `adn_skills("search", ...)` to find relevant specialized instructions.
- **Workflow Mapping**: Skills can be mapped directly to `.agents/` workflows for seamless execution.

### 2. Cursor & Windsurf (Project-Level)
Since Cursor and Windsurf look for skills in specific directories (`.cursor/skills/`, `.windsurf/skills/`), `adn_skills` serves as a **Skill Manager**.

- **Synchronization**: You can use `adn_skills` to "export" a skill from your central knowledge graph into your project's local directory.
- **Global Library**: Maintain a master library of skills in Advanced Memory and pull them into specific projects as needed.

### 3. Zed (Contextual Reference)
In Zed, where MCP tools are accessed via the assistant panel:

- **Library Exploration**: Use `adn_skills("list")` to see available capabilities.
- **Injection**: Read a skill via `adn_skills("read", name="...")` and prompt the assistant to "Apply the instructions from this skill to the current project."

---

## 🚀 Example Workflows

### Case A: Generating a New Capability
1. **User**: "I need to start doing security audits on our Python code."
2. **Agent**: Calls `adn_skills("creator", content="Expert Python security auditor following OWASP standards")`.
3. **Advanced Memory**: Generates a `SKILL.md` with audit checklists and Playwright recon patterns.
4. **Agent**: Calls `adn_skills("create", name="python-security", content=generated_content)`.

### Case B: Project Onboarding
1. **Agent**: Opens a new React project in Cursor.
2. **Agent**: Queries Advanced Memory: `adn_skills("search", query="React clean architecture")`.
3. **Agent**: Finds the "React Architect" skill and suggests: "I see you have a specialized React skill in your memory. Should I export it to `.cursor/skills/` for this project?"

---

**Last Updated**: 2026-01-27
**Status**: January 2026 SOTA Protocol
