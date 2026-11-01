# Claude Skills Sources

This directory contains curated Claude Skills from official and community sources.

**Last Updated**: 2025-10-28  
**Total Skills**: 27+

## Official Skills

### Anthropic Skills Repository
- **Source**: https://github.com/anthropics/skills
- **Author**: Anthropic
- **License**: Apache-2.0
- **Skills Count**: 27
- **Description**: Official Claude Skills examples from Anthropic, covering developer tools, creative applications, and productivity enhancements.
- **Quality**: High (official examples, well-structured)

**Included Skills**:
- MCP Builder - Build Model Context Protocol servers
- Skill Creator - Create new Claude Skills
- Document Skills - Work with DOCX, PPTX files
- Theme Factory - Create visual themes
- Internal Comms - Company communications
- Webapp Testing - Test web applications
- And more...

## Community Skills

### Awesome Claude Skills
- **Source**: https://github.com/travisvn/awesome-claude-skills
- **Author**: travisvn
- **License**: MIT
- **Type**: Curated list of skills and resources
- **Description**: Community-curated collection of Claude Skills and resources

### Claude Skills Collection
- **Source**: https://github.com/abubakarsiddik31/claude-skills-collection
- **Author**: abubakarsiddik31
- **License**: MIT
- **Type**: Collection of official and community skills
- **Description**: Compilation of Claude Skills from various sources

## Attribution

All skills in this directory include attribution headers with:
- Original source repository URL
- Original file path
- Author/organization
- License
- Copy date

## Usage

### Browse Skills
```bash
# By category
ls official/developer/
ls official/creative/
ls official/general/

# View a skill
cat official/developer/mcp-builder/SKILL.md
```

### Import to Advanced Memory
```python
# Import all skills
adn_import("claude_skills", 
           source_path="D:/Dev/repos/mcp-central-docs/claude-skills/official/")

# Import specific category
adn_import("claude_skills",
           source_path="D:/Dev/repos/mcp-central-docs/claude-skills/official/developer/")

# Import single skill
adn_import("claude_skills",
           source_path="D:/Dev/repos/mcp-central-docs/claude-skills/official/developer/mcp-builder/SKILL.md")
```

## Quality Rating

Coming soon: Automated quality rating system (1-5 stars) based on:
- Frontmatter completeness
- Content quality
- Examples included
- Domain coverage

**The Pizza Test™**: Domain-critical topics must be present!
- Italian cooking skill without pizza = ⭐ (1 star)
- Python skill without type hints = ⭐ (1 star)
- Research skill without citations = ⭐ (1 star)

## License Notes

- **Anthropic Skills**: Apache-2.0 (permissive, allows modification and distribution)
- **Community Skills**: Various (check individual skill headers)
- **This Collection**: Organization and curation by mcp-central-docs

## Updates

Skills are updated quarterly. To update:

```powershell
cd D:\Dev\repos\mcp-central-docs\claude-skills
.\update-skills.ps1  # Coming soon
```

## Contributing

To suggest new skills or improvements:
1. Check the original source repositories
2. Submit PR to the appropriate upstream repo
3. Skills will be included in next quarterly update

---

**Maintained by**: MCP Central Docs  
**Purpose**: Curated, organized, quality-rated Claude Skills library  
**Status**: Active

