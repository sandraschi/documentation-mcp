# Agentic IDE Integration Guide

**How to integrate Claude Skills into modern Agentic IDEs following Anthropic patterns.**

## 🎯 Overview

Agentic IDEs leverage "Skills" as high-context instruction sets that guide their autonomous behavior. By following the **Anthropic Skills Pattern**, you can create portable, powerful capabilities that work across multiple environments.

### The Anthropic Skills Pattern (SOTA 2026)

A skill is defined by a structured directory:
- `SKILL.md`: Core instructions with YAML frontmatter.
- `scripts/`: Implementation scripts (Python, JS, etc.).
- `examples/`: Reference implementations.
- `resources/`: Static data or assets.

---

## 🎨 IDE-Specific Integration

### 1. Cursor
Cursor uses `.cursor/skills/` for local project-specific skills.

- **Storage**: Place skill folders in `.cursor/skills/`.
- **Engagement**: Reference skills in your `.cursorrules` or project index.
- **Auto-Discovery**: Cursor Indexing (Cmd+Shift+J) automatically processes these for context.

**Example Structure**:
```
.cursor/
  ├── skills/
  │   └── react-expert/
  │       └── SKILL.md
  └── .cursorrules
```

### 2. Windsurf
Windsurf integrates skills similarly to Cursor but with a focus on global vs. project scope.

- **Storage**: `.windsurf/skills/`.
- **Rules**: Can be enforced via `.windsurf/rules/`.
- **Flow**: Skills are considered during "Flow" state for autonomous reasoning.

### 3. Antigravity
Antigravity provides the most robust integration via the `adn_skills` tool.

- **Storage**: Managed via `adn_skills` tool or stored in `.agents/skills/`.
- **Usage**:
  - `adn_skills("read", name="skill-name")`
  - `adn_skills("list")`
- **Automation**: Skills are automatically prioritized based on task metadata and `@agents` configuration.

### 4. Zed
Zed currently leverages skills through custom prompt configuration and file referencing.

- **Integration**: Add your skill library path to Zed's project configuration.
- **Prompting**: Reference `SKILL.md` files in the prompt context to ground the model in specific domain instructions.

---

## 🛠️ Creating an "Agent-Ready" Skill

To ensure your skill works perfectly in an Agentic IDE, follow these SOTA standards:

1. **Specific YAML**: Use the `usage-triggers` metadata field.
   ```yaml
   ---
   name: api-architect
   description: Expert REST/GraphQL API design
   metadata:
     usage-triggers: "api, swagger, graphql, endpoint design"
   ---
   ```
2. **Actionable Instructions**: Avoid passive voice. Use "Always check...", "Prefer...", "Execute...".
3. **Tool Awareness**: Explicitly list compatible tools in the `allowed-tools` frontmatter (standardized in January 2026).

---

## 🚀 Deployment Checklist

- [ ] Folder name matches `name` in `SKILL.md` (kebab-case).
- [ ] `SKILL.md` includes comprehensive YAML frontmatter.
- [ ] Scripts are documented in the `SKILL.md` with usage examples.
- [ ] Skill has been tested for "Agentic Drift" (ensuring the model stays within boundaries).

---

**Last Updated**: 2026-01-27
**Status**: January 2026 SOTA Protocol
