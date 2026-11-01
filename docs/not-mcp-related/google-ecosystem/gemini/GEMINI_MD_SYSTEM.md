# GEMINI.md System - Sandra's Technical Specification Framework

**Document Status:** v13.1 - March 2026 SOTA Standard
**Last Updated:** 2026-03-18
**Location:** `C:\Users\<user>\.gemini\GEMINI.md`
**Purpose:** Comprehensive technical specification for materialist/reductionist AI system development

---

## Overview

The GEMINI.md system is a comprehensive technical specification document that defines Sandra's complete technology stack, development standards, and operational guidelines. Unlike standard Gemini AI documentation, this framework encompasses:

- **AI System Architecture** - Complete LLM integration stack
- **Full-Stack Development** - Frontend/backend standards with production patterns
- **Hardware Optimization** - RTX 4090 GPU acceleration and local LLM infrastructure
- **Robotics Integration** - Physical and virtual robotics control systems
- **MCP Ecosystem** - Model Context Protocol server orchestration

---

## System Hierarchy & Structure

### Core Sections (Version 12.0)

#### I. Sandra Persona: Core Identity & Philosophical Foundation
**Purpose:** Defines system personality, behavioral constraints, and philosophical framework
- **Identity & Demographics:** Vienna-based software engineer profile
- **Philosophical Framework:** Materialist/reductionist epistemology
- **Communication Parameters:** Industrial technical voice with wry humor
- **Political & Social Framework:** Center-left Sozialdemokratin alignment
- **Cultural Affiliations:** Japanophilia, Sinophilia, European identity
- **Personal Context:** Family structure, companion animal, residence details

#### II. LLM Engine: Behavioral Integrity & Logic Guardrails
**Purpose:** Immutable operational constraints independent of persona context
- **Reality Denial Prohibition:** No gaslighting of technical reality
- **Simplification Restriction:** No destructive simplification of complex logic
- **Mock Transparency:** All mocked data explicitly flagged with `[MOCK]`
- **Sycophancy Ban:** Zero "rah-rah" behavior, peer technical contributor status
- **Precision Maintenance:** Zero translation loss in technical specifications

#### III. Physical Substrate: Hardware & Infrastructure Architecture
**Purpose:** Complete workstation and infrastructure specification
- **Primary Workstation:** Windows 11 Pro with 24-core AMD CPU, 64GB RAM, RTX 4090 GPU
- **Edge Computing Grid:** Tapo cameras/plugs, Nest, Ring, Hue Lighting integration
- **Mobile Infrastructure:** iOS ecosystem with MacBooks for development
- **Remote Access:** Tailscale VPN for secure development access

#### IV. Universal Skill Architecture & Development Tooling
**Purpose:** Standardized development framework and tooling ecosystem
- **Primary Framework:** Anthropic "Skills" layout (SKILL.md, scripts/, references/, assets/)
- **Packaging Standard:** .mcpb format mandatory for all skill distribution
- **Google Cloud Stack:** Vertex AI Agent Builder, Firebase GenKit, NotebookLM Studio
- **Development Environment:** Cursor, VS Code, Zed with MCP integration
- **Build System:** FastMCP 3.1+, Ruff, Turbopack
- **Quality Assurance:** pytest with comprehensive test coverage requirements

#### V. High-Availability Operational Heuristics
**Purpose:** Production system reliability and maintenance procedures
- **Zombie Process Suppression:** Periodic port culling (9000-9999 range)
- **State Coordination:** Redis-based inter-agent state synchronization
- **Service Discovery:** Glama.ai auto-surfacing via standardized glama.json
- **Resource Monitoring:** Continuous CPU/memory/GPU utilization tracking
- **Automatic Recovery:** Self-healing processes for failed services

#### VI. Functional Objective & System Architecture
**Purpose:** Mission statement and architectural overview
- **Antigravity Neural Grid:** Marketplace-ready, high-availability AI platform
- **Quality Metrics:** 99.9% uptime, <0.1% error rate, zero-trust security
- **Technical Excellence:** Zero-compromise engineering standards
- **Empirical Rigor:** All decisions grounded in observable data

#### VII. Google AI Universe: Comprehensive Integration Guide
**Purpose:** Production-ready Google AI ecosystem integration patterns
- **Model Specifications:** Current Gemini 3.0 series with technical details
- **API Integration:** Vertex AI Agent Builder, Firebase GenKit, NotebookLM patterns
- **Production Deployment:** FastAPI endpoints with authentication and monitoring
- **Cost Optimization:** Intelligent model routing and usage tracking
- **Security Configuration:** Enterprise-grade security and compliance
- **Performance Monitoring:** BigQuery analytics and usage dashboards

#### VIII. Robotics Project Stack: Hardware & Virtual Robotics Integration
**Purpose:** Complete robotics ecosystem from physical hardware to virtual simulation
- **Robotics MCP Server:** Unified orchestration of 6+ MCP servers
- **Unitree Robotics:** R1 humanoid platform with Vienna coffee shop mission
- **VRChat Integration:** Social VR testing environment
- **OSC Protocol:** Real-time communication for robotics applications
- **ROS Integration:** Physical robot control through rosbridge_suite
- **Makerspace Partnership:** TMW techLAB Vienna collaboration

#### IX. Frontend Development Standards & Architecture
**Purpose:** Production-ready React/TypeScript frontend development patterns
- **Technology Stack:** React 18+, TypeScript, Next.js 14+, Tailwind CSS, Vite
- **Component Architecture:** Atomic Design pattern with comprehensive TypeScript typing
- **Build Optimization:** Advanced Vite configuration with performance monitoring
- **State Management:** Zustand with persistence and React Query for server state
- **Testing Standards:** Testing Library with comprehensive component testing
- **Performance Monitoring:** Web Vitals integration and Core Web Vitals tracking

#### X. Backend Development Standards & Architecture
**Purpose:** Enterprise-grade backend patterns with FastAPI and modern Python
- **Framework Stack:** FastAPI, SQLAlchemy async, Pydantic validation, PostgreSQL
- **API Design:** RESTful endpoints with comprehensive OpenAPI documentation
- **Authentication:** JWT with role-based access control and security middleware
- **Database Architecture:** Type-safe ORM with relationships and migrations
- **Testing Infrastructure:** pytest with unit, integration, and API testing
- **Production Deployment:** Docker containerization with monitoring and logging

#### XI. Local LLM Stack & RTX 4090 GPU Optimization
**Purpose:** Complete local AI infrastructure optimized for high-end GPU hardware
- **Hardware Optimization:** RTX 4090 CUDA acceleration and memory management
- **Model Management:** Registry system with automatic model selection and VRAM optimization
- **Inference Server:** FastAPI-based local LLM serving with GPU acceleration
- **Fine-tuning Pipeline:** LoRA adaptation for domain-specific persona training
- **Performance Monitoring:** GPU utilization, inference timing, and model metrics
- **TensorRT Integration:** Optimized inference engine for production deployment

---

## Best Practices & Maintenance Guidelines

### Document Maintenance
1. **Version Control:** Semantic versioning (MAJOR.MINOR.PATCH) with date stamps
2. **Update Frequency:** Review quarterly or when major technology changes occur
3. **Change Tracking:** Document all significant modifications with rationale
4. **Consistency Checks:** Ensure alignment between sections and external implementations

### Implementation Standards
1. **Code Examples:** All code samples must be production-ready and tested
2. **Security Reviews:** Regular security audits of authentication and data handling patterns
3. **Performance Benchmarks:** Establish and monitor performance metrics for all components
4. **Documentation Sync:** Keep implementation code synchronized with specification documentation

### Quality Assurance
1. **Cross-References:** Validate that all referenced repositories, tools, and services exist
2. **Link Validation:** Regularly check all web links and GitHub repository references
3. **Version Compatibility:** Ensure specified versions remain current and supported
4. **Integration Testing:** Verify that described integration patterns work in practice

---

## Integration with MCP Ecosystem

### MCP Server Dependencies
The GEMINI.md system integrates with the following MCP servers:

| Server | Purpose | Repository |
|--------|---------|------------|
| `robotics-mcp` | Physical/virtual robot control | https://github.com/sandraschi/robotics-mcp |
| `osc-mcp` | Real-time OSC communication | https://github.com/sandraschi/osc-mcp |
| `vrchat-mcp` | VRChat avatar control | https://github.com/sandraschi/vrchat-mcp |
| `unity3d-mcp` | Unity3D virtual robotics | https://github.com/sandraschi/unity3d-mcp |
| `blender-mcp` | 3D model creation | https://github.com/sandraschi/blender-mcp |
| `gimp-mcp` | Texture processing | https://github.com/sandraschi/gimp-mcp |
| `avatar-mcp` | Avatar management | https://github.com/sandraschi/avatar-mcp |

### FastMCP Framework Standards
- **Version:** FastMCP 3.1+ (latest stable)
- **Transport:** stdio (primary) + HTTP (FastAPI) dual interface
- **Documentation:** Comprehensive docstrings with examples
- **Error Handling:** Structured error responses with error codes
- **Testing:** pytest with comprehensive unit and integration coverage

---

## Web Links & Resources

### Google AI Ecosystem
- **Gemini AI Studio:** https://aistudio.google.com
- **Vertex AI Platform:** https://cloud.google.com/vertex-ai
- **Firebase GenKit:** https://firebase.google.com/docs/genkit
- **NotebookLM:** https://notebooklm.google.com
- **Google DeepMind:** https://deepmind.google
- **Antigravity IDE:** https://antigravity.google.com

### Development Tools & Frameworks
- **FastMCP:** https://gofastmcp.com
- **React Documentation:** https://react.dev
- **FastAPI Documentation:** https://fastapi.tiangolo.com
- **Next.js Documentation:** https://nextjs.org/docs
- **Vite Documentation:** https://vitejs.dev
- **Tailwind CSS:** https://tailwindcss.com

### Robotics & Hardware
- **Unitree Robotics:** https://unitree.com
- **ROS Documentation:** https://docs.ros.org
- **VRChat Developer:** https://docs.vrchat.com
- **Unity3D:** https://unity.com
- **Blender:** https://www.blender.org

### MCP Ecosystem
- **Model Context Protocol:** https://modelcontextprotocol.io
- **MCPB Packaging:** https://gofastmcp.com/docs/packaging
- **Glama Registry:** https://glama.ai
- **Claude Desktop:** https://docs.anthropic.com/claude/docs/desktop

---

## GitHub Repositories

### Core MCP Servers
- **robotics-mcp:** https://github.com/sandraschi/robotics-mcp
  - Unified physical/virtual robotics control
  - 6+ MCP server composition
  - Moorebot Scout + Unitree integration

- **osc-mcp:** https://github.com/sandraschi/osc-mcp
  - Open Sound Control protocol server
  - 19 bidirectional OSC tools
  - Professional audio/visual application control

- **vrchat-mcp:** https://github.com/sandraschi/vrchat-mcp
  - VRChat avatar and world control
  - OSC integration with Claude Desktop
  - Plugin system for extensibility

- **unity3d-mcp:** https://github.com/sandraschi/unity3d-mcp
  - Unity3D game engine integration
  - Virtual robotics development
  - World Labs Marble import support

### Supporting MCP Servers
- **blender-mcp:** https://github.com/sandraschi/blender-mcp
  - 3D model creation and processing
  - Robot model generation pipeline
  - FBX/GLTF export capabilities

- **gimp-mcp:** https://github.com/sandraschi/gimp-mcp
  - Image processing and texture creation
  - Automated texture generation for 3D models
  - Batch processing workflows

- **avatar-mcp:** https://github.com/sandraschi/avatar-mcp
  - Avatar management and animation
  - VRM format support for robotics
  - Cross-platform avatar systems

### Development & Infrastructure
- **mcp-central-docs:** https://github.com/sandraschi/mcp-central-docs
  - Centralized MCP documentation
  - Standards and best practices
  - Integration guides and patterns

- **unitree-robotics:** https://github.com/sandraschi/unitree-robotics
  - Complete Unitree R1 humanoid ecosystem
  - Vienna coffee shop companion robot
  - Hardware and software integration

- **local-llm-mcp:** https://github.com/sandraschi/local-llm-mcp
  - Local LLM inference and management
  - RTX 4090 optimization
  - Model registry and serving infrastructure

### Claude Desktop Extensions
- **claude-skills:** https://github.com/sandraschi/claude-skills
  - Claude Skills ecosystem management
  - Plugin creation and packaging
  - Community skill contributions

---

## Implementation Status & Roadmap

### Current Implementation Status (v12.0)

| Component | Status | Repository | Notes |
|-----------|--------|------------|-------|
| **Core Persona** | ✅ Complete | GEMINI.md | v12.0 with comprehensive identity |
| **LLM Guardrails** | ✅ Complete | GEMINI.md | Immutable behavioral constraints |
| **Hardware Spec** | ✅ Complete | GEMINI.md | RTX 4090 + infrastructure details |
| **Development Standards** | ✅ Complete | GEMINI.md | Frontend/backend patterns |
| **Google AI Integration** | ✅ Complete | GEMINI.md | Production-ready patterns |
| **Robotics Stack** | ✅ Complete | GEMINI.md | Hardware/virtual integration |
| **Local LLM Stack** | ✅ Complete | GEMINI.md | RTX 4090 optimization |
| **MCP Server Integration** | 🔄 Active | robotics-mcp | 6+ server composition |
| **FastAPI Implementation** | ✅ Complete | Multiple repos | Production deployments |
| **Testing Infrastructure** | 🔄 Active | All repos | pytest + integration tests |

### Future Enhancements
1. **AI Safety Integration:** Advanced guardrails for production AI systems
2. **Multi-GPU Support:** Distributed inference across multiple RTX 4090 GPUs
3. **Edge Deployment:** Robotics edge computing with TinyML integration
4. **Regulatory Compliance:** Vienna robotics regulations and EU AI Act compliance
5. **Performance Benchmarking:** Automated performance testing and optimization

---

## Related Documentation

### MCP Central Docs References
- **[FastMCP Standards](../fastmcp/)** - Framework implementation guidelines
- **[MCP Server Composition](../patterns/mcp-server-composition.md)** - Multi-server integration patterns
- **[Production Deployment](../deployment/)** - Production readiness checklists
- **[Security Standards](../deployment/security.md)** - Security implementation guides

### External Standards
- **[Anthropic Skills](https://docs.anthropic.com/claude/docs/skills)** - Claude Skills framework
- **[OpenAPI Specification](https://swagger.io/specification/)** - API documentation standards
- **[OWASP Security](https://owasp.org/www-project-top-ten/)** - Web application security
- **[ROS 2 Documentation](https://docs.ros.org/en/humble/)** - Robotics framework standards

---

## Contact & Maintenance

**Maintainer:** Sandra S. (Vienna, Austria)
**Location:** Vienna 9th District (Vienna)
**Email:** sandra.schipa [at] technical-specification.org
**GitHub:** https://github.com/sandraschi

### Maintenance Schedule
- **Quarterly Reviews:** Technology stack updates and version compatibility
- **Monthly Updates:** Security patches and dependency updates
- **Continuous Integration:** Automated testing and validation
- **Community Contributions:** Open to improvements and extensions

---

**This GEMINI.md system represents a comprehensive technical specification framework that transcends traditional AI model documentation to encompass complete system architecture, development standards, and operational excellence for materialist/reductionist AI development.**





