# Repomix MCP Server

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**Pack repositories into AI-friendly formats for comprehensive codebase analysis**

A Model Context Protocol (MCP) server that integrates [Repomix](https://repomix.com/) to provide AI assistants with powerful repository analysis capabilities.

## Quick Start

```powershell
git clone https://github.com/sandraschi/repomix-mcp
cd repomix-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

## Features

- **Repository Packing**: Convert entire repositories into AI-friendly formats (XML, Markdown, JSON, Plain text)
- **Intelligent Compression**: Tree-sitter based compression (~70% token reduction)
- **Content Analysis**: Read and analyze packed repository output
- **Pattern Search**: Search for specific code patterns within packed repositories
- **Remote Repository Support**: Pack GitHub repos without cloning
- **Security Scanning**: Built-in Secretlint integration

## Prerequisites

- **Python 3.9+**
- **Node.js 18+** (for Repomix)
- **Repomix**: Install globally with `npm install -g repomix`

##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx repomix-mcp
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "repomix-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/repomix-mcp", "run", "repomix-mcp"]
  }
}
```
##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx repomix-mcp
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "repomix-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/repomix-mcp", "run", "repomix-mcp"]
  }
}
```
### Option 2: Docker

```bash
docker compose up -d
```

### Option 3: MCPB Package

```powershell
# Build MCPB package
.\scripts\build-mcpb.ps1

# Install with MCPB
mcpb install dist\repomix-mcp.mcpb
```

## Configuration

### Cursor IDE Setup

Add to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "repomix": {
      "command": "python",
      "args": ["D:/Dev/repos/repomix-mcp/src/repomix_mcp/server.py"],
      "env": {
        "PYTHONPATH": "D:/Dev/repos/repomix-mcp/src"
      }
    }
  }
}
```

### Claude Desktop Setup

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "repomix": {
      "command": "python",
      "args": ["D:/Dev/repos/repomix-mcp/src/repomix_mcp/server.py"],
      "env": {
        "PYTHONPATH": "D:/Dev/repos/repomix-mcp/src"
      }
    }
  }
}
```

## Usage

Once configured, the following MCP tools become available to AI assistants:

### pack_repository
Pack a repository into an AI-friendly format.

**Parameters:**
- `repository_path`: Path to the repository to pack
- `output_file`: Output file path (optional)
- `style`: Format - "xml", "markdown", "json", "plain"
- `include_patterns`: Glob patterns to include
- `ignore_patterns`: Glob patterns to ignore
- `compress`: Enable Tree-sitter compression

### read_packed_output
Read and analyze packed repository output.

**Parameters:**
- `packed_file_path`: Path to the packed output file
- `max_lines`: Maximum lines to return

### search_packed_output
Search for patterns within packed repository output.

**Parameters:**
- `packed_file_path`: Path to the packed output file
- `query`: Search query/pattern
- `case_sensitive`: Case sensitive search

### list_supported_formats
List supported output formats and compression options.

## Examples

### Pack Current Repository
```
"Pack the current repository and analyze its structure"
```

### Pack with Specific Format
```
"Pack the src/ directory as markdown with compression enabled"
```

### Search for Patterns
```
"Find all authentication-related code in this repository"
```

### Analyze Dependencies
```
"Pack the package.json and requirements.txt files and analyze dependencies"
```

## Development

### Running Locally

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the MCP server
python src/repomix_mcp/server.py
```

### Testing

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run specific test
pytest tests/test_pack_repository.py -v
```

### Code Quality

```bash
# Lint
ruff check .

# Format
ruff format .

# Type check
mypy src/
```

## Architecture

```
repomix-mcp/
 src/repomix_mcp/
    server.py          # Main FastMCP server
    __init__.py        # Package initialization
    cli.py             # Command-line interface
 mcpb/
    manifest.json      # MCP server manifest
    mcpb.json         # Build configuration
 tests/                 # Test suite
 docs/                  # Documentation
 docker-compose.yml     # Docker setup
```

## API Reference

### FastMCP Tools

All tools return structured responses with `success` boolean and contextual `message` fields.

#### Error Handling
- Invalid repository paths return descriptive error messages
- Missing Repomix installation is detected and reported
- File permission issues are handled gracefully
- Network timeouts for remote repositories are managed

#### Response Format
```python
{
    "success": true,
    "message": "Operation completed successfully",
    "data": { ... }  # Tool-specific results
}
```

## Security

- **No sensitive data exposure**: Packed output excludes common secret files
- **Safe remote repository access**: HTTPS-only for Git operations
- **Local execution**: All operations run locally, no external API dependencies
- **Input validation**: All paths and parameters are validated before processing

## Performance

- **Efficient compression**: Tree-sitter provides ~70% token reduction
- **Streaming output**: Large repositories are processed without excessive memory usage
- **Caching support**: Packed outputs can be cached for repeated analysis
- **Parallel processing**: Multiple repositories can be processed concurrently

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [Repomix](https://repomix.com/) by Yamadashy for the core repository packing technology
- [FastMCP](https://FastMCP 3.1.0com/) for the MCP framework
- [Anthropic](https://anthropic.com/) for the Model Context Protocol specification
