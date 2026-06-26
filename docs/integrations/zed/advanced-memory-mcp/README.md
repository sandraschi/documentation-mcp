# Advanced Memory MCP Zed Extension

Local-first knowledge management system with MCP bidirectional communication, FastMCP 3.1.1+.3 conversational error handling, and agentic content workflows, packaged as a Zed IDE extension.

## Features

- Knowledge Graph Navigation: Bidirectional communication between LLMs and markdown files
- Project Management: Switch contexts, manage projects, and organize knowledge
- Search & Discovery: Full-text search across all content with filtering
- Conversational Error Handling: Friendly, helpful error messages instead of technical jargon
- Agentic Content Workflows: LLM-driven orchestration of knowledge management tasks
- MCPB Packaging: Standardized MCP bundle format for distribution

## Installation

### Prerequisites

1. Rust Toolchain: Install via rustup
2. Wasm Target: rustup target add wasm32-wasip1
3. Zed IDE: Download from zed.dev
4. Advanced Memory MCP: Install from GitHub

### Build Extension

```bash
# Unix/Mac
./build.sh

# Windows
.\build.ps1
```

### Install in Zed

1. Open Zed IDE
2. Press Cmd+Shift+P (Mac) or Ctrl+Shift+P (Linux/Windows)
3. Type "zed: extensions"
4. Select "Install Dev Extension"
5. Choose this directory (advanced-memory-mcp/)

## Configuration

The extension expects Advanced Memory MCP to be available via uv run --project path/to/advanced-memory-mcp --mcp. Update the path in src/lib.rs to match your Advanced Memory MCP installation location.

## Usage

Once installed, Advanced Memory MCP will appear in Zed
'
s Assistant panel as "Advanced Memory MCP". You can then:

- Navigate knowledge graphs via memory:// URLs
- Write and edit notes with semantic observations
- Search across projects with advanced filtering
- Switch between project contexts
- Use conversational error handling for better user experience

## Agentic Content Workflows

Leverage FastMCP 3.1.1+.3 sampling capabilities for intelligent knowledge management:

```javascript
// Content analysis and organization
await adn_agentic_workflow({
  "workflow_prompt": "Analyze recent notes, identify patterns, and suggest knowledge gaps",
  "available_operations": ["search_notes", "build_context", "generate_insights"],
  "max_iterations": 5
})

// Research orchestration
await adn_agentic_workflow({
  "workflow_prompt": "Conduct research on quantum computing, organize findings, and create summary",
  "available_operations": ["search_notes", "write_note", "edit_note", "generate_summary"],
  "max_iterations": 10,
  "context": {"topic": "quantum computing", "depth": "comprehensive"}
})
```

## Architecture

This Zed extension acts as a bridge between Zed
'
s AI assistant and the Advanced Memory MCP Python server:

```
Zed IDE â†’ Rust Wasm Bridge â†’ Advanced Memory MCP Server â†’ Knowledge Graph
```

## Troubleshooting

- Build fails: Ensure wasm32-wasip1 target is installed
- Server not found: Update the path to Advanced Memory MCP in src/lib.rs
- Extension not loading: Check Zed logs for Wasm compilation errors

## License

MIT License - see Advanced Memory MCP repository for full license details.

## Author

Sandra Schipal (sandraschipal@gmail.com)

