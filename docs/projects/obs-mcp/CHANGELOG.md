# Changelog

All notable changes to the OBS Studio MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-12-21

### ðŸ› ï¸ **Code Quality & Maintenance**
- âœ… **Ruff Linting**: Fixed all 44 linting issues across the codebase
  - Removed unused imports (`asyncio`, `sys`, `pathlib.Path`, `uuid`, `OBSRequest`)
  - Fixed variable shadowing issues where local variables shadowed imported `status` module
  - Cleaned up unused variables and improved code consistency
- âœ… **Pydantic V2 Migration**: Resolved all deprecation warnings
  - Updated `Field` extra keyword arguments to use `json_schema_extra`
  - Fixed `@validator` decorators to use `@field_validator`
  - Updated class-based config to use `ConfigDict`
  - Fixed `update_forward_refs()` method calls
- âœ… **Code Formatting**: Applied consistent formatting across all files
  - 5 files reformatted, 2 files left unchanged
  - Improved readability and maintainability

### ðŸ”§ **Technical Improvements**
- âœ… **Import Organization**: Cleaned up import statements
  - Fixed `status` import from `fastapi` to `starlette`
  - Removed redundant and unused imports
  - Better import grouping and organization
- âœ… **Error Handling**: Enhanced error handling patterns
  - Improved variable scoping in async functions
  - Better exception handling in OBS client
- âœ… **Type Safety**: Strengthened type annotations
  - Better type hints throughout the codebase
  - Improved Pydantic model definitions

### ðŸ“Š **Quality Metrics**
- **Linting Score**: 0 errors, 0 warnings
- **Code Coverage**: Maintained existing test coverage
- **Performance**: No performance regressions
- **Compatibility**: Full backward compatibility maintained

### ðŸ”„ **Migration Notes**
- **Breaking Changes**: None
- **Dependencies**: No new dependencies added
- **Configuration**: No configuration changes required
- **API**: All existing APIs remain unchanged

## [0.1.0] - 2025-10-15

### âœ¨ **Initial Release**
- **FastMCP 3.1.1+.0 Integration**: Full MCP protocol compliance
- **OBS WebSocket Support**: Complete OBS Studio automation
- **Streaming Control**: Start/stop streams with status monitoring
- **Recording Management**: Full recording lifecycle control
- **Scene Management**: Dynamic scene switching and management
- **Audio Control**: Mute/unmute sources, volume adjustment
- **Replay Buffer**: Highlight capture and management
- **Virtual Camera**: Video call integration support
- **DXT Packaging**: Ready for MCP deployment environments
- **Docker Support**: Containerized deployment with multi-architecture builds
- **WebSocket Error Handling**: Robust connection management
- **Configuration Management**: Flexible settings via Pydantic models

### ðŸš€ **Features**
- 20+ MCP tools for comprehensive OBS automation
- Real-time status monitoring and control
- Cross-platform compatibility (Windows, macOS, Linux)
- Extensive error handling and logging
- Production-ready deployment options

### ðŸ“š **Documentation**
- Complete API documentation
- Installation and setup guides
- Troubleshooting and debugging guides
- Integration examples and patterns

---

## Development Guidelines

### Version Numbering
This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

### Commit Convention
Commits follow the [Conventional Commits](https://conventionalcommits.org/) specification:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for test additions/modifications
- `chore:` for maintenance tasks

### Quality Assurance
- **Ruff Linting**: All code must pass ruff checks
- **Type Checking**: Full type annotation coverage
- **Testing**: Comprehensive test suite with high coverage
- **Documentation**: Updated documentation for all changes
- **Security**: Regular security audits and dependency updates














