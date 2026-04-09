# Zed IDE Integrations

This directory contains comprehensive documentation and examples for integrating MCP (Model Context Protocol) servers with the Zed IDE through its revolutionary extension system.

## ðŸŽ¯ Key Resources

### [ZED_ECOSYSTEM_EXPANSION.md](ZED_ECOSYSTEM_EXPANSION.md) ðŸŒŸ **Ecosystem Expansion & Monorepos**
## 🎯 Key Resources

### [ZED_ECOSYSTEM_EXPANSION.md](ZED_ECOSYSTEM_EXPANSION.md) 🌟 **Ecosystem Expansion & Monorepos**
Complete overview of the expanded Zed MCP ecosystem:
- 14 production extensions deployed across creative, development, media, VR, and infrastructure domains
- Monorepo handling solutions for repos with both MCP servers and webapps
- Intelligent entry point detection and automated extension generation
- Path to Zed registry submission with quality assurance pipeline

### [ZED_LATEST_RESEARCH_APR_2026.md](ZED_LATEST_RESEARCH_APR_2026.md) 🚀 **Latest Research (April 2026)**
Detailed analysis of the April 2026 releases (0.230.x):
- Latest release telemetry (0.230.2)
- New features: Top-down streaming, native devcontainers, and Git Graph v2
- Mature ACP Registry integration and comparison vs Cursor and Antigravity

### [ZED_OVERVIEW.md](ZED_OVERVIEW.md) 📊 **Executive Summary**
Comprehensive overview of Zed's position in the agentic IDE landscape:
- Revolutionary AI-native architecture vs traditional VSCode-derived IDEs
- FOSS leadership and unique local LLM capabilities
- Technical strengths and competitive advantages
- Strategic roadmap and market positioning

### [ZED_MCP_EXTENSIONS_GUIDE.md](ZED_MCP_EXTENSIONS_GUIDE.md) ðŸ› ï¸ **Implementation Guide**
Complete technical guide for creating Zed MCP extensions:
- Step-by-step implementation with code examples
- Architecture patterns and best practices
- Essential GitHub repositories and development workflow
- Troubleshooting and advanced features

### [ZED_HISTORY_AND_ECOSYSTEM.md](ZED_HISTORY_AND_ECOSYSTEM.md) ðŸ“ˆ **History & Analysis**
Deep analysis of Zed's emergence and competitive positioning:
- "Coming from behind" strategic advantages
- Technical architecture comparison with VSCode ecosystem
- Unique features and peculiarities
- Multi-agent capability assessment (not yet implemented)

### [ZED_FOSS_AND_LOCAL_LLM.md](ZED_FOSS_AND_LOCAL_LLM.md) ðŸŒŸ **FOSS & Local LLM**
Zed's unique position as the only truly open source AI IDE:
- FOSS excellence in proprietary AI IDE landscape
- Revolutionary local LLM integration capabilities
- Privacy, security, and cost advantages
- Technical implementation and performance benchmarks

### [ZED_TECHNICAL_ANALYSIS.md](ZED_TECHNICAL_ANALYSIS.md) ðŸ”¬ **Technical Deep Dive**
Comprehensive technical analysis and competitive comparison:
- Architecture superiority (Rust + Wasm vs Electron + Node.js)
- Performance benchmarks and optimization strategies
- Security model and extension isolation
- SWOT analysis and market positioning

### [ZED_GITHUB_REPOSITORIES.md](ZED_GITHUB_REPOSITORIES.md) ðŸ“š **Repository Guide**
Essential guide to Zed's GitHub ecosystem and development workflow:
- Core repositories with detailed explanations and usage patterns
- Development workflow and contribution processes
- Staying current with Zed's rapid evolution
- Quality standards and community governance

## ðŸ—ï¸ Zed Architecture Highlights

Zed represents a **fundamental breakthrough** in IDE design:

- **AI-Native**: Built from the ground up for AI integration (not bolted on)
- **WebAssembly Extensions**: Secure sandboxing with native performance
- **MCP Integration**: Seamless external tool connectivity
- **True FOSS**: Community-driven development with rapid iteration
- **Local LLM Support**: Unique privacy-preserving AI capability
- **Modern Tech Stack**: Rust + GPU acceleration vs Electron/Chromium

## ðŸ“Š 14 Production Extensions Deployed

### ðŸŽ¨ **Creative & Design Suite** (4 extensions)
- **inkscape-mcp**: Vector graphics and SVG editing (SOTA reference implementation)
- **blender-mcp**: 3D modeling and animation
- **gimp-mcp**: Professional image editing
- **ocr-mcp**: Multi-engine document processing

### ðŸ› ï¸ **Development & Gaming Suite** (2 extensions)
- **unity3d-mcp**: Unity game development tools
- **filesystem-mcp**: Advanced file operations

### ðŸŽ¬ **Media & Content Suite** (3 extensions)
- **plex-mcp**: Media server management
- **calibre-mcp**: Ebook library tools
- **osc-mcp**: Open Sound Control protocol

### ðŸŒ **VR & Social Suite** (2 extensions)
- **resonite-mcp**: VR world creation
- **vrchat-mcp**: VRChat development tools

### âš™ï¸ **Infrastructure Suite** (2 extensions)
- **virtualization-mcp**: VM and container management
- **advanced-memory-mcp**: Knowledge graph management

### ðŸ  **Monorepo Support**
All extensions include intelligent entry point detection for repos containing both MCP servers and webapp frontends, ensuring clean isolation and proper execution.

## ðŸ”— Essential Zed GitHub Repositories

| Repository | Purpose | Status |
|------------|---------|--------|
| [`zed-industries/zed`](https://github.com/zed-industries/zed) | Main IDE codebase | ðŸ”¥ Weekly releases |
| [`zed-industries/extensions`](https://github.com/zed-industries/extensions) | Official extension registry | ðŸ† Quality curated |
| [`zed-industries/zed-extension-api`](https://github.com/zed-industries/zed-extension-api) | Extension API specification | ðŸ”„ Rapid evolution |
| [`zed-industries/zed-playground`](https://github.com/zed-industries/zed-playground) | Development sandbox | ðŸ§ª Prototyping |
| [`zed-industries/docs`](https://github.com/zed-industries/zed/tree/main/docs) | Developer documentation | ðŸ“– Comprehensive |

## ðŸš€ Quick Start

1. **Install Zed**: Download from [zed.dev](https://zed.dev)
2. **Install Rust**: `rustup` toolchain required
3. **Add Wasm target**: `rustup target add wasm32-wasip1`
4. **Read the guides**: Start with [ZED_ECOSYSTEM_EXPANSION.md](ZED_ECOSYSTEM_EXPANSION.md)

## ðŸŽ¯ Competitive Advantages

### ðŸ† **Only Truly FOSS AI IDE**
- Complete open source vs proprietary Cursor/Windsurf
- Transparent development and community governance
- No vendor lock-in or subscription requirements

### ðŸ¤– **Unique Local LLM Integration**
- Run AI models locally for complete privacy
- Zero API costs after initial setup
- Offline functionality unmatched by cloud-only competitors

### âš¡ **Architectural Superiority**
- Rust core + WebAssembly vs Electron/Chromium
- 2-3s startup vs 5-15s for VSCode-derived IDEs
- Memory efficient: 200-400MB vs 500MB-2GB+

### ðŸš€ **Development Velocity**
- Weekly releases vs competitors' monthly cycles
- Immediate bug fixes and feature iteration
- Community-driven innovation

## ðŸ”§ Monorepo Challenge Solved

**Problem**: MCP repos containing both servers and webapps create installation complexity.

**Solution**: Intelligent entry point detection automatically finds and runs only the MCP server component:

- Scans `pyproject.toml` `[project.scripts]` sections
- Checks common server locations and naming patterns
- Supports complex monorepo architectures
- Ensures clean isolation between webapp and MCP server execution

## ðŸ“‹ Quality Assurance Standards

All extensions meet **SOTA (State-of-the-Art)** standards:

- âœ… **PyPI Distribution**: `pip install` and `uv pip install` support
- âœ… **uv/uvx Execution**: One-shot execution without installation
- âœ… **MCPB Compatibility**: Claude Desktop and Windsurf configuration
- âœ… **GitHub Source**: Direct installation from repositories
- âœ… **Cross-Platform**: Windows, macOS, Linux support
- âœ… **Documentation**: Comprehensive INSTALL.md and README.md
- âœ… **CI/CD**: Automated testing and Wasm compilation
- âœ… **Security**: Pre-commit hooks and vulnerability scanning

## ðŸ¤ Community & Contributing

Zed maintains **true FOSS principles**:
- Transparent development process
- Community extension registry
- Rapid iteration based on user feedback
- High-quality standards for all contributions

### Zed Registry Submission Process

1. **Prepare Extension**: Ensure all quality standards are met
2. **Fork Registry**: `git clone https://github.com/YOUR_USERNAME/extensions.git`
3. **Add Submodule**: `git submodule add https://github.com/sandraschi/YOUR-MCP extensions/YOUR-MCP`
4. **Submit PR**: Zed team reviews and merges to official registry

### Development Workflow

Extensions are developed with:
- **Template Automation**: Standardized generation from proven templates
- **Quality Gates**: Automated linting, testing, and security scanning
- **Monorepo Intelligence**: Automatic MCP server detection and isolation
- **Cross-Platform Testing**: Verified compatibility across all target platforms

## ðŸ“š Related MCP Central Docs

- [MCP Server Registry](../) - Other MCP server implementations
- [FastMCP Framework](../../docs/FAST_MCP_3.1.1+_MIGRATION.md) - Python MCP development
- [Cross-Reference Index](../../CROSS_REFERENCE_INDEX.md) - Finding related documentation

## ðŸ”® Future Developments

- **Phase 1**: Submit core extensions (inkscape, unity, filesystem) to Zed registry
- **Phase 2**: Roll out creative suite (blender, gimp, ocr)
- **Phase 3**: Add media and infrastructure extensions
- **Phase 4**: Specialized VR and social tools
- **Ongoing**: Automated extension generation for new MCP repos

---

**Maintained by**: Sandra Schipal
**Ecosystem Scale**: 14 production extensions deployed
**Quality Standard**: SOTA packaging and distribution
**Monorepo Support**: Intelligent entry point detection
**Registry Status**: Ready for Zed official submission

*From single proof-of-concept to comprehensive ecosystem: Zed's MCP revolution is here.*

