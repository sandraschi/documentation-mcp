# MCP Deeplink Installation - Portfolio Standard

**Status**: MANDATORY for all MCP repositories  
**Effective**: 2025-10-28  
**Reference Implementation**: advanced-memory-mcp v1.0.0b6  
**Priority**: HIGH

## Overview

All MCP repositories MUST implement one-click deeplink installation to provide professional user experience and reduce installation friction from minutes to seconds.

## Standard Requirements

### 1. Supported Clients (Minimum)

**REQUIRED**:
- ✅ Cursor IDE
- ✅ VS Code

**OPTIONAL** (recommended):
- Claude Desktop (config generator)
- Windsurf (when available)
- Other MCP-compatible clients

### 2. Implementation Files

#### New Files Required (5)

```
src/{package}/utils/deeplink_generator.py       # Core deeplink logic
src/{package}/cli/commands/deeplink.py          # CLI deeplink command
src/{package}/cli/commands/setup.py             # Interactive setup wizard
tests/utils/test_deeplink_generator.py          # Comprehensive tests
docs/user-guide/DEEPLINK_INSTALLATION.md        # User documentation
```

#### Modified Files Required (3)

```
src/{package}/cli/commands/__init__.py          # Add deeplink, setup imports
README.md                                        # Add one-click installation section
CHANGELOG.md or release notes                    # Document new feature
```

### 3. Deeplink Format Specification

#### Cursor IDE Format
```
cursor://settings/mcp?name={name}&config={base64_config}
```

**Parameters**:
- `name`: Package name (e.g., "advanced-memory")
- `config`: Base64-encoded JSON configuration

**Example Config**:
```json
{
  "command": "uv",
  "args": [
    "--directory",
    "C:\\Users\\{user}\\AppData\\Local\\Programs\\advanced-memory-mcp",
    "run",
    "advanced-memory",
    "mcp"
  ]
}
```

#### VS Code Format
```
vscode://user/settings?path={path}
```

**Path**: System-specific path to VS Code settings file

**Note**: VS Code requires file write + manual restart (less seamless than Cursor)

### 4. Code Template

#### deeplink_generator.py Template

```python
'''Deeplink generation for MCP client configuration.'''

import base64
import json
import platform
from pathlib import Path
from typing import Dict, Optional


def get_package_install_location() -> Path:
    '''Get the installation location for the package.'''
    if platform.system() == 'Windows':
        appdata = Path.home() / 'AppData' / 'Local' / 'Programs'
        return appdata / 'YOUR-PACKAGE-mcp'
    else:
        return Path.home() / '.local' / 'share' / 'YOUR-PACKAGE-mcp'


def generate_cursor_deeplink(
    package_name: str = 'YOUR-PACKAGE',
    install_path: Optional[Path] = None,
) -> str:
    '''Generate a Cursor IDE deeplink for one-click installation.'''
    if install_path is None:
        install_path = get_package_install_location()
    
    config = {
        'command': 'uv',
        'args': [
            '--directory',
            str(install_path),
            'run',
            package_name,
            'mcp',
        ],
    }
    
    config_json = json.dumps(config)
    config_b64 = base64.urlsafe_b64encode(config_json.encode()).decode()
    
    return f'cursor://settings/mcp?name={package_name}&config={config_b64}'


def generate_vscode_config(
    package_name: str = 'YOUR-PACKAGE',
    install_path: Optional[Path] = None,
) -> Dict:
    '''Generate VS Code MCP configuration.'''
    if install_path is None:
        install_path = get_package_install_location()
    
    return {
        'mcpServers': {
            package_name: {
                'command': 'uv',
                'args': [
                    '--directory',
                    str(install_path),
                    'run',
                    package_name,
                    'mcp',
                ],
            },
        },
    }


def decode_cursor_deeplink(deeplink: str) -> Dict:
    '''Decode a Cursor deeplink to extract configuration.'''
    if not deeplink.startswith('cursor://settings/mcp?'):
        raise ValueError('Invalid Cursor deeplink format')
    
    # Parse query parameters
    query = deeplink.split('?')[1]
    params = {}
    for param in query.split('&'):
        key, value = param.split('=')
        params[key] = value
    
    # Decode config
    config_b64 = params.get('config', '')
    config_json = base64.urlsafe_b64decode(config_b64).decode()
    config = json.loads(config_json)
    
    return {
        'name': params.get('name'),
        'config': config,
    }
```

### 5. CLI Command Template

#### deeplink.py Template

```python
'''CLI command for generating deeplinks.'''

import typer
from rich.console import Console
from rich.panel import Panel

from YOUR_PACKAGE.utils.deeplink_generator import (
    generate_cursor_deeplink,
    generate_vscode_config,
)

app = typer.Typer()
console = Console()


@app.command()
def deeplink(
    client: str = typer.Argument(
        'cursor',
        help='AI client: cursor, vscode, claude',
    ),
):
    '''Generate deeplink for one-click installation.'''
    
    if client.lower() == 'cursor':
        link = generate_cursor_deeplink()
        console.print(Panel(
            f'[bold cyan]Cursor IDE One-Click Install[/bold cyan]\n\n'
            f'Click this link:\n{link}\n\n'
            f'Or run: cursor://settings/mcp?...',
            title='Cursor Deeplink',
        ))
    
    elif client.lower() == 'vscode':
        config = generate_vscode_config()
        console.print(Panel(
            f'[bold cyan]VS Code Configuration[/bold cyan]\n\n'
            f'{json.dumps(config, indent=2)}',
            title='VS Code Config',
        ))
    
    else:
        console.print(f'[red]Unknown client: {client}[/red]')
```

### 6. Testing Requirements

**Minimum 20 Tests Required**:

```python
def test_generate_cursor_deeplink():
    '''Test basic Cursor deeplink generation.'''
    
def test_decode_cursor_deeplink():
    '''Test decoding Cursor deeplinks.'''
    
def test_vscode_config():
    '''Test VS Code config generation.'''
    
def test_windows_path():
    '''Test Windows path handling.'''
    
def test_linux_path():
    '''Test Linux path handling.'''
    
def test_macos_path():
    '''Test macOS path handling.'''
    
# ... 14 more tests for edge cases
```

**Coverage Requirements**:
- ✅ All platforms (Windows, Linux, macOS)
- ✅ All clients (Cursor, VS Code)
- ✅ Edge cases (IPv6, HTTPS, custom paths)
- ✅ Error handling (invalid deeplinks)

### 7. Documentation Requirements

#### README.md Section (Required)

```markdown
### ⚡ One-Click Installation

**Cursor IDE** (Recommended):
```bash
your-package deeplink cursor
```

**VS Code**:
```bash
your-package deeplink vscode
```

**Interactive Setup**:
```bash
your-package setup
```

For detailed installation instructions, see [Installation Guide](user-guide/DEEPLINK_INSTALLATION.md).
```

#### User Guide (Required)

Create `docs/user-guide/DEEPLINK_INSTALLATION.md` with:
- One-click installation instructions
- Manual installation fallback
- Troubleshooting section
- Platform-specific notes

### 8. Quality Standards

#### Code Quality (MANDATORY)
- ✅ Zero ruff errors
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings (FastMCP 3.1 / SOTA style)
- ✅ Windows compatible (no emojis in CLI output)

#### Test Quality (MANDATORY)
- ✅ Minimum 20 tests
- ✅ 100% test pass rate
- ✅ All edge cases covered
- ✅ Platform compatibility verified

#### Documentation Quality (MANDATORY)
- ✅ User installation guide complete
- ✅ README updated with one-click section
- ✅ CLI help text clear and helpful
- ✅ Examples included

## Implementation Checklist

### Phase 1: Setup (5 minutes)
- [ ] Create directory structure
- [ ] Copy template files from advanced-memory-mcp
- [ ] Find-replace package names

### Phase 2: Code (10 minutes)
- [ ] Implement deeplink_generator.py
- [ ] Implement deeplink.py CLI command
- [ ] Implement setup.py wizard
- [ ] Update CLI __init__.py

### Phase 3: Testing (10 minutes)
- [ ] Create test_deeplink_generator.py
- [ ] Run tests: `pytest tests/utils/test_deeplink_generator.py -v`
- [ ] Verify 20+ tests passing
- [ ] Fix any failures

### Phase 4: Documentation (5 minutes)
- [ ] Create DEEPLINK_INSTALLATION.md
- [ ] Update README.md
- [ ] Update CHANGELOG.md
- [ ] Add release notes

### Phase 5: Quality (5 minutes)
- [ ] Run: `ruff check . --fix`
- [ ] Run: `ruff format .`
- [ ] Verify zero errors
- [ ] Test deeplink generation manually

**Total Time**: ~30 minutes per repository

## Automation

### Script: add-deeplinks-to-repo.ps1

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$TargetRepo,
    
    [Parameter(Mandatory=$true)]
    [string]$PackageName,
    
    [Parameter(Mandatory=$true)]
    [string]$PackageTitle
)

# Copy files from reference implementation
$RefRepo = "D:\Dev\repos\advanced-memory-mcp"

# Copy utils
Copy-Item "$RefRepo\src\advanced_memory\utils\deeplink_generator.py" `
          "$TargetRepo\src\$PackageName\utils\"

# Copy CLI commands
Copy-Item "$RefRepo\src\advanced_memory\cli\commands\deeplink.py" `
          "$TargetRepo\src\$PackageName\cli\commands\"
Copy-Item "$RefRepo\src\advanced_memory\cli\commands\setup.py" `
          "$TargetRepo\src\$PackageName\cli\commands\"

# Copy tests
Copy-Item "$RefRepo\tests\utils\test_deeplink_generator.py" `
          "$TargetRepo\tests\utils\"

# Copy docs
Copy-Item "$RefRepo\docs\user-guide\DEEPLINK_INSTALLATION.md" `
          "$TargetRepo\docs\user-guide\"

# Find-replace package names
$files = Get-ChildItem "$TargetRepo\src\$PackageName" -Recurse -File
foreach ($file in $files) {
    (Get-Content $file.FullName) `
        -replace 'advanced-memory', $PackageName `
        -replace 'advanced_memory', ($PackageName -replace '-', '_') `
        -replace 'Advanced Memory', $PackageTitle |
    Set-Content $file.FullName
}

Write-Host "Deeplinks added to $TargetRepo" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update CLI __init__.py imports" -ForegroundColor Cyan
Write-Host "2. Run: ruff check . --fix" -ForegroundColor Cyan
Write-Host "3. Run: pytest tests/utils/test_deeplink_generator.py -v" -ForegroundColor Cyan
Write-Host "4. Update README.md" -ForegroundColor Cyan
```

## Rollout Plan

### Tier 1: Immediate (Week 1)
1. advanced-memory-mcp ✅ (Reference implementation)
2. rtorrent-mcp 📋
3. notepadpp-mcp 📋
4. mcp-studio 📋
5. immich-mcp 📋

### Tier 2: High Priority (Week 2)
6. database-operations-mcp 📋
7. fastsearch-mcp 📋
8. git-mcp 📋
9. filesystem-mcp 📋

### Tier 3: Standard (Weeks 3-4)
10-15. Remaining MCP repositories 📋

**Target**: 100% completion by end of November 2025

## Success Metrics

### User Experience
- Installation time: 5 minutes → 5 seconds (60x faster)
- Success rate: ~60% → >95%
- Support requests: -50%

### Code Quality
- Ruff errors: 0
- Test pass rate: 100%
- Test coverage: 20+ tests per repo

### Documentation
- One-click section in every README
- Complete user guides
- Consistent formatting

### Portfolio
- 15/15 repos with deeplinks
- "One-click install" marketing claim valid
- Professional polish throughout

## Competitive Advantage

### vs Composio Rube
- ✅ Matches one-click installation UX
- ✅ Multiple servers (portfolio advantage)
- ✅ All open source (vs proprietary server)
- ✅ Triple-interface (stdio + HTTP + SSE)

### vs Other MCP Servers
- ✅ Most MCP servers lack deeplinks
- ✅ First portfolio with one-click across ALL servers
- ✅ Professional UX throughout

**Message**: "We set the standard for MCP server installation UX"

## Support & Resources

### Reference Implementation
- **Repository**: advanced-memory-mcp
- **Version**: v1.0.0b6
- **Tag**: v1.0.0b6
- **Files**: `src/advanced_memory/utils/deeplink_generator.py` and related

### Documentation
- **Standard**: This document (mcp-central-docs/DEEPLINK_STANDARD.md)
- **Checklist**: See [Quick Implementation Checklist](#-quick-implementation-checklist-30-minute-guide) below
- **Tracker**: repos/DEEPLINK_ROLLOUT_TRACKER.md

### Help
- Review reference implementation
- Copy template files
- Run automation script
- Test with provided test suite

## Version History

- **v1.0** (2025-10-28): Initial standard created
  - Reference implementation: advanced-memory-mcp v1.0.0b6
  - Status: MANDATORY for all repos
  - Rollout: 4 weeks

---

---

## ⚡ Quick Implementation Checklist (30-Minute Guide)

### 1. Files to Copy from advanced-memory-mcp
```bash
# 1. Deeplink generator
cp advanced-memory-mcp/src/advanced_memory/utils/deeplink_generator.py \
   your-repo/src/{package}/utils/

# 2. Deeplink CLI command
cp advanced-memory-mcp/src/advanced_memory/cli/commands/deeplink.py \
   your-repo/src/{package}/cli/commands/

# 3. Setup wizard
cp advanced-memory-mcp/src/advanced_memory/cli/commands/setup.py \
   your-repo/src/{package}/cli/commands/

# 4. Tests
cp advanced-memory-mcp/tests/utils/test_deeplink_generator.py \
   your-repo/tests/utils/

# 5. Documentation
cp advanced-memory-mcp/docs/user-guide/DEEPLINK_INSTALLATION.md \
   your-repo/docs/user-guide/
```

### 2. Find-Replace
```
advanced-memory → your-package-name
advanced_memory → your_package_name
Advanced Memory → Your Package Name
```

### 3. Update CLI __init__.py
```python
from . import (
    ...,
    deeplink,  # Add
    setup,     # Add
)

__all__ = [
    ...,
    "deeplink",  # Add
    "setup",     # Add
]
```

### 4. Update README.md
```markdown
### ⚡ One-Click Installation

**Cursor IDE** (Recommended):
```bash
your-package deeplink cursor
```

**VS Code**:
```bash
your-package deeplink vscode
```

**Interactive Setup**:
```bash
your-package setup
```
```

### 5. Test & Verify
```bash
# Run tests (expect 20+ passes)
pytest tests/utils/test_deeplink_generator.py -v

# Fix formatting
ruff check . --fix
```

**Time**: 30 minutes | **Impact**: 60x faster user onboarding
