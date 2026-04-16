# PyWinAuto MCP - Project Status

**Last Updated:** 2025-11-29  
**Version:** 0.3.0 (Portmanteau Edition)  
**Repository:** [github.com/sandraschi/pywinauto-mcp](https://github.com/sandraschi/pywinauto-mcp)  
**Status:** âœ… Production Ready

---

## Overview

PyWinAuto MCP is a FastMCP 3.1.1+.1 compliant server providing **programmatic control of the Windows desktop** through the Model Context Protocol. It enables AI agents (Claude, etc.) to see, interact with, and automate any Windows application.

### Core Capabilities

- **Desktop Visibility**: List windows, read UI elements, extract text via OCR
- **UI Interaction**: Click buttons, type text, navigate menus, fill forms
- **Window Management**: Position, resize, minimize, maximize windows
- **Visual Intelligence**: Screenshots, OCR text extraction, template matching
- **Face Recognition**: Biometric security for sensitive automation workflows
- **System Utilities**: Clipboard operations, process listing, health checks

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.3.0 | 2025-11-29 | Portmanteau Edition - consolidated 60+ tools to 8 |
| 0.2.x | 2025-10 | Individual tools, tool explosion issues |
| 0.1.x | 2025-09 | Initial release |

---

## Portmanteau Architecture

### Why Portmanteau?

The previous architecture had **60+ individual tools** scattered across multiple files with duplicates. This caused:
- Tool explosion overwhelming Claude/users
- Cognitive overload when discovering capabilities
- Duplicate functionality across files
- Import pattern inconsistencies

### The Solution: 8 Comprehensive Tools

| Tool | Operations | Purpose |
|------|------------|---------|
| `automation_windows` | 11 | Window management (list, find, position, etc.) |
| `automation_elements` | 14 | UI element interaction (click, text, wait, etc.) |
| `automation_mouse` | 9 | Mouse control (move, click, scroll, drag) |
| `automation_keyboard` | 4 | Keyboard input (type, press, hotkey) |
| `automation_visual` | 4 | Vision/OCR (screenshot, extract_text, find_image) |
| `automation_face` | 5 | Face recognition (add, recognize, list, delete) |
| `automation_system` | 7 | System utilities (health, clipboard, processes) |
| `get_desktop_state` | 1 | Comprehensive UI element discovery |

**Result:** Same 60+ operations, but exposed through 8 clean tools.

---

## Tool Quick Reference

### automation_windows
```python
automation_windows("list")                                    # List all windows
automation_windows("find", title="Notepad", partial=True)     # Find window
automation_windows("maximize", handle=12345)                  # Maximize
automation_windows("position", handle=12345, x=0, y=0, width=1920, height=1080)
```

### automation_elements
```python
automation_elements("click", window_handle=12345, control_id="Button1")
automation_elements("set_text", window_handle=12345, control_id="Edit1", text="Hello")
automation_elements("wait", window_handle=12345, control_id="Loading", timeout=10.0)
```

### automation_mouse
```python
automation_mouse("position")                     # Get cursor position
automation_mouse("click", x=500, y=300)          # Click at position
automation_mouse("drag", x=100, y=100, target_x=500, target_y=300)
```

### automation_keyboard
```python
automation_keyboard("type", text="Hello World!")
automation_keyboard("hotkey", keys=["ctrl", "c"])  # Copy
automation_keyboard("hotkey", keys=["alt", "f4"])  # Close window
```

### automation_visual
```python
automation_visual("screenshot")                              # Full screen
automation_visual("screenshot", window_handle=12345)         # Window only
automation_visual("extract_text", image_path="screen.png")   # OCR
```

### automation_face
```python
automation_face("add", name="admin", image_path="photo.jpg")
automation_face("recognize", image_path="unknown.jpg")
```

### automation_system
```python
automation_system("health")
automation_system("clipboard_get")
automation_system("clipboard_set", text="Copied text")
```

### get_desktop_state
```python
get_desktop_state()                                    # Basic UI tree
get_desktop_state(use_vision=True, use_ocr=True)       # Full analysis
```

---

## Use Cases

### 1. Desktop Discovery
Claude can enumerate all windows and UI elements, answering "What's open on my desktop?"

### 2. Application Automation
Automate any Windows application: fill forms, click buttons, navigate menus.

### 3. Cross-Application Workflows
Copy data between apps, generate reports spanning multiple applications.

### 4. Accessibility Testing
Deep UI inspection to audit accessibility compliance.

### 5. Face-Gated Security
Require face recognition before sensitive automation operations.

---

## Dependencies

### Core (Required)
- `fastmcp>=3.1.1+.1,<3.0.0`
- `pywinauto>=0.6.8`
- `pillow>=10.0.0`

### Optional Features
- `pytesseract>=0.3.10` - OCR text extraction
- `face-recognition>=1.3.0` - Face recognition
- `opencv-python>=4.8.0` - Visual operations

---

## Configuration

### Claude Desktop
```json
{
  "mcpServers": {
    "pywinauto": {
      "command": "python",
      "args": ["-m", "pywinauto_mcp"],
      "cwd": "D:\\Dev\\repos\\pywinauto-mcp"
    }
  }
}
```

### Environment Variables
```ini
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
TIMEOUT=10.0
FACE_RECOGNITION_TOLERANCE=0.6
```

---

## Known Limitations

1. **Windows Only** - No macOS/Linux support (PyWinAuto is Windows-specific)
2. **Elevated Apps** - UAC-elevated applications require elevated MCP server
3. **DRM Content** - Some apps block UI automation APIs
4. **Games** - Most games block input simulation

---

## Development Status

| Component | Status |
|-----------|--------|
| Portmanteau Tools | âœ… Complete |
| FastMCP 3.1.1+.1 | âœ… Compliant |
| Unit Tests | ðŸŸ¡ Needs migration to portmanteau |
| Documentation | âœ… Complete |
| Glama.ai Gold | ðŸŸ¡ Pending rescan |

---

## Links

- [Repository](https://github.com/sandraschi/pywinauto-mcp)
- [Usage Scenarios](../../../pywinauto-mcp/docs/USAGE_SCENARIOS.md)
- [Portmanteau Pattern](../../patterns/PORTMANTEAU_CONCEPT.md)

---

*Part of the MCP Central Docs project documentation.*


