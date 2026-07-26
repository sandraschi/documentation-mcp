# .cursorrules Rule #1: Central Docs Requirement

**Policy:** ALL MCP repos MUST have Rule #1 pointing to central documentation

**Status:** Mandatory  
**Last Updated:** 2025-10-24

---

## 🎯 The Rule

**Every `.cursorrules` file in every MCP repo MUST start with:**

```markdown
## 📚 RULE #1: Check Central Documentation First

**BEFORE making any changes, ALWAYS check:**

- **Central Docs Location:** `D:\Dev\repos\mcp-central-docs\`
- **Standards:** `mcp-central-docs/STANDARDS.md` - Documentation standards
- **FastMCP Guide:** `mcp-central-docs/fastmcp/migration-guide.md` - Framework 3.1 standards
- **MCPB Packaging:** `mcp-central-docs/MCPB_PACKAGING_STANDARDS.md` - Package standards
- **Patterns:** `mcp-central-docs/patterns/` - Design patterns (portmanteau, etc.)
- **Templates:** `mcp-central-docs/templates/` - Documentation templates
- **This Repo Status:** `mcp-central-docs/repos/{repo-name}/STATUS.md` - Improvement tracking

**Why central docs?** Single source of truth for all MCP projects. Prevents duplication and ensures consistency.
```

---

## 🤔 Why This Matters

### Benefits of Rule #1

1. **Single Source of Truth** - No conflicting standards across repos
2. **Immediate Context** - Cursor/AI knows where standards are from startup
3. **Consistency** - All repos follow same patterns
4. **Discoverability** - New contributors know where to look
5. **Maintainability** - Update standards once, applies to all
6. **Scalability** - Add 100 repos, same standards reference

### Without Rule #1

❌ **Problems:**
- Each repo has different standards
- Standards conflict and diverge
- Updates require changing 15+ repos
- New contributors confused
- AI doesn't know where standards are
- Duplication and inconsistency

### With Rule #1

✅ **Solutions:**
- Hub-and-spoke architecture
- Update central docs once
- All repos stay in sync
- Clear authority on standards
- AI checks standards first
- Consistency across all repos

---

## 📋 Implementation Checklist

### For New Repos

- [ ] Copy `.cursorrules.template` to repo
- [ ] Customize placeholders (repo name, status, etc.)
- [ ] Verify Rule #1 is at the top
- [ ] Verify all paths point to `mcp-central-docs/`
- [ ] Test: Open in Cursor and verify AI sees Rule #1

### For Existing Repos

- [ ] Check if `.cursorrules` exists
- [ ] Check if Rule #1 exists
- [ ] Check if Rule #1 is FIRST (not buried)
- [ ] Update to match template if needed
- [ ] Verify paths are correct
- [ ] Test: Open in Cursor and verify

### Verification Command

```powershell
# Check if Rule #1 exists in repo
Select-String -Path .cursorrules -Pattern "RULE #1" -CaseSensitive
```

**Expected:** Should find "RULE #1: Check Central Documentation First"

---

## 🏗️ Architecture: Hub and Spoke

```
                    mcp-central-docs/
                    (Hub - Single Source of Truth)
                            |
         +------------------+------------------+
         |                  |                  |
    repo-1/           repo-2/           repo-3/
  .cursorrules      .cursorrules      .cursorrules
  Rule #1 ──────▶  Rule #1 ──────▶  Rule #1 ──────▶
  points to hub    points to hub    points to hub
```

### Flow

1. **Developer/AI opens repo** in Cursor
2. **Cursor reads `.cursorrules`**
3. **Rule #1 says:** "Check central docs first!"
4. **AI/Developer navigates to** `mcp-central-docs/`
5. **Gets standards, templates, patterns**
6. **Applies consistently** across all repos

---

## 📝 Template

See: `templates/.cursorrules.template` for the complete template with Rule #1.

**Quick copy:**

```bash
cp D:\Dev\repos\mcp-central-docs\templates\.cursorrules.template .cursorrules
```

Then customize placeholders.

---

## 🔧 Maintenance

### When Central Docs Location Changes

**If `mcp-central-docs/` moves:**

1. Update path in `.cursorrules.template`
2. Run batch update across all repos:

```powershell
# PowerShell script to update all repos
$repos = @(
    "advanced-memory-mcp",
    "database-operations-mcp",
    # ... all 15 repos
)

foreach ($repo in $repos) {
    $path = "D:\Dev\repos\$repo\.cursorrules"
    if (Test-Path $path) {
        (Get-Content $path) -replace 'D:\\Dev\\repos\\mcp-central-docs', 'NEW_PATH' | 
            Set-Content $path
        Write-Host "Updated: $repo"
    }
}
```

### Monthly Verification

**Check all repos have Rule #1:**

```powershell
# Verify script
$repos = Get-ChildItem -Path "D:\Dev\repos" -Directory
foreach ($repo in $repos) {
    $cursorrules = Join-Path $repo.FullName ".cursorrules"
    if (Test-Path $cursorrules) {
        $hasRule1 = Select-String -Path $cursorrules -Pattern "RULE #1" -Quiet
        if (-not $hasRule1) {
            Write-Warning "Missing Rule #1: $($repo.Name)"
        }
    } else {
        Write-Warning "Missing .cursorrules: $($repo.Name)"
    }
}
```

---

## 🎯 Success Criteria

### A repo is compliant when:

- ✅ `.cursorrules` file exists
- ✅ Rule #1 is present
- ✅ Rule #1 is FIRST (before other rules)
- ✅ Points to `mcp-central-docs/`
- ✅ Lists key documents (STANDARDS, FASTMCP, MCPB, patterns, templates)
- ✅ Includes repo-specific STATUS.md link
- ✅ Explains WHY central docs matter

### Verification

```bash
# Open repo in Cursor
# Ask: "What standards should I follow?"
# AI should reference mcp-central-docs/ immediately
```

**Expected response:** AI mentions checking central docs first.

---

## 📚 Examples

### Good Example (advanced-memory-mcp)

```markdown
# advanced-memory-mcp Cursor Rules

## 📚 RULE #1: Check Central Documentation First

**BEFORE making any changes, ALWAYS check:**

- **Central Docs Location:** `D:\Dev\repos\mcp-central-docs\`
- **Standards:** `mcp-central-docs/STANDARDS.md` - Documentation standards
...

**Why central docs?** Single source of truth for all MCP projects.

---

## 🎯 Triple Initiatives (Active)
...
```

**✅ Good because:**
- Rule #1 is FIRST
- Clear paths to central docs
- Explains WHY
- Easy to find and read

---

### Bad Example

```markdown
# my-repo Cursor Rules

## Code Standards

Use ruff for linting...

## Testing

Use pytest...

## Central Docs

Check mcp-central-docs sometimes.
```

**❌ Bad because:**
- No Rule #1
- Central docs buried at bottom
- No clear paths
- No explanation of importance
- Easy to miss

---

## 🚀 Rollout Plan

### Phase 1: Template (Complete)
- ✅ Created `.cursorrules.template` with Rule #1
- ✅ Updated advanced-memory-mcp as reference

### Phase 2: Batch Update (Next)
- [ ] Update all 15 tracked repos
- [ ] Verify each has Rule #1
- [ ] Test with Cursor

### Phase 3: Enforcement (Ongoing)
- [ ] Add to repo checklist
- [ ] Verify in audits
- [ ] Update as needed

---

## 💡 Tips

### For AI Assistants

"When opening a new repo, immediately check if `.cursorrules` exists and if Rule #1 points to central docs. If not, add it!"

### For Developers

"Before starting work, verify `.cursorrules` has Rule #1. If unsure about standards, follow the links in Rule #1."

### For Reviews

"Check PRs include `.cursorrules` updates when standards change."

---

## ❓ FAQ

**Q: Why Rule #1 and not Rule #2?**  
A: First rule has highest priority. Cursor reads top-to-bottom.

**Q: What if my repo has special standards?**  
A: Add after Rule #1. Central docs come first, then repo-specific.

**Q: Do I update all repos when central docs change?**  
A: No! Rule #1 just points to central docs. Update central docs once.

**Q: What if central docs path changes?**  
A: Run batch update script to fix paths in all repos.

**Q: Can I skip Rule #1 for simple repos?**  
A: No. ALL repos must have Rule #1. Consistency is key.

---

**Policy Status:** Mandatory  
**Compliance:** Required for all MCP repos  
**Enforcement:** Via audits and reviews  
**Last Updated:** 2025-10-24
