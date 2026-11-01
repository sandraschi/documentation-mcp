# Claude Skills Plugin Installation Guide

**For Multi-Skill Plugins** (cooking-skills.zip with 30 skills, etc.)

## Recommended: Manual Installation (30 seconds)

**Most Reliable Method**:

1. Locate your plugin zip file (e.g., `cooking-skills.zip`)
2. Open Claude Desktop
3. Click Settings (gear icon)
4. Navigate to Skills or Extensions
5. **Drag and drop** the .zip file into the upload zone
6. Wait for processing
7. Verify all skills appear in the list

**Time**: <30 seconds  
**Reliability**: 100%  
**Maintenance**: Zero

## Experimental: Automated Installation (Fragile!)

⚠️ **USE WITH EXTREME CAUTION** ⚠️

**Requirements**:
```bash
pip install pywinauto pillow pyautogui
```

**Usage**:
```bash
# Test mode (safe - just checks if it can find Claude Desktop)
python install-plugin-automated.py --test cooking-skills.zip

# Dry run (shows what would happen)
python install-plugin-automated.py --dry-run cooking-skills.zip

# Actual installation attempt (FRAGILE!)
python install-plugin-automated.py cooking-skills.zip
```

### Fragility Warnings

**This script WILL break if**:
- ❌ Claude Desktop UI changes
- ❌ Window positions change  
- ❌ Claude Desktop updates
- ❌ Screen resolution different
- ❌ UI element IDs change

**Success rate**: ~30-50% (very fragile!)

**When it fails**: Script tells you to install manually

### When Automation Makes Sense

**✅ Good use case**:
- cooking-skills.zip (30 skills) = 1 automated installation
- developer-tools.zip (50 skills) = 1 automated installation
- Multi-skill plugins = ONE fragile operation

**❌ Bad use case**:
- Installing 100 individual skill zips one by one
- Better to package into plugins first!

### Fallback Process

If automation fails (likely):

```
⚠️  AUTOMATION FAILED - MANUAL FALLBACK:

Drag this file: D:\path\to\cooking-skills.zip
Drop it in Claude Desktop → Settings → Skills
```

The script always provides manual fallback instructions.

## Why This Limitation Exists

**Claude Desktop Design**:
- GUI-first application
- No CLI interface
- No API for Skills installation
- Drag-and-drop UX paradigm

**Anthropic hasn't provided**:
- ❌ `claude-desktop skills install cooking-skills.zip` (CLI)
- ❌ API endpoint for installation
- ❌ Skills directory watching (~/.claude-skills/ auto-load)

## Comparison to Other Installation Methods

| Method | Automation | Reliability | Use Case |
|--------|------------|-------------|----------|
| **MCP Deeplinks** | ✅ Full | 100% | Cursor, VS Code |
| **Manual Skills Install** | ❌ None | 100% | Claude Desktop |
| **Automated Skills** | ⚠️ Fragile | 30-50% | Batch multi-skill plugins |
| **MCPB** | ❌ Drag-drop | 100% | Claude Desktop extensions |

## Best Practices

### 1. Package Multiple Skills Together

**Don't do this**:
```
italian-cooking.zip
french-cooking.zip
japanese-cooking.zip
... × 30 files
= 30 manual installations
```

**Do this instead**:
```
cooking-skills.zip
  └── Contains 30 skills
= 1 manual installation
```

### 2. Use Automation Sparingly

**When to automate**:
- Testing new plugin packages
- Installing large multi-skill plugins (50+ skills)
- CI/CD testing scenarios

**When to skip automation**:
- Single skill installs (manual is faster!)
- First-time installations (manual to learn)
- Production deployments (manual is safer)

### 3. Always Have Manual Fallback

The automation script ALWAYS provides manual instructions:
```
If automation fails:
Drag D:\path\to\plugin.zip into Claude Desktop → Settings → Skills
```

## Package First, Automate Second

**Workflow**:

```powershell
# 1. Create multi-skill plugin (100% reliable)
.\package-plugin.ps1 `
    -PluginName "cooking-skills" `
    -SkillPaths @(
        "italian-cooking",
        "french-cooking",
        "japanese-cooking"
    ) `
    -Description "30 regional cooking skills"

# Result: cooking-skills.zip with 30 skills

# 2. Install (choose one):

# Option A: Manual (recommended - 30 seconds, 100% reliable)
# → Open Claude Desktop → Settings → Skills → Drag zip

# Option B: Automated (experimental - fragile but worth trying)
python install-plugin-automated.py cooking-skills.zip
```

**Result**: Either way, ONE operation installs 30 skills!

## Future Hope

**What we hope Anthropic adds**:

```bash
# CLI installation (would be amazing!)
claude-desktop skills install cooking-skills.zip

# Or directory watching
mkdir ~/claude-skills
cp cooking-skills.zip ~/claude-skills/
# Claude auto-installs on startup

# Or API endpoint
curl -X POST http://localhost:9222/skills/install \
  -F "file=@cooking-skills.zip"
```

**Status**: None of these exist yet  
**Hope**: Anthropic adds them eventually

## Error Handling

### Common Failures

**"Claude Desktop not found"**:
- Make sure Claude Desktop is running
- Check window title matches expected patterns

**"Could not locate drop zone"**:
- UI structure changed
- Element IDs changed
- Fallback to manual

**"Automation failed"**:
- Most common outcome
- Always provides manual instructions

### Success Rate

**Realistic expectations**:
- First try: 30% success
- After tweaking: 50% success
- After UI updates: 0% (breaks completely)

**Manual success rate**: 100%

## Conclusion

**Automation exists** but is fragile  
**Use case**: Multi-skill plugins only (e.g., 100 skills in one zip)  
**Reliability**: Low (~30-50%)  
**Fallback**: Always manual instructions provided  
**Recommendation**: Package into plugins, install manually (fastest!)

**The Math**:
- Manual: 30 seconds × 1 plugin = 30 seconds
- Automated: 2 minutes + 50% failure rate = probably slower
- **Winner**: Manual installation is actually faster!

**But**: If automation works, it's satisfying to watch! 🤖

---

**Status**: Experimental automation available  
**Warnings**: Comprehensive fragility warnings included  
**Recommendation**: Use multi-skill plugins + manual installation  
**Reality**: GUI automation rarely worth the complexity for this use case

## 🦾 Installing Skills in Agentic IDEs

Modern IDEs offer streamlined ways to load skills directly into your project context.

### 1. Cursor (Local Project)
1. Copy the skill folder (e.g., `react-expert/`) into `.cursor/skills/` in your project root.
2. If `.cursor/skills/` doesn't exist, create it.
3. Restart Cursor or refresh the index.
4. **Usage**: Cursor will automatically pick up the instructions in `SKILL.md` when relevant to your active task.

### 2. Windsurf (Local Project)
1. Place the skill folder in `.windsurf/skills/`.
2. Ensure the `SKILL.md` is valid.
3. Windsurf's "Flow" mode will automatically integrate these instructions.

### 3. Antigravity (Universal)
1. Use the `adn_skills` tool:
   ```python
   # Import a skill folder
   adn_skills("create", name="new-skill", content="...")
   ```
2. Or place folders in the designated `.agents/skills/` path in your workspace.

### 4. Zed
1. Add the path to your skills library in the Zed settings JSON.
2. Reference specific `SKILL.md` files in your prompt context as needed.

---

**Last Updated**: 2026-01-27

