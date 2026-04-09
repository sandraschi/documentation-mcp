# Zed GitHub Repositories: Essential Guide

**Critical repositories for Zed IDE development and MCP extensions**

## 🏆 Core Zed Repositories

### 1. **zed-industries/zed** ⭐⭐⭐ **MUST USE**
**Primary Repository - The Heart of Zed**
- **Purpose**: Main Zed IDE codebase and core functionality
- **Languages**: Rust (primary), TypeScript/JavaScript
- **Activity**: 🔥 **Weekly releases** - extremely active development
- **Key Directories**:
  - `extensions/` - Extension system implementation
  - `crates/zed_extension_api/` - API definitions and traits
  - `crates/language_models/` - AI/LLM integration
  - `docs/` - Developer documentation and guides
- **For MCP Developers**: Study the extension loading mechanism and API evolution
- **Releases**: Major version bumps indicate breaking API changes

### 2. **zed-industries/extensions** ⭐⭐⭐ **MUST USE**
**Official Extension Registry - Quality Curated**
- **Purpose**: Community extension hosting and distribution
- **Structure**: Git submodules for each extension
- **Submission Process**:
  ```bash
  # Fork the repo
  git clone https://github.com/YOUR_USERNAME/extensions.git
  cd extensions

  # Add your extension as submodule
  git submodule add https://github.com/YOUR_USERNAME/your-extension extensions/your-extension

  # Submit PR
  git add .
  git commit -m "Add your-extension"
  git push origin main
  # Create PR to zed-industries/extensions
  ```
- **Quality Standards**: Strict code review, security audit, documentation requirements
- **Discovery**: Primary place users find extensions
- **For MCP Developers**: Your extensions belong here for official distribution

### 3. **zed-industries/zed-extension-api** ⭐⭐⭐ **MUST USE**
**API Specification - The Contract**
- **Purpose**: Rust crate defining extension interface and traits
- **Current Version**: `0.2.0` (as of Jan 2026)
- **Breaking Changes**: Frequent with Zed releases
- **Key Traits**:
  - `Extension` - Main extension trait you implement
  - `ContextServerId` - Server identification
  - `Command` - Process spawning interface
- **Documentation**: Inline Rust docs are authoritative
- **For MCP Developers**: This is your primary dependency

## 🛠️ Development Tools

### 4. **zed-industries/zed-playground** ⭐⭐ **RECOMMENDED**
**Development Sandbox - Testing Ground**
- **Purpose**: Isolated environment for extension development and testing
- **Features**:
  - Hot reload during development
  - Debugging tools and logging
  - Isolated from main Zed installation
- **Use Cases**:
  - Rapid prototyping before full extension
  - Testing extension loading/unloading
  - Debugging extension lifecycle issues
- **Setup**: Clone and run as separate Zed instance

### 5. **zed-industries/docs** ⭐⭐ **RECOMMENDED**
**Developer Documentation - Learning Resource**
- **Purpose**: Comprehensive guides for extension development
- **Content**:
  - Extension API tutorials
  - Best practices and patterns
  - Troubleshooting guides
  - Architecture explanations
- **Languages**: Markdown with code examples
- **Updates**: Kept current with API changes

## 🌐 Community Resources

### 6. **zed-extensions** (GitHub Organization) ⭐ **OPTIONAL**
**Community Extensions - Experimental**
- **Purpose**: Community-maintained extensions not in official registry
- **Quality**: Variable - evaluate carefully
- **Use Cases**:
  - Finding experimental features
  - Inspiration for your own extensions
  - Community patterns and approaches
- **Warning**: Not officially vetted - check security and code quality

## 📋 Repository Usage Matrix

| Repository | Purpose | When to Use | Frequency |
|------------|---------|-------------|-----------|
| **zed** | Study core implementation | Understanding architecture | Occasional |
| **extensions** | Publish your extension | Ready for distribution | One-time |
| **zed-extension-api** | Implement extensions | Every extension project | Daily |
| **zed-playground** | Develop & test | Active development | Daily |
| **docs** | Learn & troubleshoot | Getting started, issues | As needed |
| **zed-extensions** | Find inspiration | Research phase | Occasional |

## 🔄 Development Workflow

### Typical Extension Development Cycle:

1. **Study API**: Read `zed-extension-api` crate documentation
2. **Prototype**: Use `zed-playground` for initial testing
3. **Implement**: Build against `zed-extension-api`
4. **Test**: Extensive testing in `zed-playground`
5. **Document**: Follow patterns from `docs`
6. **Submit**: Add to `extensions` registry via PR
7. **Maintain**: Watch `zed` releases for API changes

### Staying Current:

- **Follow** `zed-industries/zed` releases for API changes
- **Watch** `zed-industries/zed-extension-api` for crate updates
- **Monitor** `zed-industries/extensions` for new patterns
- **Check** Zed Discord `#extensions` for community discussion

## 🚨 Critical Notes

### API Evolution
- **Breaking Changes**: Frequent with Zed's rapid development
- **Version Pinning**: Always pin `zed_extension_api` to specific version
- **Testing**: Test against multiple Zed versions when possible

### Security Considerations
- **Sandbox**: Extensions run in Wasm sandbox - cannot access host filesystem
- **Process Spawning**: Only way to access external tools (like MCP servers)
- **Review**: Official extensions undergo security review

### FOSS Philosophy
Zed exemplifies **true open source development**:
- Transparent roadmap and development
- Community-driven feature decisions
- Rapid iteration based on user feedback
- High-quality standards maintained

## 📞 Getting Help

### Official Channels
- **GitHub Issues**: `zed-industries/zed` for bugs, `extensions` for submissions
- **Discord**: `#extensions` channel for community help
- **Documentation**: `zed-industries/docs` for tutorials

### Community Resources
- **Awesome Zed**: Community-curated extension list
- **Extension Examples**: Study existing extensions in registry
- **MCP Community**: Cross-pollination with MCP server developers

---

**Author**: Sandra Schipal
**Purpose**: Essential reference for Zed extension development
**Last Updated**: January 15, 2026
