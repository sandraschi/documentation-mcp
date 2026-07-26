# FastMCP Skills & Prompts: Expert Guidance

**Last Updated:** 2026-04-22
**Standard:** FastMCP 3.4.2 (originally written for 3.2.0 — prompts/skills API unchanged)

FastMCP 3.2 provides standardized mechanisms for delivering **Expert Guidance** to AI agents. By decoupling instructions from the client, we ensure consistent behavior across Claude Desktop, Cursor, and custom orchestrators.

---

## 1. Prompts: Dynamic Templates

Prompts are parameterized message templates registered on the server. They provide "System Instructions" or "Task Blueprints" on demand.

### Implementation
```python
@mcp.prompt()
def database_expert(focus: str = "general") -> str:
    """Load instructions for acting as a database expert."""
    base = "You are a DB expert. Use db_connection to begin."
    if focus == "audit":
        return base + "\n\nAnalyze schemas for injection vulnerabilities."
    return base
```

### Why use Prompts?
- **Consistency**: One source of truth for "How to use this server."
- **Parameterization**: Dynamically tailor instructions based on the current task.
- **Client Agnostic**: Any MCP-capable client can call and inject these prompts.

---

## 2. Skills: Portable Expertise

**Skills** are directories containing expert instructions (`SKILL.md`) and supporting resources. FastMCP exposes these via the `skill://` resource scheme.

### Client-side agent skills (Huashu Design, Cursor, Codex, …)

Some ecosystems use the same “skill” name for **instructions installed in the agent client** (for example under `%USERPROFILE%\.agents\skills\` on Windows after `npx skills add …`). Those are **not** MCP resources; they do not traverse `resources/list` from your server. Fleet documentation for a third-party example: [integrations/huashu-design-skill.md](../integrations/huashu-design-skill.md).

### The Skill Structure
```
skills/
└── coding-standard/
    ├── SKILL.md       # Primary instructions
    └── boilerplate.py # Reference code
```

### Exposing Skills
Use the `SkillsDirectoryProvider` to bundle and expose skills from your server package.

```python
from fastmcp.providers import SkillsDirectoryProvider

mcp.add_provider(
    SkillsDirectoryProvider(roots=["./skills"])
)
```
*Creates: `skill://coding-standard/SKILL.md`.*

---

## 3. Prompts vs. Skills: Choosing the Pattern

| Pattern | Data Type | Usage |
|---|---|---|
| **Prompt** | `Message` | Immediate context injection (e.g., "Act as a specialist"). |
| **Skill** | `Resource` | Long-form reference, checklists, and portable repositories. |

---

## 4. Discovery in 3.2

In FastMCP 3.2, prompts and skills are fully discoverable via the standard MCP `prompts/list` and `resources/list` methods. 
- **High-Fidelity RAG**: Ensure your skill `SKILL.md` and prompt docstrings follow the **3-4-100** rule for optimal discovery.

---

## References
- [tool-documentation.md](./tool-documentation.md)
- [fastmcp-32-fleet-capability-map.md](./fastmcp-32-fleet-capability-map.md)
- [agentic-sampling.md](./agentic-sampling.md)
