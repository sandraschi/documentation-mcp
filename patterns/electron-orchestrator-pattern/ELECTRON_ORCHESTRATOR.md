# ⚛️ Electron Orchestrator Pattern

**Location:** `patterns/electron-orchestrator-pattern/`  
**Purpose:** Strategy for using Electron's Main Process to manage and orchestrate background AI services (Python, C++ binaries) while providing a premium desktop frontend.

---

## 🧐 The "Fashionable" Problem
Many modern AI/MCP projects rely on a multi-stack approach:
- **Backend**: Python (FastAPI/Aiohttp) serving game engines or OCR models.
- **Frontend**: Web-based dashboards (React/Vue/Vanilla).
- **Tooling**: Bash or PowerShell scripts to start everything.

**The result?** A "cluttered terminal" UX where users have to see and manage background process windows.

---

## 🚀 The Solution: The Electron Orchestrator
The **Electron Orchestrator** pattern moves the responsibility of process management from the user's terminal to the **Electron Main Process (Node.js)**.

### **Core Tenets:**
1. ✅ **Zero-Terminal UX**: Background processes are spawned with `windowsHide: true`.
2. ✅ **Lifecycle Synergy**: Processes are born with the app and DIE with the app (no orphaned `python.exe`).
3. ✅ **Integrated Health**: The app can poll background ports and show status (Green/Yellow/Red) without user intervention.
4. ✅ **Premium Desktop Feeling**: A dedicated `.exe` with native window management, system tray, and notifications.

---

## 🛠️ Implementation Blueprint

### **1. Directory Structure (Monorepo)**
```
project-root/
├── electron/           # The orchestrator shell
│   ├── main.js         # Logic: spawn() + monitor()
│   └── package.json    # Electron & packaging deps
├── backend/            # The heavy lifting (Python/C++/etc.)
└── frontend/           # The UI (served by backend or local files)
```

### **2. The Master Setup (Node.js `spawn`)**
The orchestrator uses `child_process.spawn` to manage the stack:
```javascript
// electron/main.js
const { spawn } = require('child_process');

function spawnService(script, name) {
  const proc = spawn('python', [script], { 
      windowsHide: true,
      stdio: 'pipe' 
  });
  
  proc.stdout.on('data', d => console.log(`[${name}] ${d}`));
  return proc;
}

// Lifecycle: Kill all on exit
app.on('window-all-closed', () => {
    activeProcs.forEach(p => p.kill());
    app.quit();
});
```

---

## 🌟 Case Studies

### **🎮 Games Collection (The Reference Implementation)**
Originally a browser-only suite, the Games Collection uses this pattern to:
- Simultaneously spawn **Stockfish**, **KataGo**, and **YaneuraOu**.
- Launch the main **Web Server**.
- Provide a unified desktop window with no visible Python consoles.

### **📷 OCR App (Future Profiteer)**
Instead of making the user run an OCR server manually, a "ScanApp" can:
2. Spawn the Tesseract/PyTorch backend on launch.
3. Open a "Scanning Portal" window.
4. Kill the heavy AI models instantly when the window is closed to free up RAM.

---

## 🎓 Why This Matters for 2026 SOTA
In the agentic era, we often focus on the "Brain" (MCP). But for a **Product** to feel premium, the "Body" (UI/UX) must be friction-less. The Electron Orchestrator pattern provides that bridge for specialized AI applications.

---

## 🏷️ Tags
`electron` `orchestration` `process-management` `mcp-ux` `desktop-shell` `vienna-technical-standards`
