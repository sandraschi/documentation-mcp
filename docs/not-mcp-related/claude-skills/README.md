# Claude Skills Library

**Quality-Rated Collection of Claude Skills**

This directory contains curated Claude Skills from Anthropic and the community, automatically rated for quality using "The Pizza Test™" methodology.

## 📊 Quick Stats

- **Total Skills**: 70+
- **Average Quality**: *** (56/100)
- **Sources**: Anthropic Official + Community
- **Quality Ratings**: 1-5 stars
- **Last Updated**: 2026-01-27

## 🌟 Quality Distribution

See [INDEX.md](INDEX.md) for complete quality-rated list.

**Quality Tiers**:
- ***** (90-100): Excellent - Best of the best
- **** (75-89): Good - Recommended  
- *** (60-74): Acceptable - Usable
- ** (40-59): Below Average - Needs work
- * (0-39): Poor - Major issues

## 📁 Directory Structure

```
claude-skills/
├── official/          # Anthropic's official skills
│   ├── developer/     # Development tools
│   ├── creative/      # Creative applications
│   ├── data-science/  # Data and analytics
│   └── general/       # General purpose
├── community/         # Community-contributed skills
│   ├── awesome-skills/
│   └── skills-collection/
├── INDEX.md          # Quality-rated skill list
├── SOURCES.md        # Attribution and sources
└── README.md         # This file
```

## 🍕 The Pizza Test™

Our quality rating system includes domain-specific critical checks:

**Italian Cooking Skill without pizza** = ⭐ (automatic 1-star!)  
**Python Skill without type hints** = ⭐  
**Research Skill without citations** = ⭐

Critical topics MUST be covered for a skill to be considered complete.

## 🎯 Top-Rated Skills

See [INDEX.md](INDEX.md) for the complete list. Some highlights:

**4-Star Skills** (****):
- `algorithmic-art` - Generative art creation (86/100)
- `docx` - Word document manipulation (86/100)
- `pptx` - PowerPoint generation (86/100)
- `xlsx` - Excel spreadsheet handling (83/100)
- `skill-creator` - Create new skills (81/100)
- `slack-gif-creator` - GIF creation for Slack (79/100)
- `mcp-builder` - Build MCP servers (76/100)

**3-Star Skills** (***):
- `webapp-testing` - Web app testing (73/100)
- `canvas-design` - Canvas-based designs (67/100)

## 💡 How to Use

### Browse Skills

```bash
# View all skills
cd D:\Dev\repos\mcp-central-docs\claude-skills

# Check a specific skill
cat official/developer/mcp-builder/SKILL.md

# See quality index
cat INDEX.md
```

### Import to Advanced Memory

```python
# Import all skills
adn_import("claude_skills", 
           source_path="D:/Dev/repos/mcp-central-docs/claude-skills/official/")

# Import only high-quality (4-5 star) skills
# (filter manually based on INDEX.md)

# Import single skill
adn_import("claude_skills",
           source_path="D:/Dev/repos/mcp-central-docs/claude-skills/official/developer/mcp-builder/SKILL.md")
```

### Use Directly in Claude Desktop

1. Copy skill folder to your Skills directory
2. Claude Desktop → Settings → Skills → Refresh
3. Skills appear in available skills list

## 🦾 Agentic IDE Integration

Modern Agentic IDEs (Cursor, Windsurf, Antigravity, Zed) can natively integrate these skills to enhance their autonomous capabilities.

- **Cursor**: Use `.cursor/skills/` directory for project-specific skills.
- **Windsurf**: Use `.windsurf/skills/` or global skill configuration.
- **Antigravity**: Native support via `adn_skills` and `.agents/` workflows.
- **Zed**: Integration via custom prompt engineering and skill file referencing.

→ Detailed Integration Guide: [AGENTIC_IDE_INTEGRATION.md](AGENTIC_IDE_INTEGRATION.md)

## 📖 Quality Rating Methodology

Each skill is analyzed on **100 points**:

### Frontmatter Quality (20 points)
- Complete YAML metadata
- Valid kebab-case naming
- Clear description
- Author and license info

### Content Quality (50 points)
- Clear structure with sections
- Detailed instructions
- Code examples included
- Sufficient depth (word count)

### Domain Coverage (30 points)
- Complete topic coverage
- No obvious gaps
- Domain-specific requirements met
- Best practices included

**See**: [analyze-skills.py](analyze-skills.py) for implementation details.

## 🔍 Attribution

All skills include attribution headers:

```markdown
<!--
SOURCE: https://github.com/anthropics/skills
ORIGINAL_PATH: mcp-builder/SKILL.md
AUTHOR: Anthropic
LICENSE: Apache-2.0
COPIED: 2025-10-28
-->
```

## 📚 Sources

**Official**:
- [Anthropic Skills](https://github.com/anthropics/skills) - Apache-2.0

**Community**:
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills) - MIT
- [Claude Skills Collection](https://github.com/abubakarsiddik31/claude-skills-collection) - MIT

See [SOURCES.md](SOURCES.md) for complete source information.

## 🔄 Updates

Skills are updated quarterly. To refresh:

```powershell
cd D:\Dev\repos\mcp-central-docs\claude-skills
.\organize-skills.ps1
python analyze-skills.py
```

## 📝 License

- **Skills**: Original licenses (see attribution headers)
- **Organization/Curation**: This collection structure and rating system
- **Analyzer**: MIT (analyze-skills.py)

## 🎯 Next Steps

1. **Browse [INDEX.md](INDEX.md)** - See all skills sorted by quality
2. **Check [SOURCES.md](SOURCES.md)** - Attribution and sources
3. **Import to Advanced Memory** - Use the skills in your knowledge base
4. **Use in Claude Desktop** - Deploy skills directly

---

**Maintained by**: MCP Central Docs  
**Purpose**: Curated, quality-rated Claude Skills library  
**Quality Standard**: The Pizza Test™  
**Status**: 70+ skills analyzed and rated

