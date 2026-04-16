# WinRAR MCP

[![Status](https://img.shields.io/badge/status-Beta-yellow.svg)](https://github.com/sandraschi/winrar-mcp)
[![Operating System](https://img.shields.io/badge/OS-Windows-blue.svg)](https://github.com/sandraschi/winrar-mcp)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![MCP Version](https://img.shields.io/badge/MCP-2.14.1-blue)](https://mcp-standard.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1-green.svg)](https://github.com/PrefectHQ/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A FastMCP 3.1 server that provides programmatic access to **WinRAR functionality**.

> ** Windows-Only**: This MCP server requires WinRAR and is designed exclusively for Windows environments.

**Status: Beta - Windows Archive Management (v0.3.1)**

## Features

- Create, extract, and manage RAR/ZIP archives
- Support for password protection and encryption
- File compression with various algorithms and levels
- **Advanced Analysis & Intelligence:**
  - Compression efficiency analysis across algorithms
  - Batch operations with parallel processing
  - Archive comparison and diff analysis
  - Intelligent backup with versioning/retention
  - Archive health monitoring and repair
  - Secure file operations and wiping
- Batch processing of archive operations
- Repository archiving with automatic exclusions
- Self-extracting executable creation
- Progress tracking and notifications
- DXT package for easy deployment and integration

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 (Windows-only due to WinRAR dependency)
- **Python**: 3.8+
- **WinRAR**: Must be installed and available in system PATH
- **Optional**: Virtual environment (recommended)

##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx winrar-mcp
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "winrar-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/winrar-mcp", "run", "winrar-mcp"]
  }
}
```

### Option 1: For Cursor IDE

**Important:** Cursor uses system Python. Install dependencies in the Python that Cursor uses:

```powershell
# Find system Python path (check Cursor error logs if needed)
# Example: C:\Users\sandr\AppData\Local\Programs\Python\Python310\python.exe
python -m uv pip install -r requirements.txt
python -m uv pip install -e .
```

See `CURSOR_SETUP.md` for detailed Cursor configuration instructions.

### Option 2: npm/npx (Recommended for Claude Desktop)

Install via npm for easy access:

```powershell
# Install globally
npm install -g @sandraschi/winrar-mcp

# Or use npx (no installation needed)
npx @sandraschi/winrar-mcp
```

**Note:** Python 3.8+ and WinRAR must be installed separately. The npm package will check for Python during installation.

### Option 3: From Source

1. Clone the repository:

   ```powershell
   git clone https://github.com/sandraschi/winrar-mcp.git
   cd winrar-mcp
   ```

2. Create and activate a virtual environment (recommended):

   ```powershell
   uv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   uv pip install -e .[dev]
   ```

### Option 4: DXT Package

1. Install the DXT CLI:

   ```bash
   npm install -g @anthropic/dxt
   ```

2. Install the WinRAR MCP package:

   ```bash
   dxt install path/to/winrarmcp-0.1.0.dxt
   ```

3. Start the server:

   ```bash
   dxt start winrarmcp
   ```

## Configuration

Copy `.env.example` to `.env` and update the settings:

```ini
# WinRAR MCP Configuration
WINRAR_PATH=C:\\Program Files\\WinRAR\\WinRAR.exe
DEFAULT_COMPRESSION_LEVEL=5  # 0-5 (0=store, 1=fastest, 3=fast, 5=normal, 7=maximum, 9=ultra)
DEFAULT_METHOD=RAR5          # RAR, RAR4, RAR5, ZIP
LOG_LEVEL=INFO
HOST=0.0.0.0
PORT=8000
```

## Usage

### Running the Server

Backend (FastAPI + MCP at `/mcp`, FastMCP 3.1):

```powershell
uv run uvicorn winrarmcp.server:app --host 127.0.0.1 --port 8000 --reload
```

Or from the app module: `uv run uvicorn winrarmcp.main:app --host 127.0.0.1 --port 8000 --reload`.
MCP HTTP transport is mounted at `/mcp`; use that path for MCP clients.

### Example API Requests

Create a new archive:

```http
POST /api/v1/archive/create
Content-Type: application/json

{
  "files": ["path/to/file1.txt", "path/to/file2.txt"],
  "archive_path": "output.rar",
  "password": "secure123",
  "compression_level": 5,
  "method": "RAR5"
}
```

Extract an archive:

```http
POST /api/v1/archive/extract
Content-Type: application/json

{
  "archive_path": "archive.rar",
  "output_dir": "extracted_files",
  "password": "secure123"
}
```

## DXT Packaging

To create a DXT package:

1. Install required tools:

   ```powershell
   # Install 7-Zip if not already installed
   # Download from https://www.7-zip.org/
   ```

2. Run the packaging script:

   ```powershell
   .\package_dxt.ps1
   ```

3. The package will be created in the `dist` directory.

For detailed DXT package documentation, see [DXT_README.md](DXT_README.md).

## Development

### Setting Up Development Environment

#### Quick Setup (Recommended)

**Windows:**
```powershell
.\scripts\setup_dev_env.ps1
```

**Linux/Mac:**
```bash
./scripts/setup_dev_env.sh
```

This will install all development dependencies and set up pre-commit hooks.

#### Manual Setup

1. Install development dependencies:
```powershell
pip install -e ".[dev]"
```

2. Install pre-commit hooks:
```powershell
pre-commit install
pre-commit install --hook-type commit-msg
```

### Code Quality Tools

#### Linting and Formatting
```powershell
# Check code quality
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/

# Format code
ruff format src/ tests/
```

#### Type Checking
```powershell
mypy src/ --ignore-missing-imports
```

#### Security Scanning
```powershell
# Install security tools
pip install bandit safety

# Run security scans
bandit -r src/
safety check
```

### Running Tests

It is recommended to use the `just` dashboard for test orchestration:

```powershell
# Run all tests via pytest
just test

# Run tests with coverage reporting (HTML output)
just test-cov

# Rerun only failed tests
just test-failed
```

Manual execution:
```powershell
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/winrarmcp --cov-report=html

# Run specific test
pytest tests/test_archive_service.py -v
```

### Pre-commit Hooks

Pre-commit hooks automatically run on every commit to ensure code quality:

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **Bandit**: Security scanning
- **Safety**: Dependency vulnerability checking
- **Import sorting**: Keep imports organized
- **Large file check**: Prevent committing large files

To run pre-commit manually:
```powershell
pre-commit run --all-files
```

## CI/CD

This project uses GitHub Actions for continuous integration and deployment.

### CI Pipeline

The CI pipeline runs on every push and pull request and includes:

1. **Code Quality Checks** (Ubuntu):
   - Ruff formatting and linting
   - MyPy type checking

2. **Testing** (Windows):
   - Tests across Python 3.10, 3.11, 3.12
   - Coverage reporting

3. **Security Scanning** (Ubuntu):
   - Bandit security analysis
   - Safety dependency vulnerability checks

### Release Process

Releases are automatically created when you push a version tag:

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

This triggers:
- Automated testing and quality checks
- Package building and PyPI publishing
- GitHub release creation

### Branch Protection

The `main`/`master` branch has branch protection rules requiring:
- All CI checks to pass
- At least one reviewer approval for pull requests
- Linear history (no merge commits)

## License

MIT


## Webapp Dashboard

Functional web interface for archive management. Ports: **10762** = backend (Starlette), **10763** = frontend (Vite).

### Pages

| Page | What it does |
|------|-------------|
| Dashboard | Live health check, job counters, quick-nav |
| Repo Archiver | Scans repos root, reads `.gitignore` → WinRAR exclusions, async archive jobs |
| Archive Browser | List / info / test / extract any archive by path |
| Compression Lab | Runs RAR5 m1/m3/m5 analysis, shows bar chart + best recommendation |
| Jobs | Auto-refreshing job list with result detail |
| Status | Backend health, env var docs |
| **Testing** | Modular orchestration via `just test` / `just test-cov` |

### Start

```powershell
cd D:\Dev\repos\winrar-mcp\webapp
.\start.ps1
```

Script kills port zombies, creates venv, installs Python + npm deps, waits for backend health, opens browser.

### Environment overrides

| Variable | Default |
|----------|---------|
| `REPOS_ROOT` | `D:\Dev\repos` |
| `WINRAR_PATH` | `C:\Program Files\WinRAR\Rar.exe` |
| `UNRAR_PATH` | `C:\Program Files\WinRAR\UnRAR.exe` |
| `OUTPUT_DIR` | `D:\Dev\repos\temp` |
