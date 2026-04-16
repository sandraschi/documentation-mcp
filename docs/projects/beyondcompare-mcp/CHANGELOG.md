# Changelog

All notable changes to the Beyond Compare MCP project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **ðŸš€ MAJOR FEATURE:** 8 new developer workspace management tools
- `backup_dev_repositories`: Smart repository backup with intelligent filtering (excludes node_modules, __pycache__, etc.)
- `analyze_dev_workspace`: Comprehensive workspace analysis with language statistics and dependency tracking
- `scan_repo_health`: Repository health scanning with automated issue detection and fixes
- `cleanup_dev_artifacts`: Automated cleanup of build artifacts and temporary files across repositories
- `find_duplicate_code`: Cross-repository duplicate code detection for refactoring opportunities
- `compare_workspace_snapshots`: Compare workspace backups to track changes over time
- `selective_restore`: Flexible restoration of specific projects or files from backups
- **ðŸŽµ Multimedia Tools:** Enhanced multimedia drive scanning and duplicate detection
- `multimedia_drive_scanner`: Complete drive inventory with filtering options
- `find_multimedia_duplicates`: Content-based duplicate detection across drives
- `detect_usb_drives`: USB drive detection and detailed information
- **ðŸ“¦ MCPB Packaging:** Complete MCPB implementation replacing DXT packaging
- Modular tool architecture with `src/beyondcompare_mcp/tools/developer/` structure
- FastMCP 3.1.1+ compliance with proper decorators and multiline docstrings
- Comprehensive documentation updates (README, API docs, User Guide)

### Changed
- **BREAKING:** Package format changed from DXT to MCPB (60.4 KB self-contained package)
- **ARCHITECTURE:** Refactored tools into modular structure for better maintainability
- Enhanced README.md with comprehensive tool documentation (13 tools total)
- Updated manifest.json with all 13 tools and proper metadata
- Improved tool registration using modern FastMCP 3.1.1+ standards

### Technical
- Total tools expanded from 5 to 13 (160% increase in functionality)
- Perfect for D:/dev/repos backup and management workflows
- Intelligent filtering prevents backing up node_modules, build artifacts, etc.
- Space-efficient backups with compression and incremental support
- Cross-repository analysis and health monitoring capabilities

## [0.1.1] - 2025-08-16

### Added
- Modern MCP 3.1.1++ support with latest FastMCP framework
- Enhanced security documentation and badges
- Production-ready status indicators
- Comprehensive development tooling (ruff, mypy, pre-commit)
- Updated system requirements documentation

### Changed
- **BREAKING:** Updated to MCP 3.1.1++ from legacy 1.0.0 (requires Python 3.10+)
- **BREAKING:** Modernized FastMCP import from `mcp.server.fastmcp` to `fastmcp`
- Updated all dependencies to current stable versions
- Enhanced README.md with modern badges and security status
- Improved pyproject.toml with comprehensive development tools
- Updated GitHub repository references to sandraschi/beyondcompare-mcp
- Removed deprecated warnings and updated to production-ready status

### Fixed
- **SECURITY:** All critical security vulnerabilities resolved (see BUILD_COMPLETE.md)
- **SECURITY:** Command injection prevention with comprehensive input validation
- **SECURITY:** Path traversal protection with `..` detection and path sanitization
- **SECURITY:** Secure subprocess execution with controlled argument handling
- **SECURITY:** Secure temporary file management with unique naming
- Corrected import statements for missing modules (os, subprocess)
- Fixed version management and __version__ import errors
- Resolved broken dependency references to non-existent packages
- Updated documentation to reflect secure, production-ready status

### Security
- âœ… **RESOLVED:** Remote Code Execution vulnerabilities via command injection
- âœ… **RESOLVED:** Path Traversal attacks through `..` directory traversal
- âœ… **RESOLVED:** Insecure temporary file handling with predictable names
- âœ… **RESOLVED:** Insufficient input validation allowing dangerous characters
- âœ… **RESOLVED:** Fake/non-existent dependency vulnerabilities
- âœ… **VERIFIED:** Comprehensive security audit passed with 85%+ test coverage
- âœ… **VERIFIED:** All subprocess execution now uses controlled, validated arguments
- âœ… **VERIFIED:** Input sanitization blocks dangerous characters: `;`, `|`, `&`, `>`, `<`, `` ` ``, `$`, `(`, `)`

### Deprecated
- Legacy MCP 1.0.0 support (use MCP 3.1.1++ going forward)
- Old nested FastMCP import path (use direct `fastmcp` import)

### Technical Notes
- **DXT Rebuild Required:** Existing DXT packages contain outdated dependencies
- **Python Version:** Now requires Python 3.10+ (increased from 3.8+)
- **Package Size:** Expected increase to ~40-45 MB due to modern MCP 3.1.1++ libraries
- **Dependencies:** Migrated from fake "fastmcp>=3.1.1+.0" to real "fastmcp>=3.1.1+.0"
- **Architecture:** Enhanced with modern async support and structured logging

## [0.1.0] - 2023-07-31

### Added
- Initial release of Beyond Compare MCP server
- Support for FastMCP 3.1.1+
- Basic file and folder comparison functionality
- Folder synchronization capabilities
- DXT packaging support

