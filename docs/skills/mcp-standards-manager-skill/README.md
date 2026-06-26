# MCP Standards Manager Skill

A Claude Desktop skill for automated MCP ecosystem standards management and compliance checking.

## Installation

1. Download `mcp-standards-manager-skill.zip`
2. Import into Claude Desktop:
   - Settings → Skills → Import Skill
   - Select the ZIP file
   - Skill appears as "mcp-standards-manager"

## Usage

The skill provides standards management commands within Claude Desktop conversations:

```
# Check repository compliance
standards check-repo --repo /path/to/repo

# Generate documentation
standards generate-docs --repo /path/to/repo

# Update FastMCP versions
standards update-versions --version 2.14.3
```

## Features

- **Compliance Checking**: Automated MCP standards validation
- **Documentation Generation**: Template-based docs creation
- **Version Management**: FastMCP ecosystem updates
- **Repository Orchestration**: Cross-repo standards application

## Requirements

- Claude Desktop with skills support
- MCP repositories with proper structure
- FastMCP 2.14.3+ compatible servers

## License

MIT License - see MCP Central Docs for details.