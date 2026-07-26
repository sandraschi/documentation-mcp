# Changelog - new-mcp-server-intelligent.ps1

## [1.0.1] - 2025-10-25

### Fixed
- PowerShell variable parsing error on line 456 (`$op:` → `${op}:`)
- PowerShell variable parsing error on line 773 (`$Wrappee:` → `${Wrappee}:`)
- Script now runs without parser errors

### Changed
- Synced fixes to `templates/scripts/` and `scripts/` folders

## [1.0.0] - 2025-10-24

### Initial Release

#### Added
- Wrappee application analysis
- Knowledge base for common applications
- Intelligent tool generation
- Domain-specific portmanteau tools
- Integration guide generation
- Web service wrapper support

#### Features
- 8 pre-analyzed applications in knowledge base
- CLI/API/UI capability detection
- Intelligent tool naming
- Comprehensive integration guides
- 9.9/10 quality score output

