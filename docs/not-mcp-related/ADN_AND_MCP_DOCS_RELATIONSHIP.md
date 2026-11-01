# ADN and MCP Central Docs - Relationship Guide

**Last Updated:** 2025-12-03  
**Status:** CURRENT

---

## Overview

Advanced Memory (ADN) and MCP Central Docs serve **complementary roles** in the documentation ecosystem. Understanding when to use each maximizes efficiency.

---

## The Relationship

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚           ADN (Advanced Memory)                  â”‚
â”‚           "The Smart Scratchpad"                 â”‚
â”‚                                                  â”‚
â”‚  âœ… Automatic [[Entity]] linking                â”‚
â”‚  âœ… Semantic search & tagging                   â”‚
â”‚  âœ… Daily work, brainstorming                   â”‚
â”‚  âœ… Quick LLM interactions                      â”‚
â”‚  âœ… Knowledge graph                             â”‚
â”‚  âœ… Import/export (Obsidian, Joplin, etc.)     â”‚
â”‚                                                  â”‚
â”‚  Use: Personal knowledge base, working notes    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                  â”‚
                  â”‚ Polish & extract
                  â”‚ "Final answer" patterns
                  â”‚
                  â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         MCP Central Docs                         â”‚
â”‚         "The Reliable Reference"                 â”‚
â”‚                                                  â”‚
â”‚  âœ… Old school markdown                         â”‚
â”‚  âœ… Git-versioned history                       â”‚
â”‚  âœ… Manual [links](path.md)                     â”‚
â”‚  âœ… Zip & email to new hires!                   â”‚
â”‚  âœ… No dependencies                             â”‚
â”‚  âœ… Works everywhere                            â”‚
â”‚                                                  â”‚
â”‚  Use: Onboarding, reference, distribution       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

## When to Use ADN

### âœ… Perfect for ADN

**Daily Work:**
- "Today's progress on vienna-life-assistant"
- "Brainstorm: MCP dual interface implementation"
- "Quick note: FastMCP 3.1.1+ changed X"
- "Meeting notes with Bob about feature Y"

**Brainstorming:**
- Connecting ideas across projects
- Research notes
- "What if we..." explorations
- Linking related concepts

**Private Content:**
- Personal observations
- Draft ideas not ready for public
- LLM interaction transcripts
- Work-in-progress thinking

**Complex Queries:**
```bash
# Find all notes about FastMCP from last month
adn_search("FastMCP", after_date="1 month")

# Find notes tagged with mcp AND docker
adn_search("query", tags=["mcp", "docker"])

# Semantic search
adn_search("how to optimize docker builds")
```

**Auto-Linking:**
```markdown
Working on [[Vienna Life Assistant]] using [[FastMCP]] and [[Docker]].
Need to integrate [[Plex MCP]] and [[Calibre MCP]].

# ADN automatically creates links and relationships!
```

---

## When to Use MCP Central Docs

### âœ… Perfect for MCP Central Docs

**Polished References:**
- "FastMCP 3.1.1++ Migration Guide"
- "Docker Build Optimization Standards"
- "MCP Transport Methods (Official)"
- "Git Worktrees Tutorial"

**Distribution:**
```powershell
# Package for new hire
Compress-Archive -Path "mcp-central-docs\docs" `
                 -DestinationPath "mcp-reference-2025-12.zip"

# Email: "Here's our complete MCP reference!"
# They unzip and have everything
# No setup, no ADN, just markdown
```

**Onboarding:**
- New developer reads through systematically
- No ADN knowledge graph needed
- Works offline
- Universal (any editor, GitHub, etc.)

**Stable Standards:**
- "This is how we do portmanteau tools"
- "This is our Docker strategy"
- "These are our Git standards"
- Won't change unless intentional

---

## Feature Comparison

| Feature | ADN | MCP Central Docs |
|---------|-----|------------------|
| **Auto-linking** | âœ… `[[Entity]]` automatic | âš ï¸ Manual `[link](path.md)` |
| **Semantic search** | âœ… AI-powered | âŒ grep only |
| **Tagging** | âœ… Dynamic, flexible | âš ï¸ Frontmatter only |
| **Knowledge graph** | âœ… Automatic | âŒ Manual |
| **Import/export** | âœ… Obsidian, Joplin, etc. | âš ï¸ Git only |
| **Daily notes** | âœ… Built-in | âŒ Not designed for this |
| **Version control** | âš ï¸ File-based | âœ… Git history |
| **Portability** | âš ï¸ Needs ADN | âœ… Just markdown |
| **Onboarding** | âš ï¸ Requires setup | âœ… Unzip and read |
| **Collaboration** | âš ï¸ Sync needed | âœ… Git push/pull |
| **Stability** | âš ï¸ Living, evolving | âœ… Intentionally static |

---

## The Flow: ADN â†’ MCP Central Docs

### Example 1: Feature Development

**Day 1 (ADN):**
```markdown
# 2025-12-03 - Vienna Life Assistant MCP Integration

Quick notes:
- Need [[HTTP transport]] for [[Docker]] containers
- [[MCP Studio]] uses [[stdio transport]] pattern
- Found issue: was using HTTP incorrectly
- Correct: spawn process via stdio

Related: [[FastMCP 3.1.1+]], [[Vienna Life Assistant]]
```

**Day 7 (Polish â†’ MCP Central Docs):**
```markdown
# MCP Transport Methods

**Last Updated:** 2025-12-03

## Stdio Transport
[Polished guide with examples...]

## HTTP Transport
[Clear explanation of valid use cases...]
```

### Example 2: Docker Optimization

**Week 1 (ADN):**
```markdown
# Docker Build Times - Too Slow!

Testing different approaches:
- Try 1: --no-cache every time â†’ 5 minutes (too slow!)
- Try 2: Layer caching â†’ 10 seconds! âœ…
- Try 3: Multi-stage build â†’ Even better!

Notes:
- Copy requirements.txt BEFORE code
- System deps rarely change
- Code changes most frequently

Related: [[Docker]], [[Vienna Life Assistant]], [[Build Optimization]]
```

**Week 2 (Polish â†’ MCP Central Docs):**
```markdown
# Docker Build Optimization

**Last Updated:** 2025-12-03

## Smart Layer Caching

Order layers from least to most frequently changing:
1. System packages
2. Requirements file
3. Install packages
4. Source code

[Polished guide with benchmarks...]
```

---

## Hybrid Frontmatter Strategy

### ADN (Rich Frontmatter)

```yaml
---
title: Vienna Life Assistant MCP Integration
created: 2025-12-03
updated: 2025-12-03
tags: [mcp, vienna-life, integration, fastmcp-3.1.1+]
type: note
status: in-progress
related:
  - [[FastMCP 3.1.1+]]
  - [[MCP Studio]]
  - [[Stdio Transport]]
categories: [development, mcp]
---
```

**ADN uses this** for semantic search, tagging, relationships!

### MCP Central Docs (Simple Frontmatter)

```yaml
---
title: MCP Transport Methods
date: 2025-12-03
status: CURRENT
versions:
  - fastmcp: 3.1.1++
  - mcp-protocol: 1.0
tags: [mcp, transport, stdio, http]
related:
  - path: ../fastmcp/basics.md
    description: FastMCP implementation
  - path: ../../docker/CONTAINERIZATION_GUIDE.md
    description: Docker integration
---
```

**MCP Central Docs uses this** for basic cross-referencing (but ADN is way better!)

---

## What Each System Wins At

### ADN Wins ðŸ†

1. **Auto-linking** - `[[Entity]]` just works
2. **Semantic search** - AI-powered, understands meaning
3. **Tagging** - Flexible, dynamic, multi-dimensional
4. **Daily work** - Built for rapid note-taking
5. **Knowledge graph** - Visualize relationships
6. **Import/export** - Obsidian, Notion, Joplin, etc.

### MCP Central Docs Wins ðŸ†

1. **Distribution** - Zip and email!
2. **Onboarding** - New dev just reads markdown
3. **Portability** - No setup, works everywhere
4. **Git history** - Track every change
5. **Stability** - Doesn't change unless intentional
6. **Universal** - GitHub, IDE, any editor

---

## Use Case Matrix

| Scenario | Use ADN | Use MCP Central Docs |
|----------|---------|----------------------|
| Daily progress notes | âœ… | âŒ |
| Brainstorming | âœ… | âŒ |
| Connecting ideas | âœ… | âŒ |
| Complex searches | âœ… | âŒ |
| Private observations | âœ… | âŒ |
| Onboarding new dev | âŒ | âœ… |
| Final reference | âš ï¸ Can export | âœ… |
| Distribution | âš ï¸ Need export | âœ… |
| Standards | âŒ | âœ… |
| Patterns | âš ï¸ Draft | âœ… Final |
| Git versioning | âŒ | âœ… |
| Offline work | âš ï¸ Need ADN | âœ… Just files |

---

## Practical Examples

### Scenario 1: New Developer Onboarding

**Day 1: Send them mcp-central-docs**
```powershell
# Package documentation
Compress-Archive -Path "mcp-central-docs\docs" `
                 -DestinationPath "mcp-reference-complete.zip"

# Email: "Read through this - our standards and guides"
# They unzip, read at their own pace
# No ADN setup needed
```

**Week 2: Give them ADN access**
```bash
# After they understand basics
# Show them ADN for:
# - Daily progress tracking
# - Connecting their work to existing knowledge
# - Searching project history
```

### Scenario 2: Feature Implementation

**Brainstorm phase (ADN):**
```markdown
# HTTP Transport for Vienna Life Assistant

Thinking through implementation:
- [[MCP Studio]] uses [[stdio transport]] pattern
- But [[Docker]] containers can't spawn host processes
- Solution: [[HTTP transport]] OR mount volumes
- Related: [[FastMCP 3.1.1+]] dual interface

Questions:
- How does [[Plex MCP]] handle this?
- Check [[Tapo Camera MCP]] implementation

Tags: #mcp #transport #vienna-life #brainstorm
```

**Document phase (MCP Central Docs):**
```markdown
# MCP Transport Methods

**Last Updated:** 2025-12-03

## Stdio Transport
[Clean, polished guide...]

## HTTP Transport
[Clear implementation examples...]
```

### Scenario 3: Standards Definition

**Research (ADN):**
```markdown
Testing different [[portmanteau]] approaches:
- Try 1: Generic `str` for operation â†’ Bad discoverability
- Try 2: `Literal["list", "create"]` â†’ Perfect! âœ…
- Try 3: Separate tools â†’ Tool explosion

Conclusion: Use Literal for operation enums

Related: [[MCP Portmanteau]], [[FastMCP]], [[Tool Discoverability]]
```

**Standard (MCP Central Docs):**
```markdown
# Portmanteau Tool Best Practices

**Standard:** Use `Literal` for operation parameters

```python
from typing import Literal

@mcp.tool()
async def vm_management(
    action: Literal["list", "create", "start", "stop"]
):
    ...
```

**Rationale:** [Polished explanation...]
```

---

## Link Strategy

### ADN (Automatic!)
```markdown
Working with [[Vienna Life Assistant]] and [[FastMCP]].
Need to integrate [[Plex MCP]] via [[stdio transport]].

# ADN automatically:
# - Creates links
# - Tracks relationships
# - Builds knowledge graph
# - Enables semantic search
```

### MCP Central Docs (Manual, Intentional)
```markdown
# Vienna Life Assistant

See [MCP Integration Guide](../mcp/integration.md) for details.

Related:
- [FastMCP Basics](../fastmcp/basics.md)
- [Plex MCP](../projects/plex-mcp/STATUS.md)
- [Stdio Transport](../mcp-protocol/TRANSPORTS.md#stdio)
```

**ADN wins linking everytime!** But manual links are more explicit and intentional.

---

## Search Comparison

### ADN
```bash
# Semantic search (AI-powered)
adn_search("how to optimize docker builds for MCP servers")
# Understands MEANING, finds relevant notes

# Complex Boolean
adn_search("(FastMCP OR MCP) AND docker AND NOT archived")

# Tag-based
adn_search("transport", tags=["mcp", "stdio"])

# Date-filtered
adn_search("vienna life", after_date="1 week")
```

**Winner:** ADN ðŸ† (no contest!)

### MCP Central Docs
```powershell
# Grep (literal text)
grep -r "docker optimization" docs/

# Find files
Get-ChildItem -Recurse -Filter "*docker*.md"

# Windows search
# Type in File Explorer search box
```

**Winner:** Basic, but reliable

---

## Tagging Comparison

### ADN
```markdown
# Note with rich tagging

Tags: #mcp #fastmcp-3.1.1+ #docker #optimization #vienna-life
Categories: [development, mcp, infrastructure]
Related: [[Docker]], [[FastMCP]], [[Build Optimization]]
```

**Search:**
```bash
# Find all notes tagged fastmcp-3.1.1+ AND docker
adn_search("", tags=["fastmcp-3.1.1+", "docker"])
```

**Winner:** ADN ðŸ† (powerful, flexible, AI-enhanced)

### MCP Central Docs
```yaml
---
tags: [mcp, docker, optimization]
categories: [development]
---
```

**Search:**
```powershell
# Grep frontmatter
grep -r "tags:.*docker" docs/
```

**Winner:** Basic, manual

---

## Import/Export

### ADN
```bash
# Import from Obsidian
adn_import("obsidian", source_path="/path/to/vault")

# Export to Docsify
adn_export("docsify", export_path="/path/to/site")

# Export to PDF
adn_export("pandoc", format_type="pdf")

# Import from Notion
adn_import("notion", source_path="Notion-Export.zip")
```

**Winner:** ADN ðŸ† (designed for this!)

### MCP Central Docs
```bash
# "Import" = copy markdown files
cp other-docs/*.md mcp-central-docs/docs/

# "Export" = zip files
Compress-Archive -Path docs -DestinationPath export.zip
```

**Winner:** Basic, but portable

---

## The Ideal Workflow

### Phase 1: Research & Development (ADN)

**Use ADN for:**
- Daily progress notes
- Brainstorming features
- Connecting ideas
- Quick LLM interactions
- Research aggregation
- Decision documentation

**Example:**
```markdown
# 2025-12-03 - MCP Integration Work

Progress:
- Fixed [[stdio transport]] implementation
- Learned [[MCP Studio]] pattern
- Updated [[Vienna Life Assistant]]

Tomorrow:
- Add [[HTTP transport]] for [[Docker]]
- Test [[Plex MCP]] integration

Tags: #progress #mcp #vienna-life
```

### Phase 2: Polish & Document (MCP Central Docs)

**Extract to MCP Central Docs:**
- Standards and patterns
- Implementation guides
- Best practices
- Reference documentation

**Example:**
```markdown
# MCP Stdio Transport Pattern

**Last Updated:** 2025-12-03

Based on MCP Studio implementation...
[Polished, complete guide]
```

### Phase 3: Distribution (MCP Central Docs)

**Package for distribution:**
```powershell
# Create onboarding package for new hire
Compress-Archive -Path "mcp-central-docs\docs" `
                 -DestinationPath "onboarding-package.zip"
```

**Email includes:**
- Complete reference documentation
- No ADN setup required
- Works immediately
- All standards in one place

---

## Crosslinking Strategies

### ADN: Automatic & Semantic

```markdown
Working on [[Feature X]] using [[Tool Y]].
Related to [[Project Z]].

# ADN automatically:
# 1. Creates entity pages
# 2. Links them bidirectionally
# 3. Builds relationship graph
# 4. Enables graph traversal
```

**Winner:** ADN ðŸ† (hands down!)

### MCP Central Docs: Manual & Explicit

```markdown
# Feature X

Implementation uses [Tool Y](../tools/tool-y.md).

Related to [Project Z](../projects/project-z.md).

See also:
- [Pattern A](../patterns/pattern-a.md)
- [Guide B](../guides/guide-b.md)
```

**Benefit:** Explicit, intentional, works everywhere

---

## Real-World Examples

### Vienna Life Assistant Development

**ADN notes:**
```markdown
# Vienna Life MCP Integration - 2025-12-03

Progress:
- Implemented [[MCP Server]] with portmanteau tools
- Created [[MCP Client]] for [[Plex]], [[Calibre]], [[Ollama]]
- Fixed [[stdio transport]] (was doing HTTP wrong!)
- Added [[Media Dashboard]] widget

Issues found:
- [[Docker]] containers can't spawn host processes easily
- Solution: Mount `/repos` volume OR use HTTP transport

Next:
- Test [[Plex MCP]] integration
- Add [[Calibre MCP]] current reading
- Implement [[AI recommendations]]

Related: [[FastMCP 3.1.1+]], [[MCP Studio]], [[Docker]]
Tags: #vienna-life #mcp #integration #progress
```

**MCP Central Docs guide (polished):**
```markdown
# MCP Client Implementation Guide

**Last Updated:** 2025-12-03

## Stdio Transport Pattern

Based on real-world implementation in Vienna Life Assistant...
[Complete, polished guide with code examples]
```

---

## Strengths Summary

### ADN: The Clever One ðŸ§ 
- **Auto-magic** - Links, tags, search work automatically
- **Living system** - Grows with your knowledge
- **AI-enhanced** - Semantic understanding
- **Personal** - Your knowledge graph

### MCP Central Docs: The Reliable One ðŸ“š
- **Portable** - Zip and go!
- **Universal** - Works everywhere
- **Stable** - Intentional changes only
- **Distributable** - Email to new hire

---

## Best Practice: Use Both!

**Daily Work** â†’ ADN  
**Polish** â†’ MCP Central Docs  
**Distribute** â†’ MCP Central Docs  
**Research** â†’ ADN  
**Reference** â†’ MCP Central Docs  
**Brainstorm** â†’ ADN  
**Onboard** â†’ MCP Central Docs

---

## Related Documentation

### ADN Documentation
- `D:/Dev/repos/advanced-memory-mcp/docs/` - ADN guides
- ADN notes themselves - Living examples

### MCP Central Docs
- `../` - This repository
- `CROSS_REFERENCE_INDEX.md` - Find topics
- `DOCUMENTATION_FRESHNESS_SYSTEM.md` - Keep current

---

**Last Updated:** 2025-12-03  
**Freshness:** CURRENT  
**Note:** This relationship is stable - update only if ADN or docs strategy changes


