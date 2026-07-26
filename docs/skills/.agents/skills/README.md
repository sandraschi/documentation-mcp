# MCP Standards Skills

This directory contains Claude Desktop skills for MCP ecosystem standards management.

## Directory Structure

```
.agends/skills/
├── config.json          # Skills configuration
├── README.md           # This file
└── mcp-standards/      # MCP Standards skill
    ├── SKILL.md        # Main skill entry point
    ├── _toc.md         # Table of contents
    └── modules/        # Detailed standards documentation
        ├── mcp-scaffolding.md
        ├── mcpb-packaging.md
        ├── ai-sampling.md
        ├── frontend-sota.md
        ├── mcp-webapp-integration.md
        ├── github-workflows.md
        ├── testing.md
        ├── error-handling.md
        ├── logging.md
        ├── monitoring.md
        ├── docker-containerization.md
        └── documentation.md
```

## Skill Architecture

### Hierarchical Loading
- **SKILL.md**: Loaded first - provides overview and navigation
- **modules/*.md**: Loaded on-demand - detailed standards for specific tasks
- **_toc.md**: Table of contents for easy navigation

### Progressive Disclosure
1. **Entry Point** (SKILL.md) - Quick overview and decision tree
2. **Category Selection** - Choose relevant standards category
3. **Detailed Standards** - Load specific module for implementation
4. **Examples & Patterns** - Access concrete implementation examples

## Usage in Claude Desktop

### Importing the Skill
1. Locate the `MCP-Standards-Skill.zip` file
2. Open Claude Desktop → Skills → Import Skill
3. Select the ZIP file
4. Skill appears as "mcp-standards"

### Accessing Standards
```
# During MCP development conversations:
"When building an MCP server, what are the standards for error handling?"

# Claude Desktop loads:
# 1. SKILL.md overview
# 2. error-handling.md module (if needed)
# 3. Specific implementation patterns
```

## Standards Categories

### Development Standards
- **MCP Scaffolding**: Project structure and server templates
- **MCPB Packaging**: Build, distribution, and publishing
- **AI Sampling**: FastMCP 3.2+ sampling workflows

### Quality Assurance
- **Testing Standards**: Unit, integration, E2E testing
- **Error Handling**: Exception management and recovery
- **Logging Standards**: Structured logging patterns

### DevOps & Deployment
- **GitHub Workflows**: CI/CD and release management
- **Docker Standards**: Container architecture
- **Monitoring**: Prometheus, Grafana, Loki setup

### Documentation & Process
- **Documentation Standards**: README, CHANGELOG, PRD
- **Frontend SOTA**: React, TypeScript, Tailwind
- **MCP-WebApp Integration**: Backend-frontend bridging

## Configuration

### config.json Structure
```json
{
  "skills": [
    {
      "name": "mcp-standards",
      "path": "mcp-standards",
      "enabled": true,
      "categories": ["development", "documentation", "quality-assurance", "devops"]
    }
  ],
  "config": {
    "auto_load_modules": true,
    "cache_enabled": true
  }
}
```

## Development

### Adding New Standards
1. Create new module in `modules/` directory
2. Update `SKILL.md` with reference
3. Update `_toc.md` table of contents
4. Test skill loading in Claude Desktop

### Updating Existing Standards
1. Edit relevant module file
2. Test changes in Claude Desktop
3. Update version numbers if breaking changes
4. Regenerate ZIP package

## Performance Considerations

### Loading Strategy
- **SKILL.md**: Always loaded (~2KB) - provides navigation
- **Modules**: Loaded on-demand (~5-20KB each) - detailed content
- **Total Size**: ~200KB uncompressed, efficient for selective loading

### Memory Management
- Modules cached after first load
- Unused modules can be unloaded
- Structured for minimal context window impact

## Troubleshooting

### Skill Not Loading
- Verify SKILL.md has correct YAML frontmatter
- Check ZIP file structure
- Ensure Claude Desktop version supports skills

### Module Not Found
- Check file paths in SKILL.md references
- Verify module files exist in ZIP
- Test with Claude Desktop skill browser

### Performance Issues
- Large modules may impact loading
- Consider splitting very large modules
- Use progressive disclosure effectively

---

**This hierarchical skill structure enables Claude Desktop to provide comprehensive MCP standards guidance while maintaining efficient loading and minimal context window usage.**