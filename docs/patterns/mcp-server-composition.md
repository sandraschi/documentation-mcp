# MCP Server Composition Pattern

## Overview

FastMCP 3.1.1+.1 introduced server composition via `mount()` and `import_server()`, enabling multiple MCP servers to be combined into unified orchestrators.

## Composition Methods

### Method 1: `mount()` - Live Linking (Recommended)

```python
from fastmcp import FastMCP

main = FastMCP(name="Orchestrator")
sub = FastMCP(name="SubServer")

@sub.tool
def hello():
    return "hi"

# Live link - changes to sub are reflected in main
main.mount(sub, prefix="sub", as_proxy=True)

# Tool available as: sub_hello
```

### Method 2: `import_server()` - Static Copy

```python
# One-time copy of components
main.import_server(sub, prefix="sub")

# Changes to sub after import NOT reflected
```

### Mounting Modes

| Mode | Syntax | Behavior |
|------|--------|----------|
| Direct | `mount(server)` | Static copy, fast startup |
| Proxy | `mount(server, as_proxy=True)` | Live link, dynamic updates |
| No Prefix | `mount(server)` | Tools accessible without prefix |

## Sandra's MCP Ecosystem

### Available Servers (40+)

#### VR/Avatar Domain
- `unity3d-mcp` - Unity automation
- `avatarmcp` - VRM runtime control
- `vroidstudio-mcp` - VRM creation
- `blender-mcp` - 3D modeling
- `oscmcp` - OSC/MIDI protocol

#### Smart Home Domain
- `devices-mcp` - Lights, cameras, plugs, kitchen
- `nest-protect-mcp` - Smoke/CO detection
- `ring-mcp` - Doorbell/security

#### Media Production Domain
- `davinci-resolve-mcp` - Video editing
- `reaper-mcp` - Audio DAW
- `gimp-mcp` - Image editing
- `handbrakemcp` - Video encoding
- `plexmcp` - Media server
- `immichmcp` - Photo management
- `obsmcp` - Streaming

#### System Administration Domain
- `filesystem-mcp` - File operations
- `windows-operations-mcp` - Windows automation
- `pywinauto-mcp` - GUI automation
- `dockermcp` - Containers
- `vboxmcp` - Virtual machines
- `tailscale-mcp` - Networking
- `hasleo-backup-mcp` - Backups
- `system-admin-mcp` - System utilities

#### Knowledge Management Domain
- `advanced-memory-mcp` - Primary PKM
- `obsidianmcp` - Obsidian vaults
- `notion-mcp` - Notion databases
- `onenote-mcp` - OneNote notebooks
- `bookmarks-mcp` - Browser bookmarks
- `calibremcp` - E-book library

#### Music Domain
- `reaper-mcp` - DAW
- `virtualdj-mcp` - Live DJing
- `suno-mcp` - AI music generation

---

## Orchestrator Architectures

### 1. VR Production Pipeline

```python
from fastmcp import FastMCP, Client

vr_production = FastMCP(name="VR-Production-Pipeline")

# Mount servers
vr_production.mount(vroidstudio_mcp, prefix="vroid", as_proxy=True)
vr_production.mount(blender_mcp, prefix="blender", as_proxy=True)
vr_production.mount(unity3d_mcp, prefix="unity", as_proxy=True)
vr_production.mount(avatar_mcp, prefix="avatar", as_proxy=True)
vr_production.mount(osc_mcp, prefix="osc", as_proxy=True)
vr_production.mount(obs_mcp, prefix="obs", as_proxy=True)

# Cross-server workflow
@vr_production.tool
async def full_vtuber_setup(
    vrm_path: str,
    stream_scene: str,
) -> dict:
    """Complete VTuber setup from VRM to streaming."""
    async with Client(vr_production) as client:
        # Load avatar runtime
        await client.call_tool("avatar_avatar_load", 
            params={"avatar_id": vrm_path})
        
        # Setup emotion state machine
        await client.call_tool("avatar_emotion_state_machine",
            params={"avatar_id": "main", "states": DEFAULT_EMOTIONS})
        
        # Configure OBS
        await client.call_tool("obs_switch_scene",
            params={"scene": stream_scene})
        
        # Start OSC listener for face tracking
        await client.call_tool("osc_start_osc_listener",
            params={"port": 9001})
        
        return {"status": "ready", "streaming": True}
```

### 2. Smart Home Hub

```python
smart_home = FastMCP(name="Smart-Home-Hub")

smart_home.mount(tapo_mcp, prefix="tapo", as_proxy=True)
smart_home.mount(nest_mcp, prefix="nest", as_proxy=True)
smart_home.mount(ring_mcp, prefix="ring", as_proxy=True)
smart_home.mount(osc_mcp, prefix="osc", as_proxy=True)

@smart_home.tool
async def doorbell_response():
    """Full response when doorbell rings."""
    async with Client(smart_home) as client:
        # Capture front camera
        image = await client.call_tool("tapo_media_management",
            action="capture", camera_name="Front Door")
        
        # Turn on porch lights
        await client.call_tool("tapo_lighting_management",
            action="control_light", light_id="porch", on=True)
        
        # Send notification via OSC
        await client.call_tool("osc_send_osc_message",
            host="127.0.0.1", port=9000,
            address="/notification/doorbell",
            values=["Someone at door"])
        
        return {"status": "responded", "image": image}
```

### 3. Knowledge Management Hub

```python
knowledge = FastMCP(name="Knowledge-Hub")

knowledge.mount(advanced_memory_mcp, prefix="adn", as_proxy=True)
knowledge.mount(obsidian_mcp, prefix="obsidian", as_proxy=True)
knowledge.mount(notion_mcp, prefix="notion", as_proxy=True)
knowledge.mount(onenote_mcp, prefix="onenote", as_proxy=True)
knowledge.mount(calibre_mcp, prefix="calibre", as_proxy=True)

@knowledge.tool
async def universal_search(query: str) -> dict:
    """Search across all knowledge sources."""
    async with Client(knowledge) as client:
        results = {}
        
        # Search all sources in parallel
        tasks = [
            client.call_tool("adn_search_notes", query=query),
            client.call_tool("obsidian_search", query=query),
            client.call_tool("notion_search", query=query),
            client.call_tool("calibre_search_books", query=query),
        ]
        
        search_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "query": query,
            "adn": search_results[0],
            "obsidian": search_results[1],
            "notion": search_results[2],
            "calibre": search_results[3],
        }
```

### 4. System Administration Hub

```python
sysadmin = FastMCP(name="SysAdmin-Hub")

sysadmin.mount(filesystem_mcp, prefix="fs", as_proxy=True)
sysadmin.mount(windows_ops_mcp, prefix="win", as_proxy=True)
sysadmin.mount(pywinauto_mcp, prefix="gui", as_proxy=True)
sysadmin.mount(docker_mcp, prefix="docker", as_proxy=True)
sysadmin.mount(vbox_mcp, prefix="vbox", as_proxy=True)
sysadmin.mount(tailscale_mcp, prefix="tailscale", as_proxy=True)
sysadmin.mount(backup_mcp, prefix="backup", as_proxy=True)

@sysadmin.tool
async def dev_environment_setup(project_name: str) -> dict:
    """Setup complete development environment."""
    async with Client(sysadmin) as client:
        # Create workspace
        await client.call_tool("fs_create_directory",
            path=f"D:/Dev/{project_name}")
        
        # Start Docker services
        await client.call_tool("docker_compose_up",
            compose_file=f"D:/Dev/{project_name}/docker-compose.yml")
        
        # Connect to Tailscale network
        await client.call_tool("tailscale_connect")
        
        return {"status": "ready", "project": project_name}
```

### 5. Media Production Suite

```python
media = FastMCP(name="Media-Production-Suite")

media.mount(davinci_mcp, prefix="davinci", as_proxy=True)
media.mount(reaper_mcp, prefix="reaper", as_proxy=True)
media.mount(gimp_mcp, prefix="gimp", as_proxy=True)
media.mount(handbrake_mcp, prefix="handbrake", as_proxy=True)
media.mount(plex_mcp, prefix="plex", as_proxy=True)

@media.tool
async def video_production_pipeline(
    footage_path: str,
    output_name: str,
) -> dict:
    """Complete video production pipeline."""
    async with Client(media) as client:
        # Import and edit
        await client.call_tool("davinci_import_media", path=footage_path)
        
        # Export from DaVinci
        export_path = await client.call_tool("davinci_render",
            output=f"D:/Exports/{output_name}_raw.mov")
        
        # Encode with HandBrake
        final_path = await client.call_tool("handbrake_encode",
            input=export_path,
            output=f"D:/Exports/{output_name}.mp4",
            preset="HQ 1080p30")
        
        # Add to Plex
        await client.call_tool("plex_add_to_library",
            file=final_path, library="Videos")
        
        return {"status": "complete", "output": final_path}
```

### 6. Music & DJ Suite

```python
music = FastMCP(name="Music-DJ-Suite")

music.mount(reaper_mcp, prefix="reaper", as_proxy=True)
music.mount(virtualdj_mcp, prefix="vdj", as_proxy=True)
music.mount(suno_mcp, prefix="suno", as_proxy=True)
music.mount(osc_mcp, prefix="osc", as_proxy=True)

@music.tool
async def ai_assisted_production(prompt: str) -> dict:
    """AI-assisted music production."""
    async with Client(music) as client:
        # Generate with Suno
        generated = await client.call_tool("suno_generate",
            prompt=prompt, duration=30)
        
        # Import to Reaper
        await client.call_tool("reaper_import_audio",
            file=generated["audio_path"])
        
        # Add effects
        await client.call_tool("reaper_add_effect",
            track=0, effect="ReaEQ")
        
        return {"status": "ready", "project": generated}
```

---

## Middleware Patterns

### Authentication Middleware

```python
from fastmcp.server.middleware import AuthenticationMiddleware

orchestrator = FastMCP(name="Secure-Orchestrator")
orchestrator.add_middleware(AuthenticationMiddleware("token"))

# All mounted servers inherit auth requirement
orchestrator.mount(server_a, prefix="a")
orchestrator.mount(server_b, prefix="b")
```

### Logging Middleware

```python
from fastmcp.server.middleware import LoggingMiddleware

# Parent logging applies to all
orchestrator.add_middleware(LoggingMiddleware())

# Child can have additional logging
child = FastMCP(name="Child")
child.add_middleware(LoggingMiddleware(level="DEBUG"))
```

### Tag-Based Filtering

```python
# Only expose production-tagged tools
prod_orchestrator = FastMCP(
    name="Production",
    include_tags={"production", "stable"}
)

# Development tools automatically filtered
prod_orchestrator.mount(dev_server, prefix="dev")
```

---

## Best Practices

### 1. Prefix Naming Convention

```python
# Use short, descriptive prefixes
orchestrator.mount(unity3d_mcp, prefix="unity")  # Good
orchestrator.mount(unity3d_mcp, prefix="unity3d_mcp")  # Too long
```

### 2. Error Handling

```python
@orchestrator.tool
async def safe_workflow():
    async with Client(orchestrator) as client:
        try:
            result = await client.call_tool("sub_risky_tool")
        except Exception as e:
            return {"status": "error", "message": str(e)}
```

### 3. Parallel Execution

```python
@orchestrator.tool
async def parallel_search(query: str):
    async with Client(orchestrator) as client:
        # Execute searches in parallel
        tasks = [
            client.call_tool("a_search", query=query),
            client.call_tool("b_search", query=query),
            client.call_tool("c_search", query=query),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {"results": results}
```

---

## Implementation Checklist

- [ ] Create `vr-production-mcp` orchestrator
- [ ] Create `smart-home-mcp` orchestrator
- [ ] Create `knowledge-mcp` orchestrator
- [ ] Create `sysadmin-mcp` orchestrator
- [ ] Create `media-production-mcp` orchestrator
- [ ] Create `music-mcp` orchestrator
- [ ] Add middleware (auth, logging)
- [ ] Implement cross-server workflows
- [ ] Add tag-based filtering
- [ ] Document all composed tools

---

## References

- [FastMCP Server Composition](https://gofastmcp.com/servers/server)
- [FastMCP Middleware](https://fastmcp.wiki/en/servers/middleware)
- [[MCP Server Ecosystem - Complete Orchestrator Architecture]]


