# Changelog - new-mcp-server.ps1

## [2.1.0] - 2025-12-28

### Added
- FastMCP 3.1.1+.1 compliance (instructions parameter in constructor)
- Server-level instructions support for better AI context
- Updated documentation with correct FastMCP constructor usage

### Changed
- Updated FastMCP constructor to use `instructions` parameter instead of `description`
- Enhanced server scaffold with comprehensive instructions template
- Improved documentation examples

## [2.0.0] - 2025-10-24

### Added
- Portmanteau tools pattern implementation
- Multilevel help system (basic/intermediate/advanced)
- Status/diagnostics tool
- Complete test scaffold with pytest
- .cursorrules with Rule #1
- SOTA scripts integration

### Changed
- Updated to FastMCP 3.1.1++ (no description= parameter)
- Improved pyproject.toml generation
- Better test structure

### Fixed
- Test file tool invocation (use FunctionTool checks instead of direct calls)
- Empty [project.scripts] entry issue

## [1.0.0] - 2025-10-21

### Initial Release
- Basic MCP server scaffold generation
- FastMCP integration
- Test and CI/CD templates


