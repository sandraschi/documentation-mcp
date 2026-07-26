# Windows Computer Use MCP - Project Structure

**Version:** 0.3.0 (Portmanteau Edition)

---

## Repository Layout

```
windows-computer-use-mcp/
â”œâ”€â”€ src/
â”‚   â””â”€â”€ pywinauto_mcp/
â”‚       â”œâ”€â”€ __init__.py           # Package initialization
â”‚       â”œâ”€â”€ app.py                # FastMCP app instance
â”‚       â”œâ”€â”€ main.py               # Entry point
â”‚       â”œâ”€â”€ tools/
â”‚       â”‚   â”œâ”€â”€ __init__.py       # Tool registration
â”‚       â”‚   â”œâ”€â”€ portmanteau_windows.py     # Window management (11 ops)
â”‚       â”‚   â”œâ”€â”€ portmanteau_elements.py    # UI elements (14 ops)
â”‚       â”‚   â”œâ”€â”€ portmanteau_mouse.py       # Mouse control (9 ops)
â”‚       â”‚   â”œâ”€â”€ portmanteau_keyboard.py    # Keyboard input (4 ops)
â”‚       â”‚   â”œâ”€â”€ portmanteau_visual.py      # Vision/OCR (4 ops)
â”‚       â”‚   â”œâ”€â”€ portmanteau_face.py        # Face recognition (5 ops)
â”‚       â”‚   â”œâ”€â”€ portmanteau_system.py      # System utilities (7 ops)
â”‚       â”‚   â”œâ”€â”€ desktop_state.py           # Desktop state (standalone)
â”‚       â”‚   â””â”€â”€ archived/                  # Legacy individual tools
â”‚       â”‚       â”œâ”€â”€ basic_tools.py
â”‚       â”‚       â”œâ”€â”€ element_tools.py
â”‚       â”‚       â”œâ”€â”€ element.py
â”‚       â”‚       â”œâ”€â”€ face_recognition.py
â”‚       â”‚       â”œâ”€â”€ input.py
â”‚       â”‚       â”œâ”€â”€ mouse.py
â”‚       â”‚       â”œâ”€â”€ system_tools.py
â”‚       â”‚       â”œâ”€â”€ visual_tools.py
â”‚       â”‚       â”œâ”€â”€ visual.py
â”‚       â”‚       â””â”€â”€ window.py
â”‚       â””â”€â”€ desktop_state/        # Desktop state submodule
â”‚           â”œâ”€â”€ __init__.py
â”‚           â”œâ”€â”€ walker.py         # UI tree walker
â”‚           â”œâ”€â”€ formatter.py      # Output formatter
â”‚           â””â”€â”€ visual_state.py   # Visual state assessor
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ USAGE_SCENARIOS.md        # Comprehensive usage guide
â”‚   â”œâ”€â”€ STATUS_REPORT.md          # Current project status
â”‚   â”œâ”€â”€ desktop-state-tool.md     # Desktop state documentation
â”‚   â”œâ”€â”€ development/              # Dev guides
â”‚   â”œâ”€â”€ glama-platform/           # Glama.ai docs
â”‚   â””â”€â”€ mcp-technical/            # MCP technical docs
â”œâ”€â”€ tests/
â”‚   â””â”€â”€ (unit/integration tests)
â”œâ”€â”€ pyproject.toml               # Project configuration
â”œâ”€â”€ README.md                    # Main readme
â”œâ”€â”€ LICENSE                      # MIT License
â””â”€â”€ .env.example                 # Environment template
```

---

## Key Files

### src/pywinauto_mcp/app.py
Central FastMCP app instance. All tools import from here to avoid circular imports.

```python
from fastmcp import FastMCP

app = FastMCP(
    name="windows-computer-use-mcp",
    version="0.3.0"
)
```

### src/pywinauto_mcp/main.py
Entry point for the MCP server.

```python
def main():
    from pywinauto_mcp.app import app
    import pywinauto_mcp.tools  # Imports register all tools
    app.run()
```

### src/pywinauto_mcp/tools/__init__.py
Tool registration orchestrator. Imports all portmanteau modules which self-register.

```python
TOOL_MODULES = [
    'portmanteau_windows',
    'portmanteau_elements',
    'portmanteau_mouse',
    'portmanteau_keyboard',
    'portmanteau_visual',
    'portmanteau_face',
    'portmanteau_system',
    'desktop_state',
]
```

---

## Portmanteau Tool Pattern

Each portmanteau tool follows this structure:

```python
# portmanteau_*.py

from typing import Literal, Optional, Dict, Any
from pywinauto_mcp.app import app

@app.tool(
    name="automation_*",
    description="..."
)
def automation_*(
    operation: Literal["op1", "op2", "op3"],  # Literal for discoverability
    param1: Optional[str] = None,
    param2: Optional[int] = None
) -> Dict[str, Any]:
    """
    Comprehensive docstring documenting ALL operations.
    
    Args:
        operation: Available operations:
            - op1: Description
            - op2: Description
            - op3: Description
        param1: Parameter description
        param2: Parameter description
        
    Returns:
        Operation result with status
    """
    if operation == "op1":
        # Handle op1
        pass
    elif operation == "op2":
        # Handle op2
        pass
    # ...
```

---

## Archived Tools

The `archived/` directory contains the original individual tool implementations from v0.2.x. These are preserved for:

1. **Reference** - Understanding the original implementation
2. **Testing** - Direct function calls without MCP wrapper
3. **Migration** - Gradual transition if needed

The archived tools are NOT registered with the MCP server.

---

## Desktop State Module

The `desktop_state/` submodule provides comprehensive UI element discovery:

```
desktop_state/
â”œâ”€â”€ __init__.py        # Exports get_desktop_state tool
â”œâ”€â”€ walker.py          # UIElementWalker - traverses UI tree
â”œâ”€â”€ formatter.py       # Formats output for readability
â””â”€â”€ visual_state.py    # VisualStateAssessor - vision/OCR
```

This remains standalone (not portmanteau) because:
- Single, complex operation
- Already comprehensive
- No related operations to consolidate

---

## Configuration Files

### pyproject.toml
```toml
[project]
name = "windows-computer-use-mcp"
version = "0.3.0"
dependencies = [
    "fastmcp>=3.1.1+.1,<3.0.0",
    "pywinauto>=0.6.8",
    "pillow>=10.0.0",
]

[project.optional-dependencies]
ocr = ["pytesseract>=0.3.10"]
face = ["face-recognition>=1.3.0", "opencv-python>=4.8.0"]
all = ["pytesseract>=0.3.10", "face-recognition>=1.3.0", "opencv-python>=4.8.0"]

[project.scripts]
windows-computer-use-mcp = "pywinauto_mcp.main:main"
```

### .env (example)
```ini
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
TIMEOUT=10.0
FACE_RECOGNITION_TOLERANCE=0.6
FACE_RECOGNITION_MODEL=hog
SCREENSHOT_DIR=./screenshots
```

---

## Import Flow

```
main.py
    â””â”€â”€ app.py (FastMCP instance)
    â””â”€â”€ tools/__init__.py
        â””â”€â”€ portmanteau_windows.py â†’ imports app from app.py
        â””â”€â”€ portmanteau_elements.py â†’ imports app from app.py
        â””â”€â”€ portmanteau_mouse.py â†’ imports app from app.py
        â””â”€â”€ portmanteau_keyboard.py â†’ imports app from app.py
        â””â”€â”€ portmanteau_visual.py â†’ imports app from app.py
        â””â”€â”€ portmanteau_face.py â†’ imports app from app.py
        â””â”€â”€ portmanteau_system.py â†’ imports app from app.py
        â””â”€â”€ desktop_state.py â†’ imports app from app.py
```

All tools import the app instance from `app.py` to avoid circular imports.

---

## Development

### Running Locally
```powershell
cd D:\Dev\repos\windows-computer-use-mcp
python -m pywinauto_mcp
```

### Running Tests
```powershell
pytest tests/
```

### Verifying Imports
```powershell
python -c "from pywinauto_mcp.app import app; from pywinauto_mcp import tools; print('OK')"
```

---

*Part of the MCP Central Docs project documentation.*


