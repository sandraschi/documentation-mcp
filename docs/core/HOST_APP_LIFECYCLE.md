---
title: "Host App Lifecycle Management Standard"
category: standard
status: active
audience: mcp-dev
skill_candidate: true
related:
  - standards/WEBAPP_SOTA_STANDARDS.md
  - standards/AGENT_PROTOCOLS.md
last_updated: 2026-02-26
---

# Host App Lifecycle Management Standard (v1.0)

**Mandatory pattern for all MCP servers that depend on a host application.**

---

## I. Problem Statement

Approximately 20 servers in this fleet are non-functional if their host application (e.g., DaVinci Resolve, Blender, OBS Studio) is not installed and running. Without this standard, such servers produce cryptic Python import errors or socket timeouts that give the user and AI agents no actionable information.

**This standard mandates** that every host-app-dependent server surface a clear status and provide launch/install affordances at both the MCP tool level and the webapp dashboard level.

---

## II. The Four Application States

Every host-app-dependent server MUST be able to report exactly one of these states:

| State | Meaning | User Action |
|-------|---------|-------------|
| `not_installed` | App binary not found on system | Show download link |
| `installed_stopped` | App found but process not running | Show launch button |
| `running_unreachable` | Process exists but API/socket not ready | Show "wait / retry" |
| `ready` | Process running AND API responding | Normal operation |

---

## III. Mandatory MCP Tools

Every host-app-dependent server MUST expose these two tools:

### `get_host_app_status`
Returns the current state, version (if detectable), PID, install path, download URL, and whether launch is possible.

```json
{
  "state": "installed_stopped",
  "app_name": "DaVinci Resolve",
  "message": "DaVinci Resolve is installed but not running.",
  "pid": null,
  "install_path": "C:/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe",
  "download_url": "https://www.blackmagicdesign.com/products/davinciresolve",
  "can_launch": true
}
```

### `launch_host_app`
Attempts to start the host application. Returns success/failure and guidance.

```json
{
  "success": true,
  "message": "Launch command sent. Allow 10-15 seconds for the app to start."
}
```

---

## IV. Shared Module: `host_app_probe.py`

Each server vendors its own copy of the shared probe module, or imports from a shared package. Location within a server repo:

```
src/<package>/core/host_app_probe.py
```

### Full Implementation

```python
"""
host_app_probe.py - Reusable host application lifecycle probe.
Part of the sandraschi MCP fleet HOST_APP_LIFECYCLE standard v1.0
"""
import socket
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import psutil


class AppState(str, Enum):
    NOT_INSTALLED = "not_installed"
    INSTALLED_STOPPED = "installed_stopped"
    RUNNING_UNREACHABLE = "running_unreachable"
    READY = "ready"


@dataclass
class HostAppStatus:
    state: AppState
    app_name: str
    message: str = ""
    version: Optional[str] = None
    install_path: Optional[Path] = None
    pid: Optional[int] = None
    download_url: str = ""
    launch_cmd: Optional[list] = field(default=None)

    @property
    def can_launch(self) -> bool:
        return self.launch_cmd is not None and self.state == AppState.INSTALLED_STOPPED

    def to_dict(self) -> dict:
        return {
            "state": self.state.value,
            "app_name": self.app_name,
            "message": self.message,
            "version": self.version,
            "install_path": str(self.install_path) if self.install_path else None,
            "pid": self.pid,
            "download_url": self.download_url,
            "can_launch": self.can_launch,
        }


def probe_host_app(
    app_name: str,
    process_names: list[str],
    install_paths: list[Path],
    download_url: str = "",
    launch_cmd: Optional[list] = None,
    check_port: Optional[int] = None,
    http_health_url: Optional[str] = None,
) -> HostAppStatus:
    """
    Probe a host application through the four lifecycle states.
    
    Args:
        app_name: Human-readable app name, e.g. "DaVinci Resolve"
        process_names: List of process name fragments to match, e.g. ["Resolve"]
        install_paths: List of known install executable paths to check
        download_url: Where to download the app if not installed
        launch_cmd: Command list to launch the app, e.g. ["C:/...Resolve.exe"]
        check_port: TCP port to test for API readiness (optional)
        http_health_url: HTTP URL to GET for API readiness check (optional)
    """
    # --- State 1: NOT_INSTALLED ---
    found_path = next((p for p in install_paths if Path(p).exists()), None)
    if not found_path:
        return HostAppStatus(
            state=AppState.NOT_INSTALLED,
            app_name=app_name,
            message=f"{app_name} installation not found on this system.",
            download_url=download_url,
        )

    # --- State 2: INSTALLED_STOPPED ---
    pid = None
    for proc in psutil.process_iter(["name", "pid"]):
        try:
            if any(pn.lower() in proc.info["name"].lower() for pn in process_names):
                pid = proc.info["pid"]
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if pid is None:
        return HostAppStatus(
            state=AppState.INSTALLED_STOPPED,
            app_name=app_name,
            message=f"{app_name} is installed but not running.",
            install_path=Path(found_path),
            download_url=download_url,
            launch_cmd=launch_cmd,
        )

    # --- State 3: RUNNING_UNREACHABLE ---
    if check_port is not None:
        try:
            s = socket.create_connection(("127.0.0.1", check_port), timeout=1.5)
            s.close()
        except OSError:
            return HostAppStatus(
                state=AppState.RUNNING_UNREACHABLE,
                app_name=app_name,
                message=f"{app_name} is running (PID {pid}) but API port {check_port} is not responding yet.",
                install_path=Path(found_path),
                pid=pid,
            )

    if http_health_url is not None:
        try:
            import httpx
            r = httpx.get(http_health_url, timeout=2.0)
            r.raise_for_status()
        except Exception:
            return HostAppStatus(
                state=AppState.RUNNING_UNREACHABLE,
                app_name=app_name,
                message=f"{app_name} is running (PID {pid}) but HTTP API is not responding yet.",
                install_path=Path(found_path),
                pid=pid,
            )

    # --- State 4: READY ---
    return HostAppStatus(
        state=AppState.READY,
        app_name=app_name,
        message=f"{app_name} is running and ready (PID {pid}).",
        install_path=Path(found_path),
        pid=pid,
    )


def launch_app(status: HostAppStatus) -> tuple[bool, str]:
    """
    Launch the host app. Returns (success, message).
    Only valid when state is INSTALLED_STOPPED and launch_cmd is set.
    """
    if status.state == AppState.READY:
        return True, f"{status.app_name} is already running."
    if status.state == AppState.NOT_INSTALLED:
        return False, f"{status.app_name} is not installed. Download: {status.download_url}"
    if status.state == AppState.RUNNING_UNREACHABLE:
        return False, f"{status.app_name} is starting up. Wait a few seconds and retry."
    if not status.launch_cmd:
        return False, f"No launch command configured for {status.app_name}."

    try:
        subprocess.Popen(status.launch_cmd, close_fds=True)
        return True, f"Launch command sent for {status.app_name}. Allow 10-20 seconds to start."
    except Exception as e:
        return False, f"Launch failed: {e}"
```

---

## V. Per-Server Probe Configuration

Each server provides its own thin config module. Example configs:

### DaVinci Resolve
```python
from pathlib import Path

RESOLVE_PROBE_CONFIG = dict(
    app_name="DaVinci Resolve",
    process_names=["Resolve"],
    install_paths=[
        Path("C:/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe"),
        Path("C:/Program Files/DaVinci Resolve/Resolve.exe"),
    ],
    check_port=9990,
    download_url="https://www.blackmagicdesign.com/products/davinciresolve",
    launch_cmd=["C:/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe"],
)
```

### Blender
```python
BLENDER_PROBE_CONFIG = dict(
    app_name="Blender",
    process_names=["blender"],
    install_paths=[
        Path("C:/Program Files/Blender Foundation/Blender 4.3/blender.exe"),
        Path("C:/Program Files/Blender Foundation/Blender 4.2/blender.exe"),
        Path("C:/Program Files/Blender Foundation/Blender 4.1/blender.exe"),
    ],
    check_port=9876,
    download_url="https://www.blender.org/download/",
    launch_cmd=["blender"],
)
```

### OBS Studio
```python
OBS_PROBE_CONFIG = dict(
    app_name="OBS Studio",
    process_names=["obs64", "obs32", "obs"],
    install_paths=[
        Path("C:/Program Files/obs-studio/bin/64bit/obs64.exe"),
    ],
    check_port=4455,  # obs-websocket default
    download_url="https://obsproject.com/download",
    launch_cmd=["C:/Program Files/obs-studio/bin/64bit/obs64.exe"],
)
```

### Unity Editor
```python
UNITY_PROBE_CONFIG = dict(
    app_name="Unity Editor",
    process_names=["Unity"],
    install_paths=[
        # Unity Hub installs to versioned paths - glob not supported, list common ones
        Path("C:/Program Files/Unity/Hub/Editor/2022.3.0f1/Editor/Unity.exe"),
        Path("C:/Program Files/Unity/Hub/Editor/6000.0.0f1/Editor/Unity.exe"),
    ],
    check_port=6400,  # unity-mcp addon port
    download_url="https://unity.com/download",
    launch_cmd=None,  # Unity Hub required; direct launch not reliable
)
```

### Reaper
```python
REAPER_PROBE_CONFIG = dict(
    app_name="Reaper",
    process_names=["reaper"],
    install_paths=[
        Path("C:/Program Files/REAPER (x64)/reaper.exe"),
        Path("C:/Program Files/REAPER/reaper.exe"),
    ],
    http_health_url="http://localhost:8080/",  # ReaScript HTTP API
    download_url="https://www.reaper.fm/download.php",
    launch_cmd=["C:/Program Files/REAPER (x64)/reaper.exe"],
)
```

### Resonite / VRChat (Steam Games)
```python
RESONITE_PROBE_CONFIG = dict(
    app_name="Resonite",
    process_names=["Resonite"],
    install_paths=[
        Path("C:/Program Files (x86)/Steam/steamapps/common/Resonite/Resonite.exe"),
    ],
    download_url="https://store.steampowered.com/app/2519830/Resonite/",
    launch_cmd=["steam://rungameid/2519830"],  # Steam protocol launch
)
```

---

## VI. Webapp Dashboard Widget

Every MCP webapp for a host-app-dependent server MUST include a **Host App Status Card** as the first visible element on the Dashboard page.

### Visual States

```
READY
┌──────────────────────────────────────────────────────────┐
│  ● READY   DaVinci Resolve 20   PID 14823               │
│  Scripting API responding on port 9990                   │
│  [Open Resolve]  [API Docs]                             │
└──────────────────────────────────────────────────────────┘

INSTALLED_STOPPED
┌──────────────────────────────────────────────────────────┐
│  ○ STOPPED   DaVinci Resolve 20                         │
│  Installed at C:\Program Files\Blackmagic Design\...    │
│  ┌────────────────────────────────────────────────────┐  │
│  │              ▶  LAUNCH RESOLVE                     │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘

RUNNING_UNREACHABLE
┌──────────────────────────────────────────────────────────┐
│  ◌ STARTING   DaVinci Resolve 20   PID 14823            │
│  Process running, waiting for API on port 9990...       │
│  [Retry]                                                │
└──────────────────────────────────────────────────────────┘

NOT_INSTALLED
┌──────────────────────────────────────────────────────────┐
│  ✕ NOT INSTALLED   DaVinci Resolve                      │
│  Required to use this MCP server.                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │         ⬇  DOWNLOAD & INSTALL (Free)              │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### React Component Spec

The card MUST:
- Poll `get_host_app_status` every 5 seconds when state is not `ready`
- Poll every 30 seconds when state is `ready`
- Show a spinner during `running_unreachable` with auto-retry
- The launch button calls `launch_host_app` then switches to polling mode
- The download button opens `download_url` in a new tab
- Use status dot colors: green (ready), amber (unreachable), gray (stopped), red (not installed)

---

## VII. Affected Servers Checklist

| Server | Host App | Port/API | Priority |
|--------|----------|----------|----------|
| davinci-resolve-mcp | DaVinci Resolve | port 9990 | HIGH (reference impl) |
| blender-mcp | Blender | port 9876 | HIGH |
| unity3d-mcp | Unity Editor | port 6400 | HIGH |
| obs-mcp | OBS Studio | port 4455 | HIGH |
| reaper-mcp | Reaper | HTTP 8080 | MEDIUM |
| resonite-mcp | Resonite | process only | MEDIUM |
| vrchat-mcp | VRChat | process only | MEDIUM |
| vroidstudio-mcp | VRoid Studio | process only | MEDIUM |
| gimp-mcp | GIMP | Script-Fu socket | MEDIUM |
| resolume-mcp | Resolume Arena | HTTP API | MEDIUM |
| virtualdj-mcp | VirtualDJ | process only | MEDIUM |
| inkscape-mcp | Inkscape | process only | LOW |
| notepadpp-mcp | Notepad++ | process only | LOW |
| calibre-mcp | Calibre | calibredb binary | LOW |
| plex-mcp | Plex Media Server | HTTP 32400 | LOW |
| docker-mcp | Docker Desktop | socket | LOW |
| virtualization-mcp | VirtualBox | VBoxManage binary | LOW |
| qbt-mcp | qBittorrent | HTTP 8080 | LOW |
| pinokio-mcp | Pinokio | HTTP port | LOW |
| handbrake-mcp | HandBrakeCLI | binary only | LOW |

---

**Owner:** Sandra Schipal
**Last Updated:** 2026-02-26
**Reference Implementation:** davinci-resolve-mcp
