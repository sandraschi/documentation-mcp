# MCPB Packaging Standards

## Overview
Standards for building and distributing MCP servers using MCPB (MCP Builder) packaging system.

## MCPB Configuration

### Required Files
```
mcpb/
├── manifest.json          # Package metadata
├── mcpb.json             # Build configuration
├── prompts/              # AI prompts and instructions
│   ├── system.md
│   ├── user.md
│   └── examples.json
└── assets/               # Static assets and templates
```

### manifest.json Structure
```json
{
  "name": "server-name",
  "version": "1.0.0",
  "description": "Brief server description",
  "author": "Developer Name",
  "license": "MIT",
  "repository": "https://github.com/username/repo",
  "keywords": ["mcp", "fastmcp", "domain"],
  "engines": {
    "node": ">=18.0.0",
    "python": ">=3.10.0"
  },
  "mcp": {
    "protocol_version": "2024-11-05",
    "capabilities": {
      "tools": true,
      "resources": false,
      "prompts": true
    }
  }
}
```

### mcpb.json Structure
```json
{
  "name": "server-name",
  "version": "1.0.0",
  "type": "server",
  "runtime": "python",
  "entry_point": "src/server.py",
  "dependencies": [
    "fastmcp>=2.14.3,<3.0.0",
    "other-dependency>=1.0.0"
  ],
  "dev_dependencies": [
    "pytest>=7.0.0",
    "ruff>=0.1.0"
  ],
  "build": {
    "include": [
      "src/**/*",
      "README.md",
      "LICENSE"
    ],
    "exclude": [
      "tests/",
      ".git/",
      "__pycache__/"
    ]
  },
  "scripts": {
    "build": "mcpb build",
    "test": "python -m pytest",
    "lint": "ruff check .",
    "format": "ruff format ."
  }
}
```

## Build Process

### 1. Development Build
```bash
# Build for local development
mcpb build --dev

# Output: dist/server-name-dev.mcpb
```

### 2. Production Build
```bash
# Build for distribution
mcpb build --prod

# Output: dist/server-name-v1.0.0.mcpb
```

### 3. Validation
```bash
# Validate package structure
mcpb validate dist/server-name-v1.0.0.mcpb
```

## Distribution Channels

### PyPI Distribution
```toml
# pyproject.toml
[project]
name = "mcp-server-name"
version = "1.0.0"
description = "MCP server description"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "fastmcp>=2.14.3,<3.0.0",
    # ... other deps
]

[project.urls]
Homepage = "https://github.com/user/repo"
Repository = "https://github.com/user/repo"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### MCP Registry
```bash
# Publish to MCP registry
mcpb publish dist/server-name-v1.0.0.mcpb
```

## Quality Gates

### Pre-Build Checks
- [ ] All tests pass (`pytest`)
- [ ] Code formatting (`ruff format`)
- [ ] Linting clean (`ruff check`)
- [ ] Type checking (`mypy`)
- [ ] Documentation up to date
- [ ] Version bump appropriate

### Package Validation
- [ ] MCPB validation passes
- [ ] All dependencies resolvable
- [ ] Entry point accessible
- [ ] No circular imports
- [ ] Proper error handling

## Version Management

### Semantic Versioning
- **MAJOR**: Breaking changes
- **MINOR**: New features
- **PATCH**: Bug fixes

### Version Files
```
__init__.py:
__version__ = "1.0.0"

pyproject.toml:
version = "1.0.0"

mcpb/manifest.json:
"version": "1.0.0"
```

## Common Packaging Issues

### ❌ Dependency Conflicts
```bash
# Check for conflicts
pip check
# or
poetry check
```

### ❌ Missing Files in Build
```json
// Ensure all needed files are included
{
  "build": {
    "include": [
      "src/**/*",
      "assets/**/*",
      "templates/**/*"
    ]
  }
}
```

### ❌ Runtime Import Errors
```python
# Use relative imports or __init__.py properly
from .tools import ToolClass
from . import config
```

## Integration Testing

### Local Testing
```bash
# Install locally for testing
pip install -e .

# Test MCP server
python -c "from mcp_server_name import app; print('Server loads successfully')"
```

### IDE Integration Testing
```json
// Test in Claude Desktop config
{
  "mcpServers": {
    "test-server": {
      "command": "python",
      "args": ["-m", "mcp_server_name.server"]
    }
  }
}
```

## Next Steps
After packaging, proceed to:
1. [Distribution Standards](./distribution.md)
2. [CI/CD Standards](./cicd.md)
3. [Maintenance Standards](./maintenance.md)