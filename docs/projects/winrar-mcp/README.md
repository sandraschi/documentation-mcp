# WinRAR MCP

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://biomejs.dev"><img src="https://img.shields.io/badge/Linted_with-Biome-60a5fa?style=flat-square&logo=biome&logoColor=white" alt="Biome"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

A FastMCP 3.4.2 server that provides programmatic access to **WinRAR functionality**.

> ** Windows-Only**: This MCP server requires WinRAR and is designed exclusively for Windows environments.

**Status: Beta - Windows Archive Management (v0.3.1)**

## Quick Start

```powershell
git clone https://github.com/sandraschi/winrar-mcp
cd winrar-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

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
- Tauri 2.0 NSIS desktop installer (native/) with embedded backend
- Webapp dashboard (React + Vite + Tailwind) on port 10763
- `/api/v1/diagnostics` endpoint for CUA-NSIS smoke testing
- Tool annotations (READ_ONLY/MUTATING) on all MCP tools
- Dual transport: HTTP (uvicorn on 10762) and stdio (Claude Desktop)

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

**Note:** Python 3.12+ and WinRAR must be installed separately. The npm package will check for Python during installation.

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
DEFAULT_COMPRESSION_LEVEL=5
DEFAULT_METHOD=RAR5
LOG_LEVEL=INFO
HOST=127.0.0.1
PORT=10762
```

> **Security**: `.env` is NEVER bundled in the NSIS installer. Only `.env.example` is shipped.
> First-run setup copies `.env.example` to `%LOCALAPPDATA%\com.sandraschi.winrar-mcp\.env`.

## Usage

### Running the Server

Backend (FastAPI + MCP at `/mcp`, FastMCP 3.4.2, port 10762):

```powershell
just server
```

Or manually:
```powershell
uv run uvicorn winrarmcp.main:app --host 127.0.0.1 --port 10762 --reload
```

MCP HTTP transport is mounted at `/mcp`; use that path for MCP clients.
Stdio mode (for Claude Desktop): `uv run winrar-mcp`

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


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

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
