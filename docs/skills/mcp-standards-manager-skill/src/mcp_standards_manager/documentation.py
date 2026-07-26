"""Documentation management functionality."""

import logging
from pathlib import Path
from typing import Optional

from .core import StandardsManager


class DocumentationManager:
    """Manages documentation generation and validation."""

    def __init__(self, standards_manager: StandardsManager):
        self.standards_manager = standards_manager
        self.logger = logging.getLogger(__name__)

    def generate_repository_docs(self, repo_path: Path, repo_type: str = "mcp-server", force: bool = False) -> None:
        """Generate complete documentation set for a repository."""
        self.logger.info(f"Generating documentation for {repo_path.name}")

        # Generate README.md
        self.generate_readme(repo_path, force=force)

        # Generate INSTALL.md
        self.generate_install_guide(repo_path, force=force)

        # Generate CHANGELOG.md
        self.generate_changelog(repo_path, force=force)

        # Generate PRD.md
        self.generate_prd(repo_path, repo_type, force=force)

        # Create docs/ directory structure
        self.create_docs_structure(repo_path, repo_type)

    def generate_documentation(self, repo_path: Path, doc_type: str, force: bool = False) -> None:
        """Generate a specific type of documentation."""
        generators = {
            "readme": self.generate_readme,
            "install": self.generate_install_guide,
            "changelog": self.generate_changelog,
            "prd": lambda p, f: self.generate_prd(p, "mcp-server", f),
            "api": lambda p, f: self.generate_api_docs(p, f)
        }

        if doc_type in generators:
            generators[doc_type](repo_path, force)
        else:
            raise ValueError(f"Unknown documentation type: {doc_type}")

    def generate_readme(self, repo_path: Path, force: bool = False) -> None:
        """Generate README.md file."""
        readme_path = repo_path / "README.md"

        if readme_path.exists() and not force:
            self.logger.info("README.md already exists, skipping")
            return

        repo_name = repo_path.name
        project_description = self._infer_project_description(repo_path)

        readme_content = f"""# {repo_name}

{project_description}

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run the application
python -m {repo_name.replace('-', '_')}
```

## Status

### ✅ Tested and Working
- Basic functionality implemented and tested

### 🟡 Implemented but Untested
- Advanced features (testing pending)

### 🔄 Planned
- Additional features in future releases

## Documentation

- [Installation Guide](./INSTALL.md) - Detailed setup instructions
- [API Documentation](./docs/api/) - Complete API reference
- [Contributing Guide](./CONTRIBUTING.md) - How to contribute

## Requirements

- Python 3.10+
- See [INSTALL.md](./INSTALL.md) for detailed requirements

## License

MIT License - see [LICENSE](LICENSE) file for details.
"""

        readme_path.write_text(readme_content, encoding='utf-8')
        self.logger.info(f"Generated README.md for {repo_name}")

    def generate_install_guide(self, repo_path: Path, force: bool = False) -> None:
        """Generate INSTALL.md file."""
        install_path = repo_path / "INSTALL.md"

        if install_path.exists() and not force:
            self.logger.info("INSTALL.md already exists, skipping")
            return

        repo_name = repo_path.name

        install_content = f"""# Installation Guide

This guide covers installing {repo_name} for development and production use.

## Prerequisites

### System Requirements
- Operating System: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- Memory: Minimum 4GB RAM, Recommended 8GB+
- Disk Space: 500MB free space
- Network: Internet connection for dependency downloads

### Python Requirements
- Python 3.10 or higher
- pip 20.0+ or poetry for dependency management

## Quick Install (Recommended)

### Using pip
```bash
# Install from source
pip install -e .
```

### Using poetry (Development)
```bash
# Install with poetry
poetry install

# Activate virtual environment
poetry shell
```

## Detailed Installation

### From Source
```bash
# Clone repository
git clone https://github.com/org/{repo_name}.git
cd {repo_name}

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -e .
```

### Development Setup
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests to verify installation
pytest tests/

# Run linting
ruff check .
```

## Platform-Specific Instructions

### Windows
```powershell
# PowerShell installation
pip install -e .

# If you encounter permission errors
pip install --user -e .
```

### macOS
```bash
# Using pip
pip install -e .
```

### Linux (Ubuntu/Debian)
```bash
# Install Python if needed
sudo apt install python3 python3-pip

# Install project
pip install -e .
```

## Troubleshooting Installation

### Common Issues

#### Permission Denied
```bash
# Don't use sudo with pip
# Instead, use --user flag or virtual environment
pip install --user -e .
```

#### Import Errors After Installation
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall if necessary
pip uninstall {repo_name.replace('-', '_')}
pip install -e .
```

## Post-Installation Verification

### Basic Functionality Test
```python
import {repo_name.replace('-', '_')}

# Test basic import
print("Installation successful")
```

### Run Test Suite
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov={repo_name.replace('-', '_')}
```

## Configuration

### Environment Variables
```bash
# Set required environment variables
export DEBUG=true
```

### Configuration Files
```bash
# Copy example configuration
cp config.example.yaml config.yaml

# Edit configuration
nano config.yaml
```

## Next Steps

After installation, see:
- [Quick Start Guide](./README.md#quick-start) - Basic usage
- [API Documentation](./docs/api/) - Complete API reference
- [Configuration Guide](./docs/configuration.md) - Advanced setup
"""

        install_path.write_text(install_content, encoding='utf-8')
        self.logger.info(f"Generated INSTALL.md for {repo_name}")

    def generate_changelog(self, repo_path: Path, force: bool = False) -> None:
        """Generate CHANGELOG.md file."""
        changelog_path = repo_path / "CHANGELOG.md"

        if changelog_path.exists() and not force:
            self.logger.info("CHANGELOG.md already exists, skipping")
            return

        repo_name = repo_path.name

        changelog_content = f"""# Changelog

All notable changes to {repo_name} will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features that have been added but not yet released

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Any bug fixes

### Security
- Security-related changes

## [0.1.0] - 2024-01-20

### Added
- Initial release
- Basic functionality
- Core API endpoints

### Changed
- Improved error handling

---

## Version Numbering

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes (backward compatible)
"""

        changelog_path.write_text(changelog_content, encoding='utf-8')
        self.logger.info(f"Generated CHANGELOG.md for {repo_name}")

    def generate_prd(self, repo_path: Path, repo_type: str, force: bool = False) -> None:
        """Generate PRD.md file."""
        prd_path = repo_path / "PRD.md"

        if prd_path.exists() and not force:
            self.logger.info("PRD.md already exists, skipping")
            return

        repo_name = repo_path.name

        prd_content = f"""# Product Requirements Document

## Overview
Brief description of {repo_name} and its purpose.

## Problem Statement
What problem does this solve? Who has this problem?

## Target Audience
Who will use this product? What are their needs?

## Success Metrics
How will we measure success?
- User adoption rate
- Performance benchmarks
- Error rates
- User satisfaction scores

## Requirements

### Functional Requirements

#### ✅ Tested and Working
- Basic functionality implemented and tested

#### 🟡 Implemented but Untested
- Advanced features (testing pending)

#### 🔄 Planned
- Future enhancements

### Non-Functional Requirements

#### Performance
- Response time requirements
- Scalability requirements
- Resource usage limits

#### Security
- Authentication requirements
- Data protection standards
- Compliance requirements

## Technical Architecture

### High-Level Design
- System components and their interactions
- Technology stack decisions
- Data flow diagrams

### API Design
- RESTful API endpoints
- Authentication mechanisms
- Rate limiting

## Implementation Plan

### Phase 1 (Current)
- Basic functionality ✅
- Core features implemented 🟡

### Phase 2 (Next)
- Advanced features
- Performance optimization

### Phase 3 (Future)
- Enterprise features
- Advanced analytics

## Risks and Mitigations
- Risk: Technical challenges
  - Mitigation: Prototyping and testing

## Testing Strategy
- Unit tests for all modules
- Integration tests for API endpoints
- End-to-end tests for critical user flows

## Timeline
- Phase 1: Current
- Phase 2: Next 3 months
- Phase 3: 6+ months

## Conclusion
Summary of the product vision and next steps.
"""

        prd_path.write_text(prd_content, encoding='utf-8')
        self.logger.info(f"Generated PRD.md for {repo_name}")

    def create_docs_structure(self, repo_path: Path, repo_type: str) -> None:
        """Create docs/ directory structure."""
        docs_dir = repo_path / "docs"
        docs_dir.mkdir(exist_ok=True)

        # Create subdirectories
        subdirs = ["api", "integrations", "development", "examples"]
        for subdir in subdirs:
            (docs_dir / subdir).mkdir(exist_ok=True)

        # Create basic index file
        index_content = f"""# Documentation

Welcome to the {repo_path.name} documentation.

## Getting Started

- [Installation Guide](../INSTALL.md)
- [Quick Start Guide](../README.md#quick-start)
- [Contributing Guide](../CONTRIBUTING.md)

## API Documentation

- [API Reference](./api/)
- [Integration Guides](./integrations/)

## Development

- [Development Guide](./development/)
- [Code Examples](./examples/)
"""

        (docs_dir / "README.md").write_text(index_content, encoding='utf-8')
        self.logger.info(f"Created docs/ structure for {repo_path.name}")

    def generate_api_docs(self, repo_path: Path, force: bool = False) -> None:
        """Generate API documentation."""
        api_dir = repo_path / "docs" / "api"
        api_dir.mkdir(exist_ok=True)

        # Generate basic API docs
        api_readme = api_dir / "README.md"
        if not api_readme.exists() or force:
            api_content = f"""# API Documentation

## Overview
API documentation for {repo_path.name}.

## Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{{
  "status": "healthy",
  "version": "1.0.0"
}}
```

### GET /api/v1/status
Get system status.

**Response:**
```json
{{
  "status": "operational",
  "uptime": 3600
}}
```
"""
            api_readme.write_text(api_content, encoding='utf-8')
            self.logger.info("Generated API documentation")

    def _infer_project_description(self, repo_path: Path) -> str:
        """Infer project description from available files."""
        # Try to read from pyproject.toml
        pyproject_path = repo_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomli
                with open(pyproject_path, 'rb') as f:
                    data = tomli.load(f)
                description = data.get('project', {}).get('description', '')
                if description:
                    return description
            except Exception:
                pass

        # Default description
        repo_name = repo_path.name
        return f"{repo_name} - An MCP (Model Context Protocol) server implementation."