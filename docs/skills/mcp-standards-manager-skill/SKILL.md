<!--
SOURCE: MCP Standards Manager - Custom Skill
AUTHOR: MCP Community
LICENSE: MIT
CREATED: 2026-01-20
-->

---
name: mcp-standards-manager
description: Automated MCP ecosystem standards management, compliance checking, and documentation generation for FastMCP 3.2+ servers.
---

# MCP Standards Manager

Comprehensive standards management for the MCP ecosystem. Use this skill when working with MCP servers, documentation, or compliance requirements.

## When to Use

**Use this skill for:**
- MCP server compliance checking
- Standards documentation generation
- FastMCP version management
- Repository standards setup
- MCP ecosystem maintenance

**Don't use for:**
- General development tasks
- Non-MCP related standards
- Individual coding problems

## Commands Available

### Compliance Checking
```
# Check single repository
standards check-repo --repo /path/to/repo

# Check all repositories
standards check-all-repos

# Generate compliance report
standards compliance-report --format json
```

### Documentation Generation
```
# Generate complete documentation
standards generate-docs --repo /path/to/repo

# Generate specific document
standards generate-doc --type readme --repo /path/to/repo

# Update all docs
standards docs-update --repos all
```

### Version Management
```
# Update FastMCP versions
standards update-versions --version 2.14.3

# Check version compatibility
standards check-versions
```

### Repository Management
```
# Create new MCP server
standards create-repo --type mcp-server --name blender-mcp

# Get repository status
standards repo-status --repos all
```

## Standards Reference

### FastMCP Requirements
- **Minimum Version**: FastMCP 3.2+
- **Sampling Support**: Required for creative MCP servers
- **Enhanced Response Patterns**: Mandatory for SOTA compliance

### Repository Structure
```
mcp-server/
├── src/mcp_server_name/
├── tests/
├── docs/
├── pyproject.toml
├── README.md
└── .mcp-standards.yaml
```

### Documentation Standards
- **README.md**: Short overview with links to detailed docs
- **INSTALL.md**: Platform-specific installation instructions
- **CHANGELOG.md**: Semantic versioning format
- **PRD.md**: Product requirements document

## Progressive Usage

### Level 1: Basic Commands
Start with simple compliance checks:
```bash
standards check-repo --repo .
standards compliance-report
```

### Level 2: Documentation
Generate and update documentation:
```bash
standards generate-docs --repo .
standards docs-update
```

### Level 3: Ecosystem Management
Manage entire MCP ecosystem:
```bash
standards check-all-repos
standards update-versions --version 2.14.3
standards repo-status --repos all
```

## Error Handling

### Common Errors
```
❌ Repository not found
→ Check path and ensure directory exists

❌ Standards version mismatch
→ Update to latest standards version

❌ FastMCP version too old
→ Use: standards update-versions --version 2.14.3
```

### Getting Help
- **Command help**: `standards --help`
- **Specific command**: `standards <command> --help`
- **Standards docs**: Reference MCP Central Docs

## Best Practices

### Repository Setup
1. Always run `standards check-repo --repo .` after setup
2. Use `standards generate-docs` for initial documentation
3. Keep FastMCP versions updated with `standards update-versions`

### Regular Maintenance
- Run compliance checks weekly
- Update documentation quarterly
- Monitor FastMCP version releases

### Team Collaboration
- Use consistent standards across all repositories
- Share compliance reports with team
- Document custom standards in central docs

## Integration Points

### CI/CD Integration
```yaml
# .github/workflows/standards.yml
- name: Check Standards Compliance
  run: standards check-repo --repo .
```

### IDE Integration
- Cursor: Automatic standards validation
- VS Code: Standards checking extensions
- Pre-commit hooks: Standards enforcement

### Repository Management
- GitHub Actions: Automated compliance checks
- Repository templates: Standards-compliant structure
- Branch protection: Standards validation required

## Skill Architecture

### Core Components
- **Standards Engine**: Rule interpretation and validation
- **Documentation Engine**: Template-based generation
- **Compliance Checker**: Automated auditing
- **Repository Manager**: Cross-repo operations

### Data Flow
```
User Request → Command Parsing → Standards Engine → Repository Operations → Results
                      ↓
                Documentation Engine → Template Application → Validation
                      ↓
                Compliance Checker → Audit → Report Generation
```

## Troubleshooting

### Skill Not Loading
- Ensure SKILL.md is in correct directory
- Check YAML frontmatter syntax
- Verify Claude Desktop version compatibility

### Command Not Found
- Run `standards --help` to list available commands
- Check repository has proper MCP structure
- Ensure FastMCP dependencies are installed

### Standards Out of Date
- Run `standards update-standards` (future feature)
- Check MCP Central Docs for latest standards
- Update skill to latest version

## Version History

### 1.0.0 (Current)
- Initial release with core standards management
- FastMCP 3.2+ compliance checking
- Documentation generation and validation
- Repository management and orchestration
- Cross-platform support

### Planned Features (1.1.0)
- Real-time compliance monitoring
- Advanced documentation analysis
- Automated standards updates
- Multi-repository orchestration
- Performance optimization tools

---

**This skill maintains MCP ecosystem quality and consistency across all repositories and team members.**