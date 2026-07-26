# MCP Skills Directory

Repository for MCP ecosystem skills and standards.

## Available Skills

### MCP Standards Skill (Windsurf Compatible)
**File**: `mcp-standards-windsurf.zip`

Complete MCP ecosystem standards reference with hierarchical documentation:
- FastMCP 3.2+ requirements and sampling workflows
- Project scaffolding, packaging, and deployment standards
- Testing, error handling, logging, and monitoring patterns
- Frontend integration and documentation standards

**Import**: Settings → Skills → Import Skill → Select ZIP

### Antigravity IDE Skills (Advanced Memory MCP)
**Directory**: `.agents/skills/`

Skills formatted for Antigravity IDE with additional metadata and configuration. Contains the same MCP Standards content but with IDE-specific structure.

**Note**: Antigravity IDE uses a custom `.agents/skills/` format, not compatible with standard Claude Desktop/Windsurf skills.

## Directory Structure

```
skills/
├── README.md                          # This file
├── mcp-standards-windsurf.zip        # Windsurf-compatible skill
├── windsurf-mcp-standards/           # Source directory for ZIP
│   ├── SKILL.md                      # Entry point
│   ├── _toc.md                       # Table of contents
│   └── modules/                      # Detailed standards docs
└── .agents/                          # Antigravity IDE format
    └── skills/
        ├── config.json               # IDE configuration
        ├── README.md                 # IDE-specific docs
        └── mcp-standards/            # Same content, different format
```

## Skill Formats

### Windsurf/Claude Desktop Format
- SKILL.md at root level
- YAML frontmatter must start at line 1, column 1
- UTF-8 encoding without BOM
- Unix line endings (LF)
- Relative links: `./modules/filename.md`

### Antigravity IDE Format
- `.agents/skills/` wrapper directory
- Additional metadata and configuration files
- IDE-specific loading and management features
- Not compatible with standard Claude Desktop

## Development

### Creating New Skills
1. Create skill directory with SKILL.md
2. Add supporting documentation in subdirectories
3. Test import in target IDE
4. Generate ZIP for distribution

### Updating Standards
1. Edit modules in both formats
2. Regenerate ZIP files
3. Test compatibility across IDEs

---

**Contact**: MCP Community - Standards and Skills